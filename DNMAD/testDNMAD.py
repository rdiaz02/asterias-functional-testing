# -*- coding: iso-8859-15 -*-
"""all FunkLoad test

This isn't really working

$Id: $
"""
import time
import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase
from webunit.utility import Upload

auto_refresh_string = 'This is an autorefreshing page'
MAX_running_time = 3600 * 1 

def common_part(self, serverurl, final_output,                
		MAX_running_time = 3600,
		auto_refresh_string = auto_refresh_string):    
    server_url = serverurl
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
    print(final_body)
    self.assert_(final_body.find(final_output) >= 0,'Unexpected final result')

    
def getTempString(self,final_output):
	bodyx = self.getBody()
	if bodyx.find("ERROR") > 0:
		self.fail('Catched error')
	elif bodyx.find("http://"):
		a = bodyx.split("http://")
		urltmp = "http://" +a[2][:-1]
		print "\n" + urltmp
		self.get(urltmp, description= "Get results")	    
		final_body = self.getBody()
		if final_body.find('Fix your input data'):
			print 'error.html'
		if final_body.find(final_output):
			print 'Run OK'
		return urltmp
	else:
		self.fail('Un-catched error')
	    
    
class All(FunkLoadTestCase):
    """XXX

    This test use a configuration file All.conf.
    """              
    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = 'http://dnmad.bioinfo.cnio.es'

    def test1(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/dnmad.cgi", params=[
            ['ind_files', ''],
            ['arrays_file', Upload("./test1/data.tar.gz")],
            ['arrays_file_rg', '1'],
            ['ngr', '12'],
            ['ngc', '4'],
            ['nsr', '17'],
            ['nsc', '16'],
            ['flags', 'yes'],
            ['flagged', 'yes'],
            ['BS', 'yes'],
            ['bgsubtract', 'half'],
            ['run', 'Run']],
            description="Post /cgi-bin/dnmad.cgi")
	
	final_output = 'Results'
        common_part(self, final_output)
	stringtolook = getTempString(self, final_output)
	
	
	
    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")



if __name__ in ('main', '__main__'):
    unittest.main()
