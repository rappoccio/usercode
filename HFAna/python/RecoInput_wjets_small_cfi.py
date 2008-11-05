import FWCore.ParameterSet.Config as cms

# from 

def RecoInput() :

  maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
  readFiles = cms.untracked.vstring(
       '/store/mc/Summer08/WJets-madgraph/GEN-SIM-RECO/IDEAL_V9_v1/0005/00343F91-39A1-DD11-A3DF-00E081328940.root'
       )
  secFiles = cms.untracked.vstring() 
  source = cms.Source ("PoolSource",fileNames = readFiles, secondaryFileNames = secFiles)


  return source
