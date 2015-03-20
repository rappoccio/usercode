#!/usr/bin/env python

import math

# -------------------------------------------------------------------------------------
# Script for doing RooUnfold on the ttbar differential cross secion
# -------------------------------------------------------------------------------------

from optparse import OptionParser
parser = OptionParser()

    
# -------------------------------------------------------------------------------------
# input options
# -------------------------------------------------------------------------------------

parser.add_option('--closureTest', metavar='F', action='store_true',
                  default=False,
                  dest='closureTest',
                  help='Run closure test')

parser.add_option('--twoStep', metavar='F', action='store_true',
                  default=False,
                  dest='twoStep',
                  help='Do reco-particle and particle-parton unfolding')

parser.add_option('--systVariation', metavar='F', type='string', action='store',
                  default='nom',
                  dest='syst',
                  help='Run nominal or systematic variation?')

parser.add_option('--bkgSyst', metavar='F', type='string', action='store',
                  default='nom',
                  dest='bkgSyst',
                  help='Run nominal or systematic variation for backgrounds (nom or bkgup / bkgdn) ?')

parser.add_option('--ttbarPDF', metavar='F', type='string', action='store',
                  default='CT10_nom',
                  dest='pdf',
                  help='Which PDF set and nominal vs up/down? Or Q2 up/down?')

parser.add_option('--unfoldType', metavar='F', type='string', action='store',
                  default='full2',
                  dest='unfold',
                  help='Unfold using pt > 0 ("full" vs "full2" vs "full3", different binnings) or pt > 400 ("pt400")?')

parser.add_option('--addNoBtag', metavar='F', action='store_true',
                  default=False,
                  dest='addNoBtag',
                  help='Unfold only using category \"1 top-tag, 1 b-tag\" (default) or adding \"1 top-tag, 0 b-tag\" (use --addNoBtag)')

parser.add_option('--lepType', metavar='F', type='string', action='store',
                  default='muon',
                  dest='lepType',
                  help='Lepton type (ele or muon)')

parser.add_option('--troubleshoot', metavar='F', action='store_true',
                  default=False,
                  dest='troubleshoot',
                  help='Make troubleshooting plots')


# -------------------------------------------------------------------------------------
# load options & set plot style
# -------------------------------------------------------------------------------------

(options, args) = parser.parse_args()
argv = []

import sys

unfoldType = "_"
if options.unfold == "":
    unfoldType = ""
elif (options.unfold == "full" or options.unfold == "full2" or options.unfold == "full3" or options.unfold == "pt400") == False:
    print ""
    print "WARNING - not a valid option for unfolding type (use either \"full\" or \"pt400\"), exiting...!"
    print ""
    sys.exit()
else :
    unfoldType += options.unfold 
    print ""
    print "Unfolding using option \"" + options.unfold +"\" "
    print ""


nobtag = ""
if options.addNoBtag == True:
    nobtag = "_nobtag"


    
from ROOT import gRandom, TH1, TH1D, cout, TFile, gSystem, TCanvas, TPad, gPad, gROOT, gStyle, THStack, TLegend, TLatex, TColor

gROOT.Macro("rootlogon.C")

gStyle.SetOptStat(000000)
gStyle.SetOptTitle(0);

gStyle.SetTitleFont(43)
gStyle.SetTitleFont(43, "XYZ")
gStyle.SetTitleSize(30, "XYZ")
gStyle.SetLabelFont(43, "XYZ")
gStyle.SetLabelSize(24, "XYZ")

gStyle.SetPadTopMargin(0.07);
gStyle.SetPadRightMargin(0.05);
gStyle.SetPadBottomMargin(0.16);
gStyle.SetPadLeftMargin(0.18);
  
gSystem.Load("RooUnfold-1.1.1/libRooUnfold.so")

from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import RooUnfoldSvd


# -------------------------------------------------------------------------------------
# cross sections, efficiencies, total number of events
# -------------------------------------------------------------------------------------

# luminosity
lum = 19.7 #fb-1

# cross sections
sigma_ttbar = [ 
    [245.8*1000., 245.8*1000., 245.8*1000.],  # nominal (m<700, 700-1000, 1000-inf)
    [252.0*1000., 252.0*1000., 252.0*1000.],  # Q2 up
    [237.4*1000., 237.4*1000., 237.4*1000.]   # Q2 down
    ]
eff_ttbar = [ 
    [1.0, 0.074, 0.015],  # nominal
    [1.0, 0.074, 0.014],  # Q2 up
    [1.0, 0.081, 0.016]   # Q2 down
    ]
Nmc_ttbar = [
    [21675970., 3082812., 1249111.],  # nominal
    [14983686., 2243672., 1241650.],  # Q2 up
    [14545715*89./102., 2170074., 1308090.]    # Q2 down
    ]

if options.pdf == "scaleup" :
    ipdf = 1
elif options.pdf == "scaledown" :
    ipdf = 2
else:
    ipdf = 0


sigma_T_t = 56.4 * 1000.       # 
sigma_Tbar_t = 30.7 * 1000.    # All single-top approx NNLO cross sections from
sigma_T_s = 3.79 * 1000.       # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma8TeV
sigma_Tbar_s = 1.76 * 1000.    # 
sigma_T_tW = 11.1 * 1000.      # 
sigma_Tbar_tW = 11.1 * 1000.   # 
sigma_WJets = 36703.2 * 1000.  # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV
sigma_WJets_1jet = 5400*1.207*1000. #
sigma_WJets_2jet = 1750*1.207*1000. #
sigma_WJets_3jet = 519 *1.207*1000. #
sigma_WJets_4jet = 214 *1.207*1000. #

# MC event counts from B2G twiki here :
# https://twiki.cern.ch/twiki/bin/view/CMS/B2GTopLikeBSM53X#Backgrounds
Nmc_T_t = 3758227
Nmc_Tbar_t = 1935072
Nmc_T_s = 259961
Nmc_Tbar_s = 139974
Nmc_T_tW = 497658
Nmc_Tbar_tW = 493460
Nmc_WJets = 57709905
Nmc_WJets_1jet = 23141598
Nmc_WJets_2jet = 34044921
Nmc_WJets_3jet = 15539503
Nmc_WJets_4jet = 13382803


## hack to account for that when doing closure test, the ttbar sample is split in two 
eff_closure = 1.0
if options.closureTest == True:
    eff_closure = 2.0


# -------------------------------------------------------------------------------------
# Scaling of the various backgrounds from the theta fit
# -------------------------------------------------------------------------------------

### background counts: 1toptag+1btag (nom, up, dn), 1toptag+>=0btag (nom, up, dn))
i_bkgnorm = 0
if nobtag == "" and options.bkgSyst == "bkgup": 
    i_bkgnorm = 1
elif nobtag == "" and options.bkgSyst == "bkgdn": 
    i_bkgnorm = 2
elif nobtag == "": 
    i_bkgnorm = 0
elif options.bkgSyst == "bkgup": 
    i_bkgnorm = 4
elif options.bkgSyst == "bkgdn": 
    i_bkgnorm = 5
else:
    i_bkgnorm = 3
    
    
### muon channel
if options.pdf == "CT10_nom" and options.lepType == "muon" :   #unfold
    n_ttbarnonsemilep = [28.1642, 31.9996, 24.3289, 70.8412, 80.4882, 61.1942]   #unfold
    n_wjets           = [4.364, 4.83321, 3.89478, 174.952, 193.763, 156.141]   #unfold
    n_singletop       = [3.54622, 5.67982, 1.41262, 15.7152, 25.1704, 6.2601]   #unfold
    n_qcd             = [9.52228, 11.3246, 7.72, 59.7344, 71.0403, 48.4285]   #unfold
if options.pdf == "CT10_pdfup" and options.lepType == "muon" :   #unfold
    n_ttbarnonsemilep = [27.9857, 32.0025, 23.9689, 70.8017, 80.964, 60.6394]   #unfold
    n_wjets           = [4.00972, 4.48587, 3.53357, 162.632, 181.944, 143.319]   #unfold
    n_singletop       = [3.44369, 5.50598, 1.38139, 15.3059, 24.472, 6.13979]   #unfold
    n_qcd             = [9.87787, 11.6437, 8.112, 61.965, 73.0425, 50.8875]   #unfold
if options.pdf == "CT10_pdfdown" and options.lepType == "muon" :   #unfold
    n_ttbarnonsemilep = [28.1156, 31.7899, 24.4412, 70.6088, 79.8365, 61.3811]   #unfold
    n_wjets           = [4.65365, 5.12678, 4.18052, 185.117, 203.938, 166.296]   #unfold
    n_singletop       = [3.61272, 5.79998, 1.42547, 15.9794, 25.6539, 6.30498]   #unfold
    n_qcd             = [9.15339, 10.9935, 7.31327, 57.4203, 68.9636, 45.877]   #unfold
if options.pdf == "MSTW_nom" and options.lepType == "muon" :   #unfold
    n_ttbarnonsemilep = [28.1887, 32.0444, 24.3329, 70.932, 80.6343, 61.2297]   #unfold
    n_wjets           = [4.3956, 4.86461, 3.92659, 176.183, 194.982, 157.384]   #unfold
    n_singletop       = [3.54129, 5.67508, 1.40749, 15.6908, 25.1453, 6.23634]   #unfold
    n_qcd             = [9.59676, 11.3926, 7.80089, 60.2016, 71.4673, 48.9359]   #unfold
