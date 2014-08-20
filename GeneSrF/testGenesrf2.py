# -*- coding: iso-8859-15 -*-
"""basic_navigation FunkLoad test

$Id: $
"""
import time
import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase
from webunit.utility import Upload


auto_refresh_string = 'This is an autorefreshing page'
MAX_running_time = 3600 * 1 


### NEW: A bunch of ugly kludges so that we try twice before reporting a failure.
### For some reason, I was getting 404s in simple things, from loading
### the basic page to getting the results.


def mypost(self, theurl, theparams, thedescription):
    try:
        print '\nAt post 1\n'
        self.post(theurl, params = theparams, description= thedescription)
    except:
        print '\nAt post 1 - except\n'
        time.sleep(2)
        self.post(theurl, params = theparams, description = thedescription)


def common_part(self, final_output,                
                MAX_running_time = 3600,
                auto_refresh_string = auto_refresh_string):    
    server_url = self.server_url
    start_run = time.time()
    refresh_num = 0

    while True:
        try:
            print '\n At 01 \n'
            final_body = self.getBody()
        except:
            time.sleep(5)
            print '\n At 01 -except \n'
            final_body = self.getBody()

        print '\n At 001 \n'
        if final_body.find(auto_refresh_string) < 0:
##            print '\n This is final_body \n'
##            print str(final_body)
            break
        time.sleep(13)
        refresh_num += 1
        run_time = time.time() - start_run
        print '\n Refreshed ' + str(refresh_num) + ' times. Been running for ' + str(round(run_time/60.0, 2)) + ' minutes.\n'
        print '\n At 02 \n'

        if run_time > MAX_running_time :
            self.fail('Run longer than MAX_running_time')
        checkdoneUrl = server_url + self.getLastUrl()
        print '\n checkdoneUrl = '
        print checkdoneUrl

        try:
            print '\n At 03 \n'
            gg = self.get(checkdoneUrl,
                          description="Get /cgi-bin/checkdone.cgi")
            print '\n This is gg \n'
            print str(gg)
## why does this happen?? 
        except:
            time.sleep(5)
            print '\n At 03 - except \n'
            gg = self.get(checkdoneUrl,
                          description="Get /cgi-bin/checkdone.cgi")
            print '\n This is gg \n'
            print str(gg)

              
##    print self.getLastUrl()
    expected = final_body.find(final_output) >= 0
    if not expected:
        print 'FAILURE!!! FAILURE!!!'
        self.fail('\n ***** (begin of) Unexpected final result!!!! *****\n' + \
                 str(final_body) + \
                 '\n ***** (end of) Unexpected final result!!!! *****\n')
    else:
        print 'OK'


    
#     while True:
#         print '\nGot to 0\n'
#         ## this is a mess, but I try twice
#         try:
#             print '\nGot to 00\n'
# ##            final_body = self.getBody()
#             final_body = self.getLastUrl()
#         except:
#             print '\nGot to 00 - except\n'
#             time.sleep(4)
# ##            final_body = self.getBody()
#             final_body = self.get(server_url + self.getLastUrl())
#         print '\nGot to 1\n'
#         if final_body.find(auto_refresh_string) < 0:
#             ## time.sleep(43) ## try to avoid false error reports
#             print '\nGot to break\n'
#             print '\n printing final body \n'
#             print str(final_body)
#             break

#         time.sleep(12)
#         refresh_num += 1
#         run_time = time.time() - start_run
#         print '\nGot to 2\n'
#         print '\n Refreshed ' + str(refresh_num) + ' times. Been running for ' + str(round(run_time/60.0, 2)) + ' minutes.\n'
#         if run_time > MAX_running_time :
#             self.fail('Run longer than MAX_running_time')
#         try:
#             gg = self.get(server_url + self.getLastUrl(),
#                      description="Get /cgi-bin/checkdone.cgi")
#             print '\nGot to 3\n'
#             print ' ~~~~~~~~~~~~~~~~~ Printing some stuff ~~~~~~~~~~~~~~'
#             print str(gg)
#         except:
#             time.sleep(4)
#             gg = self.get(server_url + self.getLastUrl(),
#                      description="Get /cgi-bin/checkdone.cgi")
#             print '\nGot to 3 - except\n'
#             print ' ~~~~~~~~~~~~~~~~~ Printing some stuff ~~~~~~~~~~~~~~'
#             print str(gg)


