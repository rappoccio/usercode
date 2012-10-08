import FWCore.ParameterSet.Config as cms

process = cms.Process("GenInfo")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.MessageLogger.cerr.FwkJob.limit=1
process.MessageLogger.cerr.ERROR = cms.untracked.PSet( limit = cms.untracked.int32(0) )

###############################
####### Parameters ############
############################### 
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('runOntWtW',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run on BB->tWtW sample"),

options.register ('runOnbZtW',
                  1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run on BB->bZtW sample")

options.parseArguments()            
                                    
print options

readFiles = cms.untracked.vstring()

if options.runOnbZtW:
    readFiles.extend( [
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/BprimeBprimeToBZTWinc_M750_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_101_3_UGF.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/BprimeBprimeToBZTWinc_M750_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_100_3_Btf.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/BprimeBprimeToBZTWinc_M750_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_103_3_f7U.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/BprimeBprimeToBZTWinc_M750_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_102_5_MbH.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/BprimeBprimeToBZTWinc_M750_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_105_3_A9h.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/BprimeBprimeToBZTWinc_M750_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_104_4_fgM.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/BprimeBprimeToBZTWinc_M750_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_107_3_O82.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/BprimeBprimeToBZTWinc_M750_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_106_4_aBY.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/BprimeBprimeToBZTWinc_M750_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_109_3_Orl.root',
    '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/BprimeBprimeToBZTWinc_M750_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_108_3_Y2C.root',
        ]);

elif options.runOntWtW:
    readFiles.extend( [
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_10_3_lNR.root',
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_11_4_iPL.root',
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_12_3_kmL.root',
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_13_3_Etl.root',
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_14_4_VWT.root',
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_1_4_qzI.root',
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_15_3_Vg0.root',
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_16_1_hvB.root',
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_2_4_SXV.root',
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_3_3_pY5.root',
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_4_4_Zkt.root',
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_5_4_oTh.root',
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_6_5_p9W.root',
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_7_7_TjL.root',
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_8_4_Lxp.root',
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_9_3_c4F.root'
        ]);

if len(options.inputFiles) == 0 :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(readFiles)
                                )
else:
    filelist = []
    with open( options.inputFiles[0], 'r' ) as input_:
        for line in input_:
            filelist.append(line.strip())
            
        print 'filelist', filelist
        process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(filelist)
                                    )
        
process.GenInfo = cms.EDProducer('BoostedParticles')
                                         
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.printTree = cms.EDAnalyzer("ParticleTreeDrawer",
                                   src = cms.InputTag("prunedGenParticles"),
                                   printP4 = cms.untracked.bool(False),
                                   printPtEtaPhi = cms.untracked.bool(False),
                                   printVertex = cms.untracked.bool(False),
                                   printStatus = cms.untracked.bool(False),
                                   printIndex = cms.untracked.bool(False),
                                   status = cms.untracked.vint32( 3 )
                                   )

process.printList = cms.EDAnalyzer("ParticleListDrawer",
  maxEventsToPrint = cms.untracked.int32(20),
  printVertex = cms.untracked.bool(False),
  src = cms.InputTag("prunedGenParticles")
)

process.p = cms.Path(process.GenInfo * process.printTree * process.printList)

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('genOutputFileTest.root'),
                               outputCommands = cms.untracked.vstring('drop *',
                                                                      'keep *_GenInfo*_*_*',)
                               )

process.e = cms.EndPath(process.out)
