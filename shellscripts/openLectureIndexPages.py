#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 29/06/2013

@author: friend
'''
import sys, time
from coursera_grabber_mod import CourseraRootCourseGrabber

class LectureIndexOpener(object):

  def __init__(self):
    self.grabber = CourseraRootCourseGrabber()
    
  def openLectureIndexPagesByTxtCourseraItemsSourceFromSysArg(self):
    txt_filename = sys.argv[1]
    self.grabber.restart_items_by_reading_txt_source(txt_filename)
    self.grabber.print_stocked_courses_urls()
    ans = raw_input('Do you accept open them above in Chrome with a 2-min delay each ? (Y/n) ')
    if ans in ['n','N']:
      return
    self.openLectureIndexPagesForGivenCourses()

  def openLectureIndexPagesForGivenCourses(self):
    for course_tuple in self.grabber.course_tuple_list:
      coursera_item_obj = course_tuple[1]
      coursera_item_obj.open_course_lecture_index_page_in_browser()
      time.sleep(2 * 60)

def process():
  lecture_index_opener = LectureIndexOpener()
  lecture_index_opener.openLectureIndexPagesByTxtCourseraItemsSourceFromSysArg()
    
if __name__ == '__main__':
  process()
