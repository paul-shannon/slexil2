# practiceLists.py
#-------------------------------------------------------------------------------
import yaml
import json
import pdb
import random
from yattag import *
from yattag import Doc
#-------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------

class PracticeLists:

   inputFile = None
   practiceLists = None
   categories = None

   #----------------------------------------
   def __init__(self, inputFile, randomize=False):

      self.inputFile = inputFile
      self.parseFile()
      if(randomize):
          self.randomizeWithinLists()

   #----------------------------------------
   def parseFile(self):

      self.practiceLists = yaml.safe_load(open(self.inputFile))

   #----------------------------------------
   def randomizeWithinLists(self):

      for category in self.getCategories():
         x = self.practiceLists[category]
         random.shuffle(x)
         self.practiceLists[category] = x

   #----------------------------------------
   def getCategories(self):

       self.categories = [key for key in self.practiceLists.keys()]
       return(self.categories)

   #----------------------------------------
   def getList(self, name):

     if name in self.categories:
        return(self.practiceLists[name])
     return []

   #----------------------------------------
   def getLists(self):

     return(self.practiceLists)

   #----------------------------------------
   def getJavascript(self):

      s = '\n<script>\n'
      s += 'window.practiceLists = %s' % json.dumps(self.getLists())
      s += '\n</script>'

      return(s)

   #----------------------------------------
   def addHTML(self, htmlDoc):

      with htmlDoc.tag("div", id="practiceDiv"):
         for category in self.getCategories():
            with htmlDoc.tag("button", id="practice-%s" % category,
                             klass="practiceButton"):
                htmlDoc.text(category)

   #----------------------------------------
  
    
