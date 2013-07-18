import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")


## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )


###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')


options.register('ignoreTrigger',
                 0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Ignore trigger in selection")

options.register('muOrEle',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Use muons (0) or electrons (1)")


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
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/jdolen/TTJets_SemiLeptMGDecays_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A_ext-v1_TLBSM_53x_v3/99bd99199697666ff01397dad5652e9e/tlbsm_53x_v3_mc_1_2_Byw.root'
#'/store/results/B2G/SingleMu/StoreResults-V2-Run2012B-22Jan2013-v1_TLBSM_53x_v3-db7dd8e58134469d4e102fe8d5e205b6/SingleMu/USER/StoreResults-V2-Run2012B-22Jan2013-v1_TLBSM_53x_v3-db7dd8e58134469d4e102fe8d5e205b6/0000/A28480F8-1ED0-E211-828A-0026189438C2.root'
#'/store/results/B2G/SingleMu/StoreResults-Run2012D-22Jan2013-v1_TLBSM_53x_v3-db7dd8e58134469d4e102fe8d5e205b6/SingleMu/USER/StoreResults-Run2012D-22Jan2013-v1_TLBSM_53x_v3-db7dd8e58134469d4e102fe8d5e205b6/0000/0007D560-B5E2-E211-93AB-003048D15DB6.root'
#'/store/results/B2G/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v2_TLBSM_53x_v3-99bd99199697666ff01397dad5652e9e/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/USER/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v2_TLBSM_53x_v3-99bd99199697666ff01397dad5652e9e/0001/FECD539B-6DAC-E211-A40C-0025905938D4.root'
#'/store/results/B2G/TTJets_FullLeptMGDecays_8TeV-madgraph/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v2_TLBSM_53x_v3-99bd99199697666ff01397dad5652e9e/TTJets_FullLeptMGDecays_8TeV-madgraph/USER/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v2_TLBSM_53x_v3-99bd99199697666ff01397dad5652e9e/0000/000F0691-CFD2-E211-91F5-0026189438AD.root'
#'/store/user/lpctlbsm/mosherso/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/99bd99199697666ff01397dad5652e9e/tlbsm_53x_v3_mc_100_1_z0J.root'
#'/store/results/B2G/SingleMu/StoreResults-Run2012A-22Jan2013-v1_TLBSM_53x_v3-db7dd8e58134469d4e102fe8d5e205b6/SingleMu/USER/StoreResults-Run2012A-22Jan2013-v1_TLBSM_53x_v3-db7dd8e58134469d4e102fe8d5e205b6/0000/00752EA1-DEBB-E211-8988-002590593878.root'
#'/store/user/lpctlbsm/knash/SingleMu/SingleMu_Run2012C-PromptReco-v1_TLBSM_53x_v2/e3fb55b810dc7a0811f4c66dfa2267c9/tlbsm_53x_v2_data_36_1_6Os.root'
#'file:///uscms/home/osherson/Wtagging/SemiLep/CMSSW_5_3_2/src/Analysis/EDSHyFT/test/MARC/TRUTH/crab_0_130507_135257/res/skim_marc1_1_1_qrR.root'
#'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/knash/SingleMu/SingleMu_Run2012C-PromptReco-v1_TLBSM_53x_v2/e3fb55b810dc7a0811f4c66dfa2267c9/tlbsm_53x_v2_data_57_1_58Z.root'
#'dcap:///pnfs/cms/WAX/11/store/user/pilot/SingleMu/SingleMu_Run2012A/82fd51e0af07726fb8b1875f5746f193/ttbsm_52x_data_1_1_7O8.root'
#'dcap:///pnfs/cms/WAX/11/store/user/pilot/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/WJetsToLNu_8TeV/8f2c5ea1c4172ee3e54a11c7e5d6a05d/ttbsm_52x_mc_1_1_JUZ.root'
)
)


payloadsData = [
    'GR_P_V40_AN3_L1FastJet_AK7PFchs.txt',
    'GR_P_V40_AN3_L2Relative_AK7PFchs.txt',
    'GR_P_V40_AN3_L3Absolute_AK7PFchs.txt',
    'GR_P_V40_AN3_L2L3Residual_AK7PFchs.txt',
    'GR_P_V40_AN3_Uncertainty_AK7PFchs.txt'
                ]

