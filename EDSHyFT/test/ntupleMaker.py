#! /usr/bin/env python

# Import everything from ROOT
from ROOT import *
gROOT.Macro("~/rootlogon.C")

import sys
import glob

from array import array
from optparse import OptionParser

# Create a command line option parser
parser = OptionParser()

parser.add_option('--files', metavar='F', type='string', action='store',
                  default = "edmTest1.root",
                  dest='files',
                  help='Input files')

parser.add_option("--sample", action='store',
                  default="DY",
                  dest="sample",
                  help="Sample Name")

parser.add_option('--JES', metavar='F', type='string', action='store',
                  default='nominal',
                  dest='JES',
                  help='JEC Systematic variation. Options are "nominal, up, down"')

parser.add_option('--jetSmear', metavar='F', type='float', action='store',
                  default=0.1,
                  dest='jetSmear',
                  help='JER smearing. Standard values are 0.1 (nominal), 0.0 (down), 0.2 (up)')

parser.add_option("--data", action='store_true',
                  default=False,
                  dest="data",
                  help="data / no pileup")

parser.add_option("--runMuons", action='store_true',
                  default=False,
                  dest="runMuons",
                  help="Electrons(1), Muons(0)")

parser.add_option("--bTag",action='store',
                  default="",
                  dest="bTag",
                  help="b-tag SF")

# Parse and get arguments
(options, args) = parser.parse_args()

runMu = options.runMuons

# JEC
jecScale = 0.0
if options.JES == 'up' :
    jecScale = 1.0
elif options.JES == 'down' :
    jecScale = -1.0
flatJecUnc = 0.0

# Import what we need from FWLite
from DataFormats.FWLite import Events, Handle
ROOT.gSystem.Load('libCondFormatsJetMETObjects')

# Get the file list. 
files = glob.glob( options.files )
print 'getting files: ', files

#JEC
jecParStr = std.string('Jec12_V2_Uncertainty_AK5PFchs.txt')
jecUnc = JetCorrectionUncertainty( jecParStr )
  
#------------------------------------------------------------------

# Get the FWLite "Events"
events = Events (files)

# Get a "handle" (i.e. a smart pointer) to the vector of jets
jetsH = Handle ("std::vector<pat::Jet>")
jetsLabel = ("pfTupleEle", "jets")

metH = Handle ("std::vector<pat::MET>")
metLabel = ("pfTupleEle", "met")

trigH = Handle("pat::TriggerEvent")
trigLabel = ("patTriggerEvent", "")

vertH  = Handle ("std::vector<reco::Vertex>")
vertLabel = ("goodOfflinePrimaryVertices")

pileupWeightsH = Handle ("std::vector<float>")
pileupWeightsLabel = ("pileupReweightingProducer","pileupWeights")

if runMu:
    leptonsH  = Handle ("std::vector<pat::Muon>")
    leptonsLabel = ("pfTupleEle", "muons")
else:
    leptonsH  = Handle ("std::vector<pat::Electron>")
    leptonsLabel = ("pfTupleEle", "electrons")
      
# Create an output file and a tree
systtag = ''
if options.JES != '':
	systtag = "_" + options.JES
elif options.bTag:
    systtag = "_" + options.bTag
    
print "value of options.JES = ", options.JES		
print "value of systtag = ", systtag

f = TFile(options.sample + systtag + ".root", "RECREATE")

f.cd()
t = TTree("tree","tree")

trig_path = array('i', [0])
t.Branch('trig_path', trig_path, 'trig_path/I')

met = array('d',[0.])
t.Branch('met',met,'met/D')

wMt = array('d',[0.])
t.Branch('wMt',wMt, 'wMt/D')

lepEt = array('d',[0.])
t.Branch('lepEt',lepEt,'lepEt/D')

deltaPhiMETe = array('d',[0.])
t.Branch('deltaPhiMETe', deltaPhiMETe, 'deltaPhiMETe/D')                    

deltaPhiMETLeadingJet = array('d',[0.])
t.Branch('deltaPhiMETLeadingJet', deltaPhiMETLeadingJet, 'deltaPhiMETLeadingJet/D')

lepEta = array('d',[0.])
t.Branch('lepEta',lepEta,'lepEta/D')

if not runMu:
    eSCEta = array('d',[0.])
    t.Branch('eSCEta',eSCEta,'eSCEta/D')

lepIso = array('d',[0.])
t.Branch('lepIso',lepIso,'lepIso/D')

