import datetime
from django.db import models

class Account(models.Model):
    user_id = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=40, unique=True)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField(default=datetime.date.today)
    password = models.CharField(max_length=20)


