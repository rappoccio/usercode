#! /usr/bin/env python
import os
import glob
import time
import math

from optparse import OptionParser


parser = OptionParser()

parser.add_option('--files', metavar='F', type='string', action='store',
                  dest='files',
                  help='Input files')


parser.add_option('--outname', metavar='F', type='string', action='store',
                  default='TTSemilepAnalyzer_antibtag_w_mucut',
                  dest='outname',
                  help='output name')

parser.add_option('--set', metavar='F', type='string', action='store',
                  default='madgraph',
                  dest='set',
                  help='mcatnlo or powheg')

parser.add_option('--num', metavar='F', type='string', action='store',
                  default	=	'all',
                  dest		=	'num',
                  help		=	'file number events in millions')

parser.add_option('--etabin', metavar='F', type='string', action='store',
                  default	=	'all',
                  dest		=	'etabin',
                  help		=	'range1 range2 or all')


parser.add_option('--pileup', metavar='F', type='string', action='store',
                  default='none',
                  dest='pileup',
                  help='ttbar or wjets')

parser.add_option('--ptWeight', metavar='F', action='store_true',
                  default=False,
                  dest='ptWeight',
                  help='do pt reweighting (for MC)')

parser.add_option('--type2', metavar='F', action='store_true',
                  default=False,
                  dest='type2',
                  help='look at type 2 top events')

parser.add_option('--muOnly', metavar='F', action='store_true',
                  default=False,
                  dest='muOnly',
                  help='use only muons')

parser.add_option('--useClosestForTopMass', metavar='F', action='store_true',
                  default=False,
                  dest='useClosestForTopMass',
                  help='use closest jet for top mass, instead of b-jet in had. hemisph.')


parser.add_option('--useLoose', metavar='F', action='store_true',
                  default=False,
                  dest='useLoose',
                  help='use loose leptons (exclusive from tight)')


parser.add_option('--printEvents', metavar='F', action='store_true',
                  default=False,
                  dest='printEvents',
                  help='Print events that pass selection (run:lumi:event)')


parser.add_option('--htCut', metavar='F', type='float', action='store',
                  default=None,
                  dest='htCut',
                  help='HT cut')

# Mttbar cut for sample stitching
parser.add_option('--mttGenMax', metavar='J', type='float', action='store',
                  default=None,
                  dest='mttGenMax',
                  help='Maximum generator-level m_ttbar. Use with --makeResponse')

parser.add_option('--makeResponse', metavar='M', action='store_true',
                  default=False,
                  dest='makeResponse',
                  help='Make response for top pt unfolding')


parser.add_option('--ptCut', metavar='F', type='float', action='store',
                  default=200.0,
                  dest='ptCut',
                  help='Leading jet PT cut')

parser.add_option('--bDiscCut', metavar='F', type='float', action='store',
                  default=0.679,
                  dest='bDiscCut',
                  help='B discriminator cut')

# JEC systematics
parser.add_option('--jecSys', metavar='J', type='float', action='store',
                  default=0.0,
                  dest='jecSys',
                  help='JEC Systematic variation. Options are +1. (up 1 sigma), 0. (nominal), -1. (down 1 sigma)')

# JER systematics
parser.add_option('--jerSys', metavar='J', type='float', action='store',
                  default=0.0,
                  dest='jerSys',
                  help='JER Systematic variation in fraction')

# PDF systematics
parser.add_option('--pdfSys', metavar='J', type='float', action='store',
                  default=0.0,
                  dest='pdfSys',
                  help='PDF Systematic variation. Options are +1. (up 1 sigma), 0. (nominal), -1. (down 1 sigma)')



parser.add_option('--debug', metavar='D', action='store_true',
                  default=False,
                  dest='debug',
                  help='Print debugging info')



(options, args) = parser.parse_args()

argv = []

eventsbegin = [1,10000001,20000001,30000001,40000001,50000001,60000001,70000001]
eventsend = [10000000,20000000,30000000,40000000,50000000,60000000,70000000,80000000]

if options.num != 'all':
	ifile=int(options.num)

import ROOT
ROOT.gROOT.Macro("rootlogon.C")


if options.makeResponse :
    ROOT.gSystem.Load("RooUnfold-1.1.1/libRooUnfold")

# Nominal JER smearing
jerNom = 0.1
# Additional JEC uncertainty for CA8 jets
flatJecUnc = 0.03

if abs( options.jecSys != 0 ) or options.jerSys > 0.0 :
    ROOT.gSystem.Load('libCondFormatsJetMETObjects')
    jecParStrAK5 = ROOT.std.string('START53_V27_Uncertainty_AK5PFchs.txt')
    jecUncAK5 = ROOT.JetCorrectionUncertainty( jecParStrAK5 )
    jecParStrAK7 = ROOT.std.string('START53_V27_Uncertainty_AK7PFchs.txt')
    jecUncAK7 = ROOT.JetCorrectionUncertainty( jecParStrAK7 )    

# Define classes that use ROOT

def findClosestJet( ijet, hadJets ) :
    minDR = 9999.
    ret = -1
    for jjet in range(0,len(hadJets) ):
        if ijet == jjet :
            continue
        dR = hadJets[ijet].DeltaR(hadJets[jjet])
        if dR < minDR :
            minDR = hadJets[ijet].DeltaR(hadJets[jjet])
            ret = jjet
    return ret


def findClosestInList( p41, p4list ) :
    minDR = 9999.
    ret = None
    for j in range(0,len(p4list) ):
        dR = p4list[j].DeltaR(p41)
        if dR < minDR :
            minDR = dR
            ret = p4list[j]
    return ret


class GenTopQuark :
    pdgId = 6                    # 6 = top, -6 = antitop
    p4 = ROOT.TLorentzVector()
    decay = 0                    # 0 = hadronic, 1 = leptonic
    def __init__( self, pdgId, p4, decay ) :
        self.pdgId = pdgId
        self.p4 = p4
        self.decay = decay
    def match( self, jets ) :
        return findClosestInList( self.p4, jets )


    





import sys
from DataFormats.FWLite import Events, Handle


start_time = time.time()


print 'Getting these files : ' + options.files

files = glob.glob( options.files )
print files
toptype = '_type1'
ptwstring=''
if options.type2 == True :
	toptype='_type2'
if options.ptWeight == True :
	ptwstring='_ptWeighted'
etastring = ''
if options.etabin == 'range1':
	etastring = '_eta_range1'
if options.etabin == 'range2':
	etastring = '_eta_range2'

if options.num != 'all':
	f = ROOT.TFile( "partialfiles/"+options.outname +options.num+ptwstring+toptype+etastring+".root", "recreate" )
	name = options.outname +options.num+ptwstring+toptype+etastring
else:
	f = ROOT.TFile(options.outname + ptwstring+toptype+etastring+".root", "recreate")
	name = options.outname+ptwstring+toptype+etastring


print "Creating histograms"

PileFile = ROOT.TFile("Pileup_plots.root")
PilePlot = PileFile.Get("pweight" + options.pileup)

f.cd()
nJets = ROOT.TH1F("nJets",         "Number of Jets, p_{T} > 30 GeV;N_{Jets};Number",               20, -0.5, 19.5 )
nMuons = ROOT.TH1F("nMuons",         "Number of Muons, p_{T} > 45 GeV;N_{Muons};Number",               5, -0.5, 4.5 )
nElectrons = ROOT.TH1F("nElectrons",         "Number of Electrons, p_{T} > 60 GeV;N_{Jets};Number",               5, -0.5, 4.5 )

pfIsoPre = ROOT.TH1F("pfIsoPre", "PF relative isolation", 200, 0., 2.)
pfIsoPost = ROOT.TH1F("pfIsoPost", "PF relative isolation", 200, 0., 2.)
pfIso0 = ROOT.TH1F("pfIso0", "MET", 200, 0., 2.)
pfIso1 = ROOT.TH1F("pfIso1", "MET", 200, 0., 2.)
pfIso2 = ROOT.TH1F("pfIso2", "MET", 200, 0., 2.)
pfIso3 = ROOT.TH1F("pfIso3", "MET", 200, 0., 2.)

