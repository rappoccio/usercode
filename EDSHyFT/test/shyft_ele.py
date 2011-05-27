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

options.register ('useWJetsFilter',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Select events with the super duper W+jets skim")

options.register ('useLooseLeptonPresel',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Select events with a very loose W+jets selector, consisting of reliso cut")

options.register ('usePromptGT',
				  0,
				  VarParsing.multiplicity.singleton,
				  VarParsing.varType.int,
				  "Using GT=GR10_P_V10 for prompt data")

options.register ('useTrigger',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Select events with the HLT_Photon10/15 trigger only")
                  
options.register ('useRange135821to139980',
				  0,
				  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Selected run range 135821-139980 for HLT_Ele10_LW_L1R")

options.register ('useRange140058to143962',
				  0,
				  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
				  "Selected run range 140058_143962 for HLT_Ele15_SW_L1R")

options.register ('useRange144010to146421',
				  0,
				  VarParsing.multiplicity.singleton,
				  VarParsing.varType.int,
				  "Selected run range 144010_146421 for HLT_Ele15_SW_CaloEleId_L1R")

options.register ('useRange146428to147116',
				  0,
				  VarParsing.multiplicity.singleton,
				  VarParsing.varType.int,
				  "Selected run range 146428_147116 for HLT_Ele17_SW_CaloEleId_L1R")

options.register ('useRange147196to147454',
				  0,
				  VarParsing.multiplicity.singleton,
				  VarParsing.varType.int,
				  "Selected run range 147196_147454 for HLT_Ele17_SW_TightEleId_L1R")

                  
options.parseArguments()

print options

import sys

# Set to true for running on data
useData = options.useData
# Set the different GT for Prompt data
usePromptGT = options.usePromptGT
# Set to true to run on < 36x samples
use35x = options.use35x
# run the W+Jets selector filter
useWJetsFilter = options.useWJetsFilter
# run the loose W+Jets selector filter
useLooseLeptonPresel = options.useLooseLeptonPresel
# check the trigger
useTrigger = options.useTrigger
# check triggers for different run era
useRange135821to139980 = options.useRange135821to139980
useRange140058to143962 = options.useRange140058to143962
useRange144010to146421 = options.useRange144010to146421
useRange146428to147116 = options.useRange146428to147116
useRange147196to147454 = options.useRange147196to147454

## global tag for data (use GR_R_38X_V13::All for 38x processed rereco data otherwise GR_R_38X_V9::All for 36x data)
if useData :
	if usePromptGT:
		process.GlobalTag.globaltag = cms.string('GR10_P_V10::All')
	else :	
	    process.GlobalTag.globaltag = cms.string('GR_R_38X_V13::All')
else :
    process.GlobalTag.globaltag = cms.string('START38_V12::All')


# require no trigger for MC and bunch of triggers for different run era
from HLTrigger.HLTfilters.hltHighLevel_cfi import *
if useData == True :
	
	if useTrigger and useRange135821to139980 :
		process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::HLT", HLTPaths = ["HLT_Ele10_LW_L1R"])
		triggerFilter = "hltL1NonIsoHLTNonIsoSingleElectronLWEt10PixelMatchFilter"
		
	elif useTrigger and useRange140058to143962 :
		process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::HLT", HLTPaths = ["HLT_Ele15_SW_L1R"])
		triggerFilter = "hltL1NonIsoHLTNonIsoSingleElectronEt15PixelMatchFilter"
 		
	elif useTrigger and useRange144010to146421 :
		process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::HLT", HLTPaths = ["HLT_Ele15_SW_CaloEleId_L1R"])
		triggerFilter = "hltL1NonIsoHLTNonIsoSingleElectronEt15CaloEleIdPixelMatchFilter"

	elif useTrigger and useRange146428to147116 :
		process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::HLT", HLTPaths = ["HLT_Ele17_SW_CaloEleId_L1R"])
		triggerFilter = "hltL1NonIsoHLTNonIsoSingleElectronEt17CaloEleIdPixelMatchFilter"
		
	elif useTrigger and useRange147196to147454 :
		process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::HLT", HLTPaths = ["HLT_Ele17_SW_TightEleId_L1R"])
		triggerFilter = "hltL1NonIsoHLTNonIsoSingleElectronEt17TightEleIdDphiFilter"
		
	else :
		process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::HLT", HLTPaths = ["*"])
		triggerFilter = ""
else :
	process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::REDIGI", HLTPaths = ["*"])
	triggerFilter = ""

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
                                    thresh = cms.untracked.double(0.25)
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
                                           maxAbsZ = cms.double(24), 
                                           maxd0 = cms.double(2) 
                                           )
#Use only for data	
process.HLTFilter = cms.EDFilter("HLTSummaryFilter",
								 summary = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
								 member  = cms .InputTag 
								 (triggerFilter,"","HLT"),
								 cut     = cms.string(""),
								 minN    = cms.int32(1)
                                 )

from PhysicsTools.PatAlgos.tools.pfTools import *
postfix = "PFlow"
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC= not useData, postfix=postfix) 

postfixLoose = "PFlowLoose"
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC= not useData, postfix=postfixLoose)

# turn to false when running on data
if useData :
    getattr(process, "patElectrons"+postfix).embedGenMatch = False
    getattr(process, "patMuons"+postfix).embedGenMatch = False
    removeMCMatching(process, ['All'])


# tcMET
from PhysicsTools.PatAlgos.tools.metTools import *
addTcMET(process, 'PF')
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

#remove isolation from the pflow electrons and store another collection called loose PFlow
process.patElectronsPFlowLoose.pfElectronSource = 'pfAllElectronsPFlowLoose'
process.patElectronsPFlowLoose.isoDeposits = cms.PSet()
process.patElectronsPFlowLoose.isolationValues = cms.PSet()

print 'For PAT PF Muons: '
print process.patElectronsPFlowLoose.pfElectronSource


#Require PV wrt Beamspot
process.patElectrons.usePV = False
process.patElectronsPFlow.usePV = False
process.patElectronsPFlowLoose.usePV = False
process.patMuons.usePV = False
process.patMuonsPFlow.usePV = False
process.patMuonsPFlowLoose.usePV = False

#insert partner track info, dist and dcot for conversion rejection
process.patElectronsUserData = cms.EDProducer(
    "PATElectronUserData",
    src = cms.InputTag("patElectrons"),
	useData = cms.bool(useData==1)
)	

process.patElectronsPFlowUserData = cms.EDProducer(
    "PATElectronUserData",
    src = cms.InputTag("patElectronsPFlow"),
	useData = cms.bool(useData==1)
)

process.patElectronsPFlowLooseUserData = cms.EDProducer(
    "PATElectronUserData",
    src = cms.InputTag("patElectronsPFlowLoose"),
	useData = cms.bool(useData==1)
)
	
#Embed the user data process into the PAT sequence and tell selectedPatElectrons(PFlow) to use the new user collection as input
process.makePatElectrons.replace(getattr(process,"patElectrons"),getattr(process,"patElectrons")*process.patElectronsUserData)
process.selectedPatElectrons.src = "patElectronsUserData"
process.selectedPatElectrons.cut = cms.string("et > 20 & abs(eta)<3")

process.makePatElectronsPFlow.replace(getattr(process,"patElectronsPFlow"),getattr(process,"patElectronsPFlow")*process.patElectronsPFlowUserData)
process.selectedPatElectronsPFlow.src = "patElectronsPFlowUserData"
process.selectedPatElectronsPFlow.cut = cms.string("et > 20 & abs(eta)<3")

process.makePatElectronsPFlowLoose.replace(getattr(process,"patElectronsPFlowLoose"),getattr(process,"patElectronsPFlowLoose")*process.patElectronsPFlowLooseUserData)
process.selectedPatElectronsPFlowLoose.src = "patElectronsPFlowLooseUserData"
process.selectedPatElectronsPFlowLoose.cut = cms.string("et > 20 & abs(eta)<3")

process.selectedPatMuons.cut = cms.string("pt > 10 & abs(eta)<2.5")
process.selectedPatMuonsPFlow.cut = cms.string("pt > 10 & abs(eta)<2.5")
process.selectedPatMuonsPFlowLoose.cut = cms.string("pt > 10 & abs(eta)<2.5")

#secondary vertex mass
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
process.patPF2PATSequencePFlow.remove(process.patTriggerEventPFlow)
process.patPF2PATSequencePFlowLoose.remove(process.patTriggerSequencePFlowLoose)
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
        '/store/data/Run2010B/Electron/AOD/PromptReco-v2/000/147/589/7E9930AD-22D4-DF11-AA01-000423D94908.root',
        '/store/data/Run2010B/Electron/AOD/PromptReco-v2/000/147/500/EE97A9AD-9FD3-DF11-8234-0030487CD162.root',
        '/store/data/Run2010B/Electron/AOD/PromptReco-v2/000/147/462/4ADCA9BE-93D3-DF11-9C7E-001D09F251FE.root',
        '/store/data/Run2010B/Electron/AOD/PromptReco-v2/000/147/454/B490F639-B7D3-DF11-8A34-000423D98950.root',
        '/store/data/Run2010B/Electron/AOD/PromptReco-v2/000/147/454/A0C0E73B-B7D3-DF11-BD27-0030487C7E18.root',
        '/store/data/Run2010B/Electron/AOD/PromptReco-v2/000/147/454/48A1D73B-B7D3-DF11-98DD-0030487CD6D8.root',
        '/store/data/Run2010B/Electron/AOD/PromptReco-v2/000/147/454/4881D641-C3D3-DF11-A0DC-003048F024E0.root',
        

		
		## '/store/data/Run2010B/Electron/RECO/PromptReco-v2/000/147/248/CECB1E05-58D1-DF11-B404-0030487C6088.root',
##         '/store/data/Run2010B/Electron/RECO/PromptReco-v2/000/147/225/E226C2A3-2ED1-DF11-B3BF-003048F1C420.root',
##         '/store/data/Run2010B/Electron/RECO/PromptReco-v2/000/147/222/F8C896B3-37D1-DF11-809F-003048F11C58.root',
##         '/store/data/Run2010B/Electron/RECO/PromptReco-v2/000/147/222/DE0FD043-37D1-DF11-B7A2-0030487C5CE2.root',
##         '/store/data/Run2010B/Electron/RECO/PromptReco-v2/000/147/222/CA5FCBE6-34D1-DF11-93DE-00304879BAB2.root',
##         '/store/data/Run2010B/Electron/RECO/PromptReco-v2/000/147/222/AA65F949-36D1-DF11-A014-003048F1C836.root',
##         '/store/data/Run2010B/Electron/RECO/PromptReco-v2/000/147/222/A6CCAA49-36D1-DF11-8802-003048F024C2.root',
        		
            ] );
