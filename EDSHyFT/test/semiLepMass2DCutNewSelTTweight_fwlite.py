#! /usr/bin/env python
import os
import glob

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
def findClosestLepJet(lepJets ) :
    minDR = 9999.
    ret = -1
    for jjet in range(0,len(lepJets) ):
        dR = lepP4.DeltaR(lepJets[jjet])
        if dR < minDR :
            minDR = lepP4.DeltaR(lepJets[jjet])
            ret = jjet
    return ret
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


parser.add_option('--ptCut', metavar='F', type='float', action='store',
                  default=200.0,
                  dest='ptCut',
                  help='Leading jet PT cut')

parser.add_option('--bDiscCut', metavar='F', type='float', action='store',
                  default=0.679,
                  dest='bDiscCut',
                  help='B discriminator cut')

(options, args) = parser.parse_args()

argv = []

eventsbegin = [1,10000001,20000001,30000001,40000001,50000001,60000001,70000001]
eventsend = [10000000,20000000,30000000,40000000,50000000,60000000,70000000,80000000]

if options.num != 'all':
	ifile=int(options.num)

import ROOT
ROOT.gROOT.Macro("rootlogon.C")


import sys
from DataFormats.FWLite import Events, Handle

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
topTagugMassHistpremass= ROOT.TH1F("topTagugMassHistpremass",         "Mass of Top Candidate from Hadronic Jets type 1 pre mass cut;Mass;Number",  300, 0., 600. )
topTagMassHist= ROOT.TH1F("topTagMassHist",         "Mass of Top Candidate from Hadronic Jets type 1;Mass;Number",  300, 0., 600. )
topTagMassHistPostTau32= ROOT.TH1F("topTagMassHistPostTau32",         "Mass of Top Candidate from Hadronic Jets type 1;Mass;Number",  300, 0., 600. )
topTagMassHistPostBDMax= ROOT.TH1F("topTagMassHistPostBDMax",         "Mass of Top Candidate from Hadronic Jets type 1;Mass;Number",  300, 0., 600. )

topTagptHist= ROOT.TH1F("topTagptHist",         "Pt of Top Candidate from Hadronic Jets type 1;Mass;Number",  375, 0., 1500. )
topTagtau32Hist= ROOT.TH1F("topTagtau32Hist",         "tau32 of Top Candidate from Hadronic Jets type 1;Tau32;Number",  150, 0., 1.5 )
topTagBMaxHist= ROOT.TH1F("topTagBMaxHist",         "BMax of Top Candidate from Hadronic Jets type 1;CSV;Number",  150, 0., 1.5 )


topTagugmtau32Hist= ROOT.TH1F("topTagugmtau32Hist",         "tau32 of Top Candidate from Hadronic Jets type 1;Tau32;Number",  150, 0., 1.5 )
topTagugmBMaxHist= ROOT.TH1F("topTagugmBMaxHist",         "BMax of Top Candidate from Hadronic Jets type 1;CSV;Number",  150, 0., 1.5 )


ptlep= ROOT.TH1F("ptlep",         "Pt Leptonic top",  150, 0., 1500. )
topTagptHistprecuts= ROOT.TH1F("topTagptHistprecuts",         "Pt of Top Candidate from Hadronic Jets type 1;Mass;Number",  375, 0., 1500. )
topTagptHistprept= ROOT.TH1F("topTagptHistprept",         "Pt of Top Candidate from Hadronic Jets type 1;Mass;Number",  375, 0., 1500. )
minPairHist= ROOT.TH1F("minPairHist",         "Minimum Pairwise mass",  150, 0., 150. )
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


topcandugmassprekin =  ROOT.TH1F("topcandugmassprekin",         "Mass of Top Candidate from Hadronic Jets type 1 pre mass cut;Mass;Number",  300, 0., 600. )
topcandugmasspostkin =  ROOT.TH1F("topcandugmasspostkin",         "Mass of Top Candidate from Hadronic Jets type 1 pre mass cut;Mass;Number",  300, 0., 600. )
topcandugmasspostnsj =  ROOT.TH1F("topcandugmasspostnsj",         "Mass of Top Candidate from Hadronic Jets type 1 pre mass cut;Mass;Number",  300, 0., 600. )
topcandugmasspostminmass =  ROOT.TH1F("topcandugmasspostminmass",         "Mass of Top Candidate from Hadronic Jets type 1 pre mass cut;Mass;Number",  300, 0., 600. )
topcandugmassposttau32 =  ROOT.TH1F("topcandugmassposttau32",         "Mass of Top Candidate from Hadronic Jets type 1 pre mass cut;Mass;Number",  300, 0., 600. )
topcandugmasspostbmax =  ROOT.TH1F("topcandugmasspostbmax",         "Mass of Top Candidate from Hadronic Jets type 1 pre mass cut;Mass;Number",  300, 0., 600. )




