from django.contrib import admin

# Register your models here.
from backend.chatroom.models import Chatroom, Message, Timespan

admin.site.register(Chatroom)
admin.site.register(Message)
admin.site.register(Timespan)