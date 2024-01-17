var state = {};

$(document).ready(function(){
   console.log( "ready!" );

  $("#topicsButton").on("click", function(event){
      console.log("linguistic topics menu button click")
      $("#topicsItems").show()
      state["topicsMenuVisible"] = true;
      })

  $("#treesButton").on("click", function(event){
      console.log("linguistic topics menu button click")
      $("#treesItems").show()
      state["treesMenuVisible"] = true;
      })

function showDropdownMenu() {
   console.log("show dropdown menu")
   document.getElementById("topicMenu").classList.toggle("show");
   }

$(".menuItemsDiv").on("click", function(event){
  console.log("menu item selected: " + event.target.innerHTML)
  window.x = event
  })

    // Close the dropdown if the user clicks outside of it -
    // on one of the options, or somewhere else altogether

window.onclick = function(event){
  //if (!event.target.matches('.menuButton')) {
  if (!event.target.matches('#topicsButton')) {
      if(state["topicsMenuVisible"]){
         }
     $(".menuItemsDiv").hide()   // hide them all
      }
  }

/*******************

************/
}) // document.ready
