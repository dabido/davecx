from django.shortcuts import render_to_response
from django.template import RequestContext
from xml.dom import minidom
from website.lib import strip_html
from website.models import Profile, Project
import json
import urllib2

# Create your views here.
def index(request):
	profiles = Profile.objects.all()
	return render_to_response("index.html", { "profiles": profiles, "current": "home" }, context_instance=RequestContext(request))

def projects(request):
	projects = Project.objects.all()
	return render_to_response("projects.html", {"projects": projects, "current": "projects" }, context_instance=RequestContext(request))

def feed_tumblr(request, site):
	if site == "blog":
		url = "http://blog.dave.cx/api/read/"
	else:
		url = "http://thoughts.dave.cx/api/read/"

	xmlstring = urllib2.urlopen(url).read()
	xmldoc = minidom.parseString(xmlstring)

	xml_post_elements = xmldoc.getElementsByTagName('post')

	blogposts = []
	for xml_post_element in xml_post_elements:
		blogpost = {
			"title": strip_html(xml_post_element.firstChild.firstChild.nodeValue.strip()),
			"url": xml_post_element.attributes["url"].value,
			"date": xml_post_element.attributes["unix-timestamp"].value
		}

		blogposts.append(blogpost)

	return render_to_response("feed_tumblr.html", {"posts": json.dumps(blogposts)})