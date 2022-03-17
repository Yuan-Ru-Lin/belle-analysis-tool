import os
import unittest
from anatool.submit import run_list, url_list, convert_to_stem


class TestSubmitter(unittest.TestCase):

    def test_run_list(self):
        runs_gen = run_list()
        self.assertEqual(next(runs_gen).__str__(), 'ex=7&rs=6&re=872')

    def test_url_list_mc(self):
        submit = url_list(data=False)
        self.assertEqual(next(submit),
            'http://bweb3/montecarlo.php?ex=7&rs=6&re=872&ty=evtgen-uds&dt=on_resonance&bl=caseB&st=10')
        for i in range(2000): next(submit)
        self.assertEqual(next(submit),
            'http://bweb3/montecarlo.php?ex=51&rs=1725&re=1756&ty=evtgen-charm&dt=on_resonance&bl=caseB&st=0')

    def test_url_list_data(self):
        submit = url_list(data=True)
        self.assertEqual(next(submit),
            'http://bweb3/mdst.php?ex=7&rs=6&re=872&skm=HadronB&dt=on_resonance&bl=caseB')
        for i in range(499): next(submit)
        self.assertEqual(next(submit),
            'http://bweb3/mdst.php?ex=51&rs=1725&re=1756&skm=HadronBJ&dt=on_resonance&bl=caseB')

    def test_pick_certain_experiments(self):
        submit = url_list(exs=[21])
        self.assertEqual(next(submit), 'http://bweb3/montecarlo.php?ex=21&rs=2&re=96&ty=evtgen-uds&dt=on_resonance&bl=caseB&st=10'),

    def test_convert_to_stem(self):
        url = 'http://bweb3/montecarlo.php?ex=51&rs=1725&re=1756&ty=evtgen-charm&dt=on_resonance&bl=caseB&st=0'
        self.assertEqual(convert_to_stem(url), '51_1725_1756_evtgen-charm_on_resonance_caseB_0')

