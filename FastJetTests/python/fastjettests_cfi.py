import FWCore.ParameterSet.Config as cms

demo = cms.EDProducer('FastJetTests',
                      seedThreshold = cms.double( 1.0 ),
                      coneRadius = cms.double( 0.5 )
)
