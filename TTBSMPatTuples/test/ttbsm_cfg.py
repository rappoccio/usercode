# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *

###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('useData',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run this on real data")

options.register ('hltProcess',
                  'HLT',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "HLT process name to use.")

options.register ('writeFat',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Output tracks and PF candidates")


options.parseArguments()

if not options.useData :
    inputJetCorrLabel = ('AK5PF', ['L2Relative', 'L3Absolute'])
    process.source.fileNames = [
'/store/mc/Spring11/QCD_Pt_15to3000_Flat_7TeV/GEN-SIM-RECO/START311_V1A-v1/0000/FEB02EA6-0747-E011-AB86-00E081791847.root',
'/store/mc/Spring11/QCD_Pt_15to3000_Flat_7TeV/GEN-SIM-RECO/START311_V1A-v1/0000/FE628AA2-0747-E011-965E-00E081791891.root',
'/store/mc/Spring11/QCD_Pt_15to3000_Flat_7TeV/GEN-SIM-RECO/START311_V1A-v1/0000/FE5AF9C2-2047-E011-91ED-003048D46072.root'

        ]
else :
    inputJetCorrLabel = ('AK5PF', ['L2Relative', 'L3Absolute', 'L2L3Residual'])
    process.source.fileNames = [
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/547/DAFCA3B7-B850-E011-9ADF-0030487C778E.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/502/7297DBD1-6B50-E011-9FA5-0030487CD162.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/500/9E1BCB0E-6C50-E011-BC4D-0030487CD7EE.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/499/3850D990-9450-E011-BF72-0030487CD716.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/498/AC8FE79D-8450-E011-A58B-0030487CAEAC.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/495/88BEEA68-3850-E011-9F13-0030487CD17C.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/494/1C35E662-3350-E011-BAA0-003048F1183E.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/488/66D0A0F1-1850-E011-97C0-003048F1BF68.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/486/E2FB2282-1850-E011-BA61-001D09F2527B.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/484/6E1A5CBE-1650-E011-B823-003048D2C108.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/472/CA224AEB-1450-E011-84A1-001D09F2527B.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/471/5C765497-1450-E011-AD91-001D09F248F8.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/469/204A3C03-1A50-E011-B8D7-0030487C8CB6.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/467/6ABD98CE-1B50-E011-9D5F-003048F11114.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/466/F296557B-1E50-E011-8C7F-0030487CD6B4.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/463/72D3943E-2350-E011-B098-001617C3B654.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/462/E650148E-2650-E011-96BD-001617C3B654.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/456/863BF1F0-4C50-E011-9ABC-001617C3B5E4.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/455/46A4141B-4A50-E011-8ED4-001D09F24934.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/454/C2041925-DC50-E011-B0C2-0030487C7828.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/450/2EE61936-5050-E011-9731-0030487C7392.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/449/5C5D099B-4C50-E011-9779-000423D98B6C.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/447/B8CFC010-5650-E011-A6CA-0030487CD162.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/446/6810F3AF-5C50-E011-9EA3-003048F11114.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/445/5E83EDE8-5650-E011-B45D-001D09F23A3E.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/444/0E40C747-AC50-E011-8A91-0030487CD718.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/443/EAA93DE5-5750-E011-A127-001617C3B76E.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/442/70B27507-5B50-E011-99A9-0030487CD162.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/439/6658D888-B34F-E011-BE9D-001D09F24D67.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/433/12B7CF7F-B54F-E011-94B6-001D09F23C73.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/432/96E7E8AA-1150-E011-878B-001D09F28F1B.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/431/44A96589-2D50-E011-861C-003048F118D4.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/428/00E2E174-B34F-E011-9858-003048F110BE.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/427/52C35785-814F-E011-A17C-003048F117EC.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/425/F4681D39-844F-E011-B3E5-003048F024F6.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/423/2A0114B3-7C4F-E011-B719-001D09F24303.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/421/0A0F17E0-774F-E011-93C1-000423D94E70.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/413/28A09525-EB4F-E011-9AE5-003048F0258C.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/410/8094C4AE-5F4F-E011-B390-003048F118D2.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/406/4E1472A9-5F4F-E011-B062-0030487C7828.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/405/3AB185A4-D64F-E011-8394-0030487C2B86.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/404/38F2FFDA-374F-E011-AD2A-003048F024F6.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/403/64B3598B-364F-E011-8683-001D09F29849.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/386/5059F123-0B4F-E011-8DDB-0030487C2B86.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/384/463D8003-094F-E011-A4B1-0030487CD17C.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/383/7EDAB706-0D4F-E011-BBBF-0030487C6A66.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/379/14D52E14-0C4F-E011-B5AF-003048F11C58.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/377/5CBF6B69-0B4F-E011-855D-0030487CD906.root',
'/store/data/Run2011A/Jet/AOD/PromptReco-v1/000/160/329/6631A77A-2F4E-E011-AE5A-003048F118C2.root',

        ]


print options

import sys


###############################
####### Global Setup ##########
###############################

if options.useData == False :
    # global tag for MC
    process.GlobalTag.globaltag = cms.string('START311_V2::All')
else :
    # global tag for 361 data
    #process.GlobalTag.globaltag = cms.string('GR_R_38X_V14::All')
    process.GlobalTag.globaltag = cms.string('GR_R_311_V2::All')

# require scraping filter
process.scrapingVeto = cms.EDFilter("FilterOutScraping",
                                    applyfilter = cms.untracked.bool(True),
                                    debugOn = cms.untracked.bool(False),
                                    numtrack = cms.untracked.uint32(10),
                                    thresh = cms.untracked.double(0.2)
                                    )
# HB + HE noise filtering
process.load('CommonTools/RecoAlgos/HBHENoiseFilter_cfi')


# switch on PAT trigger
from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
switchOnTrigger( process, hltProcess=options.hltProcess )




process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
                                           vertexCollection = cms.InputTag('offlinePrimaryVertices'),
                                           minimumNDOF = cms.uint32(4) ,
                                           maxAbsZ = cms.double(24), 
                                           maxd0 = cms.double(2) 
                                           )




