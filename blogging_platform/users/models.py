from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = [
        ('Owner', 'Owner'),
        ('Admin', 'Admin'),
        ('Member', 'Member'),
    ]
    role = models.CharField(max_length=10, choices=ROLES, default='Member')
