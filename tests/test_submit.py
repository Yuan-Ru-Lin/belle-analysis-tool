import os
import unittest
from anatool.submit import run_list, url_list, SubmitInfo


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


class TestSubmitInfo(unittest.TestCase):

    def test_default_submit(self):
        info = SubmitInfo()
        self.assertEqual(
            (
                info.url,
                info.isMC,
                info.isCustomFile,
                info.outputname,
            ),
            (
                'http://bweb3/montecarlo.php?ex=55&rs=990&re=1093&ty=evtgen-uds&dt=on_resonance&bl=caseB&st=0',
                True,
                False,
                os.getcwd() + '/55_990_1093_evtgen-uds_on_resonance_caseB_0.root',
            )
        )

    def test_submit_for_custom_files(self):
        info = SubmitInfo('--path yourSimulation/s0/e9/data1.mdst yourSimulation/s0/e9/data2.mdst --suffix my_suffix')
        self.assertEqual(
            (
                info.url,
                info.isMC,
                info.isCustomFile,
                info.outputname,
            ),
            (
                ['yourSimulation/s0/e9/data1.mdst', 'yourSimulation/s0/e9/data2.mdst'],
                True,
                True,
                os.getcwd() + '/yourSimulation_s0_e9_my_suffix.root',
            )
        )

    def test_submit_for_mc(self):
        info = SubmitInfo('--path http://bweb3/montecarlo.php?ex=55&rs=1096&re=1136&ty=evtgen-charm&dt=on_resonance&bl=caseB&st=1 --suffix my_suffix')
        self.assertEqual(
            (
                info.url,
                info.isMC,
                info.isCustomFile,
                info.outputname,
            ),
            (
                'http://bweb3/montecarlo.php?ex=55&rs=1096&re=1136&ty=evtgen-charm&dt=on_resonance&bl=caseB&st=1',
                True,
                False,
                os.getcwd() + '/55_1096_1136_evtgen-charm_on_resonance_caseB_1_my_suffix.root',
            )
        )

    def test_submit_for_data(self):
        info = SubmitInfo('--path http://bweb3/mdst.php?ex=55&rs=1096&re=1136&skm=HadronBJ&dt=on_resonance&bl=caseB --suffix my_suffix')
        self.assertEqual(
            (
                info.url,
                info.isMC,
                info.isCustomFile,
                info.outputname,
            ),
            (
                'http://bweb3/mdst.php?ex=55&rs=1096&re=1136&skm=HadronBJ&dt=on_resonance&bl=caseB',
                False,
                False,
                os.getcwd() + '/55_1096_1136_HadronBJ_on_resonance_caseB_my_suffix.root',
            )
        )

