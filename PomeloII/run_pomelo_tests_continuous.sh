#!/bin/bash
COUNTER=0
while (true); do
        echo $COUNTER
        OF=testOut.$COUNTER
        fl-run-test -v --simple-fetch -d --debug-level=2 testPomelo.py > $OF
        let COUNTER=COUNTER+1
done
