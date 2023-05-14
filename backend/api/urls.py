from django.urls import path
from . import views

urlpatterns = [
    path("chats/<str:pk>", views.GetChat, name="chat"),
    path("chats", views.Chats, name="chats"),
]
