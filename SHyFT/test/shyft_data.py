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
process.hltLevel1GTSeed.L1SeedsLogicalExpression = cms.string('0 AND NOT (36 OR 37 OR 38 OR 39)')

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
process.patTaus.isoDeposits = cms.PSet()

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
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/F6F55DE7-FD67-DF11-A666-000423D985B0.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/F07DB0FC-D767-DF11-84D5-000423D33970.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/DECFB81E-0968-DF11-9C9E-0030487A18A4.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/CECBE189-CF67-DF11-9CB7-000423D94E70.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/C0B532D2-E167-DF11-AEA1-0030487CAEAC.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/C0AF0837-DA67-DF11-9D30-001D09F295A1.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/BCF8DBF2-F167-DF11-8F84-000423D99660.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/B640EC18-ED67-DF11-A369-001D09F23A84.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/B0E0A03F-0468-DF11-8331-000423D98930.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/AEAD3EDD-D567-DF11-A4B0-0030487C90D4.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/A0EEBCD1-DA67-DF11-8C30-000423D991D4.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/9A8E77CA-D867-DF11-B1E9-0019B9F70607.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/9A883A09-0068-DF11-B14E-0030487A322E.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/8883B0E0-CE67-DF11-BEAD-000423D952C0.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/7E74B613-0E68-DF11-A31C-0030487C8E02.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/7E40E899-F367-DF11-A236-001D09F2462D.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/60DA6322-FB67-DF11-88FC-0030487CD17C.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/6034D55A-E367-DF11-BFE5-001D09F295A1.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/3A8CE618-DD67-DF11-AB2C-000423D987E0.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/22FD643F-D067-DF11-9B48-003048678098.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/141E9A25-E867-DF11-B73D-001617E30D12.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/080CE26D-F367-DF11-B737-001D09F2AD7F.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/06300301-E667-DF11-B2B6-00304879FC6C.root',
'/store/data/Run2010A/Mu/RECO/v2/000/136/100/00DF30E7-DD67-DF11-B9DA-001617DBD5AC.root'



        ] );
process.source.fileNames = readFiles

process.source.inputCommands = cms.untracked.vstring("keep *", "drop *_MEtoEDMConverter_*_*")

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

