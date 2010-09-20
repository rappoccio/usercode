import FWCore.ParameterSet.Config as cm

from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector
from Analysis.BoostedTopAnalysis.BoostedTopWTagParams_cfi import *

wPlusBJetAnalysis = cms.PSet(
      jetSrc = cms.InputTag( "selectedPatJetsCA8PrunedPF" ),
      WPlusBJetSelection = cms.PSet(
          trigSrc = cms.InputTag( "patTriggerEvent" ),
          trig    = cms.string( "HLT_Jet30U" ),
          pfJetIDParams = cms.PSet( pfJetIDSelector.clone() ),
          jetSrc = cms.InputTag( "selectedPatJetsCA8PrunedPF" ),
          BoostedTopWJetParameters  = boostedTopWTagParams.clone( jetPtMin = 200, jetEtaMax = 2.4 ),
          jetPtMin  = cms.double(30.0),
          jetEtaMax = cms.double(3.0),
          bTagAlgorithm = cms.string( "trackCountingHighEffBJetTags" ),
          bTagOP   = cms.double( 3.3 )

      )

)
