import FWCore.ParameterSet.Config as cms

from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector

Type11QCDEstimationParams = cms.PSet( 
  Type11Selection = cms.PSet(
      pfJetIDParams = cms.PSet( pfJetIDSelector.clone() ),
    caTopJetPtMin = cms.double(250),
    caTopJetEtaCut = cms.double(2.4),
    caTopJetCollectionInputTag = cms.InputTag( "selectedPatJetsCATopTagPF" )
  ),

  caTopJetMassMin = cms.double(140),
  caTopJetMassMax = cms.double(250),
  caTopMinMassMin = cms.double(50),
  caTopMistagFileName = cms.string("caTopMistag.root")
)

