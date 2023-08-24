import os, pdb
#import importlib
import slexil
from importlib import resources as rezReader

class WebPacker:

    baseDir = None
    cssFiles = []
    jsFiles = []
    cssText = None
    jsText = None
    verbose = False
	
    def __init__(self, baseDir, verbose=False):
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
        return(self.cssText)

    def getJSText(self):
        return(self.jsText)


#
#	def getSlexiljs(self):
#		fulljsText = "".join(["<script>", self.slexiljsText, "</script>"])
#		return(fulljsText)
#
#	def getShowdownjs(self):
#		fulljsText = "".join(["<script>", self.showdownjsText, "</script>"])
#		return(fulljsText)
#
#	def getAnnotationjs(self):
#		fulljsText = "".join(["<script>", self.annotationsjsText, "</script>"])
#		return(fulljsText)

