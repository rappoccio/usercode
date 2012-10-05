###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing('python')

options.register('outFilename',
    'bTaggingEfficiency.root',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    'output file name'
)
options.register('reportEvery',
    1000,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.int,
    'Report every N events (default is N=1000)'
)
## 'maxEvents' is already registered by the Framework, changing default value
options.setDefault('maxEvents', -1)

options.parseArguments()

import FWCore.ParameterSet.Config as cms

process = cms.Process('USER')

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
	'/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_10_3_lNR.root',
	'/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_11_4_iPL.root',
	'/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_12_3_kmL.root',
	'/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_13_3_Etl.root',
	'/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_14_4_VWT.root',
	'/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_15_3_Vg0.root',
	'/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_16_1_hvB.root',
	'/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_1_4_qzI.root',
	'/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_2_4_SXV.root',
	'/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_3_3_pY5.root',
	'/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_4_4_Zkt.root',
	'/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_5_4_oTh.root',
	'/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_6_5_p9W.root',
	'/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_7_7_TjL.root',
	'/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_8_4_Lxp.root',
	'/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_9_3_c4F.root'
    )
)

process.TFileService = cms.Service('TFileService',
   fileName = cms.string(options.outFilename)
)

process.bTaggingEffAnalyzer = cms.EDAnalyzer('BTaggingEffAnalyzer',
    JetsTag            = cms.InputTag('goodPatJetsPFlow'),
    DiscriminatorTag   = cms.string('combinedSecondaryVertexBJetTags'),
    DiscriminatorValue = cms.double(0.679),
    PtNBins            = cms.int32(100),
    PtMin              = cms.double(0.),
    PtMax              = cms.double(1000.),
    EtaNBins           = cms.int32(60),
    EtaMin             = cms.double(-3.),
    EtaMax             = cms.double(3.)
)

process.p = cms.Path(process.bTaggingEffAnalyzer)
