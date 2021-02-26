from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    is_student = models.BooleanField(default=True)
    student_id = models.IntegerField(blank=True, null=True)  # TODO: set validator


class Course(models.Model):
    title = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(Account, on_delete=models.CASCADE)  # TODO: set validator


class CourseContent(models.Model):
    description = models.TextField(blank=True)
    file = models.FileField()  # TODO: need to check


class HomeWork(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=True)
    published_date = models.DateTimeField(auto_now_add=True)
    deadline_date = models.DateTimeField(blank=False, null=False)


class Answer(models.Model):
    answer = models.FileField()  # TODO: need to check
    student = models.ForeignKey(Account, on_delete=models.CASCADE)
    home_work = models.ForeignKey(HomeWork, on_delete=models.CASCADE)
    submitted_date = models.DateTimeField(auto_now=True)