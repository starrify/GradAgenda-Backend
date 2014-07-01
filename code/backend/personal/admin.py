from django.contrib import admin

# Register your models here.
from backend.personal.models import User

admin.site.register(User)