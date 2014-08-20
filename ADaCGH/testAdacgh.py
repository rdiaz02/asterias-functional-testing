# -*- coding: iso-8859-15 -*-
""" ADaCGH testing: user interface and numerical results.
"""

import time
import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase
from webunit.utility import Upload
from urllib import urlretrieve

auto_refresh_string = 'This is an autorefreshing page'
MAX_running_time = 3600 * 1 

def common_part(self, final_output,                
                MAX_running_time = 3600,
                auto_refresh_string = auto_refresh_string):
    """ Common to all tests: take care of autorefreshing and following
    links till done. Then, verify expected string in output."""
  
    server_url = self.server_url
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
    print self.getLastUrl()	
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
        self.server_url = 'http://adacgh.bioinfo.cnio.es'
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
            ['DNA.merge', 'Yes'],
            ['centering', 'Median'],
            ['methodaCGH', 'CBS'],
            ['DNA.smooth.region', '2'],
            ['DNA.outlier.SD.scale', '4'],
            ['DNA.smooth.SD.scale', '2'],
            ['DNA.trim', '0.025'],
            ['DNA.copy.alpha', '0.01'],
            ['DNA.nperm', '10000'],
            ['DNA.kmax', '25'],
            ['DNA.nmin', '200'],
            ['DNA.overlap', '0.25'],
            ['DNA.undo.prune', '0.05'],
            ['Wave.minDiff', '0.25'],
            ['PSW.nIter', '1000'],
            ['PSW.prec', '100'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="CBS")
        final_output = 'DNA.smooth.region'
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
            ['DNA.merge', 'No'],
            ['centering', 'Median'],
            ['methodaCGH', 'CBS'],
            ['DNA.smooth.region', '2'],
            ['DNA.outlier.SD.scale', '4'],
            ['DNA.smooth.SD.scale', '2'],
            ['DNA.trim', '0.025'],
            ['DNA.copy.alpha', '0.01'],
            ['DNA.nperm', '10000'],
            ['DNA.kmax', '25'],
            ['DNA.nmin', '200'],
            ['DNA.overlap', '0.25'],
            ['DNA.undo.prune', '0.05'],
            ['Wave.minDiff', '0.25'],
            ['PSW.nIter', '1000'],
            ['PSW.prec', '100'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="CBS")
        final_output = 'DNA.smooth.region'
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
            ['DNA.merge', 'Yes'],
            ['centering', 'Median'],
            ['DNA.smooth.region', '2'],
            ['DNA.outlier.SD.scale', '4'],
            ['DNA.smooth.SD.scale', '2'],
            ['DNA.trim', '0.025'],
            ['DNA.copy.alpha', '0.01'],
            ['DNA.nperm', '10000'],
            ['DNA.kmax', '25'],
            ['DNA.nmin', '200'],
            ['DNA.overlap', '0.25'],
            ['DNA.undo.prune', '0.05'],
            ['methodaCGH', 'WS'],
            ['Wave.minDiff', '0.25'],
            ['PSW.nIter', '1000'],
            ['PSW.prec', '100'],
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
            ['DNA.merge', 'Yes'],
            ['centering', 'Median'],
            ['DNA.smooth.region', '2'],
            ['DNA.outlier.SD.scale', '4'],
            ['DNA.smooth.SD.scale', '2'],
            ['DNA.trim', '0.025'],
            ['DNA.copy.alpha', '0.01'],
            ['DNA.nperm', '10000'],
            ['DNA.kmax', '25'],
            ['DNA.nmin', '200'],
            ['DNA.overlap', '0.25'],
            ['DNA.undo.prune', '0.05'],
            ['Wave.minDiff', '0.25'],
            ['methodaCGH', 'PSW'],
            ['PSW.nIter', '1000'],
            ['PSW.prec', '100'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="PSW")
        final_output = 'PSW.nIter'
        common_part(self, final_output)


    def test4(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['twofiles', 'Two.files'],
            ['acghData', Upload("TWO.files.acghdata")],
            ['positionInfo', Upload("TWO.files.positions")],
            ['acghAndPosition', Upload("empty.txt")],
            ['DNA.merge', 'Yes'],
            ['centering', 'Mean'],
            ['DNA.smooth.region', '2'],
            ['DNA.outlier.SD.scale', '4'],
            ['DNA.smooth.SD.scale', '2'],
            ['DNA.trim', '0.025'],
            ['DNA.copy.alpha', '0.01'],
            ['DNA.nperm', '10000'],
            ['DNA.kmax', '25'],
            ['DNA.nmin', '200'],
            ['DNA.overlap', '0.25'],
            ['DNA.undo.prune', '0.05'],
            ['Wave.minDiff', '0.25'],
            ['PSW.nIter', '1000'],
            ['PSW.prec', '100'],
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
            ['DNA.merge', 'Yes'],
            ['centering', 'Mean'],
            ['DNA.smooth.region', '2'],
            ['DNA.outlier.SD.scale', '4'],
            ['DNA.smooth.SD.scale', '2'],
            ['DNA.trim', '0.025'],
            ['DNA.copy.alpha', '0.01'],
            ['DNA.nperm', '10000'],
            ['DNA.kmax', '25'],
            ['DNA.nmin', '200'],
            ['DNA.overlap', '0.25'],
            ['DNA.undo.prune', '0.05'],
            ['Wave.minDiff', '0.25'],
            ['PSW.nIter', '1000'],
            ['PSW.prec', '100'],
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
            ['DNA.merge', 'Yes'],
            ['centering', 'Mean'],
            ['DNA.smooth.region', '2'],
            ['DNA.outlier.SD.scale', '4'],
            ['DNA.smooth.SD.scale', '2'],
            ['DNA.trim', '0.025'],
            ['DNA.copy.alpha', '0.01'],
            ['DNA.nperm', '10000'],
            ['DNA.kmax', '25'],
            ['DNA.nmin', '200'],
            ['DNA.overlap', '0.25'],
            ['DNA.undo.prune', '0.05'],
            ['Wave.minDiff', '0.25'],
            ['PSW.nIter', '1000'],
            ['PSW.prec', '100'],
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
            ['DNA.merge', 'Yes'],
            ['centering', 'Median'],
            ['methodaCGH', 'CBS'],
            ['DNA.smooth.region', '2'],
            ['DNA.outlier.SD.scale', '4'],
            ['DNA.smooth.SD.scale', '2'],
            ['DNA.trim', '0.025'],
            ['DNA.copy.alpha', '0.01'],
            ['DNA.nperm', '10000'],
            ['DNA.kmax', '25'],
            ['DNA.nmin', '200'],
            ['DNA.overlap', '0.25'],
            ['DNA.undo.prune', '0.05'],
            ['Wave.minDiff', '0.25'],
            ['PSW.nIter', '1000'],
            ['PSW.prec', '100'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="CBS, single array")
        final_output = 'DNA.smooth.region'
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
            ['DNA.merge', 'No'],
            ['centering', 'Median'],
            ['methodaCGH', 'CBS'],
            ['DNA.smooth.region', '2'],
            ['DNA.outlier.SD.scale', '4'],
            ['DNA.smooth.SD.scale', '2'],
            ['DNA.trim', '0.025'],
            ['DNA.copy.alpha', '0.01'],
            ['DNA.nperm', '10000'],
            ['DNA.kmax', '25'],
            ['DNA.nmin', '200'],
            ['DNA.overlap', '0.25'],
            ['DNA.undo.prune', '0.05'],
            ['Wave.minDiff', '0.25'],
            ['PSW.nIter', '1000'],
            ['PSW.prec', '100'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'Hs'],
            ['idtype', 'ug']],
            description="CBS, single array")
        final_output = 'DNA.smooth.region'
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
            ['DNA.merge', 'Yes'],
            ['centering', 'Median'],
            ['methodaCGH', 'WS'],
            ['DNA.smooth.region', '2'],
            ['DNA.outlier.SD.scale', '4'],
            ['DNA.smooth.SD.scale', '2'],
            ['DNA.trim', '0.025'],
            ['DNA.copy.alpha', '0.01'],
            ['DNA.nperm', '10000'],
            ['DNA.kmax', '25'],
            ['DNA.nmin', '200'],
            ['DNA.overlap', '0.25'],
            ['DNA.undo.prune', '0.05'],
            ['Wave.minDiff', '0.25'],
            ['PSW.nIter', '1000'],
            ['PSW.prec', '100'],
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
            ['DNA.merge', 'Yes'],
            ['centering', 'Median'],
            ['methodaCGH', 'PSW'],
            ['DNA.smooth.region', '2'],
            ['DNA.outlier.SD.scale', '4'],
            ['DNA.smooth.SD.scale', '2'],
            ['DNA.trim', '0.025'],
            ['DNA.copy.alpha', '0.01'],
            ['DNA.nperm', '10000'],
            ['DNA.kmax', '25'],
            ['DNA.nmin', '200'],
            ['DNA.overlap', '0.25'],
            ['DNA.undo.prune', '0.05'],
            ['Wave.minDiff', '0.25'],
            ['PSW.nIter', '1000'],
            ['PSW.prec', '100'],
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
            ['DNA.merge', 'Yes'],
            ['centering', 'Median'],
            ['DNA.smooth.region', '2'],
            ['DNA.outlier.SD.scale', '4'],
            ['DNA.smooth.SD.scale', '2'],
            ['DNA.trim', '0.025'],
            ['DNA.copy.alpha', '0.01'],
            ['DNA.nperm', '10000'],
            ['DNA.kmax', '25'],
            ['DNA.nmin', '200'],
            ['DNA.overlap', '0.25'],
            ['DNA.undo.prune', '0.05'],
            ['methodaCGH', 'WS'],
            ['Wave.minDiff', '0.25'],
            ['PSW.nIter', '1000'],
            ['PSW.prec', '100'],
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
            ['DNA.merge', 'Yes'],
            ['centering', 'Median'],
            ['DNA.smooth.region', '2'],
            ['DNA.outlier.SD.scale', '4'],
            ['DNA.smooth.SD.scale', '2'],
            ['DNA.trim', '0.025'],
            ['DNA.copy.alpha', '0.01'],
            ['DNA.nperm', '10000'],
            ['DNA.kmax', '25'],
            ['DNA.nmin', '200'],
            ['DNA.overlap', '0.25'],
            ['DNA.undo.prune', '0.05'],
            ['Wave.minDiff', '0.25'],
            ['methodaCGH', 'PSW'],
            ['PSW.nIter', '1000'],
            ['PSW.prec', '100'],
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
            ['acghData', Upload("acghData.KMLau")],
            ['positionInfo', Upload("positionInfo.KMLau")],
            ['acghAndPosition', Upload("empty.txt")],
            ['DNA.merge', 'Yes'],
            ['centering', 'Median'],
            ['DNA.smooth.region', '2'],
            ['DNA.outlier.SD.scale', '4'],
            ['DNA.smooth.SD.scale', '2'],
            ['DNA.trim', '0.025'],
            ['DNA.copy.alpha', '0.01'],
            ['DNA.nperm', '10000'],
            ['DNA.kmax', '25'],
            ['DNA.nmin', '200'],
            ['DNA.overlap', '0.25'],
            ['DNA.undo.prune', '0.05'],
            ['Wave.minDiff', '0.25'],
            ['methodaCGH', 'CBS'],
            ['PSW.nIter', '1000'],
            ['PSW.prec', '100'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="Position Info with extra blank fields at end")
        final_output = 'DNA.smooth.region'
        common_part(self, final_output)

    def testKMLau_b(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['twofiles', 'Two.files'],
            ['acghData', Upload("acghData.KMLau")],
            ['positionInfo', Upload("positionInfo.KMLau")],
            ['acghAndPosition', Upload("empty.txt")],
            ['DNA.merge', 'No'],
            ['centering', 'Median'],
            ['DNA.smooth.region', '2'],
            ['DNA.outlier.SD.scale', '4'],
            ['DNA.smooth.SD.scale', '2'],
            ['DNA.trim', '0.025'],
            ['DNA.copy.alpha', '0.01'],
            ['DNA.nperm', '10000'],
            ['DNA.kmax', '25'],
            ['DNA.nmin', '200'],
            ['DNA.overlap', '0.25'],
            ['DNA.undo.prune', '0.05'],
            ['Wave.minDiff', '0.25'],
            ['methodaCGH', 'CBS'],
            ['PSW.nIter', '1000'],
            ['PSW.prec', '100'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['MCR.gapAllowed', '500'],
            ['MCR.alteredLow', '0.03'],
            ['MCR.alteredHigh', '0.97'],
            ['MCR.recurrence', '75'],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="Position Info with extra blank fields at end")
        final_output = 'DNA.smooth.region'
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
            ['DNA.merge', 'Yes'],
            ['centering', 'None'],
            ['DNA.smooth.region', '2'],
            ['DNA.outlier.SD.scale', '4'],
            ['DNA.smooth.SD.scale', '2'],
            ['DNA.trim', '0.025'],
            ['DNA.copy.alpha', '0.01'],
            ['DNA.nperm', '10000'],
            ['DNA.kmax', '25'],
            ['DNA.nmin', '200'],
            ['DNA.overlap', '0.25'],
            ['DNA.undo.prune', '0.05'],
            ['Wave.minDiff', '0.25'],
            ['methodaCGH', 'CBS'],
            ['PSW.nIter', '1000'],
            ['PSW.prec', '100'],
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
        final_output = '<tr><td>3</td><td>3</td><td>sample1,sample2</td><td><div align=right> 875</div></td><td><div align=right>1035</div></td></tr>'
        common_part(self, final_output)
        final_output = '<tr><td>5</td><td>5</td><td>sample1,sample2</td><td><div align=right>1230</div></td><td><div align=right>1258</div></td></tr>'
        common_part(self, final_output)
        final_output = '<tr><td>13</td><td>13</td><td>sample1,sample3</td><td><div align=right>3070</div></td><td><div align=right>3157</div></td></tr>'
        common_part(self, final_output)

    def testMCRb(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['twofiles', 'One.file'],
            ['acghData', Upload("empty.txt")],
            ['positionInfo', Upload("empty.txt")],
            ['acghAndPosition', Upload("mcr.example.txt")],
            ['DNA.merge', 'No'],
            ['centering', 'None'],
            ['DNA.smooth.region', '2'],
            ['DNA.outlier.SD.scale', '4'],
            ['DNA.smooth.SD.scale', '2'],
            ['DNA.trim', '0.025'],
            ['DNA.copy.alpha', '0.01'],
            ['DNA.nperm', '10000'],
            ['DNA.kmax', '25'],
            ['DNA.nmin', '200'],
            ['DNA.overlap', '0.25'],
            ['DNA.undo.prune', '0.05'],
            ['Wave.minDiff', '0.25'],
            ['methodaCGH', 'CBS'],
            ['PSW.nIter', '1000'],
            ['PSW.prec', '100'],
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
        final_output = '<tr><td>3</td><td>3</td><td>sample1,sample2</td><td><div align=right> 875</div></td><td><div align=right>1035</div></td></tr>'
        common_part(self, final_output)
        final_output = '<tr><td>5</td><td>5</td><td>sample1,sample2</td><td><div align=right>1230</div></td><td><div align=right>1258</div></td></tr>'
        common_part(self, final_output)
        final_output = '<tr><td>13</td><td>13</td><td>sample1,sample3</td><td><div align=right>3070</div></td><td><div align=right>3157</div></td></tr>'
        common_part(self, final_output)


    def fail1(self):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
            ['twofiles', 'Two.files'],
            ['acghData', Upload("Adacgh.conf")],
            ['positionInfo', Upload("Adacgh.conf")],
            ['acghAndPosition', Upload("empty.txt")],
            ['DNA.merge', 'No'],
            ['centering', 'None'],
            ['DNA.smooth.region', '2'],
            ['DNA.outlier.SD.scale', '4'],
            ['DNA.smooth.SD.scale', '2'],
            ['DNA.trim', '0.025'],
            ['DNA.copy.alpha', '0.01'],
            ['DNA.nperm', '10000'],
            ['DNA.kmax', '25'],
            ['DNA.nmin', '200'],
            ['DNA.overlap', '0.25'],
            ['DNA.undo.prune', '0.05'],
            ['Wave.minDiff', '0.25'],
            ['methodaCGH', 'CBS'],
            ['PSW.nIter', '1000'],
            ['PSW.prec', '100'],
            ['PSW.p.crit', '0.15'],
            ['ACE.fdr', '0.15'],
            ['organism', 'None'],
            ['idtype', 'None'],
            ['MCR.gain', '0.2'],
            ['MCR.loss', '-0.2']
            ],
            description="Should lead to error msg")
        final_output =  'The acgh data file is not of the appropriate format'
        common_part(self, final_output)


