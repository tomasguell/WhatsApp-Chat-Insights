from django.shortcuts import render
from rest_framework.response import Response
from .funcs import leer_chat_whatsapp
from .models import Chat, Message, Sender
from rest_framework.decorators import api_view
from .serializers import ChatSerializer, MessageSerializer

# Create your views here.


@api_view(["GET", "POST"])
def ChatContent(request, pk):
    if request.method == "GET":
        messages = Message.objects.all().filter(Chat__id=pk)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


@api_view(["GET", "POST"])
def ChatStats(request, pk):
    if request.method == "GET":
        messages = Message.objects.all().filter(Chat__id=pk)
        message_count = messages.count()
        response_data = {"message_count": message_count}
        # serializer = MessageSerializer(messages, many=True)
        return Response(
            response_data
        )  # Quiero que returnee el numero de mensajes del chat


@api_view(["GET", "POST"])
def SenderContent(request, pks):  # pks (s de sender)
    if request.method == "GET":
        messages = Message.objects.all().filter(Sender__id=pks)

        serializer = MessageSerializer(messages, many=True)
        data = serializer.data
        response_data = {"sender": Sender.objects.get(id=pks).Name, "content": data}

        return Response(
            response_data
        )  # Quiero que returnee el numero de mensajes del chat


@api_view(["GET", "POST"])
def SenderContentChat(request, pks, pkc):  # pks (s de sender)
    if request.method == "GET":
        messages = Message.objects.all().filter(Sender__id=pks, Chat__id=pkc)

        serializer = MessageSerializer(messages, many=True)
        """  data = serializer.data
        response_data = {
            "sender": Sender.objects.get(id=pks).Name,
            "chat": Chat.objects.get(id=pkc).Title,
            "content": data,
        }"""

        return Response(serializer.data)


@api_view(["GET", "POST"])
def Chats(request):
    if request.method == "GET":
        chats = Chat.objects.all().filter(User=request.user)
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        pass
