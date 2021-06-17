from django.contrib import admin

# Register your models here.
from .models import Subscription, FormData

admin.site.register(Subscription)
admin.site.register(FormData)