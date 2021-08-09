import unittest
import ROOT
from plotting import Uploader
import numpy as np
import matplotlib.pyplot as plt


class TestUploader(unittest.TestCase):

    def test_upload_one_figure(self):
        u = Uploader()
        c = ROOT.TCanvas('c', '')
        h = ROOT.TH1D('h', '', 100, -10., 10.)
        h.FillRandom('gaus', 1000)
        h.Draw()
        u.register(c)
        u.upload()

    def test_upload_two_figures(self):
        with Uploader() as u:
            c1 = ROOT.TCanvas('c1', '')
            h1 = ROOT.TH1D('h1', '', 100, -10., 10.)
            h1.FillRandom('gaus', 1000)
            h1.Draw()
            u.register(c1)
            c2 = ROOT.TCanvas('c2', '')
            h2 = ROOT.TH1D('h2', '', 100, 0., 10.)
            h2.FillRandom('gaus', 1000)
            h2.Draw()
            u.register(c2)

    def test_upload_pyplot_plot(self):
        with Uploader() as u:
            fig, ax = plt.subplots(num='pyplot_fig')
            x = np.arange(0., 1., 0.01)
            ax.plot(x, x**2)
            u.register(fig)


if __name__ == '__main__':
    unittest.main()
