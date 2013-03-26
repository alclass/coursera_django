from django.contrib import admin
from coursera_app.models import Course


class CourseAdmin(admin.ModelAdmin):
  list_display  = ('name',)
  ordering      = ('name',)
  search_fields = ('name',)

admin.site.register(Course, CourseAdmin)
  