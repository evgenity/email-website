from django.db import models
from datetime import datetime

# Create your models here.

class Subscription(models.Model):
    pub_date = models.DateTimeField('date created', default=datetime.now, blank=True)
    api_key = models.CharField(max_length=50)
    email =  models.CharField(max_length=200)

    def __str__(self):
        return f'Subscription from {self.email}'

class FormData(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    form_data = models.CharField(max_length=2000, default=datetime.now, blank=True)
    send_date = models.DateTimeField('date sent')

    def __str__(self):
        return f'FormData from {self.form_data}'