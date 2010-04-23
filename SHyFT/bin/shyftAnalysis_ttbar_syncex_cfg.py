import FWCore.ParameterSet.Config as cms

process = cms.Process("FWLitePlots")


process.load('Analysis.SHyFT.shyftAnalysis_cfi')


process.inputs = cms.PSet (
    maxEvents = cms.int32(-1),
    fileNames = cms.vstring(
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbar/shyft_35x_v4_syncex/b0399e0e9cf131396b9de602835507f7/ljmet_1_1.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbar/shyft_35x_v4_syncex/b0399e0e9cf131396b9de602835507f7/ljmet_2_1.root'



        )
)

process.outputs = cms.PSet (
    outputName = cms.string('shyftPlots_ttbar_pythia_syncex.root')
)