if options.pdf == "MSTW_pdfup" and options.lepType == "muon" :   #unfold
    n_ttbarnonsemilep = [28.0767, 32.012, 24.1413, 70.8849, 80.8204, 60.9495]   #unfold
    n_wjets           = [4.3325, 4.78824, 3.87675, 174.031, 192.338, 155.725]   #unfold
    n_singletop       = [3.51415, 5.62785, 1.40045, 15.5649, 24.9269, 6.20288]   #unfold
    n_qcd             = [9.89875, 11.6612, 8.13628, 62.096, 73.1522, 51.0399]   #unfold
if options.pdf == "MSTW_pdfdown" and options.lepType == "muon" :   #unfold
    n_ttbarnonsemilep = [28.2873, 32.0608, 24.5138, 70.8918, 80.3488, 61.4349]   #unfold
    n_wjets           = [4.63485, 5.09942, 4.17028, 184.932, 203.468, 166.395]   #unfold
    n_singletop       = [3.5838, 5.75973, 1.40787, 15.8732, 25.5108, 6.23567]   #unfold
    n_qcd             = [9.57173, 11.3619, 7.7816, 60.0446, 71.2742, 48.8149]   #unfold
if options.pdf == "NNPDF_nom" and options.lepType == "muon" :   #unfold
    n_ttbarnonsemilep = [27.3348, 30.8549, 23.8147, 68.5254, 77.3499, 59.701]   #unfold
    n_wjets           = [4.74339, 5.21821, 4.26857, 188.575, 207.451, 169.698]   #unfold
    n_singletop       = [3.7092, 5.95821, 1.46019, 16.4049, 26.3518, 6.4581]   #unfold
    n_qcd             = [10.6747, 12.2539, 9.09542, 66.9635, 76.8704, 57.0566]   #unfold
if options.pdf == "NNPDF_pdfup" and options.lepType == "muon" :   #unfold
    n_ttbarnonsemilep = [27.872, 31.7098, 24.0342, 69.0227, 78.5266, 59.5188]   #unfold
    n_wjets           = [4.32935, 4.80398, 3.85472, 174.491, 193.62, 155.361]   #unfold
    n_singletop       = [3.60122, 5.76074, 1.4417, 15.9802, 25.5629, 6.39745]   #unfold
    n_qcd             = [10.4378, 12.0832, 8.79236, 65.4774, 75.7993, 55.1555]   #unfold
if options.pdf == "NNPDF_pdfdown" and options.lepType == "muon" :   #unfold
    n_ttbarnonsemilep = [23.9143, 26.6638, 21.1647, 61.8445, 68.955, 54.7339]   #unfold
    n_wjets           = [5.7301, 6.29576, 5.16445, 222.504, 244.468, 200.539]   #unfold
    n_singletop       = [10.38, 12.6828, 8.07721, 45.6484, 55.7754, 35.5214]   #unfold
    n_qcd             = [13.2824, 14.6411, 11.9237, 83.3221, 91.8455, 74.7987]   #unfold
if options.pdf == "scaleup" and options.lepType == "muon" :   #unfold
    n_ttbarnonsemilep = [28.5788, 32.5469, 24.6107, 72.3536, 82.3997, 62.3075]   #unfold
    n_wjets           = [4.29936, 4.69019, 3.90852, 173.868, 189.674, 158.063]   #unfold
    n_singletop       = [3.41799, 5.4721, 1.36387, 15.068, 24.1234, 6.01253]   #unfold
    n_qcd             = [8.14429, 10.2154, 6.07317, 51.0901, 64.0825, 38.0977]   #unfold
if options.pdf == "scaledown" and options.lepType == "muon" :   #unfold
    n_ttbarnonsemilep = [25.7471, 29.0597, 22.4344, 72.3859, 81.6991, 63.0726]   #unfold
    n_wjets           = [4.73317, 5.23569, 4.23065, 189.358, 209.462, 169.254]   #unfold
    n_singletop       = [3.67313, 5.94687, 1.39939, 16.259, 26.3237, 6.19437]   #unfold
    n_qcd             = [10.7492, 12.2991, 9.19925, 67.4309, 77.1538, 57.708]   #unfold

### electron channel
if options.pdf == "CT10_nom" and options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [29.8444, 32.7033, 26.9855, 71.3904, 78.2291, 64.5516]   #unfold
    n_wjets           = [8.42257, 8.8202, 8.02493, 310.527, 325.187, 295.867]   #unfold
    n_singletop       = [3.00695, 4.78191, 1.232, 15.3119, 24.3502, 6.27353]   #unfold
    n_qcd             = [10.42, 11.2478, 9.59218, 140.985, 152.185, 129.784]   #unfold
if options.pdf == "CT10_pdfup" and options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [30.1086, 33.1272, 27.0899, 72.439, 79.7017, 65.1764]   #unfold
    n_wjets           = [8.23543, 8.6402, 7.83066, 305.644, 320.666, 290.622]   #unfold
    n_singletop       = [3.23379, 5.11893, 1.34865, 15.5016, 24.5382, 6.46491]   #unfold
    n_qcd             = [10.0758, 10.9269, 9.22478, 136.328, 147.842, 124.813]   #unfold
if options.pdf == "CT10_pdfdown" and options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [29.4114, 32.1358, 26.6869, 70.2933, 76.8048, 63.7818]   #unfold
    n_wjets           = [8.69967, 9.10066, 8.29867, 318.012, 332.67, 303.354]   #unfold
    n_singletop       = [3.01138, 4.80829, 1.21446, 15.3209, 24.463, 6.17881]   #unfold
    n_qcd             = [10.5412, 11.3649, 9.71752, 142.624, 153.769, 131.48]   #unfold
if options.pdf == "MSTW_nom" and options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [29.3959, 32.226, 26.5658, 70.223, 76.9838, 63.4622]   #unfold
    n_wjets           = [8.62878, 9.03055, 8.22701, 317.016, 331.777, 302.255]   #unfold
    n_singletop       = [3.22865, 5.13182, 1.32549, 15.5334, 24.6898, 6.37706]   #unfold
    n_qcd             = [10.2005, 11.0468, 9.35424, 138.015, 149.466, 126.564]   #unfold
if options.pdf == "MSTW_pdfup" and options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [29.4136, 32.3277, 26.4995, 69.6511, 76.5517, 62.7505]   #unfold
    n_wjets           = [8.49389, 8.88971, 8.09807, 314.226, 328.869, 299.583]   #unfold
    n_singletop       = [3.24127, 5.12342, 1.35913, 15.6518, 24.7405, 6.56312]   #unfold
    n_qcd             = [10.1431, 10.992, 9.29415, 137.238, 148.724, 125.752]   #unfold
if options.pdf == "MSTW_pdfdown" and options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [29.0022, 31.7348, 26.2696, 69.2073, 75.7281, 62.6865]   #unfold
    n_wjets           = [8.72571, 9.11892, 8.33251, 318.833, 333.201, 304.465]   #unfold
    n_singletop       = [2.95214, 4.70101, 1.20327, 15.3144, 24.3868, 6.24205]   #unfold
    n_qcd             = [10.4353, 11.2619, 9.60862, 141.191, 152.376, 130.006]   #unfold
if options.pdf == "NNPDF_nom" and options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [29.6279, 32.4309, 26.8249, 70.2968, 76.9474, 63.6462]   #unfold
    n_wjets           = [8.58248, 8.97657, 8.1884, 315.561, 330.05, 301.071]   #unfold
    n_singletop       = [3.01911, 4.80467, 1.23356, 15.368, 24.457, 6.2791]   #unfold
    n_qcd             = [10.4597, 11.2862, 9.63307, 141.521, 152.705, 130.337]   #unfold
if options.pdf == "NNPDF_pdfup" and options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [29.9074, 32.8549, 26.96, 71.6679, 78.7309, 64.6049]   #unfold
    n_wjets           = [8.24029, 8.63951, 7.84107, 305.28, 320.07, 290.49]   #unfold
    n_singletop       = [3.05021, 4.82472, 1.2757, 15.5176, 24.5453, 6.48998]   #unfold
    n_qcd             = [10.346, 11.1763, 9.5157, 139.983, 151.217, 128.749]   #unfold
if options.pdf == "NNPDF_pdfdown" and options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [29.7156, 32.463, 26.9683, 70.9149, 77.4713, 64.3585]   #unfold
    n_wjets           = [8.68883, 9.08536, 8.2923, 318.267, 332.791, 303.742]   #unfold
    n_singletop       = [2.97043, 4.75234, 1.18851, 15.1351, 24.2145, 6.05579]   #unfold
    n_qcd             = [10.5091, 11.3338, 9.68441, 142.19, 153.348, 131.032]   #unfold
if options.pdf == "scaleup" and options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [28.9284, 31.6242, 26.2326, 65.8302, 71.9649, 59.6956]   #unfold
    n_wjets           = [9.28813, 9.68849, 8.88777, 342.661, 357.431, 327.89]   #unfold
    n_singletop       = [3.63993, 5.72424, 1.55562, 17.2889, 27.189, 7.38886]   #unfold
    n_qcd             = [10.5541, 11.387, 9.7212, 142.799, 154.068, 131.53]   #unfold
if options.pdf == "scaledown" and options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [31.289, 34.256, 28.322, 66.1724, 72.4473, 59.8976]   #unfold
    n_wjets           = [9.01791, 9.42822, 8.60759, 332.791, 347.933, 317.649]   #unfold
    n_singletop       = [3.57937, 5.6205, 1.53825, 17.1463, 26.924, 7.3687]   #unfold
    n_qcd             = [10.5305, 11.3658, 9.69518, 142.479, 153.781, 131.177]   #unfold


