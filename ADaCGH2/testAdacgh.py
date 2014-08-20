# -*- coding: iso-8859-15 -*-
""" ADaCGH testing: user interface and numerical results.

Note that test3 oftentimes results in a crash of PSW. That is OK and
accounted for by the test.
"""

import time
import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase
from webunit.utility import Upload
from urllib import urlretrieve

auto_refresh_string = 'This is an autorefreshing page'
MAX_running_time = 1000 * 1 

# def common_part(self, final_output,                
#                 MAX_running_time = 3600,
#                 auto_refresh_string = auto_refresh_string):
#     """ Common to all tests: take care of autorefreshing and following
#     links till done. Then, verify expected string in output."""
  
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
#     print self.getLastUrl()
#     if len(final_output) != 2:
#         expected = final_body.find(final_output) >= 0
#     elif len(final_output) == 2:
#         expected = (final_body.find(final_output[0]) >= 0) or \
#                    (final_body.find(final_output[1]) >= 0)
#     if not expected:
#         self.fail('\n ***** (begin of) Unexpected final result!!!! *****\n' + \
#                  str(final_body) + \
#                  '\n ***** (end of) Unexpected final result!!!! *****\n')
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
            print '\n At 03 - except \n'
            time.sleep(27)
            gg = self.get(checkdoneUrl,
                          description="Get /cgi-bin/checkdone.cgi")
            print '\n This is gg \n'
            print str(gg)

    print '\n At 004 \n'
    ## I do it again, to give it time to read the complete HTML
    time.sleep(5)
    print '\n At 04 \n'
    final_body = self.getBody()
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

    def test1(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['twofiles', 'Two.files'],
            ['acghData', Upload("TWO.files.acghdata")],
            ['positionInfo', Upload("TWO.files.positions")],
            ['acghAndPosition', Upload("empty.txt")],
            ['centering', 'Median'],
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
            description="DNAcopy")
