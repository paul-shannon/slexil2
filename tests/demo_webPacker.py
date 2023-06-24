import unittest
import re
import os
import pdb
import slexil
from slexil.webPacker import WebPacker

baseDir = os.path.dirname(slexil.__file__)

packer = WebPacker(baseDir)
packer.readJS()
jsText = packer.getJSText()
print("character count: %d" % len(jsText))
openTags = [m.start() for m in re.finditer("<script>", jsText)]
closeTags = [m.start() for m in re.finditer("</script>", jsText)]
print("js open  tags: %d" % len(openTags))
print("js close tags: %d" % len(closeTags))
