#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 27/06/2013

@author: friend
'''

import os, time

this_file_path = os.path.abspath(__file__)
THIS_DIR_PATH, filename = os.path.split(this_file_path)
try:
  PARENT_DIR_PATH = '/'.join(THIS_DIR_PATH.split('/')[:-1])
except IndexError:
  PARENT_DIR_PATH = THIS_DIR_PATH

import local_settings as ls

url_base = 'https://class.coursera.org/%(course_id)s-%(course_n_seq)s/lecture/index'        

class CourseraCourse(object):

  finished_course_ids_list = []
  
  def __init__(self, course_id=None, course_n_seq=None):
    self.course_id    = course_id
    self.course_n_seq = course_n_seq
    
  @staticmethod
  def add_to_finished_course_ids_list(course):
    if type(course) == CourseraCourse:
      CourseraCourse.finished_course_ids_list.append(course.course_id)
    else:
      raise TypeError, 'Method add_to_finished_course_ids_list(course) receive a non-CourseraCourse object'

  def __eq__(self, other_course):
    if self.course_id == other_course.course_id and self.course_n_seq == other_course.course_n_seq:
      return True
    return False 
  
  def return_dict_course_id_and_course_n_seq(self):
    return {'course_id':self.course_id, 'course_n_seq':self.course_n_seq}
    
  def form_abs_url_to_lecture_index(self):
    return url_base %self.return_dict_course_id_and_course_n_seq() 
    
          
class BrowserOpener(object):

  COURSE_FINISHED_REGISTRY_DIR_ABSPATH = 'C:/Users/up15/Downloads/coursera/Courses Finished/'
  
  def __init__(self):
    self.verify_course_finished_status()
    self.stock_urls_to_open_next()
    self.chrome_open_five_at_a_time()
    
  def verify_course_finished_status(self):
    os.chdir(self.COURSE_FINISHED_REGISTRY_DIR_ABSPATH)
    contents = os.listdir('.')
    for filename in contents:
      #print 'finished folder', filename
      if os.path.isfile(filename):
        try:
          content, _ = os.path.splitext(filename)
          id_and_n_seq = content.split(' ')[-1]
          pp = id_and_n_seq.split('-')
          course_n_seq = pp[-1]
          course_id = '-'.join(pp[:-1])
          course = CourseraCourse(course_id, course_n_seq)
          CourseraCourse.add_to_finished_course_ids_list(course)
        except IndexError:
          continue
    print 'Courses Finished', CourseraCourse.finished_course_ids_list 
    print 'Total', len(CourseraCourse.finished_course_ids_list)

  def stock_urls_to_open_next(self):
    self.stock_urls_to_chrome_open = []
    self.courseids_to_open = []
    tuplestextfile = os.path.join(ls.COURSERA_DATA_DIRPATH, 'Coursera tuples courseid and seq.txt')
    tuplelines = open(tuplestextfile).read()
    lines = tuplelines.split('\n')
    for line in lines:
      if line.startswith('#'):
        continue
      try:
        pp = line.split(',')
        course_id = pp[0]
        if course_id in CourseraCourse.finished_course_ids_list:
          print 'Course_id', course_id, 'is finished. Continuing next.'
          continue
        if course_id in self.courseids_to_open:
          continue
        ccourse = CourseraCourse()
        ccourse.course_id = course_id
        try:
          int(pp[1])
        except ValueError:
          continue
        ccourse.course_n_seq = pp[1]
      except IndexError:
        continue
      self.courseids_to_open.append(ccourse.course_id)
      url = ccourse.form_abs_url_to_lecture_index()
      self.stock_urls_to_chrome_open.append(url)

  def chrome_open_five_at_a_time(self):
    os.chdir('C:/Program Files (x86)/Google/Chrome/Application/')
    for counter, url in enumerate(self.stock_urls_to_chrome_open):
      comm = 'chrome.exe "%s"' %url
      print counter+1, url
      print comm
      '''
      os.system(comm)
      print 'Wait 10 sec.'
      time.sleep(10)
      if (counter + 1) % 7 == 0:
        ans = raw_input(' Press [ENTER] to continue. ')
        ans
      '''   

if __name__ == '__main__':
  BrowserOpener()