else : 
    readFiles.extend( [
		'/store/mc/Spring10/TTbarJets-madgraph/GEN-SIM-RECO/START3X_V26_S09-v1/0006/4C4A0E8D-C946-DF11-BCAC-003048D437D2.root',
		'/store/mc/Spring10/TTbarJets-madgraph/GEN-SIM-RECO/START3X_V26_S09-v1/0006/D87D77D2-C946-DF11-AD67-0030487D5E81.root',
		'/store/mc/Spring10/TTbarJets-madgraph/GEN-SIM-RECO/START3X_V26_S09-v1/0006/B47C6690-C946-DF11-8BC0-003048C692FA.root',
        ] );

if useData :
    process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange(
		
        '132440:157-132440:378',
		'132596:382-132596:382',
		'132596:447-132596:447',
		'132598:174-132598:175',
		'132599:1-132599:379',
		'132599:381-132599:437',
        )
	
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
	process.HLTFilter*
    process.recoJPTJets*
    process.patDefaultSequence* 
    getattr(process,"patPF2PATSequence"+postfix)*
	getattr(process,"patPF2PATSequence"+postfixLoose)* 
    process.flavorHistorySeq *
    process.prunedGenParticles
)

if useData :
#    process.patseq.remove( process.makeGenEvt )
    process.patseq.remove( process.flavorHistorySeq )
    process.patseq.remove( process.prunedGenParticles )
