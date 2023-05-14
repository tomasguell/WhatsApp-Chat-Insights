from django.urls import path
from . import views

urlpatterns = [
    path("chats/<str:pk>/content", views.ChatContent, name="chatContent"),
    path("chats/<str:pk>/stats", views.ChatStats, name="chatStats"),
    path("chats", views.Chats, name="chats"),
    path("sender/<str:pks>/content", views.SenderContent, name="senderContent"),
    path(
        "sender/<str:pks>/content/<str:pkc>",
        views.SenderContentChat,
        name="senderContentChat",  # pks (s de sender) (c de chat)
    ),
]
