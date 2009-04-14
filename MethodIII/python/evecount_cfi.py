import FWCore.ParameterSet.Config as cms

eventcount = cms.EDAnalyzer('EveCount',
				muonsrc = cms.InputTag("selectedLayer1Muons"),
				jetsrc  = cms.InputTag("selectedLayer1Jets"),
				matchsrc= cms.InputTag("selectedMuonsGenParticlesMatch"),
				verbose = cms.bool(False),
				Lxy  =  cms.double(3.0),
				bTagThreshold  = cms.double(8.0)
)
