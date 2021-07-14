import os
import unittest
from anatool.submit_parse import SubmitInfo


class TestSubmitParse(unittest.TestCase):

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
        info = SubmitInfo('--path /self/generated/mdst/s0/e9/data1.mdst /self/generated/mdst/s0/e9/data2.mdst --suffix my_suffix')
        self.assertEqual(
            (
                info.url,
                info.isMC,
                info.isCustomFile,
                info.outputname,
            ),
            (
                ['/self/generated/mdst/s0/e9/data1.mdst', '/self/generated/mdst/s0/e9/data2.mdst'],
                True,
                True,
                os.getcwd() + '/s0_e9_my_suffix.root',
            )
        )

    def test_submit_for_mc(self):
        info = SubmitInfo('--path http://bweb3/montecarlo.php?ex=55&rs=1096&re=1136&ty=evtgen-charm&dt=on_resonance&bl=caseB&st=1')
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
                os.getcwd() + '/55_1096_1136_evtgen-charm_on_resonance_caseB_1.root',
            )
        )

    def test_submit_for_data(self):
        info = SubmitInfo('--path http://bweb3/mdst.php?ex=55&rs=1096&re=1136&skm=HadronBJ&dt=on_resonance&bl=caseB')
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
                os.getcwd() + '/55_1096_1136_HadronBJ_on_resonance_caseB.root',
            )
        )