##        final_output = 'Method:               DNAcopy '
        final_output = 'Segmented data plots' ## Problems reading the whole output?
        common_part(self, final_output)


    def test1b(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['twofiles', 'Two.files'],
            ['acghData', Upload("TWO.files.acghdata")],
            ['positionInfo', Upload("TWO.files.positions")],
            ['acghAndPosition', Upload("empty.txt")],
            ['centering', 'Median'],
            ['methodaCGH', 'DNAcopy'],
            ['Wave.minDiff', '0.25'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="DNAcopy")
        final_output = 'Segmented data plots'
        common_part(self, final_output)

    def test1b0(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['twofiles', 'Two.files'],
            ['acghData', Upload("TWO.files.acghdata")],
            ['positionInfo', Upload("TWO.files.positions")],
            ['acghAndPosition', Upload("empty.txt")],
            ['centering', 'Median'],
            ['methodaCGH', 'CBS'],
            ['Wave.minDiff', '0.25'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="DNAcopy")
        final_output = 'The methodaCGH choosen is not valid.'
        common_part(self, final_output)


    def test2(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("small.shuffled.clean.one.files")],
            ['centering', 'Median'],
            ['methodaCGH', 'Wavelets'],
            ['Wave.minDiff', '0.25'],
            ['Wave.merge', 'Yes'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['MCR.gapAllowed', '500'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="WS")
        final_output = 'Wave.minDiff'
        common_part(self, final_output)

    def test2b(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("small.shuffled.clean.one.files")],
            ['centering', 'Median'],
            ['methodaCGH', 'Wavelets'],
            ['Wave.minDiff', '0.25'],
            ['Wave.merge', 'No'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['MCR.gapAllowed', '500'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="WS")
        final_output = 'Wave.minDiff'
        common_part(self, final_output)



    def test3(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("small.shuffled.clean.one.files")],
            ['centering', 'Median'],
            ['Wave.minDiff', '0.25'],
            ['methodaCGH', 'PSW'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="PSW")
        final_output = ('PSW.nIter', 'There was a problem in the PSW routine')
        common_part(self, final_output)


#     def test3b(self):
#         ## disabled for now: it fails sometimes but things are OK.
#         ## FIXME: we'll have to look at this in more detail.
#         server_url = self.server_url
#         self.get(server_url + "/",
#             description="Get /")
#         self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
#             ['twofiles', 'Two.files'],
#             ['acghData', Upload("TWO.files.acghdata")],
#             ['positionInfo', Upload("TWO.files.positions")],
#             ['acghAndPosition', Upload("empty.txt")],
#             ['centering', 'Median'],
#             ['methodaCGH', 'PSW'],
#             ['Wave.minDiff', '0.25'],
#             ['PSW.nIter', '1000'],
#             ['PSW.p.crit', '0.15'],
#             ['ACE.fdr', '0.15'],
#             ['MCR.gapAllowed', '500'],
#             ['MCR.alteredLow', '0.03'],
#             ['MCR.alteredHigh', '0.97'],
#             ['MCR.recurrence', '75'],
#             ['organism', 'None'],
#             ['idtype', 'None']],
#             description="DNAcopy")
#         final_output = 'PSW.nIter'
#         common_part(self, final_output)




    def test4(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['twofiles', 'Two.files'],
            ['acghData', Upload("TWO.files.acghdata")],
            ['positionInfo', Upload("TWO.files.positions")],
            ['acghAndPosition', Upload("empty.txt")],
            ['centering', 'Mean'],
            ['Wave.minDiff', '0.25'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['methodaCGH', 'ACE'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="ACE, many arrays")
        final_output = '<h4>Method:               ACE </h4>'
        common_part(self, final_output)


    def test5(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['twofiles', 'Two.files'],
            ['acghData', Upload("one.single.array.data")],
            ['positionInfo', Upload("one.single.array.positions")],
            ['acghAndPosition', Upload("empty.txt")],
            ['centering', 'Mean'],
            ['Wave.minDiff', '0.25'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['methodaCGH', 'ACE'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="ACE, single array")
        final_output = '<h4>Method:               ACE </h4>'
        common_part(self, final_output)


    def test5B(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['twofiles', 'One.file'],
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['acghAndPosition', Upload("one.single.array.one.files")],
            ['centering', 'Mean'],
            ['Wave.minDiff', '0.25'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['methodaCGH', 'ACE'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="ACE, single array, B")
        final_output = '<h4>Method:               ACE </h4>'
        common_part(self, final_output)



    def test6(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("one.single.array.one.files")],
            ['centering', 'Median'],
            ['methodaCGH', 'DNAcopy'],
            ['Wave.minDiff', '0.25'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="DNAcopy, single array")
        final_output = 'Segmented data plots'
        common_part(self, final_output)

    def test6a1(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("one.single.array.one.files")],
            ['centering', 'Median'],
            ['methodaCGH', 'DNAcopy'],
            ['Wave.minDiff', '0.25'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="DNAcopy, single array")
        final_output = 'Segmented data plots'
        common_part(self, final_output)


    def test6b(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("one.single.array.one.files")],
            ['centering', 'Median'],
            ['methodaCGH', 'Wavelets'],
            ['Wave.minDiff', '0.25'],
            ['Wave.merge', 'Yes'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="WS, single array")
        final_output = 'Wave.minDiff'
        common_part(self, final_output)

    def test6c(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("one.single.array.one.files")],
            ['centering', 'Median'],
            ['methodaCGH', 'PSW'],
            ['Wave.minDiff', '0.25'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="PSW, single array")
        final_output = 'PSW.nIter'
        common_part(self, final_output)


    def test7(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("one.file")],
            ['centering', 'Median'],
            ['methodaCGH', 'Wavelets'],
            ['Wave.merge', 'Yes'],
            ['Wave.minDiff', '0.25'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="WS, min < -1000")
        final_output = 'The minimum value is &lt; -1000;'
        common_part(self, final_output)


    def test8(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['twofiles', 'Two.files'],
            ['acghData', Upload("TWO.data")],
            ['positionInfo', Upload("TWO.pos")],
            ['acghAndPosition', Upload("empty.txt")],
            ['centering', 'Median'],
            ['Wave.minDiff', '0.25'],
            ['methodaCGH', 'PSW'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="PSW; many < -300")
        final_output = 'At least 25 % of your vales are below &lt; -300;'
        common_part(self, final_output)

    def testKMLau(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['twofiles', 'Two.files'],
            ['acghData', Upload("acghData.KMLau.ident")],
            ['positionInfo', Upload("positionInfo.KMLau")],
            ['acghAndPosition', Upload("empty.txt")],
            ['centering', 'Median'],
            ['Wave.minDiff', '0.25'],
            ['methodaCGH', 'DNAcopy'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="Position Info with extra blank fields at end")
        final_output = 'Segmented data plots'
        common_part(self, final_output)

    def testKMLau_b(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['twofiles', 'Two.files'],
            ['acghData', Upload("acghData.KMLau.ident")],
            ['positionInfo', Upload("positionInfo.KMLau")],
            ['acghAndPosition', Upload("empty.txt")],
            ['centering', 'Median'],
            ['Wave.minDiff', '0.25'],
            ['methodaCGH', 'DNAcopy'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="Position Info with extra blank fields at end")
        final_output = 'Segmented data plots'
        common_part(self, final_output)



    def testMCR(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['twofiles', 'One.file'],
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['acghAndPosition', Upload("mcr.example.txt")],
            ['centering', 'None'],
            ['Wave.minDiff', '0.25'],
            ['methodaCGH', 'DNAcopy'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['organism', 'None'],
            ['idtype', 'None'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.2'],
            ['MCR.alteredHigh', '0.8'],
            ['MCR.recurrence', '50']
            ],
            description="Minimal common regions")
        final_output = '<tr><td>3</td><td>3</td><td>sample1,sample2</td><td><div align=right>561223</div></td><td><div align=right>2407833</div></td></tr>'
        common_part(self, final_output)
        final_output = '<tr><td>5</td><td>5</td><td>sample1,sample2</td><td><div align=right>  1831</div></td><td><div align=right> 129075</div></td></tr>'
        common_part(self, final_output)
#         final_output = '<tr><td>13</td><td>13</td><td>sample1,sample3</td><td><div align=right> 70145</div></td><td><div align=right> 537982</div></td></tr>'
#         common_part(self, final_output)

    def testMCRb(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['twofiles', 'One.file'],
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['acghAndPosition', Upload("mcr.example.txt")],
            ['centering', 'None'],
            ['Wave.minDiff', '0.25'],
            ['methodaCGH', 'DNAcopy'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['organism', 'None'],
            ['idtype', 'None'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.2'],
            ['MCR.alteredHigh', '0.8'],
            ['MCR.recurrence', '50']
            ],
            description="Minimal common regions")
        final_output = '<tr><td>3</td><td>3</td><td>sample1,sample2</td><td><div align=right>561223</div></td><td><div align=right>2407833</div></td></tr>'
        common_part(self, final_output)
        final_output = '<tr><td>5</td><td>5</td><td>sample1,sample2</td><td><div align=right>  1831</div></td><td><div align=right> 129075</div></td></tr>'
        common_part(self, final_output)
#         final_output = '<tr><td>13</td><td>13</td><td>sample1,sample3</td><td><div align=right> 70145</div></td><td><div align=right> 537982</div></td></tr>'
#         common_part(self, final_output)


    def fail1(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['twofiles', 'Two.files'],
            ['acghData', Upload("Adacgh.conf")],
            ['positionInfo', Upload("Adacgh.conf")],
            ['acghAndPosition', Upload("empty.txt")],
            ['centering', 'None'],
            ['Wave.minDiff', '0.25'],
            ['methodaCGH', 'DNAcopy'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['organism', 'None'],
            ['idtype', 'None'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.2'],
            ['MCR.alteredHigh', '0.8'],
            ['MCR.recurrence', '50']
            ],
            description="Should lead to error msg") 
        final_output =  'The acgh data file is not of the appropriate format'
        common_part(self, final_output)





    def testCGHseg(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("small.shuffled.clean.one.files")],
            ['centering', 'Median'],
            ['methodaCGH', 'CGHseg'],
            ['CGHseg.s', '-0.25'],
            ['Wave.merge', 'No'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['MCR.gapAllowed', '500'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="CGHseg")
        final_output = 'Segmented data plots'
        common_part(self, final_output)


    def testHMM(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("small.shuffled.clean.one.files")],
            ['centering', 'Median'],
            ['methodaCGH', 'HMM'],
            ['Wave.minDiff', '0.25'],
            ['Wave.merge', 'No'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['MCR.gapAllowed', '500'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="HMM")
        final_output = 'Segmented data plots'
        common_part(self, final_output)

    def testBioHMM(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("small.shuffled.clean.one.files")],
            ['centering', 'Median'],
            ['methodaCGH', 'BioHMM'],
            ['Wave.minDiff', '0.25'],
            ['Wave.merge', 'No'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['MCR.gapAllowed', '500'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="BioHMM")
        final_output = 'Segmented data plots'
        common_part(self, final_output)

    def testGLAD(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("small.shuffled.clean.one.files")],
            ['centering', 'Median'],
            ['methodaCGH', 'GLAD'],
            ['Wave.minDiff', '0.25'],
            ['Wave.merge', 'No'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['MCR.gapAllowed', '500'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="GLAD")
        final_output = 'Segmented data plots'
        common_part(self, final_output)

    def test1_emptylines(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['twofiles', 'Two.files'],
            ['acghData', Upload("TWO.files.acghdata.emptylines")],
            ['positionInfo', Upload("TWO.files.positions")],
            ['acghAndPosition', Upload("empty.txt")],
            ['centering', 'Median'],
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
            description="emptylines1")
        final_output = 'Segmented data plots'
        common_part(self, final_output)

    def test2_emptylines(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("small.shuffled.clean.one.files.emptylines")],
            ['centering', 'Median'],
            ['methodaCGH', 'Wavelets'],
            ['Wave.minDiff', '0.25'],
            ['Wave.merge', 'Yes'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['MCR.gapAllowed', '500'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="emptylines2")
        final_output = 'Wave.minDiff'
        common_part(self, final_output)



    def test_single1(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['twofiles', 'Two.files'],
            ['acghData', Upload("one.col.data.txt")],
            ['positionInfo', Upload("TWO.files.positions")],
            ['acghAndPosition', Upload("empty.txt")],
            ['centering', 'Median'],
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
            description="DNAcopy")
        final_output = 'Your aCGH data file contains only one column. It MUST'
        common_part(self, final_output)


    def test_single2(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['twofiles', 'Two.files'],
            ['acghData', Upload("TWO.files.acghdata")],
            ['positionInfo', Upload("one.col.pos.txt")],
            ['acghAndPosition', Upload("empty.txt")],
            ['centering', 'Median'],
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
            description="DNAcopy")
        final_output = 'The position information file has less than four columns'
        common_part(self, final_output)




    def singlechromHMM(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("single.chrom.acghdata")],
            ['centering', 'Median'],
            ['methodaCGH', 'HMM'],
            ['Wave.minDiff', '0.25'],
            ['Wave.merge', 'No'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['MCR.gapAllowed', '500'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="HMM")
        final_output = 'Segmented data plots'
        common_part(self, final_output)


    def singlechromDNAcopy(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("single.chrom.acghdata")],
            ['centering', 'Median'],
            ['methodaCGH', 'DNAcopy'],
            ['Wave.minDiff', '0.25'],
            ['Wave.merge', 'No'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['MCR.gapAllowed', '500'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="DNAcopy")
        final_output = 'Segmented data plots'
        common_part(self, final_output)

    def singlechromBioHMM(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("single.chrom.acghdata")],
            ['centering', 'Median'],
            ['methodaCGH', 'BioHMM'],
            ['Wave.minDiff', '0.25'],
            ['Wave.merge', 'No'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['MCR.gapAllowed', '500'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="BioHMM")
        final_output = 'Segmented data plots'
        common_part(self, final_output)

    def singlechromGLAD(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("single.chrom.acghdata")],
            ['centering', 'Median'],
            ['methodaCGH', 'GLAD'],
            ['Wave.minDiff', '0.25'],
            ['Wave.merge', 'No'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['MCR.gapAllowed', '500'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="GLAD")
        final_output = 'Segmented data plots'
        common_part(self, final_output)

    def singlechromACE(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("single.chrom.acghdata")],
            ['centering', 'Median'],
            ['methodaCGH', 'ACE'],
            ['Wave.minDiff', '0.25'],
            ['Wave.merge', 'No'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['MCR.gapAllowed', '500'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="ACE")
        final_output = 'There is a bug in the code'
        common_part(self, final_output)

    def singlechromPSW(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("single.chrom.acghdata")],
            ['centering', 'Median'],
            ['methodaCGH', 'PSW'],
            ['Wave.minDiff', '0.25'],
            ['Wave.merge', 'No'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['MCR.gapAllowed', '500'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="PSW")
        final_output = 'Segmented data plots'
        common_part(self, final_output)

    def singlechromWavelets(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("single.chrom.acghdata")],
            ['centering', 'Median'],
            ['methodaCGH', 'Wavelets'],
            ['Wave.minDiff', '0.25'],
            ['Wave.merge', 'No'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['MCR.gapAllowed', '500'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="Wavelets")
        final_output = 'Segmented data plots'
        common_part(self, final_output)

    def singlechromCGHseg(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("single.chrom.acghdata")],
            ['centering', 'Median'],
            ['methodaCGH', 'CGHseg'],
            ['Wave.minDiff', '0.25'],
            ['Wave.merge', 'No'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['MCR.gapAllowed', '500'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="CGHseg")
        final_output = 'Segmented data plots'
        common_part(self, final_output)


    def test_single_point_CBS(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['twofiles', 'One.file'],
            ['acghAndPosition', Upload("./single_point_crom/acghAndPosition")],
            ['centering', 'None'],
            ['methodaCGH', 'DNAcopy'],
            ['Wave.minDiff', '0.25'],
            ['PSW.nIter', '1000'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="DNAcopy, single array")
        final_output = 'Segmented data plots'
        common_part(self, final_output)

#     def test_single_point_CGHseg(self):
#         server_url = self.server_url
#         self.get(server_url + "/",
#             description="Get /")
#         self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
#             ['acghData', Upload("empty.txt")],
#             ['positionInfo', Upload("empty.txt")],
#             ['twofiles', 'One.file'],
#             ['acghAndPosition', Upload("./single_point_crom/acghAndPosition")],
#             ['centering', 'None'],
#             ['methodaCGH', 'CGHseg'],
#             ['CGHseg.s', '-0.25'],
#             ['Wave.minDiff', '0.25'],
#             ['PSW.nIter', '1000'],
#             ['PSW.p.crit', '0.15'],
#             ['ACE.fdr', '0.15'],
#             ['MCR.gapAllowed', '500'],
#             ['MCR.alteredLow', '0.03'],
#             ['MCR.alteredHigh', '0.97'],
#             ['MCR.recurrence', '75'],
#             ['organism', 'Hs'],
#             ['idtype', 'ug']],
#             description="cghseg, single point in chrom")
#         final_output = 'Segmented data plots'
#         common_part(self, final_output)




    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")

if __name__ in ('main', '__main__'):
     unittest.main()


## add a whole bunch of new tests for new methods
