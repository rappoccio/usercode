import FWCore.ParameterSet.Config as cms
process = cms.Process("PROCESSNAME")
process.maxLuminosityBlocks = cms.untracked.PSet( 
               input = cms.untracked.int32(-1)
    )

readFiles = cms.untracked.vstring()

process.source = cms.Source("PoolSource",
                            #fileNames = cms.untracked.vstring( 
#'dcap://cmsdca.fnal.gov:24136/pnfs/fnal.gov/usr/cms/WAX/11/store/user/guofan/JetMET/ttbsm_383/ff90c3c4588c16ad10031564667fd507/ttbsm_381_94_1_N7x.root',
#'dcap://cmsdca.fnal.gov:24136/pnfs/fnal.gov/usr/cms/WAX/11/store/user/guofan/JetMET/ttbsm_383/ff90c3c4588c16ad10031564667fd507/ttbsm_381_35_1_aIW.root'
#'dcap://cmsdca.fnal.gov:24136/pnfs/fnal.gov/usr/cms/WAX/11/store/user/guofan/Jet/ttbsm_383/ff90c3c4588c16ad10031564667fd507/ttbsm_381_46_1_Zyr.root'
                            #),
                            fileNames = readFiles,
                           
                          eventsToProcess = cms.untracked.VEventRange('144086:105549435','144089:867525359',
                          '146644:980046801')
                          #eventsToSkip = cms.untracked.VEventRange('1:1-1:6','2:100-3:max'),
                          #lumisToProcess = cms.untracked.VLuminosityBlockRange('1:1-1:6','2:100-3:max'),
                          #lumisToSkip = cms.untracked.VLuminosityBlockRange('1:1-1:6','2:100-3:max'),

  )  


process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('2events_reco.root'),
    outputCommands = cms.untracked.vstring('keep *')

)

process.outpath = cms.EndPath(process.out)

readFiles.extend( [
       '/store/data/Run2010A/JetMET/RECO/Sep17ReReco_v2/0025/FEC9D4BA-1DC7-DF11-AB87-001A928116D8.root',
       '/store/data/Run2010A/JetMET/RECO/Sep17ReReco_v2/0025/FEBEB3B9-1DC7-DF11-86D1-003048678C9A.root' ] )

