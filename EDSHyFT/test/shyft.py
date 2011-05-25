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


options.register ('useLooseLeptonPresel',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Select events with a very loose W+jets selector, consisting of a simple lepton count")


options.register ('useTrigger',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Select events with the HLT_Mu9 or HLT_Mu11 triggers only")
                  
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
useLooseLeptonPresel = options.useLooseLeptonPresel
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
        process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::HLT", HLTPaths = ["HLT_Mu9", "HLT_Mu11"])
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

# JPT
process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
process.load('RecoJets.Configuration.RecoJPTJets_cff')


from PhysicsTools.PatAlgos.tools.pfTools import *
postfix = "PFlow"
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC= not useData, postfix=postfix) 

postfixLoose = "PFlowLoose"
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC= not useData, postfix=postfixLoose)



# turn to false when running on data
if useData :
    getattr(process, "patElectrons"+postfix).embedGenMatch = False
    getattr(process, "patMuons"+postfix).embedGenMatch = False
    getattr(process, "patElectrons"+postfixLoose).embedGenMatch = False
    getattr(process, "patMuons"+postfixLoose).embedGenMatch = False
    removeMCMatching(process, ['All'])


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

# PF from RECO and not using PF2PAT
addJetCollection(process,cms.InputTag('ak5PFJets'),
                 'AK5', 'PF',
                 doJTA        = True,
                 doBTagging   = True,
                 jetCorrLabel = ('AK5','PF'),
                 doType1MET   = False,
                 doL1Cleaning = False,
                 doL1Counters = False,                 
                 genJetCollection = cms.InputTag("ak5GenJets"),
                 doJetID      = True,
                 jetIdLabel   = "ak5"
                 )

# tcMET
from PhysicsTools.PatAlgos.tools.metTools import *
addTcMET(process, 'TC')
addPfMET(process, 'PF')





# Selection
process.selectedPatJetsPFlow.cut = cms.string('pt > 15 & abs(eta) < 2.4')
process.selectedPatJetsPFlowLoose.cut = cms.string('pt > 15 & abs(eta) < 2.4')
process.selectedPatJetsAK5JPT.cut = cms.string('pt > 15 & abs(eta) < 2.4')
process.selectedPatJetsAK5PF.cut = cms.string('pt > 15 & abs(eta) < 2.4')
process.selectedPatJets.cut = cms.string('pt > 20 & abs(eta) < 2.4')
process.patJets.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfos")
    )
process.patJetsPFlow.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAOD" + postfix)
    )
process.patJetsPFlowLoose.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAOD" + postfixLoose)
    )
process.patJetsAK5JPT.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAK5JPT")
    )
process.patJetsAK5PF.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAK5PF")
    )


process.patMuonsPFlowLoose.pfMuonSource = 'pfAllMuonsPFlowLoose'
process.patMuonsPFlowLoose.isoDeposits = cms.PSet()
process.patMuonsPFlowLoose.isolationValues = cms.PSet()
#process.patElectronsPFlowLoose.pfElectronSource = 'pfAllElectronsPFlowLoose'
#process.patElectronsPFlowLoose.isoDeposits = cms.PSet()
#process.patElectronsPFlowLoose.isolationValues = cms.PSet()


print 'For PAT PF Muons: '
print process.patMuonsPFlowLoose.pfMuonSource

process.selectedPatMuons.cut = cms.string("pt > 3")
process.selectedPatMuonsPFlow.cut = cms.string("pt > 3")
process.selectedPatMuonsPFlowLoose.cut = cms.string("pt > 3")
process.patMuons.usePV = False
process.patMuonsPFlow.usePV = False
process.patMuonsPFlowLoose.usePV = False
process.selectedPatElectrons.cut = cms.string("pt > 3")
process.selectedPatElectronsPFlow.cut = cms.string("pt > 3")
process.selectedPatElectronsPFlowLoose.cut = cms.string("pt > 3")
process.patElectrons.usePV = False
process.patElectronsPFlow.usePV = False
process.patElectronsPFlowLoose.usePV = False

process.patJets.userData.userFunctions = cms.vstring( "? hasTagInfo('secondaryVertex') && tagInfoSecondaryVertex('secondaryVertex').nVertices() > 0 ? "
                                                      "tagInfoSecondaryVertex('secondaryVertex').secondaryVertex(0).p4().mass() : 0")
