#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

This module contains the BrowserOpener class.

What does it do?
The BrowserOpener class does the following:
1) look up all courses that have already finished and form a list with them;
2) look up all courses that are listed on Coursera's Web Root Index;
   For the time being, this page is save from Firefox with the "Select-All" plus "View Source" help.
   This is because the Web Root Index is Ajax, ie, it brings courses as the user moves down the page.
3) Having these 2 lists, ie, the "Finished Courses" plus the "Current Listed Courses", it subtracts the former
   from the latter and the result is a list of courses that will be opened in a browsers.
   
4) The browser default here is "chromium" in Linux or "chrome.exe" in Windows. (The Windows part is not polished yet.)

5) The script issues each Course's lecture/index page, one at a time, counting 10 seconds in-between from each one, and 
   stopping when N pages have been issued, to wait for the user to hit [ENTER] to continue to the next N pages.
   
   N is default to 7, ie, at each 7 pages, the program will wait the user's action to continue.

===============
In a nut shell:
===============
  This script will open the lecture/index pages (the pages containing courses' video download links),
  from the command line, via a Web Browser.

Created on 27/06/2013

@author: friend
'''

import os,  time
import __init__
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

  #COURSE_FINISHED_REGISTRY_DIR_ABSPATH = 'C:/Users/up15/Downloads/coursera/Courses Finished/'
  COURSE_FINISHED_REGISTRY_DIR_ABSPATH = '/media/SAMSUNG_/coursera.org/aaa Triage/Courses Finished/'
  
  def __init__(self):
    self.verify_course_finished_status()
    self.stock_urls_to_open_next()
    self.chrome_open_n_at_a_time()
    
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
    tuplestextfile = os.path.join(ls.get_coursera_data_dir_ospath(), 'Coursera tuples courseid and seq.txt')
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

  def chrome_open_n_at_a_time(self, n_to_open_at_a_time = 7):
    '''
    '''
    #os.chdir('C:/Program Files (x86)/Google/Chrome/Application/')
    total = len(self.stock_urls_to_chrome_open)
    for counter, url in enumerate(self.stock_urls_to_chrome_open):
      #comm = 'chrome.exe "%s"' %url
      comm = 'chromium "%s"' %url
      print counter+1, 'of', total, url
      print comm
      os.system(comm)
      print 'Waiting 10 seconds until next browser-page-opening.'
      time.sleep(10)
      if (counter + 1) % n_to_open_at_a_time == 0:
        ans = raw_input(' Press [ENTER] to continue. ')
        ans

if __name__ == '__main__':
  BrowserOpener()
