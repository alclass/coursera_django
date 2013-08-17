#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 27/06/2013

@author: friend
'''

import codecs, os, sys
#import xml.etree.ElementTree as ET
import lxml.html
import timeutils
import __init__
import local_settings as ls

from ClassExceptionsMod import CourseraWebRootSavedPageHasNotBeenFound

os.environ['DJANGO_SETTINGS_MODULE'] = 'coursera_django.settings' # 'PBCodeInspectorStats.settings'
from coursera_app.models import CourseraCourse, Institution
#import coursera_app.models


class CourseSubset(object):

  def __init__(self):
    self.cid   = None
    self.n_seq = 0
    self.title = None
    self.university = None
    self.start_date = None
    self.duration_in_weeks = 0
    self.is_self_study = False
    self.is_start_date_TBA = False

  def get_n_seq(self):
    try:
      return int(self.n_seq)
    except ValueError:
      return 0
    
  def form_dict_attrs(self):
    return {
      'cid'   : self.cid,
      'n_seq' : self.n_seq,
      'title' : unicode(self.title),
      'university' : self.university,
      'start_date' : str(self.start_date),
      'duration_in_weeks' : self.duration_in_weeks, 
    }  
    
  def __unicode__(self):
    outstr = u'%(cid)s-%(n_seq)s %(title)s, %(university)s (%(start_date)s, %(duration_in_weeks)d weeks)' %self.form_dict_attrs()  
    return outstr
    
  def __str__(self):
    return self.__unicode__()
  
def derive_cid_and_n_seq_from_href(href):
  try:
    pp = href.split('/')
    cid_n_seq = pp[3]
    pp = cid_n_seq.split('-')
    n_seq = pp[-1]
    cid = '-'.join(pp[:-1])
    #if cid.startswith('-'):
      #cid = cid.lstrip('-')
    return cid, n_seq
  except IndexError:
    pass
  if href.startswith('/course'): # eg '/course/innovativeideas' from the browser 'file:///course/innovativeideas'
    pp = href.split('/')
    cid = pp[-1]
    n_seq = '001'
    return cid, n_seq
  return None, None
  

class CourseraWebRootPageScraper(object):
  
  def __init__(self, coursera_webrootpage_xhtml_abspath=None):
    
    self.init_coursera_webrootpage_xhtml_abspath(coursera_webrootpage_xhtml_abspath)
    self.courses_subset = []

  def init_coursera_webrootpage_xhtml_abspath(self, coursera_webrootpage_xhtml_abspath=None):
    self.coursera_webrootpage_xhtml_abspath = coursera_webrootpage_xhtml_abspath
    if self.coursera_webrootpage_xhtml_abspath == None or not os.path.isfile(self.coursera_webrootpage_xhtml_abspath):
      self.coursera_webrootpage_xhtml_abspath = ls.get_default_coursera_saved_webroot_webpage_abspath()
      if not os.path.isfile(self.coursera_webrootpage_xhtml_abspath):
        raise CourseraWebRootSavedPageHasNotBeenFound, CourseraWebRootSavedPageHasNotBeenFound.show_error_msg(self.coursera_webrootpage_xhtml_abspath)
  
  def get_xhtml_text(self):
    f = codecs.open(self.coursera_webrootpage_xhtml_abspath, 'r', 'utf-8')
    return f.read()

  def scrape_coursera_webrootpage_into_courses_subset(self):
    '''
    '''
    xhtml_root = lxml.html.fromstring(self.get_xhtml_text())
    #body = xhtml_root.xpath('./body')[0]
    #xml_courses = body.getchildren()
    xml_courses = xhtml_root.xpath('.//div')
    for xml_course in xml_courses:
      try:
        start_date_and_duration_str = xml_course.xpath('./div/span/text()')[0]
        #print 'start_date_and_duration_str', start_date_and_duration_str
        # start_date_and_duration_str example ==>>> Aug 5th (7 weeks long)
        start_date, duration_in_weeks = timeutils.parse_start_date_with_duration_in_weeks_within_parentheses(start_date_and_duration_str)
        if start_date == None and duration_in_weeks == None:
          continue
        #print 'start_date', start_date, 'duration_in_weeks', duration_in_weeks
        course_subset = CourseSubset()
        if start_date != None: 
          course_subset.start_date = start_date
        if duration_in_weeks > 0:
          course_subset.duration_in_weeks = duration_in_weeks
        elif duration_in_weeks == -1: # Self study
          course_subset.is_self_study = True
        elif duration_in_weeks == -2: # Date TBA (To Be Announced)
          course_subset.is_start_date_TBA = True
        subdivs_to_introspect = xml_course.findall(".//div[@class]")
        for subdiv in subdivs_to_introspect:
          classname = subdiv.get('class')
          if classname == 'coursera-course-listing-main': # listing_main_div
            # instropecting the course's title and its id and n_seq
            course_a_tag = subdiv.xpath('./h3/a')[0]
            if course_a_tag == None:
              continue
            href = course_a_tag.get('href')
            cid, n_seq = derive_cid_and_n_seq_from_href(href)
            if cid == None or n_seq == None:
              continue  
            course_subset.cid   = cid
            course_subset.n_seq = n_seq 
            the_courses_title = course_a_tag.text # xpath('./h3/a/text()')[0]
            if the_courses_title == None:
              continue
            the_courses_title = the_courses_title.lstrip(' \t\r\n').rstrip(' \t\r\n')
            course_subset.title = the_courses_title
            
            # instropecting the course's university listed
            # listing_statement_div = subdiv.xpath('./div')[1] # <div class="coursera-course-listing-statement">
            listing_statement_inner_divs = subdiv.xpath('./div')
            for inner_div in listing_statement_inner_divs:
              classname2 = inner_div.get('class') 
              if classname2 == 'coursera-course-listing-more coursera-course-my-listing-more':
                try:
                  university_name = inner_div.xpath('./a/text()')[0] # university's inner div with its enclosing a[@href]
                  print university_name 
                  #university_name = university_name.decode('utf-8')
                  course_subset.university = university_name
                except IndexError:
                  continue
            self.courses_subset.append(course_subset)
      except IndexError:
        continue  
  
  def list_courses_subset(self):
    for i, course_subset in enumerate(self.courses_subset):
      print str(i+1).zfill(3), course_subset
 
  def save_courses_subset_to_db(self):
    for i, course_subset in enumerate(self.courses_subset):
      #if course_subset.university == None:
        #continue
      try:
        print str(i+1).zfill(3), 'Saving to db', course_subset
      except UnicodeEncodeError:
        print str(i+1).zfill(3), 'Saving to db'
      course = CourseraCourse()
      course.cid = course_subset.cid
      course.n_seq = course_subset.get_n_seq()
      course.title = course_subset.title
      if course_subset.start_date != None:
        course.start_date = course_subset.start_date
      if course_subset.duration_in_weeks != None:
        course.duration_in_weeks = course_subset.duration_in_weeks
      #course.save()
      if course_subset.university != None:
        university_name = course_subset.university
        try:
          institution = Institution.objects.get(name=university_name)
        except Institution.DoesNotExist:
          institution = Institution()
          institution.name = university_name
          #institution.courseracourse_id = course.cid
          institution.save()
          print 'institution id', institution.id
          #CourseraCourse.objects.create(name=university_name)
        except AttributeError, e:
          print 'university_name', university_name
          print e
          #sys.exit(0)
          pass
        #course.in
        #course.institutions.add(institution.id)
      course.save()

def process():
  scraper = CourseraWebRootPageScraper()
  scraper.scrape_coursera_webrootpage_into_courses_subset()
  scraper.save_courses_subset_to_db()
  print 'Total scraped:', len(scraper.courses_subset) 


if __name__ == '__main__':
  process()
