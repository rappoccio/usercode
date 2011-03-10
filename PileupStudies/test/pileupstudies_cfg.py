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
    #mytrigs = ['HLT_Jet100U*']
    mytrigs = ['HLT_Jet30U*']
    inputJetCorrLabel = ('AK5PF', ['L2Relative', 'L3Absolute'])
    process.source.fileNames = [
#        '/store/mc/Fall10/QCD_Pt_15to3000_TuneZ2_Flat_7TeV_pythia6/GEN-SIM-RECO/START38_V12-v1/0000/02AFCD3B-BECD-DF11-9F32-00215E21DD50.root'
       #'/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0009/E8B2CA4D-42E7-DF11-988C-90E6BA442F16.root',
       #'/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0009/E847D402-12E7-DF11-97C5-003048D4EF1D.root',
       #'/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0009/6EE559BE-11E7-DF11-B575-00145E5513C1.root',
       #'/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/DC4963A1-E0E5-DF11-807E-00D0680BF898.root',
       #'/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/D8F33E3F-58E5-DF11-9FCC-0026B9548CB5.root',
       #'/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/B2D39D4C-63E6-DF11-8CFA-003048CEB070.root',
       #'/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/B28EE7AE-48E5-DF11-9F45-001F29651428.root',
       #'/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/9C7AD216-ACE5-DF11-BE50-001517255D36.root',
       #'/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/788BCB6C-ACE5-DF11-A13C-90E6BA442F1F.root',
       #'dcap:///pnfs/cms/WAX/11/store/mc/Fall10/QCD_Pt_15to3000_TuneZ2_Flat_7TeV_pythia6/GEN-SIM-RECO/START38_V12-v1/0005/F24E17D7-F3CD-DF11-89A4-00215E221938.root'
       '/store/mc/Fall10/QCD_Pt_15to3000_TuneZ2_Flat_7TeV_pythia6/AODSIM/E7TeV_ProbDist_2010Data_BX156_START38_V12-v1/0000/A860E048-30E4-DF11-8572-00215E21DD98.root'
        ]
else :
    mytrigs = ['HLT_Jet*']
    #mytrigs = ['HLT_Jet30U*']
    inputJetCorrLabel = ('AK5PF', ['L2Relative', 'L3Absolute', 'L2L3Residual'])
    process.source.fileNames = [
        '/store/data/Run2010A/JetMET/RECO/Nov4ReReco_v1/0115/BC010982-C8E9-DF11-BC86-001A92810AE6.root',
        '/store/data/Run2010A/JetMET/RECO/Nov4ReReco_v1/0115/BA550932-C1E9-DF11-B5E7-002618943961.root',
        '/store/data/Run2010A/JetMET/RECO/Nov4ReReco_v1/0115/B8DF4C2F-C1E9-DF11-97B7-002618943856.root',
        '/store/data/Run2010A/JetMET/RECO/Nov4ReReco_v1/0115/B8A3DB31-C1E9-DF11-9B82-001A92971BB8.root',
        '/store/data/Run2010A/JetMET/RECO/Nov4ReReco_v1/0115/B84D66D0-CAE9-DF11-928B-001A92810AA6.root',
        '/store/data/Run2010A/JetMET/RECO/Nov4ReReco_v1/0115/B67B11F1-C3E9-DF11-A05F-0018F3D0967A.root',
        '/store/data/Run2010A/JetMET/RECO/Nov4ReReco_v1/0115/B2F41ECD-BFE9-DF11-A93E-0030486792B8.root',
        '/store/data/Run2010A/JetMET/RECO/Nov4ReReco_v1/0115/B0A3D59B-BAE9-DF11-AAED-0026189438A2.root',
        '/store/data/Run2010A/JetMET/RECO/Nov4ReReco_v1/0115/B05DF82F-BDE9-DF11-B516-00248C55CC3C.root',
        '/store/data/Run2010A/JetMET/RECO/Nov4ReReco_v1/0115/A876C29F-C2E9-DF11-9DD6-0026189438A2.root',
        '/store/data/Run2010A/JetMET/RECO/Nov4ReReco_v1/0115/A68C5218-CEE9-DF11-B7BB-0030486792B4.root',
        '/store/data/Run2010A/JetMET/RECO/Nov4ReReco_v1/0115/A4CED181-C8E9-DF11-8E0F-0018F3D0960E.root',
        '/store/data/Run2010A/JetMET/RECO/Nov4ReReco_v1/0115/A48C8A2F-BDE9-DF11-9849-00304867BFBC.root',
        '/store/data/Run2010A/JetMET/RECO/Nov4ReReco_v1/0115/A43A1023-B9E9-DF11-BF1D-001A92971B3C.root',
        '/store/data/Run2010A/JetMET/RECO/Nov4ReReco_v1/0115/A23BA584-BEE9-DF11-8B4F-0026189438C1.root',
        '/store/data/Run2010A/JetMET/RECO/Nov4ReReco_v1/0115/9C6DE4B6-C6E9-DF11-9104-002618943977.root',
        ]


