# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *

###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('useData',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run this on real data")

options.register ('hltProcess',
                  'HLT',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "HLT process name to use.")


options.parseArguments()

if not options.useData :
    mytrigs = ['HLT_Jet100U*']
    inputJetCorrLabel = ('AK5PF', ['L2Relative', 'L3Absolute'])
    process.source.fileNames = [
#        '/store/mc/Fall10/QCD_Pt_15to3000_TuneZ2_Flat_7TeV_pythia6/GEN-SIM-RECO/START38_V12-v1/0000/02AFCD3B-BECD-DF11-9F32-00215E21DD50.root'
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0009/E8B2CA4D-42E7-DF11-988C-90E6BA442F16.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0009/E847D402-12E7-DF11-97C5-003048D4EF1D.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0009/6EE559BE-11E7-DF11-B575-00145E5513C1.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/DC4963A1-E0E5-DF11-807E-00D0680BF898.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/D8F33E3F-58E5-DF11-9FCC-0026B9548CB5.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/B2D39D4C-63E6-DF11-8CFA-003048CEB070.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/B28EE7AE-48E5-DF11-9F45-001F29651428.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/9C7AD216-ACE5-DF11-BE50-001517255D36.root',
       '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/788BCB6C-ACE5-DF11-A13C-90E6BA442F1F.root',
        ]
else :
    mytrigs = ['HLT_Jet100U*', 'HLT_Jet140U*','HLT_DiJet50U_PT50U*']    
    inputJetCorrLabel = ('AK5PF', ['L2Relative', 'L3Absolute', 'L2L3Residual'])
    process.source.fileNames = [
       '/store/data/Run2010B/Jet/AOD/PromptReco-v2/000/149/304/30B9CEA8-DDE4-DF11-B709-0030487CD718.root',
       '/store/data/Run2010B/Jet/AOD/PromptReco-v2/000/149/294/8E477C21-F8E4-DF11-8937-0030487CD6D2.root',
       '/store/data/Run2010B/Jet/AOD/PromptReco-v2/000/149/294/20681FD0-F8E4-DF11-9267-001617E30E2C.root',
       '/store/data/Run2010B/Jet/AOD/PromptReco-v2/000/149/294/12EB1F94-05E5-DF11-A954-0030487A18A4.root',
       '/store/data/Run2010B/Jet/AOD/PromptReco-v2/000/149/293/649330C7-C2E4-DF11-9ED2-003048F1182E.root',
       '/store/data/Run2010B/Jet/AOD/PromptReco-v2/000/149/291/F8941D92-F7E4-DF11-BF83-003048F024DC.root',
       '/store/data/Run2010B/Jet/AOD/PromptReco-v2/000/149/291/BCA59158-D4E4-DF11-9B51-001D09F252DA.root',
       '/store/data/Run2010B/Jet/AOD/PromptReco-v2/000/149/291/B2092557-D4E4-DF11-B75C-0030487C90C2.root',        
        ]


print options

import sys


###############################
####### Global Setup ##########
###############################

if options.useData == False :
    # global tag for MC
    process.GlobalTag.globaltag = cms.string('START38_V13::All')
else :
    # global tag for 361 data
    process.GlobalTag.globaltag = cms.string('GR_R_38X_V14::All')

# require scraping filter
process.scrapingVeto = cms.EDFilter("FilterOutScraping",
                                    applyfilter = cms.untracked.bool(True),
                                    debugOn = cms.untracked.bool(False),
                                    numtrack = cms.untracked.uint32(10),
                                    thresh = cms.untracked.double(0.2)
                                    )
# HB + HE noise filtering
process.load('CommonTools/RecoAlgos/HBHENoiseFilter_cfi')


# switch on PAT trigger
from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
switchOnTrigger( process, hltProcess=options.hltProcess )


from HLTrigger.HLTfilters.hltHighLevel_cfi import *
if mytrigs is not None :
    process.hltSelection = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::' + options.hltProcess, HLTPaths = mytrigs)
else :
    process.hltSelection = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::' + options.hltProcess, HLTPaths = ['*'])    
    



