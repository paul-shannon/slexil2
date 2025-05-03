class DropDownMenu{

   constructor(id, callback){

      this.callback = callback
      this.id = "#" + id + "Button";
      this.itemsID = "#" + id + "Items";

        //----------------
        // event handlers
        //----------------

            // button click display sthe items div
      $(this.id).on("click", () => $(this.itemsID).css("display", "block"))

            // items div hidden with click anywhere but button
      $(window).on("click", (event) => { // close the dropdown
        if(!event.target.matches(this.id)){
          $(this.itemsID).css("display", "none")
          }
        })

           // menu item click callback
      $(this.itemsID).on("click", (event) => {
        var menuText = event.target.innerHTML;
        this.callback(menuText);
        })
        
      } // ctor
   } // class 


function displayTopic(key){
   console.log("DropDownMenu.js, displayTopic: " + key)
   var annoBox = $("#annoNotesDiv");
   var annoText = lookup(key)
   console.log("annoText retrieved: " + annoText.length)
   annoBox.html(annoText);
   }

$(document).ready(function(){
    ddmTopics = new DropDownMenu("topics", displayTopic)
   })
