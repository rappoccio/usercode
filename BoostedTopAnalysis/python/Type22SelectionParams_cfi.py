import FWCore.ParameterSet.Config as cm

from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector
from Analysis.BoostedTopAnalysis.BoostedTopWTagParams_cfi import *

Type22SelectionParams = cms.PSet(
  pfJetIDParams = cms.PSet( pfJetIDSelector.clone() ),
  BoostedTopWJetParameters  = boostedTopWTagParams.clone( ),
  jetPt0 = cms.double(200),
  jetPt1 = cms.double(30),
  jetEta = cms.double(2.4),
  bTagOP = cms.double(3.3),
  bTagAlgo = cms.string("trackCountingHighEffBJetTags"),
  jetSrc = cms.InputTag( "selectedPatJetsCA8PrunedPF" )
)

