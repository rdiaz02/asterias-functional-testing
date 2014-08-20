#####   To obtain the RData for the comparisons and run this.  Of course,
#####   be sure parameters to segment are the right ones (and have the
#####   same values as the web run).

library(DNAcopy)
dataIn <- read.table("two.samp.shuffled.clean.one.file",
                     sep = "\t", header = TRUE,
                     comment.char = "")

######### Turn chromosome into a number
tmpchr <- sub("chr", "", dataIn$Chromosome)
Chrom <- as.numeric(as.character(tmpchr))
Chrom[tmpchr == "X"] <- 23
## Verify all is OK
table(Chrom, dataIn$Chromosome)


########### Order data
mid.point <- dataIn$UG.Start +
    0.5 * (dataIn$UG.End - dataIn$UG.Start)

orderindex <- order(Chrom, mid.point,
                     dataIn$UG.Start,
                     dataIn$UG.End)
## Verify no duplicate spots. Not a big deal, but better if not.
tmp <- paste(Chrom, mid.point, sep = ".")
length(tmp) == length(unique(tmp))


Chrom.ord <- Chrom[orderindex]
dataCBS <- as.matrix(dataIn[orderindex, 5:6])
maploc  <- 1:length(Chrom.ord)
cbs.object <- CNA(dataCBS, chrom = Chrom.ord,
                  maploc = maploc,
                  sampleid = colnames(dataCBS),
                  data.type = "logratio")
smoothed.cbs.object <- smooth.CNA(cbs.object)

segmented.output <- segment(smoothed.cbs.object,
                            alpha = 0.01,
                            nperm = 50000,
                            p.method = "hybrid",
                            kmax = 25,
                            nmin = 200,
                            overlap = 0.25,
                            trim = 0.025,
                            undo.prune = 0.05,
                            undo.SD = 3,
                            undo.splits = "prune")

## store these two functions;
## fc1: they compare start, end, and segment mean for a given array
fc1 <- function(x, y, name) {
    x$output[x$output$ID == name, c(3, 4, 6)] -
        y$output[y$output$ID == name, c(3, 4, 6)] 
        }
## fc2: they compare start, end, and segment mean for all arrays
fc2 <- function(x, y, tol = 1e-06) {
    tmp <- max(abs(x$output[, c(3, 4, 6)] -
        y$output[, c(3, 4, 6)] ))
    if(tmp < tol) {
        return("OK")
    } else{
        return("Failed")
    }
}

## Info about R and the library
version.R.of.run <- version
library.info <- library(help="DNAcopy")



save(file = "reference.testCBS_paral.RData", list = ls())


## load("tmp.testCBS_paral.RData")
 reordered.web <- list()
 reordered.web$output <- segment.smoothed.CNA.object$output[, c(6, 1: 5)]
 for(i in 2:5) {
     summary(reordered.web[, i] - segmented.output$output[, i])
 }







