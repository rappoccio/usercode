
import ROOT
ROOT.gROOT.Macro("rootlogon.C")


ROOT.gSystem.Load("libAnalysisTTBSMTuplesAnalysis")

from Analysis.TTBSMTuplesAnalysis import *
a = ROOT.TH1D("a", "a", 10, 0, 10)
pred = ROOT.PredictedDistribution(a, "bla", "bla", 10, 0, 10)
