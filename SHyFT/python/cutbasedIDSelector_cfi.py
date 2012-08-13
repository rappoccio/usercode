import FWCore.ParameterSet.Config as cms

cutbasedIDSelector = cms.PSet(
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
    pvSrc = cms.InputTag("goodOfflinePrimaryVertices"),
    cutsToIgnore = cms.vstring("ooemoop_EB", "hoe_EE", "ooemoop_EE")   
    )
