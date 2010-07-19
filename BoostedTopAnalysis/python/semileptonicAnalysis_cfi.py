import FWCore.ParameterSet.Config as cms

from Analysis.BoostedTopAnalysis.BoostedTopWTagParams_cfi import boostedTopWTagParams
from PhysicsTools.SelectorUtils.wplusjetsAnalysis_cfi import wplusjetsAnalysis as wPlusJets


semileptonicAnalysis = cms.PSet(
    hadronicWParams = boostedTopWTagParams.clone(),
    semileptonicSelection = cms.PSet(
        WPlusJetsParams = wPlusJets.clone(
            jetSrc = cms.InputTag("selectedPatJetsCA8PrunedPF"),
            minJets = cms.int32(2),
            muPtMin = cms.double(25.0),
            muonIdTight  = wPlusJets.muonIdTight.clone( cutsToIgnore= ['RelIso'])
            ),
        jetSrc = cms.InputTag("selectedPatJetsCA8PrunedPF"),
        trigTag = cms.InputTag("patTriggerEvent"),
        cutsToIgnore      = cms.vstring(['Trigger']), #'Relative Pt','Minimum Delta R' ,'Opposite leadJetPt'
        dRMin             = cms.double(0.5),
        ptRelMin          = cms.double(25.0),
        mu                = cms.double(0.7),
        ycut              = cms.double(0.1),
        leadJetPt         = cms.double(0.0),
        oppLeadJetPt      = cms.double(100.0),
        deltaPhi          = cms.double(3.1415926/2.0)
        )

)
