
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

options.register ('hltProcess',
                  'HLT',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "HLT process name to use.")

options.register ('useMuon',
                  1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Use muons (1) or electrons (0)")
                  
options.parseArguments()

print options

import sys

# Set to true for running on data
useData = options.useData

if options.useData == False :
    # Make sure to NOT apply L2L3Residual to MC
    corrections = ['L2Relative', 'L3Absolute']
    # global tag for 384 MC
    process.GlobalTag.globaltag = cms.string('START38_V13::All')
else :
    # Make sure to apply L2L3Residual to data
    corrections = ['L2Relative', 'L3Absolute', 'L2L3Residual']
    # global tag for 386 data
    process.GlobalTag.globaltag = cms.string('GR_R_38X_V14::All')



# Add the L1 JPT offset correction for JPT jets
jptcorrections = ['L1JPTOffset']
jptcorrections += corrections 

# require HLT_Mu9 trigger
from HLTrigger.HLTfilters.hltHighLevel_cfi import *

if options.useMuon :
    process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::" + options.hltProcess, HLTPaths = ["HLT_Mu9*", "HLT_Mu15*"])
else :
    process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::" + options.hltProcess, HLTPaths = ["HLT_EGDunnowhagoeshere*"])


process.step1.throw = False

# HB + HE noise filtering
process.load('CommonTools/RecoAlgos/HBHENoiseFilter_cfi')

# add the flavor history
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi")

 
# get the 7 TeV jet corrections
from PhysicsTools.PatAlgos.tools.jetTools import *



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


# switch on PAT trigger
from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
switchOnTrigger( process )
process.patTriggerEvent.processName = cms.string( options.hltProcess )
process.patTrigger.processName = cms.string( options.hltProcess )


process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
                                           vertexCollection = cms.InputTag('offlinePrimaryVertices'),
                                           minimumNDOF = cms.uint32(4) ,
                                           maxAbsZ = cms.double(24.0), 
                                           maxd0 = cms.double(2) 
                                           )

# Now add the two PF sequences, one for the tight leptons, the other for the loose.
# For both, do the fastjet area calculation for possible pileup subtraction correction. 

from PhysicsTools.PatAlgos.tools.pfTools import *
postfix = "PFlow"
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC= not useData, postfix=postfix) 

postfixLoose = "PFlowLoose"
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC= not useData, postfix=postfixLoose)


# turn to false when running on data
if useData :
    removeMCMatching(process, ['All'])



# We'll be using a lot of AOD so re-run b-tagging to get the
# tag infos which are dropped in AOD
switchJetCollection(process,cms.InputTag('ak5CaloJets'),
                 doJTA        = True,
                 doBTagging   = True,
                 jetCorrLabel = ('AK5Calo', cms.vstring(corrections)),
                 doType1MET   = True,
                 genJetCollection=cms.InputTag("ak5GenJets"),
                 doJetID      = True
                 )


# Add the other 6,000 jet collections that someone might hypothetically
# maybe someday think about possibly including as a cross check. 



addJetCollection(process,cms.InputTag('JetPlusTrackZSPCorJetAntiKt5'),
                 'AK5', 'JPT',
                 doJTA        = True,
                 doBTagging   = True,
                 jetCorrLabel = ('AK5JPT', cms.vstring(jptcorrections)),
                 doType1MET   = False,
                 doL1Cleaning = False,
                 doL1Counters = True,                 
                 genJetCollection = cms.InputTag("ak5GenJets"),
                 doJetID      = True,
                 jetIdLabel   = "ak5"
                 )


# PF from RECO and not using PF2PAT
addJetCollection(process,cms.InputTag('ak5PFJets'),
                 'AK5', 'PF',
                 doJTA        = True,
                 doBTagging   = True,
                 jetCorrLabel = ('AK5PF',corrections),
                 doType1MET   = False,
                 doL1Cleaning = False,
                 doL1Counters = False,                 
                 genJetCollection = cms.InputTag("ak5GenJets"),
                 doJetID      = False,
                 jetIdLabel   = "ak5"
                 )


# tcMET
from PhysicsTools.PatAlgos.tools.metTools import *
addTcMET(process, 'TC')
addPfMET(process, 'PF')





# Selection
process.selectedPatJetsPFlow.cut = cms.string('pt > 20 & abs(eta) < 2.4')
process.selectedPatJetsPFlowLoose.cut = cms.string('pt > 20 & abs(eta) < 2.4')
process.selectedPatJetsAK5JPT.cut = cms.string('pt > 20 & abs(eta) < 2.4')
process.selectedPatJetsAK5PF.cut = cms.string('pt > 20 & abs(eta) < 2.4')
process.selectedPatJets.cut = cms.string('pt > 20 & abs(eta) < 2.4')
process.patJets.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAOD")
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

process.patTaus.isoDeposits = cms.PSet()

process.patJetsPFlow.embedCaloTowers = False
process.patJetsPFlow.embedPFCandidates = False
process.patJetsPFlowLoose.embedCaloTowers = False
process.patJetsPFlowLoose.embedPFCandidates = False
process.patJetsAK5PF.embedCaloTowers = False
process.patJetsAK5PF.embedPFCandidates = False

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
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0009/E8B2CA4D-42E7-DF11-988C-90E6BA442F16.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0009/E847D402-12E7-DF11-97C5-003048D4EF1D.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0009/6EE559BE-11E7-DF11-B575-00145E5513C1.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/DC4963A1-E0E5-DF11-807E-00D0680BF898.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/D8F33E3F-58E5-DF11-9FCC-0026B9548CB5.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/B2D39D4C-63E6-DF11-8CFA-003048CEB070.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/B28EE7AE-48E5-DF11-9F45-001F29651428.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/9C7AD216-ACE5-DF11-BE50-001517255D36.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/788BCB6C-ACE5-DF11-A13C-90E6BA442F1F.root',

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


process.p1 = cms.Path(
    process.patseq
    )

process.out.SelectEvents.SelectEvents = cms.vstring('p1')


# rename output file
if useData :
    process.out.fileName = cms.untracked.string('shyft_386.root')
else :
    process.out.fileName = cms.untracked.string('shyft_386_mc.root')

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
    'drop *_MEtoEDMConverter_*_*'
    ]

if useData :
    process.out.outputCommands.append( 'keep *_towerMaker_*_*' )
    process.out.outputCommands.append( 'keep LumiSummary_lumiProducer_*_*' )
    
