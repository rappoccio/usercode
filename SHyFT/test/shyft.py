# SHyFT configuration
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *

## global tag for data
process.GlobalTag.globaltag = cms.string('START36_V9::All')

# add the flavor history
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi")

 
# get the 7 TeV jet corrections
from PhysicsTools.PatAlgos.tools.jetTools import *
switchJECSet( process, "Spring10")

# require physics declared
process.load('HLTrigger.special.hltPhysicsDeclared_cfi')
process.hltPhysicsDeclared.L1GtReadoutRecordTag = 'gtDigis'

# require scraping filter
process.scrapingVeto = cms.EDFilter("FilterOutScraping",
                                    applyfilter = cms.untracked.bool(True),
                                    debugOn = cms.untracked.bool(False),
                                    numtrack = cms.untracked.uint32(10),
                                    thresh = cms.untracked.double(0.2)
                                    )

# Run b-tagging and ak5 genjets sequences on 35x inputs
from PhysicsTools.PatAlgos.tools.cmsswVersionTools import *
run36xOn35xInput( process, "ak5GenJets")


# switch on PAT trigger
from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
switchOnTrigger( process )

# switch to 8e29 menu. Note this is needed to match SD production
process.patTriggerEvent.processName = cms.string( 'REDIGI' )
process.patTrigger.processName = cms.string( 'REDIGI' )


process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
                                           vertexCollection = cms.InputTag('offlinePrimaryVertices'),
                                           minimumNDOF = cms.uint32(4) ,
                                           maxAbsZ = cms.double(15), 
                                           maxd0 = cms.double(2) 
                                           )


from PhysicsTools.PatAlgos.tools.pfTools import *
postfix = "PFlow"
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC=False, postfix=postfix) 

# turn to false when running on data
getattr(process, "patElectrons"+postfix).embedGenMatch = False
getattr(process, "patMuons"+postfix).embedGenMatch = False


# Selection
process.selectedPatJetsPFlow.cut = cms.string("pt > 15")
process.selectedPatJets.cut = cms.string("pt > 20")
process.patJets.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfos")
    )
process.patJetsPFlow.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfos")
    )
process.selectedPatMuons.cut = cms.string("pt > 3")
process.selectedPatMuonsPFlow.cut = cms.string("pt > 3")
process.patMuons.usePV = False
process.patMuonsPFlow.usePV = False
process.selectedPatElectrons.cut = cms.string("pt > 3")
process.selectedPatElectronsPFlow.cut = cms.string("pt > 3")

# remove trigger matching for PF2PAT as that is currently broken
process.patPF2PATSequencePFlow.remove(process.patTriggerSequencePFlow)
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


# FILTERS:
# One of : >=1 mu (PF or std)
#          >=1 e (PF or std)
#          >=2 jet (PF or std)
process.muonFilter = cms.EDFilter("CandViewCountFilter",
                                  src = cms.InputTag("selectedPatMuons"),
                                  minNumber = cms.uint32(1),
                                  )

process.pfMuonFilter = cms.EDFilter("CandViewCountFilter",
                                    src = cms.InputTag("selectedPatMuonsPFlow"),
                                    minNumber = cms.uint32(1),
                                    )

process.electronFilter = cms.EDFilter("CandViewCountFilter",
                                  src = cms.InputTag("selectedPatElectrons"),
                                  minNumber = cms.uint32(1),
                                  )

process.pfElectronFilter = cms.EDFilter("CandViewCountFilter",
                                    src = cms.InputTag("selectedPatElectronsPFlow"),
                                    minNumber = cms.uint32(1),
                                    )

process.jetFilter = cms.EDFilter("CandViewCountFilter",
                                  src = cms.InputTag("selectedPatJets"),
                                  minNumber = cms.uint32(2),
                                  )

process.pfJetFilter = cms.EDFilter("CandViewCountFilter",
                                    src = cms.InputTag("selectedPatJetsPFlow"),
                                    minNumber = cms.uint32(2),
                                    )



####################
# make some quick-access shallow clones for speeding up read access

process.jetClones = cms.EDProducer("CandViewShallowCloneProducer",
                                   src = cms.InputTag('selectedPatJets'),
                                   cut = cms.string('pt > 20 & abs(eta) < 3')
                                   )

process.pfjetClones = cms.EDProducer("CandViewShallowCloneProducer",
                                   src = cms.InputTag('selectedPatJetsPFlow'),
                                   cut = cms.string('pt > 15 & abs(eta) < 3')
                                   )


# Add the files 
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()