topTagMassHistpremasshighpt= ROOT.TH1F("topTagMassHistpremasshighpt",         "Mass of Top Candidate from Hadronic Jets type 1 pre mass cut;Mass;Number",  300, 0., 600. )
topTagMassHisthighpt= ROOT.TH1F("topTagMassHisthighpt",         "Mass of Top Candidate from Hadronic Jets type 1;Mass;Number",  300, 0., 600. )
topTagptHisthighpt= ROOT.TH1F("topTagptHisthighpt",         "Pt of Top Candidate from Hadronic Jets type 1;Mass;Number",  375, 0., 1500. )
minPairHisthighpt= ROOT.TH1F("minPairHisthighpt",         "Minimum Pairwise mass",  150, 0., 150. )

ht3 = ROOT.TH1F("ht3", "HT", 200, 0., 2000.)
ht4 = ROOT.TH1F("ht4", "HT", 200, 0., 2000.)

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

ptRelVsDRMinpre = ROOT.TH2F("ptRelVsDRMinpre", "ptrel vs mindr", 40, 0, 200, 15, 0, 1.5)
ptRelVsDRMin = ROOT.TH2F("ptRelVsDRMin", "ptrel vs mindr", 200, 0, 200, 15, 0, 1.5)

events = Events (files)

postfix = ""
if options.useLoose :
    postfix = "Loose"


puHandle    	= 	Handle("int")
puLabel     	= 	( "pileup", "npvRealTrue" )



CA8Handle     	= 	Handle( "vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > >")
CA8Label      	= 	( "nsub", "CA8P4" )

TopTau2Handle       = 	Handle( "std::vector<double>" )
TopTau2Label    	= 	( "nsub" , "Tau2")

TopTau3Handle       = 	Handle( "std::vector<double>" )
TopTau3Label    	= 	( "nsub" , "Tau3")



jetPtHandle         = Handle( "std::vector<float>" )
jetPtLabel    = ( "pfShyftTupleJetsLoose",   "pt" )
jetEtaHandle         = Handle( "std::vector<float>" )
jetEtaLabel    = ( "pfShyftTupleJetsLoose",   "eta" )
jetPhiHandle         = Handle( "std::vector<float>" )
jetPhiLabel    = ( "pfShyftTupleJetsLoose",   "phi" )
jetMassHandle         = Handle( "std::vector<float>" )
jetMassLabel    = ( "pfShyftTupleJetsLoose",   "mass" )
jetDa0MassHandle         = Handle( "std::vector<float>" )
jetDa0MassLabel    = ( "pfShyftTupleJetsLoose",   "da0Mass" )
jetDa1MassHandle         = Handle( "std::vector<float>" )
jetDa1MassLabel    = ( "pfShyftTupleJetsLoose",   "da1Mass" )
jetCSVHandle         = Handle( "std::vector<float>" )
jetCSVLabel    = ( "pfShyftTupleJetsLoose",   "csv" )

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
muonPtLabel    = ( "pfShyftTupleMuonsLoose",   "pt" )
muonEtaHandle         = Handle( "std::vector<float>" )
muonEtaLabel    = ( "pfShyftTupleMuonsLoose",   "eta" )
muonPhiHandle         = Handle( "std::vector<float>" )
muonPhiLabel    = ( "pfShyftTupleMuonsLoose",   "phi" )
muonPfisoHandle         = Handle( "std::vector<float>" )
muonPfisoLabel    = ( "pfShyftTupleMuonsLoose",   "pfisoPU" )


TightmuonPtHandle         = Handle( "std::vector<float>" )
TightmuonPtLabel    = ( "pfShyftTupleMuons",   "pt" )
TightmuonEtaHandle         = Handle( "std::vector<float>" )
TightmuonEtaLabel    = ( "pfShyftTupleMuons",   "eta" )
TightmuonPhiHandle         = Handle( "std::vector<float>" )
TightmuonPhiLabel    = ( "pfShyftTupleMuons",   "phi" )
TightmuonPfisoHandle         = Handle( "std::vector<float>" )
TightmuonPfisoLabel    = ( "pfShyftTupleMuons",   "pfisoPU" )


