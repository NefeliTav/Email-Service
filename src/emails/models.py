from django.db import models
import datetime
# Create your models here.


class Email(models.Model):
    sender = models.EmailField()
    receiver = models.EmailField()
    text = models.TextField()
    date = models.DateField(default=datetime.date.today)
    time = models.TimeField(null=True)
    subject = models.CharField(max_length=200, blank=True)
    attachment = models.URLField(blank=True)
