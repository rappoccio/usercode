import FWCore.ParameterSet.Config as cms



jetStudies2011 = cms.PSet(
    # Jets: Already have jet ID applied
    jetSrc = cms.InputTag('goodPatJetsPFlow'),
    # Rho from the CA8 jets
    rhoSrc = cms.InputTag('ca8PFJetsPFlow', 'rho'),
    # Offline Primary Vertices (all of them) to reweight MC
    pvSrc = cms.InputTag('offlinePrimaryVertices'),
    # pat::TriggerEvent
    trigSrc = cms.InputTag("patTriggerEvent"),
    # Gen Jets for the extra CA8 collections
    genJetsSrc = cms.InputTag("ca8GenJetsNoNu"),
    useCA8GenJets = cms.bool(False),    
    # luminosity weighting for MC
    weightPV = cms.bool(False),
    lumiWeighting = cms.PSet(
        generatedFile = cms.string("pileup_generated.root"),
        dataFile = cms.string("pileup_160405-161312.root")
        ),
    # use b-tagging on the jets
    useBTags = cms.bool(False),
    # Order by jet mass instead of pt
    orderByMass = cms.bool(False),
    # Triggers to use (in order):
    trigs = cms.vstring([
        'HLT_Jet370_v1',
        'HLT_Jet240_v1',
        'HLT_Jet190_v1',
        'HLT_Jet150_v1',        
        'HLT_Jet110_v1',
        'HLT_Jet80_v1',
        'HLT_Jet60_v1',
        'HLT_Jet30_v1',

        ## 'HLT_DiJetAve300U_v4',
        ## 'HLT_DiJetAve180U_v4',
        ## 'HLT_DiJetAve140U_v4',
        ## 'HLT_DiJetAve100U_v4',
        ## 'HLT_DiJetAve50U_v4',
        ## 'HLT_DiJetAve70U_v4',
        ## 'HLT_DiJetAve30U_v4',
        ## 'HLT_DiJetAve15U_v4',
        ])
)