from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector

process.goodOfflinePrimaryVertices = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams = pvSelector.clone( maxZ = cms.double(24.0) ),
    src=cms.InputTag('offlinePrimaryVertices')    
    )


###############################
########## GenJet Setup #######
###############################

process.load("RecoJets.Configuration.GenJetParticles_cff")
from RecoJets.JetProducers.ca4GenJets_cfi import ca4GenJets
process.ca8GenJetsNoNu = ca4GenJets.clone( rParam = cms.double(0.8),
                                           src = cms.InputTag("genParticlesForJetsNoNu"))


###############################
#### Jet RECO includes ########
###############################

from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters
from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.CaloJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
from RecoJets.JetProducers.CATopJetParameters_cfi import *



###############################
########## PF Setup ###########
###############################

# Default PF2PAT with AK5 jets. Make sure to turn ON the L1fastjet stuff. 
from PhysicsTools.PatAlgos.tools.pfTools import *
postfix = "PFlow"
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC=not options.useData, postfix=postfix)
process.pfPileUpPFlow.Enable = True
process.pfJetsPFlow.Vertices = cms.InputTag('goodOfflinePrimaryVertices')
process.pfJetsPFlow.doAreaFastjet = True
process.pfJetsPFlow.doRhoFastjet = False
process.pfJetsPFlow.Ghost_EtaMax = 5.0
process.pfJetsPFlow.Rho_EtaMax = cms.double(5.0)

# In order to have a coherent semileptonic channel also, add
# some "loose" leptons to do QCD estimates.
process.pfIsolatedMuonsLoosePFlow = process.pfIsolatedMuonsPFlow.clone(
    combinedIsolationCut = cms.double(999.0) 
    )

process.patMuonsLoosePFlow = process.patMuonsPFlow.clone(
    pfMuonSource = cms.InputTag("pfIsolatedMuonsLoosePFlow")
    )
adaptPFMuons( process, process.patMuonsLoosePFlow, "PFlow")
process.muonMatchLoosePFlow = process.muonMatchPFlow.clone(
    src = cms.InputTag("pfIsolatedMuonsLoosePFlow")
    )
process.muonMatchPFlow.src = "pfIsolatedMuonsPFlow"

process.selectedPatMuonsLoosePFlow = process.selectedPatMuonsPFlow.clone(
    src = cms.InputTag("patMuonsLoosePFlow")
    )



process.pfIsolatedElectronsLoosePFlow = process.pfIsolatedElectronsPFlow.clone(
    combinedIsolationCut = cms.double(999.0) 
    )

process.patElectronsLoosePFlow = process.patElectronsPFlow.clone(
    pfElectronSource = cms.InputTag("pfIsolatedElectronsLoosePFlow")
    )
