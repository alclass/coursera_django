from django.contrib import admin
from coursera_app.models import CourseraCourse, Instructor, Institution, Category


class CourseraCourseAdmin(admin.ModelAdmin):
  list_display  = ('title',)
  ordering      = ('title',)
  search_fields = ('title', 'cid',)

admin.site.register(CourseraCourse, CourseraCourseAdmin)

class InstructorAdmin(admin.ModelAdmin):
  list_display  = ('name',)
  ordering      = ('name',)
  search_fields = ('name',)

admin.site.register(Instructor, InstructorAdmin)

class InstitutionAdmin(admin.ModelAdmin):
  list_display  = ('name',)
  ordering      = ('name',)
  search_fields = ('name',)

admin.site.register(Institution, InstitutionAdmin)

class CategoryAdmin(admin.ModelAdmin):
  list_display  = ('name',)
  ordering      = ('name',)
  search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)
