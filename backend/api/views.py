from django.shortcuts import render
from rest_framework.response import Response
from .funcs import leer_chat_whatsapp
from .models import Chat
from rest_framework.decorators import api_view
from .serializers import ChatSerializer

# Create your views here.


@api_view(["GET", "POST"])
def GetChat(request, pk):
    if request.method == "GET":
        chat = Chat.objects.get(id=pk)
        # print(chat.File, type(chat.File))
        # print(archivo_path)
        """serializer = ChatSerializer(chat, many=False)
        filePath = "../backend" + serializer.data["File"]
        print(serializer.data["File"], type(serializer.data["File"]))
        df = leer_chat_whatsapp(filePath)
        print(df)"""

        json_data = chat.ChatToJson
        # print(json_data)
        return Response(json_data)


@api_view(["GET", "POST"])
def Chats(request):
    if request.method == "GET":
        chats = Chat.objects.all().filter(User=request.user)
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        pass
