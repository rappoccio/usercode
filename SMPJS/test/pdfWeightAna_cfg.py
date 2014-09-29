import FWCore.ParameterSet.Config as cms

process = cms.Process("PDFANA")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
                                # replace 'myfile.root' with the source file you want to use
       fileNames = cms.untracked.vstring(
'file:/eos/uscms/store/user/smpjs/srappocc/QCD_Flat15to3000_pythia6_z2_ttbsm_v10beta_tuples_withgen_withnpv/res/ttbsm_v10beta_tuple_42x_mc_5_1_43X.root'
                                    )
                                )


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("jetMassPdfAna.root")
                                   )

process.load('Analysis.PdfWeights.pdfWeightProducer_cfi')

process.jetMassPdfUncertainty = cms.EDAnalyzer('EDJetMassPDFUncertainty',
                                       jetTag = cms.string("ak7Lite"),
                                       pdfTag = cms.InputTag("pdfWeightProducer", "pdfWeights"),
                                       generatorTag = cms.InputTag("generator"),
                                       )


process.MessageLogger.cerr.FwkReport.reportEvery = 10000


process.p = cms.Path(
    process.pdfWeightProducer * process.jetMassPdfUncertainty
    )


process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
