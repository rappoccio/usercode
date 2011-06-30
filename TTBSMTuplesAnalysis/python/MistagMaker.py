import ROOT
import copy

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

from DataFormats.FWLite import Events, Handle
from Analysis.TTBSMTuplesAnalysis import *

class MistagMaker :
    """Makes mistag rates"""
    def __init__(self, outfile):
        """Initialization"""
        self.outfileStr = outfile
        self.allTopTagHandle         = Handle (  "vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > >"  )
        self.allTopTagLabel          = ( "ttbsmAna",   "topTagP4")
        self.allTopTagMinMassHandle  = Handle( "std::vector<double>" )
        self.allTopTagMinMassLabel   = ( "ttbsmAna",   "topTagMinMass" )
        self.allTopTagNSubsHandle    = Handle("std::vector<double>" )
        self.allTopTagNSubsLabel     = ( "ttbsmAna",   "topTagNSubjets" )
        self.hemis0Handle            = Handle ("vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > >")
        self.hemis0Label             = ( "ttbsmAna", "topTagP4Hemis0" )
        self.hemis0MinMassHandle     = Handle( "std::vector<double>" )
        self.hemis0MinMassLabel      = ( "ttbsmAna", "topTagMinMassHemis0" )
        self.hemis0NSubjetsHandle    = Handle( "std::vector<double>" )
        self.hemis0NSubjetsLabel     = ( "ttbsmAna", "topTagNSubjetsHemis0"  )
        self.hemis0TopMassHandle     = Handle( "std::vector<double>" )
        self.hemis0TopMassLabel      = ( "ttbsmAna", "topTagTopMassHemis0" )
        self.hemis0PassHandle        = Handle( "std::vector<int>")
        self.hemis0PassLabel         = ( "ttbsmAna", "topTagPassHemis0" )
        self.hemis1Handle            = Handle( "vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > >")
        self.hemis1Label             = ( "ttbsmAna", "wTagP4Hemis1" )
        self.hemis1BdiscHandle       = Handle( "std::vector<double>" )
        self.hemis1BdiscLabel        = ( "ttbsmAna",   "wTagBDiscHemis1" )
        self.hemis1MuHandle          = Handle( "std::vector<double>")
        self.hemis1MuLabel           = ( "ttbsmAna",  "wTagMuHemis1" )
        self.hemis1Jet3Handle        = Handle("int")
        self.hemis1Jet3Label         = ( "ttbsmAna", "jet3Hemis1" )

        self.__book__()

    def __del__(self) :
        """(private) destructor"""
        self.f.cd()
        self.f.Write()
        self.f.Close()


    def __book__(self):
        """(private) creates histograms"""
        self.f = ROOT.TFile(self.outfileStr + '.root', "RECREATE")
        self.topJetCandPtSignal          = ROOT.TH1D("topJetCandPtSignal",          "Top Jet Cand Pt",          200,  0,  1000 )
        self.topJetCandPtSideBand        = ROOT.TH1D("topJetCandPtSideBand",        "Top Jet Cand Pt",          200,  0,  1000 )
        self.topJetCandPtAll             = ROOT.TH1D("topJetCandPtAll",             "Top Jet Cand Pt",          200,  0,  1000 )
        self.topJetCandMassSignal        = ROOT.TH1D("topJetCandMassSignal",        "Top Jet Cand Mass",        100,  0,  500 )
        self.topJetCandMassSideBand      = ROOT.TH1D("topJetCandMassSideBand",      "Top Jet Cand Mass",        100,  0,  500 )
        self.topJetCandMassAll           = ROOT.TH1D("topJetCandMassAll",            "Top Jet Cand Mass",        100,  0,  500 )
        self.topJetNsubsSignal           = ROOT.TH1D("topJetNsubsSignal",           "Top Jet Cand N Subjets",   10,   -0.5, 9.5 )
        self.topJetNsubsSideBand         = ROOT.TH1D("topJetNsubsSideBand",         "Top Jet Cand N Subjets",   10,   -0.5, 9.5 )
        self.topJetNsubsAll              = ROOT.TH1D("topJetNsubsAll",               "Top Jet Cand N Subjets",   10,   -0.5, 9.5 )
        self.topJetMinMassSignal         = ROOT.TH1D("topJetMinMassSignal",         "Top Jet Min Mass",         100,  0,  500 )
        self.topJetMinMassSideBand       = ROOT.TH1D("topJetMinMassSideBand",       "Top Jet Min Mass",         100,  0,  500 )
        self.topJetMinMassAll            = ROOT.TH1D("topJetMinMassAll",             "Top Jet Min Mass",         100,  0,  500 )
        self.type2TopProbe               = ROOT.TH1D("type2TopProbe",              "Top Probe Pt",               400,  0,  2000 )
        self.type2TopTag                 = ROOT.TH1D("type2TopTag",                "Top Tag Pt",                 400,  0,  2000 )
        self.type2TopTagMass             = ROOT.TH1D("type2TopTagMass",            "Top Tag Mass",               400,  0,  2000 )
        self.type2TopTagExp              = ROOT.TH1D("type2TopTagExp",             "Top Tag Pt Expected",        400,  0,  2000 )
        self.type2TopTagExp.Sumw2()
        self.type2TopTagExp800GeV        = ROOT.TH1D("type2TopTagExp800GeV",       "Top Tag Pt Expected",        400,  0,  2000 )
        self.type2TopTagExp800GeV.Sumw2()
        self.type2TopTag800GeV           = ROOT.TH1D("type2TopTag800GeV",          "Top Tag Pt",                 400,  0,  2000 )
        self.type2TopProbe800GeV         = ROOT.TH1D("type2TopProbe800GeV",        "Top Probe Pt",               400,  0,  2000 )
        self.type2KinTopProbe            = ROOT.TH1D("type2KinTopProbe",           "Top Probe Pt",               400,  0,  2000 )
        self.type2KinTopTag              = ROOT.TH1D("type2KinTopTag",             "Top Tag Pt",                 400,  0,  2000 )
        self.type2SideBandProbe          = ROOT.TH1D("type2SideBandProbe",         "Top Probe Pt",               400,  0,  2000 )
        self.type2SideBandTag            = ROOT.TH1D("type2SideBandTag",           "Top Tag Pt",                 400,  0,  2000 )
        self.randomTopProbe              = ROOT.TH1D("randomTopProbe",             "Top Probe Pt",               400,  0,  2000 )
        self.randomTopTag                = ROOT.TH1D("randomTopTag",               "Top Tag Pt",                 400,  0,  2000 )


    def analyze(self, event):
        """Runs the analyzer"""
        event.getByLabel (self.hemis0Label, self.hemis0Handle)
        topJets = self.hemis0Handle.product()


        nTopCand = 0
        for i in range(0,len(topJets) ) :
          if( topJets[i].pt() > 350 ) :
            nTopCand = nTopCand + 1

        if nTopCand < 1 :
            return


        event.getByLabel (self.hemis1Label, self.hemis1Handle)
        wJets = self.hemis1Handle.product()

        pairMass = 0.0
        ttMass = 0.0

        if nTopCand < 1 or len(wJets) < 2 :
          return


        event.getByLabel (self.hemis0MinMassLabel, self.hemis0MinMassHandle)
        topJetMinMass = self.hemis0MinMassHandle.product()
        event.getByLabel (self.hemis0NSubjetsLabel, self.hemis0NSubjetsHandle)
        topJetNSubjets = self.hemis0NSubjetsHandle.product()
        event.getByLabel (self.hemis0TopMassLabel, self.hemis0TopMassHandle)
        topJetMass = self.hemis0TopMassHandle.product()
        event.getByLabel (self.hemis1BdiscLabel, self.hemis1BdiscHandle)
        wJetBDisc = self.hemis1BdiscHandle.product()
        event.getByLabel (self.hemis0PassLabel, self.hemis0PassHandle )
        topJetPass = self.hemis0PassHandle.product()
        event.getByLabel (self.hemis1MuLabel, self.hemis1MuHandle)
        wJetMu = self.hemis1MuHandle.product()
        event.getByLabel (self.hemis1Jet3Label, self.hemis1Jet3Handle )
        jet3 = (self.hemis1Jet3Handle.product())[0]


        if jet3 < 1 :
          print "This is not expected, debug!"

        pairMass = (wJets[jet3]+wJets[0]).mass()
        ttMass = (wJets[jet3]+wJets[0]+topJets[0]).mass()
        jet1P4_massDown = copy.copy(topJets[0])
        jet1P4_massDown.SetM( max(jet1P4_massDown.mass()-100, 0.0) )
        #print topJets[0].px(), topJets[0].py(), topJets[0].pz(), topJets[0].mass() 
        #print jet1P4_massDown.px(), jet1P4_massDown.py(), jet1P4_massDown.pz(), jet1P4_massDown.mass()
        ttMassJet1MassDown = (wJets[jet3]+wJets[0]+jet1P4_massDown).mass()

        jet1P4_massUp = copy.copy(topJets[0])
        jet1P4_massUp.SetM( jet1P4_massUp.mass()+100 )
        ttMassJet1MassUp = (wJets[jet3]+wJets[0]+jet1P4_massUp).mass()
        #print jet1P4_massUp.px(), jet1P4_massUp.py(), jet1P4_massUp.pz(), jet1P4_massUp.mass()


        passKinCuts = (nTopCand == 1) and (wJets[0].pt() > 200)  and (wJetMu[0] < 0.4) and (wJets[jet3].pt() > 30 )
        hasBTag1    = wJetBDisc[jet3] > 3.3
        hasType2Top = wJets[0].mass() > 60 and wJets[0].mass() < 130 and pairMass > 140 and pairMass < 250
        hasTopTag   = topJetMass[0] > 140 and topJetMass[0] < 250 and topJetMinMass[0] > 50 and topJetNSubjets[0] > 2
        SBAndSR     = wJets[0].mass() > 40 and wJets[0].mass() < 150 and pairMass > 100 and pairMass < 300
        SBAndSR2    = wJets[0].mass() > 20 and wJets[0].mass() < 170 and pairMass > 60  and pairMass < 350
        passWiderTopMassCut   =   topJetMass[0] > 100 and topJetMass[0] < 300
        passTopMass           =   topJetMass[0] > 140 and topJetMass[0] < 250
        passNSubjetsCut       =   topJetNSubjets[0] > 2
        passMinMassCut        =   topJetMinMass[0] > 50
        topMassSideBand       =   (topJetMass[0] > 100 and topJetMass[0] < 140) or (topJetMass[0] > 250 and topJetMass[0] < 300)

        if passKinCuts  :

          self.topJetCandPtAll.Fill( topJets[0].pt() )
          self.topJetCandMassAll.Fill( topJets[0].mass() )
          self.topJetNsubsAll.Fill( topJetNSubjets[0] )
          self.topJetMinMassAll.Fill( topJetMinMass[0] )
          self.type2KinTopProbe.Fill( topJets[0].pt() )
          if hasTopTag  :   self.type2KinTopTag.Fill(  topJets[0].pt() )
          if not SBAndSR  :
            self.type2SideBandProbe.Fill( topJets[0].pt() )
            if hasTopTag  :   self.type2SideBandTag.Fill( topJets[0].pt() )

          if hasType2Top  :
            self.topJetCandPtSignal.Fill( topJets[0].pt() )
            self.topJetCandMassSignal.Fill( topJets[0].mass() )
            self.topJetNsubsSignal.Fill( topJetNSubjets[0] )
            self.topJetMinMassSignal.Fill( topJetMinMass[0] )

            #Make Top mistag measurement
            self.type2TopProbe.Fill( topJets[0].pt() )
            if hasTopTag :  
              self.type2TopTag.Fill( topJets[0].pt() )
              self.type2TopTagMass.Fill( topJets[0].mass() )


          if SBAndSR and (not hasType2Top) :
            self.topJetCandPtSideBand.Fill( topJets[0].pt() )
            self.topJetCandMassSideBand.Fill( topJets[0].mass() )
            self.topJetNsubsSideBand.Fill( topJetNSubjets[0] )
            self.topJetMinMassSideBand.Fill( topJetMinMass[0] )
