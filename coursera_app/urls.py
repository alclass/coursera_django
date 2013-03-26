from django.conf.urls import patterns, include, url
from django.views.generic import list_detail

from coursera_app.models import Course
#from coursera_app import views


course_list_genviewdict = {
  'queryset' : Course.objects.all().order_by('name')                           
                           }

urlpatterns = patterns('',
  url(r'courses/$', list_detail.object_list, course_list_genviewdict),
)
