from django.db import models

# Create your models here.


class Institution(models.Model):
  institution_id = models.IntegerField(unique=True)
  name = models.CharField(max_length=100)

class Instructor(models.Model):
  instructor_id = models.IntegerField(unique=True)
  name = models.CharField(max_length=100)
  institutions = models.ManyToManyField(Institution)

class Course(models.Model):
  course_id    = models.CharField(max_length=20, unique=True)
  course_n_seq = models.IntegerField()
  title        = models.CharField(max_length=100)
  description  = models.TextField()
  n_videos     = models.IntegerField(default=0)
  instructors  = models.ManyToManyField(Instructor)
  university   = models.ForeignKey(Institution)
  
  
  def return_course_id_plus_course_n_seq_dict(self):
    return {'course_id':self.course_id, 'course_n_seq':self.course_n_seq} 

  def form_rel_url_for_index_page(self):
    return 'course/%s-%d/' %(self.course_id, self.course_n_seq)

  def form_rel_url_for_lecture_index_page(self):
    return 'course/%s-%d/' %(self.course_id, self.course_n_seq)
  
  def form_rel_dir_for_downloaded_videos(self):
    id_plus_n_seq_dict = self.return_course_id_plus_course_n_seq_dict()
    return 'coursera.org/%(title)s %(id_plus_n_seq_dict)s' %{'title':self.title, 'id_plus_n_seq_dict':id_plus_n_seq_dict}
    

class VideoLecture(models.Model):
  course              = models.ForeignKey(Course, related_name='videolecture_set')
  video_n_id          = models.IntegerField()
  filename            = models.CharField(max_length=150)
  has_been_downloaded = models.BooleanField(default=False)
  duration_in_sec     = models.IntegerField(default=0) 