nvertices = array('i',[0])
t.Branch('nVertices',nvertices,'nVertices/I')

njets = array('i',[0])
t.Branch('nJets',njets,'nJets/I')

max_nJets = 20
jetEt = array('d',max_nJets*[0.])
t.Branch('jetEt',jetEt,'jetEt[nJets]/D')

minDR_je = array('d',[0.])
t.Branch('minDR_je',minDR_je,'minDR_je/D')

nTagsCSVM = array('i',[0])
t.Branch('nTagsCSVM',nTagsCSVM,'nTagsCSVM/I')

ht = array('d',[0.])
t.Branch('ht',ht,'ht/D')

ht4jets = array('d',[0.0] )
t.Branch('ht4jets', ht4jets, 'ht4jets/D')

if not options.data :
    pileupWeight = array('d',[0.])
    t.Branch('pileupWeight',pileupWeight,'pileupWeight/D')
    
    pileupWeightUp = array('d',[0.])
    t.Branch('pileupWeightUp', pileupWeightUp,'pileupWeightUp/D')
    
    pileupWeightDown = array('d',[0.0])
    t.Branch('pileupWeightDown', pileupWeightDown, 'pileupWeightDown/D')
else:
    runNumber = array('i',[0])
    t.Branch('runNumber',runNumber,'runNumber/I')
    
    eventNumber = array('L',[0])
    t.Branch('eventNumber',eventNumber,'eventNumber/I')
    
    lumiNumber = array('i',[0])
    t.Branch('lumiNumber', lumiNumber,'lumiNumber/I')

# Keep some timing information
nEventsAnalyzed = 0
timer = TStopwatch()
timer.Start()

randomGenerator = TRandom()

# loop over events
i = 0
for event in events:
    i = i + 1
    if i % 1000 == 0 :
        print "EVENT ", i
    nEventsAnalyzed = nEventsAnalyzed + 1
    
    # Get the objects 
    event.getByLabel(vertLabel,  vertH)
    event.getByLabel(jetsLabel,  jetsH)    
    event.getByLabel(leptonsLabel, leptonsH)
    event.getByLabel(metLabel, metH)
    event.getByLabel(trigLabel, trigH)
   
    # PileupReweighting
    if not options.data :
        event.getByLabel(pileupWeightsLabel, pileupWeightsH)
        pileupProduct = pileupWeightsH.product()
        pileupWeight[0] = pileupProduct[0]
        pileupWeightUp[0] = pileupProduct[1]
        pileupWeightDown[0] = pileupProduct[2]
    else:
        runNumber[0] = event.object().id().run()
        lumiNumber[0] = event.object().id().luminosityBlock() 
        eventNumber[0] = event.object().id().event()
        
  
    # Get the "product" of the handle (i.e. what it's "pointing to" in C++)
    vertices = vertH.product()
    jets = jetsH.product()
    leptons = leptonsH.product()
    metObj = (metH.product())[0]
    trigObj = trigH.product()
    
    if len(leptons) == 0:
        continue
    if len(jets) == 0:
        continue

    #JES and JER
    for ijet in jets :
        jetScale = 1.0
        if not options.data and abs(jecScale) > 0.0001 :
            jecUnc.setJetEta( ijet.eta() )
            jecUnc.setJetPt( ijet.pt() )
            upOrDown = bool(jecScale > 0.0)

            unc1 = abs(jecUnc.getUncertainty(upOrDown))
            unc2 = flatJecUnc
            unc = math.sqrt(unc1*unc1 + unc2*unc2)
            #print 'Correction = ' + str( 1 + unc * jecScale)
            jetScale = 1 + unc * jecScale

