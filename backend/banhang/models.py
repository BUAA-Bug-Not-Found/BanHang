from django.db import models
from django.contrib.auth.models import AbstractUser

class User(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32)