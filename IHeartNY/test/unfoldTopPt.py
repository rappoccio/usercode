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

parser.add_option('--normalize', metavar='F', action='store_true',
                  default=True,
                  dest='normalize',
                  help='Do normalized differential cross section')

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
# *** these are using the combined fit result ***
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
    n_ttbarnonsemilep = [29.5454, 31.7288, 27.362, 74.3116, 79.8033, 68.8199]   #unfold
    n_wjets           = [3.84511, 4.14691, 3.5433, 155.559, 167.769, 143.349]   #unfold
    n_singletop       = [4.1156, 6.03127, 2.19993, 18.5079, 27.1227, 9.8931]   #unfold
    n_qcd             = [3.24901, 4.65408, 1.84395, 18.1419, 25.9874, 10.2963]   #unfold
if options.pdf == "CT10_pdfup" and options.lepType == "muon" :   #unfold
    n_ttbarnonsemilep = [29.6872, 32.0514, 27.3231, 74.8188, 80.777, 68.8606]   #unfold
    n_wjets           = [3.48582, 3.80286, 3.16878, 141.044, 153.872, 128.216]   #unfold
    n_singletop       = [4.26181, 6.08828, 2.43534, 19.1602, 27.3717, 10.9488]   #unfold
    n_qcd             = [3.22307, 4.62543, 1.8207, 17.997, 25.8275, 10.1664]   #unfold
if options.pdf == "CT10_pdfdown" and options.lepType == "muon" :   #unfold
    n_ttbarnonsemilep = [29.2976, 31.3514, 27.2437, 73.745, 78.9148, 68.5752]   #unfold
    n_wjets           = [4.12607, 4.41843, 3.83371, 166.834, 178.655, 155.012]   #unfold
    n_singletop       = [4.06546, 6.05067, 2.08025, 18.2779, 27.2032, 9.35258]   #unfold
    n_qcd             = [3.21379, 4.61857, 1.809, 17.9452, 25.7892, 10.1011]   #unfold
if options.pdf == "MSTW_nom" and options.lepType == "muon" :   #unfold
    n_ttbarnonsemilep = [30.0253, 32.2625, 27.788, 75.6538, 81.291, 70.0167]   #unfold
    n_wjets           = [4.51859, 4.86389, 4.17329, 181.614, 195.492, 167.735]   #unfold
    n_singletop       = [3.10571, 4.53451, 1.67692, 13.7171, 20.0276, 7.40646]   #unfold
    n_qcd             = [1.4205, 2.039, 0.802001, 8.91098, 12.7909, 5.03105]   #unfold
if options.pdf == "MSTW_pdfup" and options.lepType == "muon" :   #unfold
    n_ttbarnonsemilep = [29.6667, 31.9876, 27.3457, 74.7976, 80.6493, 68.9459]   #unfold
    n_wjets           = [3.77654, 4.07085, 3.48222, 152.73, 164.632, 140.827]   #unfold
    n_singletop       = [4.36679, 6.2535, 2.48008, 19.6357, 28.1195, 11.1519]   #unfold
    n_qcd             = [3.19734, 4.59454, 1.80014, 17.8533, 25.655, 10.0516]   #unfold
if options.pdf == "MSTW_pdfdown" and options.lepType == "muon" :   #unfold
    n_ttbarnonsemilep = [29.6932, 31.8374, 27.549, 74.5324, 79.9145, 69.1504]   #unfold
    n_wjets           = [4.08374, 4.35902, 3.80846, 164.957, 176.076, 153.837]   #unfold
    n_singletop       = [4.10387, 6.04757, 2.16016, 18.4372, 27.1696, 9.70485]   #unfold
    n_qcd             = [3.12785, 4.52659, 1.72911, 17.4653, 25.2756, 9.65504]   #unfold
if options.pdf == "NNPDF_nom" and options.lepType == "muon" :   #unfold
    n_ttbarnonsemilep = [29.2599, 31.4221, 27.0978, 73.5471, 78.9818, 68.1124]   #unfold
    n_wjets           = [4.01603, 4.3159, 3.71617, 162.739, 174.89, 150.587]   #unfold
    n_singletop       = [4.26249, 6.19837, 2.32661, 19.2003, 27.9204, 10.4802]   #unfold
    n_qcd             = [3.59548, 5.00361, 2.18736, 20.0765, 27.9392, 12.2138]   #unfold