### finally extract relevant background normalizations
fitted_qcd = n_qcd[i_bkgnorm]
fitted_singletop = n_singletop[i_bkgnorm]
fitted_wjets = n_wjets[i_bkgnorm]
fitted_ttbarnonsemilep = n_ttbarnonsemilep[i_bkgnorm]


# -------------------------------------------------------------------------------------
#  read histogram files
# -------------------------------------------------------------------------------------

DIR = ""
muOrEl = "mu"
if options.lepType=="ele":
    print ""
    print "UNFOLDING FOR ELECTRON CHANNEL !!!" 
    print ""
    DIR = "_el"
    muOrEl = "el"
else:
    print ""
    print "UNFOLDING FOR MUON CHANNEL !!!" 
    print ""
    

if options.lepType=="ele":
    f_data = TFile("histfiles/2Dhist_el/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root")
    f_QCD  = TFile("histfiles/2Dhist_el/SingleEl_iheartNY_V1_el_Run2012_2Dcut_qcd.root")
else:
    f_data = TFile("histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root")
    f_QCD  = TFile("histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_qcd.root")

    
if options.closureTest == True : 
    f_ttbar_max700    = TFile("histfiles_"+options.pdf+"/2Dhists"+DIR+"/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+"_even.root")
    f_ttbar_700to1000 = TFile("histfiles_"+options.pdf+"/2Dhists"+DIR+"/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+"_even.root")
    f_ttbar_1000toInf = TFile("histfiles_"+options.pdf+"/2Dhists"+DIR+"/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+"_even.root")
    f_ttbar_max700_odd    = TFile("histfiles_"+options.pdf+"/2Dhists"+DIR+"/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+"_odd.root")
    f_ttbar_700to1000_odd = TFile("histfiles_"+options.pdf+"/2Dhists"+DIR+"/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+"_odd.root")
    f_ttbar_1000toInf_odd = TFile("histfiles_"+options.pdf+"/2Dhists"+DIR+"/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+"_odd.root")
    ## full truth samples for unfolding (two-step) particle-level to parton 
    f_ttbar_max700_pp    = TFile("TruthStudy/TT_max700_"+options.pdf+DIR+"_fullTruth_even.root")
    f_ttbar_700to1000_pp = TFile("TruthStudy/TT_Mtt-700to1000_"+options.pdf+DIR+"_fullTruth_even.root")
    f_ttbar_1000toInf_pp = TFile("TruthStudy/TT_Mtt-1000toInf_"+options.pdf+DIR+"_fullTruth_even.root")
    f_ttbar_max700_pp_odd    = TFile("TruthStudy/TT_max700_"+options.pdf+DIR+"_fullTruth_odd.root")
    f_ttbar_700to1000_pp_odd = TFile("TruthStudy/TT_Mtt-700to1000_"+options.pdf+DIR+"_fullTruth_odd.root")
    f_ttbar_1000toInf_pp_odd = TFile("TruthStudy/TT_Mtt-1000toInf_"+options.pdf+DIR+"_fullTruth_odd.root")
else :
    #f_ttbar_max700    = TFile("histfiles_"+options.pdf+"/2Dhists"+DIR+"/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+".root")
    #f_ttbar_700to1000 = TFile("histfiles_"+options.pdf+"/2Dhists"+DIR+"/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+".root")
    #f_ttbar_1000toInf = TFile("histfiles_"+options.pdf+"/2Dhists"+DIR+"/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+".root")
    f_ttbar_max700    = TFile("histfiles_"+options.pdf+"/postfit/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+".root")
    f_ttbar_700to1000 = TFile("histfiles_"+options.pdf+"/postfit/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+".root")
    f_ttbar_1000toInf = TFile("histfiles_"+options.pdf+"/postfit/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+".root")
    ## full truth samples for unfolding (two-step) particle-level to parton 
    f_ttbar_max700_pp    = TFile("TruthStudy/TT_max700_"+options.pdf+DIR+"_fullTruth.root")
    f_ttbar_700to1000_pp = TFile("TruthStudy/TT_Mtt-700to1000_"+options.pdf+DIR+"_fullTruth.root")
    f_ttbar_1000toInf_pp = TFile("TruthStudy/TT_Mtt-1000toInf_"+options.pdf+DIR+"_fullTruth.root")

f_ttbar_nonsemilep_max700    = TFile("histfiles_"+options.pdf+"/2Dhists"+DIR+"/TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+".root")
f_ttbar_nonsemilep_700to1000 = TFile("histfiles_"+options.pdf+"/2Dhists"+DIR+"/TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+".root")
f_ttbar_nonsemilep_1000toInf = TFile("histfiles_"+options.pdf+"/2Dhists"+DIR+"/TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+".root")

f_T_t     = TFile("histfiles/2Dhist"+DIR+"/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_Tbar_t  = TFile("histfiles/2Dhist"+DIR+"/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_T_s     = TFile("histfiles/2Dhist"+DIR+"/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_Tbar_s  = TFile("histfiles/2Dhist"+DIR+"/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_T_tW    = TFile("histfiles/2Dhist"+DIR+"/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_Tbar_tW = TFile("histfiles/2Dhist"+DIR+"/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")

f_WJets_1jet   = TFile("histfiles/2Dhist"+DIR+"/W1JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_WJets_2jet   = TFile("histfiles/2Dhist"+DIR+"/W2JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_WJets_3jet   = TFile("histfiles/2Dhist"+DIR+"/W3JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_WJets_4jet   = TFile("histfiles/2Dhist"+DIR+"/W4JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")


# the response matrices are simply added here, but have been filled with the full event weights (taking sample size, efficiency, etx. into account)
if options.closureTest == True : 
    response_ttbar_max700    = f_ttbar_max700_odd.Get("response_pt"+nobtag+unfoldType)
    response_ttbar_700to1000 = f_ttbar_700to1000_odd.Get("response_pt"+nobtag+unfoldType)
    response_ttbar_1000toInf = f_ttbar_1000toInf_odd.Get("response_pt"+nobtag+unfoldType)
else :
    response_ttbar_max700    = f_ttbar_max700.Get("response_pt"+nobtag+unfoldType)
    response_ttbar_700to1000 = f_ttbar_700to1000.Get("response_pt"+nobtag+unfoldType)
    response_ttbar_1000toInf = f_ttbar_1000toInf.Get("response_pt"+nobtag+unfoldType)

response = response_ttbar_max700.Clone()
response.SetName("response_pt_"+options.syst)
response.Add(response_ttbar_700to1000)
response.Add(response_ttbar_1000toInf)

## response matrices for two-step unfolding
if options.twoStep == True :
    if options.closureTest == True : 
        response_ttbar_max700_rp    = f_ttbar_max700_odd.Get("response_pt"+nobtag+unfoldType+"_rp")
        response_ttbar_700to1000_rp = f_ttbar_700to1000_odd.Get("response_pt"+nobtag+unfoldType+"_rp")
        response_ttbar_1000toInf_rp = f_ttbar_1000toInf_odd.Get("response_pt"+nobtag+unfoldType+"_rp")
        response_ttbar_max700_pp    = f_ttbar_max700_pp_odd.Get("response_pt"+unfoldType+"_pp")
        response_ttbar_700to1000_pp = f_ttbar_700to1000_pp_odd.Get("response_pt"+unfoldType+"_pp")
        response_ttbar_1000toInf_pp = f_ttbar_1000toInf_pp_odd.Get("response_pt"+unfoldType+"_pp")
        if options.troubleshoot == True:
            response_ttbar_max700_rp_even    = f_ttbar_max700.Get("response_pt"+nobtag+unfoldType+"_rp")
            response_ttbar_700to1000_rp_even = f_ttbar_700to1000.Get("response_pt"+nobtag+unfoldType+"_rp")
            response_ttbar_1000toInf_rp_even = f_ttbar_1000toInf.Get("response_pt"+nobtag+unfoldType+"_rp")
            response_ttbar_max700_pp_even    = f_ttbar_max700_pp.Get("response_pt"+unfoldType+"_pp")
            response_ttbar_700to1000_pp_even = f_ttbar_700to1000_pp.Get("response_pt"+unfoldType+"_pp")
            response_ttbar_1000toInf_pp_even = f_ttbar_1000toInf_pp.Get("response_pt"+unfoldType+"_pp")
    else:
        response_ttbar_max700_rp    = f_ttbar_max700.Get("response_pt"+nobtag+unfoldType+"_rp")
        response_ttbar_700to1000_rp = f_ttbar_700to1000.Get("response_pt"+nobtag+unfoldType+"_rp")
        response_ttbar_1000toInf_rp = f_ttbar_1000toInf.Get("response_pt"+nobtag+unfoldType+"_rp")
        response_ttbar_max700_pp    = f_ttbar_max700_pp.Get("response_pt"+unfoldType+"_pp")
        response_ttbar_700to1000_pp = f_ttbar_700to1000_pp.Get("response_pt"+unfoldType+"_pp")
        response_ttbar_1000toInf_pp = f_ttbar_1000toInf_pp.Get("response_pt"+unfoldType+"_pp")

    response_rp = response_ttbar_max700_rp.Clone()
    response_rp.SetName("response_pt_"+options.syst+"_rp")
    response_rp.Add(response_ttbar_700to1000_rp)
    response_rp.Add(response_ttbar_1000toInf_rp)
    
    response_pp = response_ttbar_max700_pp.Clone()
    response_pp.SetName("response_pt_"+options.syst+"_pp")
    response_pp.Add(response_ttbar_700to1000_pp)
    response_pp.Add(response_ttbar_1000toInf_pp)

    if options.troubleshoot :
        response_rp_even = response_ttbar_max700_rp_even.Clone()
        response_rp_even.SetName("response_pt_"+options.syst+"_rp_even")
        response_rp_even.Add(response_ttbar_700to1000_rp_even)
        response_rp_even.Add(response_ttbar_1000toInf_rp_even)
        
        response_pp_even = response_ttbar_max700_pp_even.Clone()
        response_pp_even.SetName("response_pt_"+options.syst+"_pp_even")
        response_pp_even.Add(response_ttbar_700to1000_pp_even)
        response_pp_even.Add(response_ttbar_1000toInf_pp_even)


TH1.AddDirectory(0)

# -------------------------------------------------------------------------------------
# output file for storing histograms to  
# -------------------------------------------------------------------------------------

bkgout = ""
if options.bkgSyst == "bkgup" or options.bkgSyst == "bkgdn":
    bkgout = "_"+options.bkgSyst
if options.twoStep :
    fout = TFile("UnfoldingPlots/unfold"+DIR+"_2step_"+options.pdf+"_"+options.syst+bkgout+nobtag+unfoldType+".root","recreate");
else :
    fout = TFile("UnfoldingPlots/unfold"+DIR+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+unfoldType+".root","recreate");


# -------------------------------------------------------------------------------------
# read actual histograms
# -------------------------------------------------------------------------------------

if options.closureTest == True : 
    hTrue_max700    = f_ttbar_max700_odd.Get("ptGenTop"+unfoldType)
    hTrue_700to1000 = f_ttbar_700to1000_odd.Get("ptGenTop"+unfoldType)
    hTrue_1000toInf = f_ttbar_1000toInf_odd.Get("ptGenTop"+unfoldType)

    if options.twoStep :
        hPart_max700    = f_ttbar_max700_odd.Get("ptPartTop"+unfoldType)
        hPart_700to1000 = f_ttbar_700to1000_odd.Get("ptPartTop"+unfoldType)
        hPart_1000toInf = f_ttbar_1000toInf_odd.Get("ptPartTop"+unfoldType)

        if options.troubleshoot :
            hTrue_max700_even    = f_ttbar_max700.Get("ptGenTop"+unfoldType)
            hTrue_700to1000_even = f_ttbar_700to1000.Get("ptGenTop"+unfoldType)
            hTrue_1000toInf_even = f_ttbar_1000toInf.Get("ptGenTop"+unfoldType)
            hPart_max700_even    = f_ttbar_max700.Get("ptPartTop"+unfoldType)
            hPart_700to1000_even = f_ttbar_700to1000.Get("ptPartTop"+unfoldType)
            hPart_1000toInf_even = f_ttbar_1000toInf.Get("ptPartTop"+unfoldType)
else :
    hTrue_max700    = f_ttbar_max700.Get("ptGenTop"+unfoldType)
    hTrue_700to1000 = f_ttbar_700to1000.Get("ptGenTop"+unfoldType)
    hTrue_1000toInf = f_ttbar_1000toInf.Get("ptGenTop"+unfoldType)

    if options.twoStep :
        hPart_max700    = f_ttbar_max700.Get("ptPartTop"+unfoldType)
        hPart_700to1000 = f_ttbar_700to1000.Get("ptPartTop"+unfoldType)
        hPart_1000toInf = f_ttbar_1000toInf.Get("ptPartTop"+unfoldType)

hTrue_max700.Sumw2()
hTrue_700to1000.Sumw2()
hTrue_1000toInf.Sumw2()

if options.twoStep:
    hPart_max700.Sumw2()
    hPart_700to1000.Sumw2()
    hPart_1000toInf.Sumw2()
    
    if options.troubleshoot:
        hTrue_max700_even.Sumw2()
        hTrue_700to1000_even.Sumw2()
        hTrue_1000toInf_even.Sumw2()
        hPart_max700_even.Sumw2()
        hPart_700to1000_even.Sumw2()
        hPart_1000toInf_even.Sumw2()

isTwoStep = ""
if options.twoStep:
    isTwoStep = "_2step"
   

hRecoData = f_data.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType).Clone()
hRecoData.SetName("hRecoData"+unfoldType)

hRecoQCD = f_QCD.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType).Clone()
hRecoQCD.SetName("hRecoQCD")
hRecoQCD.Sumw2()
hRecoQCD.SetFillColor(TColor.kYellow)

if options.closureTest == False : 
    hMeas = f_data.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
else :
    hMeas_max700    = f_ttbar_max700.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
    hMeas_700to1000 = f_ttbar_700to1000.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
    hMeas_1000toInf = f_ttbar_1000toInf.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
    hMeas_max700.Sumw2()
    hMeas_700to1000.Sumw2()
    hMeas_1000toInf.Sumw2()

    if options.troubleshoot :
        hMeas_max700_odd    = f_ttbar_max700_odd.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
        hMeas_700to1000_odd = f_ttbar_700to1000_odd.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
        hMeas_1000toInf_odd = f_ttbar_1000toInf_odd.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
        hMeas_max700_odd.Sumw2()
        hMeas_700to1000_odd.Sumw2()
        hMeas_1000toInf_odd.Sumw2()
    

hMeas_T_t     = f_T_t.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_Tbar_t  = f_Tbar_t.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_T_s     = f_T_s.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_Tbar_s  = f_Tbar_s.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_T_tW    = f_T_tW.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_Tbar_tW = f_Tbar_tW.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_WJets_1jet   = f_WJets_1jet.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_WJets_2jet   = f_WJets_2jet.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_WJets_3jet   = f_WJets_3jet.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_WJets_4jet   = f_WJets_4jet.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_tt0_nonsemi = f_ttbar_nonsemilep_max700.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_tt700_nonsemi = f_ttbar_nonsemilep_700to1000.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_tt1000_nonsemi = f_ttbar_nonsemilep_1000toInf.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)

hMeas_T_t.Sumw2()
hMeas_Tbar_t.Sumw2()
hMeas_T_s.Sumw2()
hMeas_Tbar_s.Sumw2()
hMeas_T_tW.Sumw2()
hMeas_Tbar_tW.Sumw2()
hMeas_WJets_1jet.Sumw2()
hMeas_WJets_2jet.Sumw2()
hMeas_WJets_3jet.Sumw2()
hMeas_WJets_4jet.Sumw2()
hMeas_tt0_nonsemi.Sumw2()
hMeas_tt700_nonsemi.Sumw2()
hMeas_tt1000_nonsemi.Sumw2()


# -------------------------------------------------------------------------------------
# Normalize histograms
# -------------------------------------------------------------------------------------

# if doing closure test, use ttbar nominal as the "measured" distribution
if options.closureTest == True : 
    hMeas_max700.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
    hMeas_700to1000.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
    hMeas_1000toInf.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
    hMeas = hMeas_max700.Clone()
    hMeas.SetName("ptRecoTop_measured")
    hMeas.Add(hMeas_700to1000)
    hMeas.Add(hMeas_1000toInf)    

    if options.troubleshoot :
        hMeas_max700_odd.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
        hMeas_700to1000_odd.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
        hMeas_1000toInf_odd.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
        hMeas_odd = hMeas_max700_odd.Clone()
        hMeas_odd.SetName("ptRecoTop_measured_odd")
        hMeas_odd.Add(hMeas_700to1000_odd)
        hMeas_odd.Add(hMeas_1000toInf_odd)    

hTrue_max700.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
hTrue_700to1000.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
hTrue_1000toInf.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
hTrue = hTrue_max700.Clone()
hTrue.SetName("pt_genTop")
hTrue.Add(hTrue_700to1000)
hTrue.Add(hTrue_1000toInf)

if options.troubleshoot and options.twoStep :
    hTrue_max700_even.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
    hTrue_700to1000_even.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
    hTrue_1000toInf_even.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
    hTrue_even = hTrue_max700_even.Clone()
    hTrue_even.SetName("pt_genTop_even")
    hTrue_even.Add(hTrue_700to1000_even)
    hTrue_even.Add(hTrue_1000toInf_even)

if options.twoStep :
    hPart_max700.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
    hPart_700to1000.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
    hPart_1000toInf.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
    hPart = hPart_max700.Clone()
    hPart.SetName("pt_partTop")
    hPart.Add(hPart_700to1000)
    hPart.Add(hPart_1000toInf)

    if options.troubleshoot :
        hPart_max700_even.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
        hPart_700to1000_even.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
        hPart_1000toInf_even.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
        hPart_even = hPart_max700_even.Clone()
        hPart_even.SetName("pt_partTop_even")
        hPart_even.Add(hPart_700to1000_even)
        hPart_even.Add(hPart_1000toInf_even)

hMeas_T_t.Scale( sigma_T_t * lum / float(Nmc_T_t) )
hMeas_Tbar_t.Scale( sigma_Tbar_t * lum / float(Nmc_Tbar_t) )
hMeas_T_s.Scale( sigma_T_s * lum / float(Nmc_T_s) )
hMeas_Tbar_s.Scale( sigma_Tbar_s * lum / float(Nmc_Tbar_s) )
hMeas_T_tW.Scale( sigma_T_tW * lum / float(Nmc_T_tW) )
hMeas_Tbar_tW.Scale( sigma_Tbar_tW * lum / float(Nmc_Tbar_tW) )

hMeas_WJets_1jet.Scale( sigma_WJets_1jet * lum / float(Nmc_WJets_1jet) )
hMeas_WJets_2jet.Scale( sigma_WJets_2jet * lum / float(Nmc_WJets_2jet) )
hMeas_WJets_3jet.Scale( sigma_WJets_3jet * lum / float(Nmc_WJets_3jet) )
hMeas_WJets_4jet.Scale( sigma_WJets_4jet * lum / float(Nmc_WJets_4jet) )


hMeas_SingleTop = hMeas_T_t.Clone()
hMeas_SingleTop.SetName("ptRecoTop_SingleTop")

hMeas_WJets = hMeas_WJets_1jet.Clone()
hMeas_WJets.SetName("ptRecoTop_WJets")

for hist in [hMeas_Tbar_t, hMeas_T_s, hMeas_Tbar_s, hMeas_T_tW, hMeas_Tbar_tW] :
    hMeas_SingleTop.Add( hist )
for hist in [hMeas_WJets_2jet,hMeas_WJets_3jet,hMeas_WJets_4jet] :
    hMeas_WJets.Add( hist )

hMeas_tt0_nonsemi.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
hMeas_tt700_nonsemi.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
hMeas_tt1000_nonsemi.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))

hMeas_TTNonSemi = hMeas_tt0_nonsemi.Clone()
hMeas_TTNonSemi.SetName("ptRecoTop_TTNonSemilep")
hMeas_TTNonSemi.Add( hMeas_tt700_nonsemi )
hMeas_TTNonSemi.Add( hMeas_tt1000_nonsemi )


# -------------------------------------------------------------------------------------
# Scale each sample to that fitted by theta
# -------------------------------------------------------------------------------------

hRecoQCD.Scale( fitted_qcd / hRecoQCD.Integral() )
hMeas_SingleTop.Scale( fitted_singletop / hMeas_SingleTop.Integral() )
hMeas_WJets.Scale( fitted_wjets / hMeas_WJets.Integral() )
hMeas_TTNonSemi.Scale( fitted_ttbarnonsemilep / hMeas_TTNonSemi.Integral() )


# -------------------------------------------------------------------------------------
# subtract backgrounds from the data distribution, but not for closure test!!! 
# -------------------------------------------------------------------------------------

if options.closureTest == False : 
    for hist in [hMeas_SingleTop, hMeas_WJets, hRecoQCD, hMeas_TTNonSemi] :
        hMeas.Add(hist, -1.)

    for ibin in xrange( hMeas.GetNbinsX() ) :
        if ( hMeas.GetBinContent( ibin ) < 0.0 ) :
            hMeas.SetBinContent( ibin, 0.0 )


# -------------------------------------------------------------------------------------
# draw background-subtracted data distribution 
# -------------------------------------------------------------------------------------

#if options.closureTest == False : 
#    cc = TCanvas("cc", "", 800, 600)
#    
#    ll = TLegend(0.4, 0.65, 0.7, 0.9)
#    ll.SetFillStyle(0)
#    ll.SetTextFont(42)
#    ll.SetTextSize(0.045)
#    ll.SetBorderSize(0)
#    
#    hMeas.SetLineColor(1)
#    hMeas.SetLineWidth(2)
#    hMeas.Draw("hist")
#    hMeas.Draw("axis,same")
#    ll.AddEntry(hMeas, "Background-subtracted data","l")
#    ll.Draw()
#    cc.SaveAs("UnfoldingPlots/unfold"+DIR+"_input"+isTwoStep+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+unfoldType+".png")
#    cc.SaveAs("UnfoldingPlots/unfold"+DIR+"_input"+isTwoStep+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+unfoldType+".eps")

if options.closureTest and options.troubleshoot and options.twoStep :
    ct1 = TCanvas("ct1", "", 800, 600)
    
    lt1 = TLegend(0.4, 0.65, 0.7, 0.9)
    lt1.SetFillStyle(0)
    lt1.SetTextFont(42)
    lt1.SetTextSize(0.045)
    lt1.SetBorderSize(0)
    
    hMeas.SetLineColor(2)
    hMeas.SetLineWidth(2)
    hMeas_odd.SetLineColor(4)
    hMeas_odd.SetLineWidth(2)
    hMeas.Draw("hist")
    hMeas_odd.Draw("hist,same")
    lt1.AddEntry(hMeas, "Unfolding input, even","l")
    lt1.AddEntry(hMeas_odd, "Unfolding input, odd","l")
    lt1.Draw()
    ct1.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_hMeas_evenVsOdd"+isTwoStep+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+unfoldType+".png")

    ct2 = TCanvas("ct2", "", 800, 600)
    
    lt2 = TLegend(0.4, 0.65, 0.7, 0.9)
    lt2.SetFillStyle(0)
    lt2.SetTextFont(42)
    lt2.SetTextSize(0.045)
    lt2.SetBorderSize(0)
    
    hPart_even.SetLineColor(2)
    hPart_even.SetLineWidth(2)
    hPart.SetLineColor(4)
    hPart.SetLineWidth(2)
    hPart_even.Draw("hist")
    hPart.Draw("hist,same")
    lt2.AddEntry(hPart_even, "Particle-level truth, even","l")
    lt2.AddEntry(hPart, "Particle-level truth, odd","l")
    lt2.Draw()
    ct2.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_hPart_evenVsOdd"+isTwoStep+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+unfoldType+".png")

    ct3 = TCanvas("ct3", "", 800, 600)
    
    lt3 = TLegend(0.4, 0.65, 0.7, 0.9)
    lt3.SetFillStyle(0)
    lt3.SetTextFont(42)
    lt3.SetTextSize(0.045)
    lt3.SetBorderSize(0)
    
    hTrue_even.SetLineColor(2)
    hTrue_even.SetLineWidth(2)
    hTrue.SetLineColor(4)
    hTrue.SetLineWidth(2)
    hTrue_even.Draw("hist")
    hTrue.Draw("hist,same")
    lt3.AddEntry(hTrue_even, "Parton-level truth, even","l")
    lt3.AddEntry(hTrue, "Parton-level truth, odd","l")
    lt3.Draw()
    ct3.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_hTrue_evenVsOdd"+isTwoStep+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+unfoldType+".png")


# -------------------------------------------------------------------------------------
# do the actual unfolding
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# trigger SF for particle-level

if unfoldType == "_pt400" or unfoldType == "":
    if options.lepType == "ele":
        trigSF_rp = [1.32581, 1.37968, 1.43356, 1.48744, 1.62214]
    else:
        trigSF_rp = [1.20002, 1.20692, 1.21382, 1.22071, 1.23795]
elif unfoldType == "_full":
    if options.lepType == "ele":
        trigSF_rp = [0.0, 0.0, 0.0, 0.0, 1.32581, 1.37968, 1.43356, 1.48744, 1.62214, 0.0]
    else:
        trigSF_rp = [0.0, 0.0, 0.0, 0.0, 1.20002, 1.20692, 1.21382, 1.22071, 1.23795, 0.0]
elif unfoldType == "_full2":
    if options.lepType == "ele":
        if options.pdf == "scaleup":
            trigSF_rp = [0.0, 0.0, 1.3516, 1.40157, 1.45154, 1.50151, 1.62643, 0.0]
        elif options.pdf == "scaledown":
            trigSF_rp = [0.0, 0.0, 1.33585, 1.38794, 1.44003, 1.49212, 1.62236, 0.0]
        else:
            trigSF_rp = [0.0, 0.0, 1.32581, 1.37968, 1.43356, 1.48744, 1.62214, 0.0]
    else:
        if options.pdf == "scaleup":
            trigSF_rp = [0.0, 0.0, 1.17308, 1.17612, 1.17915, 1.18218, 1.18976, 0.0]
        elif options.pdf == "scaledown":
            trigSF_rp = [0.0, 0.0, 1.16728, 1.17801, 1.18873, 1.19946, 1.22627, 0.0]
        else:
            trigSF_rp = [0.0, 0.0, 1.20002, 1.20692, 1.21382, 1.22071, 1.23795, 0.0]
elif unfoldType == "_full3":
    if options.lepType == "ele":
        trigSF_rp = [0.0, 1.32581, 1.37968, 1.43356, 1.48744, 1.62214, 0.0]
    else:
        trigSF_rp = [0.0, 1.20002, 1.20692, 1.21382, 1.22071, 1.23795, 0.0]
else:
    print "invalid unfolding type option"


# -------------------------------------------------------------------------------------
# one-step unfolding
if options.twoStep == False:                
    
    print "------------ UNFOLDING (set: " + options.pdf + ", syst: " + options.syst + ") ------------"
    #unfold = RooUnfoldBayes(response, hMeas, 10);
    unfold = RooUnfoldSvd(response, hMeas, 2);
    #unfold = RooUnfoldTUnfold(response, hMeas);

    # get the unfolded distribution
    hReco = unfold.Hreco()

# -------------------------------------------------------------------------------------
# two-step unfolding
else :    
    
    print "------------ UNFOLD TO PARTICLE-LEVEL (set: " + options.pdf + ", syst: " + options.syst + ") ------------"
    #unfold_rp = RooUnfoldBayes(response_rp, hMeas, 10);
    unfold_rp = RooUnfoldSvd(response_rp, hMeas, 2);
    #unfold_rp = RooUnfoldTUnfold(response_rp, hMeas);

    # get the distribution unfolded to particle-level
    hReco_rp = unfold_rp.Hreco()

    # apply trigger SF correction for particle-level -> parton
    hRecoCorr_rp = hReco_rp.Clone()
    hRecoCorr_rp.SetName("hRecoCorr_rp")
    for ibin in range(1, hReco_rp.GetXaxis().GetNbins()+1 ) :
        hRecoCorr_rp.SetBinContent(ibin, hReco_rp.GetBinContent(ibin) * trigSF_rp[ibin-1] )
        hRecoCorr_rp.SetBinError(ibin, hReco_rp.GetBinError(ibin) * trigSF_rp[ibin-1] )

    print "------------ UNFOLD TO PARTON-LEVEL (set: " + options.pdf + ", syst: " + options.syst + ") ------------"
    #unfold = RooUnfoldBayes(response_pp, hRecoCorr_rp, 10);
    unfold = RooUnfoldSvd(response_pp, hRecoCorr_rp, 2);
    #unfold = RooUnfoldTUnfold(response_pp, hRecoCorr_rp);

    # get the distribution unfolded to parton-level
    hReco = unfold.Hreco()

    

# -------------------------------------------------------------------------------------
# Translate to cross section (not events) in bins of pt N/L/BR)
# -------------------------------------------------------------------------------------

hTrue.Scale(1.0/(lum*4/27)) # true @ parton level
hMeas.Scale(1.0/(lum*4/27)) # measured @ reco level
hReco.Scale(1.0/(lum*4/27)) # unfolded to parton level
if options.twoStep:
    hPart.Scale(1.0/(lum*4/27))    # true @ parton level
    hReco_rp.Scale(1.0/(lum*4/27)) # unfolded to particle level

## correct also to post-fit top-tagging SF !!! 
# nuisance_toptag = X +/- eX
# prior = 25%
# posterior_toptag = prior_toptag * (1.0 + 0.25*X) 

if options.pdf == "CT10_nom" and options.lepType == "muon" : 
    toptag_post = 1.10649440886
if options.pdf == "CT10_pdfup" and options.lepType == "muon" : 
    toptag_post = 1.06707266216
if options.pdf == "CT10_pdfdown" and options.lepType == "muon" : 
    toptag_post = 1.13966730776
if options.pdf == "MSTW_nom" and options.lepType == "muon" : 
    toptag_post = 1.10744665435
if options.pdf == "MSTW_pdfup" and options.lepType == "muon" : 
    toptag_post = 1.09450114957
if options.pdf == "MSTW_pdfdown" and options.lepType == "muon" : 
    toptag_post = 1.13594832035
if options.pdf == "NNPDF_nom" and options.lepType == "muon" : 
    toptag_post = 1.16550559607
if options.pdf == "NNPDF_pdfup" and options.lepType == "muon" : 
    toptag_post = 1.11834541764
if options.pdf == "NNPDF_pdfdown" and options.lepType == "muon" : 
    toptag_post = 1.40246183384
if options.pdf == "scaleup" and options.lepType == "muon" : 
    toptag_post = 1.06423533136
if options.pdf == "scaledown" and options.lepType == "muon" : 
    toptag_post = 1.19994741704
if options.pdf == "CT10_nom" and options.lepType == "ele" : 
    toptag_post = 1.09579275566
if options.pdf == "CT10_pdfup" and options.lepType == "ele" : 
    toptag_post = 1.07216881228
if options.pdf == "CT10_pdfdown" and options.lepType == "ele" : 
    toptag_post = 1.11804095015
if options.pdf == "MSTW_nom" and options.lepType == "ele" : 
    toptag_post = 1.09751083131
if options.pdf == "MSTW_pdfup" and options.lepType == "ele" : 
    toptag_post = 1.0842812137
if options.pdf == "MSTW_pdfdown" and options.lepType == "ele" : 
    toptag_post = 1.1092318743
if options.pdf == "NNPDF_nom" and options.lepType == "ele" : 
    toptag_post = 1.10402528198
if options.pdf == "NNPDF_pdfup" and options.lepType == "ele" : 
    toptag_post = 1.08350599359
if options.pdf == "NNPDF_pdfdown" and options.lepType == "ele" : 
    toptag_post = 1.11391002882
if options.pdf == "scaleup" and options.lepType == "ele" : 
    toptag_post = 1.16876619788
if options.pdf == "scaledown" and options.lepType == "ele" : 
    toptag_post = 1.15662221006


#if options.closureTest == False : 
#    hMeas.Scale(1.0/toptag_post)
#    hReco.Scale(1.0/toptag_post)
#    if options.twoStep:
#        hReco_rp.Scale(1.0/toptag_post)

    
# -------------------------------------------------------------------------------------
# Correct for selection bias in requiring trigger & bin width
# -------------------------------------------------------------------------------------

## trigger SF (this is for correcting parton-level distribution & one-step unfolded distribution @ parton-level 

if unfoldType == "_full":
    if options.lepType == "ele":
        trigSF = [0.0, 0.0, 0.0, 0.0, 1.6879, 1.73525, 1.78259, 1.82994, 1.94831, 0.0]
    else:
        trigSF = [0.0, 0.0, 0.0, 0.0, 1.62046, 1.58152, 1.54259, 1.50365, 1.4063, 0.0]
elif unfoldType == "_full2":
    if options.lepType == "ele":
        if options.pdf == "scaleup":
            trigSF = [0.0, 0.0, 1.67745, 1.71964, 1.76184, 1.80403, 1.90952, 0.0]
        elif options.pdf == "scaledown":
            trigSF = [0.0, 0.0, 1.69947, 1.72769, 1.75592, 1.78415, 1.85471, 0.0]
        else:
            trigSF = [0.0, 0.0, 1.6879, 1.73525, 1.78259, 1.82994, 1.94831, 0.0]
    else:
        if options.pdf == "scaleup":
            trigSF = [0.0, 0.0, 1.57944, 1.56532, 1.55121, 1.5371, 1.50182, 0.0]
        elif options.pdf == "scaledown":
            trigSF = [0.0, 0.0, 1.56584, 1.55551, 1.54517, 1.53484, 1.509, 0.0]
        else:
            trigSF = [0.0, 0.0, 1.62046, 1.58152, 1.54259, 1.50365, 1.4063, 0.0]
elif unfoldType == "_full3":
    if options.lepType == "ele":
        trigSF = [0.0, 1.6879, 1.73525, 1.78259, 1.82994, 1.94831, 0.0]
    else:
        trigSF = [0.0, 1.62046, 1.58152, 1.54259, 1.50365, 1.4063, 0.0]
elif unfoldType == "_pt400" or unfoldType == "":
    if options.lepType == "ele":
        trigSF = [1.6879, 1.73525, 1.78259, 1.82994, 1.94831]
    else:
        trigSF = [1.62046, 1.58152, 1.54259, 1.50365, 1.4063]
else:
    print "Unvalid unfolding type!!" 

    
sumReco = 0
sumTrue = 0
sumMeas = 0
sumReco_rp = 0
sumPart = 0
for ibin in range(1, hTrue.GetXaxis().GetNbins()+1 ) :

    width = hTrue.GetBinWidth(ibin)
    
    # correct top-quark pt @ gen-level for trigger bias (for both one-step & two-step)
    hTrue.SetBinContent(ibin, hTrue.GetBinContent(ibin) * trigSF[ibin-1] / width )
    hTrue.SetBinError(ibin, hTrue.GetBinError(ibin) * trigSF[ibin-1] / width )

    # correct one-step unfolded distribution for trigger bias
    if options.twoStep == False:
        hReco.SetBinContent(ibin, hReco.GetBinContent(ibin) * trigSF[ibin-1] / width )
        hReco.SetBinError(ibin, hReco.GetBinError(ibin) * trigSF[ibin-1] / width )
    else:
        hReco.SetBinContent(ibin, hReco.GetBinContent(ibin) / width )
        hReco.SetBinError(ibin, hReco.GetBinError(ibin) / width )
        hReco_rp.SetBinContent(ibin, hReco_rp.GetBinContent(ibin) * trigSF_rp[ibin-1] / width )
        hReco_rp.SetBinError(ibin, hReco_rp.GetBinError(ibin) * trigSF_rp[ibin-1] / width )
        hPart.SetBinContent(ibin, hPart.GetBinContent(ibin) * trigSF_rp[ibin-1] / width )
        hPart.SetBinError(ibin, hPart.GetBinError(ibin) * trigSF_rp[ibin-1] / width )
            
    
    # correct measured distribution for bin width
    hMeas.SetBinContent(ibin,  hMeas.GetBinContent(ibin) / width )
    hMeas.SetBinError(ibin,  hMeas.GetBinError(ibin) / width )
    
    sumReco += hReco.GetBinContent(ibin)*width
    sumTrue += hTrue.GetBinContent(ibin)*width
    sumMeas += hMeas.GetBinContent(ibin)*width
    if options.twoStep:
        sumReco_rp += hReco_rp.GetBinContent(ibin)*width
        sumPart += hPart.GetBinContent(ibin)*width
    

# -------------------------------------------------------------------------------------
# print & draw
# -------------------------------------------------------------------------------------

## ratio of unfolded data to generator-level 
hFrac = hReco.Clone()
hFrac.SetName("hFrac")
hFrac.SetTitle(";Top quark p_{T} [GeV];Data/MC")
hFrac.Divide(hTrue)

## ratio of unfolded data to particle-level 
if options.twoStep:
    hFrac_rp = hReco_rp.Clone()
    hFrac_rp.SetName("hFrac_rp")
    hFrac_rp.SetTitle(";Particle-level top p_{T} [GeV];Data/MC")
    hFrac_rp.Divide(hPart)


bin400 = hMeas.GetXaxis().FindBin(400.)
binmax = hMeas.GetXaxis().FindBin(10000.)

print 'htrue = ' + str(hTrue.Integral(bin400,binmax))
print 'hmeas = ' + str(hMeas.Integral(bin400,binmax))
print 'hreco = ' + str(hReco.Integral(bin400,binmax))
if options.twoStep:
    print 'hreco_rp = ' + str(hReco_rp.Integral(bin400,binmax))
    print 'hpart    = ' + str(hPart.Integral(bin400,binmax))
        
print 'true sigma = ' + str(sumTrue)
print 'meas sigma = ' + str(sumMeas)
print 'reco sigma = ' + str(sumReco)
if options.twoStep:
    print 'reco_rp sigma = ' + str(sumReco_rp)
    print 'part sigma    = ' + str(sumPart)


# -------------------------------------------------------------------------------------
# draw parton-level unfolding
# -------------------------------------------------------------------------------------

c1 = TCanvas("c", "c", 700, 700)
pad1 =  TPad("pad1","pad1",0,0.3,1,1)
pad1.SetBottomMargin(0.05);
pad1.Draw();
pad1.cd();

#unfold.PrintTable (cout, hTrue);
hReco.SetMarkerStyle(21)
hMeas.SetMarkerStyle(25);

hReco.GetXaxis().SetRangeUser(400.,1200.)
hTrue.GetXaxis().SetRangeUser(400.,1200.)
hMeas.GetXaxis().SetRangeUser(400.,1200.)

hReco.SetTitle(";;d#sigma/dp_{T} [fb/GeV]")
hReco.GetYaxis().SetTitleOffset(1.2)
hReco.SetMinimum(0.0)
max = hTrue.GetMaximum()
max2 = hReco.GetMaximum()
if max2 > max:
	max = max2
hReco.SetAxisRange(0,max*1.07,"Y")
hReco.Draw()
hTrue.Draw('hist same')
hMeas.Draw('same')
hTrue.UseCurrentStyle()
hTrue.SetLineColor(4);
hTrue.GetYaxis().SetTitleSize(25)
hTrue.GetXaxis().SetLabelSize(0)


leg = TLegend(0.45, 0.55, 0.85, 0.75)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.045)
leg.SetBorderSize(0)

if options.closureTest == False : 
    leg.AddEntry( hReco, 'Unfolded data', 'p')
    leg.AddEntry( hTrue, 'Generated', 'l')
    leg.AddEntry( hMeas, 'Raw data', 'p')
else : 
    leg.AddEntry( hReco, 'Unfolded MC: Closure test', 'p')
    leg.AddEntry( hTrue, 'Generated', 'l')
    leg.AddEntry( hMeas, 'Raw MC', 'p')

leg.Draw()


# write histograms to file
if options.closureTest:
    hReco.SetName("UnfoldedMC")
else:
    hReco.SetName("UnfoldedData")

hReco.Write()
hTrue.Write()
hMeas.Write()


text1 = TLatex()
text1.SetNDC()
text1.SetTextFont(42)
#text1.DrawLatex(0.20,0.87, "#scale[1.0]{CMS Preliminary, L = 19.7 fb^{-1} at  #sqrt{s} = 8 TeV}")
text1.DrawLatex(0.5,0.8, "#scale[1.0]{L = 19.7 fb^{-1} at #sqrt{s} = 8 TeV}")


c1.cd();
pad2 =  TPad("pad2","pad2",0,0.0,1,0.28)
pad2.SetTopMargin(0.05);
pad2.SetBottomMargin(0.4);
pad2.Draw();
pad2.cd();
hFrac.SetMaximum(2.0)
hFrac.SetMinimum(0.0)
hFrac.UseCurrentStyle()
hFrac.GetYaxis().SetTitleSize(25)
hFrac.GetYaxis().SetTitleOffset(2.0)
hFrac.GetXaxis().SetTitleOffset(4.0)
hFrac.GetXaxis().SetLabelSize(25)
hFrac.GetYaxis().SetNdivisions(2,4,0,False)

hFrac.Draw("e")
hFrac.GetXaxis().SetRangeUser(400., 1200.)

c1.Update()

append = ""
if options.twoStep :
    append += "_2step"
if options.closureTest :
    append += "_closure"

#postfit = "_postfit"
postfit = ""
c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+append+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+unfoldType+postfit+".pdf", "pdf")
c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+append+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+unfoldType+postfit+".png", "png")
c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+append+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+unfoldType+postfit+".eps", "eps")



# -------------------------------------------------------------------------------------
# draw particle-level unfolding
# -------------------------------------------------------------------------------------

if options.twoStep:
    pad1.cd();

    hReco_rp.SetMarkerStyle(21)
    hMeas.SetMarkerStyle(25);

    hReco_rp.GetXaxis().SetRangeUser(400.,1200.)
    hPart.GetXaxis().SetRangeUser(400.,1200.)
    hMeas.GetXaxis().SetRangeUser(400.,1200.)

    hReco_rp.SetTitle(";;d#sigma/dp_{T} [fb/GeV]")
    hReco_rp.GetYaxis().SetTitleOffset(1.2)
    hReco_rp.SetMinimum(0.0)
    max = hPart.GetMaximum()
    max2 = hReco_rp.GetMaximum()
    if max2 > max:
        max = max2
    hReco_rp.SetAxisRange(0,max*1.07,"Y")
    hReco_rp.Draw()
    hPart.Draw('hist same')
    hMeas.Draw('same')
    hPart.UseCurrentStyle()
    hPart.SetLineColor(4);
    hPart.GetYaxis().SetTitleSize(25)
    hPart.GetXaxis().SetLabelSize(0)

        
    leg2 = TLegend(0.45, 0.55, 0.85, 0.75)
    leg2.SetFillStyle(0)
    leg2.SetTextFont(42)
    leg2.SetTextSize(0.045)
    leg2.SetBorderSize(0)

    if options.closureTest == False : 
        leg2.AddEntry( hReco_rp, 'Unfolded data', 'p')
        leg2.AddEntry( hTrue, 'Generated', 'l')
        leg2.AddEntry( hMeas, 'Raw data', 'p')
    else : 
        leg2.AddEntry( hReco_rp, 'Unfolded MC: Closure test', 'p')
        leg2.AddEntry( hTrue, 'Generated', 'l')
        leg2.AddEntry( hMeas, 'Raw MC', 'p')
    
    leg2.Draw()

    # write histograms to file
    if options.closureTest:
        hReco_rp.SetName("UnfoldedMC_rp")
    else:
        hReco_rp.SetName("UnfoldedData_rp")

    hReco_rp.Write()
    hPart.Write()
    hMeas.Write()

    text1.DrawLatex(0.5,0.8, "#scale[1.0]{L = 19.7 fb^{-1} at #sqrt{s} = 8 TeV}")

    c1.cd()
    pad2.cd()

    hFrac_rp.SetMaximum(2.0)
    hFrac_rp.SetMinimum(0.0)
    hFrac_rp.UseCurrentStyle()
    hFrac_rp.GetYaxis().SetTitleSize(25)
    hFrac_rp.GetYaxis().SetTitleOffset(2.0)
    hFrac_rp.GetXaxis().SetTitleOffset(4.0)
    hFrac_rp.GetXaxis().SetLabelSize(25)
    hFrac_rp.GetYaxis().SetNdivisions(2,4,0,False)

    hFrac_rp.Draw("e")
    hFrac_rp.GetXaxis().SetRangeUser(400., 1200.)

    c1.Update()

    append = ""
    if options.closureTest :
        append += "_closure"
        
    c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+"_2step_particle"+append+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+unfoldType+postfit+".pdf", "pdf")
    c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+"_2step_particle"+append+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+unfoldType+postfit+".png", "png")
    c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+"_2step_particle"+append+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+unfoldType+postfit+".eps", "eps")



# -------------------------------------------------------------------------------------
# plot response matrices 
# (do this in the end as the normalization otherwise will mess up the unfolding result!)
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# one-step unfolding
# -------------------------------------------------------------------------------------

gStyle.SetPadRightMargin(0.12);
cr = TCanvas("c_response", "", 800, 600)

if options.twoStep == False:
    
    hEmpty2D = response.Hresponse().Clone()
    hEmpty2D.SetName("empty2D")
    hEmpty2D.Reset()
    hEmpty2D.GetXaxis().SetTitle("Top-tagged jet p_{T} [GeV]")
    hEmpty2D.GetYaxis().SetTitle("Top quark p_{T} [GeV]")
    hEmpty2D.GetXaxis().SetLabelSize(0.045)
    hEmpty2D.GetYaxis().SetLabelSize(0.045)
    hEmpty2D.Draw()
    hResponse2D = response.Hresponse().Clone()
    hResponse2D.SetName("plottedResponse")
    
    # normalize so that for each bin of true top quark pt, the bins in measured top pt add up to 100%
    nbinsX = hResponse2D.GetNbinsX()
    nbinsY = hResponse2D.GetNbinsY()
    for iby in range(1,nbinsY+1) :
        rowIntegral = hResponse2D.Integral(1,nbinsX,iby,iby)
        #print "for y-bin " + str(iby) + " row integral = " + str(rowIntegral)
        for ibx in range(1,nbinsX+1) :
            binContent = hResponse2D.GetBinContent(ibx,iby)
            newContent = 0
            if rowIntegral > 0:
                newContent = binContent/rowIntegral*100.0
            #print "bin content x-bin " + str(ibx) + " y-bin " + str(iby) + " binContent " + str(binContent) + " newContent " + str(newContent)
            hResponse2D.SetBinContent(ibx,iby,newContent)

    gStyle.SetPaintTextFormat(".1f")
    hResponse2D.Draw("colz,same,text")
    hEmpty2D.Draw("axis,same")
    cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_responseMatrix_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".png")
    cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_responseMatrix_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".eps")
    cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_responseMatrix_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".pdf")

    hEmpty2D.SetAxisRange(450,1150,"X")
    hEmpty2D.SetAxisRange(450,1150,"Y")
    hResponse2D.SetAxisRange(450,1150,"X")
    hResponse2D.SetAxisRange(450,1150,"Y")
    hEmpty2D.Draw()
    hResponse2D.Draw("colz,same,text")
    hEmpty2D.Draw("axis,same")
    cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_responseMatrix_zoom_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".png")
    cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_responseMatrix_zoom_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".eps")
    cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_responseMatrix_zoom_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".pdf")

    response.Hresponse().SetName("responseMatrix_"+options.syst)
    response.Hresponse().Write()
    

