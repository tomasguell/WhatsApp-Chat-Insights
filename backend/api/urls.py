from django.urls import path
from . import views

urlpatterns = [
    path("chat/<str:pk>", views.getChat, name="chat"),
]
