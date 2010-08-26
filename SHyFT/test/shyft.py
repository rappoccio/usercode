# SHyFT configuration
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *


useData = True
use35x = False

## global tag for data
if useData :
    process.GlobalTag.globaltag = cms.string('GR_R_38X_V9::All')
else :
    process.GlobalTag.globaltag = cms.string('START38_V9::All')

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
if use35x :
    if useData :
        run36xOn35Input( process )
    else :
        run36xOn35xInput( process, "ak5GenJets")



# switch on PAT trigger
from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
switchOnTrigger( process )

# switch to 8e29 menu. Note this is needed to match SD production
if useData == False :
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
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC= not useData, postfix=postfix) 



# turn to false when running on data
if useData :
    getattr(process, "patElectrons"+postfix).embedGenMatch = False
    getattr(process, "patMuons"+postfix).embedGenMatch = False
    removeMCMatching(process, ['All'])

# Selection
process.selectedPatJetsPFlow.cut = cms.string('pt > 10 & abs(eta) < 2.4')
process.selectedPatJets.cut = cms.string('pt > 20 & abs(eta) < 2.4')

#process.selectedPatJetsPFlow.cut = cms.string('pt > 15 & abs(eta) < 2.4 &'
#                                              'chargedHadronEnergyFraction() > 0.0 & '
#                                              '(neutralHadronEnergy() + HFHadronEnergy()) < 0.99 & '
#                                              'chargedEmEnergyFraction() < 0.99 & '
#                                              'neutralEmEnergyFraction() < 0.99 & '
#                                              'chargedMultiplicity() > 0 &'
#                                              'numberOfDaughters() > 1 ')
#process.selectedPatJets.cut = cms.string('pt > 20 & abs(eta) < 2.4 &'
#                                         'emEnergyFraction() > 0.01 &'
#                                         'jetID().n90Hits > 1 &'
#                                         'jetID().fHPD < 0.98')
process.patJets.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfos")
    )
process.patJetsPFlow.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAOD")
    )
process.selectedPatMuons.cut = cms.string("pt > 3")
process.selectedPatMuonsPFlow.cut = cms.string("pt > 3")
process.patMuons.usePV = False
process.patMuonsPFlow.usePV = False
process.selectedPatElectrons.cut = cms.string("pt > 3")
process.selectedPatElectronsPFlow.cut = cms.string("pt > 3")
process.patElectrons.usePV = False
process.patElectronsPFlow.usePV = False

#process.patJets.userData.userFunctions = cms.vstring( "? tagInfoSecondaryVertex('secondaryVertex') != void ? "
#                                                      "tagInfoSecondaryVertex('secondaryVertex').secondaryVertex(0).p4().mass() : 0")
#process.patJets.userData.userFunctionLabels = cms.vstring('secvtxMass')

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

process.goodCaloJets = cms.EDFilter("CandViewShallowCloneProducer",
                                   src = cms.InputTag('selectedPatJets'),
                                   cut = cms.string('pt > 20 & abs(eta) < 2.4')
                                   )

process.goodPFJets = cms.EDFilter("CandViewShallowCloneProducer",
                                   src = cms.InputTag('selectedPatJetsPFlow'),
                                   cut = cms.string('pt > 10 & abs(eta) < 2.4')
                                   )


# Add the files 
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()

