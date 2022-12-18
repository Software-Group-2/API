import uuid
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Place(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    email = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    label = models.CharField(max_length=100)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    place_id = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    comment = models.CharField(max_length=500)

class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    place_id = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits = 5,decimal_places = 2)


class ErrorResponse(models.Model):
    error = models.CharField(max_length=200)
    description = models.CharField(max_length=200)


class SuccessResponse(models.Model):
    message = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
