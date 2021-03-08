from django.db import models
from account.models import Account


class Notification(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField(max_length=512)
    person = models.ForeignKey(Account,on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' ' + self.person.get_full_name()
