from django.db import models
from django.contrib.auth.models import User
import uuid



# Create your models here.
class Place(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    label = models.CharField(max_length=100)
