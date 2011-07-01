
import ROOT
import copy

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

from DataFormats.FWLite import Events, Handle
from Analysis.TTBSMTuplesAnalysis import *

class TTKinPlotsAnalyzer :
    """Analyzer to plot general kinematic informatin"""
    def __init__(self, outfile):
        self.outfile = outfile
        self.topTagHandle   = Handle ("vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > >")
        self.topTagLabel    = ( "ttbsmAna", "topTagP4" )

        self.topTagNSubjetsHandle   = Handle( "std::vector<double>")
        self.topTagNSubjetsLabel    = ( "ttbsmAna",  "topTagNSubjets" )

        self.topTagMinMassHandle   = Handle( "std::vector<double>")
        self.topTagMinMassLabel    = ( "ttbsmAna",  "topTagMinMass" )


        self.wTagHandle     = Handle( "vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > >")
        self.wTagLabel      = ( "ttbsmAna", "wTagP4" )

        self.wTagMuHandle   = Handle( "std::vector<double>")
        self.wTagMuLabel    = ( "ttbsmAna",  "wTagMu" )

        self.__book__()

    def __del__(self):
        self.f.cd()
        self.f.Write()
        self.f.Close()


    def __book__(self):
        self.f = ROOT.TFile(self.outfile + ".root", "recreate")
        self.f.cd()

        self.maxJetsWTags = 4
        self.maxJetsTopTags = 4

        self.trigsRun = ROOT.TH1F('trigsRun', 'Trigs run', 20, 0, 20 )

        self.nJetsCA8Pruned = ROOT.TH1F('nJetsCA8Pruned', 'C-A 0.8 Pruned;N_{Jets};Number', 10, 0, 10 )
        self.ptJetsCA8Pruned= []
        self.yJetsCA8Pruned = []
        self.mJetsCA8Pruned = []
        self.muJetsCA8Pruned= []

        for ijet in range(0,self.maxJetsWTags+1):
            self.ptJetsCA8Pruned.append( ROOT.TH1F('ptJetsCA8Pruned' + str(ijet),'C-A 0.8 Pruned;Jet p_{T};Number', 100, 0., 1000.) )
            self.yJetsCA8Pruned .append( ROOT.TH1F('yJetsCA8Pruned' + str(ijet), 'C-A 0.8 Pruned;Jet Rapidity;Number', 100, -2.5, 2.5) )
            self.mJetsCA8Pruned .append( ROOT.TH1F('mJetsCA8Pruned' + str(ijet), 'C-A 0.8 Pruned;Jet Mass;Number', 100, 0, 500.) )
            self.muJetsCA8Pruned.append( ROOT.TH1F('muJetsCA8Pruned' + str(ijet),'C-A 0.8 Pruned;Mass Drop (#mu = m_{0}/m_{jet});Number', 100, 0, 1) )


        self.nJetsCA8TopTag = ROOT.TH1F('nJetsCA8TopTag', 'C-A 0.8 TopTagged;N_{Jets};Number', 10, 0, 10 )
        self.ptJetsCA8TopTag= []
        self.yJetsCA8TopTag = []
        self.mJetsCA8TopTag = []
        self.minMassJetsCA8TopTag= []
        self.nSubjetsJetsCA8TopTag= []

        for ijet in range(0,self.maxJetsWTags+1):
            self.ptJetsCA8TopTag.append( ROOT.TH1F('ptJetsCA8TopTag' + str(ijet),'C-A 0.8 TopTagged;Jet p_{T};Number', 100, 0., 1000.) )
            self.yJetsCA8TopTag .append( ROOT.TH1F('yJetsCA8TopTag' + str(ijet), 'C-A 0.8 TopTagged;Jet Rapidity;Number', 100, -2.5, 2.5) )
            self.mJetsCA8TopTag .append( ROOT.TH1F('mJetsCA8TopTag' + str(ijet), 'C-A 0.8 TopTagged;Jet Mass;Number', 100, 0, 500.) )
            self.minMassJetsCA8TopTag.append( ROOT.TH1F('minMassJetsCA8TopTag' + str(ijet),'C-A 0.8 TopTagged;Min Mass;Number', 100, 0, 500.) )
            self.nSubjetsJetsCA8TopTag.append( ROOT.TH1F('nSubjetsJetsCA8TopTag' + str(ijet),'C-A 0.8 TopTagged;N_{Subjets};Number', 5, 0, 5) )



    def analyze(self, event) :
        event.getByLabel (self.wTagLabel, self.wTagHandle)
        wJets = self.wTagHandle.product()

        event.getByLabel (self.wTagMuLabel, self.wTagMuHandle)
        wJetsMu = self.wTagMuHandle.product()

        nWJets = 0
        for ijet in range(0,len(wJets)) :
            jet = wJets[ijet]
            if jet.pt() > 30 :
                nWJets += 1
                if ijet <= self.maxJetsWTags :
                    self.ptJetsCA8Pruned[ijet].Fill( jet.pt() )
                    self.yJetsCA8Pruned[ijet].Fill( jet.Rapidity() )
                    self.mJetsCA8Pruned[ijet].Fill( jet.mass() )
                    self.muJetsCA8Pruned[ijet].Fill( wJetsMu[ijet] )

        self.nJetsCA8Pruned.Fill( nWJets )


        event.getByLabel (self.topTagLabel, self.topTagHandle)
        topJets = self.topTagHandle.product()


        event.getByLabel (self.topTagNSubjetsLabel, self.topTagNSubjetsHandle)
        topTagNSubjets =self.topTagNSubjetsHandle.product()

        event.getByLabel (self.topTagMinMassLabel, self.topTagMinMassHandle)
        topTagMinMass =self.topTagMinMassHandle.product()

        nTopJets = 0
        for ijet in range(0,len(topJets)) :
            jet = topJets[ijet]
            if jet.pt() > 350 :
                nTopJets += 1
                if ijet <= self.maxJetsTopTags :
                    self.ptJetsCA8TopTag[ijet].Fill( jet.pt() )
                    self.yJetsCA8TopTag[ijet].Fill( jet.Rapidity() )
                    self.mJetsCA8TopTag[ijet].Fill( jet.mass() )
                    self.minMassJetsCA8TopTag[ijet].Fill( topTagMinMass[ijet] )
                    self.nSubjetsJetsCA8TopTag[ijet].Fill( topTagNSubjets[ijet] )

        self.nJetsCA8TopTag.Fill( nTopJets )

