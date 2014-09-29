#! /usr/bin/env python
import os
import glob

import ROOT
ROOT.gROOT.Macro("rootlogon.C")


import sys
from DataFormats.FWLite import Events, Handle


fileDir = sys.argv[1]
#fileDir = "Jet_Run2011A-May10ReReco_ttbsm_v6_ttbsmTuples_v3"
#files = ["TopTagMistagRate_ttbsm_v6_ttbsmtuples_v1.root"]
#files = ["JetPD_range1_ttbsm_v6_ttbsmTuples_v4.root"]
files = glob.glob( fileDir + "/*.root" )
print files


events = Events (files)

topTagHandle   = Handle ("vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > >")
topTagLabel    = ( "ttbsmAna", "topTagP4" )

topTagNSubjetsHandle   = Handle( "std::vector<double>")
topTagNSubjetsLabel    = ( "ttbsmAna",  "topTagNSubjets" )

topTagMinMassHandle   = Handle( "std::vector<double>")
topTagMinMassLabel    = ( "ttbsmAna",  "topTagMinMass" )


wTagHandle     = Handle( "vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > >")
wTagLabel      = ( "ttbsmAna", "wTagP4" )

wTagMuHandle   = Handle( "std::vector<double>")
wTagMuLabel    = ( "ttbsmAna",  "wTagMu" )

rhoHandle   = Handle( "double")
rhoLabel    = ( "ttbsmAna",  "rho" )

myTrigIndexHandle   = Handle( "std::vector<int>")
myTrigIndexLabel    = ( "ttbsmAna",  "myTrigIndex" )

prescalesHandle   = Handle( "std::vector<int>")
prescalesLabel    = ( "ttbsmAna",  "prescales" )

trigNamesHandle   = Handle( "std::vector<string>")
trigNamesLabel    = ( "ttbsmAna",  "trigNames" )


f = ROOT.TFile("TTKinPlots_testing.root", "recreate")
#f = ROOT.TFile( fil".root", "recreate" )
f.cd()

print "Creating histograms"

maxJetsWTags = 4
maxJetsTopTags = 4

trigsRun = ROOT.TH1F('trigsRun', 'Trigs run', 20, 0, 20 )

nJetsCA8Pruned = ROOT.TH1F('nJetsCA8Pruned', 'C-A 0.8 Pruned;N_{Jets};Number', 10, 0, 10 )
ptJetsCA8Pruned= []
yJetsCA8Pruned = []
mJetsCA8Pruned = []
muJetsCA8Pruned= []

for ijet in range(0,maxJetsWTags+1):
    ptJetsCA8Pruned.append( ROOT.TH1F('ptJetsCA8Pruned' + str(ijet),'C-A 0.8 Pruned;Jet p_{T};Number', 100, 0., 1000.) )
    yJetsCA8Pruned .append( ROOT.TH1F('yJetsCA8Pruned' + str(ijet), 'C-A 0.8 Pruned;Jet Rapidity;Number', 100, -2.5, 2.5) )
    mJetsCA8Pruned .append( ROOT.TH1F('mJetsCA8Pruned' + str(ijet), 'C-A 0.8 Pruned;Jet Mass;Number', 100, 0, 500.) )
    muJetsCA8Pruned.append( ROOT.TH1F('muJetsCA8Pruned' + str(ijet),'C-A 0.8 Pruned;Mass Drop (#mu = m_{0}/m_{jet});Number', 100, 0, 1) )


nJetsCA8TopTag = ROOT.TH1F('nJetsCA8TopTag', 'C-A 0.8 TopTagged;N_{Jets};Number', 10, 0, 10 )
ptJetsCA8TopTag= []
yJetsCA8TopTag = []
mJetsCA8TopTag = []
minMassJetsCA8TopTag= []
nSubjetsJetsCA8TopTag= []

