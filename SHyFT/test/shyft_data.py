# This is an example PAT configuration showing the usage of PAT on minbias data

# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *

## global tag for data
process.GlobalTag.globaltag = cms.string('GR10_P_V2::All')

# turn off MC matching for the process
removeMCMatching(process, ['All'])




# get the 7 TeV GeV jet corrections
from PhysicsTools.PatAlgos.tools.jetTools import *
switchJECSet( process, "Summer09_7TeV_ReReco332")

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


#_____ SELECTION ________________________________________________ 	 
#
process.selectedPatJets.cut = cms.string("pt > 20")
process.patJets.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfos")
    )
# electrons
process.selectedPatElectrons.cut = cms.string('pt > 3.0')
process.patElectrons.isoDeposits = cms.PSet()
# muons
process.selectedPatMuons.cut = cms.string("pt > 3.0")
process.patMuons.isoDeposits = cms.PSet()
# taus
process.selectedPatTaus.cut = cms.string("pt > 5 & abs(eta) < 3")
# photons
process.patPhotons.isoDeposits = cms.PSet()
#taus
process.patTaus.isoDeposits = cms.PSet()


#try to clone what we have up to here.  
from PhysicsTools.PatAlgos.tools.helpers import cloneProcessingSnippet
cloneProcessingSnippet(process, process.patDefaultSequence, "Std")

# add PF2PAT
from PhysicsTools.PatAlgos.tools.pfTools import *
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC = False)

# remove trigger matching for PF2PAT as that is currently broken
process.patDefaultSequence.remove(process.patTriggerSequence)

# now change the PF jet cut to 10 GeV
process.selectedPatJets.cut = cms.string("pt > 15")

# FILTERS:
# One of : >=1 mu (PF or std)
#          >=1 e (PF or std)
#          >=2 jet (PF or std)
process.muonFilter = cms.EDFilter("CandViewCountFilter",
                                  src = cms.InputTag("selectedPatMuonsStd"),
                                  minNumber = cms.uint32(1),
                                  )

process.pfMuonFilter = cms.EDFilter("CandViewCountFilter",
                                    src = cms.InputTag("selectedPatMuons"),
                                    minNumber = cms.uint32(1),
                                    )

process.electronFilter = cms.EDFilter("CandViewCountFilter",
                                  src = cms.InputTag("selectedPatElectronsStd"),
                                  minNumber = cms.uint32(1),
                                  )

process.pfElectronFilter = cms.EDFilter("CandViewCountFilter",
                                    src = cms.InputTag("selectedPatElectrons"),
                                    minNumber = cms.uint32(1),
                                    )

process.jetFilter = cms.EDFilter("CandViewCountFilter",
                                  src = cms.InputTag("selectedPatJetsStd"),
                                  minNumber = cms.uint32(2),
                                  )

process.pfJetFilter = cms.EDFilter("CandViewCountFilter",
                                    src = cms.InputTag("selectedPatJets"),
                                    minNumber = cms.uint32(2),
                                    )





# Add the files 
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()

readFiles.extend( [
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/EEE6A6A0-4742-DF11-B29E-0019B9F72F97.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/EAB2FD5C-3A42-DF11-AE5F-000423D98804.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/EA9A1F00-4742-DF11-898A-001D09F25438.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/E093E3BA-4242-DF11-ABD8-0030487CD704.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/CE7C3100-4742-DF11-A410-001D09F24F1F.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/CE70DDD4-5E42-DF11-AED6-001D09F24448.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/CA0F3E00-4742-DF11-B993-001D09F252DA.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/C6F10ED6-4442-DF11-8E2A-0016177CA778.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/C4E0CBB7-3B42-DF11-BB57-000423D98FBC.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/C238AD9E-4042-DF11-BC5A-0030487CD178.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/BE486F9E-4042-DF11-80FD-001617C3B76E.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/BCBB11D6-4A42-DF11-A2F4-001D09F24489.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/B6A974E6-3F42-DF11-A8B1-0030487C8CBE.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/B00EBC9E-4042-DF11-9961-0030487C6A66.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/ACBE1B97-3C42-DF11-9CAB-000423D94534.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/A299B019-3B42-DF11-8079-001617E30F50.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/A0EFA323-4442-DF11-91F1-0030487CD7B4.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/967CB9A2-4042-DF11-95D2-001617C3B70E.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/94B61F24-4442-DF11-BE00-0030487CD812.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/8A431F24-4442-DF11-8D10-0030487CD77E.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/8A385724-4442-DF11-B326-0030487CD906.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/760D60DE-3D42-DF11-82A2-000423D99EEE.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/70884523-4442-DF11-80F9-001617C3B5D8.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/703AEB7D-3C42-DF11-BA8A-000423D987FC.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/668141EE-3842-DF11-BACA-0030487C8CBE.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/60662E79-3C42-DF11-A001-000423D98EC8.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/5AADE2E4-4442-DF11-9B0F-0030487CD178.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/4E89AE58-3A42-DF11-AB48-003048D2C092.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/4E484072-4342-DF11-9128-0030487CD76A.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/4AD6A4A2-4742-DF11-B95B-001D09F24691.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/4AC5E83B-3F42-DF11-AB77-0030487CF41E.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/469EA393-3E42-DF11-9FAE-000423DD2F34.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/3EF70B15-3B42-DF11-A9D7-000423D98AF0.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/3A910E07-4242-DF11-842C-0030487CD6DA.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/385854E5-4442-DF11-A8B9-0030487CD76A.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/361DB55A-6542-DF11-9FFE-0030487CD718.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/266D69ED-3842-DF11-8935-001D09F253FC.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/0E4D13B5-4A42-DF11-9D05-001D09F29597.root',
'/store/data/Commissioning10/MinimumBias/RECO/v8/000/132/716/0E17871B-3D42-DF11-B3C7-001D09F2432B.root'

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
    process.patDefaultSequenceStd* 
    process.patDefaultSequence
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
process.out.fileName = cms.untracked.string('shyft_7TeV_firstdata_357_pat.root')

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
    'keep *_patMETsTriggerMatchStd_*_*'
    ]