process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
                                           vertexCollection = cms.InputTag('offlinePrimaryVertices'),
                                           minimumNDOF = cms.uint32(4) ,
                                           maxAbsZ = cms.double(24), 
                                           maxd0 = cms.double(2) 
                                           )

###############################
########## GenJet Setup #######
###############################

process.load("RecoJets.Configuration.GenJetParticles_cff")
from RecoJets.JetProducers.ca4GenJets_cfi import ca4GenJets
process.ca8GenJets = ca4GenJets.clone( rParam = cms.double(0.8) )


###############################
#### Jet RECO includes ########
###############################

from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters
from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.CaloJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
from RecoJets.JetProducers.CATopJetParameters_cfi import *



###############################
########## PF Setup ###########
###############################

# Default PF2PAT, switch to CA8 jets
from PhysicsTools.PatAlgos.tools.pfTools import *
postfix = "PFlow"
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC=not options.useData, postfix=postfix)
process.allPfJetsPFlow.jetAlgorithm = "CambridgeAachen"
process.allPfJetsPFlow.rParam       = 0.8
process.allPfJetsPFlow.doAreaFastjet = True
process.allPfJetsPFlow.doRhoFastjet = True
process.allPfJetsPFlow.Ghost_EtaMax = 6.0

# PF2PAT with only charged hadrons from first PV
postfixPUSub = "PFlowPUSub"
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC=not options.useData, postfix=postfixPUSub)
process.pfPileUpPFlowPUSub.Enable = True
process.allPfJetsPFlowPUSub.jetAlgorithm = "CambridgeAachen"
process.allPfJetsPFlowPUSub.rParam       = 0.8
process.allPfJetsPFlowPUSub.doAreaFastjet = True
process.allPfJetsPFlowPUSub.doRhoFastjet = True
process.allPfJetsPFlowPUSub.Ghost_EtaMax = 6.0



# turn to false when running on data
if options.useData :
    for ipostfix in [ postfix, postfixPUSub] :
        getattr(process, "patPhotons"+ipostfix).embedGenMatch = False
        getattr(process, "patElectrons"+ipostfix).embedGenMatch = False
        getattr(process, "patMuons"+ipostfix).embedGenMatch = False

    removeMCMatching( process, ['All'] )



###############################
###### Jet Pruning Setup ######
###############################


# Pruned PF Jets
process.caPrunedPFlow = cms.EDProducer(
    "SubJetProducer",
    PFJetParameters.clone( src = cms.InputTag('pfNoElectron'+postfix),
                           doAreaFastjet = cms.bool(True),
                           doRhoFastjet = cms.bool(True),
                           inputEMin = cms.double(1.0),
                           Ghost_EtaMax = cms.double(6.0)
                           ),
    AnomalousCellParameters,
    SubJetParameters,
    jetAlgorithm = cms.string("CambridgeAachen"),
    rParam = SubJetParameters.jetSize,
    jetCollInstanceName=cms.string("subjets")
    )

# Pruned PF Jets, pileup removed
process.caPrunedPFlowPUSub = cms.EDProducer(
    "SubJetProducer",
    PFJetParameters.clone( src = cms.InputTag('pfNoElectron'+postfixPUSub),
                           doAreaFastjet = cms.bool(True),
                           doRhoFastjet = cms.bool(True),
                           inputEMin = cms.double(1.0),
                           Ghost_EtaMax = cms.double(6.0)
                           ),
    AnomalousCellParameters,
    SubJetParameters,
    jetAlgorithm = cms.string("CambridgeAachen"),
    rParam = SubJetParameters.jetSize,
    jetCollInstanceName=cms.string("subjets")
    )


###############################
#### CATopTag Setup ###########
###############################

# CATopJet PF Jets
# with adjacency 
process.caTopTagPFlow = cms.EDProducer(
    "CATopJetProducer",
    PFJetParameters.clone( src = cms.InputTag('pfNoElectron'+postfix),
                           doAreaFastjet = cms.bool(True),
                           doRhoFastjet = cms.bool(True),
                           Ghost_EtaMax = cms.double(6.0)
                           ),
    AnomalousCellParameters,
    CATopJetParameters,
    jetAlgorithm = cms.string("CambridgeAachen"),
    rParam = SubJetParameters.jetSize
    )

