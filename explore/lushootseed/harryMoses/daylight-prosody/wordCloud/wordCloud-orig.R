library(wordcloud2)
library(htmlwidgets)
library(jsonlite)

f <- "spoken.txt"
f <- "morphemes.txt"
f <- "radicals-and-nouns.txt"
x <- readLines(f)

length(x) # 726
xtab <- sort(table(x))
xtab <- xtab[xtab > 3]
xtab <- xtab[xtab < 10]
words <- names(xtab)
freq <- as.integer(xtab)
tbl <- data.frame(word=words, freq=freq)
toJSON(tbl, dataframe="values")
#write

hoverFunction <- "function fubar(item, dimension, event){
    if(dimension){
       console.log('entering');
      } else {
       console.log('leaving');
      }
    }"


hover_js_function <- "function(item, dimension, event) {
  if (dimension) {
    var word = item[0];
    var frequency = item[1];
    alert('Word: ' + word + ', Frequency: ' + frequency);
  } else {
  }
}"


widget <-
wordcloud2(data = tbl,
           size = 1.0,
           color = "random-dark",
           backgroundColor = "white",
           shape = "circle",
           rotateRatio = 0.5,
           hoverFunction=hoverFunction)
           #hoverFunction=hover_js_function)

saveWidget(widget, "cloud.html", selfcontained=FALSE)
