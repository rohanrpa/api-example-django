from django.db import models

class Doctor(models.Model):
    doctor_id = models.IntegerField()
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    total_wait_time = models.IntegerField(null = True)
    total_patients = models.IntegerField(null = True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Appointment(models.Model):
    app_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    time_of_arrival = models.DateTimeField()
    start_time = models.DateTimeField(null = True)
    wait_time = models.IntegerField(null = True)

    def __str__(self):
        return self.first_name + ' ' + str(self.time_of_arrival)
