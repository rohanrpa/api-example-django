from rest_framework import serializers
from myapp.models import Doctor,Appointment

class DoctorSerializer(serializers.ModelSerializer):
	# my_field = serializers.SerializerMethodField('is_named_bar')
	class Meta:
		model = Doctor
		fields = ( 'first_name', 'last_name', 'total_wait_time', 'total_patients')

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ( 'app_id', 'first_name', 'last_name', 'time_of_arrival', 'start_time','wait_time')
