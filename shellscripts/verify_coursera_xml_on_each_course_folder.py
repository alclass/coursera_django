#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 27/06/2013

@author: friend
'''

# import defaults
import os, sys
from lxml import etree 

this_file_path = os.path.abspath(__file__)
THIS_DIR_PATH, filename = os.path.split(this_file_path)
try:
  PARENT_DIR_PATH = '/'.join(THIS_DIR_PATH.split('/')[:-1])
except IndexError:
  PARENT_DIR_PATH = THIS_DIR_PATH

sys.path.append(PARENT_DIR_PATH)
#import local_settings as ls

import popup_course_folder as cfolder

COURSERA_COURSE_INFO_XML_FILENAME = 'coursera_course.xml'

def verify_coursera_info_xml():
  etree.XML(COURSERA_COURSE_INFO_XML_FILENAME)
  # parse it!
  
def process():
  course_repo = cfolder.CourseRepo()
  course_repo.read_courses_xml_data_file()
  for course in course_repo.course_dict.keys():
    os.chdir(course.get_abspath_on_external_disk())
    xmlfiles = os.listdir('*.xml')
    if COURSERA_COURSE_INFO_XML_FILENAME not in xmlfiles:
      # copy it there
      continue
    else:
      verify_coursera_info_xml() 
  
  
if __name__ == '__main__':
  process()
