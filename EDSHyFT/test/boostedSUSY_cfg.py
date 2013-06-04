import FWCore.ParameterSet.Config as cms

process = cms.Process("SUSYGenP4")


process.load("FWCore.MessageService.MessageLogger_cfi")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.MessageLogger.cerr.FwkJob.limit=1
process.MessageLogger.cerr.ERROR = cms.untracked.PSet( limit = cms.untracked.int32(0) )

###############################
####### Parameters ############
############################### 
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')
options.register ('runOnT1t1t',
                  1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run on gg->4tchi0chi0 sample")

options.register ('runOnT1ttcc',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run on gg->ttccchi0chi0")

options.parseArguments()            
                                    
print options

readFiles = cms.untracked.vstring()

if options.runOnT1t1t:
    readFiles.extend( [
         'file:/uscms_data/d2/skhalil/BPrimeBoost/CMSSW_5_3_3/src/TopQuarkAnalysis/TopPairBSM/test/tlbsm_53x_v2_mc.root',
         #'/store/mc/Summer12/SMS-MadGraph_Pythia6Zstar_8TeV_T1t1t_2J_mGo-1000_mStop-200to750_mLSP-100to650_25GeVX25GeV_Binning/AODSIM/START52_V9_FSIM-v1/30001/FEE0969A-A691-E211-B21C-003048322CD8.r
        ]);
    
elif options.runOnT1ttcc:
    readFiles.extend( [

        ]);
    


if len(options.inputFiles) == 0 :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(readFiles),
                                )
else:
    filelist = []
    with open( options.inputFiles[0], 'r' ) as input_:
        for line in input_:
            filelist.append(line.strip())
            
        print 'filelist', filelist
        process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(filelist)
                                    )
        
process.SUSYGenP4 = cms.EDProducer('BoostedSusy')
                                         
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.printTree = cms.EDAnalyzer("ParticleTreeDrawer",
                                   src = cms.InputTag("prunedGenParticles"),
                                   printP4 = cms.untracked.bool(False),
                                   printPtEtaPhi = cms.untracked.bool(False),
                                   printVertex = cms.untracked.bool(False),
                                   printStatus = cms.untracked.bool(False),
                                   printIndex = cms.untracked.bool(False),
                                   status = cms.untracked.vint32( 3 )
                                   )

process.printList = cms.EDAnalyzer("ParticleListDrawer",
  maxEventsToPrint = cms.untracked.int32(10),
  printVertex = cms.untracked.bool(False),
  src = cms.InputTag("prunedGenParticles")
)

process.p = cms.Path(process.SUSYGenP4 * process.printTree * process.printList)

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('genOutputFile.root'),
                               outputCommands = cms.untracked.vstring('drop *',
                                                                      'keep *_SUSYGenP4*_*_*',)
                               )

process.e = cms.EndPath(process.out)
