import datetime
#from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)


class Account(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=40, unique=True)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField(default=datetime.date.today)
    password = models.CharField(max_length=20)