payloadsMC = [
    'START53_V15_L1FastJet_AK7PFchs.txt',
    'START53_V15_L2Relative_AK7PFchs.txt',
    'START53_V15_L3Absolute_AK7PFchs.txt',
    'START53_V15_Uncertainty_AK7PFchs.txt'
]

if options.useData :
    payloads = payloadsData
else :
    payloads = payloadsMC


## process.source = cms.Source("PoolSource",
##                             fileNames = cms.untracked.vstring(
## 'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/vasquez/TTJets_TuneD6T_7TeV-madgraph-tauola/ttbsm_v7_Spring11-PU_S1_-START311_V1G1-v1/6a29f0fac22a95bcd534f59b8047bd70/ttbsm_41x_mc_10_1_5eL.root',
## 'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/vasquez/TTJets_TuneD6T_7TeV-madgraph-tauola/ttbsm_v7_Spring11-PU_S1_-START311_V1G1-v1/6a29f0fac22a95bcd534f59b8047bd70/ttbsm_41x_mc_11_1_y36.root',
## 'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/vasquez/TTJets_TuneD6T_7TeV-madgraph-tauola/ttbsm_v7_Spring11-PU_S1_-START311_V1G1-v1/6a29f0fac22a95bcd534f59b8047bd70/ttbsm_41x_mc_12_1_RFD.root'

## )
## )



from HLTrigger.HLTfilters.hltHighLevel_cfi import *
if options.ignoreTrigger :
    process.hltSelection = cms.Sequence()
else :
    process.hltSelectionMu = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths = ['HLT_Mu40_eta2p1_v*'
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

    if options.muOrEle :
        process.hltSelection = cms.Sequence( ~process.hltSelectionMu * process.hltSelectionEle )
    else :
        process.hltSelection = cms.Sequence( process.hltSelectionMu )


## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(7000) )

from Analysis.SHyFT.shyftPFSelection_cfi import shyftPFSelection as shyftPFSelectionInput

process.pileup = cms.EDFilter('PileUpProducer',
                                pvSrc = cms.InputTag('goodOfflinePrimaryVertices')

)

process.pfShyftProducer = cms.EDFilter('EDSHyFTPFSelector',
                                    shyftPFSelection = shyftPFSelectionInput.clone(
                                           jetSrc = cms.InputTag('goodPatJetsCA8PrunedPFPacked'),
    					   rhoSrc = cms.InputTag('kt6PFJets', 'rho'),
					   doElectrons = cms.bool(False),
                                           jecPayloads = cms.vstring( payloads )
                                        )
                                    )

process.pfShyftProducerLoose = cms.EDFilter('EDSHyFTPFSelector',
                                            shyftPFSelection = shyftPFSelectionInput.clone(
                                                jetSrc = cms.InputTag('goodPatJetsCA8PrunedPFPacked'),
                                                muonSrc = cms.InputTag('selectedPatMuonsPFlowLoose'),
                                                electronSrc = cms.InputTag('selectedPatElectronsPFlowLoose'),
						doElectrons = cms.bool(False),
    					   	rhoSrc = cms.InputTag('kt6PFJets', 'rho'),
                                                jecPayloads = cms.vstring( payloads ),
                                                removeLooseLep = cms.bool(True)
                                                )
                                            )

process.pfShyftProducerLoose.shyftPFSelection.cutsToIgnore.append('== 1 Tight Lepton')
process.pfShyftProducerLoose.shyftPFSelection.cutsToIgnore.append('0 other lepton')
process.pfShyftProducerLoose.shyftPFSelection.cutsToIgnore.append('>=1 Jets')
process.pfShyftProducerLoose.shyftPFSelection.muonIdPFTight.cutsToIgnore.append('PFIso')
process.pfShyftProducerLoose.shyftPFSelection.electronIdPFTight.cutsToIgnore.append('PFIso')


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
            tag = cms.untracked.string("csv"),
            quantity = cms.untracked.string("bDiscriminator('combinedSecondaryVertexBJetTags')")
            ),
        cms.PSet(
            tag = cms.untracked.string("jetArea"),
            quantity = cms.untracked.string("jetArea")
            ),
        cms.PSet(
            tag = cms.untracked.string("da0Pt"),
            quantity = cms.untracked.string("daughter(0).pt()")
            ),
        cms.PSet(
            tag = cms.untracked.string("da0Eta"),
            quantity = cms.untracked.string("daughter(0).eta()")
            ),
        cms.PSet(
            tag = cms.untracked.string("da0Phi"),
            quantity = cms.untracked.string("daughter(0).phi()")
            ),
        cms.PSet(
            tag = cms.untracked.string("da0Mass"),
            quantity = cms.untracked.string("daughter(0).mass()")
            ),
        cms.PSet(
            tag = cms.untracked.string("da1Pt"),
            quantity = cms.untracked.string("daughter(1).pt()")
            ),
        cms.PSet(
            tag = cms.untracked.string("da1Eta"),
            quantity = cms.untracked.string("daughter(1).eta()")
            ),
        cms.PSet(
            tag = cms.untracked.string("da1Phi"),
            quantity = cms.untracked.string("daughter(1).phi()")
            ),
        cms.PSet(
            tag = cms.untracked.string("da1Mass"),
            quantity = cms.untracked.string("daughter(1).mass()")
            ),
        )  
    )

