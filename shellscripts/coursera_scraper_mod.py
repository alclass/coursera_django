#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 27/06/2013

@author: friend
'''

import os
this_file_path = os.path.abspath(__file__)
THIS_DIR_PATH, filename = os.path.split(this_file_path)
try:
  PARENT_DIR_PATH = '/'.join(THIS_DIR_PATH.split('/')[:-1])
except IndexError:
  PARENT_DIR_PATH = THIS_DIR_PATH

import local_settings as ls

os.environ['DJANGO_SETTINGS_MODULE'] = 'coursera_django.settings' # 'PBCodeInspectorStats.settings'
#import coursera_django.settings as settings
from coursera_app.models import Course # Inst  

htmltrunk = '''
<head>
<body>
<div class="coursera-course-listing-main">
  <h3 class="coursera-course-listing-name">
    <a href="/course/friendsmoneybytes">
      Networks: Friends, Money, and Bytes
    </a>
  </h3>
  <div class="coursera-course-listing-progress">
    <span style="left: 1px;" class="progress-label">Feb 4th</span>
    <span style="right: 1px;" class="progress-label">Jun 17th</span>
    <div class="progress-line"></div>
    <div style="left:100%" class="progress-marker"></div>
    <div style="width:100%;" class="progress-bar"></div>
  </div>
  <div class="coursera-course-listing-statement"></div>
  <div style="width:435px;" class="coursera-course-listing-more coursera-course-my-listing-more">
    <a href="/princeton" class="coursera-course-listing-university internal-home">
      Princeton University
    </a>
  </div>
</div>
</body>
</head>
'''

#import os, re #, time

#from coursera_grabber_functions import either_filename_or_default 

import lxml.html
def test1():
  page = lxml.html.fromstring(htmltrunk)
  divtext = page.xpath('//body/div/text()')[0]
  print 'divtext', divtext

from lxml import etree
#from lxml import BytesIO
def test2():
  some_xml_data = "<root>data</root>"
  root = etree.fromstring(some_xml_data)
  print(root.tag)
  print etree.tostring(root)

from io import BytesIO
def test3():
  #root = etree.fromstringlist(htmltrunk)
  some_file_like = BytesIO(htmltrunk)
  for _, element in etree.iterparse(some_file_like): # anonymous "_" is variable "event"
    if element.tag == 'div':
      print 'tag', element.tag, 'text', element.text

def test4():
  root = etree.HTML(htmltrunk)
  elements = root.findall(".//div[@class]")
  for each in elements:
    print each.get('class')

class CourseraCourse(object):
  pass

def is_course_id_good(course_id):
  if ' ' in course_id:
    return False
  if '=' in course_id:
    return False
  if '&' in course_id:
    return False
  if '?' in course_id:
    return False
  if course_id.startswith('auth_redirector'):
    return False
  return True

def process_element(element):
  elements = element.getchildren()
  # first element of incoming element <div> is expected to be <h3>
  h3 = elements[0]
  # first element is expected to be <h3>, if not, return
  if h3.tag != 'h3':
    return None
  print 'Got <h3>', h3
  elements = h3.getchildren()
  a = elements[0]
  # first element of h3 is expected to be <a>, if not, return
  if a.tag != 'a':
    return None
  url   = a.get('href')
  course_id = url.split('/')[-1]
  if not is_course_id_good(course_id):
    return None
  course = Course()
  course.course_id = course_id
  course.title = a.text
  return course

def test5():
  courses = []
  coursera_root_page_filepath = ls.get_default_coursera_stocked_root_webpage_osfilepath()
  html_text = open(coursera_root_page_filepath).read() 
  root = etree.HTML(html_text)
  elements = root.findall(".//div[@class]")
  for element in elements:
    classname = element.get('class')
    if classname == 'coursera-course-listing-main':
      course_obj = process_element(element)
      if course_obj != None:
        courses.append(course_obj)

  for i, course_obj in enumerate(courses):
    print i, course_obj.course_id
    print course_obj.title
    

if __name__ == '__main__':
  test5()
  pass