ptMu = ROOT.TH1F("ptMu", "p_{T} of Muon", 200, 0., 200.)
ptMET0 = ROOT.TH1F("ptMET0", "MET", 200, 0., 200.)
ptMET1 = ROOT.TH1F("ptMET1", "MET", 200, 0., 200.)
ptMET2 = ROOT.TH1F("ptMET2", "MET", 200, 0., 200.)
ptMET3 = ROOT.TH1F("ptMET3", "MET", 200, 0., 200.)
htLep3mu = ROOT.TH1F("htlep3mu", "H_{T}^{Lep}", 300, 0., 600.)
htLep3t1kin = ROOT.TH1F("htlep3t1kin", "H_{T}^{Lep}", 300, 0., 600.)
htLep3t1minp = ROOT.TH1F("htlep3t1minp", "H_{T}^{Lep}", 300, 0., 600.)
htLep3t1topm = ROOT.TH1F("htlep3t1topm", "H_{T}^{Lep}", 300, 0., 600.)
htLep3t1topmhighptlep = ROOT.TH1F("htlep3t1topmhighptlep", "H_{T}^{Lep}", 300, 0., 600.)
htLep3w = ROOT.TH1F("htlep3w", "H_{T}^{Lep}", 300, 0., 600.)
htLep3top = ROOT.TH1F("htlep3top", "H_{T}^{Lep}", 300, 0., 600.)
htLep0 = ROOT.TH1F("htLep0", "H_{T}^{Lep}", 300, 0., 600.)
htLep1 = ROOT.TH1F("htLep1", "H_{T}^{Lep}", 300, 0., 600.)
htLep2 = ROOT.TH1F("htLep2", "H_{T}^{Lep}", 300, 0., 600.)
htLep3 = ROOT.TH1F("htLep3", "H_{T}^{Lep}", 300, 0., 600.)
ptJet0 = ROOT.TH1F("ptJet0", "p_{T} Of Leading Jet", 300, 0., 600.)

topTagMassHistpremass= ROOT.TH1F("topTagMassHistpremass",         "Mass of Top Candidate from Hadronic Jets type 1 pre mass cut;Mass;Number",  300, 0., 600. )
topTagMassHist= ROOT.TH1F("topTagMassHist",         "Mass of Top Candidate from Hadronic Jets type 1;Mass;Number",  300, 0., 600. )
topTagMassHistPostTau32= ROOT.TH1F("topTagMassHistPostTau32",         "Mass of Top Candidate from Hadronic Jets type 1;Mass;Number",  300, 0., 600. )
topTagMassHistPostBDMax= ROOT.TH1F("topTagMassHistPostBDMax",         "Mass of Top Candidate from Hadronic Jets type 1;Mass;Number",  300, 0., 600. )

topTagptHist= ROOT.TH1F("topTagptHist",         "Pt of Top Candidate from Hadronic Jets type 1;Mass;Number",  375, 0., 1500. )
topTagtau32Hist= ROOT.TH1F("topTagtau32Hist",         "tau32 of Top Candidate from Hadronic Jets type 1;Tau32;Number",  150, 0., 1.5 )
topTagBMaxHist= ROOT.TH1F("topTagBMaxHist",         "BMax of Top Candidate from Hadronic Jets type 1;CSV;Number",  150, 0., 1.5 )


ptlep= ROOT.TH1F("ptlep",         "Pt Leptonic top",  150, 0., 1500. )
topTagptHistprecuts= ROOT.TH1F("topTagptHistprecuts",         "Pt of Top Candidate from Hadronic Jets type 1;Mass;Number",  375, 0., 1500. )
topTagptHistprept= ROOT.TH1F("topTagptHistprept",         "Pt of Top Candidate from Hadronic Jets type 1;Mass;Number",  375, 0., 1500. )
minPairHist= ROOT.TH1F("minPairHist",         "Minimum Pairwise mass",  150, 0., 150. )
WMassPairHist= ROOT.TH1F("WMassPairHist",         "Minimum Pairwise mass",  150, 0., 150. )
WMassPairHistPtrel= ROOT.TH1F("WMassPairHistPtrel",         "Minimum Pairwise mass",  150, 0., 150. )
WMassPairHistDeltaR= ROOT.TH1F("WMassPairHistDeltaR",         "Minimum Pairwise mass",  150, 0., 150. )
WMassPairHistmu= ROOT.TH1F("WMassPairHistmu",         "Minimum Pairwise mass",  150, 0., 150. )
type1muHist = ROOT.TH1F("type1muHist", "#mu", 150, 0, 1.0)

nvtxvsnsj = ROOT.TH2F("nvtxvsnsj","lep top pt vs number of subjets",40,0,80,11, -0.5, 10.5 )
nvtxvsminmass = ROOT.TH2F("nvtxvsminmass","lep top pt vs number of subjets",40,0,80,150, 0., 150. )
nvtxvstopmass = ROOT.TH2F("nvtxvstopmass","lep top pt vs number of subjets",40,0,80,300, 0., 600.  )
nvtxvstau32 = ROOT.TH2F("nvtxvstau32","lep top pt vs number of subjets",40,0,80,150, 0., 1.5   )
nvtxvsbmax = ROOT.TH2F("nvtxvsbmax","lep top pt vs number of subjets",40,0,80,150, 0., 1.5   )

nsj= ROOT.TH1F("nsj",         "number of subjets",  11, -0.5, 10.5 )
nsjhighpt= ROOT.TH1F("nsjhighpt",         "number of subjets",  11, -0.5, 10.5 )
nsjmidptlep= ROOT.TH1F("nsjmidptlep",         "number of subjets ptLep mid",  11, -0.5, 10.5 )
nsjhighptlep= ROOT.TH1F("nsjhighptlep",         "number of subjets ptLep high",  11, -0.5, 10.5 )

topcandmassprekin =  ROOT.TH1F("topcandmassprekin",         "Mass of Top Candidate from Hadronic Jets type 1 pre mass cut;Mass;Number",  300, 0., 600. )
topcandmasspostkin =  ROOT.TH1F("topcandmasspostkin",         "Mass of Top Candidate from Hadronic Jets type 1 pre mass cut;Mass;Number",  300, 0., 600. )
topcandmasspostnsj =  ROOT.TH1F("topcandmasspostnsj",         "Mass of Top Candidate from Hadronic Jets type 1 pre mass cut;Mass;Number",  300, 0., 600. )
topcandmasspostminmass =  ROOT.TH1F("topcandmasspostminmass",         "Mass of Top Candidate from Hadronic Jets type 1 pre mass cut;Mass;Number",  300, 0., 600. )
topcandmassposttau32 =  ROOT.TH1F("topcandmassposttau32",         "Mass of Top Candidate from Hadronic Jets type 1 pre mass cut;Mass;Number",  300, 0., 600. )
topcandmasspostbmax =  ROOT.TH1F("topcandmasspostbmax",         "Mass of Top Candidate from Hadronic Jets type 1 pre mass cut;Mass;Number",  300, 0., 600. )




topTagMassHistpremasshighpt= ROOT.TH1F("topTagMassHistpremasshighpt",         "Mass of Top Candidate from Hadronic Jets type 1 pre mass cut;Mass;Number",  300, 0., 600. )
topTagMassHisthighpt= ROOT.TH1F("topTagMassHisthighpt",         "Mass of Top Candidate from Hadronic Jets type 1;Mass;Number",  300, 0., 600. )
topTagptHisthighpt= ROOT.TH1F("topTagptHisthighpt",         "Pt of Top Candidate from Hadronic Jets type 1;Mass;Number",  375, 0., 1500. )
minPairHisthighpt= ROOT.TH1F("minPairHisthighpt",         "Minimum Pairwise mass",  150, 0., 150. )

ht3 = ROOT.TH1F("ht3", "HT", 200, 0., 2000.)
ht4 = ROOT.TH1F("ht4", "HT", 200, 0., 2000.)
ht5 = ROOT.TH1F("ht5", "HT", 200, 0., 2000.)
ht6 = ROOT.TH1F("ht6", "HT", 200, 0., 2000.)

vtxMass3 = ROOT.TH1F("vtxMass3", "Leptonic-side secondary vertex mass;Mass;Number",  50, 0., 5. )
vtxMass4 = ROOT.TH1F("vtxMass4", "Leptonic-side secondary vertex mass;Mass;Number",  50, 0., 5. )
vtxMass5 = ROOT.TH1F("vtxMass5", "Leptonic-side secondary vertex mass;Mass;Number",  50, 0., 5. )
vtxMass6 = ROOT.TH1F("vtxMass6", "Leptonic-side secondary vertex mass;Mass;Number",  50, 0., 5. )

muHist = ROOT.TH1F("muHist", "#mu", 300, 0, 1.0)
muHisthighpt = ROOT.TH1F("muHisthighpt", "#mu", 300, 0, 1.0)
dRWbHist = ROOT.TH1F("dRWbHist", "#Delta R (W,b)", 300, 0.0, 5.0)

