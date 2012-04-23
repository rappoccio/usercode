## import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *

# Be sure to use the right global tag containing the JEC's
process.GlobalTag.globaltag = cms.string( 'START42_V13::All' )


# Get a list of good primary vertices, in 42x, these are DAF vertices
from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
process.goodOfflinePrimaryVertices = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams = pvSelector.clone( minNdof = cms.double(4.0), maxZ = cms.double(24.0), maxRho = cms.double(2.0) ),
    src=cms.InputTag('offlinePrimaryVertices'),
    filter=cms.bool(True)
    )

# First configure the default jets without CHS
process.load('RecoJets.Configuration.RecoPFJets_cff')
##-------------------- Turn-on the FastJet density calculation -----------------------
process.kt6PFJets.doRhoFastjet = True
##-------------------- Turn-on the FastJet jet area calculation for your favorite algorithm -----------------------
process.ak5PFJets.doAreaFastjet = True

# Next Configure PAT to use PF2PAT WITH CHS
from PhysicsTools.PatAlgos.tools.pfTools import *
postfix = "PFlow"
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC=True, postfix=postfix)
process.pfPileUpPFlow.Enable = True
process.pfPileUpPFlow.checkClosestZVertex = cms.bool(False)
process.pfPileUpPFlow.Vertices = cms.InputTag('goodOfflinePrimaryVertices')
process.pfJetsPFlow.doAreaFastjet = True
process.pfJetsPFlow.doRhoFastjet = False


# Compute the mean pt per unit area (rho) from the
# PFchs inputs
from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
process.kt6PFJetsPFlow = kt4PFJets.clone(
    rParam = cms.double(0.6),
    src = cms.InputTag('pfNoElectron'+postfix),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True)
    )
process.patJetCorrFactorsPFlow.rho = cms.InputTag("kt6PFJetsPFlow", "rho")


## uncomment the following lines to add ak5PFJets to your PAT output
switchJetCollection(process,cms.InputTag('ak5PFJets'),
                 doJTA        = True,
                 doBTagging   = True,
                 jetCorrLabel = ('AK5PF', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute'])),
                 doType1MET   = True,
                 genJetCollection=cms.InputTag("ak5GenJetsNoNu"),
                 doJetID      = True
                 )
process.patJetCorrFactors.rho = cms.InputTag("kt6PFJets", "rho")

# Add the PV selector and KT6 producer to the sequence
getattr(process,"patPF2PATSequence"+postfix).replace(
    getattr(process,"pfNoElectron"+postfix),
    getattr(process,"pfNoElectron"+postfix)*process.kt6PFJetsPFlow )



process.patDefaultSequence.remove( process.countPatPFParticlesPFlow )

process.selectedPatJetsPFlow.cut = cms.string("pt > 20")
process.selectedPatJets.cut = cms.string("pt > 20")

from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector
process.goodPatJetsPFlow = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                        filterParams = pfJetIDSelector.clone(),
                                        src = cms.InputTag("selectedPatJetsPFlow")
                                        )
process.goodPatJets = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                   filterParams = pfJetIDSelector.clone(),
                                   src = cms.InputTag("selectedPatJets")
                                   )




# Now add the alternative estimates of rho

process.load('RecoJets.JetProducers.fixedGridRhoProducer_cfi')
process.fixedGridRhoAllCHS = process.fixedGridRhoAll.clone(src = cms.InputTag('pfNoElectron' + postfix) )
process.fixedGridRhoCentralCHS = process.fixedGridRhoCentral.clone(src = cms.InputTag('pfNoElectron' + postfix) )
process.fixedGridRhoForwardCHS = process.fixedGridRhoForward.clone(src = cms.InputTag('pfNoElectron' + postfix) )


process.fixedGridSeq = cms.Sequence(
    process.fixedGridRhoAll*
    process.fixedGridRhoCentral*
    process.fixedGridRhoForward*
    process.fixedGridRhoAllCHS*
    process.fixedGridRhoCentralCHS*
    process.fixedGridRhoForwardCHS
    )

#from RecoJets.FFTJetProducers.fftjetpileupprocessor_pfprod_cfi import fftjet_pileup_processor_pf as fftjetPUInput
#process.fftjetPFPileup = fftjetPUInput.clone()
#process.fftjetPFCHSPileup = fftjetPUInput.clone(src = cms.InputTag('pfNoElectron' + postfix))

#process.fftjetSeq = cms.Sequence(
#    process.fftjetPFPileup*
#    process.fftjetPFCHSPileup
#    )

process.patseq = cms.Sequence(    
    process.goodOfflinePrimaryVertices*
    process.kt6PFJets*
    process.ak5PFJets*
    process.fixedGridSeq*
    #process.fftjetSeq*
    getattr(process,"patPF2PATSequence"+postfix)*
    process.patDefaultSequence*
    process.goodPatJetsPFlow*
    process.goodPatJets
    )

# Adjust the event content
process.out.outputCommands += [
    'keep *_selectedPat*_*_*',
    'keep *_goodOfflinePrimaryVertices*_*_*',
    'keep double_*_*_PAT',
    'keep *_addPileupInfo_*_*',
    'keep recoGenJets_ak5GenJetsNoNu_*_*',
    'keep *_goodPatJets*_*_*',
    'drop *_selectedPatJets*_*_*',
    'drop *_selectedPatPFParticlesPFlow_*_*',
    'drop *_selectedPatTaus*_*_*'
]



## let it run
process.p = cms.Path(
    process.patseq
    )

## ------------------------------------------------------
#  In addition you usually want to change the following
#  parameters:
## ------------------------------------------------------
#
#   process.GlobalTag.globaltag =  ...    ##  (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
#                                         ##
#   process.source.fileNames = [          ##
#    '/store/relval/CMSSW_3_8_6/RelValTTbar/GEN-SIM-RECO/START38_V13-v1/0065/F438C4C4-BCE7-DF11-BC6B-002618943885.root'
#   ]                                     ##  (e.g. 'file:AOD.root')
#                                         ##
process.maxEvents.input = 10000
#                                         ##
#   process.out.outputCommands = [ ... ]  ##  (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#                                         ##
#   process.out.fileName = ...            ##  (e.g. 'myTuple.root')
#                                         ##
process.options.wantSummary = True        ##  (to suppress the long output at the end of the job)
