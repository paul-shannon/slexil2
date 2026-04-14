# the customization hook is in the header of slexil html documents
# here we replace it with everything in custom.html, which for now
# is a few tags to include the knowledge base (kb.js) and code + css
# which uses it.

/<!-- bodyBottomInsertionHook -->/ {
  r verbCribsheet.js
  d

}

/<!-- otherControlsInsertionHook -->/ {
  r wordCloudInsertion-d3.txt
  d

}




