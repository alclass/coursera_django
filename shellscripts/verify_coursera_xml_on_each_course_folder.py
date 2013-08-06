#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 27/06/2013

@author: friend
'''

# import defaults
import os, sys
from lxml import etree 

import __init__

import local_settings as ls


COURSERA_COURSE_INFO_XML_FILENAME = 'coursera_course.xml'


class CourseraCourse(object):
  
  def __init__(self, course_id, course_n_seq):
    self.course_id    = course_id
    self.course_n_seq = course_n_seq


class ProgramFlowError(ValueError):
  pass
  
def instantiate_CourseraCourse_from_folder_name_or_None(folder_name):
  try:
    pp = folder_name.split(' ')
    course_id_and_course_n_seq = pp[-1]
    ppp = course_id_and_course_n_seq.split('-')
    course_id = '-'.join(ppp[:-1])
    course_n_seq = ppp[-1]
    # test it to be an int!
    int(course_n_seq)
    return CourseraCourse(course_id, course_n_seq)
  except IndexError:
    return None
  except ValueError:
    return None
  raise ProgramFlowError, 'Something Exception is missing in source code to avoid this exception raising, that Program Flow should not have crossed this "raise" instruction' 
  

def verify_coursera_courses_info_xml():
  os.chdir(ls.COURSERA_EXTERNAL_DISK_ROOTDIR_ABSPATH)
  entries = os.listdir('.')
  for entry in entries:
    if not os.path.isdir(entry):
      continue
    coursera_course = instantiate_CourseraCourse_from_folder_name_or_None(entry)
    if coursera_course == None:
      continue
    # chdir_into_coursera_course_folder(coursera_course)
    
    
  
def process():
  verify_coursera_courses_info_xml()
  
if __name__ == '__main__':
  process()
