assert <- function(x, message) {
 if(any(is.na(x)) || !all(x)) stop(message)
}


dataRead <- function(dataName) {
    assign(paste(dataName, ".covar", sep = ""),
           read.table(paste(dataName, ".data.txt", sep = ""),
                      header = FALSE, sep = "\t",
                      row.names = 1),
           env = .GlobalEnv)
     assign(paste(dataName, ".class", sep = ""),
            scan(paste(dataName, ".class.txt",  sep = ""), what = "",),
            env = .GlobalEnv)
}


generateData <- function(numc = numCl, 
                         agediff = runif(1, 0, 0.0001),
                         meandiff = runif(1, 0, 0.0051),
                         ngenes = nGenes,
                         ndiff = nDiff,
                         cl2diff = runif(1, 0, 0.0001)) {

    ntot <- sum(numc)
    genes <- matrix(rnorm(ngenes * ntot),
                    ncol = ntot)
    
    covar <- data.frame(Class =
                        rep(seq(0, numGroups - 1), numc),
                        Age = rnorm(ntot),
                        Age2 = rnorm(ntot),
                        Class2 = sample(c(-1, 0, 1), ntot, replace = TRUE))

    classDiff <- meandiff * covar$Class
    
    agediffef <- agediff * covar$Age
    cl2eff <- cl2diff* covar$Class2
    otherEffects <- agediffef + cl2eff

    genes <- t(t(genes) + otherEffects)
    genes[1:ndiff, ] <- t(t(genes[1:ndiff, ]) + classDiff)

    genes <- genes[sample(1:ngenes), ]

    covar$Class2 <- factor(covar$Class2)
    covar$Class <- factor(covar$Class)
    return(list(geneExpression = genes, covars = covar))
}


permutRegres <- function(genes, depvar, B) {
    ## multtest does not deal with regression, but
    ## Pomelo II does. Here is a simple way of getting
    ## permutation-based p-values.
    ## Sure, this is _very_ slow
    cat("\n Computing observed statistic  \n")
    obsStat <- apply(genes, 1,
                     function(x) {summary(lm(depvar ~ x))$coeff[2, 3]})
    N <- length(depvar)
    countLarger <- rep(0, nrow(genes))
    absObsStat <- abs(obsStat)
    for(i in 1:B) {
        cat("\n Doing permutation ", i, "\n")
        depPerm <- sample(depvar)
        permStat <- apply(genes, 1,
                          function(x) {abs(summary(lm(depPerm ~ x))$coeff[2, 3])})
        addToCount <- ifelse(permStat >= absObsStat, 1, 0)
        countLarger <- countLarger + addToCount
    }
    unadjp <-  (countLarger + 1)/(B + 1)
    return(list(statistic = obsStat,
                unadjp = unadjp,
                adjp = p.adjust(unadjp, method = "BH"),
                B = B))
}


doMultest <- function(genes = Data$geneExpression,
                      class = Data$covar$Class,
                      testtype = testType,
                      B=200000) {
    
    if(testtype == "Regres") {
        permutRegres(genes, class, B = B)
    } else {       
        mtTmp <- mt.maxT(genes, class, testtype, B=B)
        toOrder <- order(mtTmp$index)
        unadjp <- mtTmp$rawp[toOrder]
        return(list(statistic = mtTmp$teststat[toOrder],
                unadjp = unadjp,
                adjp = p.adjust(unadjp, method = "BH"),
                B=B))
    }
}


stretched.out <- function(x, file) {
    ## Use params for write.table so that most
    ## files written in the way programs take them:
    ## a vector
    write.table(x, file = file,
                quote = FALSE, sep = "\t",
                eol = "\t",
                col.names = FALSE,
                row.names = FALSE)
}


exportData <- function(Data = Data,
                       ngenes = nGenes,
                       out_added_covars = FALSE,
                       out_surv = FALSE,
                       outGene  = "./tmp/geneexpr.txt",
                       outClass = "./tmp/class.txt",
                       outCovs  = "./tmp/othercovs.txt",
                       outSurv  = "./tmp/surv.txt",
                       outEvent = "./tmp/event.txt") {
    ## Write data as text, so that the web applications
    ## can use these data

    
    ## We must ensure no name repetitions
    gnl <- round(runif(nGenes, 7, 80))
    namesRepeated <- TRUE
    while(namesRepeated) {
        geneNames <-
            sapply(gnl,
                   function(x)
                   paste(sample(CHARS_FOR_NAMES, x, replace = TRUE),
                         sep = "", collapse = ""))
        if(length(unique(geneNames)) == nGenes)
            namesRepeated <- FALSE
##        assert(length(unique(geneNames)) <= nGenes)
    }

    tmpd <- data.frame(gn = geneNames,
                       Data$geneExpression)
    write.table(tmpd, file = outGene, 
                quote = FALSE, sep = "\t",
                col.names = FALSE,
                row.names = FALSE)
    if(out_surv) {
        stretched.out(Data$SurvTime, file = outSurv)
        stretched.out(Data$Event, file = outEvent)
    } else {
        stretched.out(Data$Class, file = outClass)
    }
    
    if(out_added_covars) {
        write.table(Data$covars[, -1],
                    file = outCovs, 
                    quote = FALSE, sep = "\t",
                    col.names = FALSE,
                    row.names = FALSE)
    }
}


