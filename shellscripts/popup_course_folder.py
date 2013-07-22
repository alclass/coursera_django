#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 27/06/2013

@author: friend
'''

# import defaults
import os, sys
from lxml import etree 

this_file_path = os.path.abspath(__file__)
THIS_DIR_PATH, filename = os.path.split(this_file_path)
try:
  PARENT_DIR_PATH = '/'.join(THIS_DIR_PATH.split('/')[:-1])
except IndexError:
  PARENT_DIR_PATH = THIS_DIR_PATH

sys.path.append(PARENT_DIR_PATH)
import local_settings as ls

os.environ['DJANGO_SETTINGS_MODULE'] = 'coursera_django.settings' # 'PBCodeInspectorStats.settings'
#import coursera_django.settings as settings
# from coursera_app.models import Course #, Institution  

class FolderNameDoesNotContainValidCourseIdPlusNSeq(ValueError):
  pass

class ProgramLogicError(ValueError):
  pass

# import string

class CourseWithFolder(object):

  def __init__(self, folder_name, course_id=None, course_n_seq=None):
    self.course_id    = course_id
    self.course_n_seq = course_n_seq
    try:
      # this line below should execute when folder_name comes from the content in os.listdir('.')
      self.folder_name  = folder_name.decode('utf-8')  #unicode(folder_name, 'utf-8')
    except UnicodeEncodeError:
      # this line below, after exception raised, should execute when folder_name comes from the xml file
      self.folder_name  = folder_name
    self.derive_course_id_and_n_seq()

  def derive_course_id_and_n_seq(self):
    try:
      pp = self.folder_name.split(' ')
      last_word = pp[-1]
      ppp = last_word.split('-')
      int(ppp[-1])
      self.course_id    = '-'.join( ppp[0:-1] )
      if self.course_id == '':
        raise FolderNameDoesNotContainValidCourseIdPlusNSeq 
      self.course_n_seq = ppp[-1]
    except IndexError:
      raise FolderNameDoesNotContainValidCourseIdPlusNSeq 
    except ValueError:
      raise FolderNameDoesNotContainValidCourseIdPlusNSeq 

  def get_abspath_on_external_disk(self):
    abspath = os.path.join(CourseRepo.COURSES_BASE_DIR_ON_EXTERNAL_DISK, self.folder_name)
    return abspath
 
class CourseRepo(object):
  
  COURSERA_COURSES_XML_DATA_FILENAME = 'coursera_courses_folder_names.xml'
  COURSES_BASE_DIR_ON_EXTERNAL_DISK = '/media/SAMSUNG/coursera.org/'
  
  def __init__(self):
    self.original_executing_dir_abspath = os.path.abspath('.')
    self.course_dict = None
    self.course_tuple_list = None
    
  def form_coursera_courses_xml_data_filename_abspath(self):
    abspath = os.path.join(ls.COURSERA_DJANGO_DATADIR, self.COURSERA_COURSES_XML_DATA_FILENAME)
    return abspath 

  def listdir_and_save_course_foldernames(self):
    os.chdir(self.COURSES_BASE_DIR_ON_EXTERNAL_DISK)
    contents = os.listdir('.')
    self.course_dict = {}
    for content in contents:
      if not os.path.isdir(content):
        continue
      try:
        course = CourseWithFolder(content)
        self.course_dict[course.course_id] = course
      except FolderNameDoesNotContainValidCourseIdPlusNSeq:
        pass 
    self.write_courses_xml_data_file()
  
  def write_courses_xml_data_file(self):
    '''
    <xml>
    <course id='algo' seq='001'>
      <folder_name>
        here the folder name
      </folder_name>
    </course>
    </xml>
    '''
    page = etree.Element('xml') #, encoding='utf-8')
    doc = etree.ElementTree(page)
    #print 'dict', self.course_dict
    for course_id in self.course_dict.keys():
      course = self.course_dict[course_id]
      node = etree.SubElement(page, 'course', course_id=course.course_id, course_n_seq=course.course_n_seq)
      print 'course.folder_name', course.folder_name
      node.text = unicode(course.folder_name)  #.encode('utf-8'))
    # come back to executing dir
    os.chdir(self.original_executing_dir_abspath)
    xml_filename = self.form_coursera_courses_xml_data_filename_abspath()
    #doc.write(sys.stdout, pretty_print=True)
    print 'Writing file', xml_filename
    
    outfile = open(xml_filename,'w')
    # doc.write(sys.stdout, pretty_print=True) #, encoding=unicode)
    doc.write(outfile, pretty_print=True) #, encoding=unicode)

  def recreate_dir_listing_txt_file(self):
    self.listdir_and_save_course_foldernames()
  
  def read_courses_xml_data_file(self, reread=False):
    if self.course_dict != None and not reread:
      return
    self.course_dict = {}
    xml_filename = self.form_coursera_courses_xml_data_filename_abspath()
    doctree = etree.ElementTree(file=xml_filename)
    nodes = doctree.findall('//course')
    #print len(nodes)
    # counter = 0
    for node in nodes:
      course_id    = node.get('course_id')
      # counter += 1
      # print counter, 'course_id', course_id 
      course_n_seq = node.get('course_n_seq')
      folder_name  = node.text
      course = CourseWithFolder(course_id=course_id,course_n_seq=course_n_seq,folder_name=folder_name)
      self.course_dict[course_id] = course
  
  def translate_dict_to_tuple_list_if_needed(self):
    if self.course_tuple_list == None:
      if self.course_dict == None:
        self.read_courses_xml_data_file()
    self.course_tuple_list = self.course_dict.items()
      
  def show_course_tuple_list_with_index_order(self):
    self.translate_dict_to_tuple_list_if_needed()
    for i, tuple_list in enumerate(self.course_tuple_list):
      _, course = tuple_list
      print i, course.folder_name
  
  def find_course_by_course_id(self, course_id):
    self.read_courses_xml_data_file()
    if not course_id in self.course_dict.keys():
      return None
    course = self.course_dict[course_id]
    return course 
  
  def get_course_by_shown_list_index(self, shown_list_index):
    self.translate_dict_to_tuple_list_if_needed()
    print 'Fetching', shown_list_index,'out of len(self.course_tuple_list) =', len(self.course_tuple_list)
    course_id, course = self.course_tuple_list[shown_list_index]
    if shown_list_index == 62:
      print 'course_id, course', course_id, course, course.folder_name
    return course 
  
  def find_course_by_partial_course_id(self, partial_course_id):
    course = None        
    candidates = []
    for course_id in self.course_dict.keys():
      if course_id.startswith(partial_course_id):
        candidates.append(course_id)
    if len(candidates) > 0:
      course = self.course_dict[candidates[0]]
      if len(candidates) > 1:
        print 'Candidates:', candidates
        _ = raw_input('The first one will be used. Press [ENTER]')
    return course
  
  def go_popup_course_folder_via_course_id(self, course_id):
    if course_id != None:
      course = self.find_course_by_course_id(course_id)
      if course == None:
        course = self.find_course_by_partial_course_id(course_id)
        if course == None:
          print 'Course with course_id %s was not found.' %course_id
          return
      self.go_popup_course_folder(course)

  def go_popup_course_folder_via_shown_index(self, shown_index):
    if shown_index != None:
      print 'Getting course no.', shown_index
      course = self.get_course_by_shown_list_index(shown_index)
      if course == None:
        print 'Course with index %d was not found.' %shown_index
        return
      self.go_popup_course_folder(course)
  
  def go_popup_course_folder(self, course):
    course_folder_abspath = os.path.join(self.COURSES_BASE_DIR_ON_EXTERNAL_DISK, course.folder_name)
    if not os.path.isdir(course_folder_abspath):
      print 'Folder', course_folder_abspath, 'does not exist or is not available now.'
      sys.exit(1)
    print 'Opening course_id', course.course_id, 'on', course_folder_abspath 
    command = 'caja "%s"' %course_folder_abspath
    os.system(command)

class ProcessToFollow:
  DO_RECREATE_DIR_LISTING_TXT_FILE  = 1 
  DO_SHOW_DIR_LISTING_TXT_FILE      = 2 
  DO_OPEN_FOLDER_BY_LIST_INDEX      = 3
  DO_OPEN_FOLDER_BY_COURSE_ID_IF_EXISTS = 4 
  # DO_OPEN_FOLDER_BY_PARTIAL_COURSE_ID_IF_EXISTS = 5 

def decide_process_to_follow_based_on_sysargv():
  if '--recreate' in sys.argv:
    # Option 1
    return ProcessToFollow.DO_RECREATE_DIR_LISTING_TXT_FILE
  elif '--show' in sys.argv:
    # Option 2
    return ProcessToFollow.DO_SHOW_DIR_LISTING_TXT_FILE
  elif len(sys.argv) > 1:
    # check there's a number in sys.argv[1]
    arg = sys.argv[1]
    try:
      int(arg)
      # Option 3
      return ProcessToFollow.DO_OPEN_FOLDER_BY_LIST_INDEX
    except ValueError:
      # Option 4
      return ProcessToFollow.DO_OPEN_FOLDER_BY_COURSE_ID_IF_EXISTS
  return None

def process():
  follow_up_id = decide_process_to_follow_based_on_sysargv()
  if follow_up_id == None:
    return # FINISHES HERE
  course_repo = CourseRepo()
  # DO_RECREATE_DIR_LISTING_TXT_FILE  = 1 
  if follow_up_id == ProcessToFollow.DO_RECREATE_DIR_LISTING_TXT_FILE:
    course_repo.recreate_dir_listing_txt_file()
    return # FINISHES HERE
  # DO_SHOW_DIR_LISTING_TXT_FILE      = 2 
  elif follow_up_id == ProcessToFollow.DO_SHOW_DIR_LISTING_TXT_FILE:
    course_repo.show_course_tuple_list_with_index_order()
    return # FINISHES HERE
  # DO_OPEN_FOLDER_BY_LIST_INDEX      = 3
  elif follow_up_id == ProcessToFollow.DO_OPEN_FOLDER_BY_LIST_INDEX:
    try:
      shown_index = int(sys.argv[1])
    except ValueError:
      raise ProgramLogicError, 'Argument that should be guaranteed as int, failed to be so, this is a logic error. Development Team should take a look at.' 
    course_repo.go_popup_course_folder_via_shown_index(shown_index)
    return # FINISHES HERE
  # DO_OPEN_FOLDER_BY_COURSE_ID_IF_EXISTS = 4 
  elif follow_up_id == ProcessToFollow.DO_OPEN_FOLDER_BY_COURSE_ID_IF_EXISTS:
    supposed_course_id = sys.argv[1] 
    course_repo.go_popup_course_folder_via_course_id(supposed_course_id)
    return # FINISHES HERE
  
if __name__ == '__main__':
  process()