print options

import sys


###############################
####### Global Setup ##########
###############################

if options.useData == False :
    # global tag for MC
    process.GlobalTag.globaltag = cms.string('MC_38Y_V14::All')
else :
    # global tag for 361 data
    #process.GlobalTag.globaltag = cms.string('GR_R_38X_V14::All')
    process.GlobalTag.globaltag = cms.string('GR_R_38X_V15::All')

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
#from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
#switchOnTrigger( process, hltProcess=options.hltProcess )


from HLTrigger.HLTfilters.hltHighLevel_cfi import *
if mytrigs is not None :
    process.hltSelection = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::' + options.hltProcess, HLTPaths = mytrigs)
    process.hltSelection.throw = False
else :
    process.hltSelection = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::' + options.hltProcess, HLTPaths = ['*'])    
    
process.hltSelection.throw = False


process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
                                           vertexCollection = cms.InputTag('offlinePrimaryVertices'),
                                           minimumNDOF = cms.uint32(4) ,
                                           maxAbsZ = cms.double(24), 
                                           maxd0 = cms.double(2) 
                                           )




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

# Default PF2PAT, switch to AK5 jets
from PhysicsTools.PatAlgos.tools.pfTools import *
from PhysicsTools.PatAlgos.tools.coreTools import *
postfixAK5 = "PFlowAK5"
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC=not options.useData, postfix=postfixAK5)
process.pfPileUpPFlowAK5.Enable = False
process.pfJetsPFlowAK5.doAreaFastjet = True
process.pfJetsPFlowAK5.doRhoFastjet = False
process.pfJetsPFlowAK5.Ghost_EtaMax = 6.5


# PF2PAT with only charged hadrons from first PV
postfixPUSubAK5 = "PFlowPUSubAK5"
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC=not options.useData, postfix=postfixPUSubAK5)
process.pfPileUpPFlowPUSubAK5.Enable = True
process.pfJetsPFlowPUSubAK5.doAreaFastjet = True
process.pfJetsPFlowPUSubAK5.doRhoFastjet = False
process.pfJetsPFlowPUSubAK5.Ghost_EtaMax = 6.5


from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
process.kt6PFJets = kt4PFJets.clone(
    src = cms.InputTag("pfNoElectronPFlowAK5"),
    rParam = cms.double(0.6),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True),
    Ghost_EtaMax = cms.double(6.5)
    )
process.kt6PFJetsPUSub = kt4PFJets.clone(
    src = cms.InputTag("pfNoElectronPFlowPUSubAK5"),
    rParam = cms.double(0.6),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True),
    Ghost_EtaMax = cms.double(6.5)
    )

removeSpecificPATObjects(process, ['Taus'], postfix=postfixAK5 )
removeSpecificPATObjects(process, ['Taus'], postfix=postfixPUSubAK5 )

# turn to false when running on data
if options.useData :
    for ipostfix in [ postfixAK5, postfixPUSubAK5] :
        getattr(process, "patPhotons"+ipostfix).embedGenMatch = False
        getattr(process, "patElectrons"+ipostfix).embedGenMatch = False
        getattr(process, "patMuons"+ipostfix).embedGenMatch = False

    removeMCMatching( process, ['All'] )

# Do some configuration of the jet modules
for jetcoll in (process.patJetsPFlowAK5,
                process.patJetsPFlowPUSubAK5
                ) :
    if options.useData == False :
        jetcoll.embedGenJetMatch = True
        jetcoll.getJetMCFlavour = True
        jetcoll.addGenPartonMatch = True
    jetcoll.addBTagInfo = True
    jetcoll.addTagInfos = False
    jetcoll.embedCaloTowers = False
    jetcoll.embedPFCandidates = False


