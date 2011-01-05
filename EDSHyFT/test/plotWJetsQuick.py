#! /usr/bin/env python


from optparse import OptionParser

# Create a command line option parser
parser = OptionParser()


# Option to use MC
parser.add_option('--doMC', action='store_true',
                  default=False,
                  dest='doMC',
                  help='use MC')


# Parse and get arguments
(options, args) = parser.parse_args()

# This is needed so that ROOT is happy after we played with the
# command line arguments
argv = []

# Import everything from ROOT
import ROOT
import sys

# Import what we need from FWLite
from DataFormats.FWLite import Events, Handle

# Get the input files
if options.doMC :
    files = [
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyftanaskim_387_v3/33b03c765ac393668d5be7f9ca26fb5d/shyft_skim_386_10_1_erc.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyftanaskim_387_v3/33b03c765ac393668d5be7f9ca26fb5d/shyft_skim_386_11_1_hBU.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyftanaskim_387_v3/33b03c765ac393668d5be7f9ca26fb5d/shyft_skim_386_12_1_E8D.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyftanaskim_387_v3/33b03c765ac393668d5be7f9ca26fb5d/shyft_skim_386_13_1_ZdT.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyftanaskim_387_v3/33b03c765ac393668d5be7f9ca26fb5d/shyft_skim_386_14_1_xV3.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyftanaskim_387_v3/33b03c765ac393668d5be7f9ca26fb5d/shyft_skim_386_15_1_8z1.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyftanaskim_387_v3/33b03c765ac393668d5be7f9ca26fb5d/shyft_skim_386_16_1_FzP.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyftanaskim_387_v3/33b03c765ac393668d5be7f9ca26fb5d/shyft_skim_386_16_1_QHD.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyftanaskim_387_v3/33b03c765ac393668d5be7f9ca26fb5d/shyft_skim_386_16_1_YQt.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyftanaskim_387_v3/33b03c765ac393668d5be7f9ca26fb5d/shyft_skim_386_1_1_mTC.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyftanaskim_387_v3/33b03c765ac393668d5be7f9ca26fb5d/shyft_skim_386_2_1_Xpk.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyftanaskim_387_v3/33b03c765ac393668d5be7f9ca26fb5d/shyft_skim_386_3_1_isl.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyftanaskim_387_v3/33b03c765ac393668d5be7f9ca26fb5d/shyft_skim_386_4_1_Pk7.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyftanaskim_387_v3/33b03c765ac393668d5be7f9ca26fb5d/shyft_skim_386_5_1_6SS.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyftanaskim_387_v3/33b03c765ac393668d5be7f9ca26fb5d/shyft_skim_386_6_1_zDe.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyftanaskim_387_v3/33b03c765ac393668d5be7f9ca26fb5d/shyft_skim_386_7_1_Dph.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyftanaskim_387_v3/33b03c765ac393668d5be7f9ca26fb5d/shyft_skim_386_8_1_USp.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneD6T_7TeV-madgraph-tauola/shyftanaskim_387_v3/33b03c765ac393668d5be7f9ca26fb5d/shyft_skim_386_9_1_ywD.root',


        ]
else :
    files = [
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2/res/muonInJet_10_1_nE5.root',
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2/res/muonInJet_1_1_xKZ.root',
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2/res/muonInJet_2_1_5KI.root',
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2/res/muonInJet_3_1_RMe.root',
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2/res/muonInJet_4_1_p0T.root',
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2/res/muonInJet_5_1_HVI.root',
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2/res/muonInJet_6_1_2v6.root',
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2/res/muonInJet_7_1_XoF.root',
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2/res/muonInJet_8_1_S9s.root',
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2/res/muonInJet_9_1_1JL.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu15Region/res/muonInJet_1_1_qZV.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu15Region/res/muonInJet_2_1_JFY.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu15Region/res/muonInJet_3_1_y0P.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu15Region/res/muonInJet_4_1_9GO.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu15Region/res/muonInJet_5_1_dsU.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu9Region/res/muonInJet_1_1_WTq.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu9Region/res/muonInJet_2_1_mKs.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu9Region/res/muonInJet_3_1_loE.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu9Region/res/muonInJet_4_1_XkB.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu9Region/res/muonInJet_5_1_Gkh.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu9Region/res/muonInJet_6_1_nES.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu9Region/res/muonInJet_7_1_ZVt.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu9Region/res/muonInJet_8_1_4mi.root',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_singlemuonInJet_v2_HLT_Mu9Region/res/muonInJet_9_1_xkV.root',


        ]


# Get the FWLite "Events"
events = Events (files)

# Get a "handle" (i.e. a smart pointer) to the vector of jets
jetsH  = Handle ("std::vector<pat::Jet>")

# Get the label we assigned to our vector of jets
jetsLabel = ("pfShyftSkim", "jets")


# Create an output file and a histogram 
f = ROOT.TFile("wjetsQuick.root", "RECREATE")
f.cd()
secvtxMass = ROOT.TH1F("secvtxMass","secvtxMass",   100, 0.0,  10.0 )



# Keep some timing information
nEventsAnalyzed = 0
timer = ROOT.TStopwatch()
timer.Start()


# loop over events
i = 0
for event in events:
    i = i + 1
    if i % 1000 == 0 :
        print i
    nEventsAnalyzed = nEventsAnalyzed + 1

    # Get the jets "by label" from label "jetsLabel", and put them into "jetsH"
    event.getByLabel (jetsLabel,  jetsH)
    # Get the "product" of the handle (i.e. what it's "pointing to" in C++)
    jets = jetsH.product()
    
    # Now loop over the jets, and store the secondary vertex mass.
    # Here, we've pre-stored the mass with a "user-defined" variable in the pat::Jet, called "secvtxMass"
    for jet in jets :
        mass =jet.userFloat('secvtxMass')
        secvtxMass.Fill( mass )

# Done processing the events!


# Stop our timer
timer.Stop()

# Print out our timing information
rtime = timer.RealTime(); # Real time (or "wall time")
ctime = timer.CpuTime(); # CPU time
print("Analyzed events: {0:6d}").format(nEventsAnalyzed);
print("RealTime={0:6.2f} seconds, CpuTime={1:6.2f} seconds").format(rtime,ctime)
print("{0:4.2f} events / RealTime second .").format( nEventsAnalyzed/rtime)
print("{0:4.2f} events / CpuTime second .").format( nEventsAnalyzed/ctime)

# "cd" to our output file
f.cd()

# Write our histogram
secvtxMass.Write()

# Close it
f.Close()
