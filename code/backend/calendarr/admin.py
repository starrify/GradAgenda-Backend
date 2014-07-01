from django.contrib import admin

# Register your models here.
from backend.calendarr.models import EventItem

admin.site.register(EventItem)