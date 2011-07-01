import ROOT
import copy

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

from DataFormats.FWLite import Events, Handle
from Analysis.TTBSMTuplesAnalysis import *

class Type11Analyzer :
    """Run 1 + 1 Analysis"""
    def __init__(self, useMC, outfile, mistagFile):
        self.outfile = outfile
        self.mistagFileStr = mistagFile
        self.useMC = useMC
        
        self.allTopTagHandle = Handle (  "vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > >"  )
        self.allTopTagLabel  = ( "ttbsmAna",   "topTagP4")
        self.allTopTagMinMassHandle  = Handle( "std::vector<double>" )
        self.allTopTagMinMassLabel   = ( "ttbsmAna",   "topTagMinMass" )
        self.allTopTagNSubsHandle    = Handle("std::vector<double>" )
        self.allTopTagNSubsLabel     = ( "ttbsmAna",   "topTagNSubjets" )

        self.hemis0Handle   = Handle ("vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > >")
        self.hemis0Label    = ( "ttbsmAna", "topTagP4Hemis0" )

        self.hemis0MinMassHandle     = Handle( "std::vector<double>" )
        self.hemis0MinMassLabel  = ( "ttbsmAna", "topTagMinMassHemis0" )

        self.hemis0NSubjetsHandle    = Handle( "std::vector<double>" )
        self.hemis0NSubjetsLabel = ( "ttbsmAna", "topTagNSubjetsHemis0"  )

        self.hemis0TopMassHandle     = Handle( "std::vector<double>" )
        self.hemis0TopMassLabel  = ( "ttbsmAna", "topTagTopMassHemis0" )

        self.hemis0PassHandle        = Handle( "std::vector<int>")
        self.hemis0PassLabel   = ( "ttbsmAna", "topTagPassHemis0" )

        self.hemis1Handle   = Handle ("vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > >")
        self.hemis1Label    = ( "ttbsmAna", "topTagP4Hemis1" )

        self.hemis1MinMassHandle     = Handle( "std::vector<double>" )
        self.hemis1MinMassLabel  = ( "ttbsmAna", "topTagMinMassHemis1" )

        self.hemis1NSubjetsHandle    = Handle( "std::vector<double>" )
        self.hemis1NSubjetsLabel = ( "ttbsmAna", "topTagNSubjetsHemis1"  )

        self.hemis1TopMassHandle     = Handle( "std::vector<double>" )
        self.hemis1TopMassLabel  = ( "ttbsmAna", "topTagTopMassHemis1" )

        self.hemis1PassHandle        = Handle( "std::vector<int>")
        self.hemis1PassLabel   = ( "ttbsmAna", "topTagPassHemis1" )



        self.__book__()



    def __del__ (self):
        """(Internal) Destructor"""
        print 'Goodbye from Type11Analyzer. Before I go, I will delete some stuff'
        self.f.cd()
        self.mttPredDist.GetPredictedHist().Write()
        self.mttPredDist.GetObservedHist().Write()
        self.mttPredDist.GetTaggableHist().Write()
        print '1'
        self.f.Write()
        self.f.Close()
        print '4'
        self.mistagFile.Close()
        print '5'

        print 'So long!'

    def __book__( self ) :
        """(Internal) Books histograms"""

        self.mistagFile = ROOT.TFile(self.mistagFileStr + ".root")
        self.mistagFile.cd()
        self.mistag = self.mistagFile.Get("TYPE12_KIN_MISTAG").Clone()
        self.mistag.SetName('mistag')
        ROOT.SetOwnership( self.mistag, False )
        
        self.f = ROOT.TFile( self.outfile + ".root", "recreate" )
        self.f.cd()

        self.mttPredDist                 = ROOT.PredictedDistribution( self.mistag, "mttPredDist", "mTT Mass",       1000, 0,  5000 )


        ROOT.SetOwnership( self.mttPredDist, False )
        
        self.jetEta               = ROOT.TH1F("jetEta",               "jetEta",            100, -4,    4)
        self.jetMass              = ROOT.TH1F("jetMass",              "jetMass",        100,  0,  500 )
        self.jetPt                = ROOT.TH1F("jetPt",                "jetPt",          400,  0,  2000 )    
        self.jetMinMass           = ROOT.TH1F("jetMinMass",           "jetMinMass",          400,  0,  200 )
        self.topTagMass           = ROOT.TH1F("topTagMass",           "Top Tag Mass",             100,  0,  500 )
        self.topTagMinMass        = ROOT.TH1F("topTagMinMass",               "Top Tag MinMass",             100,  0,  200 )
        self.topTagPt             = ROOT.TH1F("topTagPt",                    "Top Tag Pt",               400,  0,  2000 )
        self.mttCandMass          = ROOT.TH1F("mttCandMass",                     "mTT Cand Mass",                 1000, 0,  5000 )
        self.mttMass              = ROOT.TH1F("mttMass",                     "mTT Mass",                 1000, 0,  5000 )
    
        

    def analyze(self, event) :
        """Analyzes event"""
        event.getByLabel (self.hemis0Label, self.hemis0Handle)
        topJets0 = self.hemis0Handle.product()
        

        nTopCand0 = 0
        for i in range(0,len(topJets0) ) :
          if( topJets0[i].pt() > 350 ) :
            nTopCand0 = nTopCand0 + 1

        if nTopCand0 < 1 :
            return

        event.getByLabel (self.hemis1Label, self.hemis1Handle)
        topJets1 = self.hemis1Handle.product()
        
        nTopCand1 = 0
        for i in range(0,len(topJets1) ) :
            if( topJets1[i].pt() > 350 ) :
                nTopCand1 = nTopCand1 + 1

        if nTopCand1 < 1:
            return
        
        pairMass = 0.0
        ttMass = 0.0

        event.getByLabel (hemis0MinMassLabel, hemis0MinMassHandle)
        topJet0MinMass = hemis0MinMassHandle.product()
        event.getByLabel (hemis0NSubjetsLabel, hemis0NSubjetsHandle)
        topJet0NSubjets = hemis0NSubjetsHandle.product()
        event.getByLabel (hemis0TopMassLabel, hemis0TopMassHandle)
        topJet0Mass = hemis0TopMassHandle.product()
        event.getByLabel (hemis0PassLabel, hemis0PassHandle )
        topJet0Pass = hemis0PassHandle.product()
        event.getByLabel (hemis1Label, hemis1Handle)
        topJet1MinMass = hemis1MinMassHandle.product()
        event.getByLabel (hemis1NSubjetsLabel, hemis1NSubjetsHandle)
        topJet1NSubjets = hemis1NSubjetsHandle.product()
        event.getByLabel (hemis1TopMassLabel, hemis1TopMassHandle)
        topJet1Mass = hemis1TopMassHandle.product()
        event.getByLabel (hemis1PassLabel, hemis1PassHandle )
        topJet1Pass = hemis1PassHandle.product()

        ttMass = 0.0
        deltaPhi = topJets0[0].phi() - topJets1[0].phi()
        if deltaPhi > pi:
            deltaPhi = deltaPhi - 2*pi
        if deltaPhi < -pi:
            deltaPhi = deltaPhi + 2*pi

        ptCuts = topJets0[0].pt() > 350 and topJets1[0].pt() > 350
        etaCuts = fabs(topJets0[0].eta()) < 2.4 and fabs(topJets1[0].eta()) < 2.4
        deltaPhiCut = fabs(deltaPhi)>2.1
        passType11KinCuts   = ptCuts and etaCuts and deltaPhiCut
    
        topTag0        = topJet0Mass[0] > 140 and topJet0Mass[0] < 250 and topJet0MinMass[0] > 50 and topJet0NSubjets[0] > 2
        topTag1        = topJet1Mass[0] > 140 and topJet1Mass[0] < 250 and topJet1MinMass[0] > 50 and topJet1NSubjets[0] > 2
        passType11     = topTag0 and topTag1
        ttMass   = (topJets0[0]+topJets1[0]).mass()
   
        if passType11KinCuts :
            jetMass.Fill( topJets0[0].mass() )
            jetMass.Fill( topJets1[0].mass() )
            jetPt.Fill( topJets0[0].pt() )
            jetPt.Fill( topJets1[0].pt() )
            jetEta.Fill( topJets0[0].eta() )
            jetEta.Fill( topJets1[0].eta() )
            jetMinMass.Fill( topJet0MinMass[0] )
            jetMinMass.Fill( topJet1MinMass[0] )
            mttCandMass.Fill( ttMass )

            if passType11  :
                topTagMass.Fill( topJets0[0].mass() )
                topTagMass.Fill( topJets1[0].mass() )
                topTagPt.Fill( topJets0[0].mass() )
                topTagPt.Fill( topJets1[0].mass() )
                topTagMinMass.Fill( topJet0MinMass[0] )
                topTagMinMass.Fill( topJet1MinMass[0] )
                mttMass.Fill( ttMass )

            #background estiation
            x = ROOT.gRandom.Uniform()        
            if x < 0.5 :
                if topTag0 :
                    self.mttPredDist.        Accumulate( ttMass, topJets1[0].pt(), topTag1 )
            if x >= 0.5 :
                if topTag1 :
                    self.mttPredDist.        Accumulate( ttMass, topJets0[0].pt(), topTag0 )



