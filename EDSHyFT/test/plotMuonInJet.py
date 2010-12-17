#! /usr/bin/env python


from optparse import OptionParser


parser = OptionParser()


# Option to just print out the pre-fit numbers
parser.add_option('--doMC', action='store_true',
                  default=False,
                  dest='doMC',
                  help='use MC')



(options, args) = parser.parse_args()

argv = []


import ROOT
import sys
from DataFormats.FWLite import Events, Handle

if options.doMC :
    files = [
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_muonInJet_387_v2/res/muonInJet_10_1_x4H.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_muonInJet_387_v2/res/muonInJet_11_1_sUa.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_muonInJet_387_v2/res/muonInJet_12_1_3Xb.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_muonInJet_387_v2/res/muonInJet_13_1_M8i.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_muonInJet_387_v2/res/muonInJet_14_1_Q11.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_muonInJet_387_v2/res/muonInJet_15_1_I05.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_muonInJet_387_v2/res/muonInJet_16_1_YFu.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_muonInJet_387_v2/res/muonInJet_1_1_svW.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_muonInJet_387_v2/res/muonInJet_2_1_Ex0.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_muonInJet_387_v2/res/muonInJet_3_1_C9k.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_muonInJet_387_v2/res/muonInJet_4_1_pGQ.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_muonInJet_387_v2/res/muonInJet_5_1_XRN.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_muonInJet_387_v2/res/muonInJet_6_1_dR6.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_muonInJet_387_v2/res/muonInJet_7_1_Snp.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_muonInJet_387_v2/res/muonInJet_8_1_wUI.root',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_muonInJet_387_v2/res/muonInJet_9_1_ZC0.root'


        ]
else :
    files = [
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_muonInJet_v2/res/muonInJet_1_1_VtB.root',
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_muonInJet_v2/res/muonInJet_2_1_WNC.root',
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_muonInJet_v2/res/muonInJet_3_1_GIf.root',
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_muonInJet_v2/res/muonInJet_4_1_5AM.root',
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_muonInJet_v2/res/muonInJet_5_1_niX.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_muonInJet_v2_HLT_Mu15Region/res/muonInJet_1_1_auz.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_muonInJet_v2_HLT_Mu15Region/res/muonInJet_2_1_8ZC.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_muonInJet_v2_HLT_Mu15Region/res/muonInJet_3_1_ynB.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_muonInJet_v2_HLT_Mu15Region/res/muonInJet_4_1_l0t.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_muonInJet_v2_HLT_Mu15Region/res/muonInJet_5_1_PfY.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_muonInJet_v2_HLT_Mu9Region/res/muonInJet_1_1_Z5O.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_muonInJet_v2_HLT_Mu9Region/res/muonInJet_2_1_RYp.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_muonInJet_v2_HLT_Mu9Region/res/muonInJet_3_1_huM.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_muonInJet_v2_HLT_Mu9Region/res/muonInJet_4_1_7PP.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_muonInJet_v2_HLT_Mu9Region/res/muonInJet_5_1_tOC.root'

        ]

    
events = Events (files)
secvtxMassH  = Handle ("std::vector<float>")


# for now, label is just a tuple of strings that is initialized just
# like and edm::InputTag
label1 = ("jetsDump", "jetSecvtxMass")

if options.doMC :
    f = ROOT.TFile("plotMuonInJetMC.root", "RECREATE")
else :
    f = ROOT.TFile("plotMuonInJetData.root", "RECREATE")
f.cd()


secvtxMass = ROOT.TH1F("secvtxMass","secvtxMass",   100, 0.0,  10.0 )


# loop over events
i = 0
for event in events:
    i = i + 1
    if i % 1000 == 0 :
        print i
    # use getByLabel, just like in cmsRun
    event.getByLabel (label1, secvtxMassH)

    # get the product
    masses1 =secvtxMassH.product()

    for mass in masses1 :
        secvtxMass.Fill( mass )

f.cd()

secvtxMass.Write()

f.Close()