electronPtHandle         = Handle( "std::vector<float>" )
electronPtLabel    = ( "pfShyftTupleElectronsLoose",   "pt" )
electronEtaHandle         = Handle( "std::vector<float>" )
electronEtaLabel    = ( "pfShyftTupleElectronsLoose",   "eta" )
electronPhiHandle         = Handle( "std::vector<float>" )
electronPhiLabel    = ( "pfShyftTupleElectronsLoose",   "phi" )
electronPfisoHandle         = Handle( "std::vector<float>" )
electronPfisoLabel    = ( "pfShyftTupleElectronsLoose",   "pfisoPU" )

metHandle = Handle( "std::vector<float>" )
metLabel = ("pfShyftTupleMETLoose",   "pt" )

metphiHandle = Handle( "std::vector<float>" )
metphiLabel = ("pfShyftTupleMETLoose",   "phi" )

goodEvents = []
goodEventst1 = []
mptv=0
# loop over events
count = 0
print "Start looping"
nhptbj=0

if options.set == 'mcatnlo':
	print "Using MC@NLO"
	weightFile = ROOT.TFile("ptlepNewSelmcatnlo_2Dweight.root")
elif options.set == 'powheg':
	print "Using Powheg"
	weightFile = ROOT.TFile("ptlepNewSelpowheg_2Dweight.root")
else:
	print "Using MadGraph"
	weightFile = ROOT.TFile("ptlepNewSel_2Dweight.root")
if options.ptWeight == False :
	print "Turning pt reweighting off"
weightPlot = weightFile.Get("lepptweight")