mWCand = ROOT.TH1F("mWCand",         "Mass of W Candidate from Hadronic Jets;Mass;Number",  200, 0., 200. )
mWCandhighpt = ROOT.TH1F("mWCandhighpt",         "Mass of W Candidate from Hadronic Jets;Mass;Number",  200, 0., 200. )
mTopCand = ROOT.TH1F("mTopCand",         "Mass of Top Candidate from Hadronic Jets;Mass;Number",  300, 0., 600. )
mTopCandhighpt = ROOT.TH1F("mTopCandhighpt",         "Mass of Top Candidate from Hadronic Jets;Mass;Number",  300, 0., 600. )




leptopptvstopmassprekin = ROOT.TH2F("leptopptvstopmassprekin","lep top pt vs topmass",150,0,1500,300, 0., 600. )
leptopptvstopmasspostkin = ROOT.TH2F("leptopptvstopmasspostkin","lep top pt vs topmass",150,0,1500,300, 0., 600. )
leptopptvstopmasspostnsj = ROOT.TH2F("leptopptvstopmasspostnsj","lep top pt vs topmass",150,0,1500,300, 0., 600. )
leptopptvstopmasspostminmass = ROOT.TH2F("leptopptvstopmasspostminmass","lep top pt vs topmass",150,0,1500,300, 0., 600. )
leptopptvstopmassposttau32 = ROOT.TH2F("leptopptvstopmassposttau32","lep top pt vs topmass",150,0,1500,300, 0., 600. )
leptopptvstopmasspostbmax = ROOT.TH2F("leptopptvstopmasspostbmax","lep top pt vs topmass",150,0,1500,300, 0., 600. )




leptopptvsnsj = ROOT.TH2F("leptopptvsnsj","lep top pt vs number of subjets",150,500,2000,11, -0.5, 10.5 )

mWCandVsMuCut = ROOT.TH2F("mWCandVsMuCut", "Mass of W candidate versus #mu cut", 20, 0, 200, 10, 0, 1.0)
mWCandVsMTopCand = ROOT.TH2F("mWCandVsMTopCand","WCand+bJet Mass vs WCand mass",200,0.,200.,600,0.,600.)

mWCandVsPtWCand = ROOT.TH2F("mWCandVsPtWCand", "Mass of W candidate versus p_{T} of W candidate", 100, 0, 1000, 20, 0, 200)
mWCandVsPtWCandMuCut = ROOT.TH2F("mWCandVsPtWCandMuCut", "Mass of W candidate versus p_{T} of W candidate", 100, 0, 1000, 20, 0, 200)

ptTopCand = ROOT.TH1F("ptTopCand", "WCand+bJet p_{T};p_{T} (GeV/c);Number", 250, 0., 1000.)
ptWFromTopCand = ROOT.TH1F("ptWFromTopCand", "WCand in Type-2 top cand p_{T};p_{T} (GeV/c);Number", 250, 0., 1000.)
ptbFromTopCand = ROOT.TH1F("ptbFromTopCand", "bCand in Type-2 top cand p_{T};p_{T} (GeV/c);Number", 250, 0., 1000.)


if options.makeResponse == True : 
    response = ROOT.RooUnfoldResponse(10, 300., 1300., 10, 300., 1300.)
    response.SetName('response_pt')
    ptGenTop = ROOT.TH1F("ptGenTop", "Generated top p_{T};p_{T} (GeV/c);Number", 10, 300., 1300.)

ptRecoTop = ROOT.TH1F("ptRecoTop", "Reconstructed top p_{T};p_{T} (GeV/c);Number", 10, 300., 1300.)

events = Events (files)

postfix = ""
if options.useLoose :
    postfix = "Loose"


puHandle    	= 	Handle("int")
puLabel     	= 	( "pileup", "npvRealTrue" )

npvHandle    	= 	Handle("unsigned int")
npvLabel     	= 	( "pileup", "npv" )


nsubCA8Handle     	= 	Handle( "vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > >")
nsubCA8Label      	= 	( "nsub", "CA8P4" )

TopTau2Handle       = 	Handle( "std::vector<double>" )
TopTau2Label    	= 	( "nsub" , "Tau2")

TopTau3Handle       = 	Handle( "std::vector<double>" )
TopTau3Label    	= 	( "nsub" , "Tau3")

ak5JetPtHandle         = Handle( "std::vector<float>" )
ak5JetPtLabel    = ( "pfShyftTupleJets" + postfix + "AK5",   "pt" )
ak5JetEtaHandle         = Handle( "std::vector<float>" )
ak5JetEtaLabel    = ( "pfShyftTupleJets" + postfix + "AK5",   "eta" )
ak5JetPhiHandle         = Handle( "std::vector<float>" )
ak5JetPhiLabel    = ( "pfShyftTupleJets" + postfix + "AK5",   "phi" )
ak5JetMassHandle         = Handle( "std::vector<float>" )
ak5JetMassLabel    = ( "pfShyftTupleJets" + postfix + "AK5",   "mass" )
ak5JetDa0MassHandle         = Handle( "std::vector<float>" )
ak5JetDa0MassLabel    = ( "pfShyftTupleJets" + postfix + "AK5",   "da0Mass" )
ak5JetDa1MassHandle         = Handle( "std::vector<float>" )
ak5JetDa1MassLabel    = ( "pfShyftTupleJets" + postfix + "AK5",   "da1Mass" )
ak5JetCSVHandle         = Handle( "std::vector<float>" )
ak5JetCSVLabel    = ( "pfShyftTupleJets" + postfix + "AK5",   "csv" )
ak5JetSecvtxMassHandle         = Handle( "std::vector<float>" )
ak5JetSecvtxMassLabel    = ( "pfShyftTupleJets" + postfix + "AK5",   "secvtxMass" )

ca8PrunedJetPtHandle         = Handle( "std::vector<float>" )
ca8PrunedJetPtLabel    = ( "pfShyftTupleJets" + postfix + "CA8Pruned",   "pt" )
ca8PrunedJetEtaHandle         = Handle( "std::vector<float>" )
ca8PrunedJetEtaLabel    = ( "pfShyftTupleJets" + postfix + "CA8Pruned",   "eta" )
ca8PrunedJetPhiHandle         = Handle( "std::vector<float>" )
ca8PrunedJetPhiLabel    = ( "pfShyftTupleJets" + postfix + "CA8Pruned",   "phi" )
ca8PrunedJetMassHandle         = Handle( "std::vector<float>" )
ca8PrunedJetMassLabel    = ( "pfShyftTupleJets" + postfix + "CA8Pruned",   "mass" )
ca8PrunedJetDa0MassHandle         = Handle( "std::vector<float>" )
ca8PrunedJetDa0MassLabel    = ( "pfShyftTupleJets" + postfix + "CA8Pruned",   "da0Mass" )
ca8PrunedJetDa1MassHandle         = Handle( "std::vector<float>" )
ca8PrunedJetDa1MassLabel    = ( "pfShyftTupleJets" + postfix + "CA8Pruned",   "da1Mass" )
ca8PrunedJetCSVHandle         = Handle( "std::vector<float>" )
ca8PrunedJetCSVLabel    = ( "pfShyftTupleJetsCA8" + postfix,   "csv" )

topTagPtHandle         = Handle( "std::vector<float>" )
topTagPtLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "pt" )
topTagEtaHandle         = Handle( "std::vector<float>" )
topTagEtaLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "eta" )
topTagPhiHandle         = Handle( "std::vector<float>" )
topTagPhiLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "phi" )
topTagMassHandle         = Handle( "std::vector<float>" )
topTagMassLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "mass" )
topTagMinMassHandle         = Handle( "std::vector<float>" )
topTagMinMassLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "minMass" )
topTagNSubjetsHandle         = Handle( "std::vector<float>" )
topTagNSubjetsLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "nSubjets" )

topTagsj0csvLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "topsj0csv" )
topTagsj0csvHandle         = Handle( "std::vector<float>" )
topTagsj1csvLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "topsj1csv" )
topTagsj1csvHandle         = Handle( "std::vector<float>" )
topTagsj2csvLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "topsj2csv" )
topTagsj2csvHandle         = Handle( "std::vector<float>" )
topTagsj3csvLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "topsj3csv" )
topTagsj3csvHandle         = Handle( "std::vector<float>" )

topTagsj0ptLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "topsj0pt" )
topTagsj0ptHandle         = Handle( "std::vector<float>" )
topTagsj1ptLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "topsj1pt" )
topTagsj1ptHandle         = Handle( "std::vector<float>" )
topTagsj2ptLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "topsj2pt" )
topTagsj2ptHandle         = Handle( "std::vector<float>" )
topTagsj3ptLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "topsj3pt" )
topTagsj3ptHandle         = Handle( "std::vector<float>" )

