import FWCore.ParameterSet.Config as cms

# from 

def RecoInput() : 
 return cms.Source("PoolSource",
                   debugVerbosity = cms.untracked.uint32(200),
                   debugFlag = cms.untracked.bool(True),
                   
                   fileNames = cms.untracked.vstring(
    'dcache:/pnfs/cms/WAX/resilient/baites/wjets/Aug-03-2008/wc_patLayer1_10TeV.root'
     
     )
                   )
