from django.contrib import admin

# Register your models here.

# register the receipient model
from .models import Sensor_data, Receipients

@admin.register(Receipients)
class ReceipientsAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'location')