## Data <- generateData()
## exportData()
## doMultest()






#######################################


##  Comparing output


getNPerms <- function(filename = "./tmp-files/results.txt") {
    ## This uses too much knowledge of the output format
    s1 <- system("grep 'Permutations used:' ./tmp-files/results.txt",
                 intern = TRUE)
    nPerms <- as.numeric(strsplit(s1, "\t")[[1]][3])
    return(nPerms)
}

getReferencePerms <- function(multestObject){
    return(multestObject$B)
}


pvToSuccessFailure <- function(p, n) {
    suc <- round(p * n)
    return(cbind(suc, n - suc))
}


readPomeloOutput <- function(filename = "./tmp-files/results.txt") {
    pomtmp <- read.table(file = filename, header = TRUE, sep = "\t",
                         quote = "", skip = 13)
    return(pomtmp[order(pomtmp[, 1]), ])
}

comparepV <- function(succ1, fail1, succ2, fail2){
    ## fisher's exact test to compare p-values
tmp <- cbind(succ1, fail1, succ2, fail2)
    return(apply(tmp,  1,
                 function(x)
                 prop.test(rbind(c(x[1], x[2]), c(x[3], x[4])))$p.value))
##                 fisher.test(rbind(c(x[1], x[2]), c(x[3], x[4])))$p.value))
}

pvMessage <- function(pvpv) {
    ##pvpv are p-values of p-value differences
    cat("\n With these many tests, under independence, \n",
        " you should expect about ", round(0.05 * length(pvpv)), "\n",
        "p-values less than 0.05.\n")
    cat("\n There are ", sum(pvpv < 0.05), " such p-values less than 0.05.\n")
}
    


pvComps <- function(pv.pomelo, pv.reference, 
                   npermsPomelo, npermsRef, names) {
## compares p-values from permutation tests    
    sf.reference <- t(sapply(pv.reference,# ference$unadjp,
                            function(z)
                            pvToSuccessFailure(z, npermsRef)))
    sf.pomelo    <- t(sapply(pv.pomelo,
                            function(z)
                            pvToSuccessFailure(z, npermsPomelo)))
    pv.diffs.pvs <- comparepV(sf.reference[, 1],
                              sf.reference[, 2],
                              sf.pomelo[, 1],
                              sf.pomelo[, 2])
    pvMessage(pv.diffs.pvs)
    pv.failed <- which(pv.diffs.pvs < 0.05)
    if (length(pv.failed)) {
        cat("\n         Cases with significantly different p-values are:\n")
        for(i in pv.failed) {
            cat("          ", names[i],
                ", p-value of proportion comparison: ",
                pv.diffs.pvs[i],
                "; Reference: ", pv.reference[i],
                "; Pomelo results: ", pv.pomelo[i], "\n")
        }
    }
    if(length(pv.failed) > (2 * 0.05 * length(pv.diffs.pvs))) {
        c2 <- (" WARNING: likely problem with p-value comparison\n")
    } else {
        c2 <- "OK"
    }
}



compareAppr <- function(x, y, names,
                        tol = .Machine$double.eps ^ 0.5) {
    ## Compares numeric values
    f1 <- function(a, b, name) {
        equality <- all.equal(a, b, check.attributes = FALSE,
                              tolerance = tol)
        nonEqMessage <- paste("Equality failed at ",
                              name,". Values are",
                              a, ", ", b, ". ",
                              equality, sep = "")

        ifelse(isTRUE(equality), "OK", nonEqMessage)
    }
    eqcomp <- mapply(f1, x, y, names)
    if(all(eqcomp == "OK")) return("OK")
    else return(eqcomp[eqcomp != "OK"])
}

compareAppr2 <- function(x, y, names,
                         tol = 0.015,
                         machinetol = .Machine$double.eps ^ 0.5) {
    ## Compares numeric values
    ## we flag a difference is the difference is tol times the
    ## smallest value (or if the difference is undetetable given
    ## machine precission and the coming and goings of roundings, etc)
    f1 <- function(a, b, name) {
        equality <-
            isTRUE((((abs(a - b))/min(abs(a), abs(b))) < tol)
                   || (abs(a - b) < machinetol))
        nonEqMessage <- paste("Equality failed at ",
                              name,". Values are ",
                              a, ", ", b, ". ",
                              " abs(a - b) = ", abs(a - b),
                              "; min(abs(a), abs(b)) = ", min(abs(a), abs(b)),
                              "; ratio = ", abs(a - b)/min(abs(a), abs(b)),
                              sep = "")

        ifelse(isTRUE(equality), "OK", nonEqMessage)
    }
    eqcomp <- mapply(f1, x, y, names)
    if(all(eqcomp == "OK")) return("OK")
    else return(eqcomp[eqcomp != "OK"])
}




