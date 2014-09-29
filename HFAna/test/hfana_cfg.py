# Import configurations
import FWCore.ParameterSet.Config as cms


patInput = True
output = False

flavor = 'wjets'
histfile = flavor + 'Ana.root'
outfile = './' + flavor + '_patLayer1.root'


# set up process
if patInput == False :
    process = cms.Process("HFANA")
else :
    process = cms.Process("HFPAT")

print 'Flavor = ' + flavor
if patInput == True : 
    print 'PatInput = True'
else :
    print 'PatInput = False'
if output == True :    
    print 'Output = True'
else :
    print 'Output = False'
    
print 'Histfile = ' + histfile

print 'outfile = ' + outfile

# this defines the input files

if flavor == 'wbb' :
    from Analysis.HFAna.PatInput_wbb_cfi import *
elif flavor == 'wcc' :
    from Analysis.HFAna.PatInput_wcc_cfi import *
elif flavor == 'wc' :
    from Analysis.HFAna.PatInput_wc_cfi import *
elif flavor == 'vqq' :
    from Analysis.HFAna.PatInput_vqq_cfi import *
elif flavor == 'wjets' :
    from Analysis.HFAna.PatInput_wjets_cfi import *
else :
    from Analysis.HFAna.PatInput_vqq_cfi import *
        
        
# set the number of events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)




# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.categories.append('PATLayer0Summary')
process.MessageLogger.cerr.INFO = cms.untracked.PSet(
    default          = cms.untracked.PSet( limit = cms.untracked.int32(0)  ),
    PATLayer0Summary = cms.untracked.PSet( limit = cms.untracked.int32(-1) )
)
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

# Load geometry
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string('IDEAL_V9::All')
process.load("Configuration.StandardSequences.MagneticField_cff")

# input MC stuff
process.load( "SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load( "PhysicsTools.HepMCCandAlgos.genParticles_cfi")
process.load( "PhysicsTools.HepMCCandAlgos.genEventWeight_cfi")
process.load( "PhysicsTools.HepMCCandAlgos.genEventScale_cfi")

process.load( "RecoJets.Configuration.GenJetParticles_cff")
process.load( "RecoJets.JetProducers.SISConeJetParameters_cfi" )
process.load( "RecoJets.JetProducers.GenJetParameters_cfi" )
process.load( "RecoJets.JetProducers.FastjetParameters_cfi" )
process.load( "RecoJets.JetProducers.sisCone5GenJets_cff")


# input flavor history stuff
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryProducer_cfi")
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryFilter_cfi")

process.printList = cms.EDAnalyzer( "ParticleListDrawer",
                                    src =  cms.InputTag( "genParticles" ),
                                    maxEventsToPrint = cms.untracked.int32( 10 )
#                                    printOnlyHardInteraction = cms.untracked.bool( True )
)

# input pat sequences
process.load("PhysicsTools.PatAlgos.patLayer0_cff")
process.load("PhysicsTools.PatAlgos.patLayer1_cff")

process.selectedLayer1Jets.cut = cms.string('et > 20.0 & abs(eta) < 2.5 & nConstituents > 0')
process.selectedLayer1Muons.cut = cms.string('pt > 30.0 & abs(eta) < 5.0')
if flavor != 'qcd_50_80' :
    process.countLayer1Leptons.minNumber = cms.uint32(1)
    
process.countLayer1Jets.minNumber = cms.uint32(1)
#process.countLayer1Leptons.maxNumber = cms.uint32(1)



# input pat analyzer sequence
process.load("Analysis.HFAna.hfana_cfi")



# load the pat layer 1 event content
process.load("PhysicsTools.PatAlgos.patLayer1_EventContent_cff")

# request a summary at the end of the file
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

# define the source, from reco input
process.source = RecoInput()
#process.source.skipEvents = cms.untracked.uint32(0)


# talk to TFileService
process.TFileService = cms.Service("TFileService",
    fileName = cms.string(histfile)
)

# define event selection to be that which satisfies 'p'
process.patEventSelection = cms.PSet(
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('p')
    )
)


# define path 'p'. This will produce all of the objects.
# This is the path that will be used to write the output to
# a data file. 
process.p = cms.Path(
#    process.printList*
    process.genJetParticles*process.sisCone5GenJets*
    process.bFlavorHistoryProducer*
    process.cFlavorHistoryProducer)

# load the different paths to make the different HF selections
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi")

# Set the threshold for output logging to 'info'
process.MessageLogger.cerr.threshold = 'INFO'


# talk to output module

if output == True :

    print "Output file is " + outfile
    
    # extend event content to include pat analyzer kit objects
    process.patLayer1EventContent.outputCommands.extend(['keep *_bFlavorHistoryProducer_*_*'])
    process.patLayer1EventContent.outputCommands.extend(['keep *_cFlavorHistoryProducer_*_*'])
    process.patLayer1EventContent.outputCommands.extend(['keep *_sisCone5GenJets_*_*'])

    process.out = cms.OutputModule("PoolOutputModule",
                                   process.patEventSelection,
                                   process.patLayer1EventContent,
                                   verbose = cms.untracked.bool(False),
                                   fileName = cms.untracked.string(outfile)
                                   )


    # define output path
    process.outpath = cms.EndPath(process.out)

