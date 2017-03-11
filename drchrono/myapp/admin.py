from django.contrib import admin

from myapp.models import Doctor
from myapp.models import Appointment

admin.site.register(Doctor)
admin.site.register(Appointment)