# -*- tab-width: 3 -*-
# -*- coding: utf-8 -*-

from yattag import *
from yattag import Doc

class DropDownMenu:

   menuTitle = None
   menuOptions = []
   menuID = None
   
   def __init__(self, menuTitle, menuID, menuOptions):
      # print("dropDownMenu ctor, menuID: %s" % menuID)
      self.menuTitle = menuTitle
      self.menuID = menuID
      self.menuOptions = menuOptions

   def toHTML(self, htmlDoc):
      with htmlDoc.tag("div",  klass="dropdownMenu"):
         id2 = "%sButton" % self.menuID
         with htmlDoc.tag("button", id=id2, klass="menuButton"):
            htmlDoc.text(self.menuTitle)
         id2 = "%sItems" % self.menuID
         with htmlDoc.tag("div", id=id2, klass="menuItemsDiv"):
           optionClasses = "menuItem"
           #print(self.menuOptions)
           for option in self.menuOptions:
              with htmlDoc.tag("div", klass=optionClasses):
                 htmlDoc.text(option)
