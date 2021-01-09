from django.db import models
from django.utils import timezone
from django.db.models import Count, CharField, Model
from django.urls import reverse


class Subscribe(models.Model):
    email_id = models.EmailField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email_id
