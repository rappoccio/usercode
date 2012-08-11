import FWCore.ParameterSet.Config as cms

#from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector as pvSel
from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
#from PhysicsTools.SelectorUtils.jetIDSelector_cfi import jetIDSelector
#from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector
from PhysicsTools.SelectorUtils.pfMuonSelector_cfi import pfMuonSelector
from PhysicsTools.SelectorUtils.pfElectronSelector_cfi import pfElectronSelector


wplusjetsAnalysis = cms.PSet(

    electronIdTest = cms.PSet(
    version = cms.string('NONE'),    
    deta_EB  =  cms.double(7.0e-03),
    dphi_EB  =  cms.double(8.0e-01),
    sihih_EB =  cms.double(1.0e-02),
    hoe_EB   =  cms.double(1.5e-01), 
    d0_EB    =  cms.double(4.0e-02),
    dZ_EB    =  cms.double(2.0e-01), 
    ooemoop_EB = cms.double(0),
    deta_EE    = cms.double(1.0e-02),
    dphi_EE    = cms.double(7.0e-01),
    sihih_EE   = cms.double(3.0e-02),
    hoe_EE     = cms.double(0),
    d0_EE      = cms.double(4.0e-02),
    dZ_EE      = cms.double(2.0e-01),
    ooemoop_EE = cms.double(0),
    cutsToIgnore = cms.vstring("ooemoop_EB", "hoe_EE", "ooemoop_EE")
    ),
    
    # Primary vertex
    pvSelector = cms.PSet(
    pvSrc = cms.InputTag('goodOfflinePrimaryVertices'),
    minNdof = cms.double(4.0),
    maxZ = cms.double(24.0),
    maxRho = cms.double(2.0),
    NPV = cms.int32(1),
    ),    
    # input parameter sets
    muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
    electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
    jetSrc = cms.InputTag('selectedPatJetsPFlow'),
    jetClonesSrc = cms.InputTag('myClones'),
    metSrc = cms.InputTag('patMETsPFlow'),
    trigSrc = cms.InputTag('patTriggerEvent'),
    muTrig = cms.string('HLT_Mu9'),
    eleTrig = cms.string('HLT_Ele10_LW_L1R'),
    pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
    rhoSrc  = cms.InputTag('kt6PFJetsPFlow', 'rho'),
    useWP95Selection = cms.bool(False),
    useWP70Selection = cms.bool(True),
    usePFIso = cms.bool(True),
    useNoID  = cms.bool(False),
    useVBTFDetIso  = cms.bool(False),
    # tight muons
    muonIdTight = pfMuonSelector.clone(
    version = cms.string('SPRING11'),
    Chi2 = cms.double(10.0),
    D0 = cms.double(0.02),
    NHits = cms.int32(11),
    NValMuHits = cms.int32(0),
    PFIso = cms.double(0.125),
    nPixelHits = cms.int32(1),
    nMatchedStations=cms.int32(1),
    cutsToIgnore=cms.vstring()
    ),
    # tight electrons
    electronIdTight = pfElectronSelector.clone(
    version = cms.string('SPRING11'),
    MVA = cms.double(-0.01),
    MaxMissingHits = cms.int32(1),
    D0 = cms.double(0.02),
    electronIDused = cms.string('eidSuperTightMC'),
    ConversionRejection = cms.bool(False),
    PFIso = cms.double(0.1),
    cutsToIgnore = cms.vstring('MVA', 'ConversionRejection', 'MaxMissingHits')
    ),
    # loose electrons
    electronIdLoose = pfElectronSelector.clone(
    version = cms.string('SPRING11'),
    MVA = cms.double(-0.01),
    MaxMissingHits = cms.int32(1),
    D0 = cms.double(999.0),
    electronIDused = cms.string('eidLooseMC'),
    ConversionRejection = cms.bool(False),
    PFIso = cms.double(0.2),
    cutsToIgnore = cms.vstring('MVA', 'D0', 'MaxMissingHits', 'ConversionRejection')
    ),
    # loose muons
    muonIdLoose = pfMuonSelector.clone(
    version = cms.string('SPRING11'),
    Chi2 = cms.double(999.0),
    D0 = cms.double(999.0),
    NHits = cms.int32(-1),
    NValMuHits = cms.int32(-1),
    PFIso = cms.double(0.2),
    nPixelHits = cms.int32(1),
    nMatchedStations=cms.int32(1),
    cutsToIgnore=cms.vstring('Chi2','D0','NHits','NValMuHits','nPixelHits','nMatchedStations')
    ),
    # loose jets
    #jetIdLoose = jetIDSelector.clone(),
    #pfjetIdLoose = pfJetIDSelector.clone(),
    # kinematic cuts
    minJets        = cms.int32( 1 ),
    muPlusJets     = cms.bool( True ),
    ePlusJets      = cms.bool( False ),
    muPtMin        = cms.double( 30.0 ),
    muEtaMax       = cms.double( 2.1 ),
    eleEtMin       = cms.double( 20.0 ),
    eleEtaMax      = cms.double( 2.4 ),
    muPtMinLoose   = cms.double( 10.0 ),
    muEtaMaxLoose  = cms.double( 2.5 ),
    eleEtMinLoose  = cms.double( 15.0 ),
    eleEtaMaxLoose = cms.double( 2.5 ),
    elDist         = cms.double( 0.02 ),
    elDcot         = cms.double( 0.02 ),
    eRelIso        = cms.double( 0.1 ),
    eEtCut         = cms.double( 30. ),
    vertexCut      = cms.double( 1.),
    dxy            = cms.double( 0.02),
    jetPtMin       = cms.double( 30.0 ),
    jetEtaMax      = cms.double( 2.4 ),
    jetScale       = cms.double( 0.0 ),
    jetUncertainty = cms.double( 0.0 ),
    jetSmear       = cms.double( 0.0 ),
    ePtScale       = cms.double( 0.0 ),
    ePtUncertaintyEE = cms.double( 0.025), 
    metMin         = cms.double( 0.0 ),
    metMax         = cms.double( 100000.0),
    wMTMax         = cms.double( 100000.0),
    unclMetScale   = cms.double( 0.0 ),
    muJetDR        = cms.double( 0.3 ),
    useJetClones   = cms.bool(False),
    eleJetDR       = cms.double( 0.3 ),
    rawJetPtCut    = cms.double( 0.0 ),
    useData        = cms.bool(False),
    jecPayloads    = cms.vstring([
    'Jec12_V1_L1FastJet_AK5PFchs.txt',
    'Jec12_V1_L2Relative_AK5PFchs.txt',
    'Jec12_V1_L3Absolute_AK5PFchs.txt',
    'Jec12_V1_L2L3Residual_AK5PFchs.txt',
    'Jec12_V1_Uncertainty_AK5PFchs.txt', ])
    #useL1Offset    = cms.bool(True),#Dummy variable: will remove it next time
    #jecPayload     = cms.string('Jec11_V2_AK5PFchs_Uncertainty.txt')
)
