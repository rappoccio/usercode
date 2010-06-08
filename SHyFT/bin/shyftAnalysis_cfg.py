import FWCore.ParameterSet.Config as cms

process = cms.Process("FWLitePlots")


process.load('Analysis.SHyFT.shyftAnalysis_cfi')

process.inputs = cms.PSet (
    fileNames = cms.vstring(
'dcap:///pnfs/cms/WAX/11/store/user/lannon/TTbarJets-madgraph/SHYFT_pat357/b0399e0e9cf131396b9de602835507f7/ljmet_9_1.root',
'dcap:///pnfs/cms/WAX/11/store/user/lannon/TTbarJets-madgraph/SHYFT_pat357/b0399e0e9cf131396b9de602835507f7/ljmet_8_1.root',
'dcap:///pnfs/cms/WAX/11/store/user/lannon/TTbarJets-madgraph/SHYFT_pat357/b0399e0e9cf131396b9de602835507f7/ljmet_7_1.root',
'dcap:///pnfs/cms/WAX/11/store/user/lannon/TTbarJets-madgraph/SHYFT_pat357/b0399e0e9cf131396b9de602835507f7/ljmet_75_1.root'
        ),
        maxEvents = cms.int32(100)
)

process.outputs = cms.PSet (
    outputName = cms.string('shyftPlots.root')
)
