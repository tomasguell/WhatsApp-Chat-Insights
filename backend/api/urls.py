from django.urls import path
from . import views

urlpatterns = [
    path("chats/<str:pk>", views.getChat, name="chat"),
    path("chats", views.getChats, name="chats"),
]
