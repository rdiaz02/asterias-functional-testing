# -*- coding: iso-8859-15 -*-
""" ADaCGH testing: user interface and numerical results.
"""

import time
import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase
from webunit.utility import Upload
from urllib import urlretrieve

auto_refresh_string = 'This is an autorefreshing page'
MAX_running_time = 3600 * 1 

def common_part(self, final_output,                
                MAX_running_time = 3600,
                auto_refresh_string = auto_refresh_string):
    """ Common to all tests: take care of autorefreshing and following
    links till done. Then, verify expected string in output."""
  
    server_url = self.server_url
    start_run = time.time()
    refresh_num = 0
    
    while True:
        final_body = self.getBody()
        if final_body.find(auto_refresh_string) < 0:
            break
        time.sleep(32)
        refresh_num += 1
        run_time = time.time() - start_run
        print '\n Refreshed ' + str(refresh_num) + ' times. Been running for ' + str(round(run_time/60.0, 2)) + ' minutes.\n'
        if run_time > MAX_running_time :
            self.fail('Run longer than MAX_running_time')
        self.get(server_url + self.getLastUrl(),
                 description="Get /cgi-bin/checkdone.cgi")
    print self.getLastUrl()	
    expected = final_body.find(final_output) >= 0
    if not expected:
        self.fail('\n ***** (begin of) Unexpected final result!!!! *****\n' + \
                 str(final_body) + \
                 '\n ***** (end of) Unexpected final result!!!! *****\n')
    else:
        print 'OK'



  
class ADaCGH(FunkLoadTestCase):
    """
    This test use a configuration file Adacgh.conf
    (though it ain't really needed).
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = 'http://adacgh2.bioinfo.cnio.es'
        ##self.server_url = self.conf_get('main', 'url')


    def testCBS_paral(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("two.sample.shuffled.num.test")],
            ['centering', 'None'],
            ['methodaCGH', 'DNAcopy'],
            ['Wave.minDiff', '0.25'],
            ['Wave.merge', 'Yes'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="CBS; numerical of parallel")
        final_output = 'Segmented data plots'
        common_part(self, final_output)
        url_before_get = self.getLastUrl()
        urlretrieve(server_url +
                    url_before_get.replace('results.html', 'CBS.output.txt'),
                    filename = 'CBS.web.output.txt')
        import rpy ## to verify numerical output
        print '##########  @@@@@@@@@@@@@@   Testing   CBS'
        tmp = rpy.r('source("test-num.R")')
        tmp = rpy.r('test.cbs()')
        print tmp
#          if tmp == 'OK':
#              print 'OK'
#          else:
#              self.fail('testCBS_paral failed')

    def testHMM_paral(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("two.sample.shuffled.num.test")],
            ['centering', 'None'],
            ['methodaCGH', 'HMM'],
            ['Wave.minDiff', '0.25'],
            ['Wave.merge', 'Yes'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="CBS; numerical of parallel")
        final_output = 'Segmented data plots'
        common_part(self, final_output)
        url_before_get = self.getLastUrl()
        urlretrieve(server_url +
                    url_before_get.replace('results.html', 'HMM.output.txt'),
                    filename = 'HMM.web.output.txt')
        import rpy ## to verify numerical output
        print '##########  @@@@@@@@@@@@@@   Testing   HMM'
        tmp = rpy.r('source("test-num.R")')
        tmp = rpy.r('test.hmm()')
        print tmp


    def testBioHMM_paral(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("two.sample.shuffled.num.test")],
            ['centering', 'None'],
            ['methodaCGH', 'BioHMM'],
            ['Wave.minDiff', '0.25'],
            ['Wave.merge', 'Yes'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="BioHMM; numerical of parallel")
        final_output = 'Segmented data plots'
        common_part(self, final_output)
        url_before_get = self.getLastUrl()
        urlretrieve(server_url +
                    url_before_get.replace('results.html', 'BioHMM.output.txt'),
                    filename = 'BioHMM.web.output.txt')
        import rpy ## to verify numerical output
        print '##########  @@@@@@@@@@@@@@   Testing   BioHMM'
        tmp = rpy.r('source("test-num.R")')
        tmp = rpy.r('test.biohmm()')
        print tmp

    def testGLAD_paral(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("two.sample.shuffled.num.test")],
            ['centering', 'None'],
            ['methodaCGH', 'GLAD'],
            ['Wave.minDiff', '0.25'],
            ['Wave.merge', 'Yes'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="GLAD; numerical of parallel")
        final_output = 'Segmented data plots'
        common_part(self, final_output)
        url_before_get = self.getLastUrl()
        urlretrieve(server_url +
                    url_before_get.replace('results.html', 'GLAD.output.txt'),
                    filename = 'GLAD.web.output.txt')
        import rpy ## to verify numerical output
        print '##########  @@@@@@@@@@@@@@   Testing   GLAD'
        tmp = rpy.r('source("test-num.R")')
        tmp = rpy.r('test.glad()')
        print tmp


    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")

if __name__ in ('main', '__main__'):
     unittest.main()
