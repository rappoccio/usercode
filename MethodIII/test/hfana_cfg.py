# Import configurations
import FWCore.ParameterSet.Config as cms


patInput = True
output = False

flavor = 'wbb'
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
    from Analysis.MethodIII.PatInput_vqq_cfi import *
elif flavor == 'wcc' :
    from Analysis.MethodIII.PatInput_vqq_cfi import *
elif flavor == 'wc' :
    from Analysis.MethodIII.Pattuple_wc_cfi import *
elif flavor == 'wjets' :
    from Analysis.MethodIII.Pattuple_wjets_cfi import *
elif flavor == 'ttjets' :
    from Analysis.MethodIII.Pattuple_ttbar_cfi  import *
#else :
#    from Analysis.MethodIII.PatInput_vqq_cfi import *
        

        
# set the number of events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
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


process.load("Analysis.VPlusJets.goodLeptons_cfi")

process.goodLeptons.minMuons = cms.uint32(1)
process.goodLeptons.maxMuons = cms.uint32(1)
process.goodLeptons.maxElectrons = cms.uint32(0)

#process.countLayer1Jets.minNumber = cms.uint32(1)
#process.countLayer1Leptons.maxNumber = cms.uint32(1)



# input pat analyzer sequence
process.load("Analysis.MethodIII.hfana_cfi")
if flavor == 'ttjets' :
   process.hfAna.FlavorHistory = False
#process.hfAna.verbose = True

process.hfAna_wbb         = process.hfAna.clone()
process.hfAna_wb          = process.hfAna.clone()
process.hfAna_wcc         = process.hfAna.clone()
process.hfAna_wc          = process.hfAna.clone()
process.hfAna_wbb_gs      = process.hfAna.clone()
process.hfAna_wcc_gs      = process.hfAna.clone()
process.hfAna_wbb_comp    = process.hfAna.clone()
process.hfAna_wcc_comp    = process.hfAna.clone()
process.hfAna_wbb_gs_comp = process.hfAna.clone()
process.hfAna_wcc_gs_comp = process.hfAna.clone()
process.hfAna_wjets       = process.hfAna.clone()


# load the pat layer 1 event content
process.load("PhysicsTools.PatAlgos.patLayer1_EventContent_cff")

# request a summary at the end of the file
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

# define the source, from reco input
process.source = RecoInput()
process.source.skipEvents = cms.untracked.uint32(0)


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
    process.cFlavorHistoryProducer*
    process.goodLeptons
)



# load the different paths to make the different HF selections


import PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi as flavortools


process.wbb         = flavortools.wbb
process.wbb         *= process.goodLeptons * process.hfAna_wbb

process.wb          = flavortools.wb
process.wb          *= process.goodLeptons * process.hfAna_wb

process.wbb_gs      = flavortools.wbb_gs
process.wbb_gs      *= process.goodLeptons * process.hfAna_wbb_gs

process.wbb_comp    = flavortools.wbb_comp
process.wbb_comp    *= process.goodLeptons * process.hfAna_wbb_comp

process.wbb_gs_comp = flavortools.wbb_gs_comp
process.wbb_gs_comp *= process.goodLeptons * process.hfAna_wbb_gs_comp

process.wcc         = flavortools.wcc
process.wcc         *= process.goodLeptons * process.hfAna_wcc

process.wc          = flavortools.wc
process.wc          *= process.goodLeptons * process.hfAna_wc

process.wcc_gs      = flavortools.wcc_gs
process.wcc_gs      *= process.goodLeptons * process.hfAna_wcc_gs

process.wcc_comp    = flavortools.wcc_comp
process.wcc_comp    *= process.goodLeptons * process.hfAna_wcc_comp

process.wcc_gs_comp = flavortools.wcc_gs_comp
process.wcc_gs_comp *= process.goodLeptons * process.hfAna_wcc_gs_comp

process.wjets       = flavortools.wjets
process.wjets       *= process.goodLeptons * process.hfAna_wjets

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
                                   verbose = cms.untracked.bool(True),
                                   fileName = cms.untracked.string(outfile)
                                   )


    # define output path
    process.outpath = cms.EndPath(process.out)

