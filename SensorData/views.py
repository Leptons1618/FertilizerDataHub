from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import SensorData, Alarm, Process

def dashboard(request):
    # Fetch latest sensor data and alarms
    latest_sensor_data = SensorData.objects.all().order_by('-timestamp')[:10]
    latest_alarms = Alarm.objects.all().order_by('-timestamp')[:5]
    
    # Fetch historical sensor data for chart visualization
    historical_sensor_data = SensorData.objects.all().order_by('-timestamp')[:10]

    return render(request, 'dashboard.html', {
        'latest_sensor_data': latest_sensor_data,
        'latest_alarms': latest_alarms,
        'historical_sensor_data': historical_sensor_data,
    })


def get_historical_data(request, process):
    # Get the Process object or return a 404 response if not found
    process_object = get_object_or_404(Process, name=process)

    # Fetch historical sensor data for a specific process (limited to 10 data points for demonstration purposes)
    historical_sensor_data = SensorData.objects.filter(process=process_object).order_by('-timestamp')[:10]


    # # # Print the historical sensor data to the console for debugging
    # print('Process:', process)
    # print('Fetched Data:', {'timestamps': [str(data.timestamp) for data in historical_sensor_data],
    #                         'measurement_value': [data.measurement_value for data in historical_sensor_data]})

    # Prepare data for JSON response ()
    data = {
        'timestamps': [str(data.timestamp) for data in historical_sensor_data],
        'measurement_value': [data.measurement_value for data in historical_sensor_data],
    }

    return JsonResponse(data)

def get_latest_sensor_data(request):
    # Fetch the latest sensor data
    latest_sensor_data = SensorData.objects.all().order_by('-timestamp')[:20]

    # Prepare data for JSON response
    data = [
        {
            'timestamp': str(sensor_data.timestamp),
            'sensor_id': sensor_data.sensor_id,
            'measurement_value': sensor_data.measurement_value,
        }
        for sensor_data in latest_sensor_data
    ]
    
    # print(data)

    return JsonResponse(data, safe=False)

def get_latest_alarms(request):
    # Fetch the latest alarms
    latest_alarms = Alarm.objects.all().order_by('-timestamp')[:5]

    # Prepare data for JSON response
    data = [
        {
            'timestamp': str(alarm.timestamp),
            'description': alarm.description,
        }
        for alarm in latest_alarms
    ]

    return JsonResponse(data, safe=False)
