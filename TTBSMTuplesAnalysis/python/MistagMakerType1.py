import ROOT
import copy

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

from DataFormats.FWLite import Events, Handle
from Analysis.TTBSMTuplesAnalysis import *

class MistagMakerType1 :
    """Run 1 + 1 Mistag Rate"""
    def __init__(self, outfile):
        self.outfile = outfile
        
        self.allTopTagHandle = Handle (  "vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > >"  )
        self.allTopTagLabel  = ( "ttbsmAna",   "topTagP4")

        self.allTopTagTopMassHandle  = Handle( "std::vector<double>" )
        self.allTopTagTopMassLabel   = ( "ttbsmAna",   "topTagTopMass" )
        self.allTopTagMinMassHandle  = Handle( "std::vector<double>" )
        self.allTopTagMinMassLabel   = ( "ttbsmAna",   "topTagMinMass" )
        self.allTopTagNSubjetsHandle = Handle("std::vector<double>" )
        self.allTopTagNSubjetsLabel  = ( "ttbsmAna",   "topTagNSubjets" )

        self.allTopTagPassHandle  = Handle( "std::vector<int>" )
        self.allTopTagPassLabel   = ( "ttbsmAna",   "topTagPass" )
        
        self.__book__()



    def __del__ (self):
        """(Internal) Destructor"""
        print 'Goodbye from MistagMakerType1. Before I go, I will delete some stuff'
        self.f.cd()
        print '1'
        self.f.Write()
        self.f.Close()
        print '4'
        print '5'

        print 'So long!'

    def __book__( self ) :
        """(Internal) Books histograms"""

        print 'Booking histograms'
        self.f = ROOT.TFile( self.outfile + ".root", "recreate" )
        self.f.cd()

        self.topTagPt             = ROOT.TH1D("topTagPt",             "Top Tag Pt",               400,  0,  2000 )
        self.topProbePt           = ROOT.TH1D("topProbePt",           "Top Probe Pt",             400,  0,  2000 )
        self.testTagPt            = ROOT.TH1D("testTagPt",            "Top Tag Pt",               400,  0,  2000 )
        self.testProbePt          = ROOT.TH1D("testProbePt",          "Top Probe Pt",             400,  0,  2000 )
        

    def analyze(self, event) :
        """Analyzes event"""
        
        event.getByLabel (self.allTopTagLabel, self.allTopTagHandle)
        topJets = self.allTopTagHandle.product()

        nTopCand = 0
        for i in range(0,len(topJets) ) :
          if( topJets[i].pt() > 350 ) :
            nTopCand = nTopCand + 1

        if nTopCand < 2 :
            return

        event.getByLabel (self.allTopTagMinMassLabel, self.allTopTagMinMassHandle)
        topJetMinMass= self.allTopTagMinMassHandle.product()
        event.getByLabel (self.allTopTagNSubjetsLabel, self.allTopTagNSubjetsHandle)
        topJetNSubjets= self.allTopTagNSubjetsHandle.product()
        event.getByLabel (self.allTopTagTopMassLabel, self.allTopTagTopMassHandle)
        topJetMass= self.allTopTagTopMassHandle.product()
        event.getByLabel (self.allTopTagPassLabel, self.allTopTagPassHandle )
        topJetPass= self.allTopTagPassHandle.product()

        deltaPhi = topJets[0].phi() - topJets[1].phi()
        if deltaPhi > ROOT.TMath.Pi():
            deltaPhi = deltaPhi - 2*ROOT.TMath.Pi()
        if deltaPhi < -ROOT.TMath.Pi():
            deltaPhi = deltaPhi + 2*ROOT.TMath.Pi()

        ptCuts = topJets[0].pt() > 350 and topJets[1].pt() > 350
        etaCuts = abs(topJets[0].eta()) < 2.4 and abs(topJets[1].eta()) < 2.4
        deltaPhiCut = abs(deltaPhi)>2.1
        passType11KinCuts   = ptCuts and etaCuts and deltaPhiCut
    
        topTag0        = topJetMass[0] > 140 and topJetMass[0] < 250 and topJetMinMass[0] > 50 and topJetNSubjets[0] > 2
        topTag1        = topJetMass[1] > 140 and topJetMass[1] < 250 and topJetMinMass[1] > 50 and topJetNSubjets[1] > 2
        failMinMass0   = topJetMass[0] > 140 and topJetMass[0] < 250 and topJetMinMass[0] < 50  
        failMinMass1   = topJetMass[1] > 140 and topJetMass[1] < 250 and topJetMinMass[1] < 50
 
        if passType11KinCuts :
            x = ROOT.gRandom.Uniform(59298)        
            if x < 0.5 :
                if not topTag0 :
                    self.topProbePt.Fill( topJets[1].pt() )    
                    if topTag1 :
                        self.topTagPt.Fill( topJets[1].pt() )
                if failMinMass0 :
                    self.testProbePt.Fill( topJets[1].pt() )
                    if topTag1 :
                        self.testTagPt.Fill( topJets[1].pt() )
            if x >= 0.5 :
                if not topTag1 :
                    self.topProbePt.Fill( topJets[0].pt() )
                    if topTag0 :
                        self.topTagPt.Fill( topJets[0].pt() )
                if failMinMass1 :
                    self.testProbePt.Fill( topJets[0].pt() )
                    if topTag0 :
                        self.testTagPt.Fill( topJets[0].pt() )
