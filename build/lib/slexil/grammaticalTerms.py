
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
# GrammaticalTerms: a class to handle formatting of abbreviations used
# in interlinearizations, specifically to standardize all abbreviations as
# lowercase, to be rendered as small caps by the CSS style .grammatical-term
# 
#----------------------------------------------------------------------------------------------------
import re
from pprint import pprint
from yattag import *
import pdb


#------------------------------------------------------------------------------------------------------------------------
class GrammaticalTerms:

    def __init__(self, part, grammaticalTerms):
        if part.lower() in grammaticalTerms:
            self.text = part.lower()
        else:
            self.text = part

    def getTerm(self):          
        return(self.text)
