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



def common_part(self, final_output,                
                MAX_running_time = 3600,
                auto_refresh_string = auto_refresh_string):    
    server_url = self.server_url
    start_run = time.time()
    refresh_num = 0
    time.sleep(15)
    while True:
        final_body = self.getBody()
        if final_body.find(auto_refresh_string) < 0:
            break
        time.sleep(15)
        refresh_num += 1
        run_time = time.time() - start_run
        print '\n Refreshed ' + str(refresh_num) + ' times. Been running for '\
              + str(round(run_time/60.0, 2)) + ' minutes.\n'
        if run_time > MAX_running_time :
            self.fail('Run longer than MAX_running_time')
        self.get(server_url + self.getLastUrl(),
                 description="Get /cgi-bin/pals_checkdone.cgi")
        time.sleep(5)
    ## print final_body
    expected = final_body.find(final_output) >= 0
    if not expected:
        self.fail('\n ***** (begin of) Unexpected final result!!!! *****\n' + \
                 str(final_body) + \
                 '\n ***** (end of) Unexpected final result!!!! *****\n')
    else:
        print 'OK'


    
class PaLS(FunkLoadTestCase):
    """XXX

    This test use a configuration file PaLS.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = 'http://pals.bioinfo.cnio.es'
        ##self.server_url = self.conf_get('main', 'url')

    def test_testHsentrez(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------

        self.get(server_url + "/",
            description="Get /")
        self.post("http://pals.bioinfo.cnio.es/cgi-bin/intro2.py", params=[
            ['organism', 'Hs'],
            ['idType', 'entrez'],
            ['userFile', Upload("Hs-entrez.3lists.txt")],
            ['datafile', ''],
            ['pubmedIntra', '50'],
            ['pubmedInterPercent', '55'],
            ['pubmedInterMin', '50'],
            ['pubmedInterMinList', '50'],
            ['goIntra', '50'],
            ['goInterPercent', '50'],
            ['goInterMin', '50'],
            ['goInterMinList', '50'],
            ['keggIntra', '50'],
            ['keggInterPercent', '50'],
            ['keggInterMin', '50'],
            ['keggInterMinList', '50'],
            ['reactomePathIntra', '50'],
            ['reactomePathInterPercent', '50'],
            ['reactomePathInterMin', '5'],
            ['reactomePathInterMinList', '50']],
            description="Post /cgi-bin/intro2.py")
            
        final_output = 'Per list'
        common_part(self, final_output)
            

        # end of test -----------------------------------------------
    def test_Hsensembl(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------

        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/intro2.py", params=[
            ['organism', 'Hs'],
            ['idType', 'ensembl'],
            ['userFile', Upload("Hs-ens.kegg.aillats.txt")],
            ['datafile', ''],
            ['pubmedIntra', '50'],
            ['pubmedInterPercent', '50'],
            ['pubmedInterMin', '50'],
            ['pubmedInterMinList', '50'],
            ['goIntra', '10'],
            ['goInterPercent', '10'],
            ['goInterMin', '10'],
            ['goInterMinList', '10'],
            ['keggIntra', '1'],
            ['keggInterPercent', '10'],
            ['keggInterMin', '10'],
            ['keggInterMinList', '10'],
            ['reactomePathIntra', '10'],
            ['reactomePathInterPercent', '10'],
            ['reactomePathInterMin', '10'],
            ['reactomePathInterMinList', '10']],
            description="Post /cgi-bin/intro2.py")

        final_output = 'Per list'
        common_part(self, final_output)
    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")

if __name__ in ('main', '__main__'):
    unittest.main()
