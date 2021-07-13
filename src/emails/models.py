from django.db import models
import datetime
import time
# Create your models here.


class Email(models.Model):
    sender = models.EmailField()
    receiver = models.EmailField()
    text = models.TextField()
    date = models.DateField(default=datetime.date.today)
    time = models.TimeField(
        default=time.strftime("%H:%M:%S", time.localtime()))
    subject = models.CharField(max_length=200, blank=True)
    # attachment = models.URLField(blank=True)
    # the id of the email,this email responds to
    response = models.IntegerField(blank=True, null=True)
    isSpam = models.BooleanField(default=False)
