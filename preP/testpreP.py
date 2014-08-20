# -*- coding: iso-8859-15 -*-
"""basic_navigation FunkLoad test

$Id: $
"""
import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase
from webunit.utility import Upload
#from funkload.utils import xmlrpc_get_credential

MAX_running_time = 3600 * 1 

def commonOutput(self,final_output):
	bodyx = self.getBody()
	if bodyx.find("ERROR") > 0:
##		self.fail('Catched error') ## I think this will fail even when it shouldn't
		final_body = self.getBody()
		if final_body.find(final_output):
			print 'Run OK'
		else:
			print str(bodyx)
			self.fail('Caught error, but unexpected output')
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
	else:
		print str(bodyx)
		self.fail('Un-catched error')
	    


class preP(FunkLoadTestCase):
    """XXX

    This test use a configuration file BasicNavigation.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = self.conf_get('main', 'url')
        # XXX here you can setup the credential access like this
        # credential_host = self.conf_get('credential', 'host')
        # credential_port = self.conf_getInt('credential', 'port')
        # self.login, self.password = xmlrpc_get_credential(credential_host,
        #                                                   credential_port)


    def test1(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------

	self.get(server_url + "/",
		description = "Get /")
	
        self.post(server_url + "/cgi-bin/prep.py", params=[
            ['covariate', Upload("./test1/mini.lung.covar.txt")],
            ['o_filter', '1'],
            ['op_filter', '70'],
            ['o_impute', '2'],
            ['op_impute', 'knn'],
            ['op_impute_knn', '15'],
            ['o_merge', '3'],
            ['op_merge', 'mean'],
            ['o_remove', '4']],
            description="Post /cgi-bin/prep.py")
	    
	final_output = "Summary"
	commonOutput(self,final_output)


        # end of test -----------------------------------------------

    def test2(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------

	self.get(server_url + "/",
		description = "Get /")
	
        self.post(server_url + "/cgi-bin/prep.py", params=[
            ['covariate', Upload("./test2/excel.txt")],
            ['o_filter', '1'],
            ['op_filter', '70'],
            ['o_impute', '2'],
            ['op_impute', 'knn'],
            ['op_impute_knn', '15'],
            ['o_merge', '3'],
            ['op_merge', 'mean'],
            ['o_remove', '4']],
            description="Post /cgi-bin/prep.py")
	    
	final_output = "Summary"
	commonOutput(self,final_output)


        # end of test -----------------------------------------------
	
    def test3(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------

	self.get(server_url + "/",
		description = "Get /")
	
        self.post(server_url + "/cgi-bin/prep.py", params=[
            ['covariate', Upload("./test3/excel.txt")],
            ['o_filter', '1'],
            ['op_filter', '70'],
            ['o_impute', '2'],
            ['op_impute', 'knn'],
            ['op_impute_knn', '15'],
            ['o_merge', '3'],
            ['op_merge', 'mean'],
            ['o_remove', '4']],
            description="Post /cgi-bin/prep.py")
	    
	final_output = "Summary"
	commonOutput(self,final_output)
        # end of test -----------------------------------------------	

    def test4(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------

	self.get(server_url + "/",
		description = "Get /")
	
        self.post(server_url + "/cgi-bin/prep.py", params=[
            ['covariate', Upload("./test3/g1.txt")],
            ['o_filter', '1'],
            ['op_filter', '70'],
            ['o_impute', '2'],
            ['op_impute', 'knn'],
            ['op_impute_knn', '15'],
            ['o_merge', '3'],
            ['op_merge', 'mean'],
            ['o_remove', '4']],
            description="The weird segfault with data from mac")
	    
	final_output = "Calandraca"
	commonOutput(self,final_output)
        # end of test -----------------------------------------------	



    def test_only_gene_name(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------

	self.get(server_url + "/",
		description = "Get /")
	
        self.post(server_url + "/cgi-bin/prep.py", params=[
            ['covariate', Upload("./only-gene-name/input.txt")],
            ['o_filter', '1'],
            ['op_filter', '70'],
            ['o_impute', '2'],
            ['op_impute', 'knn'],
            ['op_impute_knn', '15'],
            ['o_merge', '3'],
            ['op_merge', 'mean'],
            ['o_remove', '4']],
            description="Bug 293: some rows only gene name")
	    
	final_output = "has no data"
	commonOutput(self,final_output)
        # end of test -----------------------------------------------	

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")



if __name__ in ('main', '__main__'):
    unittest.main()
