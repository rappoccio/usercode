import FWCore.ParameterSet.Config as cms

process = cms.Process("FWLitePlots")
import string
import sys

filesin = sys.argv[2]
outfile = sys.argv[3]
#outfile = 'wjets_ttbsm.root'
#filesin = 'wjets_ttbsm.txt'

#prepend = 'dcap:///pnfs/cms/WAX/11'
prepend = ''

print 'Input files from ' + filesin
print 'Output file = ' + outfile

infilenames = cms.vstring()
txtfile = open(filesin)
for line in txtfile.readlines():
   infilenames.append( prepend + string.replace(line,'\n',''))

print infilenames

from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis

process.shyftAnalysis = inputShyftAnalysis.clone(
    muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
    electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
    metSrc = cms.InputTag('patMETsPFlow'),
    jetSrc = cms.InputTag('goodPatJetsPFlow'),
    #jetSrc = cms.InputTag('selectedPatJetsPFlow'),
    pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
    jetPtMin = cms.double(25.0),
    minJets = cms.int32(5),
    eRelIso = cms.double(0.1),
    ePlusJets = cms.bool(True),
    muPlusJets = cms.bool(False),
    #usePFIso = cms.bool(True), ###
    metMin = cms.double(0.),
    wMTMax = cms.double(10000.),
    cutsToIgnore=cms.vstring('Trigger'),

    pvSelector = cms.PSet(
    pvSrc = cms.InputTag('goodOfflinePrimaryVertices'),
    minNdof = cms.double(4.0),
    maxZ = cms.double(15.0),
    maxRho = cms.double(2.0),
    ),

    muonIdTight = cms.PSet(
    version = cms.string('FALL10'),
    Chi2 = cms.double(10.0),
    D0 = cms.double(0.02),
    ED0 = cms.double(999.0),
    SD0 = cms.double(999.0),
    NHits = cms.int32(11),
    NValMuHits = cms.int32(0),
    ECalVeto = cms.double(999.0),
    HCalVeto = cms.double(999.0),
    RelIso = cms.double(0.05),
    LepZ = cms.double(1.0),
    nPixelHits = cms.int32(1),
    nMatchedStations=cms.int32(1),
    cutsToIgnore = cms.vstring('ED0', 'SD0', 'ECalVeto', 'HCalVeto'),
    RecalcFromBeamSpot = cms.bool(False),
    beamLineSrc = cms.InputTag("offlineBeamSpot"),
    pvSrc = cms.InputTag("goodOfflinePrimaryVertices"),
    ),
    
    muonIdLoose = cms.PSet(
    version = cms.string('FALL10'),
    Chi2 = cms.double(999.0),
    D0 = cms.double(999.0),
    ED0 = cms.double(999.0),
    SD0 = cms.double(999.0),
    NHits = cms.int32(-1),
    NValMuHits = cms.int32(-1),
    ECalVeto = cms.double(999.0),
    HCalVeto = cms.double(999.0),
    RelIso = cms.double(0.2),
    LepZ = cms.double(1.0),
    nPixelHits = cms.int32(1),
    nMatchedStations=cms.int32(1),        
    cutsToIgnore = cms.vstring('Chi2', 'D0', 'ED0', 'SD0', 'NHits','NValMuHits','ECalVeto','HCalVeto','LepZ','nPixelHits','nMatchedStations'),
    RecalcFromBeamSpot = cms.bool(False),
    beamLineSrc = cms.InputTag("offlineBeamSpot"),
    pvSrc = cms.InputTag("goodOfflinePrimaryVertices"),
    ),
    
    #metMax = cms.double(25.),
    
    #***********Uncomment if want to test on WJets, ZJets, Vqq, WcJets******************
    #sampleName="Wjets",
    #sampleName = "Top",
    #doMC = True,
    #heavyFlavour = True,
   #***********************************************************************************
    
    #useEleMC   = cms.bool(True),

    #********Uncomment if want to produce anti-electrons***************************
    #useAntiSelection = cms.bool(True),
    #useEleMC  = cms.bool(False)
    #*******************************************************************************
    
    )

process.inputs = cms.PSet (
    fileNames = infilenames,
    maxEvents = cms.int32(-1)
)


process.outputs = cms.PSet (
    outputName = cms.string(outfile)
)
