from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    student_id = models.IntegerField(blank=True, null=True, verbose_name='شماره دانشجویی')  # TODO: set validator


