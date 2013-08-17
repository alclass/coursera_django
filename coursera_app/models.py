import datetime
from django.db import models

from coursera_django.defaults import LECTURE_INDEX_INTERPOLATE_URL

# Create your models here.


class Category(models.Model):
  '''
  CourseraCourse's Category Django's Model 
  '''
  #institution_id = models.IntegerField(unique=True)
  # id = models.IntegerField(unique=True)
  name = models.CharField(max_length=100)

  def __unicode__(self):
    outstr = u'%s' %(self.name)
    return outstr

  def __str__(self):
    return self.__unicode__()

class Institution(models.Model):
  '''
  CourseraCourse's Institution Django's Model 
  '''
  #institution_id = models.IntegerField(unique=True)
  # id = models.IntegerField(unique=True)
  name = models.CharField(max_length=100)
  
  def __unicode__(self):
    outstr = u'%s' %(self.name)
    return outstr

  def __str__(self):
    return self.__unicode__()

class Instructor(models.Model):
  '''
  CourseraCourse's Instructor Django's Model 
  '''
  #instructor_id = models.IntegerField(unique=True)
  #id = models.IntegerField(unique=True)
  name = models.CharField(max_length=100)
  institutions = models.ManyToManyField(Institution, null=True)

  def get_1st_institution(self):
    return self.institutions.all()[0]

  def __unicode__(self):
    outstr = u'%s' %(self.name)
    return outstr

  def __str__(self):
    return self.__unicode__()


class CourseraCourse(models.Model):
  '''
  CourseraCourse Django's Model 
  '''
  cid          = models.CharField(primary_key=True, max_length=40, unique=True)
  n_seq        = models.IntegerField(default=-1)
  title        = models.CharField(max_length=100)
  description  = models.TextField(null=True, blank=True)
  start_date   = models.DateField(null=True, blank=True)
  duration_in_weeks = models.IntegerField(default=0)
  workload_in_hours_per_week = models.IntegerField(default=0)
  n_videos     = models.IntegerField(default=0)
  instructors  = models.ManyToManyField(Instructor, null=True, blank=True) #, related_name='instr+')
  institutions = models.ManyToManyField(Institution, null=True, blank=True) #, related_name='insti+')
  categories   = models.ManyToManyField(Category, null=True, blank=True) #, related_name='c+')
  #university  = models.ForeignKey(Institution)
  is_video_completed = models.BooleanField(default=False)
  
  @property
  def finish_date(self):
    '''
    '''
    if self.duration_in_weeks < 1:
      return None
    if self.start_date == None:
      return None
    n_days = self.duration_in_weeks * 7
    duration_in_delta_days = datetime.timedelta(n_days)
    finish_date = self.start_date + duration_in_delta_days
    return finish_date

  def has_course_finished(self):
    if self.duration_in_weeks < 1 or self.start_date == None:
      return False
    today = datetime.date.today()
    finish_date = self.finish_date
    if finish_date == None:
      return False
    if today > finish_date:
      return True
    return False 
  
  def is_course_finish_date_older_than(self, n_days):
    finish_date = self.finish_date
    if finish_date == None or n_days == None:
      return False 
    after_finished_days = datetime.timedelta(n_days)
    projected_date = finish_date + after_finished_days
    today = datetime.date.today()
    if today > projected_date:
      return True
    return False
      
  @property
  def instructor(self):
    return self.get_1st_instructor()

  @property
  def institution(self):
    return self.get_1st_institution()

  def get_1st_instructor(self):
    if self.instructors.count() > 0: 
      return self.instructors.all()[0]
    return None
 
  def get_1st_institution(self):
    if self.institutions.count() > 0: 
      return self.institutions.all()[0]
    return None
  
  def get_start_date_as_dashed_yyyy_mm_dd(self):
    if self.start_date != None:
      dashed_yyyymmdd_date = '%d-%02d-%02d' %(self.start_date.year, self.start_date.month, self.start_date.day)  
      return dashed_yyyymmdd_date
    return None
  
  def return_course_id_plus_course_n_seq_dict(self):
    return {'course_id':self.course_id, 'course_n_seq':self.course_n_seq} 

  def form_rel_url_for_index_page(self):
    return 'course/%s-%d/' %(self.course_id, self.course_n_seq)

  def form_rel_url_for_lecture_index_page(self):
    if self.n_seq > 0:
      return 'course/%s-%d/' %(self.course_id, self.course_n_seq)
    return 'course/%s/' %(self.course_id)

  def form_course_id_dash_n_seq_substr(self):  
    course_id_dash_n_seq = '%(cid)s-%(n_seq)03d' %{'cid':self.cid, 'n_seq':self.n_seq}
    return course_id_dash_n_seq

  def form_abs_url_to_lecture_index(self):
    '''
    course_id_and_n_seq
    LECTURE_INDEX_INTERPOLATE_URL = 'https://class.coursera.org/%(course_id_dash_n_seq)s/lecture/index'
    '''
    return LECTURE_INDEX_INTERPOLATE_URL %{'course_id_dash_n_seq' : self.form_course_id_dash_n_seq_substr()}  

  @property
  def abs_url_to_lecture_index(self):
    return self.form_abs_url_to_lecture_index()

 
  def form_rel_dir_for_downloaded_videos(self):
    id_plus_n_seq_dict = self.return_course_id_plus_course_n_seq_dict()
    return 'coursera.org/%(title)s %(id_plus_n_seq_dict)s' %{'title':self.title, 'id_plus_n_seq_dict':id_plus_n_seq_dict}

  def __unicode__(self):
    #outstr = u'Course: [%s-%03d] %s' %(self.id, self.n_seq, self.title)
    outstr = u'%s' %(self.title)
    return outstr

  def __str__(self):
    return self.__unicode__()

class VideoLecture(models.Model):
  course              = models.ForeignKey(CourseraCourse, related_name='videolecture_set')
  video_n_id          = models.IntegerField(default=-1)
  filename            = models.CharField(max_length=150)
  has_been_downloaded = models.BooleanField(default=False)
  duration_in_sec     = models.IntegerField(default=0) 

