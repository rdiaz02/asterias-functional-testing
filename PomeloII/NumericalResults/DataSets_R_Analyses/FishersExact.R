## To perform fisher's exact test analyses with R, and verify Pomelo results.


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



## Read data into R
fisher.data <- read.table("data.fisher.txt", header = FALSE, sep = "\t",
                        row.names = 1)
fisher.labels <- scan("labels.fisher.names.txt", what = "")

#### Fishers
test.stat.fisher <- function(x, y) {
    return(fisher.test(table(x, y))$p.value)
}

fisher.pv <- apply(fisher.data, 1, function(z) test.stat.fisher(z, fisher.labels))

## ver testing-multest.R


save(file = "fisher.verified.RData",
     fisher.pv)