if options.pdf == "NNPDF_pdfup" and options.lepType == "muon" :   #unfold
    n_ttbarnonsemilep = [29.9064, 32.298, 27.5147, 73.9191, 79.8304, 68.0077]   #unfold
    n_wjets           = [3.71731, 4.03376, 3.40086, 150.297, 163.091, 137.502]   #unfold
    n_singletop       = [4.59115, 6.46155, 2.72074, 20.6152, 29.0137, 12.2167]   #unfold
    n_qcd             = [3.35005, 4.75569, 1.94441, 18.706, 26.5548, 10.8572]   #unfold
if options.pdf == "NNPDF_pdfdown" and options.lepType == "muon" :   #unfold
    n_ttbarnonsemilep = [28.4181, 30.4602, 26.376, 74.0566, 79.3782, 68.7349]   #unfold
    n_wjets           = [4.28231, 4.5759, 3.98873, 173.532, 185.429, 161.635]   #unfold
    n_singletop       = [4.55516, 6.54825, 2.56207, 20.5461, 29.5359, 11.5562]   #unfold
    n_qcd             = [3.63054, 5.04976, 2.21133, 20.2722, 28.1969, 12.3476]   #unfold
if options.pdf == "scaleup" and options.lepType == "muon" :   #unfold
    n_ttbarnonsemilep = [29.1199, 31.2431, 26.9967, 73.1421, 78.4751, 67.8092]   #unfold
    n_wjets           = [4.17536, 4.45188, 3.89884, 167.269, 178.347, 156.191]   #unfold
    n_singletop       = [4.3735, 6.35102, 2.39599, 19.4241, 28.2069, 10.6414]   #unfold
    n_qcd             = [3.20629, 4.5915, 1.82107, 17.9033, 25.638, 10.1685]   #unfold
if options.pdf == "scaledown" and options.lepType == "muon" :   #unfold
    n_ttbarnonsemilep = [27.2267, 29.352, 25.1014, 77.0442, 83.0582, 71.0303]   #unfold
    n_wjets           = [4.47126, 4.77589, 4.16663, 166.264, 177.592, 154.937]   #unfold
    n_singletop       = [4.55842, 6.46376, 2.65309, 20.5063, 29.0776, 11.9351]   #unfold
    n_qcd             = [2.93531, 4.30665, 1.56396, 16.3902, 24.0475, 8.73285]   #unfold
    
### electron channel
if options.pdf == "CT10_nom" and options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [30.4236, 32.672, 28.1753, 70.4531, 75.6596, 65.2465]   #unfold
    n_wjets           = [2.69465, 2.90616, 2.48315, 130.705, 140.964, 120.446]   #unfold
    n_singletop       = [3.23182, 4.73612, 1.72752, 15.1449, 22.1944, 8.09549]   #unfold
    n_qcd             = [10.4881, 11.1397, 9.8365, 78.1238, 82.9773, 73.2703]   #unfold
if options.pdf == "CT10_pdfup" and options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [31.0298, 33.5009, 28.5587, 71.7269, 77.4389, 66.0149]   #unfold
    n_wjets           = [2.44589, 2.66835, 2.22343, 118.454, 129.228, 107.681]   #unfold
    n_singletop       = [3.33209, 4.76012, 1.90407, 15.663, 22.3757, 8.95036]   #unfold
    n_qcd             = [10.4024, 11.0573, 9.74747, 77.4854, 82.3637, 72.6071]   #unfold
if options.pdf == "CT10_pdfdown" and options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [29.8529, 31.9457, 27.7601, 69.4357, 74.3034, 64.568]   #unfold
    n_wjets           = [2.89077, 3.0956, 2.68594, 140.116, 150.045, 130.188]   #unfold
    n_singletop       = [3.17698, 4.72834, 1.62562, 14.9404, 22.2359, 7.64481]   #unfold
    n_qcd             = [10.597, 11.2433, 9.95063, 78.9348, 83.7492, 74.1204]   #unfold
