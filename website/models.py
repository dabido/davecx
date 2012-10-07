from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Profile(models.Model):
	name = models.CharField(max_length=100)
	url = models.URLField()
	icon = models.FileField(upload_to="socialicons")
	class Meta:
		verbose_name = 'Profile'
		verbose_name_plural = 'Profile'
		ordering = ['name']

	def __unicode__(self):
		return self.name

class Project(models.Model):
	PROJECT_TYPES = (
		(0, 'Website'),
		(1, 'Webapp'),
		(2, 'Desktop App'),
		(2, 'Extension')
	)

	name = models.CharField(max_length=100)
	description = models.TextField(max_length=2000)
	screenshot = models.FileField(upload_to="projects", blank=True)
	type = models.IntegerField(default=0, choices=PROJECT_TYPES)
	date = models.DateField(default=datetime.now)
	url = models.URLField(blank=True)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ['-date']