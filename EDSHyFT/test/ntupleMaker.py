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
                  default = "edmTest.root",
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

parser.add_option('--jetPtSmear', metavar='F', type='float', action='store',
                  default=0.1,
                  dest='jetPtSmear',
                  help='JER smearing. Standard values are 0.1 (nominal), 0.0 (down), 0.2 (up)')

parser.add_option('--jetEtaSmear', metavar='F', type='float', action='store',
                  default=0.1,
                  dest='jetEtaSmear',
                  help='Jet Phi smearing. Standard values are 0.1 (nominal), 0.0 (down), 0.2 (up)')

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

parser.add_option("--useC8APrune", action='store_true',
                  default=True,
                  dest="useC8APrune",
                  help="switch on(1) / off(0) C8APrune jets")

# Parse and get arguments
(options, args) = parser.parse_args()

runMu = options.runMuons
c8aPruneJets = options.useC8APrune

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

c8aPruneJetsH = Handle ("std::vector<pat::Jet>")
c8aPruneJetsLabel = ("pfTupleC8APruned", "jets")

metH = Handle ("std::vector<pat::MET>")
metLabel = ("pfTupleEle", "MET")

c8aPruneMetH = Handle ("std::vector<pat::MET>")
c8aPruneMetLabel = ("pfTupleC8APruned", "MET")

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
    
    event.getByLabel(c8aPruneJetsLabel,  c8aPruneJetsH)
    event.getByLabel(c8aPruneMetLabel,  c8aPruneMetH)
    
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
    
    if c8aPruneJets:
        jets = c8aPruneJetsH.product()
        metObj = (c8aPruneMetH.product())[0]
    else:
        jets = jetsH.product()
        metObj = (metH.product())[0]
        
    leptons = leptonsH.product()
    trigObj = trigH.product()
    
    if len(leptons) == 0:
        continue
    if len(jets) == 0:
        continue
    
    #Systematic variations studies:
    #=============================
    
    # get the P4 of the edm MET
    metP4 = metObj.p4()
    
    #L1, L2, L3 JEC are already applied to jets in EDM Ntuples
    for ijet in jets :
        
        ## get the uncorrected jets 
        uncorrJet = ijet.correctedP4(0)

        ## get p4 of L1,L2,L3 corrected jets
        #jetP4 = TLorentzVector()
        #jetP4.SetPtEtaPhi( ijet.pt(), ijet.eta(), ijet.phi(), ijet.mass() )
        jetP4     = ijet.p4()
        
        #genJets
        genJetPt  = ijet.userFloat('genJetPt')
        genJetPhi = ijet.userFloat('genJetPhi')
        genJetEta = ijet.userFloat('genJetEta')
         
        #JES 
        jetScale = 1.0
        if not options.data and abs(jecScale) > 0.0001 :
            jecUnc.setJetEta( ijet.eta() )
            jecUnc.setJetPt( ijet.pt() )
            upOrDown = bool(jecScale > 0.0)
            unc1 = abs(jecUnc.getUncertainty(upOrDown))
            unc2 = flatJecUnc
            unc = math.sqrt(unc1*unc1 + unc2*unc2)
            jetScale = 1 + unc * jecScale

        ##Jet energy resolution smearing
        if not options.data and abs(options.jetPtSmear)>0.0001 and genJetPt>15.0:
            scale = options.jetPtSmear
            recopt = ijet.pt()
            genpt = genJetPt
            deltapt = (recopt-genpt)*scale
            ptscale = max(0.0, (recopt+deltapt)/recopt)
            jetScale*=ptscale

        ##Jet angular resolution smearing
        etaScale = 1.0
        phiScale = 1.0
        if not options.data and abs(options.jetEtaSmear)>0.0001 and genJetPt>15.0:
            scale = options.jetPtSmear
            recoeta = ijet.eta()
            recophi = ijet.phi()
            geneta = genJetEta
            genphi = genJetPhi
            deltaeta = (recoeta-geneta)*scale
            deltaphi = (recophi-genphi)*scale
            etascale = max(0.0, (recoeta+deltaeta)/recoeta)
            phiscale = max(0.0, (recophi+deltaphi)/recophi)
           
        #Reset the jet p4

        #------(FIX ME)----
           
        #jetP4.SetPt( ijet.pt() * jetScale )
        #jetP4.SetM ( ijet.m() * jetScale )
        #jetP4.SetEta( ijet.eta() * jetScale * etaScale )
        #jetP4.SetPhi( ijet.phi() * jetScale * phiScale )

        #For the time being, let's only smear in pt.
        ijet.setP4( ijet.p4() * jetScale )

        #remove the uncorrected jets
        metP4.SetPx(metP4.px() + uncorrJet.px())
        metP4.SetPy(metP4.py() + uncorrJet.py())

        #apply the SF and add back the jets and also correct the MET
        metP4.SetPx(metP4.px() - uncorrJet.px() * jetScale)
        metP4.SetPy(metP4.py() - uncorrJet.py() * jetScale)
      
        
        

    #Reset MET
    metObj.setP4(metP4)

    #########################
    
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
