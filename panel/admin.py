from django.contrib import admin

from .models import Course, CourseContent, HomeWork, Answer

# Register your models here.
admin.site.register(Course)
admin.site.register(CourseContent)
admin.site.register(HomeWork)
admin.site.register(Answer)