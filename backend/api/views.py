from django.shortcuts import render
from rest_framework.response import Response
from .funcs import leer_chat_whatsapp
from .models import Chat
from rest_framework.decorators import api_view
from .serializers import ChatSerializer

# Create your views here.


@api_view(["GET"])
def getChat(request, pk):
    chat = Chat.objects.get(id=pk)
    # print(chat.File, type(chat.File))
    # print(archivo_path)
    serializer = ChatSerializer(chat, many=False)
    filePath = "../backend" + serializer.data["File"]
    print(serializer.data["File"], type(serializer.data["File"]))
    df = leer_chat_whatsapp(filePath)
    print(df)

    # json_data = chat.ChatToJson
    # print(json_data)
    return Response(df)
