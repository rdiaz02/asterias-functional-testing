"""
Drive one of our web-based applications for numerical testing.

Using FunkLoad's basic_navigation, but without requiring unit testing
framework, it allows to upload a specific set of files, and download the
results. 

 Example

 pom1 = NumTesting()
 pom1.setUp('http://pomelo2.bioinfo.cnio.es')
 pom1.send_get_pomelo('c4', 'event', '', 't', '3000')


License:
--------
this file adds some modifications to the classes and methods
defined in the file funkload/FunkLoadTestCase of the funkload library.
The funkload library has been developed and is copyright by Benoit
Delbosc, http://funkload.nuxeo.org/.

The funkload library is licensed under the GNU GPL license, v. 2, and thus
this file is also licensed under the GNU GPL v. 2. This file is copyright,
(c), Ramon Diaz-Uriarte, http://ligarto.org/rdiaz.

"""


import time
import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase
from webunit.utility import Upload
from urllib import urlretrieve

auto_refresh_string = 'This is an autorefreshing page'
MAX_running_time = 3600 * 1 


URL_APPL          = 'http://pomelo2.bioinfo.cnio.es'
FINAL_OUTPUT      = 'Output table:'
FILE_TO_DOWNLOAD  = 'multest_parallel.res'
LOCAL_FILE        = './tmp-files/results.txt'
POST_APPL         = '/cgi-bin/pomeloII.cgi'
TMP_DIR           = '/http/pomelo2/www/tmp/'


LONG_SLEEP   = 24 ## 184
MEDIUM_SLEEP = 5 ## 67
BRIEF_SLEEP  = 1 ## 5 




class NumTesting(FunkLoadTestCase):
    #     def __init__(self):
    #         self.setUp()

    def __init__(self, methodName='', options=None):
        """ 
        Initialise the test case. Note that methodName is encoded in bench
        mode to provide additional information like thread_id, concurrent
        virtual users. I (R.D-U) took this init from the FunkLoadTestCase
        class, and modified it so that it works stand alone. 
        """
        self.in_bench_mode = False
        self.meta_method_name = ''
#         if mmn_is_bench(methodName):
#             self.in_bench_mode = True
#         else:
#             self.in_bench_mode = False
#         self.test_name, self.cycle, self.cvus, self.thread_id = mmn_decode(
#             methodName)
        self.test_name, self.cycle, self.cvus, self.thread_id = \
                        ('pomeloStandAlone', 1, 0, 1)
#         self.meta_method_name = methodName
#         self.suite_name = self.__class__.__name__
        self.suite_name = 'pomeloStandAloneSuite'
#         unittest.TestCase.__init__(self, methodName=self.test_name)
        self._response = None
        self.options = options
        self.debug_level = 2 ## getattr(options, 'debug_level', 0)
        self._funkload_init()
        self._dump_dir = getattr(options, 'dump_dir', None)
        self._dumping =  self._dump_dir and True or False
        self._viewing = getattr(options, 'firefox_view', False)
        self._accept_invalid_links = getattr(options, 'accept_invalid_links',
                                             False)
        self._simple_fetch = True ##getattr(options, 'simple_fetch', False)
        self._stop_on_fail = getattr(options, 'stop_on_fail', False)
        if self._viewing and not self._dumping:
            # viewing requires dumping contents
            self._dumping = True
            self._dump_dir = mkdtemp('_funkload')
        self._loop_mode = getattr(options, 'loop_steps', False)
        if self._loop_mode:
            if options.loop_steps.count(':'):
                steps = options.loop_steps.split(':')
                self._loop_steps = range(int(steps[0]), int(steps[1]))
            else:
                self._loop_steps = [int(options.loop_steps)]
            self._loop_number = options.loop_number
            self._loop_recording = False
            self._loop_records = []

    def setUp(self, URL_APPL):
        """Setting up test."""
##        self.logd("setUp")
        self.server_url = URL_APPL
        ##self.server_url = self.conf_get('main', 'url')
        
        
    def get_results(self,                 
                    MAX_running_time = 3600,
                    auto_refresh_string = auto_refresh_string,
                    files = {FILE_TO_DOWNLOAD: LOCAL_FILE}):
        """ Download results from the application.
        This function could be used with all applications, but
        strings for FILE_TO_DOWNLOAD, LOCAL_FILE, and FINAL_OUTPUT
        would need to be passed as arguments. """
         
        server_url = self.server_url
        start_run = time.time()
        refresh_num = 0
       
        while True:
            final_body = self.getBody()
            if final_body.find(auto_refresh_string) < 0:
                break
            time.sleep(LONG_SLEEP)
            refresh_num += 1
            run_time = time.time() - start_run
            print '\n Refreshed ' + str(refresh_num) + ' times. Been running for '\
                  + str(round(run_time/60.0, 2)) + ' minutes.\n'
            if run_time > MAX_running_time :
                self.fail('Run longer than MAX_running_time')
            
            self.get(server_url + self.getLastUrl(),
                     description="Get /cgi-bin/checkdone.cgi")
 
        ## The next is to exit gracefully and meaningfully
        ## if we have screwed up
             
        self.assert_(final_body.find(FINAL_OUTPUT) >= 0,
                     '\n ***** (begin of) Unexpected final result!!!! *****\n' + \
                     str(final_body) + \
                     '\n ***** (end of) Unexpected final result!!!! *****\n')

        url_before_get = self.getLastUrl()
        time.sleep(MEDIUM_SLEEP)
        for keys in files:
            urlretrieve(server_url +
                        url_before_get.replace('results.html', keys),
                        filename = files[keys])


