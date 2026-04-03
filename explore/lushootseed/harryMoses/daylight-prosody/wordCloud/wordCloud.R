library(wordcloud2)
library(htmlwidgets)
library(jsonlite)

f <- "spoken.txt"
f <- "morphemes.txt"
f <- "radicals-and-nouns.txt"
x <- readLines(f)

length(x) # 1313
xtab <- sort(table(x))
length(xtab)  # 278
xtab <- xtab[xtab > 3]
xtab <- xtab[xtab < 10]
length(xtab)
words <- names(xtab)
freq <- as.integer(xtab)
tbl <- data.frame(word=words, freq=freq)
toJSON(tbl, dataframe="values")

wordcloud2(data = tbl,
           size = 1.0,
           color = "random-dark",
           backgroundColor = "white",
           shape = "circle",
           rotateRatio = 0.5)

print(tbl)
