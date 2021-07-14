import os
import unittest
import glob
from anatool.submit_parse import build_parser, SubmitInfo
from anatool.submit_parse import TreatDataAsMCError


class TestSubmitParse(unittest.TestCase):

    def setUp(self):
        self.submit = SubmitInfo()

    def tearDown(self):
        self.submit = None

    def test_default_submit(self):
        self.assertEqual(
            (
                self.submit.url,
                self.submit.isMC,
                self.submit.isCustomMC,
                self.submit.outputname,
            ),
            (
                'http://bweb3/montecarlo.php?ex=55&rs=990&re=1093&ty=evtgen-uds&dt=on_resonance&bl=caseB&st=0', 
                True,
                False,
                os.path.dirname(os.path.abspath(__file__)) + '/mc_55_990_1093_evtgen-uds_on_resonance_caseB_0.root',
            )
        )

    @unittest.skip('Because I am rewriting the module.')
    def test_submit_for_file(self):
        args = self.parser.parse_args(f'file {os.environ["REPO"]}/pnbark_threshold_enhancement/s0/e9 k_true --outputDir {self.test_dir}'.split())
        info = SubmitInfo(args)
        self.assertTrue(os.path.isdir(self.test_dir))
        self.assertEqual(
            (
                True,
                glob.glob('/group/belle/users/leonlin/belle_simulation/mc/out_data/mdst/pnbark_threshold_enhancement/s0/e9/*mdst'),
                f'{self.test_dir}/s0_e9_k_true.root',
                False,
            ),
            (
                info.isMC,
                info.url,
                info.outputname,
                info.generic,
            )
        )

    @unittest.skip('Because I am rewriting the module.')
    def test_submit_for_mc(self):
        args = self.parser.parse_args(f'mc 55 990 1093 evtgen-uds on_resonance caseB 0 --outputDir {self.test_dir}'.split())
        info = SubmitInfo(args)
        self.assertEqual(
            (
                True,
                'http://bweb3/montecarlo.php?ex=55&rs=990&re=1093&ty=evtgen-uds&dt=on_resonance&bl=caseB&st=0',
                f'{self.test_dir}/mc_55_990_1093_evtgen-uds_on_resonance_caseB_0.root',
                True,
            ),
            (
                info.isMC,
                info.url,
                info.outputname,
                info.generic,
            )
        )

    @unittest.skip('Because I am rewriting the module.')
    def test_submit_for_data(self):
        args = self.parser.parse_args(f'data 55 990 1093 HadronBJ on_resonance caseB --outputDir {self.test_dir}'.split())
        info = SubmitInfo(args)
        self.assertEqual(
            (
                False,
                'http://bweb3/mdst.php?ex=55&rs=990&re=1093&skm=HadronBJ&dt=on_resonance&bl=caseB',
                f'{self.test_dir}/data_55_990_1093_HadronBJ_on_resonance_caseB.root',
            ),
            (
                info.isMC,
                info.url,
                info.outputname,
            )
        )

    @unittest.skip('Because I am rewriting the module.')
    def test_ask_if_generic_when_submit_for_data(self):
        args = self.parser.parse_args(f'data 55 990 1093 HadronBJ on_resonance caseB --outputDir {self.test_dir}'.split())
        info = SubmitInfo(args)
        with self.assertRaises(TreatDataAsMCError):
            info.generic

    @unittest.skip('I have not figured out how to test this without running a real basf2 job, which is going to be slow.')
    def test_pass_additional_argument_to_basf2(self):
        pass