for event in events:
    weight = 1.0
    count = count + 1
    if count % 10000 == 0 :
      print  '--------- Processing Event ' + str(count)
    if options.num != 'all':
	if not (eventsbegin[ifile-1] <= count <= eventsend[ifile-1]):
		continue 
    #if count > 200000:
	#break
 #   if mptv % 100 == 0 :
  #    print  '--------- mptv fail ' + str(mptv)



    #Require exactly one lepton (e or mu)

    lepType = 0 # Let 0 = muon, 1 = electron    
    event.getByLabel (muonPtLabel, muonPtHandle)
    if not muonPtHandle.isValid():
	mptv+=1
        continue
    muonPts = muonPtHandle.product()

    #if True :
     #   event.getByLabel (muonPfisoLabel, muonPfisoHandle)
      #  if not muonPfisoHandle.isValid():
       #     continue
        #muonPfisos = muonPfisoHandle.product()

    nMuonsVal = 0
    for imuonPt in range(0,len(muonPts)):
        muonPt = muonPts[imuonPt]
        if muonPt > 45.0 :
                nMuonsVal += 1
                lepType = 0   
	else:
		continue 
             
    if options.pileup != 'none':   
    	event.getByLabel (puLabel, puHandle)
    	PileUp 		= 	puHandle.product()
    	bin1 = PilePlot.FindBin(PileUp[0]) 
    	weight *= PilePlot.GetBinContent(bin1)
	#print "weight is " + str(weight)
        
    nMuons.Fill( nMuonsVal,weight )
    #print "Filling???"
    if nMuonsVal > 0 :
        ptMu.Fill( muonPts[0],weight )

    event.getByLabel (electronPtLabel, electronPtHandle)
    electronPts = electronPtHandle.product()

    event.getByLabel (topTagEtaLabel, topTagEtaHandle)
    topTagEta = topTagEtaHandle.product()
    if not options.type2:
	if len(topTagEta)<1:
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
            continue
    else :
        if nMuonsVal != 1:
            continue


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

        
    event.getByLabel (metLabel, metHandle)
    mets = metHandle.product()
    met = mets[0]

    htLepVal = met + lepP4.Perp()

    htLep0.Fill( htLepVal,weight )
    ptMET0.Fill( met,weight )

    event.getByLabel (jetPtLabel, jetPtHandle)
    jetPts = jetPtHandle.product()


    nJetsVal = 0
    for jetPt in jetPts:
        if jetPt > 30.0 :
            nJetsVal += 1
    
    nJets.Fill( nJetsVal,weight )

    # Require >= 2 jets above 30 GeV
    if nJetsVal < 2 :
        continue

    htLep1.Fill( htLepVal,weight )
    ptMET1.Fill( met,weight )
    ptJet0.Fill( jetPts[0],weight )
    
    # Require leading jet pt to be pt > 200 GeV


    htLep2.Fill( htLepVal,weight )
    ptMET2.Fill( met,weight )
    event.getByLabel (jetCSVLabel, jetCSVHandle)
    jetCSVs = jetCSVHandle.product()

    ntags = 0
    for csv in jetCSVs :
        if csv > options.bDiscCut :
            ntags += 1

    if ntags < 1 :
        continue




    htLep3.Fill( htLepVal,weight )
    ptMET3.Fill( met,weight )
    # Break the jets up by hemisphere
    event.getByLabel (jetEtaLabel, jetEtaHandle)
    jetEtas = jetEtaHandle.product()
    event.getByLabel (jetPhiLabel, jetPhiHandle)
    jetPhis = jetPhiHandle.product()
    event.getByLabel (jetMassLabel, jetMassHandle)
    jetMasss = jetMassHandle.product()
    event.getByLabel (jetDa0MassLabel, jetDa0MassHandle)
    jetDa0Masses = jetDa0MassHandle.product()
    event.getByLabel (jetDa1MassLabel, jetDa1MassHandle)
    jetDa1Masses = jetDa1MassHandle.product()


    hadJets = []
    hadJetsMu = []
    hadJetsBDisc = []
    lepJets = []
    lepcsvs = []
    ht = htLepVal
    event.getByLabel (metphiLabel, metphiHandle)
    metphis = metphiHandle.product()
    metphi = metphis[0]
    #print metphi
    metv = ROOT.TLorentzVector()
    metv.SetPtEtaPhiM( met, 0.0, metphi, 0.0)

    if met < 50 :
        continue

    htmu = met + lepPt
    if htmu < 150 :
        continue


    event.getByLabel (TightmuonPtLabel, TightmuonPtHandle)
    event.getByLabel (TightmuonEtaLabel, TightmuonEtaHandle)
    event.getByLabel (TightmuonPhiLabel, TightmuonPhiHandle)
    nTightmuVal = 0
    if TightmuonPtHandle.isValid() :
        tightmuPts = TightmuonPtHandle.product()
        tightmuEtas = TightmuonEtaHandle.product()            
        tightmuPhis = TightmuonPhiHandle.product()
        muP4 = ROOT.TLorentzVector()
        muP4.SetPtEtaPhiM( tightmuPts[0], tightmuEtas[0], tightmuPhis[0], lepMass )
        if muP4.DeltaR(lepP4) < 0.1:
            nTightmuVal += 1


    for ijet in range(0,len(jetPts)) :
        if jetPts[ijet] > 30.0 :
            jet = ROOT.TLorentzVector()
            jet.SetPtEtaPhiM( jetPts[ijet], jetEtas[ijet], jetPhis[ijet], jetMasss[ijet] )
            ht += jet.Perp()
            if jet.DeltaR( lepP4 ) > ROOT.TMath.Pi() / 2.0 :
                hadJets.append( jet )
                hadJetsBDisc.append( jetCSVs[ijet] )
                mu0 = jetDa0Masses[ijet] / jetMasss[ijet]
                mu1 = jetDa1Masses[ijet] / jetMasss[ijet]
                mu = mu0
                if mu1 > mu0 :
                    mu = mu1
                hadJetsMu.append( mu )
            else :
                lepJets.append( jet )
		lepcsvs.append(jetCSVs[ijet])

    ht3.Fill( ht,weight )

    if len(lepJets) < 1:
        continue

    closejet = findClosestLepJet(lepJets ) 
    if nTightmuVal < 1 :
        if lepJets[closejet].DeltaR(lepP4) < 0.8:
            lepJets[closejet] = lepJets[closejet] - lepP4

    ptrel = lepP4.Perp(lepJets[closejet].Vect())
    Pass2d = 0
    minDR = lepJets[closejet].DeltaR(lepP4)

    ptRelVsDRMinpre.Fill(ptrel, minDR, weight)

    if minDR > 0.5:
        Pass2d += 1

    if ptrel > 25:
        Pass2d += 1
        
    if Pass2d < 1: 
	continue 
   # passed = 1
    ptRelVsDRMin.Fill(ptrel, minDR, weight)


    if options.htCut is not None and ht < options.htCut :
        continue


    ht4.Fill( ht,weight )
    highestMassJetIndex = -1
    highestJetMass = -1.0
    bJetCandIndex = -1
    # Find highest mass jet for W-candidate
    for ijet in range(0,len(hadJets)):
        antitagged = hadJetsBDisc[ijet] < options.bDiscCut or options.bDiscCut < 0.0 
        if hadJets[ijet].M() > highestJetMass and antitagged :
            highestJetMass = hadJets[ijet].M()
            highestMassJetIndex = ijet
            

    # Find b-jet candidate
    if options.useClosestForTopMass == True :
        # If we want the closest, grab it
        bJetCandIndex = findClosestJet( highestMassJetIndex, hadJets )
    else :
        # If we want the b-jet candidate to b-tagged,
        # take the highest pt b-tagged jet
        for ijet in range(0,len(hadJets)):
            if ijet == highestMassJetIndex :
                continue
            if hadJetsBDisc[ijet] > options.bDiscCut :
                bJetCandIndex = ijet
                break

    if len(lepJets) < 1:
	continue 

    leptoppt = (metv+lepJets[0]+lepP4).Perp()
    pt1 = leptoppt 
    Bin = weightPlot.FindBin(pt1)
    ttweight = weightPlot.GetBinContent(Bin)


