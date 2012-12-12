import FWCore.ParameterSet.Config as cms


pvSelector = cms.PSet(
    pvSrc = cms.InputTag('offlinePrimaryVertices'),
    minPVNdof = cms.double(5.0),
    maxPVZ = cms.double(15.0)
    )
