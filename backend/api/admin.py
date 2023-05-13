from django.contrib import admin
from .models import Chat, Message


admin.site.register(Chat)
# Register your models here.
admin.site.register(Message)
