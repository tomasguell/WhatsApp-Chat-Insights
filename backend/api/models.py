from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .funcs import leer_chat_whatsapp
import json
from datetime import datetime


# Create your models here.
class Chat(models.Model):
    Title = models.CharField(max_length=50)
    File = models.FileField(upload_to="utils/files")

    @property
    def ChatToJson(self):
        from .serializers import ChatSerializer

        serializer = ChatSerializer(self, many=False)
        filePath = "../backend" + serializer.data["File"]
        df = leer_chat_whatsapp(filePath)
        json_data = df.to_json(orient="records")
        return json_data


class Message(models.Model):
    Date = models.DateField()
    Time = models.TimeField()
    Sender = models.CharField(max_length=50)
    Message = models.TextField(max_length=1000)
    Chat = models.ForeignKey(Chat, on_delete=models.CASCADE)


@receiver(post_save, sender=Chat)
def populate_messages(sender, instance, created, **kwargs):
    if created:
        json_data = instance.ChatToJson
        messages = json.loads(json_data)
        message_objects = []

        for message_data in messages:
            message = Message(
                Date=message_data["Fecha"],
                Time=message_data["Hora"],
                Sender=message_data["Remitente"],
                Message=message_data["Mensaje"],
                Chat=instance,
            )
            message_objects.append(message)

        Message.objects.bulk_create(message_objects)
