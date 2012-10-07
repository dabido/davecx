from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url("^favicon\.ico", 'django.views.generic.simple.redirect_to', {'url': 'http://davecx.s3.amazonaws.com/img/favicon.ico'}),
	# Examples:
	# url(r'^$', 'davecx.views.home', name='home'),
	# url(r'^davecx/', include('davecx.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns("website.views", 
	url('^$', 'index'),
	url('^p/$', 'projects'),
	url(r'^feed/blog.json', 'feed_tumblr', {"site": "blog"}),
	url(r'^feed/thoughts.json', 'feed_tumblr', {"site": "thoughts"}),
)

if settings.DEBUG:
	urlpatterns += staticfiles_urlpatterns()


	urlpatterns += patterns('',
		url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
			'document_root': settings.MEDIA_ROOT,
		}),
	)