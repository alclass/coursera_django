#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 27/06/2013

@author: friend
'''

# import defaults
import datetime, os, time

import __init__
import local_settings as ls

from coursera_app.models import CourseraCourse, Instructor, Institution, Category

from ClassExceptionsMod import CourserasRepoRootFolderHasNotBeenFoundOrInexists 
import xml.etree.ElementTree as ET

class CourseraXmlInfoGenerator(object):

  COURSERA_COURSE_INFO_WEB_PAGE_URL_BASE = 'https://www.coursera.org/course/%(course_id)s'
  
  def __init__(self, coursera_repo_root_dir=None):
    self.set_coursera_repo_root_dir(coursera_repo_root_dir)
    self.xml_root = ET.Element('coursera_course')
  
  def set_coursera_repo_root_dir(self, coursera_repo_root_dir=None):
    self.coursera_repo_root_dir = coursera_repo_root_dir
    if self.coursera_repo_root_dir == None:
      self.coursera_repo_root_dir = ls.get_coursera_external_disk_rootdir_abspath()
    if not os.path.isdir(self.coursera_repo_root_dir):
      raise CourserasRepoRootFolderHasNotBeenFoundOrInexists, CourserasRepoRootFolderHasNotBeenFoundOrInexists.show_error_msg(self.external_disk_root_dir)  
      
  def show_xml_tags_info(self):
    '''
    The XML per course is the following:
    
  <coursera_courses>
    <course id="course_id" n_seq="course_n_seq">
      <title>title</title>
      <description>description text</description>
      <start_date>yyyy-mm-dd</start_date>
      <duration_in_weeks>n_weeks</duration_in_weeks>
      <workload_in_hours_per_day>n_hours_per_day</workload_in_hours_per_day>
      <professors>
        <professor id="professor1_id" institution_id="institutionA_id">professor1</professor>
        <professor id="professor2_id" institution_id="institutionB_id">professor2</professor>
        <professor id="professor3_id" institution_id="institutionC_id">professorN</professor>
      </professors>
      <institutions>
        <institution institution_id="inst1_id">institution1</institution>
        <institution institution_id="inst2_id">institution2</institution>
        <institution institution_id="instN_id">institutionN</institution>
      </institutions>
      <categories>
        <category category_id="catg1_id">category1</category>
        <category category_id="catg2_id">category2</category>
        <category category_id="catgN_id">categoryN</category>
      </categories>
    <course>
  </coursera_courses>
    '''
    return self.show_xml_tags_info.__str__

  def fill_in_xml_tags_for_course(self, xml_course):
    '''
    '''
    course_tag_attribs = {'id':xml_course.cid, 'n_seq':str(xml_course.n_seq)}
    course_tag = ET.SubElement(self.xml_root, 'course', course_tag_attribs)
    
    title_tag = ET.SubElement(course_tag, 'title')
    title_tag.text = xml_course.title

    description_tag = ET.SubElement(course_tag, 'description')
    description_tag.text = xml_course.description
    
    start_date_tag = ET.SubElement(course_tag, 'start_date')
    start_date_tag.text = xml_course.get_start_date_as_dashed_yyyy_mm_dd()
    
    duration_in_weeks_tag = ET.SubElement(course_tag, 'duration_in_weeks')
    duration_in_weeks_tag.text = str(xml_course.duration_in_weeks)

    workload_in_hours_per_day_tag = ET.SubElement(course_tag, 'workload_in_hours_per_day')
    workload_in_hours_per_day_tag.text = str(xml_course.workload_in_hours_per_day)
    
    self.fill_in_xml_tags_for_the_professors_trunk(xml_course, course_tag)

    self.fill_in_xml_tags_for_the_institutions_trunk(xml_course, course_tag)
     
    self.fill_in_xml_tags_for_the_categories_trunk(xml_course, course_tag)


  def fill_in_xml_tags_for_the_professors_trunk(self, xml_course, course_tag):
    '''
    '''    
    professors_tag = ET.SubElement(course_tag, 'professors')
    for professor in xml_course.instructors.all():
      institution = professor.get_1st_institution()
      professor_tag_attribs = {'id':str(professor.id), 'institution_id':str(institution.id)} # professor.institution_id
      professor_tag = ET.SubElement(professors_tag, 'professor', professor_tag_attribs)
      professor_tag.text = professor.name


  def fill_in_xml_tags_for_the_institutions_trunk(self, xml_course, course_tag):
    '''
    '''    
    institutions_tag = ET.SubElement(course_tag, 'institutions')
    for institution in xml_course.institutions.all():
      institution_tag_attribs = {'id':str(institution.id)}
      institution_tag = ET.SubElement(institutions_tag, 'institution_tag', institution_tag_attribs)
      institution_tag.text = institution.name

  def fill_in_xml_tags_for_the_categories_trunk(self, xml_course, course_tag):
    '''
    '''    
    categories_tag = ET.SubElement(course_tag, 'institutions')
    for category in xml_course.categories.all():
      category_tag_attribs = {'id':str(category.id)}
      category_tag = ET.SubElement(categories_tag, 'category_tag', category_tag_attribs)
      category_tag.text = category.name

  def save_xml_as_file(self):
    xml_filename = '%s.xml' %time.ctime()
    xmlfile_abspath = os.path.join(self.coursera_repo_root_dir, xml_filename)
    print 'Writing Coursera Course Info XML', xmlfile_abspath
    xml_tree = ET.ElementTree(self.xml_root)
    xml_tree.write(xmlfile_abspath)
  
  def __unicode__(self):
    outstr = u'''
    '''
    return outstr
  
  def __str__(self):
    return self.__unicode__()
  

def make_test_course():

  course = CourseraCourse()
  course.cid = 'introstats2'
  course.n_seq = 1 # '001'

  course.title = 'Introduction to Statistics'
  course.description = 'Introduction to Statistics is nice course!'

  course.start_date = datetime.date(2013, 4, 5)
  course.duration_in_weeks = 8
  # course.workload_in_hours_per_day = 3
  course.workload_in_hours_per_week = 3

  institution = Institution()
  institution.id = 10
  institution.name = 'Harvard Univ.'
  course.institutions = [institution] 

  professor =  Instructor()
  professor.id = 10
  professor.name = 'John Joey'
  professor.institution = institution
  course.instructors = [professor]

  category =  Category()
  category.id = 10
  category.name = 'Mathematics & Statistics'
  course.categories = [category]
  
  print 'course', course
  print 'Instructors', course.instructors.values()

  return course  

def test_gen_xml(xml_course):
  
  tmp_dir = '/home/dados/Sw3/SwDv/CompLang SwDv/PythonSwDv/DjangoSwDv/coursera_django/coursera_app_data/tmpcoursestoscrape/'
  xml_generator = CourseraXmlInfoGenerator(tmp_dir)  
  xml_generator.fill_in_xml_tags_for_course(xml_course)
  xml_generator.save_xml_as_file()

def test1():
  
  xml_course = make_test_course()
  print xml_course
  print 'instructors', xml_course.instructors.all() 
  #return
  #test_gen_xml(xml_course)

def test2():
  
  xml_course = CourseraCourse.objects.get(cid='introstats')
  print xml_course 
  #return
  tmp_dir = '/home/dados/Sw3/SwDv/CompLang SwDv/PythonSwDv/DjangoSwDv/coursera_django/coursera_app_data/tmpcoursestoscrape/'
  xml_generator = CourseraXmlInfoGenerator(tmp_dir)  
  xml_generator.fill_in_xml_tags_for_course(xml_course)
  xml_generator.save_xml_as_file()


def process():
  test1()

if __name__ == '__main__':
  process()
