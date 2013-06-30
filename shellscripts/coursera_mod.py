#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 27/06/2013

@author: friend
'''

import defaults
import os

class CourseraCourse(object):
  
  url_base_course_root_page = 'https://class.coursera.org/%(course_id)s-%(course_n_seq)s/'
  url_base_lecture_index    = url_base_course_root_page + 'lecture/index/'
  
  def __init__(self, course_id, course_n_seq = '001'):
    self.course_id    = course_id
    self.course_n_seq = course_n_seq

  def set_course_title(self, course_title):
    self.course_title = course_title

  def set_start_date(self, start_date):
    self.start_date = start_date

  def set_duration_in_weeks(self, duration_in_weeks):
    self.duration_in_weeks = duration_in_weeks
    
  def get_tuple_attrs_as_dict(self):
    return {'course_id':self.course_id, 'course_n_seq':self.course_n_seq}
  
  def form_url_to_lecture_index(self):
    return self.url_base_lecture_index %self.get_tuple_attrs_as_dict()  

  def get_browser(self):
    if self.browser == None:
      return defaults.DEFAULT_BROWSER
    return self.browser 

  def set_browser(self, browser):
    if browser not in defaults.AVAILABLE_BROWSERS:
      return
    self.browser = browser

  def open_course_lecture_index_page_in_browser(self):
    url = self.form_url_to_lecture_index()
    command = '%s "%s"' %(self.get_browser(), url)
    print command
    os.system(command)
  
  def __eq__(self, obj):
    try:
      if self.course_id == obj.course_id and self.course_n_seq == self.course_n_seq:
        return True
    except AttributeError:
      pass
    return False 
  
  def __str__(self):
    return self.__unicode__()
  
  def __unicode__(self):
    outstr = '''course_id = %s (seq=%s)''' %(self.course_id, self.course_n_seq)
    return outstr

        
if __name__ == '__main__':
  pass
