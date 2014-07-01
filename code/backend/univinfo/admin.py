from django.contrib import admin

# Register your models here.
from backend.univinfo.models import University, College, Major, Grade, Professor, OfficeHour, Course, Lecture

admin.site.register(University)
admin.site.register(College)
admin.site.register(Major)
admin.site.register(Grade)
admin.site.register(Professor)
admin.site.register(OfficeHour)
admin.site.register(Course)
admin.site.register(Lecture)