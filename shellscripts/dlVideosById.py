#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 27/06/2013

@author: friend
'''
import os, sys, time
import json

COURSES_DATA_JSON_FILENAME = 'coursera_courses_with_videoids.json.dat'

def pick_up_args_as_ints():
  videoids = []
  for arg in sys.argv[1:]:
    try:
      n_id = int(arg)
      videoids.append(n_id)
    except ValueError:
      pass
  return videoids

class VideoCourseDownloader(object):
  
  DEFAULT_IN_BETWEEN_DOWNLOAD_PAUSE = 3 * 60 # THREE_MINUTES_IN_SECONDS
  url_base = 'https://class.coursera.org/%(course_id)s-%(course_n_seq)s/lecture/%(video_n_id)'
  
  def __init__(self, course_id, course_n_seq):
    self.course_id    = course_id    # 'analyticalchem'
    self.course_n_seq = course_n_seq # '001'

  def get_url_dict(self, video_n_id):
    return {'course_id':self.course_id, 'course_n_seq':self.course_n_seq, 'video_n_id':video_n_id}

  def get_url(self, video_n_id):
    url_dict = self.get_url_dict(video_n_id)
    url = self.url_base %url_dict
    return url
  
  def issue_command(self, video_n_id):
    url = self.get_url(video_n_id)
    command_base = 'chromium %s' %url
    print command_base
    #os.system(command_base)

  def feed_in_video_n_ids(self, video_n_ids):
    self.video_n_ids = video_n_ids

  def set_in_between_pause(self, in_between_pause):
    try:
      self.in_between_pause = int(in_between_pause)
    except ValueError:
      self.in_between_pause = None

  def get_pause_time_or_default(self, in_between_pause = None):
    try:
      in_between_pause = int(in_between_pause)
    except ValueError:
      in_between_pause = None
    if in_between_pause == None:
      if self.in_between_pause != None:
        in_between_pause = self.in_between_pause
      else:
        in_between_pause = self.DEFAULT_IN_BETWEEN_DOWNLOAD_PAUSE
    return in_between_pause
    
  def start_downloading_n_ids(self, in_between_pause = None):
    for video_n_id in self.video_n_ids:
      self.issue_command(video_n_id)
      time.sleep(self.get_pause_time_or_default(in_between_pause))
    

class CoursesDataPicker(object):
  
  def __init__(self):
    self.dlVideoObjs = []
    self.read_json_data_file()
    self.stock_courses_to_videodownloader()


  def read_json_data_file(self):
    json_filename = COURSES_DATA_JSON_FILENAME
    fp = open(json_filename)
    course_jsondict = json.load(fp=fp, encoding='UTF-8')
    self.courses = []
    n_id = course_jsondict['course_id']
    n_seq = course_jsondict['course_n_seq']
    dlVideoObj = VideoCourseDownloader(n_id, n_seq)
    video_n_ids = course_jsondict['video_n_ids']
    dlVideoObj.feed_in_video_n_ids(video_n_ids)
    self.courses.append(dlVideoObj)
      
  def stock_courses_to_videodownloader(self):
    for course in self.courses:
      dlVideoObj = VideoCourseDownloader(course.id, course.course_n_seq)
      dlVideoObj.feed_in_video_n_ids(course.video_n_ids)
      self.dlVideoObjs.append(dlVideoObj)

  def start_courses_download_process(self):
    for dlVideoObj in self.dlVideoObjs:
      dlVideoObj.start_downloading_n_ids()
    
if __name__ == '__main__':
  CoursesDataPicker().start_courses_download_process()
