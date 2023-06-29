import os, pdb
import slexil

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

       self.cssFiles.append(os.path.join(baseDir, "bootstrap.min.css.py"))
       self.cssFiles.append(os.path.join(baseDir, "slexil.css.py"))

       self.jsFiles.append(os.path.join(baseDir, "showdown.js.py"))
       self.jsFiles.append(os.path.join(baseDir, "jquery-3.6.3.min.js.py"))
       self.jsFiles.append(os.path.join(baseDir, "slexil.js.py"))
       self.jsFiles.append(os.path.join(baseDir, "bootstrap.bundle.min.js.py"))
       self.jsFiles.append(os.path.join(baseDir, "annotations.js.py"))

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
           f = open(file)
           newText = f.read()
           cssText = cssText + "\n<style>\n" + newText + "\n</style>\n"
           f.close()
        self.cssText = cssText

    def readJS(self):
        jsText = ""
        for file in self.jsFiles:
           f = open(file)
           newText = f.read()
           jsText = jsText + "\n<script>\n" +  newText + "\n</script>\n";
           f.close()
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