process.CATopTagInfosPFlow = cms.EDProducer("CATopJetTagger",
                                    src = cms.InputTag("caTopTagPFlow"),
                                    TopMass = cms.double(171),
                                    TopMassMin = cms.double(0.),
                                    TopMassMax = cms.double(250.),
                                    WMass = cms.double(80.4),
                                    WMassMin = cms.double(0.0),
                                    WMassMax = cms.double(200.0),
                                    MinMassMin = cms.double(0.0),
                                    MinMassMax = cms.double(200.0),
                                    verbose = cms.bool(False)
                                    )




# CATopJet PF Jets
# with adjacency 
process.caTopTagPFlowPUSub = cms.EDProducer(
    "CATopJetProducer",
    PFJetParameters.clone( src = cms.InputTag('pfNoElectron'+postfixPUSub),
                           doAreaFastjet = cms.bool(True),
                           doRhoFastjet = cms.bool(True),
                           Ghost_EtaMax = cms.double(6.0)
                           ),
    AnomalousCellParameters,
    CATopJetParameters,
    jetAlgorithm = cms.string("CambridgeAachen"),
    rParam = SubJetParameters.jetSize
    )

process.CATopTagInfosPFlowPUSub = cms.EDProducer("CATopJetTagger",
                                    src = cms.InputTag("caTopTagPFlowPUSub"),
                                    TopMass = cms.double(171),
                                    TopMassMin = cms.double(0.),
                                    TopMassMax = cms.double(250.),
                                    WMass = cms.double(80.4),
                                    WMassMin = cms.double(0.0),
                                    WMassMax = cms.double(200.0),
                                    MinMassMin = cms.double(0.0),
                                    MinMassMax = cms.double(200.0),
                                    verbose = cms.bool(False)
                                    )





# CATopJet PF Jets


#process.PF2PAT += ( process.ca8PFJets*
#                    process.caPrunedPFJets*
#                    process.caTopTagPFJets*
#                    process.CATopPFJetTagInfos)

# add the modules to the sequence

for ipostfix in [postfix, postfixPUSub] :
    for module in (
        getattr(process,"CATopTagInfos" + ipostfix),
        getattr(process,"caTopTag" + ipostfix),
        getattr(process,"caPruned" + ipostfix)
        ) :
        getattr(process,"patPF2PATSequence"+ipostfix).replace( getattr(process,"pfNoElectron"+ipostfix), getattr(process,"pfNoElectron"+ipostfix)*module )

# We'll be using a lot of AOD so re-run b-tagging to get the
# tag infos which are dropped in AOD
switchJetCollection(process,cms.InputTag('ak5PFJets'),
                 doJTA        = True,
                 doBTagging   = True,
                 jetCorrLabel = inputJetCorrLabel,
                 doType1MET   = True,
                 genJetCollection=cms.InputTag("ak5GenJets"),
                 doJetID      = True
                 )


addJetCollection(process, 
                 cms.InputTag('caPrunedPFlow'),         # Jet collection; must be already in the event when patLayer0 sequence is executed
                 'CA8Pruned', 'PF',
                 doJTA=True,            # Run Jet-Track association & JetCharge
                 doBTagging=True,       # Run b-tagging
                 jetCorrLabel=inputJetCorrLabel,
                 doType1MET=False,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 genJetCollection = cms.InputTag("ca8GenJets"),
                 doJetID = False
                 )


addJetCollection(process, 
                 cms.InputTag('caTopTagPFlow'),
                 'CATopTag', 'PF',
                 doJTA=True,
                 doBTagging=True,
                 jetCorrLabel=inputJetCorrLabel,
                 doType1MET=False,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 genJetCollection = cms.InputTag("ca8GenJets"),
                 doJetID = False
                 )

