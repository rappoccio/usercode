import FWCore.ParameterSet.Config as cms

process = cms.Process("OWNPARTICLES")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration/StandardSequences/Services_cff')
process.load('Configuration/StandardSequences/Generator_cff')

from Configuration.GenProduction.PythiaUESettings_cfi import *
process.source = cms.Source("PythiaSource",
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    comEnergy = cms.untracked.double(10000.0),
    crossSection = cms.untracked.double(1.151),
    PythiaParameters = cms.PSet(
        pythiaUESettingsBlock,
        processParameters = cms.vstring('PMAS(6,1)=172.3 ! t quark mass', 
            'PMAS(347,1)= 3000.0 ! graviton mass', 
            'PARP(50)=0.54  ! c(k/Mpl) * 5.4', 
            'MSEL=0         ! User defined processes', 
            'MSUB(391)=1    ! ffbar->G*', 
            'MSUB(392)=1    ! gg->G*', 
            '5000039:ALLOFF ! Turn off graviton decays', 
            '5000039:ONIFANY 6 ! graviton decays into top', 
            '24:ALLOFF ! Turn off W decays', 
            '24:ONIFANY 1 2 3 4 5 6 ! W decays to quarks', 
            'CKIN(3)=25.    ! Pt hat lower cut', 
            'CKIN(4)=-1.    ! Pt hat upper cut', 
            'CKIN(13)=-10.  ! etamin', 
            'CKIN(14)=10.   ! etamax', 
            'CKIN(15)=-10.  ! -etamax', 
            'CKIN(16)=10.   ! -etamin'),
        parameterSets = cms.vstring('pythiaUESettings', 
            'processParameters')
    )
)


process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.myProducerLabel = cms.EDProducer('FastJetTests',
                      seedThreshold = cms.double( 1.0 ),
                      coneRadius = cms.double( 0.5 )
)

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('myOutputFile.root'),
                               dropMetaDataForDroppedData = cms.untracked.bool(True),
                               outputCommands = cms.untracked.vstring(['drop *',
                                                                       'keep *_myProducerLabel_*_*' ])
)

  
process.p = cms.Path(process.myProducerLabel)

process.e = cms.EndPath(process.out)
