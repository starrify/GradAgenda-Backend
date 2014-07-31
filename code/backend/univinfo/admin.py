from django.contrib import admin

# Register your models here.
from backend.univinfo.models import University, Major, Professor, Course, Section, Lecture

admin.site.register(University)
admin.site.register(Major)
admin.site.register(Professor)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Lecture)