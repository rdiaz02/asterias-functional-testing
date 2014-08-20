## Limma's examples in the help rely on randomly generated data.
## We'll do the same here.
## Note that we do not scale values here. This leads to small numerical
## diffs, but serves as furhter testing.

library(limma)
source("../pomelo_testing_util.R")


## We will test:

# a) t-test
# b) paired-t test
# c) plain anova (3 class comparison)
# d) a factorial model

## We will follow examples in limma's manual
## If possible, we use real data to which we add covars to
## simulate effects other effects

####   a) t-test; see, 8.4 and 8.5 in limma guide
dataRead("leukemia")
leukemia.class <- factor(leukemia.class)
design <- model.matrix(~ 0 + leukemia.class)
colnames(design) <- c("ALL", "AML")
cont.matrix <- makeContrasts(AMLvsALL=AML-ALL, levels = design)
fit <- lmFit(leukemia.covar, design)
fit2 <- contrasts.fit(fit, cont.matrix)
fit2 <- eBayes(fit2)
leukemia.t_limma <- my.topTable(fit2, 1)
## returns 

##      ProbeID                    t                P.Value              adj.P.Val
## 829     G829 -10.7733641409271268 1.2307261836976967e-13 3.7549455864616725e-10



####   b) paired t-test; see, 8.3 in limma guide

## paired leukemia constructed by deleting the first 16 columns
## awk 'OFS="\t" {print $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30, $31, $32, $33, $34, $35, $36, $37, $38}' leukemia.class.txt > leukemia-paired.class.txt
# awk 'OFS="\t" {print $1, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30, $31, $32, $33, $34, $35, $36, $37, $38, $39}' leukemia.data.txt > leukemia-paired.data.txt

leukemia.covar.paired <- leukemia.covar[, -c(1:16)]
leukemia.class.paired <- leukemia.class[ -c(1:16)]
leukemia.pairs <- rep((1:11), 2)

SibShip <- factor(leukemia.pairs)
Treat <- factor(leukemia.class.paired)
design <- model.matrix(~ SibShip + Treat)
fit <- lmFit(leukemia.covar.paired, design)
fit <- eBayes(fit)
leukemia.t_limma_paired <- my.topTable(fit, 12)
leukemia.paired.t_limma_paired <- leukemia.t_limma_paired

## c) Anova, 3 class; 8.6 in limma

dataRead("breast.3.class")
breast.3.class.class <- factor(breast.3.class.class)
design <- model.matrix(~ 0 + breast.3.class.class)
colnames(design) <- c("a", "b", "c")
cont.matrix <- makeContrasts(a-b, a-c, b-c, levels = design)
fit <- lmFit(breast.3.class.covar, design)
fit2 <- contrasts.fit(fit, cont.matrix)
fit2 <- eBayes(fit2)

F.breast <- my.topFTable(fit2)
t1.breast <- my.topTable(fit2, 1)
t2.breast <- my.topTable(fit2, 2)
t3.breast <- my.topTable(fit2, 3)



## d) Anova with covars; 8.7 in limma manual
## A set of random covars
set.seed(1)
covs.breast <- matrix(rnorm(95 *4), ncol = 4)
covs.breast[, 1] <- 100 * covs.breast[, 1] + 10
colnames(covs.breast) <- paste("V", 1:4, sep = "")
write.table(file = "covs.breast.txt", covs.breast, col.names = TRUE,
            row.names = FALSE, sep = "\t")
## zz: recall to edit manually and add a "#"!!!!!!!

## Scaled covars: same as below, but this will be better behaved, numerically
design <- model.matrix(~ 0 + scale(covs.breast) + breast.3.class.class)
colnames(design) <- c(paste("v", 1:4, sep = ""), "a", "b", "c")
cont.matrix <- makeContrasts(a-b, a-c, b-c, levels = design)
fit <- lmFit(breast.3.class.covar, design)
fit2 <- contrasts.fit(fit, cont.matrix)
fit2 <- eBayes(fit2)

F.breast.cov <- my.topFTable(fit2)
t1.breast.cov <- my.topTable(fit2, 1)
t2.breast.cov <- my.topTable(fit2, 2)
t3.breast.cov <- my.topTable(fit2, 3)

leukemia.paired.t_limma_paired <- leukemia.t_limma_paired
save(F.breast.cov, t1.breast.cov, t2.breast.cov, t3.breast.cov,
     F.breast, t1.breast, t2.breast, t3.breast,
     leukemia.t_limma, leukemia.paired.t_limma_paired,
     file = "Limma.verified.RData")






     

###### Other parameterizations

design <- model.matrix(~ 0 + covs.breast + breast.3.class.class)
colnames(design)[5:7] <- c("a", "b", "c")
cont.matrix <- makeContrasts(a-b, a-c, b-c, levels = design)
fit <- lmFit(breast.3.class.covar, design)
fit2 <- contrasts.fit(fit, cont.matrix)
fit2 <- eBayes(fit2)

F.breast.cov <- my.topFTable(fit2)
t1.breast.cov <- my.topTable(fit2, 1)
t2.breast.cov <- my.topTable(fit2, 2)
t3.breast.cov <- my.topTable(fit2, 3)

### Another parameterization: with intercept
design <- model.matrix(~ covs.breast + breast.3.class.class)
colnames(design)[6:7] <- c("b", "c")
colnames(design)[1] <- c("Intercept")
fit <- lmFit(breast.3.class.covar, design)
fit2 <- eBayes(fit)
FI.breast.cov <- my.topFTable(fit2)   ## Of course, this is NOT like the above
tb.breast.cov <- my.topTable(fit2, 6) ## Like t1.breast.cov
tc.breast.cov <- my.topTable(fit2, 7) ## Like t2.breast.cov



