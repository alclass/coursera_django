#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 29/06/2013

@author: friend
'''

import os

def either_filename_or_default(filename, default_fallback, must_exist_locally = True):
  if filename == None:
    return default_fallback
  if not os.path.isfile(filename):
    if not must_exist_locally:
      # ie, file is to be created
      return filename
    return default_fallback
  return filename 

def get_filename_param_or_default(extra_params, default_fallback, must_exist_locally = True):
  if extra_params == None or type(extra_params) != dict:
    return default_fallback
  if not extra_params.has_key('filename'):
    return default_fallback
  filename = extra_params['filename']
  return either_filename_or_default(filename, default_fallback, must_exist_locally)