adaptPFElectrons( process, process.patElectronsLoosePFlow, "PFlow")

process.selectedPatElectronsLoosePFlow = process.selectedPatElectronsPFlow.clone(
    src = cms.InputTag("patElectronsLoosePFlow")
    )


process.looseLeptonSequence = cms.Sequence(
    process.pfIsolatedMuonsLoosePFlow +
    process.muonMatchLoosePFlow +
    process.patMuonsLoosePFlow +
    process.selectedPatMuonsLoosePFlow +    
    process.pfIsolatedElectronsLoosePFlow +
    process.patElectronsLoosePFlow +
    process.selectedPatElectronsLoosePFlow
    )


# turn to false when running on data
if options.useData :
    removeMCMatching( process, ['All'] )
    process.looseLeptonSequence.remove( process.muonMatchLoosePFlow )

###############################
###### Bare CA 0.8 jets #######
###############################
from RecoJets.JetProducers.ca4PFJets_cfi import ca4PFJets
process.ca8PFJetsPFlow = ca4PFJets.clone(
    rParam = cms.double(0.8),
    src = cms.InputTag('pfNoElectron'+postfix),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True),    
    Ghost_EtaMax = cms.double(5.0),    
    Rho_EtaMax = cms.double(5.0) )


###############################
###### Jet Pruning Setup ######
###############################


# Pruned PF Jets
process.caPrunedPFlow = cms.EDProducer(
    "SubJetProducer",
    PFJetParameters.clone( src = cms.InputTag('pfNoElectron'+postfix),
                           doAreaFastjet = cms.bool(True),
                           doRhoFastjet = cms.bool(False),
                           Ghost_EtaMax = cms.double(5.0),
                           Rho_EtaMax = cms.double(5.0)
                           ),
    AnomalousCellParameters,
    SubJetParameters,
    jetAlgorithm = cms.string("CambridgeAachen"),
    rParam = SubJetParameters.jetSize,
    jetCollInstanceName=cms.string("subjets")
    )

process.caPrunedPFlow.nSubjets = cms.int32(2)

###############################
#### CATopTag Setup ###########
###############################

# CATopJet PF Jets
# with adjacency 
process.caTopTagPFlow = cms.EDProducer(
    "CATopJetProducer",
    PFJetParameters.clone( src = cms.InputTag('pfNoElectron'+postfix),
                           doAreaFastjet = cms.bool(True),
                           doRhoFastjet = cms.bool(False),
                           Ghost_EtaMax = cms.double(5.0),
                           Rho_EtaMax = cms.double(5.0)                           
                           ),
    AnomalousCellParameters,
    CATopJetParameters,
    jetAlgorithm = cms.string("CambridgeAachen"),
    rParam = SubJetParameters.jetSize
    )

process.CATopTagInfosPFlow = cms.EDProducer("CATopJetTagger",
                                    src = cms.InputTag("caTopTagPFlow"),
                                    TopMass = cms.double(171),
                                    TopMassMin = cms.double(0.),
                                    TopMassMax = cms.double(250.),
                                    WMass = cms.double(80.4),
                                    WMassMin = cms.double(0.0),
                                    WMassMax = cms.double(200.0),
                                    MinMassMin = cms.double(0.0),
                                    MinMassMax = cms.double(200.0),
                                    verbose = cms.bool(False)
                                    )





# CATopJet PF Jets

for ipostfix in [postfix] :
    for module in (
        getattr(process,"ca8PFJets" + ipostfix),        
        getattr(process,"CATopTagInfos" + ipostfix),
        getattr(process,"caTopTag" + ipostfix),
        getattr(process,"caPruned" + ipostfix)
        ) :
        getattr(process,"patPF2PATSequence"+ipostfix).replace( getattr(process,"pfNoElectron"+ipostfix), getattr(process,"pfNoElectron"+ipostfix)*module )


# Use the good primary vertices everywhere. 
for imod in [process.patMuonsPFlow, process.patMuonsLoosePFlow, process.patElectronsPFlow, process.patElectronsLoosePFlow] :
    imod.pvSrc = "goodOfflinePrimaryVertices"

addJetCollection(process, 
                 cms.InputTag('ca8PFJetsPFlow'),         # Jet collection; must be already in the event when patLayer0 sequence is executed
                 'CA8', 'PF',
                 doJTA=True,            # Run Jet-Track association & JetCharge
                 doBTagging=True,       # Run b-tagging
                 jetCorrLabel=inputJetCorrLabel,
                 doType1MET=False,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 genJetCollection = cms.InputTag("ca8GenJetsNoNu"),
                 doJetID = False
                 )


