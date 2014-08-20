####################################################################


#####    Testing of numerical output

#####    Very difficult to automate, because of stochasticity in methods.
##       with current data set used, CBS is +/- OK, but not the HMM-based methods.

#####   To obtain the RData for the comparisons and run this.  Of course,
#####   be sure parameters to segment are the right ones (and have the
#####   same values as the web run).



####  Beware: for CBS, if by Array*Chromosome, the pre-smoothing stage is not identical!!
####  Thus, code is changed in web server, to ensure usage of A method.

#### Prepare data set
dataIn <- read.table("two.sample.shuffled.num.test",
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
dataCGH <- as.matrix(dataIn[orderindex, 5:6])
Pos.ord <- mid.point[orderindex]


make.hmm.obj <- function(data, chrom, pos) {
    Clone <- 1:nrow(data)
    obj <- create.aCGH(data.frame(data),
                       data.frame(Clone = Clone,
                                  Chrom = chrom,
                                  kb     = pos))
    return(obj)
}

doHMM <- function(data, nsamp) {
    res <- find.hmm.states(data, aic = TRUE, bic = FALSE)
    hmm(data) <- res
    r1 <<- hmm(data)
    m <- matrix(NA, nrow = nrow(data$hmm$states.hmm[[1]]),
                ncol = nsamp)
    for(j in 1:nsamp) {
        m[, j] <- mergeLevels(data$hmm$states.hmm[[1]][, 2 + (6 * j)],
                              data$hmm$states.hmm[[1]][, 2 + (6 * j) - 2])$vecMerged
    }
    write.table(file = "HMM.R.output.txt", m)
    return(m)
}

fHMM <- function(data, chrom, pos) {
    obj <- make.hmm.obj(data, chrom, pos)
    return(doHMM(obj, ncol(data)))
}
    

fBioHMM <- function(data, Chrom, Pos) {
    uchrom <- unique(Chrom)
    m <- matrix(NA, nrow = nrow(data), ncol = ncol(data))
    for (j in 1:ncol(data)) {
        dataj <- data[, j]
        smoothed <- NULL
        
        for (ic in uchrom) {
            ydat <- dataj[Chrom == ic]
            n <- length(ydat)
            res <- snapCGH:::fit.model(sample = 1, chrom = ic, dat = matrix(ydat, ncol = 1),
                             datainfo = data.frame(Name = 1:n, Chrom = rep(ic, n),
                             Position = Pos[Chrom == ic]))
            
            smoothed <- c(smoothed, res$out.list$mean)
        }
        m[, j] <- mergeLevels(data[, j], smoothed)$vecMerged
    }
    write.table(file = "BioHMM.R.output.txt", m)
    return(m)
}



fGLAD <- function(data, Chrom, Pos) {
    m <- matrix(NA, nrow = nrow(data), ncol = 2 * ncol(data))
    Pos <- if (is.null(Pos)) (1:nrow(data)) else Pos
    for(j in 1:ncol(data)) {
        x <- data[, j]
        tmpf <- data.frame(LogRatio = x,
                           PosOrder = Pos,
                           Chromosome = Chrom)
        tmpf <- list(profileValues = tmpf)
        class(tmpf) <- "profileCGH"
        outglad <- glad.profileCGH(tmpf)
        m[, ((2 * j) - 1)] <- outglad$profileValues$Smoothing
        m[, (2 * j)] <- outglad$profileValues$ZoneGNL
    }
    write.table(file = "GLAD.R.output.txt", m)
    return(m)
}







make.cbs.obj <- function(tmp, chrom, pos) {
    cna.obj <- CNA(tmp, chrom, pos,
                         data.type = "logratio")
    return(cna.obj)
}

mergeDNAcopy <- function(object) {
    numarrays <- ncol(object$data) - 2
    ## zz: we must get numarray from object
    
    if(!(inherits(object, "DNAcopy")))
        stop("This function can only be applied to DNAcopy objects")
    merged_segments <- list()
    merged_segments$chrom.numeric <- object$data$chrom ## verify its numeric zz!!
    merged_segments$segm <- list()
    for(arraynum in 1:numarrays) {
        obs <- object$data[, 2 + arraynum]
        segmented <-
            object$output[object$output$ID ==
                          colnames(object$data)[2 + arraynum], ]
        segmentus <- object$data$maploc
        for(i in 1:nrow(segmented)) {
            segmentus[(segmented[i,'loc.end'] >= segmentus) &
                      (segmented[i,'loc.start'] <= segmentus)] <-
                          segmented[i,'seg.mean']
        }
        segmentus2 <- mergeLevels(obs, segmentus)$vecMerged
        classes.ref <- which.min(abs(unique(segmentus2)))
        classes.ref <- unique(segmentus2)[classes.ref]
        ref <- rep(0, length(segmentus2))
        ref[segmentus2 > classes.ref] <- 1
        ref[segmentus2 < classes.ref] <- -1
        merged_segments$segm[[arraynum]] <- cbind(obs,
                                                  merged.mean = segmentus2,
                                                  alteration = ref)
    }
    class(merged_segments) <- c(class(merged_segments),
                                "mergedDNAcopy")
    return(merged_segments)
}    

fCBSo <- function(data, chrom, pos) {
    ## this is the old one, with prunning
    data <- make.cbs.obj(data, chrom, pos)
    smoothed <- smooth.CNA(data)
    segmented <- segment(smoothed, undo.splits = "prune", nperm = 10000)
    res <- mergeDNAcopy(segmented)
    return(res)
}


fCBS <- function(data, chrom, pos) {
    data <- make.cbs.obj(data, chrom, pos)
    smoothed <- smooth.CNA(data)
    segmented <- segment(smoothed, undo.splits = "none", nperm = 10000)
    res <- mergeDNAcopy(segmented)
    write.table(file = "CBS.R.output.txt", res)
    return(res)
}


fc3 <- function(x, y, tol = 1e-06) {
    tmp <- max(abs(x - y))
    if(tmp < tol) {
        return("OK")
    } else{
        return("Failed? ---but look at figures; tests can seem to fail when really OK")
    }
}

cbs.compare <- function(res.cbs.r, res.web, filename = "cbscompare.pdf") {
    rcbs <- matrix(unlist(res.cbs.r$segm), ncol = 3 * length(res.cbs.r))
    res.web <- res.web[ , -(1:6)]
    ncl <- ncol(res.web)
    pdf(file = filename)
    for(i in seq(from = 2, to = ncl - 1, by = 3)) {
        par(pty = "s")
        plot(jitter(res.web[, i]), jitter(rcbs[, i]))
        abline(a = 0, b = 1, lty = 2)
    }
    dev.off()

    fc3(rcbs, res.web, tol = 5e-05) ## cbs only provides four digits
}
    

hmm.compare <- function(rd, wd, filename = "hmmcompare.pdf") {
    ncrd <- ncol(rd)
    wdo <- wd[, 8 + (0:(ncrd - 1)) * 3]
    pdf(file = filename)
    for(i in 1:ncrd) {
        par(pty = "s")
        plot(jitter(rd[, i]), jitter(wdo[, i]))
        abline(a = 0, b = 1, lty = 2)
    }
    dev.off()
    fc3(rd, wdo)
}
    

glad.compare <- function(rd, wd) {
    ncrd <- ncol(rd)/2
    nocols <- 1:6
    nocols <- c(nocols, 7 + (0:(ncrd - 1))* 3)
    wdo <- wd[, -nocols]
    pdf(file = "gladcompare.pdf")
    for(i in 1:ncrd) {
        par(pty = "s")
        plot(jitter(rd[, i]), jitter(wdo[, i]))
        abline(a = 0, b = 1, lty = 2)
    }
    dev.off()
    fc3(rd, wdo)
}


test.cbs <- function() {
    ## this will not work if tilingArray loaded ...
    try(detach("package:tilingArray"))
    library(DNAcopy)
    library(aCGH)
    cbs.r.out <- fCBS(dataCGH, Chrom.ord, pos = 1:length(Chrom.ord))
    cbs.web.out <- read.table("CBS.web.output.txt", sep = "\t", header = TRUE)
    rv <- cbs.compare(cbs.r.out, cbs.web.out)
    save(file = "cbs.test.RData", list = ls())
    return(rv)
}

test.hmm <- function() {
    library(aCGH)
    library(snapCGH)
    hmm.r.out <- fHMM(dataCGH, Chrom.ord, pos = 1:length(Chrom.ord))
    hmm.web.out <- read.table("HMM.web.output.txt", sep = "\t", header = TRUE)
    rv <- hmm.compare(hmm.r.out, hmm.web.out)
    save(file = "hmm.test.RData", list = ls())
    return(rv)
}    
test.biohmm <- function() {
    library(aCGH)
    library(snapCGH)
    biohmm.r.out <- fBioHMM(dataCGH, Chrom.ord, Pos.ord)
    biohmm.web.out <- read.table("BioHMM.web.output.txt", sep = "\t", header = TRUE)
    rv <- hmm.compare(biohmm.r.out, biohmm.web.out, filename = "biohmmcompare.pdf")
    save(file = "biohmm.test.RData", list = ls())
    return(rv)
}
    
test.glad <- function() {
    library(GLAD)
    glad.r.out <- fGLAD(dataCGH, Chrom.ord, NULL)
    glad.web.out <- read.table("GLAD.web.output.txt", sep = "\t", header = TRUE)
    rv <- glad.compare(glad.r.out, glad.web.out)
    save(file = "glad.test.RData", list = ls())
    return(rv)
}
    



##  Because of name conflicts, cannot load all packs. at same time
## library(DNAcopy)
## library(aCGH)


## ## Note that there is variability among runs, which can lead to apparently
## ## failed tests. The current data set seems to (almost) always lead to the same
## ## solutions, but it need not be so.

## ## the actual computations and comparisons
## cbs.r.out <- fCBS(dataCGH, Chrom.ord, pos = 1:length(Chrom.ord))
## cbs.web.out <- read.table("CBS.output.txt", sep = "\t", header = TRUE)
## cbs.compare(cbs.r.out, cbs.web.out)

## ## If you think there is variability among runs of CBS, wait till you see HMMs!

## library(snapCGH)
## hmm.r.out <- fHMM(dataCGH, Chrom.ord, pos = 1:length(Chrom.ord))
## hmm.web.out <- read.table("HMM.output.txt", sep = "\t", header = TRUE)
## hmm.compare(hmm.r.out, hmm.web.out)

## biohmm.r.out <- fBioHMM(dataCGH, Chrom.ord, Pos.ord)
## biohmm.web.out <- read.table("BioHMM.output.txt", sep = "\t", header = TRUE)
## hmm.compare(biohmm.r.out, biohmm.web.out)
## ## If we wanted to get really fancy, we'd try to formally compare results
## ## from multiple runs of each. But the plots above are enough, probably.



## ## GLAD seems fairly stable.

## glad.r.out <- fGLAD(dataCGH, Chrom.ord, NULL)
## glad.web.out <- read.table("GLAD.output.txt", sep = "\t", header = TRUE)
## glad.compare(glad.r.out, glad.web.out)