# -------------------------------------------------------------------------------------
# two-step unfolding
# -------------------------------------------------------------------------------------

if options.twoStep:

    # -------------------------------------------------------------------------------------
    ### reco to particle level
    hEmpty2D_rp = response_rp.Hresponse().Clone()
    hEmpty2D_rp.SetName("empty2D_rp")
    hEmpty2D_rp.Reset()
    hEmpty2D_rp.GetXaxis().SetTitle("Top-tagged jet p_{T} [GeV]")
    hEmpty2D_rp.GetYaxis().SetTitle("Particle-level top p_{T} [GeV]")
    hEmpty2D_rp.GetXaxis().SetLabelSize(0.045)
    hEmpty2D_rp.GetYaxis().SetLabelSize(0.045)
    hEmpty2D_rp.Draw()
    hResponse2D_rp = response_rp.Hresponse().Clone()
    hResponse2D_rp.SetName("plottedResponse_rp")

    if options.troubleshoot :
        hEmpty2D_rp_even = response_rp_even.Hresponse().Clone()
        hEmpty2D_rp_even.SetName("empty2D_rp_even")
        hEmpty2D_rp_even.Reset()
        hEmpty2D_rp_even.GetXaxis().SetTitle("Top-tagged jet p_{T} [GeV]")
        hEmpty2D_rp_even.GetYaxis().SetTitle("Particle-level top p_{T} [GeV]")
        hEmpty2D_rp_even.GetXaxis().SetLabelSize(0.045)
        hEmpty2D_rp_even.GetYaxis().SetLabelSize(0.045)
        #hEmpty2D_rp_even.Draw()
        hResponse2D_rp_even = response_rp_even.Hresponse().Clone()
        hResponse2D_rp_even.SetName("plottedResponse_rp_even")

        hEmpty2D_rp.Draw()
        gStyle.SetPaintTextFormat(".1f")
        hResponse2D_rp.Draw("colz,same,text")
        hEmpty2D_rp.Draw("axis,same")
        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_responseMatrix_rp_odd_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".png")

        hEmpty2D_rp_even.Draw()
        gStyle.SetPaintTextFormat(".1f")
        hResponse2D_rp_even.Draw("colz,same,text")
        hEmpty2D_rp_even.Draw("axis,same")
        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_responseMatrix_rp_even_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".png")
    
    # normalize so that for each bin of particle-level top pt, the bins in measured top pt add up to 100%
    nbinsX = hResponse2D_rp.GetNbinsX()
    nbinsY = hResponse2D_rp.GetNbinsY()
    for iby in range(1,nbinsY+1) :
        rowIntegral = hResponse2D_rp.Integral(1,nbinsX,iby,iby)
        #print "for y-bin " + str(iby) + " row integral = " + str(rowIntegral)
        for ibx in range(1,nbinsX+1) :
            binContent = hResponse2D_rp.GetBinContent(ibx,iby)
            newContent = 0
            if rowIntegral > 0:
                newContent = binContent/rowIntegral*100.0
            #print "bin content x-bin " + str(ibx) + " y-bin " + str(iby) + " binContent " + str(binContent) + " newContent " + str(newContent)
            hResponse2D_rp.SetBinContent(ibx,iby,newContent)

    hEmpty2D_rp.Draw()
    gStyle.SetPaintTextFormat(".1f")
    hResponse2D_rp.Draw("colz,same,text")
    hEmpty2D_rp.Draw("axis,same")
    cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_rp_"+options.pdf+"_"+options.syst+nobtag+unfoldType+postfit+".png")
    cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_rp_"+options.pdf+"_"+options.syst+nobtag+unfoldType+postfit+".eps")
    cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_rp_"+options.pdf+"_"+options.syst+nobtag+unfoldType+postfit+".pdf")
    
    hEmpty2D_rp.SetAxisRange(450,1150,"X")
    hEmpty2D_rp.SetAxisRange(450,1150,"Y")
    hResponse2D_rp.SetAxisRange(450,1150,"X")
    hResponse2D_rp.SetAxisRange(450,1150,"Y")
    hEmpty2D_rp.Draw()
    hResponse2D_rp.Draw("colz,same,text")
    hEmpty2D_rp.Draw("axis,same")
    cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_rp_zoom_"+options.pdf+"_"+options.syst+nobtag+unfoldType+postfit+".png")
    cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_rp_zoom_"+options.pdf+"_"+options.syst+nobtag+unfoldType+postfit+".eps")
    cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_rp_zoom_"+options.pdf+"_"+options.syst+nobtag+unfoldType+postfit+".pdf")


    response_rp.Hresponse().SetName("responseMatrix_rp_"+options.syst)
    response_rp.Hresponse().Write()
    
    
    # -------------------------------------------------------------------------------------
    ### particle level to parton level 
    hEmpty2D_pp = response_pp.Hresponse().Clone()
    hEmpty2D_pp.SetName("empty2D_pp")
    hEmpty2D_pp.Reset()
    hEmpty2D_pp.GetXaxis().SetTitle("Particle-level top p_{T} [GeV]")
    hEmpty2D_pp.GetYaxis().SetTitle("Top quark p_{T} [GeV]")
    hEmpty2D_pp.GetXaxis().SetLabelSize(0.045)
    hEmpty2D_pp.GetYaxis().SetLabelSize(0.045)
    #hEmpty2D_pp.SetAxisRange(0,1100,"X")
    hEmpty2D_pp.Draw()
    hResponse2D_pp = response_pp.Hresponse().Clone()
    hResponse2D_pp.SetName("plottedResponse_pp")

    if options.troubleshoot :
        hEmpty2D_pp_even = response_pp_even.Hresponse().Clone()
        hEmpty2D_pp_even.SetName("empty2D_pp_even")
        hEmpty2D_pp_even.Reset()
        hEmpty2D_pp_even.GetXaxis().SetTitle("Particle-level top p_{T} [GeV]")
        hEmpty2D_pp_even.GetYaxis().SetTitle("Top quark p_{T} [GeV]")
        hEmpty2D_pp_even.GetXaxis().SetLabelSize(0.045)
        hEmpty2D_pp_even.GetYaxis().SetLabelSize(0.045)
        #hEmpty2D_pp_even.Draw()
        hResponse2D_pp_even = response_pp_even.Hresponse().Clone()
        hResponse2D_pp_even.SetName("plottedResponse_pp_even")

        hEmpty2D_pp.Draw()
        gStyle.SetPaintTextFormat(".1f")
        hResponse2D_pp.Draw("colz,same,text")
        hEmpty2D_pp.Draw("axis,same")
        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_responseMatrix_pp_odd_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".png")
        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_responseMatrix_pp_odd_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".eps")
        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_responseMatrix_pp_odd_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".pdf")

        hEmpty2D_pp_even.Draw()
        gStyle.SetPaintTextFormat(".1f")
        hResponse2D_pp_even.Draw("colz,same,text")
        hEmpty2D_pp_even.Draw("axis,same")
        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_responseMatrix_pp_even_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".png")
        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_responseMatrix_pp_even_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".eps")
        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_responseMatrix_pp_even_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".pdf")
    
    # normalize so that for each bin of particle-level top pt, the bins in measured top pt add up to 100%
    nbinsX = hResponse2D_pp.GetNbinsX()
    nbinsY = hResponse2D_pp.GetNbinsY()
    for iby in range(1,nbinsY+1) :
        rowIntegral = hResponse2D_pp.Integral(1,nbinsX,iby,iby)
        #print "for y-bin " + str(iby) + " row integral = " + str(rowIntegral)
        for ibx in range(1,nbinsX+1) :
            binContent = hResponse2D_pp.GetBinContent(ibx,iby)
            newContent = 0
            if rowIntegral > 0:
                newContent = binContent/rowIntegral*100.0
            #print "bin content x-bin " + str(ibx) + " y-bin " + str(iby) + " binContent " + str(binContent) + " newContent " + str(newContent)
            hResponse2D_pp.SetBinContent(ibx,iby,newContent)

    gStyle.SetPaintTextFormat(".1f")
    hResponse2D_pp.Draw("colz,same,text")
    hEmpty2D_pp.Draw("axis,same")
    cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_pp_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".png")
    cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_pp_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".eps")
    cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_pp_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".pdf")
    
    hEmpty2D_pp.SetAxisRange(450,1150,"X")
    hEmpty2D_pp.SetAxisRange(450,1150,"Y")
    hResponse2D_pp.SetAxisRange(450,1150,"X")
    hResponse2D_pp.SetAxisRange(450,1150,"Y")
    hEmpty2D_pp.Draw()
    hResponse2D_pp.Draw("colz,same,text")
    hEmpty2D_pp.Draw("axis,same")
    cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_pp_zoom_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".png")
    cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_pp_zoom_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".eps")
    cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_pp_zoom_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".pdf")

    response_pp.Hresponse().SetName("responseMatrix_pp_"+options.syst)
    response_pp.Hresponse().Write()



fout.Close()