jetidstring = cms.string('pt > 25 & abs(eta) < 2.4')

# Do some configuration of the jet modules
for jetcoll in (process.selectedPatJetsPFlowAK5,
                process.selectedPatJetsPFlowPUSubAK5
                ) :
    jetcoll.cut = jetidstring

from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector
process.goodPatJetsPFlowPUSubAK5 = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                                filterParams = pfJetIDSelector.clone(),
                                                src = cms.InputTag("selectedPatJetsPFlowPUSubAK5"),
                                                filter = cms.bool(True)
                                                )

process.goodPatJetsPFlowAK5 = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                           filterParams = pfJetIDSelector.clone(),                                           
                                           src = cms.InputTag("selectedPatJetsPFlowAK5"),
                                           filter = cms.bool(True)
                                           )

process.jetFilter = cms.EDFilter("CandViewCountFilter",
                                 src = cms.InputTag("goodPatJetsPFlowPUSubAK5"),
                                 minNumber = cms.uint32(2),
                                 maxNumber = cms.uint32(2),
                                 filter=cms.bool(True)
                                  )




# remove trigger matching for PF2PAT as that is currently broken
#process.patPF2PATSequencePFlow.remove(process.patTriggerSequencePFlow)
#process.patPF2PATSequencePFlowPUSub.remove(process.patTriggerSequencePFlowPUSub)
    
# let it run

process.patseq = cms.Sequence(
    process.hltSelection*
    process.scrapingVeto*
    process.primaryVertexFilter*
    process.HBHENoiseFilter*
    getattr(process,"patPF2PATSequence"+postfixPUSubAK5)*
    process.goodPatJetsPFlowPUSubAK5*
    process.jetFilter*
    getattr(process,"patPF2PATSequence"+postfixAK5)*
    process.goodPatJetsPFlowAK5*
    process.kt6PFJets*
    process.kt6PFJetsPUSub
    )


process.p0 = cms.Path(
    process.patseq
    )

process.out.SelectEvents.SelectEvents = cms.vstring('p0')
    
# rename output file
process.out.fileName = cms.untracked.string('pileupstudies_387.root')

# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)


# process all the events
process.maxEvents.input = 3000
process.options.wantSummary = True
process.out.dropMetaData = cms.untracked.string("DROPPED")




process.source.inputCommands = cms.untracked.vstring("keep *", "drop *_MEtoEDMConverter_*_*")



process.out.outputCommands = [
    'drop *_cleanPat*_*_*',
    'keep *_selectedPat*_*_*',
    'keep *_goodPat*_*_*',    
    'keep *_patMETs*_*_*',
    'drop patJets_selectedPatJets*__PAT',
#    'keep recoPFCandidates_particleFlow_*_*',
    'drop recoPFCandidates_selected*_pfCandidates_PAT',
    'keep *_offlineBeamSpot_*_*',
    'keep *_offlinePrimaryVertices*_*_*',
    'drop patPFParticles_*_*_*',
    'keep patTriggerPaths_patTrigger*_*_*',
    'keep patTriggerEvent_patTriggerEvent*_*_*',
    'drop *_*KT6*_*_*',
    'keep double_*PFlow*_*_*',
    'keep double_*kt6*_*_*',    
    'keep *_TriggerResults_*_*',
    'keep *_hltTriggerSummaryAOD_*_*',
    'keep *_ak5GenJets_*_*',
    'drop patTaus_*_*_*',
    'drop recoBaseTagInfosOwned_selected*_tagInfos_PAT',
    'keep recoGenJets_selected*_*_PAT',
    'drop CaloTowers_selected*_caloTowers_PAT'
    ]

if options.useData :
    process.out.outputCommands += ['drop *_MEtoEDMConverter_*_*',
                                   'keep LumiSummary_lumiProducer_*_*'
                                   ]
else :
    process.out.outputCommands += ['keep recoGenJets_ak5GenJets_*_*',
                                   'keep recoGenJets_kt6GenJets_*_*',
                                   'keep GenRunInfoProduct_generator_*_*',
                                   'keep GenEventInfoProduct_generator_*_*'
                                   ]

