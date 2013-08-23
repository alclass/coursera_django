#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

This module contains the BrowserOpener class.

What does it do?
The BrowserOpener class does the following:
1) look up all courses that have already finished and form a list with them;
2) look up all courses that are listed on Coursera's Web Root Index;
   For the time being, this page is saved from Firefox with the "Select-All" plus "View Source" help.
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
import defaults
from coursera_app.models import CourseraCourse
#from coursera_django.defaults import LECTURE_INDEX_INTERPOLATE_URL

class WorkCourse(object):

  finished_course_ids_list = []
  
  def __init__(self, ccourse=None, n_seq=None):
    self.ccourse   = ccourse
    
  @staticmethod
  def add_to_finished_course_ids_list(ccourse):
    if type(ccourse) == CourseraCourse:
      WorkCourse.finished_course_ids_list.append(ccourse.cid)
    else:
      raise TypeError, 'Method add_to_finished_course_ids_list(course) receive a non-CourseraCourse object'

  def __eq__(self, other_course):
    if self.ccourse.cid == other_course.cid and self.ccourse.n_seq == other_course.n_seq:
      return True
    return False 


class BrowserOpener(object):

  #COURSE_FINISHED_REGISTRY_DIR_ABSPATH = 'C:/Users/up15/Downloads/coursera/Courses Finished/'


  def __init__(self, registry_folder_with_finished_courses_abspath=None):
    self.cid_and_n_seq_dict_from_courseras_webrootpage = {}
    self.ccourses_to_open_their_lecture_index_pages_on_browser = []
    #self.set_registry_folder_with_finished_courses_abspath(registry_folder_with_finished_courses_abspath)
    #self.verify_course_finished_status()
    self.fill_in_cid_and_n_seq_dict_from_courseras_webrootpage()
    self.confirm_ccourses_that_are_apt_for_lecture_index_pages_opening_on_browser()
    #self.chrome_open_n_at_a_time()
    
  def set_registry_folder_with_finished_courses_abspath(self, registry_folder_with_finished_courses_abspath=None):
    if registry_folder_with_finished_courses_abspath == None:
      self.registry_folder_with_finished_courses_abspath = ls.COURSE_FINISHED_REGISTRY_DIR_ABSPATH
      return
    self.registry_folder_with_finished_courses_abspath = registry_folder_with_finished_courses_abspath    

  def verify_course_finished_status(self):
    '''
    @deprecated: this method will be removed
    '''
    os.chdir(self.registry_folder_with_finished_courses_abspath)
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
          ccourse = CourseraCourse(course_id, course_n_seq)
          wcourse = WorkCourse(ccourse)
          WorkCourse.add_to_finished_course_ids_list(wcourse)
        except IndexError:
          continue
    print 'Courses Finished', WorkCourse.finished_course_ids_list
    print 'Total', len(WorkCourse.finished_course_ids_list)

  def fill_in_cid_and_n_seq_dict_from_courseras_webrootpage(self):
    '''
    The url-stock comes directly from a text file.
    This text file, in turn, is produced by CourseraWebRootPageScraperMod.py
      ie, they are the courses listed in Coursera's Web Root Course Index Page
    '''
    # tuplestextfile = os.path.join(ls.get_coursera_app_data_dir_abspath(), 'Coursera tuples courseid and seq.txt')
    tuplestextfile = ls.get_default_textfile_with_extracted_ids_and_nseqs_from_coursera_webrootpage_abspath()
    tuplelines = open(tuplestextfile).read()
    lines = tuplelines.split('\n')
    for line in lines:
      if line.startswith('#'):
        continue
      try:
        pp = line.split(',')
        course_id = pp[0]
        if course_id in WorkCourse.finished_course_ids_list:
          print 'Course_id', course_id, 'is finished. Continuing next.'
          continue
        n_seq = int(pp[1])
        if n_seq == 0:
          continue
      except IndexError:
        continue
      except ValueError:
        continue
      self.cid_and_n_seq_dict_from_courseras_webrootpage[course_id]=n_seq
    print "Total courses found at coursera's webrootpage:", len(self.cid_and_n_seq_dict_from_courseras_webrootpage) 

  def get_course_or_create_it_or_None(self, cid, n_seq):
    if n_seq == 0:
      return None
    try:
      ccourse = CourseraCourse.objects.get(cid=cid)
    except CourseraCourse.DoesNotExist:
      ccourse = CourseraCourse()
      ccourse.cid = cid
      ccourse.n_seq = n_seq
      ccourse.save()
      return ccourse
    if ccourse.n_seq == -1:
      ccourse.n_seq = n_seq
    if ccourse.n_seq != n_seq:
      return None
    return ccourse

  def confirm_ccourses_that_are_apt_for_lecture_index_pages_opening_on_browser(self):
    '''
    '''
    ndays = 17
    for cid in self.cid_and_n_seq_dict_from_courseras_webrootpage.keys():
      n_seq = self.cid_and_n_seq_dict_from_courseras_webrootpage[cid]
      #print 'Confirm or not', cid, n_seq,
      ccourse = self.get_course_or_create_it_or_None(cid, n_seq)
      if ccourse == None:
        continue
      #print 'ccourse.finish_date', ccourse.finish_date,
      if ccourse.is_course_finish_date_older_than(ndays):
        # print 'Older than 17 days, not confirming it.'
        continue
      #print 'Not older than 17 days, confirming it now.'
      self.ccourses_to_open_their_lecture_index_pages_on_browser.append(ccourse)
    print 'There are %d courses to open their lecture/index pages.' %len(self.ccourses_to_open_their_lecture_index_pages_on_browser)
    for i, ccourse in enumerate(self.ccourses_to_open_their_lecture_index_pages_on_browser):
      try:
        title = unicode(ccourse)
      except UnicodeEncodeError:
        title = ccourse.title.encode('utf-8')
      print i+1, ccourse.cid, title  

  def chrome_open_n_at_a_time(self, n_to_open_at_a_time = 7):
    '''
    '''
    #os.chdir('C:/Program Files (x86)/Google/Chrome/Application/')
    total = len(self.ccourses_to_open_their_lecture_index_pages_on_browser)
    for counter, ccourse in enumerate(self.ccourses_to_open_their_lecture_index_pages_on_browser):
      #comm = 'chrome.exe "%s"' %url
      url = ccourse.form_abs_url_to_lecture_index()
      comm = 'chromium "%s"' %url
      print counter+1, 'of', total, url
      print comm
      os.system(comm)
      print 'Waiting %d seconds until next browser-page-opening.' %defaults.WAIT_TIME_IN_BETWEEN_PAGE_OPENING
      time.sleep(defaults.WAIT_TIME_IN_BETWEEN_PAGE_OPENING)
      '''
      if (counter + 1) % n_to_open_at_a_time == 0:
        ans = raw_input(' Press [ENTER] to continue. ')
        ans'''

def process():
  browser_opener = BrowserOpener()
  browser_opener.chrome_open_n_at_a_time()

if __name__ == '__main__':
  process()
