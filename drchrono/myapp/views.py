from django.shortcuts import render,redirect, render_to_response
from django.contrib.auth.decorators import login_required
import requests
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth import login, logout as my_logout
from django.views.generic import View
from django.http import JsonResponse
from datetime import datetime
from django.core import serializers
from service import new_appointment,patch_appointment,patch_patient,login_as_doc, data_from_url,setWaitTime, getDuration
from myapp.models import *
from myapp.serializers import *


class IndexView(View):

	def get(self, request, *args, **kwargs):
		return render(request,'index.html')
	
class HomeView(View):

	def get(self, request, *args, **kwargs):
		if (request.user.is_anonymous() == True or request.user.is_authenticated() == False) :
			return render(request,'index.html')
		else:
			instance = request.user.social_auth.get(provider='drchrono')
			user_name = str(instance)
			request.session['un'] = user_name
			request.session['access_token'] = instance.extra_data['access_token']
			data = data_from_url(request,'https://drchrono.com/api/users')
			for da in data:
				if da['username'] == user_name:
					if da['is_doctor'] == True:
						request.session['doc_id'] = da['doctor']
						login_as_doc(request,da['doctor'])
			return render(request,'home.html')


class DoctorsView(View):

	def get(self, request, *args, **kwargs):
		return render(request,'doctors.html')

class KioskView(View):

	def get(self, request, *args, **kwargs):
		return render(request,'kiosk.html')
	
	
class PatienstView(View):

    def get(self, request):
        if (request.GET.has_key("fname") and request.GET.has_key("lname") and request.GET.has_key("dob")):
			filter = {
					'first_name' : request.GET.get('f_name'),
					'last_name' : request.GET.get('l_name'),
					'date_of_birth' : request.GET.get('dob'),
			}
			instance = request.user.social_auth.get(provider='drchrono')
			username = str(instance)

			access_token = instance.extra_data['access_token']
			headers = {'Authorization': 'Bearer %s' % access_token,}
			patient = requests.get('https://drchrono.com/api/patients',filter, headers=headers).json()
			return JsonResponse(patient)
        else:
            return JsonResponse({"status": "false"}, status=500)

    def post(self, request):
        if (request.POST.has_key("patient_id")):
            status_code = patch_patient(request)
            return JsonResponse({"response": status_code})
        else:
            return JsonResponse({"status": "false"}, status=500)



class AppointmentView(View):

	def get(self, request):
	    if (request.GET.has_key("p_id")):
			now = datetime.now()
			date = now.strftime('%Y-%m-%d')
			instance = request.user.social_auth.get(provider='drchrono')
			username = str(instance)

			access_token = instance.extra_data['access_token']
			headers = {'Authorization': 'Bearer %s' % access_token,}
			posts = requests.get('https://drchrono.com/api/appointments',{"date": date,"patient":request.GET.get('p_id')}, headers=headers).json()
			html = render_to_string('patient_details.html', {'result': posts['results'][0]})
			return HttpResponse(html)
	    else:
	        return JsonResponse({"status": "false"}, status=500)
   
	def post(self, request, *args, **kwargs):
		if (request.POST['appointment_id'] ):
			new_appointment(request.POST['appointment_id'],request.POST['fname'],request.POST['lname'])
			status_code = patch_appointment(request)
			return JsonResponse({"response": status_code})
		else:
			return JsonResponse({"status": "false"}, status=500)

		
class DoctorAppointmentView(View):

    def get(self, request):
		now = datetime.now()
		date = now.strftime('%Y-%m-%d')
		instance = request.user.social_auth.get(provider='drchrono')
		username = str(instance)

		access_token = instance.extra_data['access_token']
		headers = {'Authorization': 'Bearer %s' % access_token,}
		test = requests.get('https://drchrono.com/api/appointments',{"date": date},headers=headers).json()
		html = render_to_string('doctors_result.html', {'result': test['results'],'status':request.GET['status']})
		return HttpResponse(html)


    def post(self, request):
        if (request.POST.has_key('appointment_id') ):
            status_code = patch_appointment(request)
            if(request.POST['status'] == 'In Session'):
                setWaitTime(request,request.POST['appointment_id'])
            return JsonResponse({"response": status_code})
        else:
            return JsonResponse({"status": "false"}, status=500)

def getdoctordetails(request):

	try:
		doctor = Doctor.objects.get(doctor_id=request.session['doc_id'])
		num_patients = Appointment.objects.exclude(start_time__isnull=True)
		print len(num_patients)

	except Doctor.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = DoctorSerializer(doctor)
		ans = serializer.data
		if lem(num_patients) != 0:
			ans["count"] = len(num_patients)
		else:
			ans["count"] = 1
		print ans
		return JsonResponse(ans)

	
def appointment_detail(request,app_id):
    try:
        appointment = Appointment.objects.get(app_id=app_id)
    except Appointment.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AppointmentSerializer(appointment)
        return JsonResponse(serializer.data)

def appointment_all(request):
    try:
        appointment = Appointment.objects.all()
    except Appointment.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
		serializer = AppointmentSerializer(appointment,many=True)
		html = render_to_string('appointments.html', {'result': serializer.data})
		return HttpResponse(html)

def get_time(request,app_id):
	print app_id
	appointment = Appointment.objects.get(app_id=app_id)
	now = datetime.now()
	appointment.start_time = now
	dur = getDuration(str(now),str(appointment.time_of_arrival))
	appointment.wait_time = dur
	print dur
	return HttpResponse(dur) 

def logout(request):
	my_logout(request)
	return redirect('/')