comparePomelo <- function(pomelo, reference, fisher = FALSE) {
## Compares statistc, p-value and FDR for non-limma and non-permutation tests
    if(! fisher) {
        names <- pomelo$ID
        cat("\n\n Comparing coefficients:    ")
        c1 <- compareAppr(pomelo$obs_stat, reference$coefficient,
                          pomelo$ID)
        cat(c1)
        cat("\n\n Comparing p-values:        ")
        c2 <- compareAppr(pomelo$unadj.p, reference$pvalue,
                          pomelo$ID)
        cat(c2)
        cat("\n\n Verifying FDR adjustment:  ")
        c3 <- compareAppr(pomelo$FDR_indep,
                          p.adjust(pomelo$unadj.p, method = "BH"),
                          pomelo$ID)
        cat(c3)
        cat("\n\n")
        if(!(all(c1 == "OK", c2 == "OK", c3 == "OK"))) {
            cat("\n ERROR: At least one test failed. See above.\n")
            return("ERROR: test failed")
        }
    } else { ## fisher's test
        names <- pomelo$ID
        cat("\n\n Comparing p-values:        ")
        c2 <- compareAppr(pomelo$unadj.p, reference, 
                          pomelo$ID)
        cat(c2)
        cat("\n\n Verifying FDR adjustment:  ")
        c3 <- compareAppr(pomelo$FDR_indep,
                          p.adjust(pomelo$unadj.p, method = "BH"), 
                          pomelo$ID)
        cat(c3)
        cat("\n\n")
        if(!(all(c2 == "OK", c3 == "OK"))) {
            cat("\n ERROR: At least one test failed. See above.\n")
            return("ERROR: test failed")
        }        
    }
}



comparePermutPomelo <- function(pomelo, reference, 
                                compare.p.values = 1) {
    ## Compares statistc, p-value and FDR for permutation tests
    ## Note: we use the abs(statistic) because the sign
    ## depends on silly details of how R and C++ order
    ## (lexicographically) the values
    npermsRef <- getReferencePerms(reference)
    npermsPomelo <- getNPerms()
    names <- pomelo$ID
    cat("\n\n Comparing coefficients:    ")
    c1 <- compareAppr(pomelo$obs_stat, reference$statistic,
                      pomelo$ID)
    cat(c1)
    if(compare.p.values) {
        cat("\n\n Comparing p-values:        ")
        c2 <- pvComps(pomelo$unadj.p, reference$unadjp,
                      npermsPomelo, npermsRef, names)
    } else {
        c2 <- "OK"
    }
    
    cat("\n\n Verifying FDR adjustment:  ")
    c3 <- compareAppr(pomelo$FDR_indep,
                      p.adjust(pomelo$unadj.p, method = "BH"),
                      pomelo$ID)
    cat(c3)
    cat("\n\n")
    if(!(all(c1 == "OK", c2 == "OK", c3 == "OK"))) {
        cat("\n ERROR: At least one test failed. See above.\n")
        return("ERROR: test failed")
    }
}



comparePomeloLimma <- function(pomelo, reference, tol = 1e-02) {
## Compares statistc, p-value and FDR for limma tests
    ## Note that there seem to be numerical differences among
    ## limma versions; thus the compareAppr2
    names <- pomelo$ID
    cat("\n\n Comparing coefficients:    ")
    c1 <- compareAppr2(pomelo$obs_stat, reference$t,
                      pomelo$ID, tol = tol)
    cat(c1)
    cat("\n\n Comparing p-values:        ")
    c2 <- compareAppr2(pomelo$unadj.p, reference$P.Value,
                      pomelo$ID, tol = tol)
    cat(c2)
    cat("\n\n Comparing FDR adjustment:  ")
    c3 <- compareAppr2(pomelo$FDR_indep, reference$adj.P.Val,
                      pomelo$ID, tol = tol)

    ##     c3 <- compareAppr(pomelo$FDR_indep,
    ##                       p.adjust(pomelo$unadj.p, method = "BH"),
    ##                       pomelo$ID)
    cat(c3)
    cat("\n\n")
    if(!(all(c1 == "OK", c2 == "OK", c3 == "OK"))) {
        cat("\n ERROR: At least one test failed. See above.\n")
        return("ERROR: test failed")
    }
}







###########################################

my.topTable <- function(name, coef, comparison, write.out = FALSE) {
  nr <- nrow(name)
  tmp <- topTable(name, coef = coef, adjust.method = "BH", sort.by = "p",
                  number = nr)
  reorder <- order(as.numeric(rownames(tmp)))
  tmp <- tmp[reorder, c(1, 3, 4, 5)]
  
##   if(write.out) {
##     write.table(tmp, file = paste(comparison, "-table.txt", sep = ""), 
##                 col.names = TRUE, row.names = TRUE,
##                 sep = "\t")
##   }
##   nr2 <- nrow(tmp)
##   cat("\n Comparison:\n                  ", comparison, "\n")
##   cat("\n ", nr2, " clones selected\n\n")
  tmp
}

my.topFTable <- function(efit) {
  tmp <- data.frame(ProbeID = rownames(efit$p.value),
                    F = efit$F,
                    P.Value = efit$F.p.value,
                    adj.P.Val = p.adjust(efit$F.p.value, method = "BH"))
  tmp
}
