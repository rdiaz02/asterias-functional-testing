#!/usr/bin/python2.4

"""Script for automated (hourly, daily, whatever) testing of minimal
Pomelo II functionality. Verifies cgi and MPI.
You can set up a chron job so that this is script is run, say, every hour."""


## Next are to be substituted by installation script

EMAIL_LOGIN    = "" 
EMAIL_PASSWORD = ""
EMAIL_RECEIVERS = ('', '')



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
fi, fo = \
    os.popen4('fl-run-test -q --no-color testPomelo.py Pomelo.test_regression')
time.sleep(280) ## should be plenty
foout = fo.readlines()
if foout[3] != 'OK\n':
    # if something happens, send email
    for receiver in EMAIL_RECEIVERS:
        send_from_gmail(receiver,
                        '[CjLUSTER] Automatic pomelo test failed',
                        '[CLUSTER] Automatic pomelo test failed')
   
