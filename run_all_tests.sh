#!/bin/bash
echo "***********************"
echo "Testing preP"
cd ./preP/
fl-run-test  -v --simple-fetch -d --debug-level=2 testpreP.py
echo "***********************"
echo "Testing Tnasas"
cd ../Tnasas
fl-run-test  -v --simple-fetch -d --debug-level=2 testTnasas.py
echo "***********************"
echo "Testing ADaCGH"
cd ../ADaCGH2
fl-run-test  -v --simple-fetch -d --debug-level=2 testAdacgh.py
echo "***********************"
echo "GeneSrF"
cd ../GeneSrF
fl-run-test  -v --simple-fetch -d --debug-level=2 testGenesrf2.py
echo "***********************"
echo "Testing SignS"
cd ../SignS
fl-run-test  -v --simple-fetch -d --debug-level=2 testSigns2.py
echo "***********************"
echo "Testing PomeloII"
cd ../PomeloII
fl-run-test  -v --simple-fetch -d --debug-level=2 testPomelo.py
echo "***********************"
echo "Testing PaLS"
cd ../PaLS
fl-run-test  -v --simple-fetch -d --debug-level=2 testPaLS.py

