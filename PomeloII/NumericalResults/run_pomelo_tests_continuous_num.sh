#!/bin/bash
COUNTER=0
while (true); do
        echo $COUNTER
        OF=testNumOut.$COUNTER
        ./pomelo-num.py > $OF
        let COUNTER=COUNTER+1
done
