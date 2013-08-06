#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 27/06/2013

@author: friend
'''

import os, re #, os, time

#from coursera_grabber_functions import either_filename_or_default 
from coursera_grabber_functions import either_filename_or_default
from coursera_grabber_functions import get_filename_param_or_default
from coursera_mod import CourseraCourse

import __init__
import local_settings as ls

class CourseraItemsReadSourceUnknown(ValueError):
  pass

class CourseraWebRootCourseExtractor(object):

  re_text_to_find = 'class[.]coursera[.]org/(\w+)[-](\d+)/auth/' # auth_redirector?type=login&subtype=normallecture_id=(\w+)'
  re_compiled_text_to_find = re.compile(re_text_to_find) 

  DEFAULT_COURSERA_ITEMS_WEBROOT_HTML_FILENAME = ls.get_default_coursera_stocked_root_webpage_osfilepath()  
  DEFAULT_COURSERA_ITEMS_TXT_FILENAME          = 'Coursera Items.txt' 
  DEFAULT_COURSERA_ITEMS_JSON_FILENAME         = 'Coursera Items.json' 

  COURSERA_COURSES_IN_WEBROOT_HTML = 1
  COURSERA_COURSES_IN_STOCKED_TXT  = 2
  COURSERA_COURSES_IN_STOCKED_JSON = 3

  def __init__(self):
    '''
      At construction time, initialize dict self.unique_course_id_dict 
    '''
    self.empty_items()

  def empty_items(self):
    self.unique_course_id_dict = {} 
    self.course_tuple_list = [] 

  def restart_items_by_reading_txt_source(self, course_items_source_txt_filename):
    '''
    Via this method, there is no default filename "second option"
    However, if course_items_source_txt_filename does not exist, an exception will be raised
    If txt file does exist, method will:
      1) invoke empty items
      2) call process chain method fill_in_items_by_read_source() with ajusted arguments 
    '''
    if not os.path.isfile(course_items_source_txt_filename):
      raise CourseraItemsReadSourceUnknown, 'file %s does not exist.' %(course_items_source_txt_filename)
    self.empty_items()
    self.fill_in_items_by_read_source(self.COURSERA_COURSES_IN_STOCKED_TXT, filename = course_items_source_txt_filename) 

  def restart_items_by_reading_htmlwebroot_source(self, course_items_source_htmlwebroot_filename=None):
    course_items_source_htmlwebroot_filename = self.return_course_items_source_htmlwebroot_filename_or_default_or_raise(course_items_source_htmlwebroot_filename)
    self.empty_items()
    self.fill_in_items_by_read_source(self.COURSERA_COURSES_IN_WEBROOT_HTML, filename = course_items_source_htmlwebroot_filename) 
  
  def fill_in_items_by_read_source(self, read_source_id, **extra_params):
    '''
      This is a 2-step process:
      1) Get self.unique_course_id_dict according to its possible source (ie, HTML, text, json)
      2) Transpose this dict {*course_id:course_n_seq} to a tuple list [*(course_id,course_n_seq)]
    '''
    self.fill_in_dict_items_by_read_source(read_source_id, **extra_params)
    self.transpose_course_dict_stock_to_tuple_list()

  def fill_in_dict_items_by_read_source(self, read_source_id, **extra_params):
    '''
      This method aims to fill up course items dict represented by self.unique_course_id_dict
      To do so, it will call a specialized method according to data's possible source (ie, HTML, text, json)
    '''

    if read_source_id == self.COURSERA_COURSES_IN_WEBROOT_HTML:
      course_items_source_html_filename = get_filename_param_or_default(extra_params, self.DEFAULT_COURSERA_ITEMS_WEBROOT_HTML_FILENAME) # default: must_exist_locally = True
      self.read_and_stock_dict_course_items_from_webroot_source(course_items_source_html_filename)
      return

    elif read_source_id == self.COURSERA_COURSES_IN_STOCKED_TXT:
      course_items_source_txt_filename = get_filename_param_or_default(extra_params, self.DEFAULT_COURSERA_ITEMS_TXT_FILENAME) # default: must_exist_locally = True
      self.read_and_stock_dict_course_items_from_txt_source(course_items_source_txt_filename)
      return

      # raise CourseraItemsReadSourceUnknown, 'Parameter filename for stock txt is missing'

    elif read_source_id == self.COURSERA_COURSES_IN_STOCKED_JSON:
      course_items_source_json_filename = get_filename_param_or_default(extra_params, self.DEFAULT_COURSERA_ITEMS_JSON_FILENAME) # default: must_exist_locally = True
      self.read_and_stock_dict_course_items_from_json_source(course_items_source_json_filename)
      return

    raise CourseraItemsReadSourceUnknown, 'CourseraItemsReadSourceUnknown'

  def return_course_items_source_htmlwebroot_filename_or_default_or_raise(self, course_items_source_htmlwebroot_filename=None):
    '''
    Private method that returns 
     course_items_source_htmlwebroot_filename or its default
     or raise an exception if neither file nor default exists
    '''
    if course_items_source_htmlwebroot_filename == None:
      course_items_source_htmlwebroot_filename = ls.get_default_coursera_stocked_root_webpage_osfilepath()
    if not os.path.isfile(course_items_source_htmlwebroot_filename):
      raise CourseraItemsReadSourceUnknown, 'file %s does not exist.' %(course_items_source_htmlwebroot_filename)
    return course_items_source_htmlwebroot_filename
  
  def read_and_stock_dict_course_items_from_webroot_source(self, course_items_source_htmlwebroot_filename=None):
    '''
    1st read option: Course items are withdrawn from HTML Webroot file source
    '''
    course_items_source_htmlwebroot_filename = self.return_course_items_source_htmlwebroot_filename_or_default_or_raise(course_items_source_htmlwebroot_filename)
    text = open(course_items_source_htmlwebroot_filename).read()
    re_find_obj = self.re_compiled_text_to_find.finditer(text)
    for each_re_found in re_find_obj:
      course_id    = each_re_found.group(1)
      course_n_seq = each_re_found.group(2)
      try:
        # this below should not raise ValueError, if it does, continue without adding it to dict
        int(course_n_seq)
      except ValueError:
        continue
      if self.unique_course_id_dict.has_key(course_id):
        continue
      coursera_item_obj = CourseraCourse(course_id, course_n_seq)
      self.unique_course_id_dict[course_id] = coursera_item_obj

  def read_and_stock_dict_course_items_from_txt_source(self, course_items_source_txt_filename):
    '''
    2nd read option: Course items are brought in from TXT file source
    '''
    lines = open(course_items_source_txt_filename).readlines()
    for line in lines:
      if line.startswith('#'):
        continue
      # clean up line
      line = line.rstrip('\t\r\n')
      try:
        twovalues = line.split(',')
        course_id = twovalues[0]  
        course_id = course_id.lstrip().rstrip()
        course_n_seq = twovalues[1]
        course_n_seq = course_n_seq.lstrip().rstrip()
        try:
          # this below should not raise ValueError, if it does, continue without adding it to dict
          int(course_n_seq)
        except ValueError:
          continue
        coursera_item_obj = CourseraCourse(course_id, course_n_seq)
      except IndexError:
        continue
      self.unique_course_id_dict[course_id] = coursera_item_obj

  def read_and_stock_dict_course_items_from_json_source(self, course_items_source_json_filename):
    '''
    2nd read option: Course items are withdrawn from TXT file source
    '''
    pass

  def transpose_course_dict_stock_to_tuple_list(self):      
    self.course_tuple_list = self.unique_course_id_dict.items()
    self.course_tuple_list.sort(key = lambda x : x[0])
    
  def print_stocked_courses_urls(self):
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

  def write_to_txtfile_current_stocked_coursera_items(self, txt_filename=None):
    '''
      Write stocked course items to a txt file source
    '''
    n_items = len(self.course_tuple_list)
    if n_items == 0:
      return
    txt_filename = either_filename_or_default(txt_filename, self.DEFAULT_COURSERA_ITEMS_TXT_FILENAME, must_exist_locally = False)
    print 'Writing %d lines to %s' %(n_items, txt_filename)
    fileobj = open(txt_filename, 'w')
    for tuple_item in self.course_tuple_list:
      # the 1st tuple element is course_id, the second is an object with at least attributes course_id and course_n_seq 
      course_item_obj = tuple_item[1]
      line = '%(course_id)s,%(course_n_seq)s' %course_item_obj.get_tuple_attrs_as_dict()
      fileobj.write(line + '\n')
    fileobj.close()

def process():
  extractor = CourseraWebRootCourseExtractor()
  extractor.restart_items_by_reading_htmlwebroot_source()  
  extractor.write_to_txtfile_current_stocked_coursera_items()        
        
if __name__ == '__main__':
  process()
