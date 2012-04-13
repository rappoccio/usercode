import FWCore.ParameterSet.Config as cms


pvFilter = cms.EDFilter("PVFilter",
                          pvSrc = cms.InputTag('offlinePrimaryVertices'),
                          minPVNdof = cms.double(5.0),
                          maxPVZ = cms.double(15.0)
                                    )
