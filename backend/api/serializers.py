from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Chat, Message


class ChatSerializer(ModelSerializer):
    participantes = SerializerMethodField()

    class Meta:
        model = Chat
        fields = "__all__"

    def get_participantes(self, chat):
        senders = (
            chat.message_set.all().values_list("Sender__Name", flat=True).distinct()
        )
        return list(senders)


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
