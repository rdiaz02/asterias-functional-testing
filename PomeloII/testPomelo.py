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
    time.sleep(3)
    print '\n At 00 \n'
    while True:
        try:
            print '\n At 01 \n'
            final_body = self.getBody()
        except:
            time.sleep(5)
            print '\n At 01-except \n'
            final_body = self.getBody()
        print '\nGot to 1\n'
        if final_body.find(auto_refresh_string) < 0:
            print '\nGot to break\n'
            break
        time.sleep(13)
        refresh_num += 1
        run_time = time.time() - start_run
        print '\nGot to 2\n'
        print '\n Refreshed ' + str(refresh_num) + ' times. Been running for '\
              + str(round(run_time/60.0, 2)) + ' minutes.\n'
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
            time.sleep(5)
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


    #     self.get(server_url + self.getLastUrl(),
    #              description="Get /cgi-bin/checkdone.cgi")
    #     print '\nGot to 3\n'
    #     time.sleep(15)
    #     print '\nGot to 4\n'
    # ## print final_body
    # expected = final_body.find(final_output) >= 0
    # print '\nGot to 5\n'
    # if not expected:
    #     self.fail('\n ***** (begin of) Unexpected final result!!!! *****\n' + \
    #              str(final_body) + \
    #              '\n ***** (end of) Unexpected final result!!!! *****\n')
    # else:
    #     print 'OK'


def common_weird(self):
    ''' For weird names, we do something special, otherwise it takes
    forever.  We do not wait for it to really finish and return results,
    because getting back the results, and reading and processing them
    takes forever. We just let it run for a few minutes, and thats it. If
    it crashes, the run would not return the checkdone.cgi, and thus this
    test would fail.
    Not needed in the weird_2 directory.    '''
    server_url = self.server_url
    start_run = time.time()
    refresh_num = 0
 
    for i in range(0, 5):
        print 'Looping inside common weird ' + str(refresh_num + 1) + '\n'
        time.sleep(2)
        lastu = self.getLastUrl()
        print 'lastu = ' + lastu
        self.get(server_url + lastu)
        refresh_num += 1
    print "OK"
