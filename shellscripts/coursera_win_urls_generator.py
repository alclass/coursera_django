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
  
  course_id = None
  course_n_seq = None
  
  def return_dict_course_id_and_course_n_seq(self):
    return {'course_id':self.course_id, 'course_n_seq':self.course_n_seq}
    
  def form_abs_url_to_lecture_index(self):
    return url_base %self.return_dict_course_id_and_course_n_seq() 
    
          
class CourseIdOnFolderFetcher(object):
  
  def __init__(self):
    self.read_folder_and_parse_course_ids()
    # self.chrome_open_five_at_a_time()
    
  def read_folder_and_parse_course_ids(self):
    folder_path = 'G:/coursera.org/'
    folder_contents = os.listdir(folder_path)
    folders =[]
    for content in folder_contents:
      content_abspath = os.path.join(folder_path, content)
      if os.path.isdir(content_abspath):
        folders.append(content_abspath)
    course_ids = []; counter = 0
    for folder in folders:
      try:
        last_word = folder.split(' ')[-1]
        if last_word.find('-') < 0:
          continue 
        try:
          # last_word must have an int after a '-' (dash): for the url is composed of the course_id plus a course_n_seq (ex. posa-001)
          pp = last_word.split('-')
          if len(pp) != 2:
            continue
          int(pp[-1])
          course = CourseraCourse()
          course.course_id = pp[0]
          course.course_n_seq = pp[1]
          counter += 1  
          print counter, course.form_abs_url_to_lecture_index()
          #course_ids.append(course_id)
        except ValueError:
          continue
      except IndexError:
        continue
      
            
if __name__ == '__main__':
  CourseIdOnFolderFetcher()