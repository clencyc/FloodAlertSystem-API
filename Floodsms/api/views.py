from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

from .models import Sensor_data, Receipients, SMSDeliveryReport
from .serializers import SensorDataSerializer
import africastalking
from decouple import config
import re

# Initialize Africa's Talking SDK
africastalking.initialize(
    username=config('AT_USERNAME'),
    api_key=config('AT_API_KEY')
)
sms = africastalking.SMS

class SensorDataView(APIView):
    @extend_schema(
        request=SensorDataSerializer,
        responses={
            200: {
                "status": "success",
                "sms_error": "Optional error message if SMS sending fails"
            },
            400: "Validation errors"
        },
        description="Endpoint to submit sensor data. Sends SMS alerts if critical conditions are met."
    )
    def post(self, request):
        serializer = SensorDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.validated_data
            if self.check_alert(data):
                sms_result = self.send_sms(data)
                if sms_result.get('error'):
                    return Response({"status": "success", "sms_error": sms_result['error']}, status=status.HTTP_200_OK)
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def check_alert(self, data):
        readings = data.get('readings', {})
        return readings.get('water_level_cm', 0) > 100 or data.get('alert_level') == 'critical'

    def send_sms(self, data):
        area_name = data['location'].get('area_name', '')
        recipients = Receipients.objects.filter(location=area_name).values_list('phone_number', flat=True)
        if not recipients:
            return {"error": f"No recipients found for {area_name}"}

        valid_recipients = [phone for phone in recipients if re.match(r'^\+\d{10,15}$', phone)]
        if not valid_recipients:
            return {"error": "No valid phone numbers in international format"}

        message = f"EVACUATION ALERT: High water levels in {area_name}. Evacuate now!"
        try:
            response = sms.send(message, valid_recipients, config('AT_SENDER_ID'))
            print(f"SMS Response: {response}")
            if response['SMSMessageData']['Recipients']:
                for recipient in response['SMSMessageData']['Recipients']:
                    SMSDeliveryReport.objects.create(
                        message_id=recipient['messageId'],
                        phone_number=recipient['number'],
                        status=recipient['status']
                    )
                return {"status": "SMS sent", "details": response['SMSMessageData']['Recipients']}
            return {"error": response['SMSMessageData']['Message']}
        except Exception as e:
            print(f"SMS sending failed: {e}")
            return {"error": str(e)}

class SMSDeliveryCallbackView(APIView):
    @extend_schema(
              request=None,
              responses={
                   200: {
                          "status": "callback received"
                   }
              },
              description="Endpoint to handle SMS delivery callbacks from Africa's Talking."
    )
    def post(self, request):
        data = request.data
        print(f"Delivery Callback: {data}")
        if data.get('id') and data.get('phoneNumber') and data.get('status'):
            SMSDeliveryReport.objects.create(
                message_id=data['id'],
                phone_number=data['phoneNumber'],
                status=data['status']
            )
        return Response({"status": "callback received"}, status=status.HTTP_200_OK)