#######################TYPE2ONLY
    if options.type2 == True:
			
     if jetPts[0] < 200 :
        continue	
     if options.ptWeight == True :
		t1weight=weight*ttweight
     else:
		t1weight=weight		
     if highestJetMass >= 0 : # and hadJets[highestMassJetIndex].Perp() > 200.0 :
        if bJetCandIndex >= 0 :
        	topCandP4 = hadJets[highestMassJetIndex] + hadJets[bJetCandIndex]
		if topCandP4.Perp()>400.:
        		muHisthighpt.Fill( hadJetsMu[highestMassJetIndex],t1weight)
        		if hadJetsMu[highestMassJetIndex] < 0.4 :
	        		mWCandhighpt.Fill( highestJetMass,t1weight )	 
                		if 60.0 < highestJetMass < 130.0 :  
                    			mTopCandhighpt.Fill( topCandP4.M(),t1weight )

	htLep3mu.Fill(htLepVal,t1weight)
        muHist.Fill( hadJetsMu[highestMassJetIndex],t1weight)
        mWCandVsMuCut.Fill( highestJetMass, hadJetsMu[highestMassJetIndex],t1weight)
        mWCandVsPtWCand.Fill( hadJets[highestMassJetIndex].Perp(), highestJetMass,t1weight )
        #if bJetCandIndex >= 0 :
        #    dRWbHist.Fill( hadJets[highestMassJetIndex].DeltaR(hadJets[bJetCandIndex] ) )
        if hadJetsMu[highestMassJetIndex] < 0.4 :
	    htLep3w.Fill(htLepVal,t1weight)
            mWCand.Fill( highestJetMass,t1weight )
            scale = 1.0
            mWCandVsPtWCandMuCut.Fill( hadJets[highestMassJetIndex].Perp(), highestJetMass,t1weight )
            if bJetCandIndex >= 0 :
                hadJets[highestMassJetIndex] *= scale
                hadJets[bJetCandIndex] *= scale
                topCandP4 = hadJets[highestMassJetIndex] + hadJets[bJetCandIndex]
                mWCandVsMTopCand.Fill( highestJetMass, topCandP4.M(),t1weight )

                if 60.0 < highestJetMass < 130.0 :
		    htLep3top.Fill(htLepVal,t1weight)
                    mTopCand.Fill( topCandP4.M(),t1weight )
                    ptTopCand.Fill( topCandP4.Perp(),t1weight )
                    ptWFromTopCand.Fill( hadJets[highestMassJetIndex].Perp(),t1weight )
                    ptbFromTopCand.Fill( hadJets[bJetCandIndex].Perp(),t1weight )
                    dRWbHist.Fill( hadJets[highestMassJetIndex].DeltaR(hadJets[bJetCandIndex]),t1weight)
                    #print 'w index = ' + str(highestMassJetIndex) + ', b index = ' + str(bJetCandIndex) + ', dR = ' + str(hadJets[highestMassJetIndex].DeltaR(hadJets[bJetCandIndex] ))
                    if hadJets[bJetCandIndex].Perp()>120.0:
			goodEvents.append( [ event.object().id().run(), event.object().id().luminosityBlock(), event.object().id().event() ] )

     continue