if options.pdf == "MSTW_nom" and options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [32.5295, 34.9534, 30.1056, 77.6335, 83.4182, 71.8488]   #unfold
    n_wjets           = [5.33551, 5.74324, 4.92779, 202.842, 218.342, 187.341]   #unfold
    n_singletop       = [3.09066, 4.51253, 1.66879, 14.1608, 20.6756, 7.64606]   #unfold
    n_qcd             = [15.1826, 16.1222, 14.2429, 205.423, 218.136, 192.709]   #unfold
if options.pdf == "MSTW_pdfup" and options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [30.2959, 32.6661, 27.9257, 69.133, 74.5416, 63.7244]   #unfold
    n_wjets           = [2.65105, 2.85765, 2.44444, 128.026, 138.004, 118.049]   #unfold
    n_singletop       = [3.374, 4.83177, 1.91623, 15.9862, 22.8932, 9.07924]   #unfold
    n_qcd             = [10.4802, 11.1303, 9.83011, 78.0649, 82.9072, 73.2227]   #unfold
if options.pdf == "MSTW_pdfdown" and options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [29.4834, 31.6124, 27.3544, 68.3667, 73.3035, 63.4299]   #unfold
    n_wjets           = [2.86815, 3.06149, 2.67481, 138.079, 147.386, 128.771]   #unfold
    n_singletop       = [3.1211, 4.59934, 1.64286, 14.9587, 22.0436, 7.87385]   #unfold
    n_qcd             = [10.5141, 11.1634, 9.86484, 78.3175, 83.1537, 73.4813]   #unfold
if options.pdf == "NNPDF_nom" and options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [29.9561, 32.1696, 27.7425, 68.9934, 74.0916, 63.8952]   #unfold
    n_wjets           = [2.81272, 3.02274, 2.6027, 136.948, 147.174, 126.723]   #unfold
    n_singletop       = [3.41655, 4.96823, 1.86487, 15.7704, 22.9328, 8.60801]   #unfold
    n_qcd             = [10.5615, 11.2205, 9.90251, 78.6707, 83.5796, 73.7619]   #unfold
if options.pdf == "NNPDF_pdfup" and options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [30.0837, 32.4895, 27.6779, 69.5541, 75.1164, 63.9917]   #unfold
    n_wjets           = [2.60593, 2.82776, 2.38409, 126.424, 137.186, 115.662]   #unfold
    n_singletop       = [3.59811, 5.06395, 2.13226, 16.9029, 23.789, 10.0168]   #unfold
    n_qcd             = [10.54, 11.1946, 9.88535, 78.5103, 83.3866, 73.6341]   #unfold
if options.pdf == "NNPDF_pdfdown" and options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [30.1898, 32.3592, 28.0204, 70.061, 75.0955, 65.0265]   #unfold
    n_wjets           = [2.99923, 3.20485, 2.79361, 145.669, 155.656, 135.683]   #unfold
    n_singletop       = [3.62101, 5.20537, 2.03665, 16.7915, 24.1385, 9.44444]   #unfold
    n_qcd             = [10.4654, 11.1311, 9.79968, 77.9548, 82.9136, 72.996]   #unfold
if options.pdf == "scaleup" and options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [30.5948, 32.8256, 28.3641, 67.7576, 72.698, 62.8173]   #unfold
    n_wjets           = [2.9727, 3.16958, 2.77583, 138.739, 147.928, 129.551]   #unfold
    n_singletop       = [2.87133, 4.16962, 1.57303, 15.3831, 22.3388, 8.42754]   #unfold
    n_qcd             = [11.644, 12.2664, 11.0217, 86.7342, 91.3703, 82.0982]   #unfold
if options.pdf == "scaledown" and options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [31.4704, 33.9269, 29.0139, 65.4972, 70.6098, 60.3845]   #unfold
    n_wjets           = [2.63983, 2.81968, 2.45998, 136.729, 146.044, 127.413]   #unfold
    n_singletop       = [2.82311, 4.00312, 1.64311, 15.8357, 22.4547, 9.21667]   #unfold
    n_qcd             = [12.1023, 12.712, 11.4926, 90.1481, 94.6896, 85.6065]   #unfold


