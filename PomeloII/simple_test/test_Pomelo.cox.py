# -*- coding: iso-8859-15 -*-
"""pomelo.cox FunkLoad test

$Id: $
"""
import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase
from webunit.utility import Upload
#from funkload.utils import xmlrpc_get_credential

class Pomelo.cox(FunkLoadTestCase):
    """XXX

    This test use a configuration file Pomelo.cox.conf.
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

    def test_pomelo.cox(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------


        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("covariate")],
            ['class_labels', Upload("time")],
            ['censored_indicator', Upload("event")],
            ['testtype', 'Cox'],
            ['num_permut', '2000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="Post /cgi-bin/pomeloII.cgi")

        self.get(server_url + "/cgi-bin/pomelo_checkdone.cgi?newDir=465879024509411405449967614",
            description="Get /cgi-bin/pomelo_checkdone.cgi")

        self.get(server_url + "/cgi-bin/pomelo_checkdone.cgi?newDir=465879024509411405449967614",
            description="Get /cgi-bin/pomelo_checkdone.cgi")

        # end of test -----------------------------------------------

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")



if __name__ in ('main', '__main__'):
    unittest.main()