#######################TYPE2ONLY


    event.getByLabel (topTagPtLabel, topTagPtHandle)
    topTagPt = topTagPtHandle.product()
    event.getByLabel (topTagEtaLabel, topTagEtaHandle)
    topTagEta = topTagEtaHandle.product()
    event.getByLabel (topTagPhiLabel, topTagPhiHandle)
    topTagPhi = topTagPhiHandle.product()
    event.getByLabel (topTagMassLabel, topTagMassHandle)
    topTagMass = topTagMassHandle.product()
    event.getByLabel (topTagMinMassLabel, topTagMinMassHandle)
    topTagMinMass = topTagMinMassHandle.product()
    event.getByLabel (topTagNSubjetsLabel, topTagNSubjetsHandle)
    topTagNSub = topTagNSubjetsHandle.product()
    ntagslep=0

    ugmass = -1
    
    sjmass = []
    sjeta = []
    sjphi = []
    sjpt = []

    if len(topTagPt) < 1:
	continue


############################GROOMED MASS CALCULATION
    event.getByLabel (topTagsj0ptLabel, topTagsj0ptHandle)
    Topsj0pt 		= 	topTagsj0ptHandle.product() 

    event.getByLabel (topTagsj0etaLabel, topTagsj0etaHandle)
    Topsj0eta 		= 	topTagsj0etaHandle.product() 

    event.getByLabel (topTagsj0phiLabel, topTagsj0phiHandle)
    Topsj0phi 		= 	topTagsj0phiHandle.product() 

    event.getByLabel (topTagsj0massLabel, topTagsj0massHandle)
    Topsj0mass 		= 	topTagsj0massHandle.product() 

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
    topcomp = ROOT.TLorentzVector()
    topcomp.SetPtEtaPhiM( sjpt[0], sjeta[0], sjphi[0], sjmass[0] )
    #print str(topTagNSub[0]) + " subjets"
    for isub in range(1,int(topTagNSub[0])):
	#print isub
	sj.SetPtEtaPhiM( sjpt[isub], sjeta[isub], sjphi[isub], sjmass[isub] )
	#print sj.M()
	topcomp+=sj
    ugmass = topcomp.M()
