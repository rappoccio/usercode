# SHyFT configuration
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *


###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('useData',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run this on real data")

options.register ('use35x',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run on samples produced with <= 35x")

options.register ('use38x',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run on samples produced with >= 38x")


options.register ('useWJetsFilter',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Select events with the W+jets selector")


options.register ('useTrigger',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Select events with the HLT_Mu9 trigger only")
                  
options.register ('muonIdIgnoredCuts',
                  [],
                  VarParsing.multiplicity.list,
                  VarParsing.varType.string,
                  "Cuts to ignore for tight muon definition")
                  
options.parseArguments()

print options

import sys

# Set to true for running on data
useData = options.useData
# Set to true to run on < 36x samples
use35x = options.use35x
# run the W+Jets selector filter
useWJetsFilter = options.useWJetsFilter
# check the trigger
useTrigger = options.useTrigger

## global tag for data
if useData :
    process.GlobalTag.globaltag = cms.string('GR_R_38X_V9::All')
else :
    process.GlobalTag.globaltag = cms.string('START38_V9::All')


# require HLT_Mu9 trigger
from HLTrigger.HLTfilters.hltHighLevel_cfi import *
if useData == True :
    if useTrigger :
        process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::HLT", HLTPaths = ["HLT_Mu9"])
    else :
        process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::HLT", HLTPaths = ["*"])
else :
    if useTrigger :
        process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::REDIGI", HLTPaths = ["HLT_Mu9"])
    else :
        process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::REDIGI", HLTPaths = ["*"])


# HB + HE noise filtering
process.load('CommonTools/RecoAlgos/HBHENoiseFilter_cfi')

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
if useData == False and options.use38x == False :
    process.patTriggerEvent.processName = cms.string( 'REDIGI' )
    process.patTrigger.processName = cms.string( 'REDIGI' )


process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
                                           vertexCollection = cms.InputTag('offlinePrimaryVertices'),
                                           minimumNDOF = cms.uint32(4) ,
                                           maxAbsZ = cms.double(24.0), 
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


# tcMET
from PhysicsTools.PatAlgos.tools.metTools import *
addTcMET(process, 'TC')

# JPT
process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
process.load('RecoJets.Configuration.RecoJPTJets_cff')

addJetCollection(process,cms.InputTag('JetPlusTrackZSPCorJetAntiKt5'),
                 'AK5', 'JPT',
                 doJTA        = True,
                 doBTagging   = True,
                 jetCorrLabel = ('AK5','JPT'),
                 doType1MET   = False,
                 doL1Cleaning = False,
                 doL1Counters = False,                 
                 genJetCollection = cms.InputTag("ak5GenJets"),
                 doJetID      = True,
                 jetIdLabel   = "ak5"
                 )


# Selection
process.selectedPatJetsPFlow.cut = cms.string('pt > 15 & abs(eta) < 2.4')
process.selectedPatJetsAK5JPT.cut = cms.string('pt > 15 & abs(eta) < 2.4')
process.selectedPatJets.cut = cms.string('pt > 20 & abs(eta) < 2.4')
process.patJets.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfos")
    )
process.patJetsPFlow.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAOD")
    )
process.patJetsAK5JPT.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAK5JPT")
    )

if len(options.muonIdIgnoredCuts) > 0 :
    print '------ SWITCHING PF Muons to use non-PF-isolated muons, we are ignoring cuts ----------'
    process.patMuonsPFlow.pfMuonSource = 'pfAllMuonsPFlow'
    process.patMuonsPFlow.isoDeposits = cms.PSet()
    process.patMuonsPFlow.isolationValues = cms.PSet()
    print 'For PAT PF Muons: '
    print process.patMuonsPFlow.pfMuonSource

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


# Add the files 
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()

if useData :
    readFiles.extend( [
        '/store/data/Run2010B/Mu/RECO/PromptReco-v2/000/146/511/0E57A1DF-A7C7-DF11-B2E1-003048F1C836.root',
        '/store/data/Run2010B/Mu/RECO/PromptReco-v2/000/146/510/F8CFD025-7AC7-DF11-970C-001617C3B76A.root',
        '/store/data/Run2010B/Mu/RECO/PromptReco-v2/000/146/510/D4C82E6A-85C7-DF11-8B24-0019B9F709A4.root',
        '/store/data/Run2010B/Mu/RECO/PromptReco-v2/000/146/510/B01897AD-7BC7-DF11-A16B-001D09F241F0.root',
        '/store/data/Run2010B/Mu/RECO/PromptReco-v2/000/146/510/ACFB1223-8DC7-DF11-9D6D-001D09F232B9.root',
        '/store/data/Run2010B/Mu/RECO/PromptReco-v2/000/146/510/72745CEC-81C7-DF11-B136-0030487A1990.root',
        '/store/data/Run2010B/Mu/RECO/PromptReco-v2/000/146/510/5895BD1D-7FC7-DF11-B488-0030487C635A.root',
        '/store/data/Run2010B/Mu/RECO/PromptReco-v2/000/146/510/4C8075C0-86C7-DF11-AB7A-0030487C635A.root',
        '/store/data/Run2010B/Mu/RECO/PromptReco-v2/000/146/510/24A944A4-7DC7-DF11-B7C2-003048D373AE.root',
        '/store/data/Run2010B/Mu/RECO/PromptReco-v2/000/146/510/22CC2E69-85C7-DF11-8C63-001D09F2B30B.root',
        '/store/data/Run2010B/Mu/RECO/PromptReco-v2/000/146/510/0A2B7AA7-7DC7-DF11-A0EB-003048D2BE12.root',
        '/store/data/Run2010B/Mu/RECO/PromptReco-v2/000/146/509/62C11A97-45C7-DF11-BBB7-001D09F241F0.root',
        '/store/data/Run2010B/Mu/RECO/PromptReco-v2/000/146/506/8AA215A3-4EC7-DF11-8999-003048F118DE.root',
        '/store/data/Run2010B/Mu/RECO/PromptReco-v2/000/146/445/BCA934AE-FAC6-DF11-9143-003048F024FA.root',
        '/store/data/Run2010B/Mu/RECO/PromptReco-v2/000/146/442/289F629E-F3C6-DF11-BB6E-001D09F231B0.root',
        '/store/data/Run2010B/Mu/RECO/PromptReco-v2/000/146/440/AE467D73-E5C6-DF11-91E6-003048F01E88.root',
        '/store/data/Run2010B/Mu/RECO/PromptReco-v2/000/146/438/DE0A4969-D5C6-DF11-9DA2-003048F024DE.root',
        '/store/data/Run2010B/Mu/RECO/PromptReco-v2/000/146/437/D0C578A5-E4C6-DF11-837B-0030487CD7B4.root',
        '/store/data/Run2010B/Mu/RECO/PromptReco-v2/000/146/437/A660F145-F6C6-DF11-A67F-001D09F2516D.root',
        '/store/data/Run2010B/Mu/RECO/PromptReco-v2/000/146/437/60BD2F82-DDC6-DF11-AA84-001D09F2910A.root',
        '/store/data/Run2010B/Mu/RECO/PromptReco-v2/000/146/437/42BD67BF-F4C6-DF11-9704-0030487C608C.root',
        '/store/data/Run2010B/Mu/RECO/PromptReco-v2/000/146/437/4030584E-D7C6-DF11-BDB0-000423D9890C.root',
    

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
#    process.makeGenEvt *
    process.step1*
    process.scrapingVeto*
    process.primaryVertexFilter*
    process.HBHENoiseFilter*
    process.recoJPTJets*
    process.patDefaultSequence* 
    getattr(process,"patPF2PATSequence"+postfix)*
    process.flavorHistorySeq *
    process.prunedGenParticles
    #    process.kludgedJPTJets
)

if useData :
#    process.patseq.remove( process.makeGenEvt )
    process.patseq.remove( process.flavorHistorySeq )
    process.patseq.remove( process.prunedGenParticles )
else :
    process.patseq.remove( process.scrapingVeto )
    process.patseq.remove( process.primaryVertexFilter )
    process.patseq.remove( process.HBHENoiseFilter )    

from PhysicsTools.SelectorUtils.wplusjetsAnalysis_cfi import wplusjetsAnalysis as inputwplusjetsAnalysis

process.shyftMuCalo = cms.EDFilter( 'EDWPlusJets',
                                    inputwplusjetsAnalysis.clone(
                                        jetPtMin = cms.double(25.0),
                                        muJetDR = cms.double(0.),
                                        cutsToIgnore = cms.vstring( ['MET Cut'        ,
                                                                     'Z Veto'         ,
                                                                     'Conversion Veto',
                                                                     'Cosmic Veto'    ,
                                                                     '>=1 Jets'       ,
                                                                     '>=2 Jets'       ,
                                                                     '>=3 Jets'       ,
                                                                     '>=4 Jets'       ,
                                                                     '>=5 Jets'                                                                     
                                                                     ] ),
                                        muonIdTight = inputwplusjetsAnalysis.muonIdTight.clone(
                                            cutsToIgnore=cms.vstring(options.muonIdIgnoredCuts)
                                            )
                                        )
                                    )

process.shyftMuJPT = process.shyftMuCalo.clone(
    jetSrc = cms.InputTag('selectedPatJetsAK5JPT'),
    metSrc = cms.InputTag('patMETsTC'),
    jetPtMin = cms.double(25.0),
    muJetDR = cms.double(0.),
    cutsToIgnore = cms.vstring( ['MET Cut'        ,
                                 'Z Veto'         ,
                                 'Conversion Veto',
                                 'Cosmic Veto'    ,
                                 '>=1 Jets'       ,
                                 '>=2 Jets'       ,
                                 '>=3 Jets'       ,
                                 '>=4 Jets'       ,
                                 '>=5 Jets'                                                                     
                                 ] ),
    muonIdTight = inputwplusjetsAnalysis.muonIdTight.clone(
        cutsToIgnore=cms.vstring(options.muonIdIgnoredCuts)
        )
    )

process.shyftMuPF = process.shyftMuCalo.clone(
    muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
    electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
    jetSrc = cms.InputTag('selectedPatJetsPFlow'),
    metSrc = cms.InputTag('patMETsPFlow'),
    trigSrc = cms.InputTag('patTriggerEvent'),
    muJetDR = cms.double(0.),
    jetPtMin = cms.double(20.0),
    cutsToIgnore = cms.vstring( ['MET Cut'        ,
                                 'Z Veto'         ,
                                 'Conversion Veto',
                                 'Cosmic Veto'    ,
                                 '>=1 Jets'       ,
                                 '>=2 Jets'       ,
                                 '>=3 Jets'       ,
                                 '>=4 Jets'       ,
                                 '>=5 Jets'                                                                     
                                 ] ),
    muonIdTight = inputwplusjetsAnalysis.muonIdTight.clone(
        cutsToIgnore=cms.vstring(options.muonIdIgnoredCuts)
        )
    )



process.shyftSeqCalo = cms.Sequence( process.shyftMuCalo )
process.shyftSeqPF = cms.Sequence( process.shyftMuPF )
process.shyftSeqJPT = cms.Sequence( process.shyftMuJPT )

process.p1 = cms.Path(
    process.patseq
    )

if not useWJetsFilter :
    process.out.SelectEvents.SelectEvents = cms.vstring('p1')
else : 
    process.p2 = cms.Path(
        process.patseq *
        process.shyftSeqCalo
        )

    process.p3 = cms.Path(
        process.patseq *
        process.shyftSeqPF
        )
    process.p4 = cms.Path(
        process.patseq *
        process.shyftSeqJPT
        )
    process.out.SelectEvents.SelectEvents = cms.vstring('p2', 'p3', 'p4')    


# rename output file
if useData :
    process.out.fileName = cms.untracked.string('shyft_382.root')
else :
    process.out.fileName = cms.untracked.string('shyft_382_mc.root')

# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

# process all the events
process.maxEvents.input = 50000
process.options.wantSummary = True
process.out.dropMetaData = cms.untracked.string("DROPPED")

from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoCleaning
from PhysicsTools.PatAlgos.patEventContent_cff import patExtraAodEventContent
from PhysicsTools.PatAlgos.patEventContent_cff import patTriggerEventContent
#process.out.outputCommands = patEventContentNoCleaning
#process.out.outputCommands += patExtraAodEventContent
#process.out.outputCommands += patTriggerEventContent
process.out.outputCommands = [
    'keep GenRunInfoProduct_generator_*_*',
    'keep GenEventInfoProduct_generator_*_*',
    'keep *_flavorHistoryFilter_*_*',
    'keep *_prunedGenParticles_*_*',
    'keep *_decaySubset_*_*',
    'keep *_initSubset_*_*',
    'drop *_cleanPat*_*_*',
    'keep *_selectedPat*_*_*',
    'keep *_patMETs*_*_*',
#    'keep recoPFCandidates_particleFlow_*_*',
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
    'keep *_*goodPFJets_*_*',
    'keep *_kludgedJPTJets_*_*'
    ]

if useData :
    process.out.outputCommands.append( 'keep *_towerMaker_*_*' )
