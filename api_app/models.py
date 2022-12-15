import uuid
from django.db import models
from django.contrib.auth.models import User




# Create your models here.
class Place(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    label = models.CharField(max_length=100)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post_id = models.CharField(max_length=100)
    sender_id = models.CharField(max_length=100)
    comment = models.CharField(max_length=500)
