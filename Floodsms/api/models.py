from django.db import models
from django.utils.translation import gettext as _

# Create your models here
class SMSDeliveryReport(models.Model):
    message_id = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message_id} - {self.status}"

class Sensor_data(models.Model):
    sensor_id = models.CharField(max_length=100, unique=True, primary_key=True)
    sensor_timestamp = models.DateTimeField(auto_now_add=True)
    # sensor readings
    location = models.JSONField(_(""))
    readings = models.JSONField(_(""))
    alert_level = models.CharField(max_length=20)
    # sensor_temperature = models.FloatField()
    # sensor_humidity = models.FloatField()
    # sensor_soil_moisture = models.FloatField()
    battery_level = models.FloatField()
    network_status = models.CharField(max_length=20, default="2G")
    created_at = models.DateTimeField(auto_now_add=True)
    # anomaly for the AI
    # anomaly = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.sensor_id} - {self.sensor_timestamp}"


class Receipients(models.Model):
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.location} - {self.phone_number}"

    # Add any other fields you need for the recipients