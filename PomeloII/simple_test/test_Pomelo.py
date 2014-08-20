# -*- coding: iso-8859-15 -*-
"""pomelo FunkLoad test

$Id: $
"""
import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase
from webunit.utility import Upload
#from funkload.utils import xmlrpc_get_credential

class Pomelo(FunkLoadTestCase):
    """XXX

    This test use a configuration file Pomelo.conf.
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

    def test_pomelo(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------


        self.get(server_url + "/",
            description="Get /")

        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("covariate")],
            ['class_labels', Upload("event")],
            ['censored_indicator', Upload("empty.txt")],
            ['testtype', 't'],
            ['num_permut', '2000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="Post /cgi-bin/pomeloII.cgi")

        self.get(server_url + "/cgi-bin/pomelo_checkdone.cgi?newDir=4527100384224111405449294871",
            description="Get /cgi-bin/pomelo_checkdone.cgi")

        # end of test -----------------------------------------------

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")



if __name__ in ('main', '__main__'):
    unittest.main()
