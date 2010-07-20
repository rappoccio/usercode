import FWCore.ParameterSet.Config as cms


shyftAnalysis = cms.PSet(
    # input parameter sets
    muonSrc = cms.InputTag('selectedPatMuonsStd'),
    electronSrc = cms.InputTag('selectedPatElectronsStd'),
    jetSrc = cms.InputTag('selectedPatJetsStd'),
    metSrc = cms.InputTag('patMETsStd'),
    trigSrc = cms.InputTag('patTriggerEventStd'),
    sampleName = cms.string("top"),
    mode = cms.int32(0),
    heavyFlavour = cms.bool(False),

    # object ID

    # tight muons
    muonIdTight = cms.PSet(
        version = cms.string('SUMMER08'),
        Chi2 = cms.double(10.0),
        D0 = cms.double(0.2),
        NHits = cms.int32(11),
        ECalVeto = cms.double(4.0),
        HCalVeto = cms.double(6.0),
        RelIso = cms.double(0.05),
        ),
    # tight electrons
    electronIdTight = cms.PSet(
        version = cms.string('SUMMER08'),
        D0 = cms.double(0.02),
        RelIso = cms.double( 0.1 )
        ),
    # loose muons
    muonIdLoose = cms.PSet(
        version = cms.string('SUMMER08'),
        Chi2 = cms.double(10.0),
        D0 = cms.double(0.2),
        NHits = cms.int32(11),
        ECalVeto = cms.double(4.0),
        HCalVeto = cms.double(6.0),
        RelIso = cms.double(0.2),
        cutsToIgnore = cms.vstring('Chi2', 'D0', 'NHits','ECalVeto','HCalVeto')
        ),
    # loose electrons
    electronIdLoose = cms.PSet(
        version = cms.string('SUMMER08'),
        D0 = cms.double(0.2),
        RelIso = cms.double( 0.2 ),
        cutsToIgnore = cms.vstring('D0')
        ),
    # loose jets
    jetIdLoose = cms.PSet(
        version = cms.string('CRAFT08'),
        quality = cms.string('LOOSE')
        ),
    # kinematic cuts
    minJets        = cms.int32( 1 ),
    muPlusJets     = cms.bool( True ),
    ePlusJets      = cms.bool( False ),
    muPtMin        = cms.double( 20.0 ),
    muEtaMax       = cms.double( 2.1 ),
    elePtMin       = cms.double( 20.0 ),
    eleEtaMax      = cms.double( 2.4 ),
    muPtMinLoose   = cms.double( 20.0 ),
    muEtaMaxLoose  = cms.double( 2.1 ),
    elePtMinLoose  = cms.double( 20.0 ),
    eleEtaMaxLoose = cms.double( 2.4 ),    
    jetPtMin       = cms.double( 20.0 ),
    jetEtaMax      = cms.double( 3.0 ),
    jetScale       = cms.double( 1.0 )
)
