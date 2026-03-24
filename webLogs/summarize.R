library(jsonlite)
library(ipapi.r)
tbl.sites <- read.table("ip.csv", sep=",", header=TRUE)
#f <- "2026-mar-15.txt"
#f <- "2026-mar-13.txt"
f <- "2026-mar-17.txt"
f <- "2026-mar-20.txt"
f <- "2026-mar-23.txt"

tbl.in <- read.table(f, sep="\t", header=FALSE)
deleters <- c(1,3,5,7,9)
tbl.in <- tbl.in[, -deleters]
head(tbl.in)
colnames(tbl.in) <- c("hits", "files", "kb", "visits", "host")

tbl <- data.frame(city=character(0), hits=integer(0), visits=integer(0),
                  files=integer(0), host=character(0), state=character(0), country=character(0))

for(i in seq_len(nrow(tbl.in))){
   visits = tbl.in$visits[i]
   host <- tbl.in$host[i]
   hits <- tbl.in$hits[i]
   fileCount <- tbl.in$files[i]
   #x <- fromJSON(IPQuery(host))$location
   #city <- x$city
   #state <- x$state
   #country <- x$country
   #countryCode <- x$country_code
   city <- "unknown"
   if(host %in% tbl.sites$ip)
      city <- subset(tbl.sites, ip==host)$site
   newRow <- list(city=city, hits=hits, visits=visits,
                  files=fileCount, host=host)
   tbl <- rbind(tbl, newRow)
   #printf("%40s %4d  %15s  %20s %5s",
   #       city, visits, fileCount, host, state, countryCode)
   }

new.order <- order(tbl$hits, decreasing=TRUE)
tbl <- tbl[new.order,]
print(tbl)