### The basic infrastructure is here, but testing needs to be done by hand;
        ### there is a lot of intertest varation in number of segments,
        ### which makes it extremely hard to automate tests.
        ### The twelve runs on 2006-12-18 worked OK.

#     def testCBS_paral(self):
#         server_url = self.server_url
#         self.get(server_url + "/",
#             description="Get /")
#         self.post(server_url + "/cgi-bin/adacghR.cgi", params=[
#             ['acghData', Upload("empty.txt")],
#             ['positionInfo', Upload("empty.txt")],
#             ['twofiles', 'One.file'],
#             ['acghAndPosition', Upload("two.samp.shuffled.clean.one.file")],
#             ['DNA.merge', 'No'],
#             ['centering', 'None'],
#             ['methodaCGH', 'CBS'],
#             ['DNA.smooth.region', '2'],
#             ['DNA.outlier.SD.scale', '4'],
#             ['DNA.smooth.SD.scale', '2'],
#             ['DNA.trim', '0.025'],
#             ['DNA.copy.alpha', '0.01'],
#             ['DNA.nperm', '50000'],
#             ['DNA.kmax', '25'],
#             ['DNA.nmin', '200'],
#             ['DNA.overlap', '0.25'],
#             ['DNA.undo.prune', '0.05'],
#             ['Wave.minDiff', '0.25'],
#             ['PSW.nIter', '1000'],
#             ['PSW.prec', '100'],
#             ['PSW.p.crit', '0.15'],
#             ['ACE.fdr', '0.15'],
#             ['MCR.gapAllowed', '500'],
#             ['MCR.alteredLow', '0.03'],
#             ['MCR.alteredHigh', '0.97'],
#             ['MCR.recurrence', '75'],
#             ['organism', 'None'],
#             ['idtype', 'None']],
#             description="CBS; numerical of parallel")
#         final_output = 'DNA.smooth.region'
#         common_part(self, final_output)
#         url_before_get = self.getLastUrl()
#         urlretrieve(server_url +
#                     url_before_get.replace('results.html', '.RData'),
#                     filename = 'tmp.testCBS_paral.RData')
#         import rpy ## to verify numerical output
#          tmp = rpy.r('load("reference.testCBS_paral.RData")')
#          tmp = rpy.r('load("tmp.testCBS_paral.RData")')
#          tmp = rpy.r('fc2(segmented.output, segment.smoothed.CNA.object)')
#          if tmp == 'OK':
#              print 'OK'
#          else:
#              self.fail('testCBS_paral failed')

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")

if __name__ in ('main', '__main__'):
     unittest.main()
