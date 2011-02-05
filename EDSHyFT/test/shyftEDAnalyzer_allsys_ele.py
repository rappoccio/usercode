import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

#input stuff for Run/Lumi selection with the "JSON"-formatted files from the PVT group
import FWCore.PythonUtilities.LumiList as LumiList


## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )


###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('useFlavorHistory',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Flavor History Mode")

options.register('sampleNameInput',
                 'top',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Sample name to give histograms")

options.register ('allSys',
                  1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run all systematics (1) or just the central one (0)")

options.register('ignoreTrigger',
                 1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Ignore trigger in selection")


options.parseArguments()

print options

import sys

if options.useFlavorHistory > 0 :
    useFlavorHistory = True
else :
    useFlavorHistory = False

inputDoMC=True

inputSampleName = options.sampleNameInput

inputCutsToIgnore = []
if options.ignoreTrigger == 1 :
    inputCutsToIgnore.append( 'Trigger' )

## Source
if len(options.inputFiles) == 0 :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
                                    #'dcap:///pnfs/cms/WAX/11/store/user/deisher/QCD_Pt-20to30_EMEnriched_TuneZ2_7TeV-pythia6/shyft_387_v1/737d7c15907ff9528cafe5c4f5f659dc/shyft_386_mc_9_1_srJ.root'
                                    #'dcap:///pnfs/cms/WAX/11/store/user/skhalil/TTJets_TuneZ2_7TeV-madgraph-tauola/shyft_387_v1/1bcebbd0f1a486aa7aaef10a50ee94bd/shyft_386_mc_9_1_54K.root'
                                     'dcap:///pnfs/cms/WAX/11/store/user/skhalil/VQQJetsToLL_TuneD6T_scaledown_7TeV-madgraph-tauola/shyft_387_v1/58c449dbeb9a6e986b9b7014f36267b3/shyft_386_mc_78_2_X1i.root'
                                    )
                                )
else :
    filelist = open( options.inputFiles[0], 'r' )
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
                                    filelist.readlines()
                                    )
                                )

if inputDoMC == False :
    process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange( myList )

## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(3000) )

from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("shyftStudies.root")
                                   )

#_____________________________________PF__________________________________________________
process.pfRecoShyftAna = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = inputShyftAnalysis.clone(
                                        muonSrc = cms.InputTag('selectedPatMuons'),
                                        electronSrc = cms.InputTag('selectedPatElectrons'),
                                        metSrc = cms.InputTag('patMETsPF'),
                                        jetSrc = cms.InputTag('selectedPatJetsAK5PF'),                                       
                                        jetPtMin = cms.double(25.0),
                                        minJets = cms.int32(5),
                                        metMin = cms.double(20.0),                                        
                                        heavyFlavour = cms.bool( useFlavorHistory ),
                                        doMC = cms.bool( inputDoMC),
                                        sampleName = cms.string(inputSampleName),
                                        identifier = cms.string('PF'),
                                        jetAlgo = cms.string("pf"),
                                        reweightBTagEff = cms.bool(True),
                                        useCustomPayload = cms.bool(True),
                                        bcEffScale = cms.double(1.00),
                                        lfEffScale = cms.double(0.9),
                                        jetSmear = cms.double(0.1),
                                        cutsToIgnore=cms.vstring(inputCutsToIgnore)
                                        )                                    
                                    )

#___________Special case of MET > 30 and MET < 20 GeV_________________
process.pfRecoShyftAnaMETMax20 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF MET <20'),
        metMin = cms.double(0.0),
        metMax = cms.double(20.0),
        )
    )

process.pfRecoShyftAnaMETMin30 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF MET >30'),
        metMin = cms.double(30.0)
        )
    )


#_____________________________________PFlow__________________________________________________
process.pfShyftAna = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = inputShyftAnalysis.clone(
                                        muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
                                        electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
                                        metSrc = cms.InputTag('patMETsPFlow'),
                                        jetSrc = cms.InputTag('selectedPatJetsPFlow'),
                                        jetPtMin = cms.double(25.0),
                                        minJets = cms.int32(5),
                                        metMin = cms.double(20.0),                                        
                                        heavyFlavour = cms.bool( useFlavorHistory ),
                                        doMC = cms.bool( inputDoMC),
                                        sampleName = cms.string(inputSampleName),
                                        identifier = cms.string('PFlow'),
                                        jetAlgo = cms.string("pf"),
                                        reweightBTagEff = cms.bool(True),
                                        useCustomPayload = cms.bool(True),
                                        bcEffScale = cms.double(1.00),
                                        lfEffScale = cms.double(0.9),
                                        jetSmear = cms.double(0.1),
                                        cutsToIgnore=cms.vstring(inputCutsToIgnore)
                                        )                                    
                                    )