process.patJets.userData.userFunctionLabels = cms.vstring('secvtxMass')


process.patJetsPFlow.userData.userFunctions = cms.vstring( "? hasTagInfo('secondaryVertex') && tagInfoSecondaryVertex('secondaryVertex').nVertices() > 0 ? "
                                                      "tagInfoSecondaryVertex('secondaryVertex').secondaryVertex(0).p4().mass() : 0")
process.patJetsPFlow.userData.userFunctionLabels = cms.vstring('secvtxMass')


process.patJetsPFlowLoose.userData.userFunctions = cms.vstring( "? hasTagInfo('secondaryVertex') && tagInfoSecondaryVertex('secondaryVertex').nVertices() > 0 ? "
                                                      "tagInfoSecondaryVertex('secondaryVertex').secondaryVertex(0).p4().mass() : 0")
process.patJetsPFlowLoose.userData.userFunctionLabels = cms.vstring('secvtxMass')


# remove trigger matching for PF2PAT as that is currently broken
process.patPF2PATSequencePFlow.remove(process.patTriggerSequencePFlow)
process.patPF2PATSequencePFlowLoose.remove(process.patTriggerSequencePFlowLoose)
process.patPF2PATSequencePFlow.remove(process.patTriggerEventPFlow)
process.patPF2PATSequencePFlowLoose.remove(process.patTriggerEventPFlowLoose)
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
        '/store/mc/Spring10/TTbarJets-madgraph/GEN-SIM-RECO/START3X_V26_S09-v1/0006/4C4A0E8D-C946-DF11-BCAC-003048D437D2.root',
        '/store/mc/Spring10/TTbarJets-madgraph/GEN-SIM-RECO/START3X_V26_S09-v1/0006/D87D77D2-C946-DF11-AD67-0030487D5E81.root',
        '/store/mc/Spring10/TTbarJets-madgraph/GEN-SIM-RECO/START3X_V26_S09-v1/0006/B47C6690-C946-DF11-8BC0-003048C692FA.root'
        ] );

    
process.source.fileNames = readFiles


# let it run

#print
#print "============== Warning =============="
#print "technical trigger filter:    DISABLED"
#print "physics declare bit filter:  DISABLED"
#print "primary vertex filter:       DISABLED"

process.patseq = cms.Sequence(
    process.step1*
    process.scrapingVeto*
    process.primaryVertexFilter*
    process.HBHENoiseFilter*
    process.recoJPTJets*
    process.patDefaultSequence* 
    getattr(process,"patPF2PATSequence"+postfix)*
    getattr(process,"patPF2PATSequence"+postfixLoose)*    
    process.flavorHistorySeq *
    process.prunedGenParticles
)

if useData :
    process.patseq.remove( process.flavorHistorySeq )
    process.patseq.remove( process.prunedGenParticles )
else :
    process.patseq.remove( process.scrapingVeto )
    process.patseq.remove( process.primaryVertexFilter )
    process.patseq.remove( process.HBHENoiseFilter )    


process.isolatedPatMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("selectedPatMuons"),
    cut = cms.string("(trackIso+caloIso)/pt < 0.1"),
    filter=cms.bool(True)                                       
)

process.isolatedPatMuonsPFlow = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("selectedPatMuonsPFlow"),
    cut = cms.string(""),
    filter=cms.bool(True)
)

process.p1 = cms.Path(
    process.patseq
    )

if not useLooseLeptonPresel :
    process.out.SelectEvents.SelectEvents = cms.vstring('p1')
else : 
    process.p2 = cms.Path(
        process.patseq *
        process.isolatedPatMuons
        )
    process.p3 = cms.Path(
        process.patseq *
        process.isolatedPatMuonsPFlow
        )    

    process.out.SelectEvents.SelectEvents = cms.vstring('p2', 'p3')    


# rename output file
if useData :
    process.out.fileName = cms.untracked.string('shyft_382.root')
else :
    process.out.fileName = cms.untracked.string('shyft_382_mc.root')

# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

# process all the events
process.maxEvents.input = 100
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
    'keep *_*goodPFJets_*_*'
    ]

if useData :
    process.out.outputCommands.append( 'keep *_towerMaker_*_*' )
    process.out.outputCommands.append( 'keep LumiSummary_lumiProducer_*_*' )
    
