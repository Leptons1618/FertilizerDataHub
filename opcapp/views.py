from django.shortcuts import render
from django.views import View
from pymongo import MongoClient
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import asyncio

matplotlib.use('Agg')  # Set Matplotlib to non-interactive mode

class OPCDataView(View):
    async def get(self, request):
        print('Passing the last 10 OPC simulator data from the database to the template')

        # Connect to MongoDB
        mongo_client = MongoClient("mongodb+srv://lept0n5:talkingmoon@sandbox.sknzcx0.mongodb.net/")
        database = mongo_client["fertilizer_industry_management"]

        # Get the last 10 records from the database asynchronously
        loop = asyncio.get_event_loop()
        sensor_data = await loop.run_in_executor(None, lambda: list(database.sensor_data.find().sort([("timestamp", -1)]).limit(100)))

        # Plot the data using Matplotlib
        timestamps = [entry["timestamp"] for entry in sensor_data]
        values = [entry["value"] for entry in sensor_data]

        plt.plot(timestamps, values)
        plt.xlabel('Timestamp')
        plt.ylabel('Value')
        plt.title('OPC Data Plot')

        # Save the plot as a PNG file in the static folder
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        img_data = base64.b64encode(img_buffer.read()).decode('utf-8')

        # Close the Matplotlib figure explicitly
        plt.close()

        return render(request, 'opc_data.html', {'sensor_data': sensor_data[:10], 'plot_image': img_data})

@method_decorator(csrf_exempt, name='dispatch')
class OPCDataApiView(View):
    async def get(self, request):
        print('API Endpoint: Fetching the latest OPC simulator data')

        # Connect to MongoDB
        mongo_client = MongoClient("mongodb+srv://lept0n5:talkingmoon@sandbox.sknzcx0.mongodb.net/")
        database = mongo_client["fertilizer_industry_management"]

        # Get the last 10 records from the database asynchronously
        loop = asyncio.get_event_loop()
        sensor_data = await loop.run_in_executor(None, lambda: list(database.sensor_data.find().sort([("timestamp", -1)]).limit(10)))

        # Plot the data using Matplotlib
        timestamps = [entry["timestamp"] for entry in sensor_data]
        values = [entry["value"] for entry in sensor_data]

        plt.plot(timestamps, values)
        plt.xlabel('Timestamp')
        plt.ylabel('Value')
        plt.title('OPC Data Plot')

        # Save the plot as a PNG file in the static folder
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        img_data = base64.b64encode(img_buffer.read()).decode('utf-8')

        # Close the Matplotlib figure explicitly
        plt.close()

        # Return data as JSON
        response_data = {
            'sensor_data': [{'timestamp': entry['timestamp'], 'value': entry['value']} for entry in sensor_data],
            'plot_image': img_data,
        }
        return JsonResponse(response_data, safe=False)
