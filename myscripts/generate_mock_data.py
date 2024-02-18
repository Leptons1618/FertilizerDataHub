import random
import time
from datetime import datetime
from pymongo import MongoClient

def determine_alarm_status(measurement_value, threshold_low_low, threshold_low, threshold_high, threshold_high_high):
    if measurement_value < threshold_low_low:
        return "Low Low"
    elif threshold_low_low <= measurement_value < threshold_low:
        return "Low"
    elif threshold_high_high >= measurement_value > threshold_high:
        return "High"
    elif measurement_value >= threshold_high_high:
        return "High High"
    else:
        return "Normal"

def generate_sensor_data(num_data_points, processes, process_collection, sensor_data_collection, alarm_collection):
    # Define threshold values
    threshold_low_low = 20
    threshold_low = 40
    threshold_high = 80
    threshold_high_high = 90

    for _ in range(num_data_points):
        timestamp = datetime.now()
        sensor_id = random.randint(1, 10)
        measurement_value = random.uniform(0, 100)
        process = random.choice(processes)

        # Determine alarm status based on the measurement value and thresholds
        alarm_status = determine_alarm_status(measurement_value, threshold_low_low, threshold_low, threshold_high, threshold_high_high)

        # Store the process data in the "process" collection (if not already present)
        process_data = {'name': process}
        process_collection.update_one(process_data, {'$setOnInsert': process_data}, upsert=True)

        # Create and save a SensorData instance
        sensor_data = {
            'sensor_id': sensor_id,
            'measurement_value': measurement_value,
            'timestamp': timestamp,
            'process': process,
            'alarm_status': alarm_status
        }
        sensor_data_collection.insert_one(sensor_data)

        # If the alarm status is not "Normal", create an Alarm instance
        if alarm_status != "Normal":
            description = f"Alarm for process {process}"

            alarm_data = {
                'timestamp': timestamp,
                'description': description,
                'process': process,
                'alarm_status': alarm_status
            }
            alarm_collection.insert_one(alarm_data)

            # Print the alarm to the console
            print(f"Alarm: {timestamp} - {description} - Process Name: {process}")

        # Print the sensor data to the console
        print(f"Sensor Data:\n Timestamp: {timestamp} - Sensor ID: {sensor_id} - Measurement Value: {measurement_value} - Process Name: {process} - Alarm Status: {alarm_status}")
        print(f'_________________________________________________________')

if __name__ == "__main__":
    # Connect to the MongoDB database
    mongo_client = MongoClient("mongodb+srv://lept0n5:talkingmoon@sandbox.sknzcx0.mongodb.net/")
    db = mongo_client["testdb"]

    num_data_points = 1  # The number of data points to generate

    processes = ["Mixing", "Baking", "Packaging"]

    print("Generating mock sensor data and alarms...")
    # Run the script in an infinite loop
    while True:
        try:
            generate_sensor_data(num_data_points, processes, db["process"], db["sensor_data"], db["alarm"])
            time.sleep(2)  # Sleep for 2 seconds

        except KeyboardInterrupt:
            print("Exiting...")
            break