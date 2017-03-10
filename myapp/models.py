from django.db import models

class Patient(models.Model):
	patient_id = models.IntegerField(blank=True,unique=True)
	name = models.CharField(max_length=256)
	date_of_birth = models.DateField(null=True)
	email = models.CharField(max_length=256, blank=True)
	message_status = models.CharField(max_length=256, blank=True)
	year = models.IntegerField(blank=True)

	def __unicode__(self):
		return '{}'.format(self.name)