### finally extract relevant background normalizations
fitted_qcd = n_qcd[i_bkgnorm]
fitted_singletop = n_singletop[i_bkgnorm]
fitted_wjets = n_wjets[i_bkgnorm]
fitted_ttbarnonsemilep = n_ttbarnonsemilep[i_bkgnorm]


# -------------------------------------------------------------------------------------
#  read histogram files
# -------------------------------------------------------------------------------------

DIR = ""
ttDIR = "2Dhists"
dataDIR = "2Dhist"
muOrEl = "mu"
if options.lepType=="ele":
    print ""
    print "UNFOLDING FOR ELECTRON CHANNEL !!!" 
    print ""
    DIR = "_el"
    ttDIR = "qcd_el"
    dataDIR = "qcd_el"
    muOrEl = "el"
else:
    print ""
    print "UNFOLDING FOR MUON CHANNEL !!!" 
    print ""
    

if options.lepType=="ele":
    f_data = TFile("histfiles/"+dataDIR+"/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root")
    f_QCD  = TFile("histfiles/"+dataDIR+"/SingleEl_iheartNY_V1_el_Run2012_2Dcut_qcd.root")
else:
    f_data = TFile("histfiles/"+dataDIR+"/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root")
    f_QCD  = TFile("histfiles/"+dataDIR+"/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_qcd.root")

    
if options.closureTest == True : 
    f_ttbar_max700    = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+"_even.root")
    f_ttbar_700to1000 = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+"_even.root")
    f_ttbar_1000toInf = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+"_even.root")
    f_ttbar_max700_odd    = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+"_odd.root")
    f_ttbar_700to1000_odd = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+"_odd.root")
    f_ttbar_1000toInf_odd = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+"_odd.root")
else :
    f_ttbar_max700    = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+".root")
    f_ttbar_700to1000 = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+".root")
    f_ttbar_1000toInf = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+".root")

f_ttbar_nonsemilep_max700    = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+".root")
f_ttbar_nonsemilep_700to1000 = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+".root")
f_ttbar_nonsemilep_1000toInf = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+".root")

