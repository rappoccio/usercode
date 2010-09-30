import FWCore.ParameterSet.Config as cms

process = cms.Process("FWLitePlots")


process.load('Analysis.SHyFT.shyftAnalysis_cfi')

process.inputs = cms.PSet (
    fileNames = cms.vstring(
'/Users/rappocc/data_local/shyft/ljmet_1_1.root',
'/Users/rappocc/data_local/shyft/ljmet_2_1.root'
        ),
        maxEvents = cms.int32(-1)
)

process.outputs = cms.PSet (
    outputName = cms.string('shyftPlots.root')
)
