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
    print '\n Start common_part \n'
    server_url = self.server_url
    start_run = time.time()
    refresh_num = 0
    print '\n At 00 \n'
    while True:
        try:
            print '\n At 01 \n'
            final_body = self.getBody()
        except:
            time.sleep(5)
            print '\n At 01-except \n'
            final_body = self.getBody()

        print '\n At 001 \n'
        if final_body.find(auto_refresh_string) < 0:
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
        except:
            time.sleep(15)
            print '\n At 03 - except \n'
            gg = self.get(checkdoneUrl,
                          description="Get /cgi-bin/checkdone.cgi")
            print '\n This is gg \n'
            print str(gg)
    expected = final_body.find(final_output) >= 0
    if not expected:
        self.fail('\n ***** (begin of) Unexpected final result!!!! *****\n' + \
                 str(final_body) + \
                 '\n ***** (end of) Unexpected final result!!!! *****\n')
    else:
        print 'OK'

    
class Tnasas(FunkLoadTestCase):
    """XXX

    This test use a configuration file Genesrf.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = 'http://tnasas.bioinfo.cnio.es'

    def test1(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        print '\n Start post \n'
        self.post(server_url + "/cgi-bin/tnasasR.cgi", params=[
            ['covariate', Upload("xdata2.txt")],
            ['class', Upload("Class")],
            ['model', 'dlda'],
            ['genesel', 'Fratio'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="dlda and f ratio")
        final_output = 'Classification algorithm:                         DLDA; gene selection using F statistic'
        common_part(self, final_output)

    def test2(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        print '\n Start post \n'
        self.post(server_url + "/cgi-bin/tnasasR.cgi", params=[
            ['covariate', Upload("xdata2.txt")],
            ['class', Upload("Class")],
            ['model', 'knn'],
            ['genesel', 'Wilcoxon'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="knn and wilcoxon")
        final_output = 'Classification algorithm:                         NN; gene selection using Wilcoxon statistic'
        common_part(self, final_output)

    def test3(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        print '\n Start post \n'
        self.post(server_url + "/cgi-bin/tnasasR.cgi", params=[
            ['covariate', Upload("xdata2.txt")],
            ['class', Upload("Class")],
            ['model', 'randomforest'],
            ['genesel', 'Fratio'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="rF and Fratio")
        final_output = 'Classification algorithm:                         Random forest; gene selection using F statistic'
        common_part(self, final_output)

    def test4(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        print '\n Start post \n'
        self.post(server_url + "/cgi-bin/tnasasR.cgi", params=[
            ['covariate', Upload("xdata2.txt")],
            ['class', Upload("Class")],
            ['model', 'svm'],
            ['genesel', 'randomforest'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="svm and randomforest gene sel")
        final_output = 'Classification algorithm:                         SVM (linear kernel); gene selection using Random Forest'
        common_part(self, final_output)

    def test5(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        print '\n Start post \n'
        self.post(server_url + "/cgi-bin/tnasasR.cgi", params=[
            ['covariate', Upload("xdata2.txt")],
            ['class', Upload("Class")],
            ['model', 'PAM'],
            ['genesel', 'Fratio'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="PAM")
        final_output = 'Classification algorithm:                         Shrunken centroids (PAM)'
        common_part(self, final_output)



    def test1_Named(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        print '\n Start post \n'
        self.post(server_url + "/cgi-bin/tnasasR.cgi", params=[
            ['covariate', Upload("./with.mm.names/short.covar2.txt")],
            ['class', Upload("./with.mm.names/class")],
            ['model', 'dlda'],
            ['genesel', 'Fratio'],
            ['organism', 'Mm'],
            ['idtype', 'ug']],
            description="dlda and f ratio, Named")
        final_output = 'Classification algorithm:                         DLDA; gene selection using F statistic'
        common_part(self, final_output)

    def test2_Named(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        print '\n Start post \n'
        self.post(server_url + "/cgi-bin/tnasasR.cgi", params=[
            ['covariate', Upload("./with.mm.names/short.covar2.txt")],
            ['class', Upload("./with.mm.names/class")],
            ['model', 'knn'],
            ['genesel', 'Wilcoxon'],
            ['organism', 'Mm'],
            ['idtype', 'ug']],
            description="knn and wilcoxon, Named")
        final_output = 'Classification algorithm:                         NN; gene selection using Wilcoxon statistic'
        common_part(self, final_output)

    def test3_Named(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        print '\n Start post \n'
        self.post(server_url + "/cgi-bin/tnasasR.cgi", params=[
            ['covariate', Upload("./with.mm.names/short.covar2.txt")],
            ['class', Upload("./with.mm.names/class")],
            ['model', 'randomforest'],
            ['genesel', 'Fratio'],
            ['organism', 'Mm'],
            ['idtype', 'ug']],
            description="randomforest and f ratio, named")
        final_output = 'Classification algorithm:                         Random forest; gene selection using F statistic'
        common_part(self, final_output)

    def test4_Named(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        print '\n Start post \n'
        self.post(server_url + "/cgi-bin/tnasasR.cgi", params=[
            ['covariate', Upload("./with.mm.names/short.covar2.txt")],
            ['class', Upload("./with.mm.names/class")],
            ['model', 'svm'],
            ['genesel', 'randomforest'],
            ['organism', 'Mm'],
            ['idtype', 'ug']],
            description="svm and random forest, Named")
        final_output = 'Classification algorithm:                         SVM (linear kernel); gene selection using Random Forest'
        common_part(self, final_output)

    def test5_Named(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        print '\n Start post \n'
        self.post(server_url + "/cgi-bin/tnasasR.cgi", params=[
            ['covariate', Upload("./with.mm.names/short.covar2.txt")],
            ['class', Upload("./with.mm.names/class")],
            ['model', 'PAM'],
            ['genesel', 'Fratio'],
            ['organism', 'Mm'],
            ['idtype', 'ug']],
            description="PAM, Named")
        final_output = 'Classification algorithm:                         Shrunken centroids (PAM)'
        common_part(self, final_output)



    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")

if __name__ in ('main', '__main__'):
     unittest.main()