#_____________________________________JPT__________________________________________________
process.jptShyftAna = cms.EDAnalyzer('EDSHyFT',
                                     shyftAnalysis = inputShyftAnalysis.clone(
                                         metSrc = cms.InputTag('patMETsTC'),
                                         jetSrc = cms.InputTag('selectedPatJetsAK5JPT'),                                         
                                         jetPtMin = cms.double(30.0),
                                         metMin = cms.double(20.0),
                                         minJets = cms.int32(5),
                                         heavyFlavour = cms.bool( useFlavorHistory ),
                                         doMC = cms.bool( inputDoMC),
                                         sampleName = cms.string(inputSampleName),
                                         identifier = cms.string('JPT'),
                                         jetAlgo = cms.string("jpt"),
                                         reweightBTagEff = cms.bool(True),
                                         useCustomPayload = cms.bool(True),
                                         bcEffScale = cms.double(1.00),
                                         lfEffScale = cms.double(0.9),
                                         cutsToIgnore=cms.vstring(inputCutsToIgnore)
                                        )
                                     
                                     )


#______________To extract secvtx shapes and >=3 tag jets count _____________________

process.pfRecoShyftAnaMC = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MC'),
    simpleSFCalc = cms.bool(False),
	reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    )
    )

process.pfRecoShyftAnaMCNoMET = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MC no MET'),
    simpleSFCalc = cms.bool(False),
    reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    metMin = cms.double(0.0),
    )
    )

process.pfRecoShyftAnaMCMax20MET = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MC MET < 20'),
    simpleSFCalc = cms.bool(False),
    reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    metMin = cms.double(0.0),
    metMax = cms.double(20.0),
    )
    )

process.pfRecoShyftAnaMCMin30MET = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MC MET > 30'),
    simpleSFCalc = cms.bool(False),
    reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    metMin = cms.double(30.0),
    )
    )

#_________PF2PAT____________________
process.pfShyftAnaMC = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF MC'),
        simpleSFCalc = cms.bool(False),
        reweightBTagEff = cms.bool(False),
        useCustomPayload = cms.bool(False),  
        )
    )

process.pfShyftAnaMCNoMET = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PFlow MC no MET'),
    simpleSFCalc = cms.bool(False),
    reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    metMin = cms.double(0.0),
    )
    )

#_________JPT____________________
process.jptShyftAnaMC = process.jptShyftAna.clone(
    shyftAnalysis = process.jptShyftAna.shyftAnalysis.clone(
    identifier = cms.string('JPT MC'),
    simpleSFCalc = cms.bool(False),
    reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    )
    )

process.jptShyftAnaMCNoMET = process.jptShyftAna.clone(
    shyftAnalysis = process.jptShyftAna.shyftAnalysis.clone(
    identifier = cms.string('JPT MC no MET'),
    simpleSFCalc = cms.bool(False),
    reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    metMin = cms.double(0.0),
    )
    )


################################################
#_______________Systematics__________________
#################################################

#________________________btagging Systematics ____________________________


#____________________PF___________________


process.pfRecoShyftAnaReweightedUnity = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted, unity'),
        reweightBTagEff = cms.bool(True),
        useCustomPayload = cms.bool(True),                                                      
        bcEffScale = cms.double(1.00),
        lfEffScale = cms.double(1.00),        
        )
    )

process.pfRecoShyftAnaReweightedBTag080 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted BTag 080'),
        reweightBTagEff = cms.bool(True),
        useCustomPayload = cms.bool(True),                                                   
        bcEffScale = cms.double(0.80),
        lfEffScale = cms.double(0.9),        
        )
    )

process.pfRecoShyftAnaReweightedBTag090 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted BTag 090'),
        reweightBTagEff = cms.bool(True),
        useCustomPayload = cms.bool(True),
        bcEffScale = cms.double(0.90),
        lfEffScale = cms.double(0.9),        
        )
    )


process.pfRecoShyftAnaReweightedBTag110 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted BTag 110'),
        reweightBTagEff = cms.bool(True),
        useCustomPayload = cms.bool(True),                                                    
        bcEffScale = cms.double(1.10),
        lfEffScale = cms.double(0.9),        
        )
    )

process.pfRecoShyftAnaReweightedBTag120 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted BTag 120'),
        reweightBTagEff = cms.bool(True),
        useCustomPayload = cms.bool(True),                                                    
        bcEffScale = cms.double(1.20),
        lfEffScale = cms.double(0.9),        
        )
    )


##LF

process.pfRecoShyftAnaReweightedLFTag070 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted LFTag 070'),
        reweightBTagEff = cms.bool(True),
        useCustomPayload = cms.bool(True),                                                    
        lfEffScale = cms.double(0.70),
        bcEffScale = cms.double(1.00),        
        )
    )

