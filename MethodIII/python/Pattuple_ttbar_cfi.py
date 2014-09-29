import FWCore.ParameterSet.Config as cms

# from 

def RecoInput() : 
 return cms.Source("PoolSource",
                   debugVerbosity = cms.untracked.uint32(200),
                   debugFlag = cms.untracked.bool(True),
                   
                   fileNames = cms.untracked.vstring(
        'dcap:///pnfs/cms/WAX/resilient/guofan/TTJets_patuple/TTJets_testPatTuple_1.root',
        'dcap:///pnfs/cms/WAX/resilient/guofan/TTJets_patuple/TTJets_testPatTuple_2.root',
        'dcap:///pnfs/cms/WAX/resilient/guofan/TTJets_patuple/TTJets_testPatTuple_3.root',
        'dcap:///pnfs/cms/WAX/resilient/guofan/TTJets_patuple/TTJets_testPatTuple_4.root',
        'dcap:///pnfs/cms/WAX/resilient/guofan/TTJets_patuple/TTJets_testPatTuple_5.root',
        'dcap:///pnfs/cms/WAX/resilient/guofan/TTJets_patuple/TTJets_testPatTuple_6.root',
        'dcap:///pnfs/cms/WAX/resilient/guofan/TTJets_patuple/TTJets_testPatTuple_7.root',
        'dcap:///pnfs/cms/WAX/resilient/guofan/TTJets_patuple/TTJets_testPatTuple_8.root',
        'dcap:///pnfs/cms/WAX/resilient/guofan/TTJets_patuple/TTJets_testPatTuple_9.root',
        'dcap:///pnfs/cms/WAX/resilient/guofan/TTJets_patuple/TTJets_testPatTuple_10.root',
            )
                   )