topTagsj0etaLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "topsj0eta" )
topTagsj0etaHandle         = Handle( "std::vector<float>" )
topTagsj1etaLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "topsj1eta" )
topTagsj1etaHandle         = Handle( "std::vector<float>" )
topTagsj2etaLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "topsj2eta" )
topTagsj2etaHandle         = Handle( "std::vector<float>" )
topTagsj3etaLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "topsj3eta" )
topTagsj3etaHandle         = Handle( "std::vector<float>" )

topTagsj0phiLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "topsj0phi" )
topTagsj0phiHandle         = Handle( "std::vector<float>" )
topTagsj1phiLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "topsj1phi" )
topTagsj1phiHandle         = Handle( "std::vector<float>" )
topTagsj2phiLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "topsj2phi" )
topTagsj2phiHandle         = Handle( "std::vector<float>" )
topTagsj3phiLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "topsj3phi" )
topTagsj3phiHandle         = Handle( "std::vector<float>" )

topTagsj0massLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "topsj0mass" )
topTagsj0massHandle         = Handle( "std::vector<float>" )
topTagsj1massLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "topsj1mass" )
topTagsj1massHandle         = Handle( "std::vector<float>" )
topTagsj2massLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "topsj2mass" )
topTagsj2massHandle         = Handle( "std::vector<float>" )
topTagsj3massLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "topsj3mass" )
topTagsj3massHandle         = Handle( "std::vector<float>" )

muonPtHandle         = Handle( "std::vector<float>" )
muonPtLabel    = ( "pfShyftTupleMuons" + postfix,   "pt" )
muonEtaHandle         = Handle( "std::vector<float>" )
muonEtaLabel    = ( "pfShyftTupleMuons" + postfix,   "eta" )
muonPhiHandle         = Handle( "std::vector<float>" )
muonPhiLabel    = ( "pfShyftTupleMuons" + postfix,   "phi" )
muonPfisoHandle         = Handle( "std::vector<float>" )
muonPfisoLabel    = ( "pfShyftTupleMuons" + postfix,   "pfisoPU" )

electronPtHandle         = Handle( "std::vector<float>" )
electronPtLabel    = ( "pfShyftTupleElectrons" + postfix,   "pt" )
electronEtaHandle         = Handle( "std::vector<float>" )
electronEtaLabel    = ( "pfShyftTupleElectrons" + postfix,   "eta" )
electronPhiHandle         = Handle( "std::vector<float>" )
electronPhiLabel    = ( "pfShyftTupleElectrons" + postfix,   "phi" )
electronPfisoHandle         = Handle( "std::vector<float>" )
electronPfisoLabel    = ( "pfShyftTupleElectrons" + postfix,   "pfisoPU" )

metHandle = Handle( "std::vector<float>" )
metLabel = ("pfShyftTupleMET" + postfix,   "pt" )

metphiHandle = Handle( "std::vector<float>" )
metphiLabel = ("pfShyftTupleMET" + postfix,   "phi" )

if options.pdfSys != 0.0 : 
	pdfWeightCT10Handle = Handle( "std::vector<double>" )
	pdfWeightCT10Label = ("ct10weights",   "pdfWeights" )

	pdfWeightMSTWHandle = Handle( "std::vector<double>" )
	pdfWeightMSTWLabel = ("mstwweights",   "pdfWeights" )

	pdfWeightNNPDFHandle = Handle( "std::vector<double>" )
	pdfWeightNNPDFLabel = ("nnpdfweights",   "pdfWeights" )


if options.makeResponse == True : 
    genParticlesPtHandle = Handle( "std::vector<float>")
    genParticlesPtLabel = ( "pfShyftTupleGenParticles", "pt")
    genParticlesEtaHandle = Handle( "std::vector<float>")
    genParticlesEtaLabel = ( "pfShyftTupleGenParticles", "eta")
    genParticlesPhiHandle = Handle( "std::vector<float>")
    genParticlesPhiLabel = ( "pfShyftTupleGenParticles", "phi")
    genParticlesMassHandle = Handle( "std::vector<float>")
    genParticlesMassLabel = ( "pfShyftTupleGenParticles", "mass")
    genParticlesPdgIdHandle = Handle( "std::vector<float>")
    genParticlesPdgIdLabel = ( "pfShyftTupleGenParticles", "pdgId")
    genParticlesStatusHandle = Handle( "std::vector<float>")
    genParticlesStatusLabel = ( "pfShyftTupleGenParticles", "status")

if options.jerSys != 0.0 :
    ak5GenJetPtHandle = Handle( "std::vector<float>")
    ak5GenJetPtLabel = ("pfShyftTupleAK5GenJets", "pt")
    ak5GenJetEtaHandle = Handle( "std::vector<float>")
    ak5GenJetEtaLabel = ("pfShyftTupleAK5GenJets", "eta")
    ak5GenJetPhiHandle = Handle( "std::vector<float>")
    ak5GenJetPhiLabel = ("pfShyftTupleAK5GenJets", "phi")
    ak5GenJetMassHandle = Handle( "std::vector<float>")
    ak5GenJetMassLabel = ("pfShyftTupleAK5GenJets", "mass")

    ca8GenJetPtHandle = Handle( "std::vector<float>")
    ca8GenJetPtLabel = ("pfShyftTupleCA8GenJets", "pt")
    ca8GenJetEtaHandle = Handle( "std::vector<float>")
    ca8GenJetEtaLabel = ("pfShyftTupleCA8GenJets", "eta")
    ca8GenJetPhiHandle = Handle( "std::vector<float>")
    ca8GenJetPhiLabel = ("pfShyftTupleCA8GenJets", "phi")
    ca8GenJetMassHandle = Handle( "std::vector<float>")
    ca8GenJetMassLabel = ("pfShyftTupleCA8GenJets", "mass")

goodEvents = []
goodEventst1 = []
# loop over events
count = 0
print "Start looping"
nhptbj=0
npassed = 0

if options.set == 'mcatnlo':
	print "Using MC@NLO Weights"
	weightFile = ROOT.TFile("ptlepNewSelmcatnlo_weight.root")
elif options.set == 'powheg':
	print "Using Powheg Weights"
	weightFile = ROOT.TFile("ptlepNewSelpowheg_weight.root")
else:
	print "Using MadGraph Weights"
	weightFile = ROOT.TFile("ptlepNewSel_weight.root")
weightPlot = weightFile.Get("lepptweight")
if options.ptWeight == False :
	print "Turning pt reweighting off"
