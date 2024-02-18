from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('historical-data/<str:process>/', views.get_historical_data, name='get_historical_data'),
    path('latest-sensor-data/', views.get_latest_sensor_data, name='get_latest_sensor_data'),
    path('latest-alarms/', views.get_latest_alarms, name='get_latest_alarms'),
]