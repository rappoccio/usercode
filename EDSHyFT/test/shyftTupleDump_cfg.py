import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")


###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')


options.register('usePDFs',
                 0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Ignore trigger in selection")



options.register('useData',
                 1,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Use data (1) or MC (0)")



options.parseArguments()

print options

import sys

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/cjenkins/TTJets_TuneZ2_7TeV-madgraph-tauola/TTJets_TuneZ2_7TeV_madgraphTauola_Summer11_PU_S4_START42_V11_v1/b2fdf3a86ce2d334c5e8a1bb8085ae3f/ttbsm_42x_mc_204_1_4PV.root'

)
)

if len(options.inputFiles) > 0 :
    process.source.fileNames = options.inputFiles



payloads = [
    'Jec11_V3_L1FastJet_AK5PFchs.txt',
    'Jec11_V3_L2Relative_AK5PFchs.txt',
    'Jec11_V3_L3Absolute_AK5PFchs.txt',
    'Jec11_V3_Uncertainty_AK5PFchs.txt'
]


## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100000) )

from Analysis.SHyFT.shyftPFSelection_cfi import shyftPFSelection as shyftPFSelectionInput


process.load('Analysis.PdfWeights.pdfWeightProducer_cfi')


process.pfShyftProducer = cms.EDFilter('EDSHyFTPFSelector',
                                    shyftPFSelection = shyftPFSelectionInput.clone(
                                           jetSrc = cms.InputTag('goodPatJetsPFlow'),
                                           jecPayloads = cms.vstring( payloads )
                                        )
                                    )


## std sequence to produce the kinematic fit for semi-leptonic events
process.load('TopQuarkAnalysis.TopKinFitter.TtSemiLepKinFitProducer_Muons_cfi')

process.kinFitTtSemiLepEvent.jets = cms.InputTag("pfShyftProducer", "jets")
process.kinFitTtSemiLepEvent.mets = cms.InputTag("pfShyftProducer", "MET")
process.kinFitTtSemiLepEvent.leps = cms.InputTag("pfShyftProducer", "muons")

process.load("TopQuarkAnalysis.TopKinFitter.TtSemiLepKinFitProducer_Muons_cfi")



process.pfShyftTupleJets = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducer", "jets"),
    lazyParser = cms.untracked.bool(True),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("mass"),
            quantity = cms.untracked.string("mass")
            ),
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
        cms.PSet(
            tag = cms.untracked.string("ssvhe"),
            quantity = cms.untracked.string("bDiscriminator('simpleSecondaryVertexHighEffBJetTags')")
            ),
        cms.PSet(
            tag = cms.untracked.string("secvtxMass"),
            quantity = cms.untracked.string("userFloat('secvtxMass')")
            ),
        cms.PSet(
            tag = cms.untracked.string("jetArea"),
            quantity = cms.untracked.string("jetArea")
            ),
        )  
    )

if not options.useData :
    process.pfShyftTupleJets.variables.append(
        cms.PSet(
            tag = cms.untracked.string("flavor"),
            quantity = cms.untracked.string("partonFlavour()")
            )
        )


process.pfShyftTupleMuons = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducer", "muons"),
    lazyParser = cms.untracked.bool(True),
    eventInfo = cms.untracked.bool(False),
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
        cms.PSet(
            tag = cms.untracked.string("pfiso"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso') + " +
                                            "userIsolation('pat::PfNeutralHadronIso') + " +
                                            "userIsolation('pat::PfGammaIso')"
                                            )
            ),
        )  
    )


process.pfShyftTupleMET = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducer", "MET"),
    lazyParser = cms.untracked.bool(True),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
            )
        )  
    )


process.pfShyftTupleElectrons = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducer", "electrons"),
    lazyParser = cms.untracked.bool(True),
    eventInfo = cms.untracked.bool(False),
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
        cms.PSet(
            tag = cms.untracked.string("pfiso"),
            quantity = cms.untracked.string("userIsolation('PfAllParticleIso')")
            ),
        )  
    )


process.p = cms.Path(
    process.pfShyftProducer*
    process.pfShyftTupleJets*
    process.pfShyftTupleMuons*
    process.pfShyftTupleElectrons*
    process.pfShyftTupleMET
    )

if options.usePDFs :
    process.p += process.pdfWeightProducer


process.MessageLogger.cerr.FwkReport.reportEvery = 1000




process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string("TTJets_TuneZ2_7TeV_madgraphTauola_Summer11_PU_S4_START42_V11_v1_shyftDump.root"),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
                               outputCommands = cms.untracked.vstring('drop *',
                                                                      #'keep *_pfShyftProducer_*_*',
                                                                      'keep *_pfShyftTuple*_*_*',
                                                                      'keep *_pdfWeightProducer_*_*'
                                                                      #'keep *_kinFitTtSemiLepEvent_*_*'
                                                                      ) 
                               )
process.outpath = cms.EndPath(process.out)

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.out.dropMetaData = cms.untracked.string("DROPPED")
