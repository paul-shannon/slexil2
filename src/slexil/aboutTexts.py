
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

# ------------------------------------------------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------------------------------------------


import dash_core_components as dcc
import dash_html_components as html


class AboutTexts:
    def __init__(self):
        self.mainDiv = self.makeMainDiv()

    def getMainDiv(self):
        return self.mainDiv

    def makeMainDiv(self):
        print("===== building About tab")
        basics = self.makeBasics()
        ELAN = self.makeELAN()
        sound = self.makeSound()
        abbr = self.makeAbbr()
        preview = self.makePreview()
        download = self.makeDownload()
        privacy = self.makePrivacy()
        credits = self.makeCredits()
        anchor = html.Div(html.A("top", href="#top"), className="anchor")

        children = [basics, ELAN, sound, abbr, preview, download, privacy, credits, anchor]

        mainDiv = html.Div(className="aboutMain", children=children)
        return mainDiv

    def makeBasics(self):
        title = html.H3("SLEXIL basics", id="top")
        text = dcc.Markdown('''SLEXIL is a DASH/FLASK web application written in Python that allows users to create 
        animated HTML from ELAN projects for the presentation and playback of texts. SLEXIL is 
        compatible with any modern web browser and does not require the user to install any 
        software on their computers. Project components (.eaf file, sound file, list of 
        abbreviations) can be uploaded through the web interface and configured; SLEXIL then builds a webpage which can 
        be previewed and downloaded to the user’s computer. This software is Open Source; source code for the 
        project is available on [GitHub](https://github.com/davidjamesbeck/slexil.git).''')

        basics = html.Div(className='aboutContents',children=[title,text])
        return basics

    def makeELAN(self):
        title = html.H3("ELAN files")
        text = dcc.Markdown('''SLEXIL works from the .eaf file of an ELAN project. Minimally, the .eaf file should have 
        two tiers, one for transcribed speech and the other a free translation. The file should be 
        time-aligned so that time intervals correspond, directly or indirectly, to what 
        will be presented as numbered lines in the text. SLEXIL supports two lines of interlinearization 
        consisting of paired annotations on separate tiers that exhaustively parse the line of text 
        being analyzed; mismatched or missing annotations on either of these two lines will generate 
        errors that will appear in the ERRORS.log file that is downloaded with your final project. 
        Two additional tiers can be processed as well, one that will appear immediately below the 
        numbered transcription line and another that will appear immediately below the free 
        translation. These are in a one-to-one relationship to the numbered line and cannot be 
        subdivided into smaller annotations.''')

        ELAN = html.Div(className='aboutContents',children=[title,text])
        return ELAN

    def makeSound(self):
        title = html.H3("Sound files")
        text = dcc.Markdown('''In order to facilitate line-by-line playback, SLEXIL parses the audio recording 
                accompanying the project into smaller files corresponding to the time codes provided in the ELAN file. These 
                smaller sound files, along with the full recording used for continuous playback, are stored in a folder 
                named "audio" in the project directory. ''')
        text2 = dcc.Markdown('''SLEXIL uses PySoundFile to handle audio and can accept files in a variety of common 
                formats, including WAV, AIFF, RAW, and FLAC. A full list of acceptable encodings can be 
                found [here](http://www.mega-nerd.com/libsndfile/#Features). SLEXIL does not currently work with MP3.''')

        sound = html.Div(className='aboutContents',children=[title, text, text2])
        return sound

    def makeAbbr(self):
        title = html.H3("Abbreviations")
        text1 = dcc.Markdown('''If your text is interlinearized, you can provide a list of abbreviations in plain 
        text (UTF-8) format; these will be displayed in small caps. The abbreviations file must be formatted as follows:''')
        text2 = html.Ol(children=[
            html.Li('''List each abbreviation on a separate line. Do not include definitions. Give 
        abbreviations in ALL CAPS if that is how they appear in the ELAN file;'''),
            html.Li(children=['''List each part of an abbreviation that comes separated by punctuation on a separate line 
        (e.g., if you have “''',
                             html.Span("pl.poss", className="smallCaps"),
        '''” and “''',
                             html.Span("pfv:past", className="smallCaps"),
        '''”, list “''',
                              html.Span("pl”, “poss”, “pfv”, “past”", className="smallCaps"),
        ''' separately);''']),
            html.Li(children=['''Don’t include numbers for grammatical person—if you have things like “3A” or “1''',
                              html.Span("pl", className="smallCaps"),
        '''”, include “A” and “''',
                             html.Span("pl", className="smallCaps"),
        '''” in your list, but not “3A”, “1''',
                              html.Span("pl", className="smallCaps"),
        '''” or “1”, “2”, “3”;''']),
            html.Li(children=['''Abbreviations that include subparts in superscript or subscript should be included in 
            the list along with HTML tags for super- or subscripting—for example, “''',
                            html.Span(className="smallCaps", children=['pl',html.Sub('excl')]),
                            '''” would be listed as “pl<sub>excl</sub>”. Use “<sup></sup>” tags for superscripting in the same way.'''])
        ])
        text3 = dcc.Markdown('''Super/subscripting for lexical items rather than grammatical abbreviations may 
        have to be applied manually in the ELAN or HTML file itself.''')

        abbr = html.Div(className='aboutContents',children=[title,text1,text2,text3])
        return abbr

    def makePreview(self):
        title = html.H3("Page preview")
        text = dcc.Markdown('''Prior to downloading the final product, the project can be viewed by following the
                "Open preview" link that appears after you click on the "Make page" button. This link will open the
                HTML document created by SLEXIL in a new tab in your browser. Note, however, that the line by line playback 
                icons and the audioplayer visible in the window may not be functional, depending on which browser and 
                which platform you are using to run SLEXIL. On a Mac, Chrome allows both line by line and continuous 
                playback, Firefox supports only line by line playback, and neither work in Safari. We have not tested 
                playback in the preview tab on other browsers, or on Windows or Linux platforms. Playback should be
                fully functional in the downloaded project regardless.''')

        preview = html.Div(className='aboutContents',children=[title,text])
        return preview

    def makeDownload(self):
        title = html.H3("Working with the downloaded project")
        text = dcc.Markdown('''Once you have built your SLEXIL project on the website, it can be downloaded as a folder 
        to your computer. The folder will be named for the title of your project and contains the 
        following: 1) an .html file, also named after your project; 2) a folder called “audio” 
        that contains the sound files needed by the project; 3) a CSS style sheet; 4) an ERRORS log 
        file (this will be empty if all went well); 5) two Javascript files used by the project 
        for playback. The .html file can be opened in any browser and will support line-by-line 
        and continuous playback as long as it is in the same folder as the other project components; 
        the CSS stylesheet can be edited to change the look of the page to your heart’s content. 
        The project can be uploaded to any webserver and will continue to work as long as the 
        directory structure is maintained (or appropriate changes are made to the .html file). 
        With proper modifications, the HTML code can be cut and pasted into various content 
        management systems like WordPress, though the details of this will depend on the system 
        and how it is set up to handle Javascript and media files.''')

        download = html.Div(className='aboutContents',children=[title,text])
        return download

    def makeCredits(self):
        title = html.H3("Credits")
        text = dcc.Markdown('''SLEXIL was created (in no particular order) by David Beck and Paul Shannon. Feedback, 
        bug reports, requests for assistance, and lavish praise can be sent to [David] (mailto:david.beck@ualberta.ca).''')

        credits = html.Div(className='aboutContents',children=[title,text])
        return credits

    def makePrivacy(self):
        title = html.H3("Privacy and copyright")
        text = dcc.Markdown('''Materials uploaded to the SLEXIL website are not retained and remain the property of the 
        uploader. They will not be viewed or used for any purpose by the adminstrators of this website. Recordings and texts 
        persist on the site for a short period after upload but are removed by an automatic process several times per 
        week; during the retention period they are not accessible to anyone but the site administrators. The site administrators 
        are not responsible for storing or archiving any materials or projects uploaded to or generated by 
        this site. Copyright of any project generated using SLEXIL belongs fully to the project's owner. We urge any 
        user working with data from indigenous or minority language communities to be sensitive to cultural and legal 
        conventions regarding provenance, attribution, authorship, and ownership of data particular to the context 
        in which they work.''')

        credits = html.Div(className='aboutContents',children=[title,text])
        return credits
