import FWCore.ParameterSet.Config as cms

process = cms.Process("FWLitePlots")


process.load('Analysis.SHyFT.shyftAnalysis_cfi')


process.inputs = cms.PSet (
    fileNames = cms.vstring(
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/RelValTTbar/shyft_35x_v3/1e2b4cadbe0380f8ac5134ff55904d15/ljmet_1.root',
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/RelValTTbar/shyft_35x_v3/1e2b4cadbe0380f8ac5134ff55904d15/ljmet_2.root',
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/RelValTTbar/shyft_35x_v3/1e2b4cadbe0380f8ac5134ff55904d15/ljmet_3.root'
        )
)

process.outputs = cms.PSet (
    outputName = cms.string('shyftPlots.root')
)
