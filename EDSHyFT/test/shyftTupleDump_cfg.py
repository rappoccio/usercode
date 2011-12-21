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
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Use data (1) or MC (0)")

options.register('useMuTrigs',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Use muon triggers (1) or not (0)")

options.register('useEleTrigs',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Use electron triggers (1) or not (0)")

options.register('useLooseElectrons',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Add loose electron collection (1) or not (0)")

options.register('useLooseMuons',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Add loose muon collection (1) or not (0)")

options.parseArguments()

print options

useData = True
if options.useData == 0 :
    useData = False

import sys


payloadsData = [
    'Jec11_V3_L1FastJet_AK5PFchs.txt',
    'Jec11_V3_L2Relative_AK5PFchs.txt',
    'Jec11_V3_L3Absolute_AK5PFchs.txt',
    'Jec11_V3_L2L3Residual_AK5PFchs.txt',
    'Jec11_V3_Uncertainty_AK5PFchs.txt',    
]

payloadsMC = [
    'Jec11_V3_L1FastJet_AK5PFchs.txt',
    'Jec11_V3_L2Relative_AK5PFchs.txt',
    'Jec11_V3_L3Absolute_AK5PFchs.txt',
    'Jec11_V3_Uncertainty_AK5PFchs.txt',    
]

if useData :
    jetSmear = 0.0
    payloads = payloadsData
    inputFiles = [
        'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/vasquez/SingleMu/ttbsm_v9_Run2011A-PromptReco-v4/f8e845a0332c56398831da6c30999af1/ttbsm_42x_data_326_1_ZF4.root'
        ]

else :
    jetSmear = 0.1
    payloads = payloadsMC
    inputFiles = [
        'dcap:///pnfs/cms/WAX/11//store/user/lpctlbsm/srappocc/TTJets_TuneZ2_7TeV-madgraph-tauola/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_9_1_7Fg.root'
        ]


from HLTrigger.HLTfilters.hltHighLevel_cfi import *
if options.useMuTrigs == 0 and options.useEleTrigs == 0 :
    process.hltSelection = cms.Sequence()
else :
    process.hltSelectionMu = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths = ['HLT_Mu30_v1',
                                                                                                       'HLT_Mu30_v2',
                                                                                                       'HLT_Mu30_v3',
                                                                                                       'HLT_Mu30_v4',
                                                                                                       'HLT_Mu30_v5',
                                                                                                       'HLT_Mu30_v7',
                                                                                                       'HLT_Mu40_eta2p1_v1',
                                                                                                       'HLT_Mu40_eta2p1_v4',
                                                                                                       'HLT_Mu40_eta2p1_v5',
                                                                                                       ])
    process.hltSelectionEle = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths =  ['HLT_Ele45_CaloIdVT_TrkIdT_v1',
                                                                                                         'HLT_Ele45_CaloIdVT_TrkIdT_v2',
                                                                                                         'HLT_Ele45_CaloIdVT_TrkIdT_v3',
                                                                                                         'HLT_Ele52_CaloIdVT_TrkIdT_v1',
                                                                                                         'HLT_Ele52_CaloIdVT_TrkIdT_v2',
                                                                                                         'HLT_Ele65_CaloIdVT_TrkIdT_v1',
                                                                                                         'HLT_Ele25_WP80_PFMT40_v2'
                                                                                                         ])
    process.hltSelectionMu.throw = False
    process.hltSelectionEle.throw = False

    if options.useMuTrigs == 0 and options.useEleTrigs == 1 :
        process.hltSelection = cms.Sequence( ~process.hltSelectionMu * process.hltSelectionEle )
    elif options.useMuTrigs == 1 and options.useEleTrigs == 0 :
        process.hltSelection = cms.Sequence( ~process.hltSelectionEle * process.hltSelectionMu )
    elif options.useMuTrigs == 1 and options.useEleTrigs == 1 :
        process.hltSelection = cms.Sequence( process.hltSelectionEle * process.hltSelectionMu )

process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring( inputFiles )
)

if len(options.inputFiles) > 0 :
    process.source.fileNames = options.inputFiles



## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100000) )

from Analysis.SHyFT.shyftselection_cfi import wplusjetsAnalysis as shyftSelectionInput


if options.usePDFs: 
	process.load('Analysis.PdfWeights.pdfWeightProducer_cfi')


process.pfShyftProducerMu = cms.EDFilter('EDSHyFTSelector',
                                    shyftSelection = shyftSelectionInput.clone(
        muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
        electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
        metSrc = cms.InputTag('patMETsPFlow'),
        jetSrc = cms.InputTag('goodPatJetsPFlow'),
        pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
        ePlusJets = cms.bool( False ),
        muPlusJets = cms.bool( True ),
        jetPtMin = cms.double(10.0),##
        minJets = cms.int32(1),
        metMin = cms.double(0.0),
	muPtMin = cms.double(35.0),
        identifier = cms.string('PFMu'),
        cutsToIgnore=cms.vstring( ['Trigger'] ),
        useData = cms.bool(useData),
        jetSmear = cms.double(jetSmear),
        jecPayloads = cms.vstring( payloads )
        )
        )
process.pfShyftProducerMuLoose = cms.EDFilter('EDSHyFTSelector',
                                              shyftSelection = shyftSelectionInput.clone(
                                                jetSrc = cms.InputTag('goodPatJetsPFlow'),
                                                muonSrc = cms.InputTag('selectedPatMuonsLoosePFlow'),
                                                electronSrc = cms.InputTag('selectedPatElectronsLoosePFlow'),
                                                ePlusJets = cms.bool( False ),
                                                muPlusJets = cms.bool( True ),
                                                jetPtMin = cms.double(10.0),##
                                                minJets = cms.int32(1),
                                                metMin = cms.double(0.0),
                                                muPtMin = cms.double(35.0),
                                                identifier = cms.string('PFMuLoose'),
                                                cutsToIgnore=cms.vstring( ['Trigger','== 1 Tight Lepton','== 1 Tight Lepton, Mu Veto','== 1 Lepton'] ),
                                                useData = cms.bool(useData),
                                                jetSmear = cms.double(jetSmear),
                                                jecPayloads = cms.vstring( payloads ),
                                                removeLooseLep = cms.bool(True)
                                                )
                                            )
process.pfShyftProducerMuLoose.shyftSelection.muonIdTight.cutsToIgnore.append('PFIso')

process.pfShyftProducerEle = cms.EDFilter('EDSHyFTSelector',
                                    shyftSelection = shyftSelectionInput.clone(
        muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
        electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
        metSrc = cms.InputTag('patMETsPFlow'),
        jetSrc = cms.InputTag('goodPatJetsPFlow'),
        pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
        ePlusJets = cms.bool( True ),
        muPlusJets = cms.bool( False ),
        jetPtMin = cms.double(10.0),##
        eEtCut = cms.double(35.0),
        usePFIso = cms.bool(True),
        useVBTFDetIso  = cms.bool(False),
        useWP95Selection = cms.bool(False),
        useWP70Selection = cms.bool(True),
        minJets = cms.int32(1),
        metMin = cms.double(0.0),
	muPtMin = cms.double(35.0),
        identifier = cms.string('PFEle'),
        cutsToIgnore=cms.vstring( ['Trigger'] ),
        useData = cms.bool(useData),
        jetSmear = cms.double(jetSmear),
        jecPayloads = cms.vstring( payloads )
        )
        )

process.pfShyftProducerEleLoose = process.pfShyftProducerEle.clone(
    shyftSelection = process.pfShyftProducerEle.shyftSelection.clone(
    useWP95Selection = cms.bool(True),# if CiC ID loose, then pf reliso<0.2 is applied
    useWP70Selection = cms.bool(False),
    )
    )

process.pfShyftTupleJetsMu = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducerMu", "jets"),
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
    process.pfShyftTupleJetsMu.variables.append(
        cms.PSet(
            tag = cms.untracked.string("flavor"),
            quantity = cms.untracked.string("partonFlavour()")
            )
        )
    process.pfShyftTupleJetsMu.variables.append(
        cms.PSet(
            tag = cms.untracked.string("genJetPt"),
            quantity = cms.untracked.string("? userInt('matched') ? genJet().pt : -10")
            )
    )

process.pfShyftTupleJetsMuLoose = process.pfShyftTupleJetsMu.clone(
    src = cms.InputTag("pfShyftProducerMuLoose", "jets"),
    )

process.pfShyftTupleJetsEle = process.pfShyftTupleJetsMu.clone(
    src = cms.InputTag("pfShyftProducerEle", "jets"),
    )

process.pfShyftTupleJetsEleLoose = process.pfShyftTupleJetsMu.clone(
    src = cms.InputTag("pfShyftProducerEleLoose", "jets"),
    )

process.pfShyftTupleMuons = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducerMu", "muons"),
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

process.pfShyftTupleMuonsLoose = process.pfShyftTupleMuons.clone(
    src = cms.InputTag("pfShyftProducerMuLoose", "muons")
    )


process.pfShyftTupleMETMu = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducerMu", "MET"),
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

process.pfShyftTupleMETMuLoose = process.pfShyftTupleMETMu.clone(
    src = cms.InputTag("pfShyftProducerMuLoose", "MET")
    )

process.pfShyftTupleMETEle = process.pfShyftTupleMETMu.clone(
    src = cms.InputTag("pfShyftProducerEle", "MET"),
    )

process.pfShyftTupleMETEleLoose = process.pfShyftTupleMETEle.clone(
    src = cms.InputTag("pfShyftProducerEleLoose", "MET"),
    )

process.pfShyftTupleElectrons = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducerEle", "electrons"),
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

process.pfShyftTupleElectronsLoose = process.pfShyftTupleElectrons.clone(
    src = cms.InputTag("pfShyftProducerEleLoose", "electrons"),
    )


process.PUNtupleDumper = cms.EDProducer(
    "PUNtupleDumper",
    PUscenario = cms.string("42X")
    )

## if not options.useData:
##     process.p0 = cms.Path(
##         process.PUNtupleDumper
##         )

process.p1 = cms.Path(
    process.hltSelection*
    process.pfShyftProducerMu*
    process.pfShyftTupleJetsMu*
    process.pfShyftTupleMuons*
    process.pfShyftTupleMETMu
    )

process.p2 = cms.Path(
    process.hltSelection*
    process.pfShyftProducerEle*
    process.pfShyftTupleJetsEle*
    process.pfShyftTupleElectrons*
    process.pfShyftTupleMETEle
    )

if not options.useData:
    process.p0 = cms.Path( process.PUNtupleDumper )


if options.usePDFs :
    process.p1 += process.pdfWeightProducer
    process.p2 += process.pdfWeightProducer

process.p3 = cms.Path()
process.p4 = cms.Path() 
if options.useLooseElectrons:
    process.p3 = cms.Path(
        process.hltSelection*
        process.pfShyftProducerEleLoose*
        process.pfShyftTupleJetsEleLoose*
        process.pfShyftTupleElectronsLoose*
        process.pfShyftTupleMETEleLoose
        )
if options.useLooseMuons :
    process.p4 = cms.Path(
        process.hltSelection*
        process.pfShyftProducerMuLoose*
        process.pfShyftTupleJetsMuLoose*
        process.pfShyftTupleMuonsLoose*
        process.pfShyftTupleMETMuLoose
        )
        


process.MessageLogger.cerr.FwkReport.reportEvery = 1000


process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string("shyftDump.root"),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p1','p2','p3','p4') ),
                               outputCommands = cms.untracked.vstring('drop *',
                                                                      #'keep *_pfShyftProducer_*_*',
                                                                      'keep *_PUNtupleDumper_*_*',
                                                                      'keep *_pfShyftTuple*_*_*',
                                                                      'keep *_pdfWeightProducer_*_*'
                                                                      #'keep *_kinFitTtSemiLepEvent_*_*'
                                                                      ) 
                               )
process.outpath = cms.EndPath(process.out)

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.out.dropMetaData = cms.untracked.string("DROPPED")
