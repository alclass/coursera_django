from django.db import models

# Create your models here.


class Course(models.Model):
  name = models.CharField(max_length=100)
  coursera_id  = models.CharField(max_length=20, unique=True)
  rel_index_url    = models.CharField(max_length=150)
  rel_lectures_url = models.CharField(max_length=150)
  n_of_downloaded_video_files = models.IntegerField(default=0)
  
# class CourseBag(models.Model):

class VideoLecture(models.Model):
  course = models.ForeignKey(Course, related_name='videolecture_set')
  filename            = models.CharField(max_length=150)
  has_been_downloaded = models.BooleanField(default=False)
  duration_in_sec     = models.IntegerField(default=0) 

  