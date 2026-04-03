library(jsonlite)
json <- toJSON(read.table("radicals.tsv", sep="\t", header=TRUE))
f <- file("radicals.json", open="a")
writeLines(json, f, sep="\n");
close(f)