#         try:
#             gg = self.get(server_url + self.getLastUrl(),
#                      description="Get /cgi-bin/checkdone.cgi")
#             print '\nGot to 3 B\n'
#             print ' ~~~~~~~~~~~~~~~~ Printing some stuff ~~~~~~~~~~~~~~'
#             print str(gg)
#         except:
#             time.sleep(4)
#             gg = self.get(server_url + self.getLastUrl(),
#                      description="Get /cgi-bin/checkdone.cgi")
#             print '\nGot to 3 B - except\n'
#             print ' ~~~~~~~~~~~~~~~~ Printing some stuff ~~~~~~~~~~~~~~'
#             print str(gg)
#         print '\nGot to 4\n'
#     expected = final_body.find(final_output) >= 0
#     if not expected:
#         print 'FAILURE!!! FAILURE!!!'
#         self.fail('\n ***** (begin of) Unexpected final result!!!! *****\n' + \
#                  str(final_body) + \
#                  '\n ***** (end of) Unexpected final result!!!! *****\n')
#     else:
#         print 'OK'


    
class GeneSrF(FunkLoadTestCase):
    """XXX

    This test use a configuration file Genesrf.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = 'http://genesrf.bioinfo.cnio.es'
        ##self.server_url = self.conf_get('main', 'url')

    def test1(self):
        server_url = self.server_url

        try:
            self.get(server_url + "/",
                     description="Get /")
        except:
            print '\n self.get except\n'
            time.sleep(5)
            self.get(server_url + "/",
                     description="Get /")


        # self.post(server_url + "/cgi-bin/genesrfR.cgi", params=[
        #     ['covariate', Upload("xdata2.txt")],
        #     ['class', Upload("Class")],
        #     ['organism', 'None'],
        #     ['idtype', 'None']],
        #     description="simple test")

        mypost(self, theurl = server_url + "/cgi-bin/genesrfR.cgi", theparams=[
            ['covariate', Upload("xdata2.txt")],
            ['class', Upload("Class")],
            ['organism', 'None'],
            ['idtype', 'None']],
            thedescription="simple test")


        final_output = '<h3>Variable selection using all data </h3><h4>Variables used</h4>'
        common_part(self, final_output)



    def test2(self):
        server_url = self.server_url

        # self.get(server_url + "/",
        #     description="Get /")
        try:
            self.get(server_url + "/",
                     description="Get /")
        except:
            print '\n self.get except\n'
            time.sleep(5)
            self.get(server_url + "/",
                     description="Get /")



        mypost(self, server_url + "/cgi-bin/genesrfR.cgi", theparams=[
            ['covariate', Upload("./with.mm.names/short.covar2.txt")],
            ['class', Upload("./with.mm.names/class")],
            ['organism', 'Mm'],
            ['idtype', 'ug']],
            thedescription="test with organism and idtype and pals")

        final_output = '<h3>Variable selection using all data </h3><h4>Variables used</h4>'
        common_part(self, final_output)


    def test3(self):
        server_url = self.server_url

        # self.get(server_url + "/",
        #     description="Get /")

        try:
            self.get(server_url + "/",
                     description="Get /")
        except:
            print '\n self.get except\n'
            time.sleep(5)
            self.get(server_url + "/",
                     description="Get /")


        mypost(self, server_url + "/cgi-bin/genesrfR.cgi", theparams=[
            ['covariate', Upload("./srbct.data.txt")],
            ['class', Upload("./srbct.class.txt")],
            ['organism', 'Mm'],
            ['idtype', 'ug']],
            thedescription="four class set --check figures")

        final_output = '<h3>Variable selection using all data </h3><h4>Variables used</h4>'
        common_part(self, final_output)



    def test4(self):
        server_url = self.server_url

        # self.get(server_url + "/",
        #     description="Get /")

        try:
            self.get(server_url + "/",
                     description="Get /")
        except:
            print '\n self.get except\n'
            time.sleep(5)
            self.get(server_url + "/",
                     description="Get /")


        mypost(self, server_url + "/cgi-bin/genesrfR.cgi", theparams=[
            ['covariate', Upload("./srbct.data.txt")],
            ['class', Upload("./srbct.class.letra.txt")],
            ['organism', 'Mm'],
            ['idtype', 'ug']],
            thedescription="four class set with non-num class --check figures")

        final_output = '<h3>Variable selection using all data </h3><h4>Variables used</h4>'
        common_part(self, final_output)


    def test5(self):
        server_url = self.server_url

        # self.get(server_url + "/",
        #     description="Get /")
        try:
            self.get(server_url + "/",
                     description="Get /")
        except:
            print '\n self.get except\n'
            time.sleep(5)
            self.get(server_url + "/",
                     description="Get /")


        mypost(self, server_url + "/cgi-bin/genesrfR.cgi", theparams=[
            ['covariate', Upload("./colon.data.txt")],
            ['class', Upload("./colon.class.txt")],
            ['organism', 'Mm'],
            ['idtype', 'ug']],
            thedescription="two class set with non-num class --check figures")

        final_output = '<h3>Variable selection using all data </h3><h4>Variables used</h4>'
        common_part(self, final_output)


    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")

if __name__ in ('main', '__main__'):
     unittest.main()