if useData :
    readFiles.extend( [
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0160/9CF95657-2E98-DF11-AD1B-0017A4770C2C.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0160/4C8C296F-2E98-DF11-8009-0017A477082C.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0159/A6CBE127-2E98-DF11-88BB-0017A477083C.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0159/989FEAAD-2E98-DF11-B111-0017A4770C2C.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0159/8296D8FD-2D98-DF11-B1F4-00237DA13C16.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0159/784926DF-2D98-DF11-8A14-001E0B471C92.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0159/5C1EEC96-2E98-DF11-870B-0017A4771024.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0159/4A41F991-2E98-DF11-AEC3-0017A477100C.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0158/EC8712FE-F797-DF11-B69A-0017A4770C3C.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0158/EA2FA044-FB97-DF11-AB67-0017A4771008.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0158/DE11BA4C-F997-DF11-9BBA-0017A4770C08.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0158/CCDDA631-FA97-DF11-8BAE-0017A4771008.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0158/B0ACA57B-F997-DF11-9A9D-0017A4770C28.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0158/7C8EDD97-FC97-DF11-AE40-0017A4770C1C.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0158/62C95FEC-FF97-DF11-97A5-0017A4770C2C.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0158/38CAB533-FA97-DF11-802A-0017A477081C.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/F83A0240-AD97-DF11-BF65-001E0B48E92A.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/EE19768C-B397-DF11-8980-0017A4770820.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/DCF1D923-B197-DF11-A86D-002481A60370.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/DC20688E-B197-DF11-B56C-0017A4770C28.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/D6A37406-BA97-DF11-ACEE-0017A4770C28.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/D6A0488B-C397-DF11-AEC4-0017A477080C.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/D25E50CD-B597-DF11-84D3-0017A4770C2C.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/C80654AB-8697-DF11-8335-00237DA15C66.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/C444FA8D-C397-DF11-85D4-0017A4770400.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/C2438902-B497-DF11-8241-0017A4770434.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/BA541A4A-9197-DF11-96B2-0017A4771034.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/BA51862D-AE97-DF11-B74C-0017A4770C28.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/B44D958C-B397-DF11-8995-0017A4770C08.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/AE698DAD-C597-DF11-AAE9-001E0B48E92A.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/ACCBDA28-C097-DF11-A93B-0017A4771030.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/9E4661D3-B397-DF11-8D04-0017A4770830.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/9CA6F4C6-B597-DF11-9090-001E0B476CB8.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/9C654480-B197-DF11-A0B6-0017A477100C.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/9A906381-B397-DF11-8489-0017A477100C.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/943DFF7E-C397-DF11-BB3B-001E0B48E92A.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/8E2A6DC1-B897-DF11-A22D-0017A4771030.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/8C7960C7-C297-DF11-9164-0017A4770C28.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/8C0F6A34-B197-DF11-8D6A-0017A477102C.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/6CC8F31C-B097-DF11-A964-0017A4770C2C.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/6877ED8F-C597-DF11-9F09-0017A4770420.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/64E8FD8D-B397-DF11-A5F6-0017A477083C.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/6044B94A-B697-DF11-8A2B-0017A4770424.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/5C28C196-C397-DF11-A083-0017A4770404.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/505E0F0B-C397-DF11-96A2-00237DA24DE0.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/3CF9C0AF-B897-DF11-90F1-0017A477100C.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/3CE4BA4F-B697-DF11-A295-0017A4771004.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/3CA430EF-BD97-DF11-93FE-0017A4770800.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/2EC17D81-B197-DF11-B3D5-0017A4770C0C.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/22E67103-B497-DF11-94CA-0017A4770800.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/1E66E778-B197-DF11-9AAF-0017A4770C28.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/108B9680-C097-DF11-AA1A-0017A477100C.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/0AC80A6D-B597-DF11-ABB6-0017A4771008.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0157/0A111481-B397-DF11-B8EB-0017A477080C.root',
'/store/data/Run2010A/Mu/RECO/Jul23ReReco_PreProd_v1/0156/5E455BE7-7897-DF11-94D9-0022649C40A8.root'

        ] );
else : 
    readFiles.extend( [
        '/store/mc/Spring10/TTbarJets-madgraph/GEN-SIM-RECO/START3X_V26_S09-v1/0005/B8E00316-AD46-DF11-A92F-0030487D5EBD.root',
        '/store/mc/Spring10/TTbarJets-madgraph/GEN-SIM-RECO/START3X_V26_S09-v1/0005/B8558647-9D46-DF11-AD71-003048D3CA06.root',
        '/store/mc/Spring10/TTbarJets-madgraph/GEN-SIM-RECO/START3X_V26_S09-v1/0005/B8499034-A346-DF11-B3C5-00304889D562.root',
        '/store/mc/Spring10/TTbarJets-madgraph/GEN-SIM-RECO/START3X_V26_S09-v1/0005/B833FD14-9946-DF11-9D0C-0030487F1BCF.root'        
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
    process.goodCaloJets * 
    process.goodPFJets *
    process.flavorHistorySeq *
    process.prunedGenParticles 
)

if useData :
    process.patseq.remove( process.makeGenEvt )
    process.patseq.remove( process.flavorHistorySeq )
    process.patseq.remove( process.prunedGenParticles )

process.p1 = cms.Path(
    process.patseq
    )

process.out.SelectEvents.SelectEvents = cms.vstring('p1')


# rename output file
process.out.fileName = cms.untracked.string('shyft_382_pat.root')

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
    'keep *_*goodCaloJets_*_*',
    'keep *_*goodPFJets_*_*'
    ]