##    def test_pomelo(self):  ###, Covar, Class, Status, Test_type, Num_permut):
    def send_get_pomelo(self, Covar, Class, Status, Test_type, Num_permut,
                        paired_indicator = None, other_covars = None):
        """
        Do a POST sending the files and get results.
        Sets application-specific parameters.
        This should be the only application-specific function.
        """
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        time.sleep(BRIEF_SLEEP)
        if not Test_type in ('t_limma_paired', 'Anova_limma'):
            self.post(server_url + POST_APPL, params=[
                ['covariate', Upload(Covar)],
                ['class_labels', Upload(Class)],
                ['censored_indicator', Upload(Status)],
                ['testtype', Test_type],
                ['num_permut', Num_permut],
                ['idtype', 'None'],
                ['organism', 'None']],
                      description = "Post ")
            time.sleep(MEDIUM_SLEEP)
            self.get_results(self)
        elif Test_type == 't_limma_paired':
            self.post(server_url + POST_APPL,
                      params=[
                ['covariate', Upload(Covar)],
                ['class_labels', Upload(Class)],
                ['censored_indicator', Upload(Status)],
                ['testtype', Test_type],
                ['num_permut', Num_permut],
                ['paired_indicator', Upload(paired_indicator)],
                ['idtype', 'None'],
                ['organism', 'None']],
                      description="Post ")
            time.sleep(MEDIUM_SLEEP)
            self.get_results(self)
        elif Test_type == 'Anova_limma':
            ## get ready for a break in the logic...
            self.post(server_url + POST_APPL,
                      params=[
                ['covariate', Upload(Covar)],
                ['class_labels', Upload(Class)],
                ['censored_indicator', Upload(Status)],
                ['testtype', Test_type],
                ['num_permut', Num_permut],
                ['idtype', 'None'],
                ['organism', 'None']],
                      description="Post ")
            ## Handle the enter additional covariates
            url1 = self.getLastUrl()
            tmpDir = url1[(url1.rfind('?newDir=') + 8):]
            time.sleep(MEDIUM_SLEEP)
            if other_covars:
                ## FIXME: allow more/other covar names
                self.post(server_url + "/cgi-bin/check_covariables.cgi", params=[
                    ['covariables', Upload(other_covars)],
                    ['cgi_option', 'check_covariables'],
                    ['tmp_dir', TMP_DIR + tmpDir]],
                    description="Post /cgi-bin/check_covariables.cgi")
                time.sleep(MEDIUM_SLEEP)
                self.post(server_url + "/cgi-bin/check_covariables.cgi",
                          params=[
                    ['cgi_option', 'covar_launch'],
                    ['tmp_dir', TMP_DIR + tmpDir],
                    ['V1', 'V1'],
                    ['V2', 'V2'],
                    ['V3', 'V3'],
                    ['V4', 'V4'],
                    ['submit_button', ' Send selected covariables ']],
                          description="check_covariables.cgi: submit V1, V2, V3, V4")
            else:
                self.post(server_url + "/cgi-bin/check_covariables.cgi",
                          params=[
                    ['covariables', Upload('empty.txt')],
                    ['cgi_option', 'continue'],
                    ['tmp_dir', TMP_DIR + tmpDir]],
                          description="check_covariables.cgi: don't use any")
            print '\n tmp directory is: ' + tmpDir
            while True:  ## wait for computations to finish
                final_body = self.getBody()
                if final_body.find(auto_refresh_string) < 0:
                    break
                time.sleep(LONG_SLEEP)
                print '   ... waiting for checkdone.cgi to be done'
                self.get(server_url + self.getLastUrl(),
                     description="Get /cgi-bin/checkdone.cgi")
            url2 = self.getLastUrl()
            self.get(server_url + \
                     url2.replace('results.html', 'class_compare.html'),
                     description = "Get to the class comparison page")
            time.sleep(MEDIUM_SLEEP)
            ## Post all the class comparisons: FIXME: make general looping over all pairs
            self.post(server_url + "/cgi-bin/Anova_contrasts.cgi",
                      params = [
                ['tmp_dir', TMP_DIR + tmpDir],
                ['cgi_option', 'class_comp'],
                ['class1', '0'],
                ['class2', '1']],
                      description = "Post class0 vs class1")
            time.sleep(MEDIUM_SLEEP)
            self.post(server_url + "/cgi-bin/Anova_contrasts.cgi",
                      params = [
                ['tmp_dir', TMP_DIR + tmpDir],
                ['cgi_option', 'class_comp'],
                ['class1', '0'],
                ['class2', '2']],
                      description = "Post class0 vs class2")
            time.sleep(MEDIUM_SLEEP)
            self.post(server_url + "/cgi-bin/Anova_contrasts.cgi",
                      params = [
                ['tmp_dir', TMP_DIR + tmpDir],
                ['cgi_option', 'class_comp'],
                ['class1', '1'],
                ['class2', '2']],
                      description = "Post class1 vs class2")
            ###  Get results
            ###  FIXME: parameterize this
            time.sleep(MEDIUM_SLEEP)
            files = {'Class0-Class1.res':'./tmp-files/class0-class1.txt',
                     'Class0-Class2.res':'./tmp-files/class0-class2.txt',
                     'Class1-Class2.res':'./tmp-files/class1-class2.txt'}
            for keys in files:
                urlretrieve(server_url +
                            url2.replace('results.html', keys),
                            filename = files[keys])
            

