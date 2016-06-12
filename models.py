from __future__ import unicode_literals
import datetime
from django.db import models
from tinymce.models import HTMLField
from taggit.managers import TaggableManager

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=50)
    tags = TaggableManager()
    publish_date = models.DateField(default=datetime.date.today)
    deck = models.TextField(max_length=200)
    img_name = models.CharField(null=True, max_length=50, blank=True)
    post_body = HTMLField()

class PushSubscriber(models.Model):
    sub_id = models.CharField(null=False, unique=True, max_length=500)
