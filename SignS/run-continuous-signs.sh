#!/bin/bash
COUNTER=0
while (true); do
        echo $COUNTER
        OF=SignS.testOut.E.$COUNTER
        fl-run-test  -v --simple-fetch -d --debug-level=2 testSigns2.py > $OF
        let COUNTER=COUNTER+1
done
