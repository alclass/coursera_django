#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 29/06/2013

@author: friend
'''

from coursera_mod import CourseraCourse
from coursera_grabber_mod import CourseraRootCourseGrabber

import unittest
class Test(unittest.TestCase):
  
  def test_empty_items(self):
    '''
    Test grabber when it SHOULD have non empty items
    Here there are 2 subtests:
      ST#1 : items should be empty after constructor 
      ST#2 : items should be empty after method empty_items() is invoked
    '''
    grabber = CourseraRootCourseGrabber()
    # ST#1 : items should be empty after constructor 
    self.assertEqual([], grabber.course_tuple_list)
    grabber.empty_items()
    # ST#2 : items should be empty after method empty_items() is invoked 
    self.assertEqual([], grabber.course_tuple_list)

  def test_non_empty_items(self):
    '''
    Test grabber for non-empty items when it SHOULD NOT have non-empty items
    '''
    grabber = CourseraRootCourseGrabber()
    course_id = 'anycourse'
    course_n_seq = '001'
    coursera_item_obj = CourseraCourse(course_id, course_n_seq)
    # adding one arbitrary course arbitrarily
    grabber.course_tuple_list = [(coursera_item_obj.course_id, coursera_item_obj)] 
    # it must NOT be empty if an item was added to it 
    self.assertNotEqual([], grabber.course_tuple_list)

  def test_saved_txt(self):
    '''
    Here follows this test's rationale:

    :: First (ST#1) SubTest
    1) Read coursera's items from its webroot html page
    2) Write the items to a test text file
    3) Copy items to a 'buffer' list 
    4) Empty items data from the stocking object
    5) Read coursera's items from the given test text file, just writen out above
    6) Assert equality of buffered items with current items read from the test text file in the previous step

    :: Second (ST#2) SubTest
    7) Recopy items to the 'buffer' list 
    8) Again empty items data from the stocking object
    9) Refetch items now via a different method
    10) Again, a second time, assert equality of buffered items with current items read from the test text file in the previous step
    '''
    grabber = CourseraRootCourseGrabber()
    grabber.fill_in_items_by_read_source(grabber.COURSERA_COURSES_IN_WEBROOT_HTML)
    # hardcopy course_tuple_list
    course_tuple_list = grabber.course_tuple_list[:] 
    target_txt_filename = 'test_txt_of_coursera_items.txt'
    grabber.write_to_txtfile_current_stocked_coursera_items(target_txt_filename)
    grabber.empty_items()
    grabber.fill_in_items_by_read_source(grabber.COURSERA_COURSES_IN_STOCKED_TXT, filename = target_txt_filename)
    self.assertEqual(course_tuple_list, grabber.course_tuple_list)
    # test the same items fetch, but via a different method 
    course_tuple_list = grabber.course_tuple_list[:] 
    grabber.restart_items_by_reading_txt_source(target_txt_filename)
    self.assertEqual(course_tuple_list, grabber.course_tuple_list)
    
  def test_saved_json(self):
    '''
    This test's rationale:
    1) Read coursera's items from its webroot html page
    2) Write the items to the default txt file
    3) Copy items to a 'buffer' list 
    4) Empty items data from the stocking object
    5) Read coursera's items from the default txt file, just writen out above
    6) assert equality of buffered items with current items read from txt file in the previous step
    '''
    pass
    
unittest.main()
