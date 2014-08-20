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



# def common_part(self, final_output,                
#                 MAX_running_time = 3600,
#                 auto_refresh_string = auto_refresh_string):    
#     server_url = self.server_url
#     start_run = time.time()
#     refresh_num = 0
    
#     while True:
#         final_body = self.getBody()
#         if final_body.find(auto_refresh_string) < 0:
#             break
#         time.sleep(32)
#         refresh_num += 1
#         run_time = time.time() - start_run
#         print '\n Refreshed ' + str(refresh_num) + ' times. Been running for ' + str(round(run_time/60.0, 2)) + ' minutes.\n'
#         if run_time > MAX_running_time :
#             self.fail('Run longer than MAX_running_time')
#         self.get(server_url + self.getLastUrl(),
#                  description="Get /cgi-bin/checkdone.cgi")
#     expected = final_body.find(final_output) >= 0
#     if not expected:
# #        self.fail(' ERROR HERE')
#         self.fail('\n ***** (begin of) Unexpected final result!!!! *****\n' + \
#                  str(final_body) + \
#                  '\n ***** (end of) Unexpected final result!!!! *****\n')
#         sys.exit()
#     else:
#         print 'OK'



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

   
class Signs(FunkLoadTestCase):
    """XXX

    This test use a configuration file Signs.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = 'http://signs2.bioinfo.cnio.es'
        ##self.server_url = self.conf_get('main', 'url')

    def test1(self):
        server_url = self.server_url

        self.get(server_url + "/",
            description="Get /")

        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./test1/mini.lung.covar.txt")],
            ['time', Upload("./test1/mini.lung.surv.txt")],
            ['event', Upload("./test1/mini.lung.event.txt")],
##            ['validation', 'on'],
            ['validationcovariate', Upload("./test1/empty.txt")],
            ['validationtime', Upload("./test1/empty.txt")],
            ['validationevent', Upload("./test1/empty.txt")],
            ['methodSurv', 'FCMS'],
            ['Minp', '0.1'],
            ['MaxSize', '100'],
            ['MinSize', '10'],
            ['MinCor', '0.5'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="Post /cgi-bin/signsR.cgi")

        final_output = 'No groups that meet the p, minimum correlation and size restrictions.'
        common_part(self, final_output)



    def test2(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------


        self.get(server_url + "/",
            description="Get /")

        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./test2/mini.lung.covar.txt")],
            ['time', Upload("./test2/mini.lung.surv.txt")],
            ['event', Upload("./test2/mini.lung.event.txt")],
            ['validation', 'on'],
            ['validationcovariate', Upload("./test2/empty.txt")],
            ['validationtime', Upload("./test2/empty.txt")],
            ['validationevent', Upload("./test2/empty.txt")],
            ['methodSurv', 'FCMS'],
            ['Minp', '0.1'],
            ['MaxSize', '100'],
            ['MinSize', '10'],
            ['MinCor', '0.5'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="Post /cgi-bin/signsR.cgi")

        final_output = '<h1> SignS INPUT ERROR </h1>\n<p> validationcovariate  file has size 0 </p>'
        common_part(self, final_output, MAX_running_time = 30)


    def test_division_by_zero(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------


        self.get(server_url + "/",
            description="Get /")

        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./division.by.zero/covariate")],
            ['time', Upload("./division.by.zero/time")],
            ['event', Upload("./division.by.zero/event")],
#            ['validation', 'on'],
#            ['validationcovariate', Upload("./test2/empty.txt")],
#            ['validationtime', Upload("./test2/empty.txt")],
#            ['validationevent', Upload("./test2/empty.txt")],
            ['methodSurv', 'FCMS'],
            ['Minp', '0.5'],
            ['MaxSize', '100'],
            ['MinSize', '2'],
            ['MinCor', '0.2'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="Division by zero")

        MAX_running_time = 3600 * 6 

        final_output = '<p> Total of  2 signature components selected'
        common_part(self, final_output)

#     def test3(self):
#         # The description should be set in the configuration file
#         server_url = self.server_url
#         # begin of test ---------------------------------------------


#         self.get(server_url + "/",
#             description="Get /")

#         self.post(server_url + "/cgi-bin/signsR.cgi", params=[
#             ['covariate', Upload("./test3/covar")],
#             ['time', Upload("./test3/time")],
#             ['event', Upload("./test3/event")],
# #            ['validation', 'on'],
# #            ['validationcovariate', Upload("./test2/empty.txt")],
# #            ['validationtime', Upload("./test2/empty.txt")],
# #            ['validationevent', Upload("./test2/empty.txt")],
#             ['methodSurv', 'FCMS'],
#             ['Minp', '0.5'],
#             ['MaxSize', '100'],
#             ['MinSize', '2'],
#             ['MinCor', '0.2'],
#             ['organism', 'None'],
#             ['idtype', 'None']],
#             description="Division by zero")
#         final_output = '<p> Total of  2 signature components selected and  72 genes.</p>'
#         common_part(self, final_output)

    def test3_validation(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./test3/covar")],
            ['time', Upload("./test3/time")],
            ['event', Upload("./test3/event")],
            ['validation', 'on'],
            ['validationcovariate', Upload("./test3/covar")],
            ['validationtime', Upload("./test3/time")],
            ['validationevent', Upload("./test3/event")],
            ['methodSurv', 'FCMS'],
            ['Minp', '0.7'],
            ['MaxSize', '100'],
            ['MinSize', '2'],
            ['MinCor', '0.4'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="Division by zero")

        final_output = '<p> Total of  2 signature components selected and  63 genes.</p>'
        common_part(self, final_output)

    def test4_validation(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./test3/covar")],
            ['time', Upload("./test3/time")],
            ['event', Upload("./test3/event")],
            ['validation', 'on'],
            ['validationcovariate', Upload("./test3/covar")],
            ['validationtime', Upload("./test3/validation.time")],
            ['validationevent', Upload("./test3/validation.event")],
            ['methodSurv', 'FCMS'],
            ['Minp', '0.7'],
            ['MaxSize', '100'],
            ['MinSize', '2'],
            ['MinCor', '0.4'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="Identical time and status validation")

        final_output = 'User Input ERROR'
        common_part(self, final_output)


    def test_identical(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./test3/covar")],
            ['time', Upload("./test3/validation.time")],
            ['event', Upload("./test3/validation.event")],
            ['methodSurv', 'FCMS'],
            ['Minp', '0.7'],
            ['MaxSize', '100'],
            ['MinSize', '2'],
            ['MinCor', '0.4'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="Identical time and status")

        final_output = 'User Input ERROR'
        common_part(self, final_output)



    def test_apache2(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./apache-prob2/covariate")],
            ['time', Upload("./apache-prob2/class_labels")],
            ['event', Upload("./apache-prob2/survival_time")],
            ['methodSurv', 'FCMS'],
            ['Minp', '0.7'],
            ['MaxSize', '100'],
            ['MinSize', '2'],
            ['MinCor', '0.4'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="More than one Name line")
        final_output = 'You have more than one line with #Name (or #NAME or #name), in the data matrix '
        common_part(self, final_output)

    def test_apache3(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./apache-prob3/covariate")],
            ['time', Upload("./apache-prob3/class_labels")],
            ['event', Upload("./apache-prob3/survival_time")],
            ['methodSurv', 'FCMS'],
            ['Minp', '0.05'],
            ['MaxSize', '100'],
            ['MinSize', '5'],
            ['MinCor', '0.8'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description=' Name with "')
        final_output = 'Total of  1 signature components selected and  8 genes'
        common_part(self, final_output)



    def test_signs_pals(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./names-genes/covariate")],
            ['time', Upload("./names-genes/time")],
            ['event', Upload("./names-genes/event")],
            ['methodSurv', 'FCMS'],
            ['Minp', '0.1'],
            ['MaxSize', '100'],
            ['MinSize', '10'],
            ['MinCor', '0.5'],
            ['organism', 'Mm'],
            ['idtype', 'ug']],
            description=' Test PaLS-valid output')
        final_output = 'Total of  2 signature components selected and  26 genes.'
        common_part(self, final_output)


    def test_signs_pals_should_not_crash(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./names-genes/covariate")],
            ['time', Upload("./names-genes/event")],
            ['event', Upload("./names-genes/time")],
            ['methodSurv', 'FCMS'],
            ['Minp', '0.1'],
            ['MaxSize', '100'],
            ['MinSize', '10'],
            ['MinCor', '0.5'],
            ['organism', 'Mm'],
            ['idtype', 'ug']],
            description=' Used to cause an "Surv(time, event) : Invalid status value"')
        final_output = 'Your status data is not valid; can only be 0 or 1'
        common_part(self, final_output)


    def testTGD1(self):
        server_url = self.server_url

        self.get(server_url + "/",
            description="Get /")

        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./test1/mini.lung.covar.txt")],
            ['time', Upload("./test1/mini.lung.surv.txt")],
            ['event', Upload("./test1/mini.lung.event.txt")],
##            ['validation', 'on'],
            ['validationcovariate', Upload("./test1/empty.txt")],
            ['validationtime', Upload("./test1/empty.txt")],
            ['validationevent', Upload("./test1/empty.txt")],
            ['methodSurv', 'TGD'],
            ['maxiter', '10'],
            ['epi', '5e-06'],
            ['tau', '.90'],
            ['MinCor', '0.5'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="Post /cgi-bin/signsR.cgi")

        final_output = 'maxiter smaller than smallest accepted value'
        common_part(self, final_output)



    def testTGD2(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------


        self.get(server_url + "/",
            description="Get /")

        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./test2/mini.lung.covar.txt")],
            ['time', Upload("./test2/mini.lung.surv.txt")],
            ['event', Upload("./test2/mini.lung.event.txt")],
            ['validation', 'on'],
            ['validationcovariate', Upload("./test2/empty.txt")],
            ['validationtime', Upload("./test2/empty.txt")],
            ['validationevent', Upload("./test2/empty.txt")],
            ['methodSurv', 'TGD'],
            ['maxiter', '3000'],
            ['epi', '5e-06'],
            ['tau', '.99'],
            ['MinCor', '0.5'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="Post /cgi-bin/signsR.cgi")

        final_output = '<h1> SignS INPUT ERROR </h1>\n<p> validationcovariate  file has size 0 </p>'
        common_part(self, final_output, MAX_running_time = 30)


    def testTGD_division_by_zero(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------


        self.get(server_url + "/",
            description="Get /")

        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./division.by.zero/covariate")],
            ['time', Upload("./division.by.zero/time")],
            ['event', Upload("./division.by.zero/event")],
#            ['validation', 'on'],
#            ['validationcovariate', Upload("./test2/empty.txt")],
#            ['validationtime', Upload("./test2/empty.txt")],
#            ['validationevent', Upload("./test2/empty.txt")],
            ['methodSurv', 'TGD'],
            ['maxiter', '5000'],
            ['epi', '5e-08'],
            ['tau', '0.9'],
            ['MinCor', '0.2'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="Division by zero")

        MAX_running_time = 3600 * 6 

        final_output = 'Selected genes (ordered by decreasing value of their coefficient)'
        common_part(self, final_output)


    def testTGD3_validation(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./test3/covar")],
            ['time', Upload("./test3/time")],
            ['event', Upload("./test3/event")],
            ['validation', 'on'],
            ['validationcovariate', Upload("./test3/covar")],
            ['validationtime', Upload("./test3/time")],
            ['validationevent', Upload("./test3/event")],
            ['methodSurv', 'TGD'],
            ['maxiter', '10000'],
            ['epi', '5e-06'],
            ['tau', '1'],
            ['MinCor', '0.4'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="Division by zero")

        final_output = 'Selected genes (ordered by decreasing value of their coefficient)'
        common_part(self, final_output)


    def testTGD_apache2(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./apache-prob2/covariate")],
            ['time', Upload("./apache-prob2/class_labels")],
            ['event', Upload("./apache-prob2/survival_time")],
            ['methodSurv', 'TGD'],
            ['maxiter', '5500'],
            ['epi', '6e-05'],
            ['tau', '0.99'],
            ['MinCor', '0.4'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="More than one Name line")
        final_output = 'You have more than one line with #Name (or #NAME or #name), in the data matrix '
        common_part(self, final_output)

    def testTGD_apache3(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./apache-prob3/covariate")],
            ['time', Upload("./apache-prob3/class_labels")],
            ['event', Upload("./apache-prob3/survival_time")],
            ['methodSurv', 'TGD'],
            ['maxiter', '5000'],
            ['epi', '5e-05'],
            ['tau', '.9'],
            ['MinCor', '0.8'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description=' Name with "')
        final_output = 'Selected genes (ordered by decreasing value of their coefficient)'
        common_part(self, final_output)



    def testTGD_signs_pals(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./names-genes/covariate")],
            ['time', Upload("./names-genes/time")],
            ['event', Upload("./names-genes/event")],
            ['methodSurv', 'TGD'],
            ['maxiter', '6000'],
            ['epi', '6e-06'],
            ['tau', '.90'],
            ['MinCor', '0.5'],
            ['organism', 'Mm'],
            ['idtype', 'ug']],
            description=' Test PaLS-valid output')
        final_output = 'Selected genes (ordered by decreasing value of their coefficient)'
        common_part(self, final_output)


    def testTGD_signs_pals_should_not_crash(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./names-genes/covariate")],
            ['time', Upload("./names-genes/event")],
            ['event', Upload("./names-genes/time")],
            ['methodSurv', 'TGD'],
            ['maxiter', '4000'],
            ['epi', '5e-06'],
            ['tau', '0.9'],
            ['MinCor', '0.5'],
            ['organism', 'Mm'],
            ['idtype', 'ug']],
            description=' Used to cause an "Surv(time, event) : Invalid status value"')
        final_output = 'Your status data is not valid; can only be 0 or 1'
        common_part(self, final_output)



    def testcforest1(self):
        server_url = self.server_url

        self.get(server_url + "/",
            description="Get /")

        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./test1/mini.lung.covar.txt")],
            ['time', Upload("./test1/mini.lung.surv.txt")],
            ['event', Upload("./test1/mini.lung.event.txt")],
##            ['validation', 'on'],
            ['validationcovariate', Upload("./test1/empty.txt")],
            ['validationtime', Upload("./test1/empty.txt")],
            ['validationevent', Upload("./test1/empty.txt")],
            ['methodSurv', 'cforest'],
            ['ngenes', '1'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="Post /cgi-bin/signsR.cgi")

        final_output = 'ngenes smaller than smallest accepted value'
        common_part(self, final_output)



    def testcforest2(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------


        self.get(server_url + "/",
            description="Get /")

        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./test2/mini.lung.covar.txt")],
            ['time', Upload("./test2/mini.lung.surv.txt")],
            ['event', Upload("./test2/mini.lung.event.txt")],
            ['validation', 'on'],
            ['validationcovariate', Upload("./test2/empty.txt")],
            ['validationtime', Upload("./test2/empty.txt")],
            ['validationevent', Upload("./test2/empty.txt")],
            ['methodSurv', 'cforest'],
            ['ngenes', '3000'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="Post /cgi-bin/signsR.cgi")

        final_output = '<h1> SignS INPUT ERROR </h1>\n<p> validationcovariate  file has size 0 </p>'
        common_part(self, final_output, MAX_running_time = 30)


    def testcforest_division_by_zero(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------


        self.get(server_url + "/",
            description="Get /")

        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./division.by.zero/covariate")],
            ['time', Upload("./division.by.zero/time")],
            ['event', Upload("./division.by.zero/event")],
            ['methodSurv', 'cforest'],
            ['ngenes', '50'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="Division by zero")

        MAX_running_time = 3600 * 6 

        final_output = 'Genes selected in each of the cross-validation runs'
        common_part(self, final_output)


    def testcforest3_validation(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./test3/covar")],
            ['time', Upload("./test3/time")],
            ['event', Upload("./test3/event")],
            ['validation', 'on'],
            ['validationcovariate', Upload("./test3/covar")],
            ['validationtime', Upload("./test3/time")],
            ['validationevent', Upload("./test3/event")],
            ['methodSurv', 'cforest'],
            ['ngenes', '100'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="Division by zero")

        final_output = 'Genes selected in each of the cross-validation runs'
        common_part(self, final_output)


    def testcforest_apache2(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./apache-prob2/covariate")],
            ['time', Upload("./apache-prob2/class_labels")],
            ['event', Upload("./apache-prob2/survival_time")],
            ['methodSurv', 'cforest'],
            ['ngenes', '100'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="More than one Name line")
        final_output = 'You have more than one line with #Name (or #NAME or #name), in the data matrix '
        common_part(self, final_output)

    def testcforest_apache3(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./apache-prob3/covariate")],
            ['time', Upload("./apache-prob3/class_labels")],
            ['event', Upload("./apache-prob3/survival_time")],
            ['methodSurv', 'cforest'],
            ['ngenes', '200'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description=' Name with "')
        final_output = 'Genes selected in each of the cross-validation runs'
        common_part(self, final_output)



    def testcforest_signs_pals(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./names-genes/covariate")],
            ['time', Upload("./names-genes/time")],
            ['event', Upload("./names-genes/event")],
            ['methodSurv', 'cforest'],
            ['ngenes', '300'],
            ['organism', 'Mm'],
            ['idtype', 'ug']],
            description=' Test PaLS-valid output')
        final_output = 'Genes selected in each of the cross-validation runs'
        common_part(self, final_output)


    def testcforest_signs_pals_should_not_crash(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./names-genes/covariate")],
            ['time', Upload("./names-genes/event")],
            ['event', Upload("./names-genes/time")],
            ['methodSurv', 'cforest'],
            ['ngenes', '200'],
            ['organism', 'Mm'],
            ['idtype', 'ug']],
            description=' Used to cause an "Surv(time, event) : Invalid status value"')
        final_output = 'Your status data is not valid; can only be 0 or 1'
        common_part(self, final_output)



    def testglmboost2(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------


        self.get(server_url + "/",
            description="Get /")

        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./test2/mini.lung.covar.txt")],
            ['time', Upload("./test2/mini.lung.surv.txt")],
            ['event', Upload("./test2/mini.lung.event.txt")],
            ['validation', 'on'],
            ['validationcovariate', Upload("./test2/empty.txt")],
            ['validationtime', Upload("./test2/empty.txt")],
            ['validationevent', Upload("./test2/empty.txt")],
            ['methodSurv', 'glmboost'],
            ['ngenes', '3000'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="Post /cgi-bin/signsR.cgi")

        final_output = '<h1> SignS INPUT ERROR </h1>\n<p> validationcovariate  file has size 0 </p>'
        common_part(self, final_output, MAX_running_time = 30)


    def testglmboost_division_by_zero(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------


        self.get(server_url + "/",
            description="Get /")

        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./division.by.zero/covariate")],
            ['time', Upload("./division.by.zero/time")],
            ['event', Upload("./division.by.zero/event")],
            ['methodSurv', 'glmboost'],
            ['ngenes', '50'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="Division by zero")

        MAX_running_time = 3600 * 6 

        final_output = 'Genes selected in each of the cross-validation runs'
        common_part(self, final_output)


    def testglmboost3_validation(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./test3/covar")],
            ['time', Upload("./test3/time")],
            ['event', Upload("./test3/event")],
            ['validation', 'on'],
            ['validationcovariate', Upload("./test3/covar")],
            ['validationtime', Upload("./test3/time")],
            ['validationevent', Upload("./test3/event")],
            ['methodSurv', 'glmboost'],
            ['ngenes', '100'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="Division by zero")

        final_output = 'Genes selected in each of the cross-validation runs'
        common_part(self, final_output)


    def testglmboost_apache2(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./apache-prob2/covariate")],
            ['time', Upload("./apache-prob2/class_labels")],
            ['event', Upload("./apache-prob2/survival_time")],
            ['methodSurv', 'glmboost'],
            ['ngenes', '100'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="More than one Name line")
        final_output = 'You have more than one line with #Name (or #NAME or #name), in the data matrix '
        common_part(self, final_output)

    def testglmboost_apache3(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./apache-prob3/covariate")],
            ['time', Upload("./apache-prob3/class_labels")],
            ['event', Upload("./apache-prob3/survival_time")],
            ['methodSurv', 'glmboost'],
            ['ngenes', '200'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description=' Name with "')
        final_output = 'Genes selected in each of the cross-validation runs'
        common_part(self, final_output)



    def testglmboost_signs_pals(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./names-genes/covariate")],
            ['time', Upload("./names-genes/time")],
            ['event', Upload("./names-genes/event")],
            ['methodSurv', 'glmboost'],
            ['ngenes', '300'],
            ['organism', 'Mm'],
            ['idtype', 'ug']],
            description=' Test PaLS-valid output')
        final_output = 'Genes selected in each of the cross-validation runs'
        common_part(self, final_output)


    def testglmboost_signs_pals_should_not_crash(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/signsR.cgi", params=[
            ['covariate', Upload("./names-genes/covariate")],
            ['time', Upload("./names-genes/event")],
            ['event', Upload("./names-genes/time")],
            ['methodSurv', 'glmboost'],
            ['ngenes', '200'],
            ['organism', 'Mm'],
            ['idtype', 'ug']],
            description=' Used to cause an "Surv(time, event) : Invalid status value"')
        final_output = 'Your status data is not valid; can only be 0 or 1'
        common_part(self, final_output)




    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")

if __name__ in ('main', '__main__'):
     unittest.main()
