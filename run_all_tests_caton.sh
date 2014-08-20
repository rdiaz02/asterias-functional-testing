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
echo "Testing GeneSrF"
cd ../GeneSrF
fl-run-test  -v --simple-fetch -d --debug-level=2 testGenesrf.py
echo "***********************"
echo "Testing PomeloII"
cd ../PomeloII
fl-run-test  -v --simple-fetch -d --debug-level=2 testPomelo.py
echo "***********************"
echo "Testing PomeloII Numerical"
cd ./NumericalResults
./pomelo-num.py
