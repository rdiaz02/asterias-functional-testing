## To perform survival analyses with R, and verify Pomelo results.


####  Copyright (C)  2006, Ramón Díaz-Uriarte, Edward R. Morrissey

#### This program is free software; you can redistribute it and/or
#### modify it under the terms of the Affero General Public License
#### as published by the Affero Project, version 1
#### of the License.

#### This program is distributed in the hope that it will be useful,
#### but WITHOUT ANY WARRANTY; without even the implied warranty of
#### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#### Affero General Public License for more details.

#### You should have received a copy of the Affero General Public License
#### along with this program; if not, you can download if
#### from the Affero Project at http://www.affero.org/oagpl.html

rm(list = ls())

#####  Data: download from
## http://signs.bioinfo.cnio.es/Examples/example.data.sets.SignS.tar.gz


## Read data into R
aml.covar <- read.table("aml.covar.txt", header = FALSE, sep = "\t",
                        row.names = 1)
dlbcl.covar <- read.table("dlbcl.160.covar.txt", header = FALSE, sep = "\t",
                          row.names = 1)
breast.covar <- read.table("breast.covar.txt", header = FALSE, sep = "\t",
                           row.names = 1)
aml.event <- scan("aml.event.txt")
aml.surv <- scan("aml.surv.txt")
dlbcl.event <- scan("dlbcl.160.event.txt")
dlbcl.surv <- scan("dlbcl.160.surv.txt")
breast.event <- scan("breast.event.txt")
breast.surv <- scan("breast.surv.txt")


library(survival)

coxF <- function(x, surv, status, iter.max = 200, ...) {
    tmp <- coxph(Surv(surv, status) ~ x,
                 method = "efron",
                 control = coxph.control(iter.max = iter.max))
        return(c(tmp$coef, summary(tmp)$waldtest[[3]]))
}

aml.results <- t(apply(aml.covar, 1, function(x) coxF(x, aml.surv, aml.event)))
dlbcl.results <- t(apply(dlbcl.covar, 1, function(x) coxF(x, dlbcl.surv, dlbcl.event)))
breast.results <- t(apply(breast.covar, 1, function(x) coxF(x, breast.surv, breast.event)))

colnames(aml.results) <- colnames(dlbcl.results) <-
    colnames(breast.results) <- c("coefficient", "pvalue")

breast.results <- data.frame(breast.results)
dlbcl.results <- data.frame(dlbcl.results)
aml.results <- data.frame(aml.results)

save(file = "cox.verified.RData",
     aml.results, dlbcl.results, breast.results)


## For controling differences between versions
version
packageDescription("survival")
