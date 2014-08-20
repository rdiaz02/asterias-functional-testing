#!/bin/bash
COUNTER=0
while (true); do
        echo $COUNTER
        OF=testOut.$COUNTER
        ./run_all_tests.sh > $OF
        let COUNTER=COUNTER+1
done