addJetCollection(process, 
                 cms.InputTag('caPrunedPFlow'),         # Jet collection; must be already in the event when patLayer0 sequence is executed
                 'CA8Pruned', 'PF',
                 doJTA=True,            # Run Jet-Track association & JetCharge
                 doBTagging=True,       # Run b-tagging
                 jetCorrLabel=inputJetCorrLabel,
                 doType1MET=False,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 genJetCollection = cms.InputTag("ca8GenJetsNoNu"),
                 doJetID = False
                 )


addJetCollection(process, 
                 cms.InputTag('caTopTagPFlow'),
                 'CATopTag', 'PF',
                 doJTA=True,
                 doBTagging=True,
                 jetCorrLabel=inputJetCorrLabel,
                 doType1MET=False,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 genJetCollection = cms.InputTag("ca8GenJetsNoNu"),
                 doJetID = False
                 )


###############################
### TagInfo and Matching Setup#
###############################

# Do some configuration of the jet substructure things
for jetcoll in (process.patJetsPFlow,
                process.patJetsCA8PF,
                process.patJetsCA8PrunedPF,
                process.patJetsCATopTagPF
                ) :
    if options.useData == False :
        jetcoll.embedGenJetMatch = True
        jetcoll.getJetMCFlavour = True
        jetcoll.addGenPartonMatch = True
    # Add CATopTag info... piggy-backing on b-tag functionality
    jetcoll.addBTagInfo = True
    jetcoll.addTagInfos = True
    jetcoll.embedCaloTowers = False
    jetcoll.embedPFCandidates = False
#    jetcoll.embedGenJet = False



###############################
#### Selections Setup #########
###############################

# AK5 Jets
#   PF
process.selectedPatJetsPFlow.cut = cms.string("pt > 30")
process.patJetsPFlow.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAODPFlow")
    )
process.patJetsPFlow.addTagInfos = True
process.patJetsPFlow.embedCaloTowers = False
process.patJetsPFlow.embedPFCandidates = False

process.patJetsPFlow.userData.userFunctions = cms.vstring( "? hasTagInfo('secondaryVertex') && tagInfoSecondaryVertex('secondaryVertex').nVertices() > 0 ? "
                                                      "tagInfoSecondaryVertex('secondaryVertex').secondaryVertex(0).p4().mass() : 0")
process.patJetsPFlow.userData.userFunctionLabels = cms.vstring('secvtxMass')


# CA8 jets
process.selectedPatJetsCA8PF.cut = cms.string("pt > 30")

# CA8 Pruned jets
process.selectedPatJetsCA8PrunedPF.cut = cms.string("pt > 30")

# CA8 TopJets
process.selectedPatJetsCATopTagPF.cut = cms.string("pt > 30")
process.patJetsCATopTagPF.tagInfoSources = cms.VInputTag(
    cms.InputTag('CATopTagInfosPFlow')
    )

# electrons
process.selectedPatElectronsPFlow.cut = cms.string('pt > 10.0')
process.patElectronsPFlow.embedTrack = cms.bool(True)
process.selectedPatElectronsLoosePFlow.cut = cms.string('pt > 10.0')
process.patElectronsLoosePFlow.embedTrack = cms.bool(True)
# muons
process.selectedPatMuonsPFlow.cut = cms.string("pt > 10.0")
process.patMuonsPFlow.embedTrack = cms.bool(True)
process.selectedPatMuonsLoosePFlow.cut = cms.string("pt > 10.0")
process.patMuonsLoosePFlow.embedTrack = cms.bool(True)
# taus
process.selectedPatTausPFlow.cut = cms.string("pt > 5 & abs(eta) < 3")
# photons
process.patPhotonsPFlow.isoDeposits = cms.PSet()
#taus
process.patTausPFlow.isoDeposits = cms.PSet()

# Apply jet ID to all of the jets upstream. We aren't going to screw around
# with this, most likely. So, we don't really to waste time with it
# at the analysis level. 
from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector
process.goodPatJetsPFlow = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                        filterParams = pfJetIDSelector.clone(),
                                        src = cms.InputTag("selectedPatJetsPFlow")
                                        )
process.goodPatJetsCA8PF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                        filterParams = pfJetIDSelector.clone(),
                                        src = cms.InputTag("selectedPatJetsCA8PF")
                                        )
