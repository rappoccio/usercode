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
    pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
    jetPtMin = cms.double(30.0),
    minJets = cms.int32(5),
    eRelIso = cms.double(0.1),
    ePlusJets = cms.bool(True),
    muPlusJets = cms.bool(False),
    usePFIso = cms.bool(False), ###
    metMin = cms.double(0.),
    wMTMax = cms.double(10000.),
    #useVBTFDetIso  = cms.bool(True),
    cutsToIgnore=cms.vstring('Trigger'),   
    jetScale =cms.double(0.1),
    doMC = cms.bool(True),
    puUp = cms.bool(True),
    #metMax = cms.double(25.),
    
    #***********Uncomment if want to test on WJets, ZJets, Vqq, WcJets******************
    #sampleName="Wjets",
    #sampleName = "Top",
    #doMC = True,
    #heavyFlavour = True,  
    )

process.inputs = cms.PSet (
    fileNames = infilenames,
    maxEvents = cms.int32(5000)
)


process.outputs = cms.PSet (
    outputName = cms.string(outfile)
)