else :
    process.patseq.remove( process.scrapingVeto )
    process.patseq.remove( process.primaryVertexFilter )
    process.patseq.remove( process.HBHENoiseFilter )
    process.patseq.remove( process.HLTFilter )

from PhysicsTools.SelectorUtils.wplusjetsAnalysis_cfi import wplusjetsAnalysis as inputwplusjetsAnalysis

process.shyftEleCalo = cms.EDFilter( 'EDWPlusJets',
                                      inputwplusjetsAnalysis.clone(
                                        jetPtMin = cms.double(25.0),
                                        muJetDR = cms.double(0.),
                                        eleEtMin = cms.double(15),
                                        eleEtaMax = cms.double(3.),
                                        eleEtaMaxLoose = cms.double(3.),
										minJets = cms.int32(0),
                                        useEleMC = cms.bool(True),
										useAntiSelection = cms.bool(False),
                                        cutsToIgnore = cms.vstring( ['== 1 Tight Lepton, Mu Veto',
			                                                         '== 1 Lepton'      ,
	                                                                 'MET Cut'          ,
                                                                     'Z Veto'           ,
																	 'Conversion Veto A',
																	 'Conversion Veto B',
                                                                     'Cosmic Veto'      ,														   
                                                                     '>=1 Jets'         ,
                                                                     '>=2 Jets'         ,
                                                                     '>=3 Jets'         ,
                                                                     '>=4 Jets'         ,
                                                                     '>=5 Jets'                                                                     
                                                                     ] )
                                        )
                                    )

