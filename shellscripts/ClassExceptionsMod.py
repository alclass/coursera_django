#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
ClassExceptionsMod.py
'''


class CourseraFileOrFolderNotFound(OSError):

  error_msg = "CourseraFileOrFolderNotFound %s"
  
  @classmethod
  def show_error_msg(cls, str_to_interpolate):
    return cls.error_msg %str_to_interpolate

class CourserasRepoRootFolderHasNotBeenFoundOrInexists(CourseraFileOrFolderNotFound):
  error_msg = "Coursera'sRepo Root Folder [%s] Has Not Been Found Or Inexists."
  # inherits @classmethod show_error_msg(cls, str_to_interpolate)

class CourseraWebRootSavedPageHasNotBeenFound(CourseraFileOrFolderNotFound):
  error_msg = "Coursera Web Root Saved Page (%s) Has Not Been Found."
  # inherits @classmethod show_error_msg(cls, str_to_interpolate)

class CourseraLectureIndexPagesConventionedFolderHasNotBeenFound(CourseraFileOrFolderNotFound):
  error_msg = "Coursera Lecture Index Pages Conventioned Folder (%s) Has Not Been Found."
  # inherits @classmethod show_error_msg(cls, str_to_interpolate)

class CourseraLectureIndexPageHasNotBeenFound(CourseraFileOrFolderNotFound):
  error_msg = "Coursera Lecture Index Page (%s) Has Not Been Found."
  # inherits @classmethod show_error_msg(cls, str_to_interpolate)


def process():
  pass

if __name__ == '__main__':
  process()