process.pfRecoShyftAnaReweightedLFTag080 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted LFTag 080'),
        reweightBTagEff = cms.bool(True),
        useCustomPayload = cms.bool(True),                                                    
        lfEffScale = cms.double(0.80),
        bcEffScale = cms.double(1.00),        
        )
    )


process.pfRecoShyftAnaReweightedLFTag090 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted LFTag 090'),
        reweightBTagEff = cms.bool(True),
        useCustomPayload = cms.bool(True),                                                    
        lfEffScale = cms.double(0.90),
        bcEffScale = cms.double(1.00),        
        )
    )

process.pfRecoShyftAnaReweightedLFTag100 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted LFTag 100'),
        reweightBTagEff = cms.bool(True),
        useCustomPayload = cms.bool(True),                                                       
        lfEffScale = cms.double(1.00),
        bcEffScale = cms.double(1.00),        
        )
    )


process.pfRecoShyftAnaReweightedLFTag110 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted LFTag 110'),
        reweightBTagEff = cms.bool(True),
        useCustomPayload = cms.bool(True),                                                       
        lfEffScale = cms.double(1.10),
        bcEffScale = cms.double(1.10),        
        )
    )

#____________________JES up and down with MET Cut > 20_______________________

process.pfRecoShyftAnaJES095 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        jetScale = cms.double(-1.0),
        jetUncertainty = cms.double(0.053),
        identifier = cms.string('PFJES095')
        )
    )

process.pfRecoShyftAnaJES105 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        jetScale = cms.double(1.0),
        jetUncertainty = cms.double(0.053),
        identifier = cms.string('PFJES105')
        )
    )

process.pfRecoShyftAnaJER000 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        jetSmear = cms.double(0.00),
        identifier = cms.string('PFJER000')
        )
    )

process.pfRecoShyftAnaJER020 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        jetSmear = cms.double(0.20),
        identifier = cms.string('PFJER020')
        )
    )

process.pfRecoShyftAnaMETRES090 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        unclMetScale = cms.double( 0.90 ),
        identifier = cms.string('PFMETRES090')
        )
    )

process.pfRecoShyftAnaMETRES110 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        unclMetScale = cms.double( 1.10 ),
        identifier = cms.string('PFMETRES110')
        )
    )

process.pfRecoShyftAnaEleEEPt125 =  process.pfRecoShyftAna.clone(
     shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        ePtScale = cms.double(1.0),
        ePtUncertaintyEE = cms.double( 0.025),
        identifier = cms.string('PFEleEEPt125')
        )
    )

process.pfRecoShyftAnaEleEEPt075 =  process.pfRecoShyftAna.clone(
     shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        ePtScale = cms.double(-1.0),
        ePtUncertaintyEE = cms.double( 0.025),
        identifier = cms.string('PFEleEEPt075')
        )
    )
#____________________JES up and down with MET Cut > 30_______________________
process.pfRecoShyftAnaJES095METMin30 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        metMin = cms.double(30.0),
        jetScale = cms.double(-1.0),
        jetUncertainty = cms.double(0.053),
        identifier = cms.string('PFJES095 MET >30')
        )
    )

process.pfRecoShyftAnaJES105METMin30 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        metMin = cms.double(30.0),
        jetScale = cms.double(1.0),
        jetUncertainty = cms.double(0.053),
        identifier = cms.string('PFJES105 MET >30')
        )
    )

process.pfRecoShyftAnaJER000METMin30 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        metMin = cms.double(30.0),
        jetSmear = cms.double(0.00),
        identifier = cms.string('PFJER000 MET > 30')
        )
    )

process.pfRecoShyftAnaJER020METMin30 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        metMin = cms.double(30.0),
        jetSmear = cms.double(0.20),
        identifier = cms.string('PFJER020 MET >30')
        )
    )


process.pfRecoShyftAnaMETRES090METMin30 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        metMin = cms.double(30.0),
        unclMetScale = cms.double( 0.90 ),
        identifier = cms.string('PFMETRES090 MET > 30')
        )
    )

process.pfRecoShyftAnaMETRES110METMin30 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        metMin = cms.double(30.0),
        unclMetScale = cms.double( 1.10 ),
        identifier = cms.string('PFMETRES110 MET > 30')
        )
    )


#____________________JPT_______________________
process.jptShyftAnaJES095 = process.jptShyftAna.clone(
    shyftAnalysis = process.jptShyftAna.shyftAnalysis.clone(
        jetScale = cms.double(0.95),
        identifier = cms.string('JPTJES095')
        )
    )

