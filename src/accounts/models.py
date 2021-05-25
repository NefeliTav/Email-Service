from django.db import models
from django.contrib.auth.models import User
import datetime

class Account(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField(default=datetime.date.today)
    password = models.CharField(max_length=20)
