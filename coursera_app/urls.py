from django.conf.urls import patterns, include, url
# old: from django.views.generic import list_detail
from django.views.generic.list   import ListView

from coursera_app.models import CourseraCourse, Institution
#from coursera_app import views


#===============================================================================
# courses_by_knowledgearea_detail_genviewdict =  {
#   'queryset': KnowledgeArea.objects.all(),
#   'template_name': 'TTC_app/courses_by_knowledgearea.html', 
#   'context_object_name': 'knowledge_area',
# }
#===============================================================================

course_list_genviewdict = {
  'queryset' : CourseraCourse.objects.all().order_by('title')                           
}

institution_list_genviewdict = {
  'queryset' : Institution.objects.all().order_by('name')                           
}

urlpatterns = patterns('',
  # old: url(r'courses/$', list_detail.object_list, course_list_genviewdict),
  url(r'courses/$', ListView.as_view(**course_list_genviewdict)),
  # url(r'knowledgeareas/(?P<object_id>\d+)/courses/$', ListView.as_view(**courses_by_knowledgearea_detail_genviewdict)),
  url(r'institutions/$', ListView.as_view(**institution_list_genviewdict)),
)
