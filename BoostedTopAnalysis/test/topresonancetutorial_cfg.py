import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        'file:/uscms/home/jdolen/nobackup/BoostedTop533/exampleB2GPAT_ZPrimeToTTJets_M1000GeV_W10GeV_TuneZ2star_8TeV-madgraph-tauola/12BA2820-6F15-E211-8AE9-003048678F6C.root'
    )
)

process.TFileService = cms.Service("TFileService",
      fileName = cms.string("histo.root"),
      closeFileFast = cms.untracked.bool(True)
  )


process.demo = cms.EDAnalyzer('TopResonanceTutorial'
)


process.p = cms.Path(process.demo)
