from django.contrib import admin
from website.models import *

class ProjectAdmin(admin.ModelAdmin):
	list_display = ('name', 'type', 'active', 'date', 'url')
	search_fields = ['name']

class ProfileAdmin(admin.ModelAdmin):
	list_display = ('name', 'url', 'icon')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Profile, ProfileAdmin)