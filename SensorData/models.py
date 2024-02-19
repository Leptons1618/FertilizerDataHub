from django.db import models

# Process model to represent the different processes in the factory (e.g. Mixing, Baking, Packaging)
class Process(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "process"
        managed = True

class SensorData(models.Model):
    sensor_id = models.AutoField(primary_key=True)
    measurement_value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    alarm_status = models.CharField(max_length=100)

    def __str__(self):
        return f"SensorData ID: {self.sensor_id}, Process: {self.process.name}"

    class Meta:
        db_table = "sensor_data"

class Alarm(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    alarm_status = models.CharField(max_length=100)

    def __str__(self):
        return f"Process: {self.process.name}, Alarm: {self.description}"

    class Meta:
        db_table = "alarm"