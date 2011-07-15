import ROOT
import copy

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

from DataFormats.FWLite import Events, Handle
from Analysis.TTBSMTuplesAnalysis import *

class Type12Analyzer :
    """Run 1 + 2 Analysis"""
    def __init__(self, useMC, outfile, mistagFile,collectionLabelSuffix, veto11, useGenWeight=False):
        self.outfile = outfile
        self.mistagFileStr = mistagFile
        self.useMC = useMC
        self.veto11 = veto11
        self.useGenWeight=useGenWeight
       
        label = 'ttbsmAna'+collectionLabelSuffix

        self.allTopTagHandle = Handle (  "vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > >"  )
        self.allTopTagLabel  = ( label,   "topTagP4")
        self.allTopTagMinMassHandle  = Handle( "std::vector<double>" )
        self.allTopTagMinMassLabel   = ( label,   "topTagMinMass" )
        self.allTopTagNSubjetsHandle    = Handle("std::vector<double>" )
        self.allTopTagNSubjetsLabel     = ( label,   "topTagNSubjets" )
        #self.allTopTagNSubsHandle    = Handle("std::vector<double>" )
       # self.allTopTagNSubsLabel     = ( label,   "topTagNSubjets" )
        self.allTopTagTopMassHandle  = Handle( "std::vector<double>" )
        self.allTopTagTopMassLabel   = ( label,   "topTagTopMass" )

        self.hemis0Handle   = Handle ("vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > >")
        self.hemis0Label    = ( label, "topTagP4Hemis0" )

        self.hemis0MinMassHandle     = Handle( "std::vector<double>" )
        self.hemis0MinMassLabel  = ( label, "topTagMinMassHemis0" )

        self.hemis0NSubjetsHandle    = Handle( "std::vector<double>" )
        self.hemis0NSubjetsLabel = ( label, "topTagNSubjetsHemis0"  )

        self.hemis0TopMassHandle     = Handle( "std::vector<double>" )
        self.hemis0TopMassLabel  = ( label, "topTagTopMassHemis0" )

        self.hemis0PassHandle        = Handle( "std::vector<int>")
        self.hemis0PassLabel   = ( label, "topTagPassHemis0" )

        self.hemis1Handle     = Handle( "vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > >")
        self.hemis1Label      = ( label, "wTagP4Hemis1" )

        self.hemis1BdiscHandle         = Handle( "std::vector<double>" )
        self.hemis1BdiscLabel    = ( label,   "wTagBDiscHemis1" )

        self.hemis1MuHandle           = Handle( "std::vector<double>")
        self.hemis1MuLabel      = ( label,  "wTagMuHemis1" )

        self.hemis1Jet3Handle    = Handle("int")
        self.hemis1Jet3Label     = ( label, "jet3Hemis1" )
        self.__book__()



    def __del__ (self):
        """(Internal) Destructor"""
        print 'Goodbye from Type12Analyzer. Before I go, I will delete some stuff'
        self.f.cd()
        self.mttPredDist.GetPredictedHist().Write()
        self.mttPredDist.GetObservedHist().Write()
        self.mttPredDist.GetTaggableHist().Write()
        print '1'

        self.mttPredDistModMass.GetPredictedHist().Write()
        self.mttPredDistModMass.GetObservedHist().Write()
        self.mttPredDistModMass.GetTaggableHist().Write()
        print '2'

        self.mttPredDistMod2Mass.GetPredictedHist().Write()
        self.mttPredDistMod2Mass.GetObservedHist().Write()
        self.mttPredDistMod2Mass.GetTaggableHist().Write()
    
        self.mttPredDistModMassFlat.GetPredictedHist().Write()
        self.mttPredDistModMassFlat.GetObservedHist().Write()
        self.mttPredDistModMassFlat.GetTaggableHist().Write()

        self.mttPredDistMod3MassFlat.GetPredictedHist().Write()
        self.mttPredDistMod3MassFlat.GetObservedHist().Write()
        self.mttPredDistMod3MassFlat.GetTaggableHist().Write()
    
        self.mttPredDistMod3MassFlatSubtract.GetPredictedHist().Write()
        self.mttPredDistMod3MassFlatSubtract.GetObservedHist().Write()
        self.mttPredDistMod3MassFlatSubtract.GetTaggableHist().Write()
        
   
 
        print '3'

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
        self.mistagSubtract = self.mistagFile.Get("TYPE12_KIN_MISTAG_SUBTRACT_TTBAR").Clone()
        self.mistagSubtract.SetName('mistagSubtract')
        ROOT.SetOwnership( self.mistag, False )
        
        self.f = ROOT.TFile( self.outfile + ".root", "recreate" )
        self.f.cd()

        self.mttPredDist                 = ROOT.PredictedDistribution( self.mistag, "mttPredDist", "mTT Mass",       1000, 0,  5000 )
        self.mttPredDistModMass          = ROOT.PredictedDistribution( self.mistag, "mttPredDistModMass","mTT Mass", 1000, 0,  5000 )
        self.mttPredDistMod2Mass         = ROOT.PredictedDistribution( self.mistag, "mttPredDistMod2Mass","mTT Mass",1000, 0,  5000 )
        self.mttPredDistModMassFlat      = ROOT.PredictedDistribution( self.mistag, "mttPredDistModMassFlat","mTT Mass",1000, 0,  5000 )
        self.mttPredDistMod3MassFlat     = ROOT.PredictedDistribution( self.mistag, "mttPredDistMod3MassFlat","mTT Mass",1000, 0,  5000 )
        self.mttPredDistMod3MassFlatSubtract = ROOT.PredictedDistribution( self.mistagSubtract, "mttPredDistMod3MassFlatSubtract","mTT Mass",1000, 0,  5000 )


        ROOT.SetOwnership( self.mttPredDist, False )
        ROOT.SetOwnership( self.mttPredDistModMass, False )
        ROOT.SetOwnership( self.mttPredDistMod2Mass, False )
        ROOT.SetOwnership( self.mttPredDistModMassFlat, False )
        ROOT.SetOwnership( self.mttPredDistMod3MassFlat, False )
        ROOT.SetOwnership( self.mttPredDistMod3MassFlatSubtract, False )
        
        self.nJets                       = ROOT.TH1F("nJets",         "Number of Jets",               20, -0.5, 19.5 )
        self.topJetCandEta               = ROOT.TH1F("topJetCandEta",     "Top Cand eta",                 50,   -3.0, 3.0 )
        self.wCandVsTopCandMass          = ROOT.TH2F("wCandVsTopCandMass",  "W Cand Vs Top Cand Mass",  50, 0,  250,  100,  0,  500 )
        self.wCandWithMassVsTopCandMass  = ROOT.TH2F("wCandWithMassVsTopCandMass",  "W Cand Vs Top Cand Mass",  50, 0,  250,  100,  0,  500 )
        self.wCandVsTopCandMassType12    = ROOT.TH2F("wCandVsTopCandMassType12",    "Top Cand Vs W Cand Mass",  50, 0,  250,  100,  0,  500 )
        self.wCandVsTopCandMassType12WithTopTag  = ROOT.TH2F("wCandVsTopCandMassType12WithTopTag",  "Top Cand Vs W Cand Mass", 50,  0,  250,  100,  0,  500 )
        self.wCandMassType12             = ROOT.TH1F("wCandMassType12",             "W Cand Mass",              50, 0,  250 )
        self.wCandMassType12AfterTopTag  = ROOT.TH1F("wCandMassType12AfterTopTag",  "W Cand Mass",              50, 0,  250 )
        self.wCandPtType12               = ROOT.TH1F("wCandPtType12",               "W Cand Pt",                200,  0,  1000 )
        self.wCandPtType12AfterTopTag    = ROOT.TH1F("wCandPtType12AfterTopTag",    "W Cand Pt",                200,  0,  1000 )
        self.nearJetPt                   = ROOT.TH1F("nearJetPt",                   "Near Jet Pt",              200,  0,  1000 )
        self.nearJetPtAfterTopTag        = ROOT.TH1F("nearJetPtAfterTopTag",        "Near Jet Pt",              200,  0,  1000 )
        self.nearJetbValue               = ROOT.TH1F("nearJetbValue",               "Near Jet b Discriminator", 100,  0,  20 )
        self.nearJetbValueAfterTopTag    = ROOT.TH1F("nearJetbValueAfterTopTag",    "Near Jet b Discriminator", 100,  0,  20 )
        self.thirdLeadJetbValue          = ROOT.TH1F("thirdLeadJetbValue",           "Third Lead Jet b Discriminator", 100,  0,  20 )
        self.thirdLeadJetPt              = ROOT.TH1F("thirdLeadJetPt",               "Third Lead Jet PT",        200,  0,  1000 )
        self.topJetCandPtSignal          = ROOT.TH1F("topJetCandPtSignal",          "Top Jet Cand Pt",          200,  0,  1000 )
        self.topJetCandPtSideBand        = ROOT.TH1F("topJetCandPtSideBand",        "Top Jet Cand Pt",          200,  0,  1000 )
        self.topJetCandPtAll             = ROOT.TH1F("topJetCandPtAll",             "Top Jet Cand Pt",          200,  0,  1000 )
        self.topJetCandMassSignal        = ROOT.TH1F("topJetCandMassSignal",        "Top Jet Cand Mass",        100,  0,  500 )
        self.topJetCandMassSideBand      = ROOT.TH1F("topJetCandMassSideBand",      "Top Jet Cand Mass",        100,  0,  500 )
        self.topJetCandMassAll           = ROOT.TH1F("topJetCandMassAll",            "Top Jet Cand Mass",        100,  0,  500 )
        self.topJetNsubsSignal           = ROOT.TH1F("topJetNsubsSignal",           "Top Jet Cand N Subjets",   10,   -0.5, 9.5 )
        self.topJetNsubsSideBand         = ROOT.TH1F("topJetNsubsSideBand",         "Top Jet Cand N Subjets",   10,   -0.5, 9.5 )
        self.topJetNsubsAll              = ROOT.TH1F("topJetNsubsAll",               "Top Jet Cand N Subjets",   10,   -0.5, 9.5 )
        self.topJetMinMassSignal         = ROOT.TH1F("topJetMinMassSignal",         "Top Jet Min Mass",         100,  0,  500 )
        self.topJetMinMassSideBand       = ROOT.TH1F("topJetMinMassSideBand",       "Top Jet Min Mass",         100,  0,  500 )
        self.topJetMinMassAll            = ROOT.TH1F("topJetMinMassAll",             "Top Jet Min Mass",         100,  0,  500 )
        self.pairMassType12              = ROOT.TH1F("pairMassType12",              "Pair Jet Mass",            200,  0,  1000 )
        self.pairMassType12AfterTopTag   = ROOT.TH1F("pairMassType12AfterTopTag",   "Pair Jet Mass",            200,  0,  1000 )
        self.pairMassType12AfterTopTagWithWMass  = ROOT.TH1F("pairMassType12AfterTopTagWithWMass",    "Pair Jet Mass",            200,  0,  1000 )
        self.topJetCandMass              = ROOT.TH1F("topJetCandMass",              "Top Jet Cand Mass",        100,  0,  500 )
        self.topJetCandPt                = ROOT.TH1F("topJetCandPt",                "Top Jet Cand Pt",          400,  0,  2000 )
        self.topTagMass                  = ROOT.TH1F("topTagMass",                  "Top Tag Mass",             100,  0,  500 )
        self.topTagPt                    = ROOT.TH1F("topTagPt",                    "Top Tag Pt",               400,  0,  2000 )
        self.mttMass                     = ROOT.TH1F("mttMass",                     "mTT Mass",                 1000, 0,  5000 )
        self.mttMassTriggerWeight        = ROOT.TH1F("mttMassTriggerWeight",        "mTT Mass",                 1000, 0,  5000 )
        self.mttMassVeto11               = ROOT.TH1F("mttMassVeto11",               "mTT Mass",                 1000, 0,  5000 )
        self.mttMassTriggerWeightVeto11  = ROOT.TH1F("mttMassTriggerWeightVeto11",  "mTT Mass",                 1000, 0,  5000 )
        self.mttMassJet1MassDown         = ROOT.TH1F("mttMassJet1MassDown",         "mTT Mass",                 1000, 0,  5000 )
        self.mttBkgWithMistag            = ROOT.TH1F("mttBkgWithMistag",            "mTT Mass",                 1000, 0,  5000 )
        self.mttBkgWithMistag.Sumw2()
        self.mttBkgWithMistagModMass     = ROOT.TH1F("mttBkgWithMistagModMass",     "mTT Mass",                 1000, 0,  5000 )
        self.mttBkgWithMistagModMass.Sumw2()
        self.mttBkgWithMistagMod2Mass    = ROOT.TH1F("mttBkgWithMistagMod2Mass",    "mTT Mass",                 1000, 0,  5000 )
        self.mttBkgWithMistagMod2Mass.Sumw2()
        self.mttBkgWithMistagUp          = ROOT.TH1F("mttBkgWithMistagUp",          "mTT Mass",                 1000, 0,  5000 )
        self.mttBkgWithMistagUp.Sumw2()
        self.mttBkgWithMistagDown        = ROOT.TH1F("mttBkgWithMistagDown",        "mTT Mass",                 1000, 0,  5000 )
        self.mttBkgWithMistagDown.Sumw2()

        self.mttMassWithBTag             = ROOT.TH1F("mttMassWithBTag",             "mTT Mass With BTag",       1000, 0,  5000 )
        self.jet3BTagPt                  = ROOT.TH1F("jet3BTagPt",                  "Jet 3 BTag",               200,   0,  1000 )
        self.mttBkgShape                 = ROOT.TH1F("mttBkgShape",                 "mTT Bkg Shape",            1000, 0,  5000 )
        self.mttBkgShapeMassUp           = ROOT.TH1F("mttBkgShapeMassUp",           "mTT Bkg Shape",            1000, 0,  5000 )
        self.mttBkgShapeMassDown         = ROOT.TH1F("mttBkgShapeMassDown",         "mTT Bkg Shape",            1000, 0,  5000 )
        self.mttBkgShapeWithMassCut      = ROOT.TH1F("mttBkgShapeWithMassCut",      "mTT Bkg Shape",            1000, 0,  5000 )
        self.mttBkgShapeWithSideBandMass = ROOT.TH1F("mttBkgShapeWithSideBandMass", "mTT Bkg Shape",            1000, 0,  5000 )
        self.mttBkgShapeWithSideBand1Mass = ROOT.TH1F("mttBkgShapeWithSideBand1Mass",  "mTT Bkg Shape",            1000, 0,  5000 )
        self.mttBkgShapeWithSideBand2Mass = ROOT.TH1F("mttBkgShapeWithSideBand2Mass",  "mTT Bkg Shape",            1000, 0,  5000 )
        self.mttBkgShapeWithSideBand3Mass = ROOT.TH1F("mttBkgShapeWithSideBand3Mass",  "mTT Bkg Shape",            1000, 0,  5000 )
        self.mttBkgShapeWithSideBand4Mass = ROOT.TH1F("mttBkgShapeWithSideBand4Mass",  "mTT Bkg Shape",            1000, 0,  5000 )
        self.mttBkgShapeWithSideBand5Mass = ROOT.TH1F("mttBkgShapeWithSideBand5Mass",  "mTT Bkg Shape",            1000, 0,  5000 )
        self.mttBkgShapeWithSideBand6Mass = ROOT.TH1F("mttBkgShapeWithSideBand6Mass",  "mTT Bkg Shape",            1000, 0,  5000 )
        self.mttBkgShapeWithSideBand7Mass = ROOT.TH1F("mttBkgShapeWithSideBand7Mass",  "mTT Bkg Shape",            1000, 0,  5000 )

        self.type2TopProbe               = ROOT.TH1F("type2TopProbe",              "Top Probe Pt",               400,  0,  2000 )
        self.type2TopTag                 = ROOT.TH1F("type2TopTag",                "Top Tag Pt",                 400,  0,  2000 )
        self.type2TopTagMass             = ROOT.TH1F("type2TopTagMass",            "Top Tag Mass",               400,  0,  2000 )
        self.type2TopTagExp              = ROOT.TH1F("type2TopTagExp",             "Top Tag Pt Expected",        400,  0,  2000 )
        self.type2TopTagExp.Sumw2()
        self.jet1MassTag                 = ROOT.TH1F("jet1MassTag",                "Jet 1 Mass",                 400,  0,  2000 )
        self.jet1MassMod                 = ROOT.TH1F("jet1MassMod",                "Jet 1 Mass",                 400,  0,  2000 )
        self.jet1MassExp                 = ROOT.TH1F("jet1MassExp",                "Jet 1 Mass",                 400,  0,  2000 )
        self.jet1MassExp.Sumw2()
        self.jet1EtaTag                  = ROOT.TH1F("jet1EtaTag",                 "Jet 1 Eta",                  50,   -2.5, 2.5 )
        self.jet1EtaExp                  = ROOT.TH1F("jet1EtaExp",                 "Jet 1 Eta",                  50,   -2.5, 2.5 )
        self.jet1EtaExp.Sumw2()

        self.jet2Pt                      = ROOT.TH1F("jet2Pt",                     "Jet 2 Pt",                   400,  0,  2000 )
        self.jet2PtExp                   = ROOT.TH1F("jet2PtExp",                  "Jet 2 Pt Exp",               400,  0,  2000 )
        self.jet2PtExp.Sumw2()
        self.jet2MassTag                 = ROOT.TH1F("jet2MassTag",                "Jet 2 Mass",                 400,  0,  2000 )
        self.jet2MassExp                 = ROOT.TH1F("jet2MassExp",                "Jet 2 Mass",                 400,  0,  2000 )
        self.jet2MassExp.Sumw2()
        self.jet2EtaTag                  = ROOT.TH1F("jet2EtaTag",                 "Jet 2 Eta",                  50,   -2.5, 2.5 )
        self.jet2EtaExp                  = ROOT.TH1F("jet2EtaExp",                 "Jet 2 Eta",                  50,   -2.5, 2.5 )
        self.jet2EtaExp.Sumw2()

        self.jet3Pt                      = ROOT.TH1F("jet3Pt",                     "Jet 3 Pt",                   400,  0,  2000 )
        self.jet3PtExp                   = ROOT.TH1F("jet3PtExp",                  "Jet 3 Pt Exp",               400,  0,  2000 )
        self.jet3PtExp.Sumw2()
        self.jet3MassTag                 = ROOT.TH1F("jet3MassTag",                "Jet 3 Mass",                 400,  0,  2000 )
        self.jet3MassExp                 = ROOT.TH1F("jet3MassExp",                "Jet 3 Mass",                 400,  0,  2000 )
        self.jet3MassExp.Sumw2()
        self.jet3EtaTag                  = ROOT.TH1F("jet3EtaTag",                 "Jet 3 Eta",                  50,   -2.5, 2.5 )
        self.jet3EtaExp                  = ROOT.TH1F("jet3EtaExp",                 "Jet 3 Eta",                  50,   -2.5, 2.5 )
        self.jet3EtaExp.Sumw2()



        self.type2TopTagWith1TeV         = ROOT.TH1F("type2TopTagWith1TeV",        "Top Tag Pt",                 400,  0,  2000 )
        self.type2TopTagExpWith1TeV      = ROOT.TH1F("type2TopTagExpWith1TeV",     "Top Tag Pt Expected",        400,  0,  2000 )
        self.type2TopTagExpWith1TeV.Sumw2()
        self.type2TopTagExp800GeV        = ROOT.TH1F("type2TopTagExp800GeV",       "Top Tag Pt Expected",        400,  0,  2000 )
        self.type2TopTagExp800GeV.Sumw2()
        self.type2TopTag800GeV           = ROOT.TH1F("type2TopTag800GeV",          "Top Tag Pt",                 400,  0,  2000 )
        self.type2TopProbe800GeV         = ROOT.TH1F("type2TopProbe800GeV",        "Top Probe Pt",               400,  0,  2000 )
        self.type2KinTopProbe            = ROOT.TH1F("type2KinTopProbe",           "Top Probe Pt",               400,  0,  2000 )
        self.type2KinTopTag              = ROOT.TH1F("type2KinTopTag",             "Top Tag Pt",                 400,  0,  2000 )
        self.type2SideBandProbe          = ROOT.TH1F("type2SideBandProbe",         "Top Probe Pt",               400,  0,  2000 )
        self.type2SideBandTag            = ROOT.TH1F("type2SideBandTag",           "Top Tag Pt",                 400,  0,  2000 )
        self.leadTopProbe                = ROOT.TH1F("leadTopProbe",               "Top Probe Pt",               400,  0,  2000 )
        self.leadTopTag                  = ROOT.TH1F("leadTopTag",                 "Top Tag Pt",                 400,  0,  2000 )
        self.secTopProbe                 = ROOT.TH1F("secTopProbe",                "Top Probe Pt",               400,  0,  2000 )
        self.secTopTag                   = ROOT.TH1F("secTopTag",                  "Top Tag Pt",                 400,  0,  2000 )
        self.randomTopProbe              = ROOT.TH1F("randomTopProbe",             "Top Probe Pt",               400,  0,  2000 )
        self.randomTopTag                = ROOT.TH1F("randomTopTag",               "Top Tag Pt",                 400,  0,  2000 )
        self.antitagProbe                = ROOT.TH1F("antitagProbe",               "Top Probe Pt",               400,  0,  2000 )
        self.antitagTag                  = ROOT.TH1F("antitagTag",                 "Top Tag Pt",                 400,  0,  2000 )

        self.signalTopTagEta             = ROOT.TH1F("signalTopTagEta",              "Top Tag Eta",              100,  -3, 3 )
        self.signalJet3TagEta            = ROOT.TH1F("signalJet3TagEta",             "Jet 3 Eta",                100,  -3, 3 )
        self.evtRho                      = ROOT.TH1F("evtRho",                       "Event Rho",                1001, -1.0, 1000 )

        self.NSubjets                    = ROOT.TH1F("NSubjets",                     "Number of Subjets",        10,   -0.5,   9.5 )
        self.minmass                     = ROOT.TH1F("minmass",                      "Min Mass",                 51,   -5.0,    250 )
        self.NSubjetsWithTopMass         = ROOT.TH1F("NSubjetsWithTopMass",          "Number of Subjets",        10,   -0.5,   9.5 )
        self.minmassWithTopMass          = ROOT.TH1F("minmassWithTopMass",           "Min Mass",                 51,   -5.0,    250 )

        self.NSubjetsVsMinMassAll        = ROOT.TH2F("NSubjetsVsMinMassAll",         "NSubjets Vs Min Mass",     10,   -0.5,   9.5,    51,   -5.0,    250 )
        self.NSubjetsVsMinMassSR         = ROOT.TH2F("NSubjetsVsMinMassSR",          "NSubjets Vs Min Mass",     10,   -0.5,   9.5,    51,   -5.0,    250 )

        self.nJetsSignal                 = ROOT.TH1F("nJetsSignal",                  "N Jets",                   20,   -0.5,   19.5 )
        self.cutflow                     = ROOT.TH1F("cutflow",                  "cutflow",                   10,   0,   10 )


        

    def analyze(self, event) :
        """Analyzes event"""
        event.getByLabel (self.hemis0Label, self.hemis0Handle)
        topJets = self.hemis0Handle.product()
        
        self.cutflow.Fill(0.5,1)

        nTopCand = 0
        for i in range(0,len(topJets) ) :
          if( topJets[i].pt() > 350 ) :
            nTopCand = nTopCand + 1

        if nTopCand < 1 :
            return

        self.cutflow.Fill(1.5,1)

        event.getByLabel (self.hemis1Label, self.hemis1Handle)
        wJets = self.hemis1Handle.product()

        if len(wJets) < 2 :
          return

        self.cutflow.Fill(2.5,1)

        pairMass = 0.0
        ttMass = 0.0

        
        event.getByLabel (self.hemis0MinMassLabel, self.hemis0MinMassHandle)
        topJetMinMass   = self.hemis0MinMassHandle.product()
        event.getByLabel (self.hemis0NSubjetsLabel, self.hemis0NSubjetsHandle)
        topJetNSubjets  = self.hemis0NSubjetsHandle.product()
        event.getByLabel (self.hemis0TopMassLabel, self.hemis0TopMassHandle)
        topJetMass      = self.hemis0TopMassHandle.product()
        event.getByLabel (self.hemis1BdiscLabel, self.hemis1BdiscHandle)
        wJetBDisc       = self.hemis1BdiscHandle.product()
        event.getByLabel (self.hemis0PassLabel, self.hemis0PassHandle )
        topJetPass      = self.hemis0PassHandle.product()
        event.getByLabel (self.hemis1MuLabel, self.hemis1MuHandle)
        wJetMu          = self.hemis1MuHandle.product()
        event.getByLabel (self.hemis1Jet3Label, self.hemis1Jet3Handle )
        jet3           = (self.hemis1Jet3Handle.product())[0]


        weight = 1.0
        if self.useGenWeight :
            event.getByLabel( self.weightsLabel, self.weightsHandle )
            weight = self.weightsHandle.product()[0]

        if jet3 < 1 :
          print "This is not expected, debug!"
          #print "The third jet is ", jet3, " pt is ", wJets[jet3].pt(), " eta is ", wJets[jet3].eta()
          #print "N hemis1 is ", len(wJets)

        pairMass = (wJets[jet3]+wJets[0]).mass()
        ttMass = (wJets[jet3]+wJets[0]+topJets[0]).mass()


        if not self.useMC :        
            jet1P4_massDown = copy.copy(topJets[0])
            jet1P4_massDown.SetM( max(jet1P4_massDown.mass()-100, 0.0) )
            #print topJets[0].px(), topJets[0].py(), topJets[0].pz(), topJets[0].mass() 
            #print jet1P4_massDown.px(), jet1P4_massDown.py(), jet1P4_massDown.pz(), jet1P4_massDown.mass()
            ttMassJet1MassDown = (wJets[jet3]+wJets[0]+jet1P4_massDown).mass()

            jet1P4_massUp = copy.copy(topJets[0])
            jet1P4_massUp.SetM( jet1P4_massUp.mass()+100 )
            ttMassJet1MassUp = (wJets[jet3]+wJets[0]+jet1P4_massUp).mass()
            #print jet1P4_massUp.px(), jet1P4_massUp.py(), jet1P4_massUp.pz(), jet1P4_massUp.mass()

            myrand = ROOT.gRandom.Uniform(140,250)
            jet1P4_massFlat = copy.copy(topJets[0])
            jet1P4_massFlat.SetM( myrand )
            ttMassJet1MassFlat = (wJets[jet3]+wJets[0]+jet1P4_massFlat).mass()


            type2TopMassPdf = self.mistagFile.Get( "TYPE2_TOP_TAG_MASS" )
            modJet1Mass = 0.0
            rx = ROOT.gRandom.Uniform()
            massBin = 0
            lowMassBin = type2TopMassPdf.FindBin(140)
            highMassBin = type2TopMassPdf.FindBin(250)
            for i in range( lowMassBin, highMassBin ) :
              x = type2TopMassPdf.Integral(lowMassBin,i)/type2TopMassPdf.Integral(lowMassBin,highMassBin)
              if x > rx :
                massBin = i
                break

            modJet1Mass = type2TopMassPdf.GetXaxis().GetBinCenter( massBin )
            self.jet1MassMod.Fill( modJet1Mass, weight )
            jet1P4_mod = copy.copy( topJets[0] )
            jet1P4_mod.SetM( modJet1Mass )
            ttMassMod = (wJets[jet3]+wJets[0]+jet1P4_mod).mass()
            ttMassMod2 = ttMass
            ttMassModFlat = ttMassJet1MassFlat
            ttMassMod3Flat = ttMass
            if  topJets[0].mass() < 140  :
                ttMassMod2 = ttMassMod
            if topJets[0].mass() < 140 or topJets[0].mass() > 250:
                ttMassMod3Flat = ttMassModFlat

        if self.veto11 :
            secondJetCuts = wJets[0].pt() > 200 and wJets[0].pt() < 350
        else :
            secondJetCuts = wJets[0].pt() > 200

        passKinCuts = (nTopCand == 1) and secondJetCuts  and (wJetMu[0] < 0.4) and (wJets[jet3].pt() > 30 )
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
        ## for i in range(1,len(wJets) ) :
        ##   if( wJets[i].pt() > 200 and wJets[i].mass() > 60 and wJets[i].mass() < 130 and wJetMu[i] < 0.4 )  :
        ##     checkWTag += 1
        ##     break

        if nTopCand == 1:
            self.cutflow.Fill(3.5,1)
            if secondJetCuts:
                self.cutflow.Fill(4.5,1)
                if wJets[jet3].pt() > 30:
                    self.cutflow.Fill(5.5,1)
                    if wJetMu[0] < 0.4:
                        self.cutflow.Fill(6.5,1)
                        if hasTopTag:
                            self.cutflow.Fill(7.5,1)
                            if hasType2Top:
                                self.cutflow.Fill(8.5,1)

    ######### Plot histograms
        if passKinCuts  :
          self.nJets.Fill( len(topJets)+len(wJets), weight )
          self.topJetCandMass.Fill( topJets[0].mass(), weight )
          self.topJetCandEta.Fill( topJets[0].eta() , weight)
          self.topJetCandPt.Fill( topJets[0].pt(), weight )
          self.wCandMassType12.Fill( wJets[0].mass(), weight )
          self.wCandPtType12.Fill( wJets[0].pt(), weight )
          self.pairMassType12.Fill( pairMass, weight )
          self.nearJetPt.Fill( wJets[jet3].pt(), weight )
          self.nearJetbValue.Fill( wJetBDisc[jet3], weight )
          self.thirdLeadJetbValue.Fill( wJetBDisc[1], weight )
          self.thirdLeadJetPt.Fill( wJets[1].pt(), weight )

          self.mttBkgShape.Fill( ttMass, weight )


          if not self.useMC :
              self.mttBkgShapeMassUp.Fill( ttMassJet1MassUp, weight )
              self.mttBkgShapeMassDown.Fill( ttMassJet1MassDown, weight )
          self.wCandVsTopCandMassType12.Fill( wJets[0].mass() ,  pairMass, weight )

          self.NSubjets.Fill( topJetNSubjets[0], weight )
          self.minmass.Fill( topJetMinMass[0], weight )
          if passTopMass :
            self.NSubjetsWithTopMass.Fill( topJetNSubjets[0], weight )
            self.minmassWithTopMass.Fill( topJetMinMass[0], weight )
            #if topJetNSubjets[0] < 3 :
            #  NSubjetsVsMinMassAll.Fill( topJetNSubjets[0], -1. )
            #else :
            self.NSubjetsVsMinMassAll.Fill( topJetNSubjets[0], topJetMinMass[0], weight )
            #if topJetNSubjets[0] == 2 :   print topJetMinMass[0]
            #if topJetMinMass[0] > 250 :   print topJetMinMass[0], topJetNSubjets[0]

          if hasTopTag  :
            self.topTagMass.Fill( topJets[0].mass(), weight )
            self.topTagPt.Fill( topJets[0].mass(), weight )
            self.wCandMassType12AfterTopTag.Fill( wJets[0].mass(), weight )
            self.wCandPtType12AfterTopTag.Fill( wJets[0].pt(), weight )
            self.nearJetPtAfterTopTag.Fill( wJets[jet3].pt(), weight )
            self.nearJetbValueAfterTopTag.Fill( wJetBDisc[jet3], weight )
            self.pairMassType12AfterTopTag.Fill( pairMass, weight )
            if wJets[0].mass() > 60 and wJets[0].mass() < 130 :
              self.pairMassType12AfterTopTagWithWMass.Fill( pairMass, weight )
            self.wCandVsTopCandMassType12WithTopTag.Fill( wJets[0].mass() ,  pairMass, weight )

          self.topJetCandPtAll.Fill( topJets[0].pt(), weight )
          self.topJetCandMassAll.Fill( topJets[0].mass(), weight )
          self.topJetNsubsAll.Fill( topJetNSubjets[0], weight )
          self.topJetMinMassAll.Fill( topJetMinMass[0], weight )
          self.type2KinTopProbe.Fill( topJets[0].pt(), weight )
          if hasTopTag  :   self.type2KinTopTag.Fill(  topJets[0].pt(), weight )
          if not SBAndSR  :
            self.type2SideBandProbe.Fill( topJets[0].pt(), weight )
            if hasTopTag  :   self.type2SideBandTag.Fill( topJets[0].pt(), weight )



          jet1Pt = topJets[0].pt()
          if hasType2Top  :
            self.topJetCandPtSignal.Fill( topJets[0].pt(), weight )
            self.topJetCandMassSignal.Fill( topJets[0].mass(), weight )
            self.topJetNsubsSignal.Fill( topJetNSubjets[0], weight )
            self.topJetMinMassSignal.Fill( topJetMinMass[0], weight )
            if passTopMass :
              self.NSubjetsVsMinMassSR.Fill( topJetNSubjets[0], topJetMinMass[0], weight )

            #Apply top mistag rate to estimate bkg
            ptBin = self.mistag.FindBin( jet1Pt )

            if not self.useMC :
                
                self.mttBkgWithMistag.Fill( ttMass, self.mistag.GetBinContent(ptBin) * weight )
                self.mttBkgWithMistagModMass.Fill( ttMassMod, self.mistag.GetBinContent(ptBin) * weight )
                #mttPredDistModMass.Accumulate( ttMassMod, jet1Pt, hasTopTag, 1.0 )

                self.mttBkgWithMistagMod2Mass.Fill( ttMassMod2, self.mistag.GetBinContent(ptBin) * weight )
                self.mttBkgWithMistagUp.Fill( ttMass, (self.mistag.GetBinContent(ptBin)+self.mistag.GetBinError(ptBin))* weight )
                self.mttBkgWithMistagDown.Fill( ttMass, (self.mistag.GetBinContent(ptBin)-self.mistag.GetBinError(ptBin))* weight )
                self.type2TopTagExp.Fill( topJets[0].pt(), self.mistag.GetBinContent(ptBin)* weight )
                self.jet1MassExp.Fill( topJets[0].mass(), self.mistag.GetBinContent(ptBin)* weight )
                self.jet1EtaExp.Fill( topJets[0].eta(), self.mistag.GetBinContent(ptBin)* weight )
                self.jet2PtExp.Fill( wJets[0].pt(), self.mistag.GetBinContent(ptBin)* weight )
                self.jet2MassExp.Fill( wJets[0].mass(), self.mistag.GetBinContent(ptBin)* weight )
                self.jet2EtaExp.Fill( wJets[0].eta(), self.mistag.GetBinContent(ptBin)* weight )
                self.jet3PtExp.Fill( wJets[1].pt(), self.mistag.GetBinContent(ptBin)* weight )
                self.jet3MassExp.Fill( wJets[1].mass(), self.mistag.GetBinContent(ptBin)* weight )
                self.jet3EtaExp.Fill( wJets[1].eta(), self.mistag.GetBinContent(ptBin)* weight )

            #Make Top mistag measurement
            self.type2TopProbe.Fill( topJets[0].pt() , weight )
            if hasTopTag :  
              self.type2TopTag.Fill( topJets[0].pt(), weight  )
              self.type2TopTagMass.Fill( topJets[0].mass(), weight  )
              self.jet1MassTag.Fill( topJets[0].mass(), weight  )
              self.jet1EtaTag.Fill( topJets[0].eta(), weight  )
              self.jet2Pt.Fill( wJets[0].pt(), weight  )
              self.jet2MassTag.Fill( wJets[0].mass(), weight  )
              self.jet2EtaTag.Fill( wJets[0].eta(), weight  )
              self.jet3Pt.Fill( wJets[1].pt(), weight  )
              self.jet3MassTag.Fill( wJets[1].mass(), weight  )
              self.jet3EtaTag.Fill( wJets[1].eta(), weight  )

            if ttMass > 800 and ttMass < 900 :
              self.type2TopTagExp800GeV.Fill( topJets[0].pt(), self.mistag.GetBinContent(ptBin) * weight )
              self.type2TopProbe800GeV.Fill( topJets[0].pt(), weight  )
              if hasTopTag :    self.type2TopTag800GeV.Fill( topJets[0].pt(), weight  )
            if ttMass < 1000 :
              self.type2TopTagExpWith1TeV.Fill( topJets[0].pt(), self.mistag.GetBinContent(ptBin) * weight )
              if hasTopTag :  self.type2TopTagWith1TeV.Fill( topJets[0].pt(), weight  )

          if SBAndSR and (not hasType2Top) :
            self.topJetCandPtSideBand.Fill( topJets[0].pt(), weight  )
            self.topJetCandMassSideBand.Fill( topJets[0].mass(), weight  )
            self.topJetNsubsSideBand.Fill( topJetNSubjets[0], weight  )
            self.topJetMinMassSideBand.Fill( topJetMinMass[0], weight  )


          if not self.useMC :

              if SBAndSR and passWiderTopMassCut :
                self.mttBkgShapeWithMassCut.Fill( ttMass, weight  )
              if SBAndSR and (not hasType2Top) and topMassSideBand :
                self.mttBkgShapeWithSideBandMass.Fill( ttMass, weight  )
              if SBAndSR and (not hasType2Top) and passWiderTopMassCut :
                self.mttBkgShapeWithSideBand1Mass.Fill( ttMass, weight  )
              if SBAndSR and (not hasType2Top) :
                self.mttBkgShapeWithSideBand2Mass.Fill( ttMass, weight  )
              if SBAndSR2 and (not SBAndSR ) and passWiderTopMassCut :
                self.mttBkgShapeWithSideBand3Mass.Fill( ttMass, weight  )
              if ((not passNSubjetsCut) or (not passMinMassCut)) and hasType2Top and passTopMass :
                self.mttBkgShapeWithSideBand4Mass.Fill( ttMass, weight  )
              if ((not passNSubjetsCut) or (not passMinMassCut)) and SBAndSR and passWiderTopMassCut :
                self.mttBkgShapeWithSideBand5Mass.Fill( ttMass, weight  )
              if ((not passNSubjetsCut) or (not passMinMassCut)) and SBAndSR and passTopMass :
                self.mttBkgShapeWithSideBand6Mass.Fill( ttMass, weight  )
              if ((not passNSubjetsCut) or (not passMinMassCut)) and hasType2Top and passWiderTopMassCut :
                self.mttBkgShapeWithSideBand7Mass.Fill( ttMass, weight  )

          triggerWeight = 1.0
          if topJets[0].pt() < 450:
            triggerWeight = 0.7


          isJetTagged = hasType2Top and hasTopTag
          if self.useMC is False and hasType2Top :
              self.mttPredDist.        Accumulate( ttMass,      jet1Pt, isJetTagged, weight  )
              self.mttPredDistModMass. Accumulate( ttMassMod,   jet1Pt, isJetTagged, weight  )
              self.mttPredDistMod2Mass.Accumulate( ttMassMod2,  jet1Pt, isJetTagged, weight  )
              self.mttPredDistModMassFlat.Accumulate( ttMassModFlat,  jet1Pt, isJetTagged, weight )  
              self.mttPredDistMod3MassFlat.Accumulate( ttMassMod3Flat,  jet1Pt, isJetTagged,weight )
              self.mttPredDistMod3MassFlatSubtract.Accumulate( ttMassMod3Flat,  jet1Pt, isJetTagged, weight  )
			

          if isJetTagged :
            self.mttMass.Fill( ttMass, weight  )
            self.mttMassTriggerWeight.Fill( ttMass, weight*triggerWeight  )
            if not self.useMC :
                self.mttMassJet1MassDown.Fill( ttMassJet1MassDown, weight  )
            self.nJetsSignal.Fill( len(topJets)+len(wJets) )
            if hasBTag1 :
              self.mttMassWithBTag.Fill( ttMass, weight  )
              self.jet3BTagPt.Fill( wJets[jet3].pt(), weight  )
              self.signalTopTagEta.Fill( topJets[0].eta(), weight  )
          self.signalJet3TagEta.Fill( wJets[jet3].eta(), weight  )

          event.getByLabel (self.allTopTagMinMassLabel, self.allTopTagMinMassHandle)
          topJetMinMass= self.allTopTagMinMassHandle.product()
          event.getByLabel (self.allTopTagTopMassLabel, self.allTopTagTopMassHandle)
          topJetMass= self.allTopTagTopMassHandle.product()
          event.getByLabel (self.allTopTagNSubjetsLabel, self.allTopTagNSubjetsHandle)
          topJetNSubjets= self.allTopTagNSubjetsHandle.product()

          topTag0        = topJetMass[0] > 140 and topJetMass[0] < 250 and topJetMinMass[0] > 50 and topJetNSubjets[0] > 2
          topTag1        = topJetMass[1] > 140 and topJetMass[1] < 250 and topJetMinMass[1] > 50 and topJetNSubjets[1] > 2
          passType11     = topTag0 and topTag1
          if not passType11 and isJetTagged:
            self.mttMassVeto11.Fill( ttMass, weight  )
            self.mttMassTriggerWeightVeto11.Fill( ttMass, weight*triggerWeight  )


          