##          ## also do Jet energy resolution variation 
##         if not options.data and abs(options.jetSmear)>0.0001 and ijet.genJet() != 0 and ijet.genJet().pt()>15.0:
##             scale = options.jetSmear
##             recopt = ijet.pt()
##             genpt = ijet.genJet().pt()
##             deltapt = (recopt-genpt)*scale
##             ptscale = max(0.0, (recopt+deltapt)/recopt)
##             jetScale*=ptscale   
##             print 'Correction = ' + str(jecScale)


    # store the trigger paths
    trig_path[0]  = -1
    eleHad    = "HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralPFNoPUJet"
     
    trigPaths = trigObj.paths() #TriggerPathCollection
    for ipath in trigPaths:
        if eleHad+"30_v" in ipath.name() or eleHad+"30_30_20_v" in ipath.name():
            trig_path[0] =  trigObj.path(ipath.name()).wasAccept() and trigObj.path(ipath.name()).wasRun()
            #if trig_path[0]==1: print "your path ", ipath.name(), "was run and accepted"
            
    nvertices[0] =  vertices.size()     
    met[0] = metObj.pt()
    lepEt[0] = (leptons[0]).pt()
    lepEta[0] = (leptons[0]).eta()
    if not runMu:
        eSCEta[0] = (leptons[0]).superCluster().eta()
    
    chIso = (leptons[0]).userIsolation(pat.PfChargedHadronIso)
    nhIso = (leptons[0]).userIsolation(pat.PfNeutralHadronIso)
    gIso  = (leptons[0]).userIsolation(pat.PfGammaIso)
    lepIso[0] = (chIso + nhIso + gIso)/lepEt[0] 
    
    njets[0] = len(jets)
    sumEt = leptons[0].pt() + metObj.pt()
    sumEt35 = sumEt
    sumEt4jets = sumEt
    sumEt4jets35 = sumEt
    
    nj = 0
    ntagsTCHEM = 0
    ntagsSSVHEM = 0
    ntagsCSVM = 0
    for jet in jets :
        jetEt[nj] = jet.pt()
        if nj < 4 :
            sumEt4jets += jet.pt()
            
        nj = nj + 1
        sumEt += jet.pt()

        if options.data:
            if jet.bDiscriminator('combinedSecondaryVertexBJetTags') >= 0.679 :
                ntagsCSVM = ntagsCSVM + 1  
        else:
            if options.bTag == "OutOfBox" :
                if (jet.userInt('btagRegular') & 1) == 1 :
                    ntagsCSVM = ntagsCSVM + 1
            elif options.bTag == "" :
                if (jet.userInt('btagRegular') & 2) == 2 :
                    ntagsCSVM = ntagsCSVM + 1
            elif options.bTag =="BTagSFup" :
                if (jet.userInt('btagRegular') & 4) == 4 :
                    ntagsCSVM = ntagsCSVM + 1
            elif options.bTag =="BTagSFdown" :
                if (jet.userInt('btagRegular') & 8) == 8 :
                    ntagsCSVM = ntagsCSVM + 1
                            
    ht[0] = sumEt
    ht4jets[0] = sumEt4jets
    nTagsCSVM[0] = ntagsCSVM
        
    lepton_vector = TLorentzVector()
    lepton_vector.SetPtEtaPhiM( leptons[0].pt(), leptons[0].eta(), leptons[0].phi(), leptons[0].mass() )
    nu_p4 = metObj.p4()
    wPt = lepton_vector.Pt() + nu_p4.Pt()
    wPx = lepton_vector.Px() + nu_p4.Px()
    wPy = lepton_vector.Py() + nu_p4.Py()
    wMT = TMath.Sqrt(wPt*wPt-wPx*wPx-wPy*wPy)
    wMt[0] = wMT
    minDeltaR_elejet = 5.0
    minDR_je[0] = minDeltaR_elejet
    
    met_vector = TLorentzVector()
    met_vector.SetPxPyPzE( metObj.px(), metObj.py(), metObj.pz(), metObj.et())
    deltaPhiMETe[0] = lepton_vector.DeltaPhi( met_vector )
    leadingJetVector = TLorentzVector()
    leadingJetVector.SetPxPyPzE( jets[0].px(), jets[0].py(), jets[0].pz(), jets[0].energy())
    deltaPhiMETLeadingJet[0] = met_vector.DeltaPhi( leadingJetVector )
    
    # Now loop over the jets, and figure out how many tags are per event
    t.Fill()
# Done processing the events!
# Stop our timer
timer.Stop()

# Print out our timing information
rtime = timer.RealTime(); # Real time (or "wall time")
ctime = timer.CpuTime(); # CPU time
print("Analyzed events: {0:6d}").format(nEventsAnalyzed)
print("RealTime={0:6.2f} seconds, CpuTime={1:6.2f} seconds").format(rtime,ctime)
print("{0:4.2f} events / RealTime second .").format( nEventsAnalyzed/rtime)
print("{0:4.2f} events / CpuTime second .").format( nEventsAnalyzed/ctime)

# "cd" to our output file
f.cd()

# Write our tree
t.Write()

# Close it
f.Close()
