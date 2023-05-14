from django.shortcuts import render
from rest_framework.response import Response
from .funcs import leer_chat_whatsapp, enumerateSenders
from .models import Chat, Message, Sender
from rest_framework.decorators import api_view
from .serializers import ChatSerializer, MessageSerializer, ChatSerializerReducido
from rest_framework import status
from django.db.models import Count

# Create your views here.


@api_view(["GET", "POST"])
def ChatContent(request, pk):
    if request.method == "GET":
        messages = Message.objects.all().filter(Chat__id=pk)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def ChatStats(request, pk):
    if request.method == "GET":
        # Obtener el chat
        try:
            chat = Chat.objects.get(id=pk)
        except Chat.DoesNotExist:
            return Response(
                {"error": "Chat not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Número total de mensajes
        total_messages = Message.objects.filter(Chat=chat).count()

        # Mensajes por día
        messages_by_day = (
            Message.objects.filter(Chat=chat).values("Date").annotate(count=Count("id"))
        )

        # Participantes activos
        active_participants = Sender.objects.filter(message__Chat=chat).distinct()

        # Número de mensajes por participante
        participant_message_counts = {}
        for participant in active_participants:
            participant_message_counts[participant.Name] = Message.objects.filter(
                Chat=chat, Sender=participant
            ).count()
            print(participant.Name)

        # sort de el dict
        sorted_participant_message_counts = sorted(
            participant_message_counts.items(), key=lambda x: x[1], reverse=True
        )

        # Preparar los datos de respuesta
        response_data = {
            "chat_name": chat.Title,
            "total_messages": total_messages,
            "messages_by_day": messages_by_day,
            "active_participants": list(active_participants.values("id", "Name")),
            "participant_message_counts": sorted_participant_message_counts,
        }

        return Response(response_data)


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
def SenderStats(request, pks):  # pks (s de sender)
    if request.method == "GET":
        messages = Message.objects.all().filter(Sender__id=pks)
        message_count = messages.count()
        message_history = messages.values("Date").annotate(count=Count("id"))
        serializer = MessageSerializer(messages, many=True)

        response_data = {
            "sender": Sender.objects.get(id=pks).Name,
            "message_count": message_count,
            "message_history": message_history,
        }

        return Response(
            response_data
        )  # Quiero que returnee el numero de mensajes del chat


@api_view(["GET", "POST"])
def SenderStatsChat(request, pks, pkc):  # pks (s de sender)
    if request.method == "GET":
        messages = Message.objects.all().filter(Sender__id=pks, Chat__id=pkc)
        message_count = messages.count()
        message_history = messages.values("Date").annotate(count=Count("id"))
        serializer = MessageSerializer(messages, many=True)

        response_data = {
            "chat": Chat.objects.get(id=pkc).Title,
            "sender": Sender.objects.get(id=pks).Name,
            "message_count": message_count,
            "message_history": message_history,
        }
        enumerateSenders()
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
