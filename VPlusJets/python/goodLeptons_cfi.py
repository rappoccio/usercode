#
# vplusjets_cfi.py
#

import FWCore.ParameterSet.Config as cms

goodLeptons = cms.EDFilter("VPlusJets",
                         # muons
                         makeMuons     = cms.bool( True ),
                         muonSrc       = cms.InputTag( "selectedLayer1Muons"),
                         chi2CutMuon   = cms.double( 10.0 ),
                         d0CutMuon     = cms.double( 0.2 ),  # in cm
                         nHitsCutMuon  = cms.uint32( 11 ),
                         hcalEtCutMuon = cms.double( 6.0 ), # GeV
                         ecalEtCutMuon = cms.double( 4.0 ),
                         relIsoCutMuon = cms.double( 0.1),
                         # electrons
                         makeElectrons = cms.bool( True ),
                         electronSrc       = cms.InputTag( "selectedLayer1Electrons"),
                         d0CutElectron     = cms.double( 0.2 ),  # in cm
                         relIsoCutElectron = cms.double( 0.1),
                         # filter cuts
                         minMuons = cms.uint32( 0 ),
                         maxMuons = cms.uint32( 9999 ),
                         minElectrons = cms.uint32( 0 ),
                         maxElectrons = cms.uint32( 9999 )
                         )
