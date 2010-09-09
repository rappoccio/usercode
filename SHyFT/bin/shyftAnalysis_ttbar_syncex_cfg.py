import FWCore.ParameterSet.Config as cms

process = cms.Process("FWLitePlots")


process.load('Analysis.SHyFT.shyftAnalysis_cfi')
process.shyftAnalysis.btaggerString = cms.string('simpleSecondaryVertexBJetTags')
process.shyftAnalysis.doMC = cms.bool(True)

process.inputs = cms.PSet (
    maxEvents = cms.int32(-1),
    fileNames = cms.vstring(
'dcap:///pnfs/cms/WAX/11/store/user/srappocc/TTbarJets-madgraph/shyft_38xOn35x_v3/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_9_1_4WJ.root'

        )
)

process.outputs = cms.PSet (
    outputName = cms.string('shyftPlots_ttbar_pythia_syncex.root')
)
