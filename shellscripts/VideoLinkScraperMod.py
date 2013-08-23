#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

This module contains 2 classes:

+ class VideoLinkPageScraper
+ class VideoLinkScraperDispatcher


The basic idea here is to scrape local saved files that have prefix 'videolinks_'
  
These prefixed html files have links to video lectures which have an "unview" value in a html-class attribute
  (see code for better understanding)

As the 2 classes are concerned:
  + class VideoLinkScraperDispatcher organizes the html-files fetching
  + whereas class VideoLinkPageScraper scrapes the video lecture download url's

These links are autoinvoked via chromium and downloads are timespaced by 2 min
  (or other default if it has been changed, see code for that)

Created on 27/06/2013

@author: friend
'''

import codecs, os
# sys,
import time
#import xml.etree.ElementTree as ET
import lxml.html
#import timeutils
import __init__
import local_settings as ls

from ClassExceptionsMod import CourseraLectureIndexPagesConventionedFolderHasNotBeenFound, CourseraLectureIndexPageHasNotBeenFound

os.environ['DJANGO_SETTINGS_MODULE'] = 'coursera_django.settings' # 'PBCodeInspectorStats.settings'
#from coursera_app.models import CourseraCourse, Institution
#import coursera_app.models


class VideoLinkPageScraper(object):
  
  def __init__(self, xhtml_lecture_index_page_abspath=None):
    self.download_buffer = []
    self.init_xhtml_lecture_index_page_abspath(xhtml_lecture_index_page_abspath)
    
  def init_xhtml_lecture_index_page_abspath(self, xhtml_lecture_index_page_abspath=None):
    self.xhtml_lecture_index_page_abspath = xhtml_lecture_index_page_abspath
    if self.xhtml_lecture_index_page_abspath == None or not os.path.isfile(self.xhtml_lecture_index_page_abspath):
      raise CourseraLectureIndexPageHasNotBeenFound, CourseraLectureIndexPageHasNotBeenFound.show_error_msg(CourseraLectureIndexPageHasNotBeenFound)

  def scrape_video_link_page(self):
    '''
    '''
    f = codecs.open(self.xhtml_lecture_index_page_abspath, 'r', 'utf-8')
    xhtml_text = f.read()
    xhtml_root = lxml.html.fromstring(xhtml_text)
    xml_page_resources = xhtml_root.xpath('.//li[@class]')
    for li_tag in xml_page_resources:
      li_class = li_tag.get('class')
      if li_class == 'unviewed':
        div = li_tag.find('div')
        atags = div.findall('a')
        for a in atags:
          href = a.get('href')
          if href.find('/lecture/download.mp4?lecture_id=') > -1:
            self.download_buffer.append(href)

  def download_videos(self):
    '''
    '''
    self.scrape_video_link_page()
    n_downloads = 0
    total = len(self.download_buffer)
    for i, href in enumerate(self.download_buffer):
      print i+1, '/', total, 'Browse-Opening', href
      comm = 'chromium "%s"' %href
      ret_val = os.system(comm)
      if ret_val == 0:
        n_downloads += 1
      print 'Waiting 2 min.'
      time.sleep(120)
    return n_downloads

  def recurse_divs(self, div_tag):
    print div_tag.text
    inner_div_tag = div_tag.xpath('./div')
    for div in inner_div_tag:
      self.recurse_divs(div)


class VideoLinkScraperDispatcher(object):
  '''
  '''

  VIDEOLINKS_XHTML_FILE_PREFIX = 'videolinks_'  
  
  def __init__(self, xhtml_lecture_index_pages_conventioned_folder_abspath=None):
    
    self.videolinks_xhtml_filenames = []
    self.init_xhtml_lecture_index_pages_conventioned_folder_abspath(xhtml_lecture_index_pages_conventioned_folder_abspath)

  def init_xhtml_lecture_index_pages_conventioned_folder_abspath(self, xhtml_lecture_index_pages_conventioned_folder_abspath=None):
    self.xhtml_lecture_index_pages_conventioned_folder_abspath = xhtml_lecture_index_pages_conventioned_folder_abspath
    if self.xhtml_lecture_index_pages_conventioned_folder_abspath == None or not os.path.isdir(self.xhtml_lecture_index_pages_conventioned_folder_abspath):
      self.xhtml_lecture_index_pages_conventioned_folder_abspath = ls.get_default_lecture_index_page_xhtml_files_conventioned_folder_abspath()
      if not os.path.isdir(self.xhtml_lecture_index_pages_conventioned_folder_abspath):
        raise CourseraLectureIndexPagesConventionedFolderHasNotBeenFound, CourseraLectureIndexPagesConventionedFolderHasNotBeenFound.show_error_msg(self.xhtml_lecture_index_pages_conventioned_folder_abspath)
  
  def get_first_lecture_index_page_xhtml_abspath_on_folder(self):
    self.get_all_xhtml_files_to_video_link_extract()
    try:
      filename = self.videolinks_xhtml_filenames[0]
      return self.get_lecture_index_page_xhtml_abspath(filename)
    except IndexError:
      #if self.videolinks_xhtml_filenames == None or len(self.videolinks_xhtml_filenames) == 0:
      pass
    return None

  def get_all_xhtml_files_to_video_link_extract(self):
    self.videolinks_xhtml_filenames = []
    files = os.listdir(self.xhtml_lecture_index_pages_conventioned_folder_abspath)
    for filename in files:
      if filename.startswith(VideoLinkScraperDispatcher.VIDEOLINKS_XHTML_FILE_PREFIX):
        self.videolinks_xhtml_filenames.append(filename)

  def get_lecture_index_page_xhtml_abspath(self, filename):
    lecture_index_page_xhtml_abspath = os.path.join(self.xhtml_lecture_index_pages_conventioned_folder_abspath, filename)
    return lecture_index_page_xhtml_abspath

  def process_available_video_link_files(self):
    self.get_all_xhtml_files_to_video_link_extract()
    total = len(self.videolinks_xhtml_filenames)
    n_downloads = 0
    for i, filename in enumerate(self.videolinks_xhtml_filenames):
      print 'Processing', i+1,'/', total, filename
      lecture_index_page_xhtml_abspath = self.get_lecture_index_page_xhtml_abspath(filename)
      try:
        scraper = VideoLinkPageScraper(lecture_index_page_xhtml_abspath)
        n_downloads += scraper.download_videos()
        print 'Total n_downloads', n_downloads
      except CourseraLectureIndexPageHasNotBeenFound:
        # when an opportunity opens, this exception raising must be scheduled for tests/unittest
        continue

  
def process():
  dispatcher = VideoLinkScraperDispatcher()
  #lecture_index_page_xhtml_abspath = dispatcher.get_first_lecture_index_page_xhtml_abspath_on_folder()
  #scraper = VideoLinkPageScraper(lecture_index_page_xhtml_abspath)
  #scraper.scrape_video_link_page()
  dispatcher.process_available_video_link_files()

if __name__ == '__main__':
  process()
