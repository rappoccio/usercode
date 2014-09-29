import FWCore.ParameterSet.Config as cms

process = cms.Process("FWTEST")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        '/store/relval/CMSSW_3_5_0_pre2/RelValTTbar/GEN-SIM-RECO/MC_3XY_V14-v1/0009/96EA134F-85ED-DE11-859A-002618943956.root'
    )
)

process.fwtest = cms.EDProducer('FWTest',
                                         caloSrc = cms.InputTag("ak5CaloJets"),
                                         pfSrc = cms.InputTag("ak5PFJets"),
)


process.viewtest = cms.EDAnalyzer('ViewTest',
                                  jetSrc = cms.InputTag("fwtest")
)


process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('myOutputFile.root'),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
                               outputCommands = cms.untracked.vstring('keep *_fwtest_*_*')  
)

  
process.p = cms.Path(process.fwtest*process.viewtest)

process.e = cms.EndPath(process.out)
