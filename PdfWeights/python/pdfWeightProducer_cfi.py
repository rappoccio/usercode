import FWCore.ParameterSet.Config as cms


pdfWeightProducer = cms.EDProducer('PdfWeightProducer',
                                   pdfSet = cms.vstring("cteq66.LHgrid"), 
                                   pdfName = cms.vstring("cteq66"), 
                                   nMembers = cms.vint32(44)
                                   )
