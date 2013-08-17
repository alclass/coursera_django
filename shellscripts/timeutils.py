#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 30/06/2013

@author: friend
'''

from datetime import date

array_3letter_months_english = [
  'Jan',
  'Feb',
  'Mar',
  'Apr',
  'May',
  'Jun',
  'Jul',
  'Aug',
  'Sep',
  'Oct',
  'Nov',
  'Dec',
]

def extract_n_weeks_long(n_weeks_long_str):
  weeks_long_str = n_weeks_long_str
  weeks_long_str = weeks_long_str.lstrip('(')
  n_weeks = int(weeks_long_str)
  return n_weeks

def parse_start_date_with_duration_in_weeks_within_parentheses(start_date_and_duration_str):
  '''
  The purpose of this function is to extract the pydate and an int from a string such as:
    eg: start_date_and_duration_str example ==>>> Aug 5th (7 weeks long)
  
  To Do: at some point in the future, 
    we'll have to add the "year" element extract capability
    which will be optional, ie, the function must know whether or not the string comes with the year
    and, having the year, extract it
    
  Starts in 14 days
  Starts in 3 months
  Ended a year ago
  Date TBA
  Date TBA (5 weeks long)
  '   |  '
  Your Watchlist
  (etc.)
  '''
  if start_date_and_duration_str == None:
    return None, None
  pp = start_date_and_duration_str.split(' ')
  try:
    today = date.today()
    month_str = pp[0]
    month = array_3letter_months_english.index(month_str) + 1
    day_str = pp[1]
    day_str = day_str[:-2] # strip off th (n-th), rd (third), nd (second), st (first)
    day = int(day_str)
    pydate = date(year=today.year, month = month, day = day)
    n_weeks = extract_n_weeks_long(pp[2]) 
    return pydate, n_weeks
  except IndexError:
    pass
  except ValueError:
    pass
  if start_date_and_duration_str.find('Self study') > -1:
    return None, -1  # No Date, no duration, but 'Self study'
  if start_date_and_duration_str.find('Date TBA') > -1:
    if start_date_and_duration_str.endswith('weeks long)'):
      n_weeks = extract_n_weeks_long(pp[2]) 
      return None, n_weeks
    return None, -2 # Date TBA without n_weeks duration
  return None, None # extraction not favorable to a course at the xhtml side 
