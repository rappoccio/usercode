import FWCore.ParameterSet.Config as cms
import sys

process = cms.Process("JetAnlzr")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:/tmp/mgeisler/GluGluToHToGG_M-120_7TeV-pythia6.root')
)
		
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(5)
)
		
Outfile = ""
if len(sys.argv)>2:
    Outfile= "JetAnlzr_" + str(sys.argv[2]) + ".root"
else:
    Outfile= "JetAnlzr.root"

process.TFileService = cms.Service('TFileService',
    fileName = cms.string(Outfile),
    closeFileFast = cms.untracked.bool(True),
)
    
print " Outfile set to " + Outfile
		
### conditions
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = 'MC_44_V12::All'

### standard includes
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryPilot2_cff')
process.load("Configuration.StandardSequences.RawToDigi_cff")
process.load("Configuration.EventContent.EventContent_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")

### validation-specific includes
process.load("MGeisler.PF_PU_AssoMap.cuts_cff")
process.load("Validation.Configuration.postValidation_cff")
process.TrackAssociatorByHits.SimToRecoDenominator = cms.string('reco')
from MGeisler.TrackValidator.TrackingParticleSelection_cfi import *

########### track selection configuration ########
process.cutsRecoTracks.minRapidity = cms.double(-2.5)
process.cutsRecoTracks.maxRapidity = cms.double(2.5)
		
TightSelection=False

if TightSelection:
    print " Tight Track selection is used"
    process.cutsRecoTracks.quality = cms.vstring('highPurity')
    process.cutsRecoTracks.tip = cms.double(3.)
    process.cutsRecoTracks.lip = cms.double(30.)
    process.cutsRecoTracks.ptMin = cms.double(1.)
else:
    print " Loose Track selection is used"
    process.cutsRecoTracks.quality = cms.vstring('highPurity','tight','loose')
    process.cutsRecoTracks.tip = cms.double(120.)
    process.cutsRecoTracks.lip = cms.double(280.)
    process.cutsRecoTracks.ptMin = cms.double(0.1)
    
    TrackingParticleSelectionGeneral.tipTP = cms.double(120.0)
    TrackingParticleSelectionGeneral.lipTP = cms.double(280.0)
    TrackingParticleSelectionGeneral.ptMinTP = cms.double(0.1)
    TrackingParticleSelectionGeneral.minHitTP = cms.int32(3)

### AssociationMap-specific includes		
from MGeisler.PF_PU_AssoMap.pf_pu_assomap_cfi import Tracks2Vertex
		
process.Tracks2Vertex1st = Tracks2Vertex.clone(
	AllSteps = cms.untracked.bool(False),
	VertexAssOneDim = cms.untracked.bool(False),
	VertexAssUseAbsDistance = cms.untracked.bool(True),
)
			 
process.Tracks2VertexAll = Tracks2Vertex.clone(
	AllSteps = cms.untracked.bool(True),
	VertexAssOneDim = cms.untracked.bool(False),
	VertexAssUseAbsDistance = cms.untracked.bool(True),
)		  
				  
process.FirstVertexTrackCollection1st = cms.EDProducer('FirstVertexTracks',
	  TrackCollection = cms.InputTag('cutsRecoTracks'),
          VertexTrackAssociationMap = cms.InputTag('Tracks2Vertex1st'),
)		  
				       
process.FirstVertexTrackCollectionAll = cms.EDProducer('FirstVertexTracks',
	  TrackCollection = cms.InputTag('cutsRecoTracks'),
          VertexTrackAssociationMap = cms.InputTag('Tracks2VertexAll'),
)
				
process.trackValidator = cms.EDAnalyzer('TrackValidator',
	tcLabel = cms.VInputTag(cms.InputTag("cutsRecoTracks"),cms.InputTag("FirstVertexTrackCollection1st"),cms.InputTag("FirstVertexTrackCollectionAll"),),
    	tcRefLabel = cms.InputTag("generalTracks"),
    	PULabel = cms.InputTag("addPileupInfo"),
    	TPLabel = cms.InputTag("mergedtruth","MergedTrackTruth"),
	ignoremissingtrackcollection=cms.bool(False),
	UseLogPt=cms.bool(False),
	generalTpSelector = TrackingParticleSelectionGeneral,
)
	
process.PFCandidates1st = cms.EDProducer('PFCand_NoPU_WithAM',
	  PFCandidateCollection = cms.InputTag('particleFlow'),
	  VertexCollection = cms.InputTag('offlinePrimaryVertices'),
	  VertexTrackAssociationMap = cms.InputTag('Tracks2Vertex1st'),
	  ConversionsCollection = cms.InputTag('allConversions'),
	  V0KshortCollection = cms.InputTag('generalV0Candidates','Kshort'),
	  V0LambdaCollection = cms.InputTag('generalV0Candidates','Lambda'),
	  NIVertexCollection = cms.InputTag('particleFlowDisplacedVertex'),
)

