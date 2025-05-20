from django.urls import path
from .views import SensorDataView, SMSDeliveryCallbackView

urlpatterns = [
    path('sensor-data/', SensorDataView.as_view(), name='sensor_data'),
    path('delivery-callback/', SMSDeliveryCallbackView.as_view(), name='sms_callback'),
]