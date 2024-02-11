# from django.core.management.base import BaseCommand
from opcua import Client
# from .models import OPCData
from pymongo import MongoClient
import time

# class Command(BaseCommand):
print('Reads data from the OPC simulator')
monogo_client = MongoClient("mongodb+srv://lept0n5:talkingmoon@sandbox.sknzcx0.mongodb.net/")
data = monogo_client["fertilizer_industry_management"]

try:
    client = Client("opc.tcp://Lept0n5:53530/OPCUA/SimulationServer")
    client.connect()

    while True:
        # Read the value from the OPC simulator
        value = client.get_node("ns=3;i=1002").get_value()
        # Opcua provides the timestamp of the value, use it to store the timestamp in the database
        timestamp = client.get_node("ns=3;i=1002").get_data_value().SourceTimestamp

        # Store the timestamp and value in the database
        data.sensor_data.insert_one({"timestamp": timestamp, "tag": "Sensor 1", "value": value})
        print("Value: ", value, "Timestamp: ", timestamp)
        
        # Wait for a bit before reading again
        time.sleep(1)
        
except KeyboardInterrupt:
    client.disconnect()
    print("Disconnected")
except Exception as e:
    print(e)
    client.disconnect()
    time.sleep(10)
            
