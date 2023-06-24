import os, pdb
import slexil

class WebPacker:

    baseDir = None
    cssFiles = []
    jsFiles = []
    cssText = None
    jsText = None
	
    def __init__(self, baseDir):
       self.cssFiles = []
       self.jsFiles = []

       self.cssFiles.append(os.path.join(baseDir, "bootstrap.min.css.py"))
       self.cssFiles.append(os.path.join(baseDir, "slexil.css.py"))

       self.jsFiles.append(os.path.join(baseDir, "showdown.js.py"))
       self.jsFiles.append(os.path.join(baseDir, "jquery-3.6.3.min.js.py"))
       self.jsFiles.append(os.path.join(baseDir, "slexil.js.py"))
       self.jsFiles.append(os.path.join(baseDir, "bootstrap.bundle.min.js.py"))

       for path in self.cssFiles:
          found = os.path.exists(path) 
          print("%s found? %s" % (path, found))

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
           newText = open(file).read()
           cssText = cssText + "\n<style>\n" + newText + "\n</style>\n"
        self.cssText = cssText

    def readJS(self):
        jsText = ""
        for file in self.jsFiles:
           newText = open(file).read()
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

