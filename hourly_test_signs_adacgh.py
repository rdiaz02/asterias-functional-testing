#!/usr/bin/python2.6

"""Script for automated (hourly, daily, whatever) testing of minimal
functionality of SignS and ADaCGH. Verifies cgi and MPI.
You can set up a chron job so that this is script is run, say, every hour.
This is what we do."""


## Next are to be substituted by installation script

EMAIL_LOGIN    = "somethig"
EMAIL_PASSWORD = "something"
EMAIL_RECEIVERS = ('someone',)


import os
import time
import glob
import sys
## Next are for email sending
from smtplib import *
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def send_from_gmail(email, body, subject):
    ''' Send email from gmail.'''
    server = SMTP('smtp.gmail.com', 587)
## server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(EMAIL_LOGIN, EMAIL_PASSWORD)
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = subject
    outer['To'] = email
    outer['From'] = EMAIL_LOGIN
    outer.preamble = '\n'
    # To guarantee the message ends with a newline
    outer.epilogue =''
    # Note: we should handle calculating the charset
    msg = MIMEText(body)
    # Message body
    outer.attach(msg)
    text = outer.as_string()
    server.sendmail(outer['From'], outer['To'], text)
    # SSL error because of bad comunication closing
    try:
        server.quit()
    except:
        pass


## run the script from the directory where testPomelo.py lives

def adacgh_test(testname):
    os.chdir('/home/ramon/bzr-local-repos/Testing/ADaCGH2')
    fi, fo = \
        os.popen4('fl-run-test -q --no-color --simple-fetch testAdacgh.py ADaCGH.' + testname)
    time.sleep(400) ## should be plenty
    foout = fo.readlines()
    print foout
    if foout[3] != 'OK\n':
        print '      It seems test failed!!!'
        # if something happens, send email
        for receiver in EMAIL_RECEIVERS:
            send_from_gmail(receiver,
                            '[CLUSTER] Automatic ADaCGH test failed: ' + testname,
                            '[CLUSTER] Automatic ADaCGH test failed: ' + testname)
   

def signs_test(testname):
    os.chdir('/home/ramon/bzr-local-repos/Testing/SignS')
    fi, fo = \
        os.popen4('fl-run-test -q --no-color --simple-fetch testSigns2.py Signs.' + testname)
    time.sleep(400) ## should be plenty
    foout = fo.readlines()
    print foout
    if foout[3] != 'OK\n':
        # if something happens, send email
        for receiver in EMAIL_RECEIVERS:
            send_from_gmail(receiver,
                            '[CLUSTER] Automatic SignS test failed',
                            '[CLUSTER] Automatic SignS test failed')


def genesrf_test(testname):
    os.chdir('/home/ramon/bzr-local-repos/Testing/GeneSrF')
    fi, fo = \
        os.popen4('fl-run-test -q --no-color --simple-fetch testGenesrf2.py GeneSrF.' + testname)
    time.sleep(400) ## should be plenty
    foout = fo.readlines()
    print foout
    if foout[3] != 'OK\n':
        # if something happens, send email
        for receiver in EMAIL_RECEIVERS:
            send_from_gmail(receiver,
                            '[CLUSTER] Automatic GeneSrF test failed: ' + testname,
                            '[CLUSTER] Automatic GeneSrF test failed: ' + testname)

def tnasas_test(testname):
    os.chdir('/home/ramon/bzr-local-repos/Testing/Tnasas')
    fi, fo = \
        os.popen4('fl-run-test -q --no-color --simple-fetch testTnasas.py Tnasas.' + testname)
    time.sleep(400) ## should be plenty
    foout = fo.readlines()
    print foout
    if foout[3] != 'OK\n':
        # if something happens, send email
        for receiver in EMAIL_RECEIVERS:
            send_from_gmail(receiver,
                            '[CLUSTER] Automatic Tnasas test failed: ' + testname,
                            '[CLUSTER] Automatic Tnasas test failed: ' + testname)




os.system('touch starting_hourly_signs_adacgh_test')

### For now, just a few test; not all are needed.
### uncomment the other when comprehensive testing is needed.

adacgh_test('test1')
### # adacgh_test('testGLAD')
#### adacgh_test('testCGHseg')
#### adacgh_test('testHMM')
#### adacgh_test('testBioHMM')

signs_test('test_division_by_zero')

genesrf_test('test1')
### # genesrf_test('test2')

tnasas_test('test1_Named')



os.chdir('/home/ramon/bzr-local-repos/Testing')
os.system('touch ending_hourly_signs_adacgh_test')
os.system('rm /home/ramon/bzr-local-repos/Testing/ADaCGH2/*.xml.*')
os.system('rm /home/ramon/bzr-local-repos/Testing/GeneSrF/*.xml.*')
os.system('rm /home/ramon/bzr-local-repos/Testing/SignS/*.xml.*')
os.system('rm /home/ramon/bzr-local-repos/Testing/Tnasas/*.xml.*')

