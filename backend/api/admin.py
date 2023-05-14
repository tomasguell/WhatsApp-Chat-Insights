from django.contrib import admin
from .models import Chat, Message, Sender


admin.site.register(Chat)
# Register your models here.
admin.site.register(Message)
admin.site.register(Sender)
