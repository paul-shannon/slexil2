
'''
******************************************************************
SLEXIL—Software Linking Elan XML to Illuminated Language
Copyright (C) 2019 Paul Shannon and David Beck

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

The full version of the GNU General Public License is found at
<https://www.gnu.org/licenses/>.

Information about the software can be obtained by contacting
david.beck at ualberta.ca.
******************************************************************
'''

# -*- coding: utf-8 -*-
#
# TranslationLine: a class to standardize and enforce the IJAL conventions for translation lines:
#    - begins with a left curly single quote
#    - ends with a right curly single quote
#    - has no leading or trailing whitespace
#  are embedded straight single quotes (') permitted?
#  are embedded double quotes permitted?
#----------------------------------------------------------------------------------------------------
import re
import pdb

class TranslationLine:

   rawText = ""
   cleanText = ""

   def __init__(self, rawText):
      self.rawText = rawText.strip()
      self.cleanText = self.standardize()

   def standardize(self):
      string = self.rawText
      if string[0] == "‘":
         string = string[1:]
      if string[-1] == "’":
         string = string[:-1]
      # check for apostrophes instead of squo
      if string[0] == "'":
         string = string[1:]
      if string[-1] == "'":
         string = string[:-1]
      # check for punctuation following rsquo
      regex = re.compile("’[\.,!?\)]$")
      if regex.search(string):
         punctuation = string[-1]
         string = string[:-2].strip() + punctuation
      # replace straight double quotes with smart quotes
      if '"' in string:
         string = re.sub('^"','“',string)
         string = re.sub('\s"',' “',string)
         string = string.replace('"','”')
      # todo: make these right and left single quotes optional, controlled by command line
      #string = "‘" + string.strip() + "’"
      #print("--- skipping addition of single quotes around translation line")
      string = string.strip()
      #ensure single and double quotes separated by &thinsp;
      #needs to be done here because strip() seems to remove final thin space
      #pdb.set_trace()
      if(len(string) >= 3):
         if string[1] == '“':
            string = u'‘\u2009' + string[1:]
         if string[-2] == '”':
            thinquotes = '”' + u'\u2009' + '’'
            string = string.replace('”’',thinquotes).strip()
      return string

   def getRaw(self):
      return self.rawText

   def getStandardized(self):
      return self.cleanText

  

