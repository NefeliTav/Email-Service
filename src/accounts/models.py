from pynamodb.attributes import (
    UnicodeAttribute, UTCDateTimeAttribute
)
from pynamodb.models import Model
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

'''

class Account(Model):
    class Meta:
        aws_access_key_id = None
        aws_secret_access_key = None
        table_name = 'Account'
        region = None
        host = 'http://localhost:8000/auth/signup'
        write_capacity_units = 1
        read_capacity_units = 1

    first_name = UnicodeAttribute()
    last_name = UnicodeAttribute()
    email = UnicodeAttribute(hash_key=True)
    phone = UnicodeAttribute()
    date_of_birth = UTCDateTimeAttribute(default=datetime.date.today)
    password = UnicodeAttribute()

from dynamorm import DynaModel
from marshmallow import fields
from django.conf import settings

class Account(DynaModel):
    class Table:
        resource_kwargs = {
            'endpoint_url': settings.DB_ENDPOINT
        }
        name = settings.DB_TABLE
        hash_key = "email"
        read = 1
        write = 1

    class Schema:
        first_name = fields.String()
        last_name = fields.String()
        email = fields.String()
        phone = fields.String()
        date_of_birth = fields.DateTime()
        password = fields.String()
'''
