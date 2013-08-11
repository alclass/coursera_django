from django.db import models

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
  institutions = models.ManyToManyField(Institution)

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
  cid    = models.CharField(primary_key=True, max_length=20, unique=True)
  n_seq = models.IntegerField()
  title        = models.CharField(max_length=100)
  description  = models.TextField()
  start_date   = models.DateField()
  duration_in_weeks = models.IntegerField(default=0)
  workload_in_hours_per_week = models.IntegerField(default=0)
  #workload_in_hours_per_day = models.IntegerField(default=0)
  n_videos     = models.IntegerField(default=0)
  instructors  = models.ManyToManyField(Instructor) #, related_name='instr+')
  institutions = models.ManyToManyField(Institution) #, related_name='insti+')
  categories   = models.ManyToManyField(Category) #, related_name='c+')
  #university  = models.ForeignKey(Institution)
  
  @property
  def workload_in_hours_per_day(self):
    return self.workload_in_hours_per_week
  
  def get_1st_institution(self):
    return self.institutions.all()[0]
  
  def get_start_date_as_dashed_yyyy_mm_dd(self):
    dashed_yyyymmdd_date = '%d-%02d-%02d' %(self.start_date.year, self.start_date.month, self.start_date.day)  
    return dashed_yyyymmdd_date
  
  def return_course_id_plus_course_n_seq_dict(self):
    return {'course_id':self.course_id, 'course_n_seq':self.course_n_seq} 

  def form_rel_url_for_index_page(self):
    return 'course/%s-%d/' %(self.course_id, self.course_n_seq)

  def form_rel_url_for_lecture_index_page(self):
    return 'course/%s-%d/' %(self.course_id, self.course_n_seq)
  
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
  video_n_id          = models.IntegerField()
  filename            = models.CharField(max_length=150)
  has_been_downloaded = models.BooleanField(default=False)
  duration_in_sec     = models.IntegerField(default=0) 

