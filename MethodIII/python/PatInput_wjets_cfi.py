import FWCore.ParameterSet.Config as cms

# from 

def RecoInput() : 
 return cms.Source("PoolSource",
                   debugVerbosity = cms.untracked.uint32(200),
                   debugFlag = cms.untracked.bool(True),
                   
                   fileNames = cms.untracked.vstring(
    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/WJets_preprod/PATLayer1_Output_fromAOD_full_1.root',
    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/WJets_preprod/PATLayer1_Output_fromAOD_full_2.root'
     )
                   )