############################GROOMED MASS CALCULATION


    for lepcsv in lepcsvs :
        if lepcsv > options.bDiscCut :
            	ntagslep += 1
    if ntagslep<1:
	continue
	
    #print "weight " + str(weight)

    if len(topTagPt) > 0:
        if options.ptWeight == True :
		t1weight=weight*ttweight
	else:
		t1weight=weight
	#if leptoppt > 400.0:
        jet1 = ROOT.TLorentzVector()
        jet1.SetPtEtaPhiM( topTagPt[0], topTagEta[0], topTagPhi[0], topTagMass[0] )
	if ntagslep>0:
        	if (jet1.DeltaR( lepP4) > ROOT.TMath.Pi() / 2.0) :
			ptlep.Fill(leptoppt,t1weight)
			topcandmassprekin.Fill(topTagMass[0],t1weight)

			topcandugmassprekin.Fill(ugmass,t1weight)
			leptopptvstopmassprekin.Fill(leptoppt,topTagMass[0],t1weight)
                	if (topTagPt[0] > 400.):
				
				topcandmasspostkin.Fill(topTagMass[0],t1weight)
				topcandugmasspostkin.Fill(ugmass,t1weight)
				leptopptvstopmasspostkin.Fill(leptoppt,topTagMass[0],t1weight)		
 		    		if topTagNSub[0] > 2:
					leptopptvstopmasspostnsj.Fill(leptoppt,topTagMass[0],t1weight)
					topcandmasspostnsj.Fill(topTagMass[0],t1weight)		
					topcandugmasspostnsj.Fill(ugmass,t1weight)		
					if topTagMinMass[0] > 50. :
						leptopptvstopmasspostminmass.Fill(leptoppt,topTagMass[0],t1weight)
						topcandmasspostminmass.Fill(topTagMass[0],t1weight)
						topcandugmasspostminmass.Fill(ugmass,t1weight)
    						event.getByLabel (CA8Label, CA8Handle)
    						CA8Jets 		= 	CA8Handle.product() 

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

						for iCAjet in range(0,len(CA8Jets)):
        						CAjetTLV = ROOT.TLorentzVector()
							CAjetTLV.SetPtEtaPhiM( CA8Jets[iCAjet].pt(), CA8Jets[iCAjet].eta(), CA8Jets[iCAjet].phi(), CA8Jets[iCAjet].mass() )
							if (abs(jet1.DeltaR(CAjetTLV))<0.5):
								index = iCAjet
								break

						TauDisc = Tau3[index]/Tau2[index]
				
						if TauDisc<0.6:
							leptopptvstopmassposttau32.Fill(leptoppt,topTagMass[0],t1weight)
							topcandmassposttau32.Fill(topTagMass[0],t1weight)	
							topcandugmassposttau32.Fill(ugmass,t1weight)			
							BDMax = max(Topsj0BDiscCSV[0],Topsj1BDiscCSV[0],Topsj2BDiscCSV[0])
							if BDMax>0.679:
								leptopptvstopmasspostbmax.Fill(leptoppt,topTagMass[0],t1weight)
								topcandmasspostbmax.Fill(topTagMass[0],t1weight)
								topcandugmasspostbmax.Fill(ugmass,t1weight)				




     #for ijet in range(0, len(topTagPt)) :
	ijet=0
        jet = ROOT.TLorentzVector()
        jet.SetPtEtaPhiM( topTagPt[ijet], topTagEta[ijet], topTagPhi[ijet], topTagMass[ijet] )
     	if not len(lepJets) == 0:
            if options.ptWeight == True :
		t1weight=weight*ttweight
	    else:
		t1weight=weight

            if (jet.DeltaR( lepP4) > ROOT.TMath.Pi() / 2.0) :
                if (topTagPt[ijet] > 400.):
		    topTagptHistprecuts.Fill(topTagPt[ijet],t1weight)
		    htLep3t1kin.Fill(htLepVal,t1weight)
		    nsj.Fill(topTagNSub[ijet],t1weight)
 		    if topTagNSub[ijet] > 2:
			minPairHist.Fill(topTagMinMass[ijet],t1weight)
			if topTagMinMass[ijet] > 50. :
				htLep3t1minp.Fill(htLepVal,t1weight)
                        	topTagMassHistpremass.Fill(topTagMass[ijet],t1weight)
                        	topTagugMassHistpremass.Fill(topTagMass[ijet],t1weight)

   				event.getByLabel (CA8Label, CA8Handle)
    				CA8Jets 		= 	CA8Handle.product() 

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

				for iCAjet in range(0,len(CA8Jets)):
        				CAjetTLV = ROOT.TLorentzVector()
					CAjetTLV.SetPtEtaPhiM( CA8Jets[iCAjet].pt(), CA8Jets[iCAjet].eta(), CA8Jets[iCAjet].phi(), CA8Jets[iCAjet].mass() )
					if (abs(jet.DeltaR(CAjetTLV))<0.5):
						index = iCAjet
						break

				TauDisc = Tau3[index]/Tau2[index]
				if ugmass > 150. and ugmass < 230.:
					topTagugmtau32Hist.Fill(TauDisc,t1weight)
					if TauDisc<0.6:
						BDMax = max(Topsj0BDiscCSV[ijet],Topsj1BDiscCSV[ijet],Topsj2BDiscCSV[ijet])
						topTagugmBMaxHist.Fill(BDMax,t1weight)
						
				if topTagMass[ijet] > 140. and topTagMass[ijet] < 250.:
                                        goodEventst1.append( [ event.object().id().run(), event.object().id().luminosityBlock(), event.object().id().event() ] )
					htLep3t1topm.Fill(htLepVal,t1weight) 
                        		topTagptHist.Fill(topTagPt[ijet],t1weight)					
                        		topTagMassHist.Fill(topTagMass[ijet],t1weight)
					topTagtau32Hist.Fill(TauDisc,t1weight)
					if TauDisc<0.6:
						BDMax = max(Topsj0BDiscCSV[ijet],Topsj1BDiscCSV[ijet],Topsj2BDiscCSV[ijet])
						topTagBMaxHist.Fill(BDMax,t1weight)
						topTagMassHistPostTau32.Fill(topTagMass[ijet],t1weight)
						if BDMax>0.679:
							topTagMassHistPostBDMax.Fill(topTagMass[ijet],t1weight)


print  'Total Events: ' + str(count)
print  'isvalid() cuts: ' + str(mptv)
print  'percent cuts: ' + str((100*mptv)/count)+'%'
f.cd()
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
