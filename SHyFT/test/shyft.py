# The SHyFT Configuration for PAT-tuples

# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

# load the standard PAT config 
process.load("PhysicsTools.PatAlgos.patSequences_cff")

process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

# add the flavor history
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi")

		 # shrink the event content
# jets
#_____ SELECTION ________________________________________________ 	 
#
process.selectedPatJets.cut = cms.string("pt > 15 & abs(eta) < 3")
process.patJets.embedGenJetMatch = cms.bool(False)
# electrons
process.selectedPatElectrons.cut = cms.string('pt > 3. & abs(eta) < 2.5')
process.patElectrons.isoDeposits = cms.PSet()
# muons
process.selectedPatMuons.cut = cms.string("pt > 3 & abs(eta) < 2.1")
process.patMuons.isoDeposits = cms.PSet()
# photons
process.patPhotons.isoDeposits = cms.PSet()
#taus
process.patTaus.isoDeposits = cms.PSet()

#-- Tuning of Monte Carlo matching --------------------------------------------
# Also match with leptons of opposite charge
process.electronMatch.checkCharge = False
process.muonMatch.checkCharge = False

## produce ttGenEvent
process.load("TopQuarkAnalysis.TopEventProducers.sequences.ttGenEvent_cff")

# prune gen particles

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")


process.prunedGenParticles = cms.EDProducer("GenParticlePruner",
  src = cms.InputTag("genParticles"),
  select = cms.vstring(
  "drop  *",
  "keep status = 3", #keeps all particles from the hard matrix element
  "+keep (abs(pdgId) = 11 | abs(pdgId) = 13) & status = 1" #keeps all stable muons and electrons and their (direct) mothers.
  )
)

# re-run the gen jets
from PhysicsTools.PatAlgos.tools.cmsswVersionTools import *
run33xOnReRecoMC( process,
                  genJets = "ak5GenJets",
                  postfix="")



######################
# begin changes for PF

# add the trigger information to the configuration
from PhysicsTools.PatAlgos.tools.trigTools import *
switchOnTrigger( process )
from PhysicsTools.PatAlgos.patEventContent_cff import patTriggerEventContent

# switch to 8e29 menu. Note this is needed to match SD production
#process.patTriggerEvent.processName = cms.string( 'HLT8E29' )
#process.patTrigger.processName = cms.string( 'HLT8E29' )

#try to clone what we have up to here.  
from PhysicsTools.PatAlgos.tools.helpers import cloneProcessingSnippet
cloneProcessingSnippet(process, process.patDefaultSequence, "Std")

# add PF2PAT
from PhysicsTools.PatAlgos.tools.pfTools import *
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5')

# remove trigger matching for PF2PAT as that is currently broken
process.patDefaultSequence.remove(process.patTriggerSequence)

# end changes for PF
####################

# let it run
process.p = cms.Path(
 process.makeGenEvt *
 process.patDefaultSequenceStd *
 process.patDefaultSequence*
 process.flavorHistorySeq *
 process.prunedGenParticles
 )


process.source.fileNames = [
    'file:/uscms_data/d1/rappocc/SHyFT/files/84F29E99-202C-DF11-810C-00237DA14F92.root'
#'/store/relval/CMSSW_3_5_4/RelValTTbar/GEN-SIM-RECO/START3X_V24-v1/0003/0060E652-822B-DF11-BA47-002618943972.root'
  ]
process.maxEvents.input = 1000         ##  (e.g. -1 to run on all events)

process.out.outputCommands += ['drop *_cleanPat*_*_*',
			       'keep *_flavorHistoryFilter_*_*',
                               'keep *_prunedGenParticles_*_*',
                               'keep *_selectedPat*_*_*',
			       'keep *_decaySubset_*_*',
			       'keep *_initSubset_*_*',
			       'keep *_offlineBeamSpot_*_*',
			       'keep *_offlinePrimaryVertices_*_*',
                               'keep recoTracks_generalTracks_*_*',
                               'drop patPFParticles_*_*_*',
                               'keep patTriggerObjects_patTriggerStd_*_*',
                               'keep patTriggerFilters_patTriggerStd_*_*',
                               'keep patTriggerPaths_patTriggerStd_*_*',
                               'keep patTriggerEvent_patTriggerEventStd_*_*',
                               'keep *_cleanPatPhotonsTriggerMatchStd_*_*',
                               'keep *_cleanPatElectronsTriggerMatchStd_*_*',
                               'keep *_cleanPatMuonsTriggerMatchStd_*_*',
                               'keep *_cleanPatTausTriggerMatchStd_*_*',
                               'keep *_cleanPatJetsTriggerMatchStd_*_*',
                               'keep *_patMETsTriggerMatchStd_*_*'
]
process.out.dropMetaData = cms.untracked.string("DROPPED")
process.out.fileName = 'ljmet.root'
process.options.wantSummary = True
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
