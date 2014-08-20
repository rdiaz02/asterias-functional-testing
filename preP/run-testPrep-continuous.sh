#!/bin/bash
COUNTER=0
while (true); do
        echo $COUNTER
        OF=testOut.$COUNTER
	##fl-run-test -v --simple-fetch -d --debug-level=2 testpreP.py > $OF
	fl-run-test --stop-on-fail -v --simple-fetch -d --debug-level=2 testpreP.py
        let COUNTER=COUNTER+1
done
