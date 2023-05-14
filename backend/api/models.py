from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .funcs import leer_chat_whatsapp, obtener_remitentes
import json
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.
class Chat(models.Model):
    Title = models.CharField(max_length=50)
    File = models.FileField(upload_to="utils/files")
    User = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def ChatToJson(self):
        from .serializers import ChatSerializer

        serializer = ChatSerializer(self, many=False)
        filePath = "../backend" + serializer.data["File"]
        df = leer_chat_whatsapp(filePath)

        json_data = df.to_json(orient="records")
        return json_data

    @property
    def ChatToDf(self):
        from .serializers import ChatSerializer

        serializer = ChatSerializer(self, many=False)
        filePath = "../backend" + serializer.data["File"]
        df = leer_chat_whatsapp(filePath)

        return df

    def __str__(self):
        return self.Title


class Sender(models.Model):
    Name = models.CharField(max_length=30)
    Chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Name} - {self.Chat.Title}"


class Message(models.Model):
    Date = models.DateField()
    Time = models.TimeField()
    Sender = models.ForeignKey(Sender, on_delete=models.CASCADE)
    Message = models.TextField(max_length=1000)
    Chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Sender} - {self.Date} {self.Time}"


@receiver(post_save, sender=Chat)
def populate_senders(sender, instance, created, **kwargs):
    if created:
        df_chat = instance.ChatToDf
        remitentes_unicos = obtener_remitentes(df_chat)

        sender_objects = []
        for remitente in remitentes_unicos:
            sender = Sender(Name=remitente, Chat=instance)
            sender_objects.append(sender)

        Sender.objects.bulk_create(sender_objects)


@receiver(post_save, sender=Chat)
def populate_messages(sender, instance, created, **kwargs):
    if created:
        json_data = instance.ChatToJson
        messages = json.loads(json_data)
        message_objects = []

        for message_data in messages:
            sender_name = message_data["Remitente"]
            sender, created = Sender.objects.get_or_create(
                Name=sender_name, Chat=instance
            )

            message = Message(
                Date=message_data["Fecha"],
                Time=message_data["Hora"],
                Sender=sender,
                Message=message_data["Mensaje"],
                Chat=instance,
            )
            message_objects.append(message)

        Message.objects.bulk_create(message_objects)