addJetCollection(process, 
                 cms.InputTag('caPrunedPFlowPUSub'),         # Jet collection; must be already in the event when patLayer0 sequence is executed
                 'CA8PrunedPUSub', 'PF',
                 doJTA=True,            # Run Jet-Track association & JetCharge
                 doBTagging=True,       # Run b-tagging
                 jetCorrLabel=inputJetCorrLabel,   # example jet correction name; set to None for no JEC
                 doType1MET=False,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 genJetCollection = cms.InputTag("ca8GenJets"),
                 doJetID = False
                 )


addJetCollection(process, 
                 cms.InputTag('caTopTagPFlowPUSub'),
                 'CATopTagPUSub', 'PF',
                 doJTA=True,
                 doBTagging=True,
                 jetCorrLabel=inputJetCorrLabel,
                 doType1MET=False,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 genJetCollection = cms.InputTag("ca8GenJets"),
                 doJetID = False
                 )

###############################
### TagInfo and Matching Setup#
###############################

# Do some configuration of the jet substructure things
for jetcoll in (process.patJetsPFlow,
                process.patJetsCA8PrunedPF,
                process.patJetsCATopTagPF,
                process.patJetsPFlowPUSub,
                process.patJetsCA8PrunedPUSubPF,
                process.patJetsCATopTagPUSubPF 
                ) :
    if options.useData == False :
        jetcoll.embedGenJetMatch = cms.bool(True)
        jetcoll.getJetMCFlavour = cms.bool(True)
        jetcoll.addGenPartonMatch = cms.bool(True)
    # Add CATopTag info... piggy-backing on b-tag functionality
    jetcoll.addBTagInfo = cms.bool(True)
    jetcoll.addTagInfos = cms.bool(True)
    jetcoll.embedCaloTowers = cms.bool(False)
    jetcoll.embedPFCandidates = cms.bool(False)
    jetcoll.embedGenJetMatch = cms.bool(False)



###############################
#### Selections Setup #########
###############################

process.patJets.addTagInfos = False

# AK5 Jets
#   PF
process.selectedPatJetsPFlow.cut = cms.string("pt > 50")
process.patJetsPFlow.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAODPFlow")
    )
process.patJetsPFlow.addTagInfos = True
process.patJetsPFlow.embedCaloTowers = False
process.patJetsPFlow.embedPFCandidates = False

process.patJetsPFlow.userData.userFunctions = cms.vstring( "? hasTagInfo('secondaryVertex') && tagInfoSecondaryVertex('secondaryVertex').nVertices() > 0 ? "
                                                      "tagInfoSecondaryVertex('secondaryVertex').secondaryVertex(0).p4().mass() : 0")
process.patJetsPFlow.userData.userFunctionLabels = cms.vstring('secvtxMass')


process.patJetsPFlowPUSub.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAODPFlowPUSub")
    )
process.patJetsPFlowPUSub.addTagInfos = True
process.patJetsPFlowPUSub.embedCaloTowers = False
process.patJetsPFlowPUSub.embedPFCandidates = False


process.patJetsPFlowPUSub.userData.userFunctions = cms.vstring( "? hasTagInfo('secondaryVertex') && tagInfoSecondaryVertex('secondaryVertex').nVertices() > 0 ? "
                                                      "tagInfoSecondaryVertex('secondaryVertex').secondaryVertex(0).p4().mass() : 0")
process.patJetsPFlowPUSub.userData.userFunctionLabels = cms.vstring('secvtxMass')


# CA8 Pruned jets
#  PF
process.selectedPatJetsCA8PrunedPF.cut = cms.string("pt > 50")
process.patJetsCA8PrunedPF.tagInfoSources = cms.VInputTag()

process.selectedPatJetsCA8PrunedPUSubPF.cut = cms.string("pt > 50")
process.patJetsCA8PrunedPUSubPF.tagInfoSources = cms.VInputTag()

# CA8 TopJets
#   PF
process.selectedPatJetsCATopTagPF.cut = cms.string("pt > 50")
process.patJetsCATopTagPF.tagInfoSources = cms.VInputTag(
    cms.InputTag('CATopTagInfosPFlow')
    )

process.selectedPatJetsCATopTagPUSubPF.cut = cms.string("pt > 50")
process.patJetsCATopTagPUSubPF.tagInfoSources = cms.VInputTag(
    cms.InputTag('CATopTagInfosPFlowPUSub')
    )