for ijet in range(0,maxJetsWTags+1):
    ptJetsCA8TopTag.append( ROOT.TH1F('ptJetsCA8TopTag' + str(ijet),'C-A 0.8 TopTagged;Jet p_{T};Number', 100, 0., 1000.) )
    yJetsCA8TopTag .append( ROOT.TH1F('yJetsCA8TopTag' + str(ijet), 'C-A 0.8 TopTagged;Jet Rapidity;Number', 100, -2.5, 2.5) )
    mJetsCA8TopTag .append( ROOT.TH1F('mJetsCA8TopTag' + str(ijet), 'C-A 0.8 TopTagged;Jet Mass;Number', 100, 0, 500.) )
    minMassJetsCA8TopTag.append( ROOT.TH1F('minMassJetsCA8TopTag' + str(ijet),'C-A 0.8 TopTagged;Min Mass;Number', 100, 0, 500.) )
    nSubjetsJetsCA8TopTag.append( ROOT.TH1F('nSubjetsJetsCA8TopTag' + str(ijet),'C-A 0.8 TopTagged;N_{Subjets};Number', 5, 0, 5) )

# loop over events
count = 0
ntotal = events.size()
print "Start looping"
for event in events:
    count = count + 1
    if count % 100000 == 0 :
        percentDone = float(count) / float(ntotal) * 100.0
        print 'Processing {0:10.0f}/{1:10.0f} : {2:5.2f} %'.format(
            count, ntotal, percentDone )

    if not event.object().isValid():
        continue

    event.getByLabel (myTrigIndexLabel, myTrigIndexHandle)
    if not myTrigIndexHandle.isValid():
        print 'myTrigIndex is invalid'
        continue
    myTrigIndices = myTrigIndexHandle.product()

    event.getByLabel (prescalesLabel, prescalesHandle)
    if not prescalesHandle.isValid():
        print 'prescales is invalid'
        continue
    prescales = prescalesHandle.product()

    event.getByLabel (trigNamesLabel, trigNamesHandle)
    if not trigNamesHandle.isValid():
        print 'trigNames is invalid'
        continue
    trigNames = trigNamesHandle.product()

    event.getByLabel (rhoLabel, rhoHandle)
    if not rhoHandle.isValid():
        continue
    rho = rhoHandle.product()[0]
    if abs(rho) > 100 or rho < 0.0 :
        print 'AAAACCCKK!!! rho = ' + str(rho)
        continue

    found = False
    firedTrig = -1
    for mytrig in [10, 9, 8, 7, 6, 3]:
        if mytrig in myTrigIndices :
            found = True
            firedTrig = mytrig
            break


    if not found :
        continue

    trigsRun.Fill( firedTrig )


    event.getByLabel (wTagLabel, wTagHandle)
    wJets = wTagHandle.product()

    event.getByLabel (wTagMuLabel, wTagMuHandle)
    wJetsMu = wTagMuHandle.product()


    nWJets = 0
    for ijet in range(0,len(wJets)) :
        jet = wJets[ijet]
        if jet.pt() > 30 :
            nWJets += 1
            if ijet <= maxJetsWTags :
                ptJetsCA8Pruned[ijet].Fill( jet.pt() )
                yJetsCA8Pruned[ijet].Fill( jet.Rapidity() )
                mJetsCA8Pruned[ijet].Fill( jet.mass() )
                muJetsCA8Pruned[ijet].Fill( wJetsMu[ijet] )

    nJetsCA8Pruned.Fill( nWJets )


    event.getByLabel (topTagLabel, topTagHandle)
    topJets = topTagHandle.product()

    
    event.getByLabel (topTagNSubjetsLabel, topTagNSubjetsHandle)
    topTagNSubjets =topTagNSubjetsHandle.product()

    event.getByLabel (topTagMinMassLabel, topTagMinMassHandle)
    topTagMinMass =topTagMinMassHandle.product()

    nTopJets = 0
    for ijet in range(0,len(topJets)) :
        jet = topJets[ijet]
        if jet.pt() > 350 :
            nTopJets += 1
            if ijet <= maxJetsTopTags :
                ptJetsCA8TopTag[ijet].Fill( jet.pt() )
                yJetsCA8TopTag[ijet].Fill( jet.Rapidity() )
                mJetsCA8TopTag[ijet].Fill( jet.mass() )
                minMassJetsCA8TopTag[ijet].Fill( topTagMinMass[ijet] )
                nSubjetsJetsCA8TopTag[ijet].Fill( topTagNSubjets[ijet] )

    nJetsCA8TopTag.Fill( nTopJets )



f.cd()
f.Write()
f.Close()
