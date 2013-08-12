#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 27/06/2013

@author: friend
'''

import os, sys
import xml.etree.ElementTree as ET
import lxml.html
import timeutils
import __init__
import local_settings as ls

os.environ['DJANGO_SETTINGS_MODULE'] = 'coursera_django.settings' # 'PBCodeInspectorStats.settings'
from coursera_app.models import CourseraCourse, Institution  

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
  <div class="coursera-course-listing-statement">You did not earn a statement of accomplishment</div>
  <div style="width:435px;" class="coursera-course-listing-more coursera-course-my-listing-more">
    <a href="/princeton" class="coursera-course-listing-university internal-home">
      Princeton University
    </a>
  </div>
</div>
</body>
</head>
'''

t = '''
<div data-course-id="970516" 
  class="coursera-course-listing-box coursera-course-listing-box-wide coursera-account-course-listing-box">
  <img src="https://coursera-course-photos.s3.amazonaws.com/9d/d10a1390c031cd40168543b8d3dae8/GBS.jpg" 
    class="coursera-course-listing-icon" />
  <div class="coursera-course-listing-text">
    <div style="position:relative;" class="coursera-course-listing-meta">
      <span>Aug 5th (7 weeks long)</span>
      <br />
      <div style="margin-top:15px;" 
        data-url="https://www.coursera.org/course/globalsportsbusiness" 
        data-text="I'm taking The Global Business of Sports on Coursera!" 
        data-facebook-picture="https://coursera-course-photos.s3.amazonaws.com/9d/d10a1390c031cd40168543b8d3dae8/GBS.jpg"
        data-facebook-name="I'm taking The Global Business of Sports on Coursera!"
        data-facebook-redirect="https://www.coursera.org/" 
        data-twitter-text="I'm taking The Global Business of Sports from @@pennopencourses on @Coursera!" 
        data-twitter-hashtags="globalsportsbusiness" 
        data-eventing-key="user.click.link.social" 
        data-eventing-value="course-mini" 
        class="coursera-share-buttons coursera-sharebuttons">
        <a href="https://twitter.com/share?text=I'm%20taking%20The%20Global%20Business%20of%20Sports%20from%20%40%40pennopencourses%20on%20%40Coursera!&amp;hashtags=globalsportsbusiness&amp;url=https%3A%2F%2Fwww.coursera.org%2Fcourse%2Fglobalsportsbusiness%3Fsharebuttons_ref%3Dtw"
          target="_blank" class="icon-twitter coursera-sharebuttons-icon">
        </a>
        <a href="http://www.facebook.com/dialog/feed?app_id=124275634389084&amp;link=https%3A%2F%2Fwww.coursera.org%2Fcourse%2Fglobalsportsbusiness%3Fsharebuttons_ref%3Dfb&amp;name=I'm%20taking%20The%20Global%20Business%20of%20Sports%20on%20Coursera!&amp;picture=https%3A%2F%2Fcoursera-course-photos.s3.amazonaws.com%2F9d%2Fd10a1390c031cd40168543b8d3dae8%2FGBS.jpg&amp;description=&amp;redirect_uri=https://www.coursera.org/"
          target="_blank" class="icon-facebook-sign coursera-sharebuttons-icon">
        </a>
        <a href="https://plus.google.com/share?url=https%3A%2F%2Fwww.coursera.org%2Fcourse%2Fglobalsportsbusiness%3Fsharebuttons_ref%3Dgp"
          target="_blank" class="icon-google-plus-sign coursera-sharebuttons-icon">
        </a>
      </div>
      <a href="https://class.coursera.org/globalsportsbusiness-001/auth/auth_redirector?type=login&amp;subtype=normal"
        class="btn btn-success coursera-course-button">Go to class
      </a>
      <br />
      <div class="btn-group">
        <a href="/course/globalsportsbusiness" class="internal-home">View course info</a>
        <span>&nbsp; | &nbsp;</span>
        <a href="javascript:void(0)" data-course-id="970516" class="coursera-course-listing-unenroll">Un-enroll</a>
      </div>
    </div>
    <div class="coursera-course-listing-main">
      <h3 class="coursera-course-listing-name">
        <a href="https://class.coursera.org/globalsportsbusiness-001/auth/auth_redirector?type=login&amp;subtype=normal">
          The Global Business of Sports
        </a>
      </h3>
      <div class="coursera-course-listing-progress">
        <span style="left: 1px;" class="progress-label">Aug 5th</span>
        <span style="right: 1px;" class="progress-label">Sep 23rd</span>
        <div class="progress-line"></div>
        <div style="left:14%" class="progress-marker"></div>
        <div style="width:14%;" class="progress-bar"></div>
      </div>
      <div class="coursera-course-listing-statement">
        <div style="width:435px;" class="coursera-course-listing-more coursera-course-my-listing-more">
          <a href="/penn" class="coursera-course-listing-university internal-home">University of Pennsylvania</a>
        </div>
      </div>
    </div>
  </div>
</div>
'''

