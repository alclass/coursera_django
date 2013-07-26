#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Explanation


'''
import glob, os, re, sys, time # glob, os, shutil, sys, time
import BeautifulSoup as bs
#===============================================================================
# sys.path.append('/home/friend/bin/')
# import weblinksExtractor as wle
#===============================================================================

class Counter:
  def __init__(self, total=1):
    self.seq = 0
    self.total = total
  def increment(self):
    self.seq += 1
  def showNBarTotal(self):
    return '%i/%i' %(self.seq, self.total)
counterObj = Counter() # this instantiation will change later

'''
<a data-lecture-id="12"
   data-lecture-view-link="https://class.coursera.org/compfinance-2012-001/lecture/view?lecture_id=12"
   href="https://class.coursera.org/compfinance-2012-001/lecture/12"
   rel="lecture-link"
   class="lecture-link lecture-with-slides-link">
1.3 Portfolio Returns (9:12)<i class="icon-facetime-video" style="padding-left:5px;"></i>
</a>
'''

def downloadLevel1():
  strRegExp = 'lecture/(\d+)'
  pattRegExp = re.compile(strRegExp)
  
  urlToPrint = 'https://class.coursera.org/scientificcomp-2012-001/lecture/view?lecture_id=%i'
  
  htmlTOC = 'list of lectures.html'
  text = open(htmlTOC).read()
  listOfIds = pattRegExp.findall(text)
  listOfIds = map(int, listOfIds)
  c=0
  listOfIds.sort()
  for id in listOfIds:
    c+=1
    if c <= 20:
      continue
    url = urlToPrint %(id)
    print c, url
    comm = 'firefox "%s"' %url
    os.system(comm)
    time.sleep(60)
    if c % 20 == 0:
      ans = raw_input('Continue ? [press <ENTER>]')
  print 'total', c

def getWeblinksAsSourceSrc(htmlFile):
  '''
  The video link is encapsulated inside a "source" xml tag, which in turn has a src attribute
  So to get this video link, first we find all (findAll) "source" xml elements,
    we loop thru them to get the src's attribute values and "stock" them, so to say, in a list
  The "cached" list is returned  
  '''
  text = open(htmlFile).read()
  bSoup = bs.BeautifulSoup(text)
  aTags = bSoup.findAll('source')
  urls = []
  for eachWeblink in aTags:
    url = eachWeblink.get('src')
    urls.append(url)
  return urls


objNotNone = lambda obj : obj <> None
endswithdotmp4 = lambda s : s.endswith('.mp4')
def downloadMp4IfAny(html):
  urls = getWeblinksAsSourceSrc(html)
  #urls = filter(endswithdotmp4, filter(objNotNone, urls))
  for url in urls:
    print type(url)
    if url <> None and not url.endswith('.mp4'):
      continue
    print counterObj.showNBarTotal(), html, url
    comm = 'firefox "%s"' %url
    os.system(comm)
    ans = raw_input('Continue ? [press <ENTER>]')

def getTheHtmlFiles():
  '''
  To solve in the future: return all files with absolute paths
  '''
  htmls = glob.glob('*.html')
  htmls.sort()
  return htmls

def getExtensionlessName(filename, extension='html'):
  dot_extension = '.' + extension
  if not filename.endswith(dot_extension):
    return None 
  name = filename[ : -len(dot_extension) ] #.strip('.html')
  if name.find('/') > -1:
    name = name.split('/')[-1]
  return name

def downloadLevel2():
  global counterObj
  htmls = getTheHtmlFiles()
  counterObj = Counter(len(htmls))
  print 'htmls n.', counterObj.total
  for htmlFile in htmls:
    name = getExtensionlessName(htmlFile, 'html')
    try:
      # if the line below succeeds, we're good to go!
      int(name)
      counterObj.increment()
      print 'Processing', counterObj.showNBarTotal(), htmlFile
      downloadMp4IfAny(htmlFile)
    except ValueError:
      continue
     
if __name__ == '__main__':
  downloadLevel2()  
