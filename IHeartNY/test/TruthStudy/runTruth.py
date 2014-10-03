#! /usr/bin/env python
import os
import glob
import time
import math


# -------------------------------------------------------------------------------------
# define input options
# -------------------------------------------------------------------------------------

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--files', metavar='F', type='string', action='store',
                  dest='files',
                  help='Input files')

parser.add_option('--outname', metavar='F', type='string', action='store',
                  default='test_iheartNY',
                  dest='outname',
                  help='Name of output file')

parser.add_option('--mttGenMax', metavar='J', type='float', action='store',
                  default=None,
                  dest='mttGenMax',
                  help='Maximum generator-level m_ttbar [GeV] to stitch together the ttbar samples.')


(options, args) = parser.parse_args()
argv = []

import ROOT
ROOT.gROOT.Macro("rootlogon.C")



# -------------------------------------------------------------------------------------
# define helper classes that use ROOT
# -------------------------------------------------------------------------------------

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


# -------------------------------------------------------------------------------------
# input and output files
# -------------------------------------------------------------------------------------

print 'Getting these files : ' + options.files

files = glob.glob( options.files )
print files

f = ROOT.TFile(options.outname+".root", "recreate")
name = options.outname


# -------------------------------------------------------------------------------------
# define all the histograms
# -------------------------------------------------------------------------------------

print "Creating histograms"

f.cd()

### only relevant for m(ttbar)<700 GeV - histos without mttgen cut applied
h_ttbar_mass_all_incl   = ROOT.TH1F("ttbar_mass_all_incl",   ";Mass(t#bar{t}) [GeV]; Events / 10 GeV", 300, 0, 3000)
h_ttbar_mass_pt400_incl = ROOT.TH1F("ttbar_mass_pt400_incl", ";Mass(t#bar{t}) [GeV]; Events / 10 GeV", 300, 0, 3000)

### all semileptonic events
h_ttbar_mass_all_emutau   = ROOT.TH1F("ttbar_mass_all_emutau",   ";Mass(t#bar{t}) [GeV]; Events / 10 GeV", 300, 0, 3000)
h_ttbar_mass_pt400_emutau = ROOT.TH1F("ttbar_mass_pt400_emutau", ";Mass(t#bar{t}) [GeV]; Events / 10 GeV", 300, 0, 3000)

### semileptonic ttbar --> MUON+jets final state
h_ttbar_mass_all   = ROOT.TH1F("ttbar_mass_all",   ";Mass(t#bar{t}) [GeV]; Events / 10 GeV", 300, 0, 3000)
h_ttbar_mass_pt400 = ROOT.TH1F("ttbar_mass_pt400", ";Mass(t#bar{t}) [GeV]; Events / 10 GeV", 300, 0, 3000)
h_ttbar_pt_all     = ROOT.TH1F("ttbar_pt_all",   ";p_{T}(t#bar{t}) [GeV]; Events / 5 GeV", 300, 0, 1500)
h_ttbar_pt_pt400   = ROOT.TH1F("ttbar_pt_pt400", ";p_{T}(t#bar{t}) [GeV]; Events / 5 GeV", 300, 0, 1500)

h_hadtop_mass_all   = ROOT.TH1F("hadtop_mass_all",   ";Mass(hadronic top) [GeV]; Events / 1 GeV", 300, 0, 300)
h_hadtop_mass_pt400 = ROOT.TH1F("hadtop_mass_pt400", ";Mass(hadronic top) [GeV]; Events / 1 GeV", 300, 0, 300)
h_hadtop_pt_all     = ROOT.TH1F("hadtop_pt_all",   ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0, 1500)
h_hadtop_pt_pt400   = ROOT.TH1F("hadtop_pt_pt400", ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0, 1500)

