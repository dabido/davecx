import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('blog.views',
	url('^$', 'listing'),
    url('^page/(?P<page>\d+)/$', 'listing'),

    url('^tag/(?P<tag_slug>[\w-]+)/$', 'listing'),
    url('^tag/(?P<tag_slug>[\w-]+)/page/(?P<page>\d+)/$', 'listing'),

    url('^category/(?P<category_slug>[\w-]+)/$', 'listing'),
    url('^category/(?P<category_slug>[\w-]+)/page/(?P<page>\d+)/$', 'listing'),

    url('^post/(?P<id>\d+)/(?P<slug>[\w-]+)/$', 'detail'),
    url('^about/$', 'about'),
)

urlpatterns += patterns('',
	url(r'^admin/', include(admin.site.urls)),
    url("^favicon\.ico", RedirectView.as_view(url='%simg/favicon_32x32.ico' % settings.STATIC_URL)),
)


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

    urlpatterns += patterns('',
            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                    'document_root': settings.MEDIA_ROOT,
            }),
    )
