import FWCore.ParameterSet.Config as cms

process = cms.Process("FWLitePlots")


process.load('Analysis.SHyFT.shyftAnalysis_cfi')


process.inputs = cms.PSet (
    maxEvents = cms.int32(-1),
    fileNames = cms.vstring(
'/uscms_data/d2/rappocc/SHyFTFiles/TTbar/shyft_35x_v3_syncex/ljmet_1_1.root',
'/uscms_data/d2/rappocc/SHyFTFiles/TTbar/shyft_35x_v3_syncex/ljmet_2_1.root'


        )
)

process.outputs = cms.PSet (
    outputName = cms.string('shyftPlots_ttbar_pythia_syncex.root')
)