for event in events:
	#print 'is this broken?'

    weight = 1.0
    if count % 10000 == 0 or options.debug :
      print  '--------- Processing Event ' + str(count)
    count = count + 1
    if options.num != 'all':
	if not (eventsbegin[ifile-1] <= count <= eventsend[ifile-1]):
		continue 

	    

    # Find the top and antitop quarks.
    # We also need to find the decay mode of the top and antitop quarks.
    # To do so, we look for leptons, and use their charge to assign
    # the correct decay mode to the correct quark. 
    topQuarks = []

    if options.pdfSys != 0.0 :
	event.getByLabel( pdfWeightCT10Label, pdfWeightCT10Handle )
	event.getByLabel( pdfWeightMSTWLabel, pdfWeightMSTWHandle )
	event.getByLabel( pdfWeightNNPDFLabel, pdfWeightNNPDFHandle )
	pdfWeightCT10 = pdfWeightCT10Handle.product()
	pdfWeightMSTW = pdfWeightMSTWHandle.product()
	pdfWeightNNPDF = pdfWeightNNPDFHandle.product()

	# Get the envelopes of the various PDF sets for this event.
	# Use the max and min values of all of the eigenvectors as the
	# envelope. 
	if options.pdfSys > 0 :
	    pdfWeights1 = [ i / pdfWeightCT10[0] for i in pdfWeightCT10[1::2] ]
	    pdfWeights2 = [ i / pdfWeightMSTW[0] for i in pdfWeightMSTW[1::2] ]
	    pdfWeights3 = [ i / pdfWeightNNPDF[0] for i in pdfWeightNNPDF[1::2] ]
	    pdfWeights = pdfWeights1 + pdfWeights2 + pdfWeights3
	    maxweight = 1.0
	    for iweight in pdfWeights :
		    if iweight > 0 and iweight > maxweight :
			    maxweight = iweight

	    weight *= maxweight
	else : 
	    pdfWeights1 = [ i / pdfWeightCT10[0] for i in pdfWeightCT10[2::2] ]
	    pdfWeights2 = [ i / pdfWeightMSTW[0] for i in pdfWeightMSTW[2::2] ]
	    pdfWeights3 = [ i / pdfWeightNNPDF[0] for i in pdfWeightNNPDF[2::2] ]
	    pdfWeights = pdfWeights1 + pdfWeights2 + pdfWeights3
	    minweight = 1.0
	    for iweight in pdfWeights :
		    if iweight > 0 and iweight < minweight :
			    minweight = iweight

	    weight *= minweight


		
    hadTop = None
    lepTop = None
    isSemiLeptonicGen = True
    if options.makeResponse == True :
        event.getByLabel( genParticlesPtLabel, genParticlesPtHandle )
        event.getByLabel( genParticlesEtaLabel, genParticlesEtaHandle )
        event.getByLabel( genParticlesPhiLabel, genParticlesPhiHandle )
        event.getByLabel( genParticlesMassLabel, genParticlesMassHandle )
        event.getByLabel( genParticlesPdgIdLabel, genParticlesPdgIdHandle )
        event.getByLabel( genParticlesStatusLabel, genParticlesStatusHandle )

        genParticlesPt = genParticlesPtHandle.product()
        genParticlesEta = genParticlesEtaHandle.product()
        genParticlesPhi = genParticlesPhiHandle.product()
        genParticlesMass = genParticlesMassHandle.product()
        genParticlesPdgId = genParticlesPdgIdHandle.product()
        genParticlesStatus = genParticlesStatusHandle.product()
        
        #print '------------'
        p4Top = ROOT.TLorentzVector()
        p4Antitop = ROOT.TLorentzVector()
        topDecay = 0        # 0 = hadronic, 1 = leptonic
        antitopDecay = 0    # 0 = hadronic, 1 = leptonic



        for igen in xrange( len(genParticlesPt) ) :
            #print '{0:6.0f} {1:6.0f} {2:6.2f}'.format( genParticlesPdgId[igen],
            #                                           genParticlesStatus[igen],
            #                                           genParticlesPt[igen] )
            # Figure out the top vs antitop from charge of decay products.
            # Need to know which is the hadronic one (top or antitop) to do unfolding

            if genParticlesStatus[igen] != 3 :
                continue
            if  abs(genParticlesPdgId[igen]) < 6 :
                continue
            if  abs(genParticlesPdgId[igen]) > 16 :
                continue
            

            if genParticlesStatus[igen] == 3 and genParticlesPdgId[igen] == 6 :
                gen = ROOT.TLorentzVector()
                gen.SetPtEtaPhiM( genParticlesPt[igen],
                                  genParticlesEta[igen],
                                  genParticlesPhi[igen],
                                  genParticlesMass[igen]
                    )                    
                p4Top = gen
            elif genParticlesStatus[igen] == 3 and genParticlesPdgId[igen] == -6 :
                gen = ROOT.TLorentzVector()
                gen.SetPtEtaPhiM( genParticlesPt[igen],
                                  genParticlesEta[igen],
                                  genParticlesPhi[igen],
                                  genParticlesMass[igen]
                    )
                p4Antitop = gen
            # If there is a lepton (e-, mu-, tau-) then the top is leptonic
            elif genParticlesStatus[igen] == 3 and \
                ( genParticlesPdgId[igen] == -11 or genParticlesPdgId[igen] == -13 or genParticlesPdgId[igen] == -15) :
                topDecay = 1
            # If there is an antilepton (e+, mu+, tau+) then the antitop is leptonic
            elif genParticlesStatus[igen] == 3 and \
                ( genParticlesPdgId[igen] == 11 or genParticlesPdgId[igen] == 13 or genParticlesPdgId[igen] == 15) :                
                antitopDecay = 1

        #print 'I think the top quark decay mode is ' + str(topDecay)
        topQuarks.append( GenTopQuark( 6, p4Top, topDecay) )
        #print 'I think the top antiquark decay mode is ' + str(antitopDecay)
        topQuarks.append( GenTopQuark( -6, p4Antitop, antitopDecay) )        
        if topDecay + antitopDecay == 1 :
            isSemiLeptonicGen = True
        else :
            isSemiLeptonicGen = False

        # If we are filling the response matrix, don't
        # consider "volunteer" events that pass the selection
        # even though they aren't really semileptonic events. 
        if isSemiLeptonicGen == False :
            continue	

        if topDecay == 0 :
            hadTop = topQuarks[0]
            lepTop = topQuarks[1]
        else :
            hadTop = topQuarks[1]
            lepTop = topQuarks[0]
	if options.mttGenMax is not None :
		ttbarGen = hadTop.p4 + lepTop.p4
		mttbarGen = ttbarGen.M()
		if mttbarGen > options.mttGenMax :
			continue
	ptGenTop.Fill( hadTop.p4.Perp(), weight )
    # endif (making response matrix)


    if options.debug :
        print 'Getting muons'

    lepType = 0 # Let 0 = muon, 1 = electron    
    event.getByLabel (muonPtLabel, muonPtHandle)
    if not muonPtHandle.isValid():
        if options.makeResponse == True :
            response.Miss( hadTop.p4.Perp(), weight )
        continue
    muonPts = muonPtHandle.product()

    if True :
        event.getByLabel (muonPfisoLabel, muonPfisoHandle)
        if not muonPfisoHandle.isValid():
            if options.makeResponse == True :
                response.Miss( hadTop.p4.Perp(), weight )
            continue
        muonPfisos = muonPfisoHandle.product()




    if options.debug :
        print 'nmu = ' + str(len(muonPts))
    nMuonsVal = 0
    for imuonPt in range(0,len(muonPts)):
        muonPt = muonPts[imuonPt]
        if muonPt > 45.0 :
            pfIsoPre.Fill( muonPfisos[imuonPt] / muonPt, weight )
            if options.useLoose :
		if options.debug : 
			print 'imu = ' + str(imuonPt) + ', iso/pt = ' + str( muonPfisos[imuonPt] ) + '/' + str(muonPt) + ' = ' + str(muonPfisos[imuonPt]/muonPt)
                if muonPfisos[imuonPt] / muonPt < 0.12 :
                    if options.makeResponse == True :
                        response.Miss( hadTop.p4.Perp(), weight )
                    continue
                else :
		    if options.debug :
			    print 'PASSED LOOSE!'
                    nMuonsVal += 1
                    lepType = 0
            else :
            	if muonPfisos[imuonPt] / muonPt > 0.12 :
                    if options.makeResponse == True :
                        response.Miss( hadTop.p4.Perp(), weight )
		    continue
                nMuonsVal += 1
                lepType = 0
                if options.debug :
                    print 'PASSED TIGHT!'
    if options.pileup != 'none':   
    	event.getByLabel (puLabel, puHandle)
    	PileUp 		= 	puHandle.product()
    	bin1 = PilePlot.FindBin(PileUp[0]) 
    	weight *= PilePlot.GetBinContent(bin1)
        if options.debug : 
            print "PU weight is " + str(weight)

    event.getByLabel (npvLabel, npvHandle)
    numvert 		= 	npvHandle.product()
	
    pfIsoPost.Fill( muonPfisos[imuonPt] / muonPt, weight )
    nMuons.Fill( nMuonsVal,weight )
    #print "Filling???"
    if nMuonsVal > 0 :
        ptMu.Fill( muonPts[0],weight )

    event.getByLabel (electronPtLabel, electronPtHandle)
    electronPts = electronPtHandle.product()

    event.getByLabel (topTagEtaLabel, topTagEtaHandle)
    if not topTagEtaHandle.isValid() :
	if options.makeResponse == True :
		response.Miss( hadTop.p4.Perp(), weight )
	continue 

    if options.debug :
        print 'toptag eta handle is valid'
        print 'toptag etabin is ' + options.etabin	    
    topTagEta = topTagEtaHandle.product()
    if not options.type2:
	if len(topTagEta)<1:
            if options.makeResponse == True :
                response.Miss( hadTop.p4.Perp(), weight )
	    continue 
    	if options.etabin != 'all':
		if options.etabin == 'range1':
			if abs(topTagEta[0])>1.0:
				continue
		if options.etabin == 'range2':
			if abs(topTagEta[0])<=1.0:
				continue 

    nElectronsVal = 0
  #  if nMuonsVal == 0 :
  #      for ielectronPt in range(0,len(electronPts)):
  #          electronPt = electronPts[ielectronPt]
  #          if electronPt > 45.0 :
  #              if options.useLoose :
  #                  if electronPfisos[ielectronPt] / electronPt < 0.2 :
  #                      continue
  #                  else :
  #                      nElectronsVal += 1
  #                      lepType = 1
  #              else :
  #                  nElectronsVal += 1
  #                  lepType = 1
  #                      
    nElectrons.Fill( nElectronsVal,weight )


    if not options.muOnly :
        if nMuonsVal + nElectronsVal != 1 :
            if options.makeResponse == True :
                response.Miss( hadTop.p4.Perp(), weight )
            continue
    else :
        if nMuonsVal != 1:
            if options.makeResponse == True :
                response.Miss( hadTop.p4.Perp(), weight )
            continue


    if options.debug :
        print 'Passed muon selection, onward!'
    # Now look at the rest of the lepton information.
    # We will classify jets based on hemispheres, defined
    # by the lepton.

    lepMass = 0.0
    if lepType == 0 :
        event.getByLabel (muonEtaLabel, muonEtaHandle)
        muonEtas = muonEtaHandle.product()
        event.getByLabel (muonPhiLabel, muonPhiHandle)
        muonPhis = muonPhiHandle.product()

        lepPt = muonPts[0]
        lepEta = muonEtas[0]
        lepPhi = muonPhis[0]
        lepMass = 0.105
    else :
        event.getByLabel (electronEtaLabel, electronEtaHandle)
        electronEtas = electronEtaHandle.product()
        event.getByLabel (electronPhiLabel, electronPhiHandle)
        electronPhis = electronPhiHandle.product()

        lepPt = electronPts[0]
        lepEta = electronEtas[0]
        lepPhi = electronPhis[0]

    lepP4 = ROOT.TLorentzVector()
    lepP4.SetPtEtaPhiM( lepPt, lepEta, lepPhi, lepMass )

        

    event.getByLabel (ak5JetPtLabel, ak5JetPtHandle)
    ak5JetPts = ak5JetPtHandle.product()
    event.getByLabel (ak5JetEtaLabel, ak5JetEtaHandle)
    ak5JetEtas = ak5JetEtaHandle.product()
    event.getByLabel (ak5JetPhiLabel, ak5JetPhiHandle)
    ak5JetPhis = ak5JetPhiHandle.product()
    event.getByLabel (ak5JetMassLabel, ak5JetMassHandle)
    ak5JetMasss = ak5JetMassHandle.product()



    if len(ak5JetPts) > 0 and options.jerSys != 0.0 :
        if options.debug :
            print 'getting gen jets'
        ak5GenJets = []
	ca8GenJets = []
	event.getByLabel( ak5GenJetPtLabel, ak5GenJetPtHandle )
	event.getByLabel( ak5GenJetEtaLabel, ak5GenJetEtaHandle )
	event.getByLabel( ak5GenJetPhiLabel, ak5GenJetPhiHandle )
	event.getByLabel( ak5GenJetMassLabel, ak5GenJetMassHandle )
	event.getByLabel( ca8GenJetPtLabel, ca8GenJetPtHandle )
	event.getByLabel( ca8GenJetEtaLabel, ca8GenJetEtaHandle )
	event.getByLabel( ca8GenJetPhiLabel, ca8GenJetPhiHandle )
	event.getByLabel( ca8GenJetMassLabel, ca8GenJetMassHandle )
	ak5GenJetPt = ak5GenJetPtHandle.product()
	ak5GenJetEta = ak5GenJetEtaHandle.product()
	ak5GenJetPhi = ak5GenJetPhiHandle.product()
	ak5GenJetMass = ak5GenJetMassHandle.product()
	for iak5 in xrange( len(ak5GenJetPt) ) :
		p4 = ROOT.TLorentzVector()
		p4.SetPtEtaPhiM( ak5GenJetPt[iak5],
				 ak5GenJetEta[iak5],
				 ak5GenJetPhi[iak5],
				 ak5GenJetMass[iak5],
				 )
		ak5GenJets.append(p4)

	ca8GenJetPt = ca8GenJetPtHandle.product()
	ca8GenJetEta = ca8GenJetEtaHandle.product()
	ca8GenJetPhi = ca8GenJetPhiHandle.product()
	ca8GenJetMass = ca8GenJetMassHandle.product()
	for ica8 in xrange( len(ca8GenJetPt) ) :
		p4 = ROOT.TLorentzVector()
		p4.SetPtEtaPhiM( ca8GenJetPt[ica8],
				 ca8GenJetEta[ica8],
				 ca8GenJetPhi[ica8],
				 ca8GenJetMass[ica8],
				 )
		ca8GenJets.append(p4)

    event.getByLabel (metLabel, metHandle)
    mets = metHandle.product()
    metRaw = mets[0]
    event.getByLabel (metphiLabel, metphiHandle)
    metphis = metphiHandle.product()
    metphi = metphis[0]
    met_px = metRaw * math.cos( metphi )
    met_py = metRaw * math.sin( metphi )
    

    ak5Jets = []
    if options.debug :
        print 'Smearing jets'
    if abs( options.jecSys != 0 ) or options.jerSys > 0.0 :
        if options.debug :
            print '---------- jets ------------'
        for ijet in xrange( len(ak5JetPts) ) :
            if options.debug :            
                print 'Uncorr {0:4.0f} : ({1:6.2f} {2:6.2f} {3:6.2f} {4:6.2f})'.format( ijet, ak5JetPts[ijet], ak5JetEtas[ijet], ak5JetPhis[ijet], ak5JetMasss[ijet] )
            jecUncAK5.setJetEta( ak5JetEtas[ijet] )
            jecUncAK5.setJetPt( ak5JetPts[ijet] )

            ## get the uncorrected jets
            thisJet = ROOT.TLorentzVector()
            thisJet.SetPtEtaPhiM( ak5JetPts[ijet],
                                  ak5JetEtas[ijet],
                                  ak5JetPhis[ijet],
                                  ak5JetMasss[ijet] )

            jetScale = 1.0
            if abs(options.jecSys) > 0.0001 :
                upOrDown = bool(options.jecSys > 0.0)
                unc = abs(jecUncAK5.getUncertainty(upOrDown))
                #unc2 = flatJecUnc
                #unc = math.sqrt(unc1*unc1 + unc2*unc2)
                #print 'Correction = ' + str( 1 + unc * options.jecSys)
                jetScale = 1 + unc * options.jecSys

            ## also do Jet energy resolution variation 
            if abs(options.jerSys)>0.0001 :
		genJet = findClosestInList( thisJet, ak5GenJets )
                scale = options.jerSys
                recopt = thisJet.Perp()
                genpt = genJet.Perp()
                deltapt = (recopt-genpt)*scale
                ptscale = max(0.0, (recopt+deltapt)/recopt)
                jetScale*=ptscale


            #remove the uncorrected jets
            met_px = met_px + thisJet.Px()
            met_py = met_py + thisJet.Py()


            thisJet = thisJet * jetScale
            ak5Jets.append( thisJet )
            if options.debug :            
                print 'Corr   {0:4.0f} : ({1:6.2f} {2:6.2f} {3:6.2f} {4:6.2f})'.format( ijet,
                                                                                        ak5Jets[ijet].Perp(),
                                                                                        ak5Jets[ijet].Eta(),
                                                                                        ak5Jets[ijet].Phi(),
                                                                                        ak5Jets[ijet].M() )

            met_px = met_px - thisJet.Px()
            met_py = met_py - thisJet.Py()


    met = math.sqrt(met_px*met_px + met_py*met_py)

    
    htLepVal = met + lepP4.Perp()

    htLep0.Fill( htLepVal,weight )
    ptMET0.Fill( met,weight )
    pfIso0.Fill( muonPfisos[imuonPt] / muonPt, weight )

    nJetsVal = 0
    for jet in ak5Jets :
        if jet.Perp() > 30.0 :
            nJetsVal += 1
    
    nJets.Fill( nJetsVal,weight )

    # Require >= 2 AK5 jets above 30 GeV
    if nJetsVal < 2 :
        if options.makeResponse == True :
            response.Miss( hadTop.p4.Perp(), weight )       
        continue

    htLep1.Fill( htLepVal,weight )
    ptMET1.Fill( met,weight )
    pfIso1.Fill( muonPfisos[imuonPt] / muonPt, weight )
    ptJet0.Fill( ak5Jets[0].Perp(),weight )
    if options.debug :
        print 'Have at least two jets with pt > 30 GeV'
    # Require leading jet pt to be pt > 200 GeV


    htLep2.Fill( htLepVal,weight )
    ptMET2.Fill( met,weight )
    pfIso2.Fill( muonPfisos[imuonPt] / muonPt, weight )
    event.getByLabel (ak5JetCSVLabel, ak5JetCSVHandle)
    ak5JetCSVs = ak5JetCSVHandle.product()

    event.getByLabel (ak5JetSecvtxMassLabel, ak5JetSecvtxMassHandle)
    ak5JetSecvtxMasses = ak5JetSecvtxMassHandle.product()


    ntags = 0
    for csv in ak5JetCSVs :
        if csv > options.bDiscCut :
            ntags += 1

    if ntags < 1 :
        if options.makeResponse == True :
            response.Miss( hadTop.p4.Perp(), weight )        
        continue


    if options.debug :
        print 'Have at least one b-tag'

    htLep3.Fill( htLepVal,weight )
    ptMET3.Fill( met,weight )
    pfIso3.Fill( muonPfisos[imuonPt] / muonPt, weight )

    ## event.getByLabel (ca8JetEtaLabel, ca8JetEtaHandle)
    ## ca8JetEtas = ca8JetEtaHandle.product()
    ## event.getByLabel (ca8JetPhiLabel, ca8JetPhiHandle)
    ## ca8JetPhis = ca8JetPhiHandle.product()
    ## event.getByLabel (ca8JetMassLabel, ca8JetMassHandle)
    ## ca8JetMasss = ca8JetMassHandle.product()
    ## event.getByLabel (ca8JetDa0MassLabel, ca8JetDa0MassHandle)
    ## ca8JetDa0Masses = ca8JetDa0MassHandle.product()
    ## event.getByLabel (ca8JetDa1MassLabel, ca8JetDa1MassHandle)
    ## ca8JetDa1Masses = ca8JetDa1MassHandle.product()
    

    event.getByLabel (topTagPtLabel, topTagPtHandle)
    topTagPt = topTagPtHandle.product()

    event.getByLabel (topTagPhiLabel, topTagPhiHandle)
    topTagPhi = topTagPhiHandle.product()
    event.getByLabel (topTagEtaLabel, topTagEtaHandle)
    topTagEta = topTagEtaHandle.product()
    event.getByLabel (topTagMassLabel, topTagMassHandle)
    topTagMass = topTagMassHandle.product()
    event.getByLabel (topTagMinMassLabel, topTagMinMassHandle)
    topTagMinMass = topTagMinMassHandle.product()
    event.getByLabel (topTagNSubjetsLabel, topTagNSubjetsHandle)
    topTagNSub = topTagNSubjetsHandle.product()


    event.getByLabel (topTagsj0ptLabel, topTagsj0ptHandle)
    Topsj0pt 		= 	topTagsj0ptHandle.product() 

    event.getByLabel (topTagsj0etaLabel, topTagsj0etaHandle)
    Topsj0eta 		= 	topTagsj0etaHandle.product() 

    event.getByLabel (topTagsj0phiLabel, topTagsj0phiHandle)
    Topsj0phi 		= 	topTagsj0phiHandle.product() 

    event.getByLabel (topTagsj0massLabel, topTagsj0massHandle)
    Topsj0mass 		= 	topTagsj0massHandle.product() 


    hadJets = []
    hadJetsMu = []
    hadJetsBDisc = []
    lepJets = []
    lepcsvs = []
    lepVtxMass = []
    ht = htLepVal
    #print metphi
    metv = ROOT.TLorentzVector()
    metv.SetPtEtaPhiM( met, 0.0, metphi, 0.0)

    # Use AK5 jets for the leptonic side, and
    # use CA8 jets for the hadronic side (below). This is
    # because we want to fit the secondary vertex
    # mass of the lepton-side b-jet. 
    for ijet in range(0,len(ak5Jets)) :
        if ak5Jets[ijet].Perp() > 30.0 :
            jet = ak5Jets[ijet]
            ht += jet.Perp()
            if jet.DeltaR( lepP4 ) < ROOT.TMath.Pi() / 2.0 :
                lepJets.append( jet )
		lepcsvs.append(ak5JetCSVs[ijet])
                lepVtxMass.append( ak5JetSecvtxMasses[ijet] )



    if len(lepJets) < 1:
        if options.makeResponse == True :
            response.Miss( hadTop.p4.Perp(), weight )        
	continue
	
    ht3.Fill( ht,weight )
    vtxMass3.Fill( lepVtxMass[0], weight)

    if options.htCut is not None and ht < options.htCut :
        if options.makeResponse == True :
            response.Miss( hadTop.p4.Perp(), weight )        
        continue

    if options.debug :
        print 'Passed HT cut'
    ht4.Fill( ht,weight )
    vtxMass4.Fill( lepVtxMass[0], weight)
    ## highestMassJetIndex = -1
    ## highestJetMass = -1.0
    ## bJetCandIndex = -1
    ## # Find highest mass jet for W-candidate
    ## for ijet in range(0,len(hadJets)):
    ##     antitagged = hadJetsBDisc[ijet] < options.bDiscCut or options.bDiscCut < 0.0 
    ##     if hadJets[ijet].M() > highestJetMass and antitagged :
    ##         highestJetMass = hadJets[ijet].M()
    ##         highestMassJetIndex = ijet
            


    leptoppt = (metv+lepJets[0]+lepP4).Perp()
    pt1 = leptoppt 
    Bin = weightPlot.FindBin(pt1)
    ttweight = weightPlot.GetBinContent(Bin)


    ntagslep=0

    
    sjmass = []
    sjeta = []
    sjphi = []
    sjpt = []


    sjmass.append(Topsj0mass[0])
    sjpt.append(Topsj0pt[0])
    sjeta.append(Topsj0eta[0])
    sjphi.append(Topsj0phi[0])
    if topTagNSub[0] > 1:
    	event.getByLabel (topTagsj1ptLabel, topTagsj1ptHandle)
    	Topsj1pt 		= 	topTagsj1ptHandle.product() 

    	event.getByLabel (topTagsj1etaLabel, topTagsj1etaHandle)
    	Topsj1eta 		= 	topTagsj1etaHandle.product() 

    	event.getByLabel (topTagsj1phiLabel, topTagsj1phiHandle)
    	Topsj1phi 		= 	topTagsj1phiHandle.product() 

    	event.getByLabel (topTagsj1massLabel, topTagsj1massHandle)
    	Topsj1mass 		= 	topTagsj1massHandle.product() 


    	sjmass.append(Topsj1mass[0])
    	sjpt.append(Topsj1pt[0])
    	sjeta.append(Topsj1eta[0])
    	sjphi.append(Topsj1phi[0])
    if topTagNSub[0] > 2:
    	event.getByLabel (topTagsj2ptLabel, topTagsj2ptHandle)
    	Topsj2pt 		= 	topTagsj2ptHandle.product() 


    	event.getByLabel (topTagsj2etaLabel, topTagsj2etaHandle)
    	Topsj2eta 		= 	topTagsj2etaHandle.product() 

    	event.getByLabel (topTagsj2phiLabel, topTagsj2phiHandle)
    	Topsj2phi 		= 	topTagsj2phiHandle.product()

    	event.getByLabel (topTagsj2massLabel, topTagsj2massHandle)
    	Topsj2mass 		= 	topTagsj2massHandle.product() 

    	sjmass.append(Topsj2mass[0])
    	sjpt.append(Topsj2pt[0])
    	sjeta.append(Topsj2eta[0])
    	sjphi.append(Topsj2phi[0])

    if topTagNSub[0] > 3:
    	event.getByLabel (topTagsj3ptLabel, topTagsj3ptHandle)
    	Topsj3pt 		= 	topTagsj3ptHandle.product()

    	event.getByLabel (topTagsj3etaLabel, topTagsj3etaHandle)
    	Topsj3eta 		= 	topTagsj3etaHandle.product()

    	event.getByLabel (topTagsj3phiLabel, topTagsj3phiHandle)
    	Topsj3phi 		= 	topTagsj3phiHandle.product() 

    	event.getByLabel (topTagsj3massLabel, topTagsj3massHandle)
    	Topsj3mass 		= 	topTagsj3massHandle.product()

    	sjmass.append(Topsj3mass[0])
    	sjpt.append(Topsj3pt[0])
    	sjeta.append(Topsj3eta[0])
    	sjphi.append(Topsj3phi[0])




    sj = ROOT.TLorentzVector()
    sjets = []
    sjets.append(ROOT.TLorentzVector())
    sjets[0].SetPtEtaPhiM( sjpt[0], sjeta[0], sjphi[0], sjmass[0] )
    topcomp = ROOT.TLorentzVector()
    topcomp.SetPtEtaPhiM( sjpt[0], sjeta[0], sjphi[0], sjmass[0] )
    #print str(topTagNSub[0]) + " subjets"
    for isub in range(1,int(topTagNSub[0])):
	#print isub
	sj.SetPtEtaPhiM( sjpt[isub], sjeta[isub], sjphi[isub], sjmass[isub] )
	sjets.append(ROOT.TLorentzVector())	
	sjets[isub].SetPtEtaPhiM( sjpt[isub], sjeta[isub], sjphi[isub], sjmass[isub] )
	#print sj.M()
	topcomp+=sj



    for lepcsv in lepcsvs :
        if lepcsv > options.bDiscCut :
            	ntagslep += 1
    if ntagslep<1:
        if options.makeResponse == True :
            response.Miss( hadTop.p4.Perp(), weight )        
	continue

    if options.debug :
        print 'Have a leptonic-side btag'
    ht5.Fill( ht, weight )
    vtxMass5.Fill( lepVtxMass[0], weight)
	
    #print "weight " + str(weight)
    nvtx =float(numvert[0])

    if len(topTagPt) > 0:
        if options.debug :
            print 'Have a CA8 jet'
        if options.ptWeight == True :
		t1weight=weight*ttweight
	else:
		t1weight=weight
	#if leptoppt > 400.0:
        jet1 = ROOT.TLorentzVector()
        jet1.SetPtEtaPhiM( topTagPt[0], topTagEta[0], topTagPhi[0], topTagMass[0] )
	jetScale = 1.0
        if abs( options.jecSys != 0 ) :
            jecUncAK7.setJetEta( topTagEta[0] )
            jecUncAK7.setJetPt( topTagPt[0] )
            if abs(options.jecSys) > 0.0001 :
                upOrDown = bool(options.jecSys > 0.0)
                unc1 = abs(jecUncAK7.getUncertainty(upOrDown))
                unc2 = flatJecUnc
                unc = math.sqrt(unc1*unc1 + unc2*unc2)
                #print 'Correction = ' + str( 1 + unc * options.jecSys)
                jetScale = 1 + unc * options.jecSys

	## also do Jet energy resolution variation 
	if abs(options.jerSys)>0.0001 :
	    genJet = findClosestInList( jet1, ca8GenJets )
	    scale = options.jerSys
	    recopt = jet1.Perp()
	    genpt = genJet.Perp()
	    deltapt = (recopt-genpt)*scale
	    ptscale = max(0.0, (recopt+deltapt)/recopt)
	    jetScale*=ptscale
		
	jet1 *= jetScale 
	    
	    

        jet = jet1
	ijet=0
     	if not len(lepJets) == 0:
            if options.ptWeight == True :
		t1weight=weight*ttweight
	    else:
		t1weight=weight

            passSelection = False
            if (jet.DeltaR( lepP4) > ROOT.TMath.Pi() / 2.0) :
                if (jet.Perp() > 200.):
		    topTagptHistprecuts.Fill(jet.Perp(),t1weight)
		    htLep3t1kin.Fill(htLepVal,t1weight)
		    nsj.Fill(topTagNSub[ijet],t1weight)
		    nvtxvsnsj.Fill(nvtx,topTagNSub[ijet],t1weight)
 		    if topTagNSub[ijet] > 2:
			minPairHist.Fill(topTagMinMass[ijet],t1weight)
			nvtxvsminmass.Fill(nvtx,topTagMinMass[ijet],t1weight)
			#WMassPairHist.Fill(WpairMass,t1weight)
			#WMassPairHistPtrel.Fill(WpairMassptrel,t1weight)
			#WMassPairHistDeltaR.Fill(WpairMassDeltaR,t1weight)
			#WMassPairHistmu.Fill(WPairMassmu,t1weight)
			#type1muHist.Fill(type1mu,t1weight)
			if topTagMinMass[ijet] > 50. :

				htLep3t1minp.Fill(htLepVal,t1weight)
                        	topTagMassHistpremass.Fill(jet.M(),t1weight)
				nvtxvstopmass.Fill(nvtx,jet.M(),t1weight)


   				event.getByLabel (nsubCA8Label, nsubCA8Handle)
    				nsubCA8Jets 		= 	nsubCA8Handle.product() 

    				event.getByLabel (topTagsj0csvLabel, topTagsj0csvHandle)
    				Topsj0BDiscCSV 		= 	topTagsj0csvHandle.product() 

    				event.getByLabel (topTagsj1csvLabel, topTagsj1csvHandle)
    				Topsj1BDiscCSV 		= 	topTagsj1csvHandle.product() 

    				event.getByLabel (topTagsj2csvLabel, topTagsj2csvHandle)
    				Topsj2BDiscCSV 		= 	topTagsj2csvHandle.product() 


    				event.getByLabel (TopTau2Label, TopTau2Handle)
    				Tau2		= 	TopTau2Handle.product() 

    				event.getByLabel (TopTau3Label, TopTau3Handle)
    				Tau3		= 	TopTau3Handle.product() 

				index = -1

				for iCAjet in range(0,len(nsubCA8Jets)):
        				CAjetTLV = ROOT.TLorentzVector()
					CAjetTLV.SetPtEtaPhiM( nsubCA8Jets[iCAjet].pt(), nsubCA8Jets[iCAjet].eta(), nsubCA8Jets[iCAjet].phi(), nsubCA8Jets[iCAjet].mass() )
					if (abs(jet.DeltaR(CAjetTLV))<0.5):
						index = iCAjet
						break

				TauDisc = Tau3[index]/Tau2[index]
						
				if jet.M() > 140. and jet.M() < 250.:
                                        goodEventst1.append( [ event.object().id().run(), event.object().id().luminosityBlock(), event.object().id().event() ] )
					htLep3t1topm.Fill(htLepVal,t1weight) 
                        		topTagptHist.Fill(jet.Perp(),t1weight)					
                        		topTagMassHist.Fill(jet.M(),t1weight)
					topTagtau32Hist.Fill(TauDisc,t1weight)

					nvtxvstau32.Fill(nvtx,TauDisc,t1weight)

                                        passSelection = True
				

				        ht6.Fill( ht, weight )
					vtxMass6.Fill( lepVtxMass[0], weight)

					if TauDisc<0.6:
						BDMax = max(Topsj0BDiscCSV[ijet],Topsj1BDiscCSV[ijet],Topsj2BDiscCSV[ijet])
						topTagBMaxHist.Fill(BDMax,t1weight)
						nvtxvsbmax.Fill(nvtx,BDMax,t1weight)
						topTagMassHistPostTau32.Fill(jet.M(),t1weight)
						if BDMax>0.679:
							topTagMassHistPostBDMax.Fill(jet.M(),t1weight)
	    if passSelection == True :
		npassed += 1
		ptRecoTop.Fill( topTagPt[ijet], t1weight )
            if options.makeResponse == True :		
                if passSelection == True :
                    response.Fill(  topTagPt[ijet], hadTop.p4.Perp(), t1weight )
                else :
                    response.Miss( hadTop.p4.Perp(), t1weight )



