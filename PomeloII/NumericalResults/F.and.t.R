library(multtest)


MIN_SAMPLE <- 3
MAX_SAMPLE <- 15

MIN_GROUPS <- 2
MAX_GROUPS <- 6

MIN_GENES <- 2
MAX_GENES <- 500

PROP_DIFF_MIN <- .1
PROP_DIFF_MAX <- .30

CHARS_FOR_NAMES <- c(letters, LETTERS, 0:9,
                     c("'", '"', "+", "-", "*", "?",
                       "!", "@", "$", "%", "&", "/",
                       "(", ")", "=", ".", ":", ";",
                       "ñ", "ç", "¡", "¿",
                       "á", "é", "í", "ó", "ú"))

nGenes <- round(runif(1, MIN_GENES, MAX_GENES))
nDiff <- round(runif(1, round(nGenes*PROP_DIFF_MIN),
               round(nGenes*PROP_DIFF_MAX)))

if (testType == "Anova") {
    numGroups <- round(runif(1, MIN_GROUPS, MAX_GROUPS))
    numCl <- round(runif(numGroups, MIN_SAMPLE, MAX_SAMPLE))
} else if (testType == "t") {
    numGroups <- 2
    numCl <- round(runif(2, MIN_SAMPLE, MAX_SAMPLE))
}

## To generate a data set with weird names

dataw <- generateData(numc = c(2, 2), ngenes = 100000, ndiff = 20)
exportData(dataw, 100000, outGene = "expression-weird-names.txt",
           outClass = "class-weird-names.txt")

## ## Buscar una assert function zz
## assert <- function(x) {
## }


## generateData <- function(numc = numCl, 
##                          agediff = runif(1, 0, 0.0001),
##                          meandiff = runif(1, 0, 0.0051),
##                          ngenes = nGenes,
##                          ndiff = nDiff,
##                          cl2diff = runif(1, 0, 0.0001)) {

##     ntot <- sum(numc)
##     genes <- matrix(rnorm(ngenes * ntot),
##                     ncol = ntot)
    
##     covar <- data.frame(Class =
##                         rep(seq(0, numGroups - 1), numc),
##                         Age = rnorm(ntot),
##                         Age2 = rnorm(ntot),
##                         Class2 = sample(c(-1, 0, 1), ntot, replace = TRUE))

##     classDiff <- meandiff * covar$Class
    
##     agediffef <- agediff * covar$Age
##     cl2eff <- cl2diff* covar$Class2
##     otherEffects <- agediffef + cl2eff

##     genes <- t(t(genes) + otherEffects)
##     genes[1:ndiff, ] <- t(t(genes[1:ndiff, ]) + classDiff)

##     genes <- genes[sample(1:ngenes), ]

##     covar$Class2 <- factor(covar$Class2)
##     covar$Class <- factor(covar$Class)
##     return(list(geneExpression = genes, covars = covar))
## }

## doMultest <- function(genes = Data$geneExpression,
##                       class = Data$covar$Class,
##                       testtype = testType) {
    
##     mtTmp <- mt.maxT(genes, class, testtype)
##     toOrder <- mtTmp$index[order(mtTmp$index)]
##     unadjp <- rawp[toOrder]
##     return(list(statistic = teststat[toOrder],
##                 unadjp = unadjp,
##                 adjp = p.adjust(unadjp, method = "BH")))
    
## }


## stretched.out <- function(x, file) {
##     ## Use params for write.table so that most
##     ## files written in the way programs take them:
##     ## a vector
##     write.table(x, file = file,
##                 quote = FALSE, sep = "\t",
##                 eol = "\t",
##                 col.names = FALSE,
##                 row.names = FALSE)
## }


## exportData <- function(Data = Data,
##                        ngenes = nGenes,
##                        out_added_covars = FALSE,
##                        out_surv = FALSE,
##                        outGene  = "./tmp/geneexpr.txt",
##                        outClass = "./tmp/class.txt",
##                        outCovs  = "./tmp/othercovs.txt",
##                        outSurv  = "./tmp/surv.txt",
##                        outEvent = "./tmp/event.txt") {
##     ## Write data as text, so that the web applications
##     ## can use these data

    
##     ## We must ensure no name repetitions
##     gnl <- round(runif(nGenes, 7, 40))
##     namesRepeated <- TRUE
##     while(namesRepeated) {
##         geneNames <-
##             sapply(gnl,
##                    function(x)
##                    paste(sample(CHARS_FOR_NAMES, x, replace = TRUE),
##                          sep = "", collapse = ""))
##         if(length(unique(geneNames)) == nGenes)
##             namesRepeated <- FALSE
## ##        assert(length(unique(geneNames)) <= nGenes)
##     }

##     tmpd <- data.frame(gn = geneNames,
##                        Data$geneExpression)
##     write.table(tmpd, file = outGene, 
##                 quote = FALSE, sep = "\t",
##                 col.names = FALSE,
##                 row.names = FALSE)
##     if(out_surv) {
##         stretched.out(Data$SurvTime, file = outSurv)
##         stretched.out(Data$Event, file = outEvent)
##     } else {
##         stretched.out(Data$Class, file = outClass)
##     }
    
##     if(out_added_covars) {
##         write.table(Data$covars[, -1],
##                     file = outCovs, 
##                     quote = FALSE, sep = "\t",
##                     col.names = FALSE,
##                     row.names = FALSE)
##     }
## }


## Data <- generateData()
## exportData()
## doMultest()

cucu <- doMultest()





#######################################


##  Comparing output




## getNPerms <- function(filename = "./tmp-files/results.txt") {
##     ## This uses too much knowledge of the output format
##     s1 <- system("grep 'Permutations used:' ./tmp-files/results.txt > /tmp/nperms",
##                  intern = TRUE)
##     nPerms <- strsplit(s1, "\t")[3]

## }


## pvToSuccessFailure <- function(p, n) {
##     suc <- round(p * n)
##     return(cbind(suc, n - suc))
## }


## readPomeloOutput <- function(filename = "./tmp-files/results.txt") {
##     pomtmp <- read.table(file = filename, header = TRUE, sep = "\t",
##                          quote = "", skip = 13)
##     return(pomtmp[order(pomtp[, 1]), ])

## }


## comparepV <- function(succ1, fail1, succ2, fail2){
## tmp <- cbind(succ1, fail1, succ2, fail2)
##     return(apply(tmp,  1,
##                  function(x)
##                  fisher.test(rbind(c(x[1], x[2]), c(x[3], x[4])))$p.value))
## }





###########################################
