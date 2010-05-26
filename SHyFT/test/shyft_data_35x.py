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
from PhysicsTools.PatAlgos.tools.cmsswVersionTools import *
run36xOn35xInput(process)

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
'/store/data/Run2010A/Mu/RECO/v1/000/136/082/3AC8E7CF-E466-DF11-9FC2-001D09F29524.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/082/3C4424FE-D366-DF11-94E3-0030487A18A4.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/082/5C78224D-D866-DF11-95F6-003048D2BC30.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/082/A8C6EF25-F266-DF11-948A-001D09F242EF.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/083/005827E1-1A67-DF11-8863-000423D944F0.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/083/06FE3A30-DF66-DF11-9B39-003048D2C020.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/083/2CD05D8A-1E67-DF11-8652-001D09F23C73.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/083/3239FD76-F166-DF11-9E2F-001D09F2423B.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/083/3ECCEDEC-0E67-DF11-BE5D-000423D944F0.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/083/48478122-E466-DF11-8DA4-001D09F24F1F.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/083/500CAD70-DE66-DF11-BE3C-0030487CD7EE.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/083/521FAFF7-F466-DF11-AFDF-001D09F242EA.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/083/5C7F93B8-0367-DF11-9DD7-0030486780AC.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/083/6A2183BA-E966-DF11-B177-003048673374.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/083/76BEA03D-E666-DF11-A22A-001D09F25041.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/083/7ABB5B80-EC66-DF11-8D62-0030487CD16E.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/083/945FBE42-E166-DF11-B112-000423D951D4.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/083/AA790088-0667-DF11-AADB-001D09F2841C.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/083/B825B34E-FB66-DF11-B201-000423D9880C.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/083/BE2B402A-1367-DF11-92AC-001D09F25456.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/083/C67A6AE5-2167-DF11-B625-001D09F24259.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/083/CEC8BA77-2067-DF11-9029-000423D98EC4.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/083/D2D16316-FE66-DF11-B556-001D09F2AF96.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/083/FA9AFE72-0B67-DF11-806C-001D09F2441B.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/084/32F453AE-4367-DF11-885B-000423D951D4.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/084/76D93F86-3367-DF11-B8AC-0030487CD162.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/084/9E6CAA09-2B67-DF11-BD6A-001D09F282F5.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/084/9E6E0E1C-3067-DF11-BCBF-0030487CAF5E.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/084/ACDA4F34-3967-DF11-A9AB-001D09F24DDF.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/084/B4FE9F12-3E67-DF11-BE29-0030487C8CB8.root',
'/store/data/Run2010A/Mu/RECO/v1/000/136/086/90BD6D32-4767-DF11-8A24-0030487CD6D2.root'



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

