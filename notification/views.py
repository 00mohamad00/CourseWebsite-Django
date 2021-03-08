from django.shortcuts import render
from account.models import Account
from .models import Notification


def create_notification(person: Account, title: str, text: str):
    notification = Notification(person=person, title=title, text=text)
    notification.save()


def create_notification_for_many(persons, title: str, text: str):
    for person in persons:
        notification = Notification(person=person, title=title, text=text)
        notification.save()
