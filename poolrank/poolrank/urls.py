from django.conf.urls import patterns, include, url
from views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^Register/$', register),
	(r'^Register/(\w+)/$', register),
	(r'^AccountCreated/$', account_created),
	(r'^Rankings/$', rankings),
	(r'^RecordMatch/$', record_match),
    # Examples:
    # url(r'^$', 'poolrank.views.home', name='home'),
    # url(r'^poolrank/', include('poolrank.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    
)
