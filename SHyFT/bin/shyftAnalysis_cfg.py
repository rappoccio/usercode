import FWCore.ParameterSet.Config as cms

process = cms.Process("FWLitePlots")


from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis

process.shyftAnalysis = inputShyftAnalysis.clone(
#    muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
#    electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
#    metSrc = cms.InputTag('patMETsPFlow'),
#    jetSrc = cms.InputTag('selectedPatJetsPFlow'),
    jetPtMin = cms.double(30.0),
    minJets = cms.int32(5)
    )

process.inputs = cms.PSet (
    fileNames = cms.vstring(
        'shyft_382_pat.root'
        ),
        maxEvents = cms.int32(-1)
)

process.outputs = cms.PSet (
    outputName = cms.string('shyftPlotsStd.root')
)
