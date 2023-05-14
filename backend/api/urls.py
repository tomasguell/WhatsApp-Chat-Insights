from django.urls import path
from . import views

urlpatterns = [
    path("chats/<str:pk>", views.Chat, name="chat"),
    path("chats", views.Chats, name="chats"),
]
