## Limma's examples in the help rely on randomly generated data.
## We'll do the same here.
## Note that we do not scale values here. This leads to small numerical
## diffs, but serves as furhter testing.


### This adds two tests with categorical covariates


library(limma)
source("../pomelo_testing_util.R")


## d) Anova with covars; 8.7 in limma manual
## Two sets of random covars
set.seed(1)
covs.breast2 <- matrix(sample(LETTERS[1:4], 95 *4, replace = TRUE), ncol = 4)
covs.breast2 <- data.frame(covs.breast2)
colnames(covs.breast2) <- paste("V", 1:4, sep = "")


set.seed(2)
covs.breast3 <- data.frame(matrix(sample(LETTERS[1:6], 95 *2, replace = TRUE), ncol = 2),
                           matrix(sample(letters[11:13], 95 *1, replace = TRUE), ncol = 1),
                           matrix(rnorm(95 * 1), ncol = 1))

colnames(covs.breast3) <- paste("V", 1:4, sep = "")
write.table(file = "covs.breast2.txt", covs.breast2, col.names = TRUE,
            row.names = FALSE, sep = "\t", quote = FALSE)
write.table(file = "covs.breast3.txt", covs.breast3, col.names = TRUE,
            row.names = FALSE, sep = "\t", quote = FALSE)


### read data
dataRead("breast.3.class")
breast.3.class.class <- factor(breast.3.class.class)

## Scaled covars: same as below, but this will be better behaved, numerically

design2 <- model.matrix( ~ . -1, cbind(breast.3.class.class, covs.breast2))
colnames(design2)[1:3] <- c("a", "b", "c")

cont.matrixII <- makeContrasts(a-b, a-c, b-c, levels = design2)
fitII <- lmFit(breast.3.class.covar, design2)
fitII2 <- contrasts.fit(fitII, cont.matrixII)
fitII2 <- eBayes(fitII2)

F.breast.cov2 <- my.topFTable(fitII2)
t1.covs.breast2 <- my.topTable(fitII2, 1)
t2.covs.breast2 <- my.topTable(fitII2, 2)
t3.covs.breast2 <- my.topTable(fitII2, 3)




design3 <- model.matrix(~ . -1, cbind(breast.3.class.class,
                                      covs.breast3[, 1:3],
                                      scale(covs.breast3[, 4, drop = FALSE])))

colnames(design3)[1:3] <- c("a", "b", "c")
cont.matrixIII <- makeContrasts(a-b, a-c, b-c, levels = design3)
fitIII <- lmFit(breast.3.class.covar, design3)
fitIII2 <- contrasts.fit(fitIII, cont.matrixIII)
fitIII2 <- eBayes(fitIII2)

F.breast.cov3 <- my.topFTable(fitIII2)
t1.covs.breast3 <- my.topTable(fitIII2, 1)
t2.covs.breast3 <- my.topTable(fitIII2, 2)
t3.covs.breast3 <- my.topTable(fitIII2, 3)




### save(F.breast.cov, t1.breast.cov, t2.breast.cov, t3.breast.cov,
###      F.breast, t1.breast, t2.breast, t3.breast,
###      leukemia.t_limma, leukemia.paired.t_limma_paired,
###      file = "Limma.verified.RData")



### We've got to change the names to the t1, t2, t3, etc in original


load("Limma.verified.RData.before.2009.01.20")

t1.covs.breast <- t1.breast.cov
t2.covs.breast <- t2.breast.cov
t3.covs.breast <- t3.breast.cov

save(F.breast.cov, F.breast.cov2, F.breast.cov3,
     t1.covs.breast, t2.covs.breast, t3.covs.breast,
     t1.covs.breast2, t2.covs.breast2, t3.covs.breast2,
     t1.covs.breast3, t2.covs.breast3, t3.covs.breast3,
     F.breast, t1.breast, t2.breast, t3.breast,
     leukemia.t_limma, leukemia.paired.t_limma_paired,
     file = "Limma.verified.RData")







     

### ###### Other parameterizations

### design <- model.matrix(~ 0 + covs.breast + breast.3.class.class)
### colnames(design)[5:7] <- c("a", "b", "c")
### cont.matrix <- makeContrasts(a-b, a-c, b-c, levels = design)
### fit <- lmFit(breast.3.class.covar, design)
### fit2 <- contrasts.fit(fit, cont.matrix)
### fit2 <- eBayes(fit2)

### F.breast.cov <- my.topFTable(fit2)
### t1.breast.cov <- my.topTable(fit2, 1)
### t2.breast.cov <- my.topTable(fit2, 2)
### t3.breast.cov <- my.topTable(fit2, 3)

### ### Another parameterization: with intercept
### design <- model.matrix(~ covs.breast + breast.3.class.class)
### colnames(design)[6:7] <- c("b", "c")
### colnames(design)[1] <- c("Intercept")
### fit <- lmFit(breast.3.class.covar, design)
### fit2 <- eBayes(fit)
### FI.breast.cov <- my.topFTable(fit2)   ## Of course, this is NOT like the above
### tb.breast.cov <- my.topTable(fit2, 6) ## Like t1.breast.cov
### tc.breast.cov <- my.topTable(fit2, 7) ## Like t2.breast.cov



