import FWCore.ParameterSet.Config as cms


from PhysicsTools.SelectorUtils.wplusjetsAnalysis_cfi import wplusjetsAnalysis

shyftAnalysis = cms.PSet(
    wplusjetsAnalysis.clone(     
        muonSrc = cms.InputTag('selectedPatMuonsStd'),
        electronSrc = cms.InputTag('selectedPatElectronsStd'),
        jetSrc = cms.InputTag('selectedPatJetsStd'),
        metSrc = cms.InputTag('patMETsStd'),
        trigSrc = cms.InputTag('patTriggerEventStd'),
        jetPtMin = cms.double(30.0),
        jetEtaMax = cms.double(2.4)
        ) ,
    sampleName = cms.string("top"),
    mode = cms.int32(0),
    heavyFlavour = cms.bool(False),
    doMC           = cms.bool(False),
    payload = cms.string( "PayLoad.root" ),
    bPerformanceTag = cms.string( "MCSSVMb" ),
    cPerformanceTag = cms.string( "MCSSVMc" ),
    lPerformanceTag = cms.string( "MCSSVMl" )
)
