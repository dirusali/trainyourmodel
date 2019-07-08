from django.db import models
from django.utils import timezone
from django_mysql.models import ListTextField
from django.db.models import Count, CharField, Model



class Subscribe(models.Model):
    email_id = models.EmailField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email_id
