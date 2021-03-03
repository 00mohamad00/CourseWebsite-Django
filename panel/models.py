from django.utils import timezone

from django.db import models
from account.models import Account


class Course(models.Model):
    title = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(Account, on_delete=models.CASCADE)  # TODO: set validator


class CourseContent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    file = models.FileField()  # TODO: need to check
    published_date = models.DateTimeField(default=timezone.now, editable=True)


class HomeWork(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=True)
    published_date = models.DateTimeField(auto_now_add=True)
    deadline_date = models.DateTimeField(blank=False, null=False)


class Answer(models.Model):
    answer = models.FileField()  # TODO: need to check
    student = models.ForeignKey(Account, on_delete=models.CASCADE)
    home_work = models.ForeignKey(HomeWork, on_delete=models.CASCADE)
    submitted_date = models.DateTimeField(auto_now=True)
