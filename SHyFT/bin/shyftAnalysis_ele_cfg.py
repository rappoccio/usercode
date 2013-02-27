import FWCore.ParameterSet.Config as cms

process = cms.Process("FWLitePlots")
import string
import sys

filesin = sys.argv[2]
outfile = sys.argv[3]

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
    pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
    eEt = cms.double( 30.0 ),
    jetPtMin = cms.double(30.0),
    minJets = cms.int32(5),
    eRelIso = cms.double(0.1),
    ePlusJets = cms.bool(True),
    muPlusJets = cms.bool(False),
    useNoPFIso = cms.bool(False),
    cutsToIgnore=cms.vstring('Trigger'),
    rhoSrc  = cms.InputTag('kt6PFJets', 'rho'),
    useData = cms.bool(False),
    reweightPU = cms.bool(False),
    reweightPU3D = cms.bool(False),
    jetScale =cms.double(0.1),
    doMC = cms.bool(True),
    puUp = cms.bool(True),  
    )

process.inputs = cms.PSet (
    fileNames = infilenames,
    maxEvents = cms.int32(-1)
)


process.outputs = cms.PSet (
    outputName = cms.string(outfile)
)
