import FWCore.ParameterSet.Config as cms

semilepSel = cms.EDFilter("SemiLepSel",
			  src = cms.InputTag("genParticles"),
			  verbose = cms.bool(False)
			 )