readFiles.extend( [
'/store/mc/Summer09/TTbarJets-madgraph/GEN-SIM-RECO/MC_31X_V3_7TeV-v5/0003/FE166634-2D33-DF11-977F-0030487D814B.root',
'/store/mc/Summer09/TTbarJets-madgraph/GEN-SIM-RECO/MC_31X_V3_7TeV-v5/0003/FCB9EE61-3D35-DF11-A1F6-003048C693D0.root',
'/store/mc/Summer09/TTbarJets-madgraph/GEN-SIM-RECO/MC_31X_V3_7TeV-v5/0003/FC5A46B8-FA32-DF11-8315-003048D3C7DC.root',
'/store/mc/Summer09/TTbarJets-madgraph/GEN-SIM-RECO/MC_31X_V3_7TeV-v5/0003/FC16B513-5B33-DF11-95AE-0030487F1A4F.root',
'/store/mc/Summer09/TTbarJets-madgraph/GEN-SIM-RECO/MC_31X_V3_7TeV-v5/0003/FAD09139-2D33-DF11-91E6-003048D436EA.root',
'/store/mc/Summer09/TTbarJets-madgraph/GEN-SIM-RECO/MC_31X_V3_7TeV-v5/0003/FA653160-4A33-DF11-906E-0030487F1F23.root',
'/store/mc/Summer09/TTbarJets-madgraph/GEN-SIM-RECO/MC_31X_V3_7TeV-v5/0003/F8A6CF18-E732-DF11-AD4B-003048C693EE.root',
'/store/mc/Summer09/TTbarJets-madgraph/GEN-SIM-RECO/MC_31X_V3_7TeV-v5/0003/F88CA7EA-0B33-DF11-8E59-003048D4363C.root',
'/store/mc/Summer09/TTbarJets-madgraph/GEN-SIM-RECO/MC_31X_V3_7TeV-v5/0003/F8745C50-D732-DF11-94CB-0030487D8633.root',
'/store/mc/Summer09/TTbarJets-madgraph/GEN-SIM-RECO/MC_31X_V3_7TeV-v5/0003/F84EC46F-E432-DF11-9C47-003048D436D2.root'

        ] );
process.source.fileNames = readFiles


# let it run

#print
#print "============== Warning =============="
#print "technical trigger filter:    DISABLED"
#print "physics declare bit filter:  DISABLED"
#print "primary vertex filter:       DISABLED"

process.patseq = cms.Sequence(
    process.makeGenEvt *
    process.scrapingVeto*
    process.primaryVertexFilter*
    process.patDefaultSequence* 
    getattr(process,"patPF2PATSequence"+postfix)*
    process.jetClones * 
    process.pfjetClones *
    process.flavorHistorySeq *
    process.prunedGenParticles 
)

process.p1 = cms.Path(
    process.patseq*process.muonFilter
    )

process.p2 = cms.Path(
    process.patseq*process.pfMuonFilter
    )

process.p3 = cms.Path(
    process.patseq*process.electronFilter
    )

process.p4 = cms.Path(
    process.patseq*process.pfElectronFilter
    )

process.p5 = cms.Path(
    process.patseq*process.jetFilter
    )

process.p6 = cms.Path(
    process.patseq*process.pfJetFilter
    )

# "or" the preceeding paths
process.out.SelectEvents.SelectEvents = cms.vstring('p1', 'p2', 'p3', 'p4', 'p5', 'p6')


# rename output file
process.out.fileName = cms.untracked.string('shyft_361_pat.root')

# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

# process all the events
process.maxEvents.input = 1000
process.options.wantSummary = True
process.out.dropMetaData = cms.untracked.string("DROPPED")

from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoCleaning
from PhysicsTools.PatAlgos.patEventContent_cff import patExtraAodEventContent
from PhysicsTools.PatAlgos.patEventContent_cff import patTriggerEventContent
#process.out.outputCommands = patEventContentNoCleaning
#process.out.outputCommands += patExtraAodEventContent
#process.out.outputCommands += patTriggerEventContent
process.out.outputCommands = [
    'keep *_flavorHistoryFilter_*_*',
    'keep *_prunedGenParticles_*_*',
    'keep *_decaySubset_*_*',
    'keep *_initSubset_*_*',
    'drop *_cleanPat*_*_*',
    'keep *_selectedPat*_*_*',
    'keep *_patMETs*_*_*',
    'keep recoPFCandidates_particleFlow_*_*',
    'keep *_offlineBeamSpot_*_*',
    'keep *_offlinePrimaryVertices_*_*',
    'keep recoTracks_generalTracks_*_*',
    'drop patPFParticles_*_*_*',
    'keep patTriggerObjects_patTrigger_*_*',
    'keep patTriggerFilters_patTrigger_*_*',
    'keep patTriggerPaths_patTrigger_*_*',
    'keep patTriggerEvent_patTriggerEvent_*_*',
    'keep *_cleanPatPhotonsTriggerMatch_*_*',
    'keep *_cleanPatElectronsTriggerMatch_*_*',
    'keep *_cleanPatMuonsTriggerMatch_*_*',
    'keep *_cleanPatTausTriggerMatch_*_*',
    'keep *_cleanPatJetsTriggerMatch_*_*',
    'keep *_patMETsTriggerMatch_*_*',
    'drop *_MEtoEDMConverter_*_*',
    'keep *_*jetClones_*_*'
    ]

