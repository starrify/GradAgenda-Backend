from django.contrib import admin

# Register your models here.
from backend.friend.models import FriendRelation, FriendRequest

admin.site.register(FriendRelation)
admin.site.register(FriendRequest)