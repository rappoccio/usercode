# SHyFT configuration
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *

## global tag for data
process.GlobalTag.globaltag = cms.string('GR_R_36X_V10::All')


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

# Run b-tagging sequences on 35x inputs
#from PhysicsTools.PatAlgos.tools.cmsswVersionTools import *
#run36xOn35xInput(process)

# configure HLT
process.load('L1TriggerConfig.L1GtConfigProducers.L1GtTriggerMaskTechTrigConfig_cff')
process.load('HLTrigger/HLTfilters/hltLevel1GTSeed_cfi')
process.hltLevel1GTSeed.L1TechTriggerSeeding = cms.bool(True)
process.hltLevel1GTSeed.L1SeedsLogicalExpression = cms.string('0 AND (40 OR 41) AND NOT (36 OR 37 OR 38 OR 39)')

# switch on PAT trigger
from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
switchOnTrigger( process )

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


# turn off MC matching for the process
removeMCMatching(process, ['All'])

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
process.selectedPatElectrons.cut = cms.string("pt > 3")
process.selectedPatElectronsPFlow.cut = cms.string("pt > 3")

# remove trigger matching for PF2PAT as that is currently broken
process.patPF2PATSequencePFlow.remove(process.patTriggerSequencePFlow)


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





# Add the files 
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()

readFiles.extend( [
'/store/data/Run2010A/Mu/RECO/v2/000/136/087/7AE9EF4A-7D67-DF11-97EC-0030487CD7CA.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/087/F63A8D4C-6167-DF11-BD3A-000423D944F8.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/088/2630E4C3-7267-DF11-B57C-0030487CD7C6.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/088/2AA4E6A5-7067-DF11-AF34-0030487CD6D2.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/088/38E7B9C2-6B67-DF11-BCF4-0030487C7828.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/088/40E31290-6E67-DF11-B91A-0030487CD6D8.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/088/941764C0-6467-DF11-BACC-000423D996C8.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/088/D83846A0-8367-DF11-8287-0030487C6088.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/089/D802058C-6E67-DF11-B721-000423D98634.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/091/58725305-8567-DF11-B7A2-0030487CD840.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/092/628111AD-AB67-DF11-93EB-000423D9970C.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/094/EEC8EE61-AA67-DF11-9433-001D09F251FE.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/095/5E1E4AB0-A467-DF11-A9D1-0030487CD17C.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/096/A42B63BB-B967-DF11-96D9-001617E30D12.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/097/2C54B8E6-C967-DF11-8688-001D09F24DA8.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/097/4C7E1E9F-CA67-DF11-ACD5-001D09F24498.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/098/D47463AC-D167-DF11-9492-0030487C5CE2.root'


        ] );
process.source.fileNames = readFiles

# let it run

#print
#print "============== Warning =============="
#print "technical trigger filter:    DISABLED"
#print "physics declare bit filter:  DISABLED"
#print "primary vertex filter:       DISABLED"

process.patseq = cms.Sequence(
    process.hltLevel1GTSeed*
    process.scrapingVeto*
    process.hltPhysicsDeclared*
    process.primaryVertexFilter*
    process.patDefaultSequence* 
    getattr(process,"patPF2PATSequence"+postfix)
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
process.maxEvents.input = 10000
process.options.wantSummary = True
process.out.dropMetaData = cms.untracked.string("DROPPED")

from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoCleaning
from PhysicsTools.PatAlgos.patEventContent_cff import patExtraAodEventContent
from PhysicsTools.PatAlgos.patEventContent_cff import patTriggerEventContent
#process.out.outputCommands = patEventContentNoCleaning
#process.out.outputCommands += patExtraAodEventContent
#process.out.outputCommands += patTriggerEventContent
process.out.outputCommands = [
    'drop *_cleanPat*_*_*',
    'keep *_selectedPat*_*_*',
    'keep *_patMETs*_*_*',
    'keep recoPFCandidates_particleFlow_*_*',
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
    'drop *_MEtoEDMConverter_*_*'
    ]