##  self.get(server_url + self.getLastUrl().replace('results.html', 'class_labels'))
#    final_body = self.getBody()
#    print final_body
#    self.assert_(final_body.find('WeirdClassA	WeirdClassA	WeirdClassb	WeirdClassb') >= 0,
#                 'Unexpected final result')


    
class Pomelo(FunkLoadTestCase):
    """XXX

    This test use a configuration file Pomelo.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = 'http://pomelo2.iib.uam.es'
        ##self.server_url = self.conf_get('main', 'url')

    def test_t(self):
        server_url = self.server_url

        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./simple_test/covariate")],
            ['class_labels', Upload("./simple_test/event")],
            ['censored_indicator', Upload("./simple_test/empty.txt")],
            ['testtype', 't'],
            ['num_permut', '900000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="Post /cgi-bin/pomeloII.cgi")

        final_output = 'Chosen test type: t-test<br> Permutations used'
        common_part(self, final_output)

    def test_Anova(self):
        server_url = self.server_url

        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./simple_test/covariate")],
            ['class_labels', Upload("./simple_test/event")],
            ['censored_indicator', Upload("./simple_test/empty.txt")],
            ['testtype', 'Anova'],
            ['num_permut', '3000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="Post /cgi-bin/pomeloII.cgi")

        final_output = 'your data must have more than two classes'
        common_part(self, final_output)


    def test_Cox(self):
        server_url = self.server_url

        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./simple_test/covariate")],
            ['class_labels', Upload("./simple_test/time")],
            ['censored_indicator', Upload("./simple_test/event")],
            ['testtype', 'Cox'],
            ['num_permut', '2000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="Post /cgi-bin/pomeloII.cgi")

        final_output = 'Chosen test type: Cox'
        common_part(self, final_output)

    def test_FisherIJ_wrong_input(self):
        server_url = self.server_url

        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./fisherIxJ/covariate")],
            ['class_labels', Upload("./fisherIxJ/class_labels")],
            ['censored_indicator', Upload("./fisherIxJ/empty.txt")],
            ['testtype', 'FisherIxJ'],
            ['num_permut', '3000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="Fisher IxJ wrong imput")

        final_output = 'Your data are not made of consecutive integers that start at 0'
        common_part(self, final_output)


    def test_FisherIJ_NA(self):
        server_url = self.server_url

        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./fisherIxJ.na/data")],
            ['class_labels', Upload("./fisherIxJ.na/labels")],
            ['censored_indicator', Upload("./fisherIxJ/empty.txt")],
            ['testtype', 'FisherIxJ'],
            ['num_permut', '200000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="Fisher IxJ NA")

        final_output = '<td>gene1</td><td>1</td><td>2.5e-06</td><td>2.02e-05</td><td>0.999997</td><td>0.999997</td>'
        common_part(self, final_output)



    def test_division_by_zero(self):
        server_url = self.server_url

        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./division.by.zero/covariate")],
            ['class_labels', Upload("./division.by.zero/time")],
            ['censored_indicator', Upload("./division.by.zero/event")],
            ['testtype', 'Cox'],
            ['num_permut', '3000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="Division by zero")

        final_output = 'Chosen test type: Cox'
        common_part(self, final_output)


    def test_anova_inf(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./Problema-Inf-Anova/f7.txt")],
            ['class_labels', Upload("./Problema-Inf-Anova/CLASES_ANOVA.txt")],
            ['censored_indicator', Upload("./division.by.zero/event")],
            ['testtype', 'Anova'],
            ['num_permut', '3000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="Anova Iput")
        final_output = 'Some genes have as many missings as the size  of the smallest class minus 1' 
        common_part(self, final_output)

    def test_anova_cte(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./Problema-Inf-Anova/f11.txt")],
            ['class_labels', Upload("./Problema-Inf-Anova/CLASES_ANOVA.txt")],
            ['censored_indicator', Upload("./division.by.zero/event")],
            ['testtype', 'Anova'],
            ['num_permut', '3000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="Anova constant values")
        final_output = 'Some genes are constant for all samples. This leads to variances = 0 and is probably not what you want. Please remove these genes and try again. The genes with constat values are in positions  1'
        common_part(self, final_output)

    def test_regression(self):
        print '\n\nGot to -3\n\n'
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        print '\n\nGot to -2\n\n'
        #time.sleep(5)
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./regress/covar")],
            ['class_labels', Upload("./regress/surv")],
            ['censored_indicator', Upload("./division.by.zero/event")],
            ['testtype', 'Regres'],
            ['num_permut', '3000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="Regression")
        print '\n\nGot to -1\n\n'
        time.sleep(10)
        final_output = 'Chosen test type: Regression'
        common_part(self, final_output)


    def test_apache1(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./apache-prob1/covariate")],
            ['class_labels', Upload("./apache-prob1/class_labels")],
            ['censored_indicator', Upload("./apache-prob1/empty")],
            ['testtype', 't'],
            ['num_permut', '3000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="More than one Name line")
        final_output = '<p> You have more than one line with "#Name" (or "#NAME" or "#name")," in the data matrixbut only one is allowed.'
        common_part(self, final_output)

    def test_apache2(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./apache-prob2/covariate")],
            ['class_labels', Upload("./apache-prob2/class_labels")],
            ['censored_indicator', Upload("./apache-prob2/censored_indicator")],
            ['testtype', 'Cox'],
            ['num_permut', '3000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="More than one Name line (II)")
        final_output = '<p> You have more than one line with "#Name" (or "#NAME" or "#name")," in the data matrixbut only one is allowed.'
        common_part(self, final_output)

    def test_apache3(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./apache-prob3/covariate")],
            ['class_labels', Upload("./apache-prob3/class_labels")],
            ['censored_indicator', Upload("./apache-prob3/empty")],
            ['testtype', 't'],
            ['num_permut', '2000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description='Name with "')
        final_output = 'Chosen test type: t-test'
        common_part(self, final_output)

    def test_regress_diffs(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./ngenes/c2")],
            ['class_labels', Upload("./ngenes/surv.wrong")],
            ['censored_indicator', Upload("./ngenes/empty")],
            ['testtype', 'Regres'],
            ['num_permut', '2000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description='Different number columns')
        # final_output = 'The class file and the Gene expression file<br> do not agree on the number of arrays'
        final_output = 'different number of class labels (40) and columns of data (10)'
        common_part(self, final_output)

### Three tests for limma

    def test_limma_t(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./limma_t/covariate")],
            ['class_labels', Upload("./limma_t/class_labels")],
            ['censored_indicator', Upload("")],
            ['testtype', 't_limma'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="limma_t")
        final_output = 'Chosen test type: Limma t-test'
        common_part(self, final_output)

    def test_limma_t2(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./javier-p/data.txt")],
            ['class_labels', Upload("./javier-p/class.txt")],
            ['censored_indicator', Upload("")],
            ['testtype', 't_limma'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="limma_t with extra blanks in class file")
        final_output = 'Chosen test type: Limma t-test'
        common_part(self, final_output)


    def test_limma_t_paired(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./limma_t/covariate")],
            ['class_labels', Upload("./limma_t/class_labels")],
            ['censored_indicator', Upload("")],
            ['testtype', 't_limma_paired'],
            ['paired_indicator', Upload("./limma_t/paired_indicator")],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="t_limma_paired")
        final_output = 'Chosen test type: Limma paired t-test'
        common_part(self, final_output)

### this is a very limited test, because only captures the request for
### covariates, but the numerical testing contains detail testing
        ### of actual numerical output.
    def test_limma_Anova(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./limma_anova/covariate")],
            ['class_labels', Upload("./limma_anova/class_labels")],
            ['censored_indicator', Upload("")],
            ['testtype', 'Anova_limma'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="t_limma_Anova")
        final_output = 'Add covariables to analysis'
        common_part(self, final_output)

    def test_limma_Anova2(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./ngenes/c6")],
            ['class_labels', Upload("./ngenes/event")],
            ['censored_indicator', Upload("")],
            ['testtype', 'Anova_limma'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="limma_Anova with 2 classes")
        final_output = 'Add covariables to analysis'
        common_part(self, final_output)


    def test_limma_not_estimable(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./limma_anova/covariate10")],
            ['class_labels', Upload("./limma_anova/class10")],
            ['censored_indicator', Upload("")],
            ['testtype', 'Anova_limma'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="limma_Anova not estimable problem")
        url1 = self.getLastUrl()
        tmpDir = url1[(url1.rfind('?newDir=') + 8):]
        time.sleep(3)
        self.post(server_url + "/cgi-bin/check_covariables.cgi", params=[
            ['covariables', Upload("./limma_anova/covs10")],
            ['cgi_option', 'check_covariables'],
            ['tmp_dir', '/asterias-web-apps/pomelo2/www/tmp/' + tmpDir]],
                  description="Post /cgi-bin/check_covariables.cgi")
        time.sleep(3)
        self.post(server_url + "/cgi-bin/check_covariables.cgi",
                  params=[
            ['cgi_option', 'covar_launch'],
            ['tmp_dir', '/asterias-web-apps/pomelo2/www/tmp/' + tmpDir],
            ['V1', 'V1'],
            ['submit_button', ' Send selected covariables ']],
                  description="check_covariables.cgi: submit V1")
        final_output = 'Some coefficients of your design are not estimable'
        common_part(self, final_output)



### The following test how it deals with pathological files:
### Zero, one, two rows of data, and binary data.
### It is testing a common part, but just in case we try
### t-test, Anova, regression (permutations), fisher, and a few limmas.

    def test_binary_1(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./ngenes/binary.file")],
            ['class_labels', Upload("./ngenes/event")],
            ['censored_indicator', Upload("./ngenes/empty")],
            ['testtype', 't'],
            ['num_permut', '2000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description='Name with "')
        final_output = 'INPUT ERROR'
        common_part(self, final_output)

    def test_binary_2(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./ngenes/c2")],
            ['class_labels', Upload("./ngenes/binary.file")],
            ['censored_indicator', Upload("./ngenes/empty")],
            ['testtype', 't'],
            ['num_permut', '2000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description='Name with "')
        final_output = 'INPUT ERROR'
        common_part(self, final_output)

    def test_c0a_t(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./ngenes/c0a")],
            ['class_labels', Upload("./ngenes/event")],
            ['censored_indicator', Upload("./ngenes/empty")],
            ['testtype', 't'],
            ['num_permut', '2000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description='Name with "')
        final_output = 'You need at least one gene to use Pomelo II.'
        common_part(self, final_output)

    def test_c0b_t(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./ngenes/c0b")],
            ['class_labels', Upload("./ngenes/event")],
            ['censored_indicator', Upload("./ngenes/empty")],
            ['testtype', 't'],
            ['num_permut', '2000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description='Name with "')
        final_output = 'You need at least one gene to use Pomelo II.'
        common_part(self, final_output)

    def test_c1_t(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./ngenes/c1")],
            ['class_labels', Upload("./ngenes/event")],
            ['censored_indicator', Upload("./ngenes/empty")],
            ['testtype', 't'],
            ['num_permut', '2000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description='Name with "')
        print '\n       ***** Did the self.post *****\n'
        final_output = 'Chosen test type: t-test'
        common_part(self, final_output)

    def test_c2_t(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./ngenes/c2")],
            ['class_labels', Upload("./ngenes/event")],
            ['censored_indicator', Upload("./ngenes/empty")],
            ['testtype', 't'],
            ['num_permut', '2000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description='Name with "')
        final_output = 'Chosen test type: t-test'
        common_part(self, final_output)

    def test_c0a_anova(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./ngenes/c0a")],
            ['class_labels', Upload("./ngenes/event.anova")],
            ['censored_indicator', Upload("./ngenes/empty")],
            ['testtype', 'Anova'],
            ['num_permut', '2000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description='Name with "')
        final_output = 'You need at least one gene to use Pomelo II.'
        common_part(self, final_output)

    def test_c0b_anova(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./ngenes/c0b")],
            ['class_labels', Upload("./ngenes/event.anova")],
            ['censored_indicator', Upload("./ngenes/empty")],
            ['testtype', 'Anova'],
            ['num_permut', '2000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description='Name with "')
        final_output = 'You need at least one gene to use Pomelo II.'
        common_part(self, final_output)


    def test_c1_anova(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./ngenes/c1")],
            ['class_labels', Upload("./ngenes/event.anova")],
            ['censored_indicator', Upload("./ngenes/empty")],
            ['testtype', 'Anova'],
            ['num_permut', '2000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description='Name with "')
        final_output = 'Chosen test type:  Anova'
        common_part(self, final_output)

    def test_c2_anova(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./ngenes/c2")],
            ['class_labels', Upload("./ngenes/event.anova")],
            ['censored_indicator', Upload("./ngenes/empty")],
            ['testtype', 'Anova'],
            ['num_permut', '2000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description='Name with "')
        final_output = 'Chosen test type:  Anova'
        common_part(self, final_output)

    def test_c0a_regress(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./ngenes/c0a")],
            ['class_labels', Upload("./ngenes/surv.correct")],
            ['censored_indicator', Upload("./ngenes/empty")],
            ['testtype', 'Regres'],
            ['num_permut', '2000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description='Name with "')
        final_output = 'different number of class labels (10) and columns of data (0)'
        common_part(self, final_output)

    def test_c0b_regress(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./ngenes/c0b")],
            ['class_labels', Upload("./ngenes/surv.correct")],
            ['censored_indicator', Upload("./ngenes/empty")],
            ['testtype', 'Regres'],
            ['num_permut', '2000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description='Name with "')
        final_output = 'different number of class labels (10) and columns of data (0)'
        common_part(self, final_output)

    def test_c1_regress(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./ngenes/c1")],
            ['class_labels', Upload("./ngenes/surv.correct")],
            ['censored_indicator', Upload("./ngenes/empty")],
            ['testtype', 'Regres'],
            ['num_permut', '2000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description='Name with "')
        final_output = 'Chosen test type: Regression'
        common_part(self, final_output)

    def test_c2_regress(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./ngenes/c2")],
            ['class_labels', Upload("./ngenes/surv.correct")],
            ['censored_indicator', Upload("./ngenes/empty")],
            ['testtype', 'Regres'],
            ['num_permut', '2000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description='Name with "')
        final_output = 'Chosen test type: Regression'
        common_part(self, final_output)

    def test_c0a_limma(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./ngenes/c0a")],
            ['class_labels', Upload("./ngenes/event.anova")],
            ['censored_indicator', Upload("./ngenes/empty")],
            ['testtype', 't_limma'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description='Name with "')
        final_output = 'You need at least one gene to use Pomelo II'
        common_part(self, final_output)

    def test_c0b_limma(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./ngenes/c0b")],
            ['class_labels', Upload("./ngenes/event.anova")],
            ['censored_indicator', Upload("./ngenes/empty")],
            ['testtype', 't_limma'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description='Name with "')
        final_output = 'You need at least one gene to use Pomelo II'
        common_part(self, final_output)


    def test_c1_limma(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./ngenes/c1")],
            ['class_labels', Upload("./ngenes/event.anova")],
            ['censored_indicator', Upload("./ngenes/empty")],
            ['testtype', 't_limma'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description='Name with "')
        final_output = 'For all limma tests you need at least two genes'
        common_part(self, final_output)

### Testing weird names; just that, test it can handle what it should.
        ### See F.and.t.R.
    
    def test_limma_t_weird_names(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./weird_names/covariate")],
            ['class_labels', Upload("./weird_names/class")],
            ['censored_indicator', Upload("")],
            ['testtype', 't_limma'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="limma_t weird names")
        common_weird(self)

    def test_t_weird_names(self):
        server_url = self.server_url

        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./weird_names/covariate")],
            ['class_labels', Upload("./weird_names/class")],
            ['censored_indicator', Upload("./simple_test/empty.txt")],
            ['testtype', 't'],
            ['num_permut', '3000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="Permut t, weird names")
        common_weird(self)

    def test_limma_t_weird_names_2(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./weird_names_2/covariate")],
            ['class_labels', Upload("./weird_names_2/class")],
            ['censored_indicator', Upload("")],
            ['testtype', 't_limma'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="limma_t weird names")
        final_output = 'Chosen test type: Limma t-test'
        common_part(self, final_output)


    def test_t_weird_names_2(self):
        server_url = self.server_url

        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./weird_names_2/covariate")],
            ['class_labels', Upload("./weird_names_2/class")],
            ['censored_indicator', Upload("./simple_test/empty.txt")],
            ['testtype', 't'],
            ['num_permut', '3000'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="Permut t, weird names")
        final_output = 'Chosen test type: t-test<br> Permutations used'
        common_part(self, final_output)


    def test_heat_error_1(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/pomeloII.cgi", params=[
            ['covariate', Upload("./heat_error/covariate")],
            ['class_labels', Upload("./heat_error/class_labels")],
            ['censored_indicator', Upload("")],
            ['testtype', 't_limma'],
            ['idtype', 'None'],
            ['organism', 'None']],
            description="limma_t")
        final_output = 'Chosen test type: Limma t-test'
        common_part(self, final_output)



    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")

if __name__ in ('main', '__main__'):
    unittest.main()



### Add tests that catch when we have empyt trailing tabs in class labels (bot discrete and cont.)
### Add tests (here AND/OR numerical) when we have, for covariates:
    ### a) only one numerical
    ### b) two numerical
    ### c) only one categorical
    ### d) two categorical
    ### e) a mix of the above
    ###  see directory LL-cat for something that used to break it
