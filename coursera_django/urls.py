from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'coursera_django.views.home', name='home'),
    # url(r'^coursera_django/', include('coursera_django.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^coursera/admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^coursera/admin/', include(admin.site.urls)),
    url(r'^coursera/', include('coursera_app.urls')),
)
