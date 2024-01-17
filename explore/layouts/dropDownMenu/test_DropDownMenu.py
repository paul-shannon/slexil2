from yattag import *
from dropDownMenu import DropDownMenu

def createDocument():
    
   htmlDoc = Doc()
   menu = DropDownMenu(menuTitle = "Linguistic Topics",
                       menuID="topics",
                       menuOptions=["IRR", "CTD", "CNTRPT"])

   menu2 = DropDownMenu(menuTitle="Trees", menuID="trees",
                        menuOptions=["Hemlock", "Alder", "Doug fir",
                                     "Yew", "Cedar", "Alder", "Apple", "Ash",
                                     "Aspen", "Basswood", "Birch", "Buckeye",
                                     "Buckthorn", "California-laurel", "Catalpa",
                                     "Cedar", "Cherry", "Chestnut", "Chinkapin",
                                     "Cottonwood", "Cypress", "Dogwood",
                                     "Douglas-fir", "Elm", "Fir", "Filbert", 
                                     "Sequoia", "Hawthorn", "Hazel", "Hemlock",
                                     "Honeylocust", "Holly", "Horsechestnut",
                                     "Incense-cedar", "Juniper", "Larch", "Locust",
                                     "Madrone", "Maple", "Mountain-ash",
                                     "Mountain-mahogany", "Oak", "Oregon-myrtle",
                                     "Pear", "Pine", "Plum", "Poplar",
                                     "Redcedar/Arborvitae", "Redwood",
                                     "Russian-olive", "Spruce", "Sweetgum",
                                     "Sycamore", "Tanoak", "True Cedar",
                                     "True Fir", "Walnut", "White-cedar", "Willow",
                                     "Yellow-poplar", "Yew"])



   htmlDoc.asis('<!DOCTYPE html>\n')
   with htmlDoc.tag('html', lang="en"):
       with htmlDoc.tag('head'):
           htmlDoc.asis('<meta charset="UTF-8"/>')
           htmlDoc.asis('<title>%s</title>' % "dropdown menu")
           htmlDoc.asis('<link rel="stylesheet" href="dropDownMenu.css">')
           htmlDoc.asis('<script src="https://slexilData.artsrn.ualberta.ca/includes/jquery-3.6.3.min.js"></script>')
           htmlDoc.asis('<script src="DropDownMenu.js"></script>')
       with htmlDoc.tag('body'):
           with htmlDoc.tag("div", id="menuDiv_1", style="margin: 30px;"):
              menu.toHTML(htmlDoc)
           with htmlDoc.tag("div", id="menuDiv_2", style="margin: 30px;"):
              menu2.toHTML(htmlDoc)
                  

   filename = "test_DropDownMenu.html"
   f = open(filename, "wb")
   f.write(bytes(indent(htmlDoc.getvalue()), "utf-8"))
   f.close()
   print("wrote %s" % f.name)

if __name__ == '__main__':
    createDocument()
    
              
                   
