#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 27/06/2013

@author: friend
'''

import coursera_grabber_mod as grabber


def test_read_from_webroot_html(coursera_grabber):
  coursera_grabber.restart_items_by_reading_htmlwebroot_source(coursera_grabber.DEFAULT_COURSERA_ITEMS_WEBROOT_HTML_FILENAME)
  print 'test_read_from_webroot_html(coursera_grabber):'
  coursera_grabber.print_stocked_courses_urls() 
  
def test_read_from_txt(coursera_grabber):
  txt_filename = 'test_txt_of_coursera_items.txt'
  coursera_grabber.restart_items_by_reading_txt_source(txt_filename)
  print 'test_read_from_txt(coursera_grabber):'
  coursera_grabber.print_stocked_courses_urls() 

def test(): 
  coursera_grabber = grabber.CourseraRootCourseGrabber()
  test_read_from_webroot_html(coursera_grabber)
  test_read_from_txt(coursera_grabber)
  
if __name__ == '__main__':
  test()