process.goodPatJetsCA8PrunedPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                              filterParams = pfJetIDSelector.clone(),
                                              src = cms.InputTag("selectedPatJetsCA8PrunedPF")
                                              )
process.goodPatJetsCATopTagPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                             filterParams = pfJetIDSelector.clone(),
                                             src = cms.InputTag("selectedPatJetsCATopTagPF")
                                             )

# let it run


process.patseq = cms.Sequence(
    process.scrapingVeto*
    process.goodOfflinePrimaryVertices*
    process.primaryVertexFilter*
    process.HBHENoiseFilter*
    process.genParticlesForJetsNoNu*
    process.ca8GenJetsNoNu*
    getattr(process,"patPF2PATSequence"+postfix)*
    process.looseLeptonSequence*
    process.patDefaultSequence*
    process.goodPatJetsPFlow*
    process.goodPatJetsCA8PF*
    process.goodPatJetsCA8PrunedPF*
    process.goodPatJetsCATopTagPF
    )

if options.useData == True :
    process.patseq.remove( process.genParticlesForJetsNoNu )
    process.patseq.remove( process.genJetParticles )
    process.patseq.remove( process.ca8GenJetsNoNu )


process.p0 = cms.Path(
    process.patseq
    )

process.out.SelectEvents.SelectEvents = cms.vstring('p0')
    
# rename output file
process.out.fileName = cms.untracked.string('ttbsm_413.root')

# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)


# process all the events
process.maxEvents.input = 4000
process.options.wantSummary = True
process.out.dropMetaData = cms.untracked.string("DROPPED")




process.source.inputCommands = cms.untracked.vstring("keep *", "drop *_MEtoEDMConverter_*_*")



process.out.outputCommands = [
    'drop *_cleanPat*_*_*',
    'keep *_selectedPat*_*_*',
    'keep *_goodPat*_*_*',
    'drop patJets_selectedPat*_*_*',
    'drop *_selectedPatJets_*_*',    
    'keep *_patMETs*_*_*',
    'keep *_offlineBeamSpot_*_*',
    'keep *_offlinePrimaryVertices*_*_*',
    'keep *_goodOfflinePrimaryVertices*_*_*',    
    'drop patPFParticles_*_*_*',
    'drop patTaus_*_*_*',
    'keep recoPFJets_caPruned*_*_*',
    'keep recoPFJets_caTopTag*_*_*',
    'keep patTriggerObjects_patTrigger*_*_*',
    'keep patTriggerFilters_patTrigger*_*_*',
    'keep patTriggerPaths_patTrigger*_*_*',
    'keep patTriggerEvent_patTriggerEvent*_*_*',
    'keep *_cleanPatPhotonsTriggerMatch*_*_*',
    'keep *_cleanPatElectronsTriggerMatch*_*_*',
    'keep *_cleanPatMuonsTriggerMatch*_*_*',
    'keep *_cleanPatTausTriggerMatch*_*_*',
    'keep *_cleanPatJetsTriggerMatch*_*_*',
    'keep *_patMETsTriggerMatch*_*_*',
    'keep double_*PFlow*_*_PAT',
    'keep *_TriggerResults_*_*',
    'keep *_hltTriggerSummaryAOD_*_*',
    'keep *_ak5GenJetsNoNu_*_*',
    'keep *_ca8GenJetsNoNu_*_*',    
    #'keep recoTracks_generalTracks_*_*'
    ]

if options.useData :
    process.out.outputCommands += ['drop *_MEtoEDMConverter_*_*',
                                   'keep LumiSummary_lumiProducer_*_*'
                                   ]
else :
    process.out.outputCommands += ['keep *_ca8GenJetsNoNu_*_*',
                                   'keep *_ak5GenJetsNoNu_*_*',                                   
                                   'keep GenRunInfoProduct_generator_*_*',
                                   'keep GenEventInfoProduct_generator_*_*'

                                   ]

if options.writeFat :
    if options.useData :
        process.out.outputCommands += [
            'keep *_pfNoElectron*_*_*',
            'keep recoTracks_generalTracks_*_*'
            ]
    else :
        process.out.outputCommands += [
            'keep *_genParticlesNoNu_*_*',                                       
            'keep *_pfNoElectron*_*_*',
            'keep recoTracks_generalTracks_*_*'
            ]        
            

#open('junk.py','w').write(process.dumpPython())