print  'Total Events: ' + str(count)
print  'Passed      : ' + str(npassed)
print  '            = ' + str( (float(npassed)/float(count)) * 100. ) + '%'
f.cd()

if options.makeResponse :
    response.Write()

f.Write()

f.Close()

if options.printEvents :
    Outf1   =   open("type2skim/" + name + "Type2Skim.txt", "w")
    sys.stdout = Outf1
    for goodEvent in goodEvents :
        print '{0:12.0f}:{1:12.0f}:{2:12.0f}'.format(
            goodEvent[0], goodEvent[1], goodEvent[2]
        )
    Outf2   =   open("type1skim/" + name + "Type1Skim.txt", "w")
    sys.stdout = Outf2
    for goodEvent in goodEventst1 :
        print '{0:12.0f}:{1:12.0f}:{2:12.0f}'.format(
            goodEvent[0], goodEvent[1], goodEvent[2]
        )

    Outf3   =   open("fullskim/" + name + "Skim.txt", "w")
    sys.stdout = Outf3
    for goodEvent in goodEvents :
        print '{0:12.0f}:{1:12.0f}:{2:12.0f}'.format(
            goodEvent[0], goodEvent[1], goodEvent[2]
        )
    for goodEvent in goodEventst1 :
        print '{0:12.0f}:{1:12.0f}:{2:12.0f}'.format(
            goodEvent[0], goodEvent[1], goodEvent[2]
        )


print "Total time = " + str( time.time() - start_time) + " seconds"