h_leptop_mass_all   = ROOT.TH1F("leptop_mass_all",   ";Mass(leptonic top) [GeV]; Events / 1 GeV", 300, 0, 300)
h_leptop_mass_pt400 = ROOT.TH1F("leptop_mass_pt400", ";Mass(leptonic top) [GeV]; Events / 1 GeV", 300, 0, 300)
h_leptop_pt_all     = ROOT.TH1F("leptop_pt_all",   ";p_{T}(leptonic top) [GeV]; Events / 5 GeV", 300, 0, 1500)
h_leptop_pt_pt400   = ROOT.TH1F("leptop_pt_pt400", ";p_{T}(leptonic top) [GeV]; Events / 5 GeV", 300, 0, 1500)

h_mu_eta_all   = ROOT.TH1F("mu_eta_all",   ";Muon #eta; Events / 0.025", 240, -3, 3)
h_mu_eta_pt400 = ROOT.TH1F("mu_eta_pt400", ";Muon #eta; Events / 0.025", 240, -3, 3)
h_mu_pt_all    = ROOT.TH1F("mu_pt_all",    ";Muon p_{T} [GeV]; Events / 1 GeV", 300, 0, 300)
h_mu_pt_pt400  = ROOT.TH1F("mu_pt_pt400",  ";Muon p_{T} [GeV]; Events / 1 GeV", 300, 0, 300)



# -------------------------------------------------------------------------------------
# define all variables to be read from input files
# -------------------------------------------------------------------------------------

events = Events (files)

topPtHandle    = Handle("std::vector<float>")
topPtLabel     = ("pfShyftTupleTopQuarks", "pt")
topEtaHandle   = Handle("std::vector<float>")
topEtaLabel    = ("pfShyftTupleTopQuarks", "eta")
topPhiHandle   = Handle("std::vector<float>")
topPhiLabel    = ("pfShyftTupleTopQuarks", "phi")
topMassHandle  = Handle("std::vector<float>")
topMassLabel   = ("pfShyftTupleTopQuarks", "mass")
topPdgIdHandle = Handle("std::vector<float>")
topPdgIdLabel  = ("pfShyftTupleTopQuarks", "pdgId")




# -------------------------------------------------------------------------------------
# start looping over events
# -------------------------------------------------------------------------------------

ntotal = 0

print "Start looping over events!"

