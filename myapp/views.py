from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import requests
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth import login, logout as my_logout
from django.views.generic import View
from django.http import JsonResponse
from datetime import datetime


class IndexView(View):
	def get(self, request, *args, **kwargs):
		return render(request,'index.html')
	
class HomeView(View):
	def get(self, request, *args, **kwargs):
		return render(request,'home.html')
	
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
		if (request.GET.has_key("pid")):
			print "eeeeeeeeeeeeeee"
			now = datetime.now()
			date = now.strftime('%Y-%m-%d')
			instance = request.user.social_auth.get(provider='drchrono')
			username = str(instance)

			access_token = instance.extra_data['access_token']
			headers = {'Authorization': 'Bearer %s' % access_token,}
			print request.GET['pid']
			test = requests.get('https://drchrono.com/api/appointments',{"date": date,"patient":request.GET.get('pid')}, headers=headers).json()
			return JsonResponse(test)
		else:
			return JsonResponse({"status": "false"}, status=500)

    def post(self, request):
        if (request.POST.has_key('appointment_id') ):
            new_appointment(request.POST['appointment_id'],request.POST['first_name'],request.POST['last_name'])
            status_code = patch_appointment(request)
            return JsonResponse({"response": status_code})
        else:
            return JsonResponse({"status": "false"}, status=500)

def index(request):
 	try:
 	 	user = request.user
		if user.is_authenticated() == False:
			return redirect('/login/drchrono/')
 	except:
 		user = None
 	return render(request,'index.html',{'user':user})

@login_required
def getpatients(request):
	if request.user.is_authenticated() == False:
		return HttpResponse("Login with DrChrono")
	else:
		instance = request.user.social_auth.get(provider='drchrono')
        username = str(instance)

        access_token = instance.extra_data['access_token']
        headers = {'Authorization': 'Bearer %s' % access_token,}
        patients = []
        patients_url = 'https://drchrono.com/api/patients'
        while patients_url:
			data = requests.get(patients_url, headers=headers).json()
			
			html = render_to_string('result.html', {'result': data['results']})
			return HttpResponse(html)
		
def logout(request):
	my_logout(request)
	return redirect('/')

