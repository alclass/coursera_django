#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
ClassExceptionsMod.py
'''


class CourseraFileOrFolderNotFound(OSError):
  pass

class CourserasRepoRootFolderHasNotBeenFoundOrInexists(CourseraFileOrFolderNotFound):
  error_msg = "Coursera'sRepo Root Folder [%s] Has Not Been Found Or Inexists."

  @staticmethod
  def show_error_msg(folder_name):
    return CourserasRepoRootFolderHasNotBeenFoundOrInexists.error_msg %folder_name  


def process():
  pass

if __name__ == '__main__':
  process()
