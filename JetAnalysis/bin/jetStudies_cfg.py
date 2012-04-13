import FWCore.ParameterSet.Config as cms

process = cms.Process("FWLitePlots")

process.jetStudies = cms.PSet(
    # input parameter sets
    jetSrc = cms.InputTag('selectedPatJets'),
    pfJetSrc = cms.InputTag('selectedPatJetsAK5PF'),
    metSrc = cms.InputTag('patMETs'),
    pfMetSrc = cms.InputTag('patMETsPF'),
    useCalo = cms.bool(True)
)
process.pfJetStudies = process.jetStudies.clone( useCalo = cms.bool(False) )


process.load('PhysicsTools.SelectorUtils.pfJetIDSelector_cfi')
process.load('PhysicsTools.SelectorUtils.jetIDSelector_cfi')

process.plotParameters = cms.PSet (
    doTracks = cms.bool(False),
    useMC = cms.bool(False),
    runs = cms.vint32([])
)


process.inputs = cms.PSet (
    fileNames = cms.vstring(
        'reco_7TeV_firstdata_mc_354_pat.root'
        )
)

process.outputs = cms.PSet (
    outputName = cms.string('jetPlots.root')
)
