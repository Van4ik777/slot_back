from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    money = models.IntegerField(default=1000)