process.jptShyftAnaJES105 = process.jptShyftAna.clone(
    shyftAnalysis = process.jptShyftAna.shyftAnalysis.clone(
        jetScale = cms.double(1.05),
        identifier = cms.string('JPTJES105')
        )
    )

#______________ Nominal, JES up and down without MET Cut____________

#___________________PF___________________

process.pfRecoShyftAnaNoMET = process.pfRecoShyftAna.clone(
    shyftAnalysis=process.pfRecoShyftAna.shyftAnalysis.clone(
        metMin = cms.double(0.0),
        identifier = cms.string('PF no MET')
        )
    )

process.pfRecoShyftAnaJES095NoMET = process.pfRecoShyftAnaNoMET.clone(
    shyftAnalysis = process.pfRecoShyftAnaNoMET.shyftAnalysis.clone(
        jetScale = cms.double(0.95),
        identifier = cms.string('PFJES095')
        )
    )

process.pfRecoShyftAnaJES105NoMET = process.pfRecoShyftAnaNoMET.clone(
    shyftAnalysis = process.pfRecoShyftAnaNoMET.shyftAnalysis.clone(
        jetScale = cms.double(1.05),
        identifier = cms.string('PFJES105')
        )
    )

#__________________PF2PAT_____________

process.pfShyftAnaNoMET = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF No MET'),
        metMin = cms.double(0.0)
        )
    )
process.pfShyftAnaJES095 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    jetScale = cms.double(0.95),
    identifier = cms.string('PFlowJES095')
    )
    )

process.pfShyftAnaJES105 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    jetScale = cms.double(1.05),
    identifier = cms.string('PFlowJES105')
    )
    )

#_________________JPT________________

process.jptShyftAnaNoMET = process.jptShyftAna.clone(
    shyftAnalysis = process.jptShyftAna.shyftAnalysis.clone(
        identifier = cms.string('JPT No MET'),
        metMin = cms.double(0.0)
        )
    )


process.jptShyftAnaJES095NoMET = process.jptShyftAnaNoMET.clone(
    shyftAnalysis = process.jptShyftAnaNoMET.shyftAnalysis.clone(
        jetScale = cms.double(0.95),
        identifier = cms.string('JPTJES095')
        )
    )

process.jptShyftAnaJES105NoMET = process.jptShyftAnaNoMET.clone(
    shyftAnalysis = process.jptShyftAnaNoMET.shyftAnalysis.clone(
        jetScale = cms.double(1.05),
        identifier = cms.string('JPTJES105')
        )
    )

process.s = cms.Sequence(
   process.pfRecoShyftAna*                 #Gsf+PF
   process.pfRecoShyftAnaMETMax20*
   process.pfRecoShyftAnaMETMin30*
   process.pfRecoShyftAnaJES095*    
   process.pfRecoShyftAnaJES105*
   process.pfRecoShyftAnaMETRES090*
   process.pfRecoShyftAnaMETRES110*
   process.pfRecoShyftAnaJER000*
   process.pfRecoShyftAnaJER020*
   process.pfRecoShyftAnaEleEEPt125*
   process.pfRecoShyftAnaEleEEPt075*
   #process.pfRecoShyftAnaJES095METMin30*       #MET > 30
   #process.pfRecoShyftAnaJES105METMin30*
   #process.pfRecoShyftAnaMETRES090METMin30*
   #process.pfRecoShyftAnaMETRES110METMin30*
   #process.pfRecoShyftAnaJER000METMin30*
   #process.pfRecoShyftAnaJER020METMin30*
  # process.pfRecoShyftAnaJES095NoMET*    
  # process.pfRecoShyftAnaJES105NoMET*  
    process.pfRecoShyftAnaReweightedUnity*
    process.pfRecoShyftAnaReweightedBTag080*
    process.pfRecoShyftAnaReweightedBTag090*
    process.pfRecoShyftAnaReweightedBTag110*
    process.pfRecoShyftAnaReweightedBTag120*
    process.pfRecoShyftAnaReweightedLFTag070*    
    process.pfRecoShyftAnaReweightedLFTag080*
    process.pfRecoShyftAnaReweightedLFTag090*
    process.pfRecoShyftAnaReweightedLFTag110*
    process.pfRecoShyftAnaNoMET*
    process.pfRecoShyftAnaMC*
    process.pfRecoShyftAnaMCNoMET*
    process.pfRecoShyftAnaMCMax20MET
    #process.pfRecoShyftAnaMCMin30MET
    )

process.p = cms.Path(
    process.pfRecoShyftAna*
    process.pfRecoShyftAnaMC
    )

if options.allSys == 1 :
    process.p *= process.s

process.MessageLogger.cerr.FwkReport.reportEvery = 10000