process.pfShyftTupleJetsLoose = process.pfShyftTupleJets.clone(
    src = cms.InputTag("pfShyftProducerLoose", "jets"),
    )



process.pfShyftTupleJetsLooseTopTag = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("goodPatJetsCATopTagPFPacked"),
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
            tag = cms.untracked.string("jetArea"),
            quantity = cms.untracked.string("jetArea")
            ),
        cms.PSet(
            tag = cms.untracked.string("nSubjets"),
            quantity = cms.untracked.string("numberOfDaughters()")
            ),
        cms.PSet(
            tag = cms.untracked.string("minMass"),
            quantity = cms.untracked.string("? hasTagInfo('CATop') ? tagInfo('CATop').properties().minMass : 0.0")
            ),
        cms.PSet(
            tag = cms.untracked.string("topMass"),
            quantity = cms.untracked.string("? hasTagInfo('CATop') ? tagInfo('CATop').properties().topMass : 0.0")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj0csv"),
	    quantity = cms.untracked.string("daughter(0).bDiscriminator('combinedSecondaryVertexBJetTags')")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj1csv"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 1 ? daughter(1).bDiscriminator('combinedSecondaryVertexBJetTags') : -1")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj2csv"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 2 ? daughter(2).bDiscriminator('combinedSecondaryVertexBJetTags') : -1")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj3csv"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 3 ? daughter(3).bDiscriminator('combinedSecondaryVertexBJetTags') : -1")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj0pt"),
	    quantity = cms.untracked.string("daughter(0).pt()")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj1pt"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 1 ? daughter(1).pt() : -1000")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj2pt"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 2 ? daughter(2).pt() : -1000")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj3pt"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 3 ? daughter(3).pt()  : -1000")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj0eta"),
	    quantity = cms.untracked.string("daughter(0).eta()")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj1eta"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 1 ? daughter(1).eta() : -1000")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj2eta"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 2 ? daughter(2).eta() : -1000")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj3eta"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 3 ? daughter(3).eta()  : -1000")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj0phi"),
	    quantity = cms.untracked.string("daughter(0).phi()")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj1phi"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 1 ? daughter(1).phi() : -1000")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj2phi"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 2 ? daughter(2).phi() : -1000")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj3phi"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 3 ? daughter(3).phi()  : -1000")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj0mass"),
	    quantity = cms.untracked.string("daughter(0).mass()")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj1mass"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 1 ? daughter(1).mass() : -1000")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj2mass"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 2 ? daughter(2).mass() : -1000")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj3mass"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 3 ? daughter(3).mass()  : -1000")
            ),
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
        cms.PSet(
            tag = cms.untracked.string("pfisoCH"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoNH"),
            quantity = cms.untracked.string("userIsolation('pat::PfNeutralHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoPH"),
            quantity = cms.untracked.string("userIsolation('pat::PfGammaIso')"
                                            )
            ),
	cms.PSet(
            tag = cms.untracked.string("pfisoPU"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso') + " +
                                            "max(0.0,  userIsolation('pat::PfNeutralHadronIso') + userIsolation('pat::PfGammaIso') - 0.5 * userIsolation('pat::TrackIso') )"
                                            )
            ),
        )  
    )

