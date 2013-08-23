#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 22 août 2013

@author: friend
'''
import sys

WAIT_TIME_IN_BETWEEN_PAGE_OPENING = 15

def read_defaults_config_json_file():
  global WAIT_TIME_IN_BETWEEN_PAGE_OPENING
  pass


def generate_first_defaults_in_a_json_file():
  pass

def print_usage_and_exit():
  print '''Usage:
  
  user@mach /dir$ defaults.py generate
  
  The above command generates the defaults.json file which can then be manually changed.
  Notice that it also erases previous configuration values, if any, replacing them to the defaults.
  '''
  sys.exit(0)   
  
def process():
  if 'help' in sys.argv:
    print_usage_and_exit()
  if 'generate' in sys.argv:
    print '''About to generate defaults config file (defaults.json). 
    NOTICE it will erase any previous config values in it. 
    '''
    answer = raw_input('Are you sure to generate defaults.json ? [ENTER] (or any key other than N) means ok, n or N means No. ') 
    if answer in ['n','N']:
      return
    generate_first_defaults_in_a_json_file()

if __name__ == '__main__':
  process()