process.PFCandidatesAll = cms.EDProducer('PFCand_NoPU_WithAM',
	  PFCandidateCollection = cms.InputTag('particleFlow'),
	  VertexCollection = cms.InputTag('offlinePrimaryVertices'),
	  VertexTrackAssociationMap = cms.InputTag('Tracks2VertexAll'),
	  ConversionsCollection = cms.InputTag('allConversions'),
	  V0KshortCollection = cms.InputTag('generalV0Candidates','Kshort'),
	  V0LambdaCollection = cms.InputTag('generalV0Candidates','Lambda'),
	  NIVertexCollection = cms.InputTag('particleFlowDisplacedVertex'),
)
	
from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets		
process.kt6PFJets1st = kt4PFJets.clone(
	src = cms.InputTag("PFCandidates1st"),
	rParam = cms.double(0.6),
	doAreaFastjet = cms.bool(True),
	doRhoFastjet = cms.bool(True),
	Ghost_EtaMax = cms.double(6.5),
)

process.kt6PFJetsAll = kt4PFJets.clone(
	src = cms.InputTag("PFCandidatesAll"),
	rParam = cms.double(0.6),
	doAreaFastjet = cms.bool(True),
	doRhoFastjet = cms.bool(True),
	Ghost_EtaMax = cms.double(6.5)
)

process.kt6GenJetsn = cms.EDProducer("CandViewNtpProducer",
	src = cms.InputTag("kt6GenJets"),
    	lazyParser = cms.untracked.bool(True),
    	prefix = cms.untracked.string(""),
    	eventInfo = cms.untracked.bool(True),
	variables = cms.VPSet(
		 cms.PSet(
		   tag = cms.untracked.string("pt"),
		   quantity = cms.untracked.string("pt")
		 ),
            	cms.PSet(
                   tag = cms.untracked.string("eta"),
                   quantity = cms.untracked.string("eta")
             	),
            	cms.PSet(
                   tag = cms.untracked.string("phi"),
                   quantity = cms.untracked.string("phi")
            	), 
	),     
)

process.kt6PFJets1stn = cms.EDProducer("CandViewNtpProducer", 
    src = cms.InputTag("kt6PFJets1st"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string(""),
    eventInfo = cms.untracked.bool(True),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
        ),
        cms.PSet(
            tag = cms.untracked.string("jetArea"),
            quantity = cms.untracked.string("jetArea")
        ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("eta")
        ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
        ),
    )
)

process.kt6PFJetsAlln = cms.EDProducer("CandViewNtpProducer", 
    src = cms.InputTag("kt6PFJetsAll"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string(""),
    eventInfo = cms.untracked.bool(True),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
        ),
        cms.PSet(
            tag = cms.untracked.string("jetArea"),
            quantity = cms.untracked.string("jetArea")
        ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("eta")
        ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
        ),
    )
)

process.jetanalyzer = cms.EDAnalyzer('JetAnlzr',
	genJets = cms.string("kt6GenJetsn"),
	recoJets = cms.vstring("kt6PFJetsAlln","kt6PFJets1stn"),
	PileUpInfo = cms.string("addPileupInfo")
)

# paths	

### produce the association map
process.T2V = cms.Sequence(
      process.Tracks2Vertex1st
    + process.Tracks2VertexAll
)

### produce a collection of tracks associated to the first vertex
process.FVTC = cms.Sequence(
      process.FirstVertexTrackCollection1st
    + process.FirstVertexTrackCollectionAll
)

### do the efficiency and fake rate analyses for the charged particles
process.MTV = cms.Sequence(
      #process.multiTrackValidator
      process.trackValidator
)

### produce a collection of PFCandidates associated to the first vertex
process.PFCand = cms.Sequence(
      process.PFCandidates1st
    + process.PFCandidatesAll
)

### produce a jet collection from the PFCandidates
process.PFJ = cms.Sequence(
      process.kt6PFJets1st
    + process.kt6PFJetsAll
)

### produce the edm nTuples from the jet collection
process.nTs = cms.Sequence(
      process.kt6GenJetsn
    + process.kt6PFJets1stn
    + process.kt6PFJetsAlln
)
		
### do the jet analysis
						  
process.JA = cms.Sequence(
      process.jetanalyzer
)

process.p = cms.Path(
      process.cutsRecoTracks    ### produce the track collection for the analysis of of the charged tracks
    * process.T2V		### produce the association map
    * process.FVTC		### produce a collection of tracks associated to the first vertex
    * process.MTV		### do the efficiency and fake rate analyses for the charged particles 	
    #* process.PFCand		### produce a collection of PFCandidates associated to the first vertex	
    #* process.PFJ		### produce a jet collection from the PFCandidates
    #* process.nTs		### produce the edm nTuples from the jet collection
    #* process.JA		### do the jet analysis	
)

process.schedule = cms.Schedule(
      process.p
)