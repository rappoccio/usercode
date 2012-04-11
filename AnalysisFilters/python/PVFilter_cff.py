import FWCore.ParameterSet.Config as cms


pvFilter = cms.EDFilter("PVFilter",
                          pvSrc = cms.InputTag('offlinePrimaryVertices'),
                          minPVTracks = cms.int32(4),
                          maxPVZ = cms.double(15.0)
                                    )
