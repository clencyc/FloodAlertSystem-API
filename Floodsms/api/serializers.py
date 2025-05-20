from rest_framework import status, serializers
from .models import Sensor_data, Receipients


class SensorDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Sensor_data
        fields = ['sensor_id', 'sensor_timestamp', 'location', 'readings', 'alert_level', 'battery_level', 'network_status']

    def validate(self, data):
        if not data.get('sensor_id') or not data.get('readings') or not data.get('alert_level'):
            raise serializers.ValidationError("Missing required fields: sensor_id, readings, or alert_level")
        return data

class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipients
        fields = ['phone_number', 'location']