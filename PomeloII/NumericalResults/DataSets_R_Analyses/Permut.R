## Obtain reference results for testing Pomelo II.

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

library(multtest)
source("../pomelo_testing_util.R")



## t
dataRead("leukemia")
dataRead("colon")
## need numeric vector for multtest
leukemia.class <-
    2 - as.numeric(factor(scan("leukemia.class.txt", what = "")))
colon.class <-
    2 - as.numeric(factor(scan("colon.class.txt", what = "")))


## Anova
dataRead("breast.3.class")
dataRead("brain")
dataRead("srbct")

## Regression
aml.covar <- read.table("aml.covar.txt", header = FALSE, sep = "\t",
                        row.names = 1)
dlbcl.covar <- read.table("dlbcl.160.covar.txt", header = FALSE, sep = "\t",
                          row.names = 1)
aml.surv <- scan("aml.surv.txt")
dlbcl.surv <- scan("dlbcl.160.surv.txt")


### Run multtest et al.
leukemia.t <- doMultest(genes = leukemia.covar,
                        class = leukemia.class,
                        "t")
colon.t <- doMultest(genes = colon.covar,
                     class = colon.class,
                     "t")
breast.anova <- doMultest(genes = breast.3.class.covar,
                          class = as.numeric(as.character(breast.3.class.class)),
                          "f")
brain.anova <- doMultest(genes = brain.covar,
                         class = as.numeric(as.character(brain.class)),
                         "f")
srbct.anova <- doMultest(genes = srbct.covar,
                         class = as.numeric(as.character(srbct.class)),
                         "f")
aml.small.covar <- aml.covar[1:200, ]
aml.small.regres <- doMultest(genes = aml.small.covar,
                         class = aml.surv,
                         "Regres", B = 1000)
## Not surprisingly, the above is painfully slow!


## dlbcl.regres <- doMultest(genes = dlbcl.covar,
##                            class = dlbcl.surv,
##                            "Regres")


breast.3.class.Anova <- breast.anova
brain.Anova <- brain.anova
srbct.Anova <- srbct.anova
aml.small.Regres <- aml.small.regres
save(leukemia.t, colon.t, breast.3.class.Anova, brain.Anova, srbct.Anova,
     aml.small.Regres, file = "permutations.verified.RData")
##, dlbcl.regres)
