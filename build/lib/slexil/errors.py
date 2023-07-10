
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

class Error(Exception):
    pass


class TooManyMorphsError(Error):
    '''raised when there are more divisions on the parsing line
       than on the glossing line'''

    def __init__(self, lineNumber, morphs, glosses):
        super().__init__()
        self.lineNumber = lineNumber
        self.morphs = morphs
        self.glosses = glosses


class TooManyGlossesError(Error):
    '''raised when there are more divisions on the glossing line
       than on the parsing line'''

    def __init__(self, lineNumber, morphs, glosses):
        super().__init__()
        self.lineNumber = lineNumber
        self.morphs = morphs
        self.glosses = glosses


class EmptyTiersError(Error):
    '''raised when there are fewer than two filled tiers'''

    def __init__(self, lineNumber):
        super().__init__()
        self.lineNumber = lineNumber


class MissingSpeechTiersError(Error):
    '''raised when there is nothing on the speech tier'''

    def __init__(self, lineNumber):
        super().__init__()
        self.lineNumber = lineNumber
