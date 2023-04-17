# the customization hook is in the header of slexil html documents
# here we replace it with everything in custom.html, which for now
# is a few tags to include the knowledge base (kb.js) and code + css
# which uses it.

/<!-- headCustomizationHook -->/ {
 r headCustomizations.html
 d
}

/<!-- bodyTopCustomizationHook -->/ {
  r bodyTop.html
  d
}

/<!-- bodyBottomCustomizationHook -->/ {

  r bodyBottom.html
  d

}



