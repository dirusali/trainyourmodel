
from django.db import models, OperationalError, transaction
from autoslug import AutoSlugField
from django.template.defaultfilters import slugify
from tinymce.models import HTMLField
import json
from django_mysql.models import ListTextField
from django.utils import timezone
from model_utils.models import TimeStampedModel
from lxml import html
import collections
import logging
from django.db.models import Count, CharField, Model
from django.urls import reverse
logger = logging.getLogger(__name__)
from datetime import datetime
from django.template.defaultfilters import truncatechars

class DataFile(models.Model):
    title = models.CharField(max_length=500,blank=True)