# electrons
process.selectedPatElectronsPFlow.cut = cms.string('pt > 10.0')
process.patElectronsPFlow.isoDeposits = cms.PSet()
process.patElectronsPFlow.embedTrack = cms.bool(True)
process.patElectronsPFlow.usePV = cms.bool(False)
# muons
process.selectedPatMuonsPFlow.cut = cms.string("pt > 10.0")
process.patMuonsPFlow.isoDeposits = cms.PSet()
process.patMuonsPFlow.embedTrack = cms.bool(True)
process.patMuonsPFlow.usePV = cms.bool(False)
# taus
process.selectedPatTausPFlow.cut = cms.string("pt > 5 & abs(eta) < 3")
# photons
process.patPhotonsPFlow.isoDeposits = cms.PSet()
#taus
process.patTausPFlow.isoDeposits = cms.PSet()




# remove trigger matching for PF2PAT as that is currently broken
#process.patPF2PATSequencePFlow.remove(process.patTriggerSequencePFlow)
#process.patPF2PATSequencePFlowPUSub.remove(process.patTriggerSequencePFlowPUSub)
    
# let it run

process.patseq = cms.Sequence(
    process.hltSelection*
    process.scrapingVeto*
    process.primaryVertexFilter*
    process.HBHENoiseFilter*
    process.genJetParticles*
    process.ca8GenJets*
    getattr(process,"patPF2PATSequence"+postfix)*
    getattr(process,"patPF2PATSequence"+postfixPUSub)*
    process.patDefaultSequence
    )

if options.useData == True :
    process.patseq.remove( process.genJetParticles )
    process.patseq.remove( process.ca8GenJets )


process.p0 = cms.Path(
    process.patseq
    )

process.out.SelectEvents.SelectEvents = cms.vstring('p0')
    
# rename output file
process.out.fileName = cms.untracked.string('ttbsm_386.root')

# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)


# process all the events
process.maxEvents.input = 1000
process.options.wantSummary = True
process.out.dropMetaData = cms.untracked.string("DROPPED")




process.source.inputCommands = cms.untracked.vstring("keep *", "drop *_MEtoEDMConverter_*_*")



process.out.outputCommands = [
    'drop *_cleanPat*_*_*',
    'keep *_selectedPat*_*_*',
    'keep *_patMETs*_*_*',
    'keep recoPFCandidates_particleFlow_*_*',
    'keep *_offlineBeamSpot_*_*',
    'keep *_offlinePrimaryVertices_*_*',
    'drop patPFParticles_*_*_*',
    'keep recoPFJets_caPrunedPFJets*_*_*',
    'keep recoPFJets_caTopTagPFJets*_*_*',
    'keep patTriggerObjects_patTrigger*_*_*',
    'keep patTriggerFilters_patTrigger*_*_*',
    'keep patTriggerPaths_patTrigger*_*_*',
    'keep patTriggerEvent_patTriggerEvent*_*_*',
    'keep *_cleanPatPhotonsTriggerMatch*_*_*',
    'keep *_cleanPatElectronsTriggerMatch*_*_*',
    'keep *_cleanPatMuonsTriggerMatch*_*_*',
    'keep *_cleanPatTausTriggerMatch*_*_*',
    'keep *_cleanPatJetsTriggerMatch*_*_*',
    'keep *_patMETsTriggerMatch*_*_*',
    'keep double_*PFlow*_*_*'
    ]

if options.useData :
    process.out.outputCommands += ['keep *_towerMaker_*_*',
                                   'drop *_MEtoEDMConverter_*_*',
                                   'keep LumiSummary_lumiProducer_*_*',
                                   'keep recoTracks_generalTracks_*_*',
                                   ]
else :
    process.out.outputCommands += ['keep *_genParticles_*_*',    
                                   'keep recoGenJets_ca8GenJets_*_*',
                                   'keep GenRunInfoProduct_generator_*_*',
                                   'keep GenEventInfoProduct_generator_*_*'

                                   ]


#open('junk.py','w').write(process.dumpPython())
