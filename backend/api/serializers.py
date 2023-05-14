from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Chat, Message, Sender


class SenderSerializer(ModelSerializer):
    class Meta:
        model = Sender
        fields = ("id", "Name")


class ChatSerializer(ModelSerializer):
    participantes = SerializerMethodField()

    class Meta:
        model = Chat
        fields = ("id", "Title", "participantes")

    def get_participantes(self, chat):
        senders = (
            chat.message_set.all().values_list("Sender__Name", flat=True).distinct()
        )
        return list(senders)


class SenderSerializerReducido(ModelSerializer):
    class Meta:
        model = Sender
        fields = ("Name",)


class ChatSerializerReducido(ModelSerializer):
    class Meta:
        model = Chat
        fields = ("Title",)


class MessageSerializer(ModelSerializer):
    Sender = SenderSerializerReducido()
    Chat = ChatSerializerReducido()

    class Meta:
        model = Message
        fields = "__all__"
