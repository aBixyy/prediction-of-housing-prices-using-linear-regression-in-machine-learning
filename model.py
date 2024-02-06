from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class CustomUser(AbstractUser):
    # Add custom fields here
    # For example:
    # age = models.IntegerField(blank=True, null=True)
    pass