for event in events :
        
    if ntotal % 10000 == 0:
      print  '--------- Processing Event ' + str(ntotal)
    ntotal += 1
    
    
    
    # -------------------------------------------------------------------------------------
    # read / store truth information
    # -------------------------------------------------------------------------------------

    topQuarks = []
    hadTop = None
    lepTop = None
    ttbar = None
    isSemiLeptonicGen = True
    isMuonFinalState = False

    event.getByLabel( topPtLabel, topPtHandle )
    event.getByLabel( topEtaLabel, topEtaHandle )
    event.getByLabel( topPhiLabel, topPhiHandle )
    event.getByLabel( topMassLabel, topMassHandle )
    event.getByLabel( topPdgIdLabel, topPdgIdHandle )

    topPt  = topPtHandle.product()
    topEta = topEtaHandle.product()
    topPhi = topPhiHandle.product()
    topMass   = topMassHandle.product()
    topPdgId  = topPdgIdHandle.product()
        
    p4Top = ROOT.TLorentzVector()
    p4Antitop = ROOT.TLorentzVector()
    topDecay = 0        # 0 = hadronic, 1 = leptonic
    antitopDecay = 0    # 0 = hadronic, 1 = leptonic

    muonEta = 0
    muonPt = 0
    
    # -------------------------------------------------------------------------------------
    # loop over gen particules
    for igen in xrange( len(topPt) ) :
        
        if topPdgId[igen] == 6 :
            gen = ROOT.TLorentzVector()
            gen.SetPtEtaPhiM( topPt[igen], topEta[igen], topPhi[igen], topMass[igen] )                    
            p4Top = gen
        elif topPdgId[igen] == -6 :
            gen = ROOT.TLorentzVector()
            gen.SetPtEtaPhiM( topPt[igen], topEta[igen], topPhi[igen], topMass[igen] )
            p4Antitop = gen
        # If there is an antilepton (e+, mu+, tau+) then the top is leptonic
        elif ( topPdgId[igen] == -11 or topPdgId[igen] == -13 or topPdgId[igen] == -15) :
            topDecay = 1
        # If there is an lepton (e-, mu-, tau-) then the antitop is leptonic
        elif ( topPdgId[igen] == 11 or topPdgId[igen] == 13 or topPdgId[igen] == 15) :                
            antitopDecay = 1

        # muon final state?
        if abs(topPdgId[igen]) == 13 :
            isMuonFinalState = True
            muonEta = topEta[igen]
            muonPt = topPt[igen]

        
    # -------------------------------------------------------------------------------------
    # end loop over gen particles
    # -------------------------------------------------------------------------------------

    topQuarks.append( GenTopQuark( 6, p4Top, topDecay) )
    topQuarks.append( GenTopQuark( -6, p4Antitop, antitopDecay) )
    
    if topDecay + antitopDecay == 1 :
        isSemiLeptonicGen = True
    else :
        isSemiLeptonicGen = False
        
        
    # consider semi-leptonic ttbar decays only !
    if isSemiLeptonicGen == False :
        continue	
    
    if topDecay == 0 :
        hadTop = topQuarks[0]
        lepTop = topQuarks[1]
    else :
        hadTop = topQuarks[1]
        lepTop = topQuarks[0]
        
    ttbar = hadTop.p4 + lepTop.p4
    
    
    # -------------------------------------------------------------------------------------
    # fill histograms!        
    # -------------------------------------------------------------------------------------

    ## histograms without mtt gen.level cut
    h_ttbar_mass_all_incl.Fill( ttbar.M() )

    if hadTop.p4.Perp() > 400. :
        h_ttbar_mass_pt400_incl.Fill( ttbar.M() )


    ## cut on generated m(ttbar) if stitching sample
    if options.mttGenMax is not None :
        if ttbar.M() > options.mttGenMax :
            continue


    ## histograms for e+mu+tau final states
    h_ttbar_mass_all_emutau.Fill( ttbar.M() )

    if hadTop.p4.Perp() > 400. :
        h_ttbar_mass_pt400_emutau.Fill( ttbar.M() )


    ## now require mu+jets final state only
    if isMuonFinalState is False:
        continue
    
    ## fill rest of histograms        
    h_ttbar_mass_all.Fill( ttbar.M() )
    h_ttbar_pt_all.Fill( ttbar.Perp() )
    h_hadtop_mass_all.Fill( hadTop.p4.M() )
    h_hadtop_pt_all.Fill( hadTop.p4.Perp() )
    h_leptop_mass_all.Fill( lepTop.p4.M() )
    h_leptop_pt_all.Fill( lepTop.p4.Perp() )
    h_mu_eta_all.Fill(muonEta)    
    h_mu_pt_all.Fill(muonPt)
    
    if hadTop.p4.Perp() > 400. :
        h_ttbar_mass_pt400.Fill( ttbar.M() )
        h_ttbar_pt_pt400.Fill( ttbar.Perp() )            
        h_hadtop_mass_pt400.Fill( hadTop.p4.M() )
        h_hadtop_pt_pt400.Fill( hadTop.p4.Perp() )
        h_leptop_mass_pt400.Fill( lepTop.p4.M() )
        h_leptop_pt_pt400.Fill( lepTop.p4.Perp() )
        h_mu_eta_pt400.Fill(muonEta)
        h_mu_pt_pt400.Fill(muonPt)
        
    
        
    # -------------------------------------------------------------------------------------
    # end truth loop
    # -------------------------------------------------------------------------------------

    
 
# -------------------------------------------------------------------------------------
# END OF LOOPING OVER EVENTS!!!
# -------------------------------------------------------------------------------------

f.cd()
f.Write()
f.Close()

print "Total time = " + str( time.time() - start_time) + " seconds"
