
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
# formatting.py: methods to normalize and standardize the formats of the different
# line components of the interlinear glosses


def cleanUpInterlinears(string):
   string = removeWhitespace(string)
   string = string.replace("-","–")
   return string

def removeWhitespace(string):
    string = string.replace(" ","")
    return string

def manageQuotes(string):
   if string[0] == "‘":
         string = string[1:]
   if string[-1] == "’":
         string = string[:-1]
   string = "‘" + string.strip() + "’"
   return string

def correctCapitalization(string):
   exceptions  = ["A","S","O","P"]
   if string in exceptions:
      return string
   newString = string.lower()
   return newString
   
