import FWCore.ParameterSet.Config as cms


pdfWeightProducer = cms.EDProducer('PdfWeightProducer',
                                   pdfSet = cms.string("cteq66.LHgrid"),
                                   nMembers = cms.int32(44)
                                   )
