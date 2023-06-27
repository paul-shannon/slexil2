lines <- readLines("eafSamples.txt")
names <- unlist(lapply(lines, basename))
names(lines) <- names
dups <- which(duplicated(names))
lines <- lines[-dups]
length(lines)

