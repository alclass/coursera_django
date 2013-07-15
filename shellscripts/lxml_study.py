#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 27/06/2013

@author: friend
'''
import sys
from lxml import etree

def study01():
  page = etree.Element('html')
  doc = etree.ElementTree(page)
  headElt = etree.SubElement(page, 'head')
  bodyElt = etree.SubElement(page, 'body')
  title = etree.SubElement(headElt, 'title')
  title.text = 'Your page title here'
  # <link rel='stylesheet' href='mystyle.css' type='text/css'>
  linkElt = etree.SubElement(headElt, 'link', rel='stylesheet', href='mystyle.css', type='text/css')
  linkElt.text = 'This is a link'
  p = etree.SubElement(bodyElt, 'p')
  p.text = 'Hello World!'
  #outFile = open('homemade.xml', 'w')
  #doc.write(outFile)
  outFile = open('study01.xml', 'w')
  doc.write(outFile)
  #doc.write(sys.__stdout__)

def study02():
  doc = etree.parse('study01.xml')
  doc.write(sys.__stdout__)
  # linkNode.attrib['href'] = 'http://www.nmt.edu/'

from lxml import etree as et

def study03():
  HTML_NS = "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
  XSL_NS  = "http://www.w3.org/1999/XSL/Transform"
  NS_MAP = {None: HTML_NS, "xsl": XSL_NS}
  rootName = et.QName(XSL_NS, 'stylesheet')
  root = et.Element(rootName, nsmap=NS_MAP)
  sheet = et.ElementTree(root)
  top = et.SubElement(root, et.QName(XSL_NS, "template"), match='/')
  html = et.SubElement(top, et.QName(HTML_NS, "html"))
  head = et.SubElement(html, "head")
  title = et.SubElement(head, "title")
  title.text = "Heading title"
  body = et.SubElement(html, "body")
  h1 = et.SubElement(body, "h1")
  h1.text = "Body heading"
  p = et.SubElement(body, "p")
  p.text = "Paragraph text"
  sheet.write(sys.stdout, pretty_print=True)


if __name__ == '__main__':
  #study01()
  study03()
  pass
