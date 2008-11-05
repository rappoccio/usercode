import FWCore.ParameterSet.Config as cms


hfAna = cms.EDAnalyzer("HFAna",
                       src = cms.InputTag('selectedLayer1Jets'),
                       bFlavorHistory = cms.InputTag("bFlavorHistoryProducer", "bPartonFlavorHistory"),
                       cFlavorHistory = cms.InputTag("cFlavorHistoryProducer", "cPartonFlavorHistory"),
                       genJetsSrc = cms.InputTag("iterativeCone5GenJets"),
                       verbose = cms.bool(False)
                       )