process.pfShyftTupleMuonsLoose = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducerLoose", "muons"),
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
        cms.PSet(
            tag = cms.untracked.string("pfisoCH"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoNH"),
            quantity = cms.untracked.string("userIsolation('pat::PfNeutralHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoPH"),
            quantity = cms.untracked.string("userIsolation('pat::PfGammaIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoPU"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso') + " +
                                            "max(0.0,  userIsolation('pat::PfNeutralHadronIso') + userIsolation('pat::PfGammaIso') - 0.5 * userIsolation('pat::TrackIso') )"
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

process.pfShyftTupleMETLoose = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducerLoose", "MET"),
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
        cms.PSet(
            tag = cms.untracked.string("pfisoCH"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoNH"),
            quantity = cms.untracked.string("userIsolation('pat::PfNeutralHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoPH"),
            quantity = cms.untracked.string("userIsolation('pat::PfGammaIso')"
                                            )
            ),
        )  
    )

process.pfShyftTupleElectronsLoose = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducerLoose", "electrons"),
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
        cms.PSet(
            tag = cms.untracked.string("pfisoCH"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoNH"),
            quantity = cms.untracked.string("userIsolation('pat::PfNeutralHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoPH"),
            quantity = cms.untracked.string("userIsolation('pat::PfGammaIso')"
                                            )
            ),
        )  
    )

process.nsub = cms.EDProducer("NjettinessAdder",
                              #src=cms.InputTag("goodPatJetsCA8PrunedPFPacked"),
                              src=cms.InputTag("goodPatJetsCA8PF"),
                              cone=cms.double(0.8)
                              )

 #################### keep generator-level products #####################
 
 
process.topQuarks = cms.EDFilter("CandViewSelector",
    src = cms.InputTag("prunedGenParticles"),
    cut = cms.string("status == 3 && abs(pdgId) == 6")
)

process.pfShyftTupleTopQuarks = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("topQuarks"),
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
            tag = cms.untracked.string("mass"),
            quantity = cms.untracked.string("mass")
            )
        )
    )
 
process.pfShyftTupleCA8GenJets = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("ca8GenJetsNoNu"),
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
            tag = cms.untracked.string("mass"),
            quantity = cms.untracked.string("mass")
            )
        )
    )


process.p1 = cms.Path(
    process.hltSelection*
    process.pileup*
    process.pfShyftProducerLoose *
    process.pfShyftTupleJetsLoose*
    process.pfShyftTupleJetsLooseTopTag*
    process.nsub*
    process.pfShyftTupleMuonsLoose*
    process.pfShyftTupleElectronsLoose*
    process.pfShyftTupleMETLoose*
    process.pfShyftTupleMETLoose*
    process.topQuarks*
    process.pfShyftTupleTopQuarks*
    process.pfShyftTupleCA8GenJets    
    )

process.p2 = cms.Path(
    process.hltSelection*
    process.pfShyftProducer*
    process.pfShyftTupleJets*
    process.pfShyftTupleMuons*
    process.pfShyftTupleElectrons*
    process.pfShyftTupleMET*
    process.topQuarks*
    process.pfShyftTupleTopQuarks*
    process.pfShyftTupleCA8GenJets
    )


process.MessageLogger.cerr.FwkReport.reportEvery = 1000




process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string("shyft_ultraslim.root"),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p1', 'p2') ),
                               outputCommands = cms.untracked.vstring('drop *',
                                                                      #'keep *_pfShyftProducer_*_*',
                                                                      'keep double_*_rho_*',
                                                                      'keep *_pfShyftTuple*_*_*',
                                                                      'keep *_nsub*_*_*',
                                                                      'keep *_generator_*_*',
                                                                      'keep *_pileup*_*_*'
                                                                      #'keep *_kinFitTtSemiLepEvent_*_*'
                                                                      ) 
                               )
process.outpath = cms.EndPath(process.out)

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.out.dropMetaData = cms.untracked.string("DROPPED")