f_T_t     = TFile("histfiles/"+dataDIR+"/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_Tbar_t  = TFile("histfiles/"+dataDIR+"/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_T_s     = TFile("histfiles/"+dataDIR+"/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_Tbar_s  = TFile("histfiles/"+dataDIR+"/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_T_tW    = TFile("histfiles/"+dataDIR+"/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_Tbar_tW = TFile("histfiles/"+dataDIR+"/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")

f_WJets_1jet   = TFile("histfiles/"+dataDIR+"/W1JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_WJets_2jet   = TFile("histfiles/"+dataDIR+"/W2JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_WJets_3jet   = TFile("histfiles/"+dataDIR+"/W3JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_WJets_4jet   = TFile("histfiles/"+dataDIR+"/W4JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")



# the response matrices are simply added here, but have been filled with the full event weights (taking sample size, efficiency, etx. into account)
if options.closureTest == True : 
    response_ttbar_max700    = f_ttbar_max700_odd.Get("response_pt"+nobtag)
    response_ttbar_700to1000 = f_ttbar_700to1000_odd.Get("response_pt"+nobtag)
    response_ttbar_1000toInf = f_ttbar_1000toInf_odd.Get("response_pt"+nobtag)
else :
    response_ttbar_max700    = f_ttbar_max700.Get("response_pt"+nobtag)
    response_ttbar_700to1000 = f_ttbar_700to1000.Get("response_pt"+nobtag)
    response_ttbar_1000toInf = f_ttbar_1000toInf.Get("response_pt"+nobtag)

response = response_ttbar_max700.Clone()
response.SetName("response_pt_"+options.syst)
response.Add(response_ttbar_700to1000)
response.Add(response_ttbar_1000toInf)

## response matrices for two-step unfolding
if options.twoStep == True :
    if options.closureTest == True : 
        response_ttbar_max700_rp    = f_ttbar_max700_odd.Get("response_pt"+nobtag+"_rp")
        response_ttbar_700to1000_rp = f_ttbar_700to1000_odd.Get("response_pt"+nobtag+"_rp")
        response_ttbar_1000toInf_rp = f_ttbar_1000toInf_odd.Get("response_pt"+nobtag+"_rp")
        response_ttbar_max700_pp    = f_ttbar_max700_odd.Get("response_pt_pp")
        response_ttbar_700to1000_pp = f_ttbar_700to1000_odd.Get("response_pt_pp")
        response_ttbar_1000toInf_pp = f_ttbar_1000toInf_odd.Get("response_pt_pp")
        if options.troubleshoot == True:
            response_ttbar_max700_rp_even    = f_ttbar_max700.Get("response_pt"+nobtag+"_rp")
            response_ttbar_700to1000_rp_even = f_ttbar_700to1000.Get("response_pt"+nobtag+"_rp")
            response_ttbar_1000toInf_rp_even = f_ttbar_1000toInf.Get("response_pt"+nobtag+"_rp")
            response_ttbar_max700_pp_even    = f_ttbar_max700.Get("response_pt_pp")
            response_ttbar_700to1000_pp_even = f_ttbar_700to1000.Get("response_pt_pp")
            response_ttbar_1000toInf_pp_even = f_ttbar_1000toInf.Get("response_pt_pp")
    else:
        response_ttbar_max700_rp    = f_ttbar_max700.Get("response_pt"+nobtag+"_rp")
        response_ttbar_700to1000_rp = f_ttbar_700to1000.Get("response_pt"+nobtag+"_rp")
        response_ttbar_1000toInf_rp = f_ttbar_1000toInf.Get("response_pt"+nobtag+"_rp")
        response_ttbar_max700_pp    = f_ttbar_max700.Get("response_pt_pp")
        response_ttbar_700to1000_pp = f_ttbar_700to1000.Get("response_pt_pp")
        response_ttbar_1000toInf_pp = f_ttbar_1000toInf.Get("response_pt_pp")

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
    fout = TFile("UnfoldingPlots/unfold"+DIR+"_2step_"+options.pdf+"_"+options.syst+bkgout+nobtag+".root","recreate");
else :
    fout = TFile("UnfoldingPlots/unfold"+DIR+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+".root","recreate");


# -------------------------------------------------------------------------------------
# read actual histograms
# -------------------------------------------------------------------------------------

if options.closureTest == True : 
    hTrue_max700    = f_ttbar_max700_odd.Get("ptGenTop")
    hTrue_700to1000 = f_ttbar_700to1000_odd.Get("ptGenTop")
    hTrue_1000toInf = f_ttbar_1000toInf_odd.Get("ptGenTop")

    if options.twoStep :
        hPart_max700    = f_ttbar_max700_odd.Get("ptPartTop")
        hPart_700to1000 = f_ttbar_700to1000_odd.Get("ptPartTop")
        hPart_1000toInf = f_ttbar_1000toInf_odd.Get("ptPartTop")

        if options.troubleshoot :
            hTrue_max700_even    = f_ttbar_max700.Get("ptGenTop")
            hTrue_700to1000_even = f_ttbar_700to1000.Get("ptGenTop")
            hTrue_1000toInf_even = f_ttbar_1000toInf.Get("ptGenTop")
            hPart_max700_even    = f_ttbar_max700.Get("ptPartTop")
            hPart_700to1000_even = f_ttbar_700to1000.Get("ptPartTop")
            hPart_1000toInf_even = f_ttbar_1000toInf.Get("ptPartTop")
else :
    hTrue_max700    = f_ttbar_max700.Get("ptGenTop")
    hTrue_700to1000 = f_ttbar_700to1000.Get("ptGenTop")
    hTrue_1000toInf = f_ttbar_1000toInf.Get("ptGenTop")

    if options.twoStep :
        hPart_max700    = f_ttbar_max700.Get("ptPartTop")
        hPart_700to1000 = f_ttbar_700to1000.Get("ptPartTop")
        hPart_1000toInf = f_ttbar_1000toInf.Get("ptPartTop")

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
   

hRecoData = f_data.Get("ptRecoTop"+isTwoStep+nobtag).Clone()
hRecoData.SetName("hRecoData")

hRecoQCD = f_QCD.Get("ptRecoTop"+isTwoStep+nobtag).Clone()
hRecoQCD.SetName("hRecoQCD")
hRecoQCD.Sumw2()
hRecoQCD.SetFillColor(TColor.kYellow)

if options.closureTest == False : 
    hMeas = f_data.Get("ptRecoTop"+isTwoStep+nobtag)
else :
    hMeas_max700    = f_ttbar_max700.Get("ptRecoTop"+isTwoStep+nobtag)
    hMeas_700to1000 = f_ttbar_700to1000.Get("ptRecoTop"+isTwoStep+nobtag)
    hMeas_1000toInf = f_ttbar_1000toInf.Get("ptRecoTop"+isTwoStep+nobtag)
    hMeas_max700.Sumw2()
    hMeas_700to1000.Sumw2()
    hMeas_1000toInf.Sumw2()

    if options.troubleshoot :
        hMeas_max700_odd    = f_ttbar_max700_odd.Get("ptRecoTop"+isTwoStep+nobtag)
        hMeas_700to1000_odd = f_ttbar_700to1000_odd.Get("ptRecoTop"+isTwoStep+nobtag)
        hMeas_1000toInf_odd = f_ttbar_1000toInf_odd.Get("ptRecoTop"+isTwoStep+nobtag)
        hMeas_max700_odd.Sumw2()
        hMeas_700to1000_odd.Sumw2()
        hMeas_1000toInf_odd.Sumw2()
    

hMeas_T_t     = f_T_t.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_Tbar_t  = f_Tbar_t.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_T_s     = f_T_s.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_Tbar_s  = f_Tbar_s.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_T_tW    = f_T_tW.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_Tbar_tW = f_Tbar_tW.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_WJets_1jet   = f_WJets_1jet.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_WJets_2jet   = f_WJets_2jet.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_WJets_3jet   = f_WJets_3jet.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_WJets_4jet   = f_WJets_4jet.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_tt0_nonsemi = f_ttbar_nonsemilep_max700.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_tt700_nonsemi = f_ttbar_nonsemilep_700to1000.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_tt1000_nonsemi = f_ttbar_nonsemilep_1000toInf.Get("ptRecoTop"+isTwoStep+nobtag)

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
    ct1.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_hMeas_evenVsOdd"+isTwoStep+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+".png")

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
    ct2.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_hPart_evenVsOdd"+isTwoStep+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+".png")

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
    ct3.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_hTrue_evenVsOdd"+isTwoStep+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+".png")


    
# -------------------------------------------------------------------------------------
# do the actual unfolding
# -------------------------------------------------------------------------------------


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

    print "------------ UNFOLD TO PARTON-LEVEL (set: " + options.pdf + ", syst: " + options.syst + ") ------------"
    #unfold = RooUnfoldBayes(response_pp, hReco_rp, 10);
    unfold = RooUnfoldSvd(response_pp, hReco_rp, 2);
    #unfold = RooUnfoldTUnfold(response_pp, hReco_rp);

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

    
# -------------------------------------------------------------------------------------
# Adjust for bin width
# -------------------------------------------------------------------------------------

sumReco = 0
sumTrue = 0
sumMeas = 0
sumReco_rp = 0
sumPart = 0
for ibin in range(1, hTrue.GetXaxis().GetNbins()+1 ) :

    # total cross section for pt > 400 GeV 
    if hReco.GetBinLowEdge(ibin) > 399. :
        sumReco += hReco.GetBinContent(ibin)
    if hTrue.GetBinLowEdge(ibin) > 399. :
        sumTrue += hTrue.GetBinContent(ibin)
    if hMeas.GetBinLowEdge(ibin) > 399. :
        sumMeas += hMeas.GetBinContent(ibin)
    if options.twoStep:
        if hReco_rp.GetBinLowEdge(ibin) > 399. :
            sumReco_rp += hReco_rp.GetBinContent(ibin)
        if hPart.GetBinLowEdge(ibin) > 399. :
            sumPart += hPart.GetBinContent(ibin)

    width = hTrue.GetBinWidth(ibin)
    
    hMeas.SetBinContent(ibin,  hMeas.GetBinContent(ibin) / width )
    hMeas.SetBinError(ibin,  hMeas.GetBinError(ibin) / width )

    hTrue.SetBinContent(ibin, hTrue.GetBinContent(ibin) / width )
    hTrue.SetBinError(ibin, hTrue.GetBinError(ibin) / width )

    hReco.SetBinContent(ibin, hReco.GetBinContent(ibin) / width )
    hReco.SetBinError(ibin, hReco.GetBinError(ibin) / width )
    if options.twoStep:
        hReco_rp.SetBinContent(ibin, hReco_rp.GetBinContent(ibin) / width )
        hReco_rp.SetBinError(ibin, hReco_rp.GetBinError(ibin) / width )
        hPart.SetBinContent(ibin, hPart.GetBinContent(ibin) / width )
        hPart.SetBinError(ibin, hPart.GetBinError(ibin) / width )            


# -------------------------------------------------------------------------------------
# do NORMALIZED differential cross section instead??
# -------------------------------------------------------------------------------------
if options.normalize: 
    hTrue.Scale(1.0/sumTrue)
    hReco.Scale(1.0/sumReco)
    hMeas.Scale(1.0/sumMeas)
    if options.twoStep:
        hReco_rp.Scale(1.0/sumReco_rp)
        hPart.Scale(1.0/sumPart)
    
        
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

print ''
print '-------------------------------------------------------------------------------------'
print 'sigma (raw data) = ' + str(int(sumMeas)) + ' fb'
print 'true sigma @ parton-level (pt > 400 GeV)      = ' + str(int(sumTrue)) + ' fb'
print 'measured sigma (unfolded data) @ parton-level = ' + str(int(sumReco)) + ' fb'
if options.twoStep:
    print 'true sigma @ particle-level                     = ' + str(int(sumPart)) + ' fb'
    print 'measured sigma (unfolded data) @ particle-level = ' + str(int(sumReco_rp)) + ' fb'
print '-------------------------------------------------------------------------------------'
print ''


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


xsec_title = ";;d#sigma/dp_{T} [fb/GeV]"
if options.normalize:    
    xsec_title = ";;1/#sigma d#sigma/dp_{T} [1/GeV]"

hReco.SetTitle(xsec_title)
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
hFrac.SetMaximum(1.4)
hFrac.SetMinimum(0.6)
hFrac.UseCurrentStyle()
hFrac.GetYaxis().SetTitleSize(25)
hFrac.GetYaxis().SetTitleOffset(2.0)
hFrac.GetXaxis().SetTitleOffset(4.0)
hFrac.GetXaxis().SetLabelSize(25)
hFrac.GetYaxis().SetNdivisions(4,4,0,False)

hFrac.Draw("e")
hFrac.GetXaxis().SetRangeUser(400., 1200.)

c1.Update()

append = ""
if options.twoStep :
    append += "_2step"
if options.closureTest :
    append += "_closure"

if options.pdf == "CT10_nom" or options.troubleshoot:
    c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+append+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+".pdf", "pdf")
    c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+append+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+".png", "png")
    c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+append+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+".eps", "eps")



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

    hReco_rp.SetTitle(xsec_title)
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

    hFrac_rp.SetMaximum(1.4)
    hFrac_rp.SetMinimum(0.6)
    hFrac_rp.UseCurrentStyle()
    hFrac_rp.GetYaxis().SetTitleSize(25)
    hFrac_rp.GetYaxis().SetTitleOffset(2.0)
    hFrac_rp.GetXaxis().SetTitleOffset(4.0)
    hFrac_rp.GetXaxis().SetLabelSize(25)
    hFrac_rp.GetYaxis().SetNdivisions(4,4,0,False)

    hFrac_rp.Draw("e")
    hFrac_rp.GetXaxis().SetRangeUser(400., 1200.)

    c1.Update()

    append = ""
    if options.closureTest :
        append += "_closure"
        
    if options.pdf == "CT10_nom" or options.troubleshoot:
        c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+"_2step_particle"+append+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+".pdf", "pdf")
        c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+"_2step_particle"+append+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+".png", "png")
        c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+"_2step_particle"+append+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+".eps", "eps")



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
    if options.pdf == "CT10_nom" or options.troubleshoot:
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_responseMatrix_"+options.pdf+"_"+options.syst+nobtag+".png")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_responseMatrix_"+options.pdf+"_"+options.syst+nobtag+".eps")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_responseMatrix_"+options.pdf+"_"+options.syst+nobtag+".pdf")

    hEmpty2D.SetAxisRange(450,1150,"X")
    hEmpty2D.SetAxisRange(450,1150,"Y")
    hResponse2D.SetAxisRange(450,1150,"X")
    hResponse2D.SetAxisRange(450,1150,"Y")
    hEmpty2D.Draw()
    hResponse2D.Draw("colz,same,text")
    hEmpty2D.Draw("axis,same")
    if options.pdf == "CT10_nom" or options.troubleshoot:
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_responseMatrix_zoom_"+options.pdf+"_"+options.syst+nobtag+".png")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_responseMatrix_zoom_"+options.pdf+"_"+options.syst+nobtag+".eps")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_responseMatrix_zoom_"+options.pdf+"_"+options.syst+nobtag+".pdf")
        
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
        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_responseMatrix_rp_odd_"+options.pdf+"_"+options.syst+nobtag+".png")

        hEmpty2D_rp_even.Draw()
        gStyle.SetPaintTextFormat(".1f")
        hResponse2D_rp_even.Draw("colz,same,text")
        hEmpty2D_rp_even.Draw("axis,same")
        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_responseMatrix_rp_even_"+options.pdf+"_"+options.syst+nobtag+".png")
    
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
    if options.pdf == "CT10_nom" or options.troubleshoot:
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_rp_"+options.pdf+"_"+options.syst+nobtag+".png")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_rp_"+options.pdf+"_"+options.syst+nobtag+".eps")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_rp_"+options.pdf+"_"+options.syst+nobtag+".pdf")
    
    hEmpty2D_rp.SetAxisRange(450,1150,"X")
    hEmpty2D_rp.SetAxisRange(450,1150,"Y")
    hResponse2D_rp.SetAxisRange(450,1150,"X")
    hResponse2D_rp.SetAxisRange(450,1150,"Y")
    hEmpty2D_rp.Draw()
    hResponse2D_rp.Draw("colz,same,text")
    hEmpty2D_rp.Draw("axis,same")
    if options.pdf == "CT10_nom" or options.troubleshoot:
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_rp_zoom_"+options.pdf+"_"+options.syst+nobtag+".png")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_rp_zoom_"+options.pdf+"_"+options.syst+nobtag+".eps")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_rp_zoom_"+options.pdf+"_"+options.syst+nobtag+".pdf")


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
        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_responseMatrix_pp_odd_"+options.pdf+"_"+options.syst+nobtag+".png")

        hEmpty2D_pp_even.Draw()
        gStyle.SetPaintTextFormat(".1f")
        hResponse2D_pp_even.Draw("colz,same,text")
        hEmpty2D_pp_even.Draw("axis,same")
        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_responseMatrix_pp_even_"+options.pdf+"_"+options.syst+nobtag+".png")
    
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
    if options.pdf == "CT10_nom" or options.troubleshoot:
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_pp_"+options.pdf+"_"+options.syst+nobtag+".png")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_pp_"+options.pdf+"_"+options.syst+nobtag+".eps")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_pp_"+options.pdf+"_"+options.syst+nobtag+".pdf")
    
    hEmpty2D_pp.SetAxisRange(450,1150,"X")
    hEmpty2D_pp.SetAxisRange(450,1150,"Y")
    hResponse2D_pp.SetAxisRange(450,1150,"X")
    hResponse2D_pp.SetAxisRange(450,1150,"Y")
    hEmpty2D_pp.Draw()
    hResponse2D_pp.Draw("colz,same,text")
    hEmpty2D_pp.Draw("axis,same")
    if options.pdf == "CT10_nom" or options.troubleshoot:
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_pp_zoom_"+options.pdf+"_"+options.syst+nobtag+".png")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_pp_zoom_"+options.pdf+"_"+options.syst+nobtag+".eps")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_pp_zoom_"+options.pdf+"_"+options.syst+nobtag+".pdf")

    response_pp.Hresponse().SetName("responseMatrix_pp_"+options.syst)
    response_pp.Hresponse().Write()



fout.Close()
