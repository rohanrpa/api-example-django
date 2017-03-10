import requests
from models import Doctor,Appointment
from datetime import datetime

'''
HELPER FUNCTIONS FOR THE DOCTOR TO LOGIN
ON FIRST USE, DOCTOR WILL BE REGISTERED WIT THE APP DB
'''
def check_if_registered_doc(doc_id):
    obj = Doctor.objects.filter(doctor_id = doc_id)
    return obj.exists()

def register_doc(request,doc_id):
    filter = {
                'id': doc_id
    }
    data = data_from_url(request,'https://drchrono.com/api/doctors',filter)[0]
    doc = Doctor()
    doc.first_name = data['first_name']
    doc.last_name  = data['last_name']
    doc.doctor_id = doc_id
    doc.total_wait_time = 0
    doc.total_patients = 0
    doc.save()

def login_as_doc(request,doc_id):
    check = check_if_registered_doc(doc_id)
    if check == True:
        return True
    else:
        register_doc(request, doc_id)
'''
FUNCTION TO RECORD A NEW APPOINTMENT WHENEVER A PATIENT CHECKS IN
'''
def new_appointment(app_id,fname,lname):
    appointment = Appointment()
    now = datetime.now()
    appointment.app_id = app_id
    appointment.time_of_arrival = now
    appointment.first_name = fname
    appointment.last_name = lname
    appointment.save()


def data_from_url(request,url, filter={}):
    '''
    MAIN FUNCTION TO GET DATA FROM DRCHRONO API
    '''
    data = []
    headers = {'Authorization': 'Bearer %s' %request.session['access_token'],}
    while url:
        page = requests.get(url, filter, headers=headers).json()
        data.extend(page['results'])
        url = page['next']
    return data

'''
FUNCTION TO RECORD THE TOTAL WAIT TIME OF EACH PATIENT
'''
def setWaitTime(request,app_id):
    appointment = Appointment.objects.get(app_id=app_id)
    now = datetime.now()
    appointment.start_time = now
    dur = getDuration(str(now),str(appointment.time_of_arrival))
    appointment.wait_time = dur
    doctor = Doctor.objects.get(doctor_id=int(request.session['doc_id']))
    doctor.total_wait_time = doctor.total_wait_time + dur
    doctor.total_patients = doctor.total_patients + 1
    doctor.save()
    appointment.save()

def getDuration(now,then):
    then_hr = int(then[11:13])
    now_hr = int(now[11:13])
    then_hr = then_hr - 8
    then_min = int(then[14:16])
    now_min = int(now[14:16])
    hr_diff = now_hr-then_hr
    if (hr_diff == 0):
        min_final = now_min - then_min
    else:
        hr_diff = hr_diff - 1
        min_final = (60 - then_min) + now_min
    return min_final

def patch_to_url(url, access_token, params={}):
    '''
    MAIN FUNCTION TO PATCH DATA TO DRCHRONO API
    '''
    headers = {'Authorization': 'Bearer %s' % access_token,
               'Content-type': 'application/json',}
    print("inside patch_to_url")
    response = requests.patch(url, json=params, headers=headers)

    print(response.status_code)
    return response.status_code


def get_params(request, idk):
    p = {}
    keys = request.POST.keys()
    for k in keys:
        if k not in idk:
            p[k] = request.POST[k]
    return p

def patch_appointment(request):
	'''
	HELPER FUNCTION TO PATCH APPOINTMENT DATA TO DRCHRONO API
	'''

	instance = request.user.social_auth.get(provider='drchrono')
	username = str(instance)

	access_token = instance.extra_data['access_token']

	appointment_id = request.POST['appointment_id']
	id_keys = []
	id_keys.append('appointment_id')
	if(request.POST.has_key('first_name')):
		id_keys.append('first_name')
		id_keys.append('last_name')
	params = get_params(request, id_keys)
	appointment_url = 'https://drchrono.com/api/appointments/' + str(appointment_id)
	status_code = patch_to_url(appointment_url, access_token, params)
	return status_code


def patch_patient(request):
	'''
	HELPER FUNCTION TO PATCH PATIENT DATA TO DRCHRONO API
	'''
	instance = request.user.social_auth.get(provider='drchrono')
	username = str(instance)

	access_token = instance.extra_data['access_token']

	patient_id = request.POST['patient_id']
	id_keys = []
	id_keys.append('patient_id')
	params = get_params(request, id_keys)
	patient_url = 'https://drchrono.com/api/patients/' + str(patient_id)
	status_code = patch_to_url(patient_url, access_token, params)
	return status_code
