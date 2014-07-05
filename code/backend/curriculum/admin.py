from django.contrib import admin

# Register your models here.
from backend.curriculum.models import CourseItem, Review

admin.site.register(CourseItem)
admin.site.register(Review)