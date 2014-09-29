# Import configurations
import FWCore.ParameterSet.Config as cms

output = True
flavor = 'ttjets'
outfile = './' + flavor + '_patuple.root'
histfile = 'test_histogram.root'

process = cms.Process("ANA")
print 'Flavor = ' + flavor

if output == True :
    print 'Output = True'
    print 'outfile = ' + outfile
else :
    print 'Output = False'

# this defines the input files

if flavor == 'wbb' :
    from Analysis.HFAna.PatInput_vqq_IDEAL_V9_PAT_v3_cfi import *
elif flavor == 'wcc' :
    from Analysis.HFAna.PatInput_vqq_IDEAL_V9_PAT_v3_cfi import *
elif flavor == 'wc' :
    from Analysis.HFAna.Pattuple_wc_cfi import *
elif flavor == 'wjets' :
    from Analysis.HFAna.Pattuple_wjets_cfi import *
elif flavor == 'ttjets' :
    from Analysis.HFAna.Pattuple_ttbar_cfi  import *

# set the number of events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(50)
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

# input pat sequences
process.load("PhysicsTools.PatAlgos.patLayer0_cff")
process.load("PhysicsTools.PatAlgos.patLayer1_cff")

# load the pat layer 1 event content
process.load("PhysicsTools.PatAlgos.patLayer1_EventContent_cff")

# talk to TFileService
process.TFileService = cms.Service("TFileService",
    fileName = cms.string(histfile)
)

# define the source, from reco input
process.source = RecoInput()
process.source.skipEvents = cms.untracked.uint32(0)

# define event selection to be that which satisfies 'p'
process.patEventSelection = cms.PSet(
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('p')
    )
)

process.printDecay = cms.EDAnalyzer("ParticleDecayDrawer",
					src = cms.InputTag("genParticles")
				)

process.printTree  = cms.EDAnalyzer("ParticleListDrawer",
					maxEventsToPrint = cms.untracked.int32(2),
					src = cms.InputTag("genParticles")
				)

process.selectedMuonsGenParticlesMatch = cms.EDProducer( "MCTruthDeltaRMatcherNew",
                                              src = cms.InputTag("selectedLayer1Muons"),
                                              matched = cms.InputTag("genParticles"),
                                              distMin = cms.double(0.15),
                                              matchPDGId = cms.vint32(13)
                                              )

process.load("Analysis.SemiLepSel.semilepsel_cfi")
process.semilepSel.verbose = True

process.load("Analysis.EveCount.evecount_cfi")
#process.eventcount.verbose = True
# define path 'p'. This will produce all of the objects.
# This is the path that will be used to write the output to
# a data file.
process.p = cms.Path(
	process.selectedMuonsGenParticlesMatch
	*process.semilepSel*process.printDecay
	*process.eventcount#*process.printTree

)

if output == True :
    print "Output file is " + outfile

    # extend event content to include pat analyzer kit objects
    process.patLayer1EventContent.outputCommands.extend(['keep *_selectedMuonsGenParticlesMatch_*_*'])
    process.patLayer1EventContent.outputCommands.extend(['keep *_eventcount_*_*'])

    # extend event content to include pat analyzer kit objects
    process.out = cms.OutputModule("PoolOutputModule",
                                   process.patEventSelection,
                                   process.patLayer1EventContent,
                                   verbose = cms.untracked.bool(True),
                                   fileName = cms.untracked.string(outfile)
                                   )


    # define output path
    process.outpath = cms.EndPath(process.out)

