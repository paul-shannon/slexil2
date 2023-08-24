import os, pdb
#import importlib
import slexil
from importlib import resources as rezReader

class WebPacker:

    cssFiles = []
    jsFiles = []
    cssText = None
    jsText = None
    fullText = True
    verbose = False
    baseUrl = "https://slexilData.artsrn.ualberta.ca/includes"

    def __init__(self, fullText=True, verbose=False):
       self.fullText = fullText
       self.cssFiles = []
       self.jsFiles = []
       self.verbose = verbose

       self.cssFiles.append("bootstrap.min.css")
       self.cssFiles.append("slexil.css")

       self.jsFiles.append("showdown.min.js")
       self.jsFiles.append("jquery-3.6.3.min.js")
       self.jsFiles.append("slexil.js")
       self.jsFiles.append("bootstrap.bundle.min.js")
       self.jsFiles.append("annotations.js")

       if (self.verbose):
          for path in self.cssFiles:
            found = os.path.exists(path) 
            print("%s found? %s" % (path, found))

       if (self.verbose):
          for path in self.jsFiles:
             found = os.path.exists(path) 
             print("%s found? %s" % (path, found))

    def getCSSFilenames(self):
        return (self.cssFiles)

    def getJSFilenames(self):
        return(self.jsFiles)

    def readCSS(self):
        cssText = ""
        for file in self.cssFiles:
           newText = rezReader.read_text("slexil", file)
           cssText = cssText + "\n<style>\n" + newText + "\n</style>\n"
        self.cssText = cssText

    def readJS(self):
        jsText = ""
        for file in self.jsFiles:
           newText = rezReader.read_text("slexil", file)
           jsText = jsText + "\n<script>\n" +  newText + "\n</script>\n";
        self.jsText = jsText

    def getCSSText(self):
        if(self.fullText):
           return(self.cssText)
        else:
           urlText = ""
           for file in self.cssFiles:
               urlText += "%s/%s\n" % (self.baseUrl, file)
           return(urlText)

    def getJSText(self):
        if(self.fullText):
           return(self.jsText)
        else:
           urlText = ""
           for file in self.jsFiles:
               urlText += "%s/%s\n" % (self.baseUrl, file)
           return(urlText)

