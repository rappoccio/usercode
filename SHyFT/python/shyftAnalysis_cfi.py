import FWCore.ParameterSet.Config as cms


from PhysicsTools.SelectorUtils.wplusjetsAnalysis_cfi import wplusjetsAnalysis

shyftAnalysis = cms.PSet(
    wplusjetsAnalysis.clone(     
        muonSrc = cms.InputTag('selectedPatMuons'),
        electronSrc = cms.InputTag('selectedPatElectrons'),
        jetSrc = cms.InputTag('selectedPatJets'),
        metSrc = cms.InputTag('patMETs'),
        trigSrc = cms.InputTag('patTriggerEvent'),
        jetPtMin = cms.double(30.0),
        jetEtaMax = cms.double(2.4),
#        minJets = cms.int32(5)
        ) ,
    sampleName = cms.string("top"),
    mode = cms.int32(0),
    heavyFlavour = cms.bool(False),
    doMC           = cms.bool(False),
    payload = cms.string( "PayLoad.root" ),
    bPerformanceTag = cms.string( "MCSSVMb" ),
    cPerformanceTag = cms.string( "MCSSVMc" ),
    lPerformanceTag = cms.string( "MCSSVMl" ),
    btaggerString = cms.string('simpleSecondaryVertexHighEffBJetTags'),
    identifier = cms.string('Douglas Adams'),
    reweightPDF = cms.bool(False),
    pdfSrc = cms.InputTag('generator'),
    pdfSetNames = cms.vstring( [
        "cteq65"
        , "MRST2006nnlo"
        , "MRST2007lomod"
        
        ] )
#    btaggerString = cms.string('simpleSecondaryVertexBJetTags')
)
#shyftAnalysis.pvSelector.maxZ = 24.0
