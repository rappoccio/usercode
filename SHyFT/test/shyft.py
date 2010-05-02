# The SHyFT Configuration for PAT-tuples

# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

# load the standard PAT config 
process.load("PhysicsTools.PatAlgos.patSequences_cff")

process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

# add the flavor history
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi")

from PhysicsTools.PatAlgos.tools.jetTools import *
switchJECSet( process, "Summer09_7TeV_ReReco332")


		 # shrink the event content
# jets
#_____ SELECTION ________________________________________________ 	 
#
process.selectedPatJets.cut = cms.string("pt > 20 & abs(eta) < 3")
process.patJets.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfos")
    )
# electrons
#process.selectedPatElectrons.cut = cms.string('pt > 3. & abs(eta) < 2.5')
process.patElectrons.isoDeposits = cms.PSet()
# muons
#process.selectedPatMuons.cut = cms.string("pt > 3 & abs(eta) < 2.1")
process.patMuons.isoDeposits = cms.PSet()
# taus
process.selectedPatTaus.cut = cms.string("pt > 20 & abs(eta) < 3")
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
process.patTriggerEvent.processName = cms.string( 'HLT8E29' )
process.patTrigger.processName = cms.string( 'HLT8E29' )

#try to clone what we have up to here.  
from PhysicsTools.PatAlgos.tools.helpers import cloneProcessingSnippet
cloneProcessingSnippet(process, process.patDefaultSequence, "Std")

# add PF2PAT
from PhysicsTools.PatAlgos.tools.pfTools import *
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5')

# remove trigger matching for PF2PAT as that is currently broken
process.patDefaultSequence.remove(process.patTriggerSequence)

# now change the PF jet cut to 10 GeV
process.selectedPatJets.cut = cms.string("pt > 15 & abs(eta) < 3")

# end changes for PF
####################

####################
# make some quick-access shallow clones for speeding up read access

process.stdjetClones = cms.EDProducer("CandViewShallowCloneProducer",
                                   src = cms.InputTag('selectedPatJetsStd'),
                                   cut = cms.string('pt > 20 & abs(eta) < 3')
                                   )

process.jetClones = cms.EDProducer("CandViewShallowCloneProducer",
                                   src = cms.InputTag('selectedPatJets'),
                                   cut = cms.string('pt > 15 & abs(eta) < 3')
                                   )


# let it run
process.p = cms.Path(
 process.makeGenEvt *
 process.patDefaultSequenceStd* 
 process.patDefaultSequence*
 process.flavorHistorySeq *
 process.prunedGenParticles * 
 process.stdjetClones * 
 process.jetClones
 )


process.source.fileNames = [
#        '/store/mc/Summer09/TTbar/GEN-SIM-RECO/MC_3XY_V25_preproduction-v1/0003/84F29E99-202C-DF11-810C-00237DA14F92.root',
#        '/store/mc/Summer09/TTbar/GEN-SIM-RECO/MC_3XY_V25_preproduction-v1/0002/F8535A25-E12B-DF11-AE17-0017A4770408.root',
#        '/store/mc/Summer09/TTbar/GEN-SIM-RECO/MC_3XY_V25_preproduction-v1/0002/D8B78A2E-E12B-DF11-AD04-0017A4770830.root',
#        '/store/mc/Summer09/TTbar/GEN-SIM-RECO/MC_3XY_V25_preproduction-v1/0002/AC26FFDB-E02B-DF11-9FAE-0017A4770808.root',
#        '/store/mc/Summer09/TTbar/GEN-SIM-RECO/MC_3XY_V25_preproduction-v1/0002/8A343E2E-E12B-DF11-9AB8-0017A4770420.root',
#        '/store/mc/Summer09/TTbar/GEN-SIM-RECO/MC_3XY_V25_preproduction-v1/0002/5AC0F529-E12B-DF11-8908-0017A4770438.root',
#        '/store/mc/Summer09/TTbar/GEN-SIM-RECO/MC_3XY_V25_preproduction-v1/0002/4E1AEE29-E12B-DF11-A64A-0017A4770810.root',
#        '/store/mc/Summer09/TTbar/GEN-SIM-RECO/MC_3XY_V25_preproduction-v1/0002/4AAE5D25-E12B-DF11-ADC6-0017A4770834.root'
    'file:/uscms_data/d1/rappocc/SHyFT/files/84F29E99-202C-DF11-810C-00237DA14F92.root'
#'/store/relval/CMSSW_3_5_4/RelValTTbar/GEN-SIM-RECO/START3X_V24-v1/0003/0060E652-822B-DF11-BA47-002618943972.root'
  ]
process.maxEvents.input = 100        ##  (e.g. -1 to run on all events)

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
                               'keep *_patMETsTriggerMatchStd_*_*',
                               'keep *_*jetClones_*_*',
]
process.out.dropMetaData = cms.untracked.string("DROPPED")
process.out.fileName = 'ljmet.root'
process.options.wantSummary = True
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