def scrape(html_text):
  
  root = ET.fromstring(html_text)
  divsL1 = root.iter('div')
  for divL1 in divsL1:
    data_course_div = divL1.get('data-course-id')
    if data_course_div == None:
      continue
    divsL2 = data_course_div.iter('div')
    for divL2 in divsL2:
      div_with_class_attr = divL2.get('coursera-course-listing-text')
      if div_with_class_attr == None:
        continue 
      divsL3 = divL2.iter('div')
      for divL3 in divsL3:
        listing_main_div = divL3.get('coursera-course-listing-main')
        if listing_main_div == None:
          continue
        h3_tag = listing_main_div.find('h3')
        a_tag = h3_tag.find('a')
        href = a_tag.get('href')
        pp = href.split('/')
        cid_n_seq = pp[3]
        pp = cid_n_seq.split('-')
        n_seq = pp[-1]
        cid = '-'.join(pp[:-1])
        course = CourseraCourse()
        course.title = a_tag.text
        course.cid = cid
        course.n_seq = int(n_seq)
        divsL4 = divL3.iter('div')
        for divL4 in divsL4:
          listing_progress_div = divL4.get('coursera-course-listing-progress')
          if listing_progress_div != None:
            start_date_span = listing_progress_div.find('span')
            if start_date_span != None:
              date_text = start_date_span.text
              pp = date_text.split(' ')
              month_str = pp[0]
              day_str = pp[-1]
              day_str = day_str[:-2]
              month = timeutils.array_3letter_months_english.index(month_str)
              month += 1
          listing_statement_div = divL4.get('coursera-course-listing-statement')
          if listing_statement_div != None:
            outter_div_for_university = listing_statement_div.find('div')
            university_a_tag = outter_div_for_university.find('a')
            university_class_attr = university_a_tag.get('class')
            if university_class_attr != None:
              # ok, it confirms we're in the right <div /> !
              university_name = university_a_tag.text
              institution = Institution.objects.get(name=university_name)
              course.institutions.add(institution) 
               
class CourseSubset(object):

  def __init__(self, title, start_date, duration_in_weeks, university):
    self.title = None
    self.start_date = None
    self.duration_in_weeks = None
    self.university = None

def scrape_coursera_webrootpage_into_courses_subset(html_text):
  
  courses_subset = []

  xhtml_root = lxml.html.fromstring(html_text)
  start_date_and_duration_str = xhtml_root.xpath('./div/div/span/text()')[0]
  # start_date_and_duration_str example ==>>> Aug 5th (7 weeks long)
  start_date, duration_in_weeks = timeutils.parse_start_date_with_duration_in_weeks_within_parentheses(start_date_and_duration_str)
  if start_date == None or duration_in_weeks == None:
    continue
  course_subset = CourseSubset()
  course_subset.start_date = start_date
  course_subset.duration_in_weeks = duration_in_weeks

  subdivs_to_introspect = xhtml_root.findall(".//div[@class]")
  for subdiv in subdivs_to_introspect:
    classname = subdiv.get('class')
    if classname == 'coursera-course-listing-main': # listing_main_div
      # instropecting the course's title
      the_courses_title = subdiv.xpath('./h3/a/text()')[0]
      if the_courses_title == None:
        continue
      the_courses_title = the_courses_title.lstrip(' \t\r\n').rstrip(' \t\r\n')
      course_subset.title = the_courses_title 
      
      # instropecting the course's university listed
      listing_statement_div = subdiv.xpath('./div')[1] # <div class="coursera-course-listing-statement">
      university_name = listing_statement_div.xpath('./div/a/text()')[0] # university's inner div with its enclosing a[@href]
      course_subset.university = university_name
      courses_subset.append(course_subset)  

  return courses_subset


def process():
  scrape2(t)


#import os, re #, time

#from coursera_grabber_functions import either_filename_or_default 


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
  elements_l1 = element.getchildren()
  # first element of incoming element <div> is expected to be <h3>
  print 'len(elements_l1)', len(elements_l1)
  h3 = elements_l1[0]
  # first element is expected to be <h3>, if not, return
  if h3.tag != 'h3':
    return None
  print 'Got <h3>', h3.getchildren(), 'l1',elements_l1[1].tag, elements_l1[2].tag, elements_l1[3].tag 
  elements_l2 = h3.getchildren()
  a = elements_l2[0]
  # first element of h3 is expected to be <a>, if not, return
  if a.tag != 'a':
    return None
  url   = a.get('href')
  course_id = url.split('/')[-1]
  print 'course_id', course_id 
  if not is_course_id_good(course_id):
    return None
  # "coursera-course-listing-more coursera-course-my-listing-more"
  try:
    div_that_has_university_info = elements_l1[3]
    inner_a = div_that_has_university_info.getchildren()[0]
    print 'university_class_node.text', inner_a.text
  except IndexError:
    pass
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
      sys.exit(0)

  for i, course_obj in enumerate(courses):
    print i, course_obj.course_id
    print course_obj.title

def test6():
  xhtml = etree.fromstring(htmltrunk)
  #classnode = xhtml.find('coursera-course-listing-main')
  for each in xhtml.getchildren():
    print each

if __name__ == '__main__':
  process()
  pass
