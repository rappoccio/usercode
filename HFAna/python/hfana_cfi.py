import FWCore.ParameterSet.Config as cms


hfAna = cms.EDAnalyzer("HFAna",
                       src = cms.InputTag('selectedLayer1Jets'),
                       verbose = cms.bool(False)
                       )
