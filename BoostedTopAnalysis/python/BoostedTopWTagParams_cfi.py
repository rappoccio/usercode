import FWCore.ParameterSet.Config as cms


boostedTopWTagParams = cms.PSet(
    jetPtMin = cms.double(100.0),
    jetEtaMax = cms.double(3.0),
    muMax = cms.double(0.7),
    ycut = cms.double(0.1),
    numOfDaughters = cms.uint32(2)
    )