process.shyftEleJPT = process.shyftEleCalo.clone(
    jetSrc = cms.InputTag('selectedPatJetsAK5JPT'),
    metSrc = cms.InputTag('patMETsTC'),
    jetPtMin = cms.double(25.0),
    cutsToIgnore = cms.vstring( ['== 1 Tight Lepton, Mu Veto',
			                     '== 1 Lepton'      ,
	                             'MET Cut'          ,
                                 'Z Veto'           ,
								 'Conversion Veto A',
								 'Conversion Veto B',
                                 'Cosmic Veto'      ,														   
                                 '>=1 Jets'         ,
                                 '>=2 Jets'         ,
                                 '>=3 Jets'         ,
                                 '>=4 Jets'         ,
                                 '>=5 Jets'                                                                     
                                  ] )
    )

process.shyftElePF = process.shyftEleCalo.clone(
    muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
    electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
    jetSrc = cms.InputTag('selectedPatJetsPFlow'),
    metSrc = cms.InputTag('patMETsPFlow'),
    trigSrc = cms.InputTag('patTriggerEvent'),
    jetPtMin = cms.double(20.0),
	cutsToIgnore = cms.vstring( ['== 1 Tight Lepton, Mu Veto',
			                     '== 1 Lepton'      ,
	                             'MET Cut'          ,
                                 'Z Veto'           ,
								 'Conversion Veto A',
								 'Conversion Veto B',
                                 'Cosmic Veto'      ,														   
                                 '>=1 Jets'         ,
                                 '>=2 Jets'         ,
                                 '>=3 Jets'         ,
                                 '>=4 Jets'         ,
                                 '>=5 Jets'                                                                     
                                  ] )
    )

process.shyftSeqCalo = cms.Sequence( process.shyftEleCalo )
process.shyftSeqPF = cms.Sequence( process.shyftElePF )
process.shyftSeqJPT = cms.Sequence( process.shyftEleJPT )


process.isolatedPatElectrons = cms.EDFilter("PATElectronSelector",
    src = cms.InputTag("selectedPatElectrons"),
    cut = cms.string("(dr03TkSumPt+dr03EcalRecHitSumEt+dr03HcalTowerSumEt)/et < 0.2"),
    filter=cms.bool(True)                                       
)

process.isolatedPatElectronsPFlow = cms.EDFilter("PATElectronSelector",
    src = cms.InputTag("selectedPatElectronsPFlow"),
    cut = cms.string(""),
    filter=cms.bool(True)
)

#process.isolatedPatElectronsPFlowLoose = cms.EDFilter("PATElectronSelector",
#    src = cms.InputTag("selectedPatElectronsPFlowLoose"),
#    cut = cms.string(""),
#    filter=cms.bool(True)
#)

process.p1 = cms.Path(
    process.patseq
    )


if not useLooseLeptonPresel and not useWJetsFilter:	
    process.out.SelectEvents.SelectEvents = cms.vstring('p1')
	
elif useWJetsFilter: 
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

elif useLooseLeptonPresel:
    process.p5 = cms.Path(
        process.patseq *
        process.isolatedPatElectrons
        )
    process.p6 = cms.Path(
        process.patseq *
        process.isolatedPatElectronsPFlow
        )
    #process.p7 = cms.Path(
    #    process.patseq *
    #    process.isolatedPatElectronsPFlowLoose
    #    )
    process.out.SelectEvents.SelectEvents = cms.vstring('p5', 'p6')


# rename output file
if useData :
    process.out.fileName = cms.untracked.string('shyft_383_data.root')
else :
    process.out.fileName = cms.untracked.string('shyft_mc_test.root')

# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(5000)

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
    'keep *_*goodPFJets_*_*',
    'keep *_kludgedJPTJets_*_*',
#    'keep patTriggerObjectStandAlones_*_*_*'
    ]

if useData :
    process.out.outputCommands.append( 'keep *_towerMaker_*_*' )
