#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 27/06/2013

@author: friend
'''

import os, re, time

class CourseUndeterminedAttributes(object):
  pass

class CourseAttributes(object):
  
  url_base_lecture_index = 'https://class.coursera.org/%(course_id)s-%(course_n_seq)s/lecture/index/'
  name_id = None
  n_seq   = None
  def __str__(self):
    return self.__unicode__()
  
  def form_url_to_lecture_index(self):
    return self.url_base_lecture_index %{'course_id':self.name_id, 'course_n_seq':self.n_seq}  
  
  def __unicode__(self):
    outstr = '''course_id = %s (seq=%s)''' %(self.name_id, self.n_seq)
    return outstr

class CourseraRootCourseGrabber(object):

  re_text_to_find = 'class[.]coursera[.]org/(\w+)[-](\d+)/auth/' # auth_redirector?type=login&subtype=normallecture_id=(\w+)'
  re_compiled_text_to_find = re.compile(re_text_to_find) 
  course_root_htmlfilename = 'Your Courses   Coursera.html'  

  COURSERA_ROOT_SOURCE = 1
  COURSERA_COURSES_IN_A_TXT = 2

  def __init__(self):
    self.unique_course_id_dict = {} 

  def process_by(self, items_source, **extra):
    if items_source == self.COURSERA_ROOT_SOURCE:
      self.stock_all_courses_in_dict_from_webroot()
    elif items_source == self.COURSERA_COURSES_IN_A_TXT:
      if extra.has_key('filename'):
        filename = extra['filename']
        self.stock_all_courses_in_dict_from_txt(filename)
    self.transpose_course_dict_stock_to_tuple_list()

  def stock_all_courses_in_dict_from_txt(self, filename):
    lines = open(filename).readlines()
    for line in lines:
      # should be a json! Update this!
      pass

  def stock_all_courses_in_dict_from_webroot(self):
    text = open(self.course_root_htmlfilename).read()
    re_find_obj = self.re_compiled_text_to_find.finditer(text)
    # for i, each in enumerate(re_find_obj):
    for each_re_found in re_find_obj:
      course_id    = each_re_found.group(1)
      course_n_seq = each_re_found.group(2)
      # print course_id , course_n_seq
      if self.unique_course_id_dict.has_key(course_id):
        continue
      course = CourseAttributes()
      course.name_id = course_id
      course.n_seq   = course_n_seq
      self.unique_course_id_dict[course_id] = course

  def transpose_course_dict_stock_to_tuple_list(self):      
    self.course_tuple_list = [] 
    # print len(self.unique_course_id_dict)
    self.course_tuple_list = self.unique_course_id_dict.items()
    self.course_tuple_list.sort(key = lambda x : x[0])
    # print len(self.course_tuple_list)
    
  def print_stocked_courses(self):
    for course_tuple in self.course_tuple_list:
      course = course_tuple[1]
      print course.form_url_to_lecture_index()

  def open_course_lecture_index_page_one_by_one(self):
    course_objs = zip(*self.course_tuple_list)[1]
    for course in course_objs:
      url = course.form_url_to_lecture_index()
      command = 'chromium "%s"' %url
      print command
      ans = raw_input('Press [ENTER] to open page above or n/N to jump ahead next, not opening it. ')
      if ans in ['n', 'N']:
        continue
      os.system(command)
      # time.sleep(120)
        

if __name__ == '__main__':
  coursera_root = CourseraRootCourseGrabber()
  coursera_root.open_course_lecture_index_page_one_by_one()  

