
import FWCore.ParameterSet.Config as cms

process = cms.Process("CATopJets")

process.source = cms.Source("PoolSource",
    secondaryFileNames = cms.untracked.vstring(),
    fileNames = cms.untracked.vstring('dcap:///pnfs/cms/WAX/11/store/user/rappocc/RS750_tt_jetMET/RS750_tt_jetMET/d068d0e23f2039f1c38ce13fb13d6982/PYTHIA6_Exotica_RS750_tt_jetMET_10TeV_cff_py_GEN_FASTSIM_10.root', 
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/RS750_tt_jetMET/RS750_tt_jetMET/d068d0e23f2039f1c38ce13fb13d6982/PYTHIA6_Exotica_RS750_tt_jetMET_10TeV_cff_py_GEN_FASTSIM_11.root', 
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/RS750_tt_jetMET/RS750_tt_jetMET/d068d0e23f2039f1c38ce13fb13d6982/PYTHIA6_Exotica_RS750_tt_jetMET_10TeV_cff_py_GEN_FASTSIM_12.root', 
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/RS750_tt_jetMET/RS750_tt_jetMET/d068d0e23f2039f1c38ce13fb13d6982/PYTHIA6_Exotica_RS750_tt_jetMET_10TeV_cff_py_GEN_FASTSIM_13.root', 
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/RS750_tt_jetMET/RS750_tt_jetMET/d068d0e23f2039f1c38ce13fb13d6982/PYTHIA6_Exotica_RS750_tt_jetMET_10TeV_cff_py_GEN_FASTSIM_14.root', 
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/RS750_tt_jetMET/RS750_tt_jetMET/d068d0e23f2039f1c38ce13fb13d6982/PYTHIA6_Exotica_RS750_tt_jetMET_10TeV_cff_py_GEN_FASTSIM_15.root', 
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/RS750_tt_jetMET/RS750_tt_jetMET/d068d0e23f2039f1c38ce13fb13d6982/PYTHIA6_Exotica_RS750_tt_jetMET_10TeV_cff_py_GEN_FASTSIM_16.root', 
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/RS750_tt_jetMET/RS750_tt_jetMET/d068d0e23f2039f1c38ce13fb13d6982/PYTHIA6_Exotica_RS750_tt_jetMET_10TeV_cff_py_GEN_FASTSIM_17.root', 
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/RS750_tt_jetMET/RS750_tt_jetMET/d068d0e23f2039f1c38ce13fb13d6982/PYTHIA6_Exotica_RS750_tt_jetMET_10TeV_cff_py_GEN_FASTSIM_18.root', 
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/RS750_tt_jetMET/RS750_tt_jetMET/d068d0e23f2039f1c38ce13fb13d6982/PYTHIA6_Exotica_RS750_tt_jetMET_10TeV_cff_py_GEN_FASTSIM_19.root', 
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/RS750_tt_jetMET/RS750_tt_jetMET/d068d0e23f2039f1c38ce13fb13d6982/PYTHIA6_Exotica_RS750_tt_jetMET_10TeV_cff_py_GEN_FASTSIM_1.root', 
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/RS750_tt_jetMET/RS750_tt_jetMET/d068d0e23f2039f1c38ce13fb13d6982/PYTHIA6_Exotica_RS750_tt_jetMET_10TeV_cff_py_GEN_FASTSIM_20.root', 
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/RS750_tt_jetMET/RS750_tt_jetMET/d068d0e23f2039f1c38ce13fb13d6982/PYTHIA6_Exotica_RS750_tt_jetMET_10TeV_cff_py_GEN_FASTSIM_2.root', 
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/RS750_tt_jetMET/RS750_tt_jetMET/d068d0e23f2039f1c38ce13fb13d6982/PYTHIA6_Exotica_RS750_tt_jetMET_10TeV_cff_py_GEN_FASTSIM_3.root', 
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/RS750_tt_jetMET/RS750_tt_jetMET/d068d0e23f2039f1c38ce13fb13d6982/PYTHIA6_Exotica_RS750_tt_jetMET_10TeV_cff_py_GEN_FASTSIM_4.root', 
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/RS750_tt_jetMET/RS750_tt_jetMET/d068d0e23f2039f1c38ce13fb13d6982/PYTHIA6_Exotica_RS750_tt_jetMET_10TeV_cff_py_GEN_FASTSIM_5.root', 
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/RS750_tt_jetMET/RS750_tt_jetMET/d068d0e23f2039f1c38ce13fb13d6982/PYTHIA6_Exotica_RS750_tt_jetMET_10TeV_cff_py_GEN_FASTSIM_6.root', 
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/RS750_tt_jetMET/RS750_tt_jetMET/d068d0e23f2039f1c38ce13fb13d6982/PYTHIA6_Exotica_RS750_tt_jetMET_10TeV_cff_py_GEN_FASTSIM_7.root', 
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/RS750_tt_jetMET/RS750_tt_jetMET/d068d0e23f2039f1c38ce13fb13d6982/PYTHIA6_Exotica_RS750_tt_jetMET_10TeV_cff_py_GEN_FASTSIM_8.root', 
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/RS750_tt_jetMET/RS750_tt_jetMET/d068d0e23f2039f1c38ce13fb13d6982/PYTHIA6_Exotica_RS750_tt_jetMET_10TeV_cff_py_GEN_FASTSIM_9.root')
)
process.L2L3CorJetSC5Calo = cms.EDProducer("CaloJetCorrectionProducer",
    src = cms.InputTag("sisCone5CaloJets"),
    correctors = cms.vstring('L2L3JetCorrectorSC5Calo')
)


process.gamIsoDepositEcalFromHits = cms.EDProducer("CandIsoDepositProducer",
    src = cms.InputTag("photons"),
    MultipleDepositsFlag = cms.bool(False),
    trackType = cms.string('candidate'),
    ExtractorPSet = cms.PSet(
        tryBoth = cms.bool(True),
        intStrip = cms.double(0.0),
        subtractSuperClusterEnergy = cms.bool(False),
        checkIsoInnRBarrel = cms.double(0.045),
        checkIsoExtRBarrel = cms.double(0.4),
        etMin = cms.double(-999.0),
        checkIsoEtaStripBarrel = cms.double(0.02),
        checkIsoEtRecHitEndcap = cms.double(0.3),
        DepositLabel = cms.untracked.string(''),
        detector = cms.string('Ecal'),
        barrelEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        isolationVariable = cms.string('et'),
        checkIsoEtCutEndcap = cms.double(7.0),
        endcapEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        intRadius = cms.double(0.0),
        energyMin = cms.double(0.08),
        extRadius = cms.double(0.5),
        checkIsoEtCutBarrel = cms.double(8.0),
        checkIsoEtRecHitBarrel = cms.double(0.08),
        checkIsoInnREndcap = cms.double(0.07),
        minCandEt = cms.double(15.0),
        barrelRecHits = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        ComponentName = cms.string('EgammaRecHitExtractor'),
        endcapRecHits = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        checkIsoExtREndcap = cms.double(0.4),
        checkIsoEtaStripEndcap = cms.double(0.02)
    )
)


process.eidCutBasedExt = cms.EDProducer("EleIdCutBasedExtProducer",
    src = cms.InputTag("pixelMatchGsfElectrons"),
    robustEleIDCuts = cms.PSet(
        barrel = cms.vdouble(0.115, 0.014, 0.09, 0.009),
        endcap = cms.vdouble(0.15, 0.0275, 0.092, 0.0105)
    ),
    reducedEndcapRecHitCollection = cms.InputTag("reducedEcalRecHitsEE"),
    tightEleIDCuts = cms.PSet(
        eSeedOverPinMax = cms.vdouble(99999.0, 99999.0, 99999.0, 99999.0, 99999.0, 
            99999.0, 99999.0, 99999.0),
        eSeedOverPinMin = cms.vdouble(0.24, 0.94, 0.11, 0.0, 0.32, 
            0.83, 0.0, 0.0),
        deltaPhiIn = cms.vdouble(0.032, 0.016, 0.0525, 0.09, 0.025, 
            0.035, 0.065, 0.092),
        hOverE = cms.vdouble(0.05, 0.042, 0.045, 0.0, 0.055, 
            0.037, 0.05, 0.0),
        sigmaEtaEta = cms.vdouble(0.0125, 0.011, 0.01, 0.0, 0.0265, 
            0.0252, 0.026, 0.0),
        deltaEtaIn = cms.vdouble(0.0055, 0.003, 0.0065, 0.0, 0.006, 
            0.0055, 0.0075, 0.0)
    ),
    algorithm = cms.string('eIDCB'),
    filter = cms.bool(False),
    threshold = cms.double(0.5),
    electronQuality = cms.string('robust'),
    looseEleIDCuts = cms.PSet(
        deltaPhiIn = cms.vdouble(0.05, 0.025, 0.053, 0.09, 0.07, 
            0.03, 0.092, 0.092),
        eSeedOverPin = cms.vdouble(0.11, 0.91, 0.11, 0.0, 0.0, 
            0.85, 0.0, 0.0),
        sigmaEtaEta = cms.vdouble(0.014, 0.012, 0.0115, 0.0, 0.0275, 
            0.0265, 0.0265, 0.0),
        deltaEtaIn = cms.vdouble(0.009, 0.0045, 0.0085, 0.0, 0.0105, 
            0.0068, 0.01, 0.0),
        hOverE = cms.vdouble(0.115, 0.1, 0.055, 0.0, 0.145, 
            0.12, 0.15, 0.0)
    ),
    reducedBarrelRecHitCollection = cms.InputTag("reducedEcalRecHitsEB")
)


process.corMetType1Icone5Muons = cms.EDProducer("MuonMET",
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(False),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(False),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(False),
        useCalo = cms.bool(True),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(False)
    ),
    useTrackAssociatorPositions = cms.bool(True),
    useHO = cms.bool(False),
    inputUncorMetLabel = cms.InputTag("corMetType1Icone5"),
    useRecHits = cms.bool(False),
    muonsInputTag = cms.InputTag("goodGlobalMuonsForMET"),
    metTypeInputTag = cms.InputTag("CaloMET"),
    towerEtThreshold = cms.double(0.5),
    uncorMETInputTag = cms.InputTag("met")
)


process.muParamGlobalIsoDepositCalByAssociatorHits = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
        MultipleDepositsFlag = cms.bool(True),
        MuonTrackRefType = cms.string('bestTrkSta'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(True),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(True),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(False),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(True)
        ),
        Threshold_HO = cms.double(0.1),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.1),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.025),
        Noise_HO = cms.double(0.2)
    )
)


process.allLayer1Muons = cms.EDProducer("PATMuonProducer",
    useParticleFlow = cms.bool(False),
    userData = cms.PSet(
        userClasses = cms.PSet(
            src = cms.VInputTag("")
        ),
        userFunctionLabels = cms.vstring(''),
        userFunctions = cms.vstring(''),
        userFloats = cms.PSet(
            src = cms.VInputTag("")
        ),
        userInts = cms.PSet(
            src = cms.VInputTag("")
        )
    ),
    addGenMatch = cms.bool(True),
    addResolutions = cms.bool(False),
    embedTrack = cms.bool(False),
    pfMuonSource = cms.InputTag("pfMuons"),
    addEfficiencies = cms.bool(False),
    embedPFCandidate = cms.bool(False),
    isoDeposits = cms.PSet(
        hcal = cms.InputTag("layer0MuonIsolations","muIsoDepositCalByAssociatorTowershcal"),
        tracker = cms.InputTag("layer0MuonIsolations","muIsoDepositTk"),
        user = cms.VInputTag(cms.InputTag("layer0MuonIsolations","muIsoDepositCalByAssociatorTowersho"), cms.InputTag("layer0MuonIsolations","muIsoDepositJets")),
        ecal = cms.InputTag("layer0MuonIsolations","muIsoDepositCalByAssociatorTowersecal")
    ),
    isolation = cms.PSet(
        hcal = cms.PSet(
            src = cms.InputTag("layer0MuonIsolations","muIsoDepositCalByAssociatorTowershcal"),
            deltaR = cms.double(0.3)
        ),
        tracker = cms.PSet(
            src = cms.InputTag("layer0MuonIsolations","muIsoDepositTk"),
            deltaR = cms.double(0.3)
        ),
        user = cms.VPSet(cms.PSet(
            src = cms.InputTag("layer0MuonIsolations","muIsoDepositCalByAssociatorTowersho"),
            deltaR = cms.double(0.3)
        ), 
            cms.PSet(
                src = cms.InputTag("layer0MuonIsolations","muIsoDepositJets"),
                deltaR = cms.double(0.3)
            )),
        ecal = cms.PSet(
            src = cms.InputTag("layer0MuonIsolations","muIsoDepositCalByAssociatorTowersecal"),
            deltaR = cms.double(0.3)
        )
    ),
    trigPrimMatch = cms.VInputTag(cms.InputTag("muonTrigMatchHLT1MuonNonIso"), cms.InputTag("muonTrigMatchHLT1MET65")),
    efficiencies = cms.PSet(

    ),
    embedGenMatch = cms.bool(False),
    muonSource = cms.InputTag("allLayer0Muons"),
    addTrigMatch = cms.bool(True),
    embedStandAloneMuon = cms.bool(True),
    embedCombinedMuon = cms.bool(True),
    genParticleMatch = cms.InputTag("muonMatch")
)


process.simpleSecondaryVertexBJetTagsAOD = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('simpleSecondaryVertex'),
    tagInfos = cms.VInputTag(cms.InputTag("secondaryVertexTagInfosAOD"))
)


process.patHLTDoubleIsoTauTrk3 = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltFilterL25PixelTau","","HLT")
)


process.softMuonBJetTagsAOD = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('softMuon'),
    tagInfos = cms.VInputTag(cms.InputTag("softMuonTagInfosAOD"))
)


process.patHLT2Electron = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltL1IsoDoubleElectronTrackIsolFilter","","HLT")
)


process.patHLT2Photon = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltL1IsoDoublePhotonDoubleEtFilter","","HLT")
)


process.L2L3CorJetSC7PF = cms.EDProducer("PFJetCorrectionProducer",
    src = cms.InputTag("sisCone7PFJets"),
    correctors = cms.vstring('L2L3JetCorrectorSC7PF')
)


process.L2L3CorJetSC7Calo = cms.EDProducer("CaloJetCorrectionProducer",
    src = cms.InputTag("sisCone7CaloJets"),
    correctors = cms.vstring('L2L3JetCorrectorSC7Calo')
)


process.trackCountingHighEffBJetTagsAOD = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('trackCounting3D2nd'),
    tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfosAOD"))
)


process.simpleSecondaryVertexBJetTags = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('simpleSecondaryVertex'),
    tagInfos = cms.VInputTag(cms.InputTag("secondaryVertexTagInfos"))
)


process.pfRecoTauDiscriminationAgainstMuon = cms.EDProducer("PFRecoTauDiscriminationAgainstMuon",
    a = cms.double(0.5),
    c = cms.double(0.0),
    b = cms.double(0.5),
    discriminatorOption = cms.string('noSegMatch'),
    PFTauProducer = cms.InputTag("pfRecoTauProducer")
)


process.trackCountingHighPurBJetTags = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('trackCounting3D3rd'),
    tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfos"))
)


process.eidTight = cms.EDProducer("EleIdCutBasedExtProducer",
    src = cms.InputTag("pixelMatchGsfElectrons"),
    robustEleIDCuts = cms.PSet(
        barrel = cms.vdouble(0.115, 0.014, 0.09, 0.009),
        endcap = cms.vdouble(0.15, 0.0275, 0.092, 0.0105)
    ),
    reducedEndcapRecHitCollection = cms.InputTag("reducedEcalRecHitsEE"),
    tightEleIDCuts = cms.PSet(
        eSeedOverPinMax = cms.vdouble(99999.0, 99999.0, 99999.0, 99999.0, 99999.0, 
            99999.0, 99999.0, 99999.0),
        eSeedOverPinMin = cms.vdouble(0.24, 0.94, 0.11, 0.0, 0.32, 
            0.83, 0.0, 0.0),
        deltaPhiIn = cms.vdouble(0.032, 0.016, 0.0525, 0.09, 0.025, 
            0.035, 0.065, 0.092),
        hOverE = cms.vdouble(0.05, 0.042, 0.045, 0.0, 0.055, 
            0.037, 0.05, 0.0),
        sigmaEtaEta = cms.vdouble(0.0125, 0.011, 0.01, 0.0, 0.0265, 
            0.0252, 0.026, 0.0),
        deltaEtaIn = cms.vdouble(0.0055, 0.003, 0.0065, 0.0, 0.006, 
            0.0055, 0.0075, 0.0)
    ),
    algorithm = cms.string('eIDCB'),
    filter = cms.bool(False),
    looseEleIDCuts = cms.PSet(
        deltaPhiIn = cms.vdouble(0.05, 0.025, 0.053, 0.09, 0.07, 
            0.03, 0.092, 0.092),
        eSeedOverPin = cms.vdouble(0.11, 0.91, 0.11, 0.0, 0.0, 
            0.85, 0.0, 0.0),
        sigmaEtaEta = cms.vdouble(0.014, 0.012, 0.0115, 0.0, 0.0275, 
            0.0265, 0.0265, 0.0),
        deltaEtaIn = cms.vdouble(0.009, 0.0045, 0.0085, 0.0, 0.0105, 
            0.0068, 0.01, 0.0),
        hOverE = cms.vdouble(0.115, 0.1, 0.055, 0.0, 0.145, 
            0.12, 0.15, 0.0)
    ),
    electronQuality = cms.string('tight'),
    threshold = cms.double(0.5),
    reducedBarrelRecHitCollection = cms.InputTag("reducedEcalRecHitsEB")
)


process.patHLTDoubleMu3 = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltDiMuonIsoL3IsoFiltered","","HLT")
)


process.patHLT1PhotonRelaxed = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltL1NonIsoSinglePhotonTrackIsolFilter","","HLT")
)


process.L2L3CorJetIC5PF = cms.EDProducer("PFJetCorrectionProducer",
    src = cms.InputTag("iterativeCone5PFJets"),
    correctors = cms.vstring('L2L3JetCorrectorIC5PF')
)


process.gamIsoDepositTk = cms.EDProducer("CandIsoDepositProducer",
    src = cms.InputTag("photons"),
    MultipleDepositsFlag = cms.bool(False),
    trackType = cms.string('candidate'),
    ExtractorPSet = cms.PSet(
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        DR_Max = cms.double(0.4),
        NHits_Min = cms.uint32(0),
        checkIsoInnRBarrel = cms.double(0.045),
        checkIsoExtRBarrel = cms.double(0.4),
        checkIsoEtaStripBarrel = cms.double(0.02),
        checkIsoEtRecHitEndcap = cms.double(0.3),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        barrelEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        checkIsoEtCutEndcap = cms.double(7.0),
        endcapEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.0),
        checkIsoEtCutBarrel = cms.double(8.0),
        Chi2Ndof_Max = cms.double(1e+64),
        checkIsoEtRecHitBarrel = cms.double(0.08),
        checkIsoInnREndcap = cms.double(0.07),
        BeamlineOption = cms.string('BeamSpotFromEvent'),
        minCandEt = cms.double(15.0),
        ComponentName = cms.string('TrackExtractor'),
        checkIsoExtREndcap = cms.double(0.4),
        checkIsoEtaStripEndcap = cms.double(0.02)
    )
)


process.eleIsoDepositTk = cms.EDProducer("CandIsoDepositProducer",
    src = cms.InputTag("pixelMatchGsfElectrons"),
    MultipleDepositsFlag = cms.bool(False),
    trackType = cms.string('candidate'),
    ExtractorPSet = cms.PSet(
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        DR_Max = cms.double(0.4),
        NHits_Min = cms.uint32(0),
        checkIsoInnRBarrel = cms.double(0.0),
        checkIsoExtRBarrel = cms.double(0.01),
        checkIsoEtaStripBarrel = cms.double(0.0),
        checkIsoEtRecHitEndcap = cms.double(0.3),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        barrelEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        checkIsoEtCutEndcap = cms.double(10000.0),
        endcapEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.0),
        checkIsoEtCutBarrel = cms.double(10000.0),
        Chi2Ndof_Max = cms.double(1e+64),
        checkIsoEtRecHitBarrel = cms.double(0.08),
        checkIsoInnREndcap = cms.double(0.0),
        BeamlineOption = cms.string('BeamSpotFromEvent'),
        minCandEt = cms.double(0.0),
        ComponentName = cms.string('TrackExtractor'),
        checkIsoExtREndcap = cms.double(0.01),
        checkIsoEtaStripEndcap = cms.double(0.0)
    )
)


process.patHLT2TauPixel = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltFilterL25PixelTau","","HLT")
)


process.patHLTIsoEle15LWL1I = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltL1IsoLargeWindowSingleElectronTrackIsolFilter","","HLT")
)


process.patHLTEle15LWL1R = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltL1NonIsoHLTNonIsoSingleElectronLWEt15TrackIsolFilter","","HLT")
)


process.muParamGlobalIsoDepositCalEcal = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
        MultipleDepositsFlag = cms.bool(False),
        MuonTrackRefType = cms.string('track'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        DR_Veto_H = cms.double(0.1),
        Vertex_Constraint_Z = cms.bool(False),
        Threshold_H = cms.double(0.5),
        ComponentName = cms.string('CaloExtractor'),
        Threshold_E = cms.double(0.2),
        DR_Max = cms.double(1.0),
        DR_Veto_E = cms.double(0.07),
        Weight_E = cms.double(1.0),
        Vertex_Constraint_XY = cms.bool(False),
        DepositLabel = cms.untracked.string('EcalPlusHcal'),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        Weight_H = cms.double(0.0)
    )
)


process.eleIsoDepositEcalSCVetoFromClusts = cms.EDProducer("CandIsoDepositProducer",
    src = cms.InputTag("pixelMatchGsfElectrons"),
    MultipleDepositsFlag = cms.bool(False),
    trackType = cms.string('candidate'),
    ExtractorPSet = cms.PSet(
        ComponentName = cms.string('EgammaEcalExtractor'),
        superClusters = cms.InputTag("egammaSuperClusterMerger"),
        basicClusters = cms.InputTag("egammaBasicClusterMerger"),
        extRadius = cms.double(0.6),
        DepositLabel = cms.untracked.string(''),
        etMin = cms.double(-999.0),
        superClusterMatch = cms.bool(True)
    )
)


process.L2L3CorJetIC5Calo = cms.EDProducer("CaloJetCorrectionProducer",
    src = cms.InputTag("iterativeCone5CaloJets"),
    correctors = cms.vstring('L2L3JetCorrectorIC5Calo')
)


process.softMuonNoIPBJetTagsAOD = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('softMuonNoIP'),
    tagInfos = cms.VInputTag(cms.InputTag("softMuonTagInfosAOD"))
)


process.caTopJetsProducer = cms.EDProducer("CATopJetProducer",
    ptBins = cms.vdouble(500, 800, 1300),
    useMaxTower = cms.bool(False),
    ptFracBins = cms.vdouble(0.1, 0.05, 0.05),
    rBins = cms.vdouble(0.8, 0.6, 0.4),
    algorithm = cms.int32(1),
    etFrac = cms.double(0.7),
    subjetColl = cms.string('caTopSubJets'),
    nCellBins = cms.vint32(1, 1, 1),
    useAdjacency = cms.bool(False),
    centralEtaCut = cms.double(2.5),
    debugLevel = cms.untracked.int32(0),
    sumEtEtaCut = cms.double(3.0),
    correctInputToSignalVertex = cms.bool(True),
    verbose = cms.untracked.bool(False),
    inputEtMin = cms.double(0.5),
    pvCollection = cms.InputTag("offlinePrimaryVertices"),
    jetPtMin = cms.double(1.0),
    jetType = cms.untracked.string('CaloJet'),
    src = cms.InputTag("towerMaker"),
    inputEMin = cms.double(0.0)
)


process.eidRobustLoose = cms.EDProducer("EleIdCutBasedExtProducer",
    src = cms.InputTag("pixelMatchGsfElectrons"),
    robustEleIDCuts = cms.PSet(
        barrel = cms.vdouble(0.115, 0.014, 0.09, 0.009),
        endcap = cms.vdouble(0.15, 0.0275, 0.092, 0.0105)
    ),
    reducedEndcapRecHitCollection = cms.InputTag("reducedEcalRecHitsEE"),
    tightEleIDCuts = cms.PSet(
        eSeedOverPinMax = cms.vdouble(99999.0, 99999.0, 99999.0, 99999.0, 99999.0, 
            99999.0, 99999.0, 99999.0),
        eSeedOverPinMin = cms.vdouble(0.24, 0.94, 0.11, 0.0, 0.32, 
            0.83, 0.0, 0.0),
        deltaPhiIn = cms.vdouble(0.032, 0.016, 0.0525, 0.09, 0.025, 
            0.035, 0.065, 0.092),
        hOverE = cms.vdouble(0.05, 0.042, 0.045, 0.0, 0.055, 
            0.037, 0.05, 0.0),
        sigmaEtaEta = cms.vdouble(0.0125, 0.011, 0.01, 0.0, 0.0265, 
            0.0252, 0.026, 0.0),
        deltaEtaIn = cms.vdouble(0.0055, 0.003, 0.0065, 0.0, 0.006, 
            0.0055, 0.0075, 0.0)
    ),
    algorithm = cms.string('eIDCB'),
    filter = cms.bool(False),
    looseEleIDCuts = cms.PSet(
        deltaPhiIn = cms.vdouble(0.05, 0.025, 0.053, 0.09, 0.07, 
            0.03, 0.092, 0.092),
        eSeedOverPin = cms.vdouble(0.11, 0.91, 0.11, 0.0, 0.0, 
            0.85, 0.0, 0.0),
        sigmaEtaEta = cms.vdouble(0.014, 0.012, 0.0115, 0.0, 0.0275, 
            0.0265, 0.0265, 0.0),
        deltaEtaIn = cms.vdouble(0.009, 0.0045, 0.0085, 0.0, 0.0105, 
            0.0068, 0.01, 0.0),
        hOverE = cms.vdouble(0.115, 0.1, 0.055, 0.0, 0.145, 
            0.12, 0.15, 0.0)
    ),
    electronQuality = cms.string('robust'),
    threshold = cms.double(0.5),
    reducedBarrelRecHitCollection = cms.InputTag("reducedEcalRecHitsEB")
)


process.jetProbabilityBJetTags = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('jetProbability'),
    tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfos"))
)


process.impactParameterMVABJetTags = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('impactParameterMVAComputer'),
    tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfos"))
)


process.eleIsoDepositHcalFromTowers = cms.EDProducer("CandIsoDepositProducer",
    src = cms.InputTag("pixelMatchGsfElectrons"),
    MultipleDepositsFlag = cms.bool(False),
    trackType = cms.string('candidate'),
    ExtractorPSet = cms.PSet(
        caloTowers = cms.InputTag("towerMaker"),
        ComponentName = cms.string('EgammaTowerExtractor'),
        intRadius = cms.double(0.0),
        extRadius = cms.double(0.6),
        DepositLabel = cms.untracked.string(''),
        etMin = cms.double(-999.0)
    )
)


process.pfRecoTauDiscriminationByLeadingTrackFinding = cms.EDProducer("PFRecoTauDiscriminationByLeadingTrackFinding",
    PFTauProducer = cms.InputTag("pfRecoTauProducer")
)


process.L2L3CorJetKT6PF = cms.EDProducer("PFJetCorrectionProducer",
    src = cms.InputTag("kt6PFJets"),
    correctors = cms.vstring('L2L3JetCorrectorKT6PF')
)


process.patPFRecoTauDiscriminationAgainstElectron = cms.EDProducer("PFRecoTauDiscriminationAgainstElectron",
    ApplyCut_ElectronPreID_2D = cms.bool(True),
    ElecPreID0_HOverPLead_minValue = cms.double(0.05),
    PFTauProducer = cms.InputTag("allLayer0Taus"),
    ApplyCut_ElectronPreID = cms.bool(False),
    ApplyCut_HcalTotOverPLead = cms.bool(False),
    EOverPLead_minValue = cms.double(0.8),
    ElecPreID1_EOverPLead_maxValue = cms.double(0.8),
    HcalMaxOverPLead_minValue = cms.double(0.1),
    ApplyCut_EmFraction = cms.bool(False),
    EmFraction_maxValue = cms.double(0.9),
    ApplyCut_HcalMaxOverPLead = cms.bool(False),
    Hcal3x3OverPLead_minValue = cms.double(0.1),
    ElecPreID1_HOverPLead_minValue = cms.double(0.15),
    ElecPreID0_EOverPLead_maxValue = cms.double(0.95),
    BremsRecoveryEOverPLead_minValue = cms.double(0.8),
    ApplyCut_EcalCrackCut = cms.bool(False),
    EOverPLead_maxValue = cms.double(1.8),
    HcalTotOverPLead_minValue = cms.double(0.1),
    ApplyCut_BremsRecoveryEOverPLead = cms.bool(False),
    ApplyCut_Hcal3x3OverPLead = cms.bool(False),
    ApplyCut_EOverPLead = cms.bool(False),
    BremsRecoveryEOverPLead_maxValue = cms.double(1.8)
)


process.impactParameterTagInfos = cms.EDProducer("TrackIPProducer",
    maximumTransverseImpactParameter = cms.double(0.2),
    minimumNumberOfHits = cms.int32(8),
    minimumTransverseMomentum = cms.double(1.0),
    primaryVertex = cms.InputTag("offlinePrimaryVertices"),
    maximumLongitudinalImpactParameter = cms.double(17.0),
    jetTracks = cms.InputTag("ic5JetTracksAssociatorAtVertex"),
    minimumNumberOfPixelHits = cms.int32(2),
    jetDirectionUsingTracks = cms.bool(False),
    computeProbabilities = cms.bool(True),
    useTrackQuality = cms.bool(False),
    maximumChiSquared = cms.double(5.0)
)


process.gamIsoDepositEcalFromClusts = cms.EDProducer("CandIsoDepositProducer",
    src = cms.InputTag("photons"),
    MultipleDepositsFlag = cms.bool(False),
    trackType = cms.string('candidate'),
    ExtractorPSet = cms.PSet(
        ComponentName = cms.string('EgammaEcalExtractor'),
        superClusters = cms.InputTag("egammaSuperClusterMerger"),
        basicClusters = cms.InputTag("egammaBasicClusterMerger"),
        extRadius = cms.double(0.6),
        DepositLabel = cms.untracked.string(''),
        etMin = cms.double(-999.0),
        superClusterMatch = cms.bool(False)
    )
)


process.muIsoDepositCalByAssociatorHits = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("muons"),
        MultipleDepositsFlag = cms.bool(True),
        MuonTrackRefType = cms.string('bestTrkSta'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(True),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(True),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(False),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(True)
        ),
        Threshold_HO = cms.double(0.1),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.1),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.025),
        Noise_HO = cms.double(0.2)
    )
)


process.CATopJetKit = cms.EDProducer("CATopJetKit",
    tauSrc = cms.InputTag("selectedLayer1Taus"),
    enable = cms.string(''),
    muonAxis = cms.PSet(
        m1 = cms.double(0),
        pt2 = cms.double(200),
        pt1 = cms.double(0),
        m2 = cms.double(200)
    ),
    electronSrc = cms.InputTag("selectedLayer1Electrons"),
    jetAxis = cms.PSet(
        m1 = cms.double(0),
        pt2 = cms.double(200),
        pt1 = cms.double(0),
        m2 = cms.double(200)
    ),
    photonAxis = cms.PSet(
        m1 = cms.double(0),
        pt2 = cms.double(200),
        pt1 = cms.double(0),
        m2 = cms.double(200)
    ),
    METAxis = cms.PSet(
        m1 = cms.double(0),
        pt2 = cms.double(200),
        pt1 = cms.double(0),
        m2 = cms.double(200)
    ),
    METSrc = cms.InputTag("selectedLayer1METs"),
    disable = cms.string(''),
    photonSrc = cms.InputTag("selectedLayer1Photons"),
    muonSrc = cms.InputTag("selectedLayer1Muons"),
    jetSrc = cms.InputTag("selectedLayer1Jets"),
    outputTextName = cms.string('CATopJetKit_output.txt'),
    ntuplize = cms.string('all'),
    electronAxis = cms.PSet(
        m1 = cms.double(0),
        pt2 = cms.double(200),
        pt1 = cms.double(0),
        m2 = cms.double(200)
    ),
    tauAxis = cms.PSet(
        m1 = cms.double(0),
        pt2 = cms.double(200),
        pt1 = cms.double(0),
        m2 = cms.double(200)
    ),
    trackAxis = cms.PSet(
        m1 = cms.double(0),
        pt2 = cms.double(200),
        pt1 = cms.double(0),
        m2 = cms.double(200)
    )
)


process.muParamGlobalIsoDepositCalByAssociatorTowers = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
        MultipleDepositsFlag = cms.bool(True),
        MuonTrackRefType = cms.string('bestTrkSta'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    )
)


process.patHLT2MuonNonIso = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltDiMuonNoIsoL3PreFiltered","","HLT")
)


process.muParamGlobalIsoDepositCtfTk = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
        MultipleDepositsFlag = cms.bool(False),
        MuonTrackRefType = cms.string('bestTrkSta'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("ctfGSWithMaterialTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    )
)


process.pfRecoTauDiscriminationAgainstElectron = cms.EDProducer("PFRecoTauDiscriminationAgainstElectron",
    ApplyCut_ElectronPreID_2D = cms.bool(True),
    ElecPreID0_HOverPLead_minValue = cms.double(0.05),
    PFTauProducer = cms.InputTag("pfRecoTauProducer"),
    ApplyCut_ElectronPreID = cms.bool(False),
    ApplyCut_HcalTotOverPLead = cms.bool(False),
    EOverPLead_minValue = cms.double(0.8),
    ElecPreID1_EOverPLead_maxValue = cms.double(0.8),
    HcalMaxOverPLead_minValue = cms.double(0.1),
    ApplyCut_EmFraction = cms.bool(False),
    EmFraction_maxValue = cms.double(0.9),
    ApplyCut_HcalMaxOverPLead = cms.bool(False),
    Hcal3x3OverPLead_minValue = cms.double(0.1),
    ElecPreID1_HOverPLead_minValue = cms.double(0.15),
    ElecPreID0_EOverPLead_maxValue = cms.double(0.95),
    BremsRecoveryEOverPLead_minValue = cms.double(0.8),
    ApplyCut_EcalCrackCut = cms.bool(False),
    EOverPLead_maxValue = cms.double(1.8),
    HcalTotOverPLead_minValue = cms.double(0.1),
    ApplyCut_BremsRecoveryEOverPLead = cms.bool(False),
    ApplyCut_Hcal3x3OverPLead = cms.bool(False),
    ApplyCut_EOverPLead = cms.bool(False),
    BremsRecoveryEOverPLead_maxValue = cms.double(1.8)
)


process.pfRecoTauTagInfoProducer = cms.EDProducer("PFRecoTauTagInfoProducer",
    tkminTrackerHitsn = cms.int32(3),
    tkminPt = cms.double(1.0),
    tkmaxChi2 = cms.double(100.0),
    ChargedHadrCand_AssociationCone = cms.double(0.8),
    ChargedHadrCand_tkminTrackerHitsn = cms.int32(3),
    ChargedHadrCand_tkmaxChi2 = cms.double(100.0),
    tkPVmaxDZ = cms.double(0.2),
    tkminPixelHitsn = cms.int32(0),
    PVProducer = cms.InputTag("offlinePrimaryVertices"),
    PFCandidateProducer = cms.InputTag("particleFlow"),
    ChargedHadrCand_tkminPt = cms.double(1.0),
    UsePVconstraint = cms.bool(False),
    ChargedHadrCand_tkmaxipt = cms.double(0.03),
    NeutrHadrCand_HcalclusminE = cms.double(1.0),
    ChargedHadrCand_tkminPixelHitsn = cms.int32(0),
    GammaCand_EcalclusminE = cms.double(1.0),
    PFJetTracksAssociatorProducer = cms.InputTag("ic5PFJetTracksAssociatorAtVertex"),
    smearedPVsigmaY = cms.double(0.0015),
    smearedPVsigmaX = cms.double(0.0015),
    smearedPVsigmaZ = cms.double(0.005),
    ChargedHadrCand_tkPVmaxDZ = cms.double(0.2),
    tkmaxipt = cms.double(0.03)
)


process.softMuonBJetTags = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('softMuon'),
    tagInfos = cms.VInputTag(cms.InputTag("softMuonTagInfos"))
)


process.allLayer1Jets = cms.EDProducer("PATJetProducer",
    tagInfoModule = cms.InputTag("layer0TagInfos"),
    addJetCharge = cms.bool(True),
    addGenJetMatch = cms.bool(True),
    addAssociatedTracks = cms.bool(True),
    addBTagInfo = cms.bool(True),
    partonJetSource = cms.InputTag("NOT_IMPLEMENTED"),
    addGenPartonMatch = cms.bool(True),
    JetPartonMapSource = cms.InputTag("jetFlavourAssociation"),
    genPartonMatch = cms.InputTag("jetPartonMatch"),
    discriminatorModule = cms.InputTag("layer0BTags"),
    addPartonJetMatch = cms.bool(False),
    embedGenPartonMatch = cms.bool(True),
    efficiencies = cms.PSet(

    ),
    genJetMatch = cms.InputTag("jetGenJetMatch"),
    userData = cms.PSet(
        userClasses = cms.PSet(
            src = cms.VInputTag("")
        ),
        userFunctionLabels = cms.vstring(''),
        userFunctions = cms.vstring(''),
        userFloats = cms.PSet(
            src = cms.VInputTag("")
        ),
        userInts = cms.PSet(
            src = cms.VInputTag("")
        )
    ),
    addTagInfoRefs = cms.bool(True),
    jetSource = cms.InputTag("allLayer0Jets"),
    tagInfoNames = cms.vstring('CATopJetTagger'),
    addEfficiencies = cms.bool(False),
    jetCorrFactorsSource = cms.InputTag("layer0JetCorrFactors"),
    trackAssociationSource = cms.InputTag("layer0JetTracksAssociator"),
    discriminatorNames = cms.vstring('*'),
    embedCaloTowers = cms.bool(True),
    addResolutions = cms.bool(False),
    getJetMCFlavour = cms.bool(True),
    addDiscriminators = cms.bool(False),
    trigPrimMatch = cms.VInputTag(cms.InputTag("jetTrigMatchHLT1ElectronRelaxed"), cms.InputTag("jetTrigMatchHLT2jet")),
    jetChargeSource = cms.InputTag("layer0JetCharge"),
    addJetCorrFactors = cms.bool(True),
    addTrigMatch = cms.bool(True)
)


process.eleIsoDepositEcalFromClusts = cms.EDProducer("CandIsoDepositProducer",
    src = cms.InputTag("pixelMatchGsfElectrons"),
    MultipleDepositsFlag = cms.bool(False),
    trackType = cms.string('candidate'),
    ExtractorPSet = cms.PSet(
        ComponentName = cms.string('EgammaEcalExtractor'),
        superClusters = cms.InputTag("egammaSuperClusterMerger"),
        basicClusters = cms.InputTag("egammaBasicClusterMerger"),
        extRadius = cms.double(0.6),
        DepositLabel = cms.untracked.string(''),
        etMin = cms.double(-999.0),
        superClusterMatch = cms.bool(False)
    )
)


process.corMetGlobalMuons = cms.EDProducer("MuonMET",
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(False),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(False),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(False),
        useCalo = cms.bool(True),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(False)
    ),
    useTrackAssociatorPositions = cms.bool(True),
    useHO = cms.bool(False),
    towerEtThreshold = cms.double(0.5),
    muonsInputTag = cms.InputTag("goodMuonsforMETCorrection"),
    metTypeInputTag = cms.InputTag("CaloMET"),
    useRecHits = cms.bool(False),
    uncorMETInputTag = cms.InputTag("met")
)


process.eleIsoDepositHcalFromHits = cms.EDProducer("CandIsoDepositProducer",
    src = cms.InputTag("pixelMatchGsfElectrons"),
    MultipleDepositsFlag = cms.bool(False),
    trackType = cms.string('candidate'),
    ExtractorPSet = cms.PSet(
        checkIsoInnRBarrel = cms.double(0.0),
        checkIsoExtRBarrel = cms.double(0.01),
        checkIsoEtCutEndcap = cms.double(10000.0),
        etMin = cms.double(-999.0),
        ComponentName = cms.string('EgammaHcalExtractor'),
        endcapEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        checkIsoEtaStripBarrel = cms.double(0.0),
        intRadius = cms.double(0.0),
        checkIsoEtRecHitEndcap = cms.double(0.3),
        extRadius = cms.double(0.5),
        checkIsoEtCutBarrel = cms.double(10000.0),
        checkIsoExtREndcap = cms.double(0.01),
        checkIsoEtRecHitBarrel = cms.double(0.08),
        DepositLabel = cms.untracked.string(''),
        checkIsoInnREndcap = cms.double(0.0),
        checkIsoEtaStripEndcap = cms.double(0.0),
        hcalRecHits = cms.InputTag("hbhereco"),
        minCandEt = cms.double(0.0),
        barrelEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEB")
    )
)


process.allLayer1METs = cms.EDProducer("PATMETProducer",
    metSource = cms.InputTag("allLayer0METs"),
    userData = cms.PSet(
        userClasses = cms.PSet(
            src = cms.VInputTag("")
        ),
        userFunctionLabels = cms.vstring(''),
        userFunctions = cms.vstring(''),
        userFloats = cms.PSet(
            src = cms.VInputTag("")
        ),
        userInts = cms.PSet(
            src = cms.VInputTag("")
        )
    ),
    muonSource = cms.InputTag("muons"),
    addEfficiencies = cms.bool(False),
    addResolutions = cms.bool(False),
    genMETSource = cms.InputTag("genMet"),
    trigPrimMatch = cms.VInputTag(cms.InputTag("metTrigMatchHLT1MET65")),
    efficiencies = cms.PSet(

    ),
    addGenMET = cms.bool(True),
    addMuonCorrections = cms.bool(True),
    addTrigMatch = cms.bool(True)
)


process.patHLTMu11 = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltSingleMuNoIsoL3PreFiltered11","","HLT")
)


process.patHLTLooseIsoTauMET30L1MET = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltFilterSingleTauMETEcalIsolationRelaxed","","HLT")
)


process.trackCountingHighPurBJetTagsAOD = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('trackCounting3D3rd'),
    tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfosAOD"))
)


process.L2L3CorJetKT4Calo = cms.EDProducer("CaloJetCorrectionProducer",
    src = cms.InputTag("kt4CaloJets"),
    correctors = cms.vstring('L2L3JetCorrectorKT4Calo')
)


process.btagSoftElectrons = cms.EDProducer("SoftElectronProducer",
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(False),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(False),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(False)
    ),
    TrackTag = cms.InputTag("generalTracks"),
    BasicClusterTag = cms.InputTag("hybridSuperClusters","hybridBarrelBasicClusters"),
    EndcapRecHitCollection = cms.InputTag("reducedEcalRecHitsEE"),
    HBHERecHitTag = cms.InputTag("hbhereco"),
    BarrelRecHitCollection = cms.InputTag("reducedEcalRecHitsEB"),
    DiscriminatorCut = cms.double(0.9),
    HOverEConeSize = cms.double(0.3)
)


process.caloRecoTauProducer = cms.EDProducer("CaloRecoTauProducer",
    LeadTrack_minPt = cms.double(5.0),
    MatchingConeSize_min = cms.double(0.0),
    ECALSignalConeSizeFormula = cms.string('0.15'),
    TrackerIsolConeMetric = cms.string('DR'),
    TrackerSignalConeMetric = cms.string('DR'),
    ECALSignalConeSize_min = cms.double(0.0),
    ECALRecHit_minEt = cms.double(0.5),
    MatchingConeMetric = cms.string('DR'),
    TrackerSignalConeSizeFormula = cms.string('0.07'),
    MatchingConeSizeFormula = cms.string('0.10'),
    TrackerIsolConeSize_min = cms.double(0.0),
    TrackerIsolConeSize_max = cms.double(0.6),
    TrackerSignalConeSize_max = cms.double(0.6),
    PVProducer = cms.string('offlinePrimaryVertices'),
    TrackerSignalConeSize_min = cms.double(0.0),
    JetPtMin = cms.double(0.0),
    AreaMetric_recoElements_maxabsEta = cms.double(2.5),
    ECALIsolConeMetric = cms.string('DR'),
    ECALIsolConeSizeFormula = cms.string('0.50'),
    ECALIsolConeSize_max = cms.double(0.6),
    ECALSignalConeMetric = cms.string('DR'),
    TrackLeadTrack_maxDZ = cms.double(0.2),
    Track_minPt = cms.double(1.0),
    TrackerIsolConeSizeFormula = cms.string('0.50'),
    ECALSignalConeSize_max = cms.double(0.6),
    ECALIsolConeSize_min = cms.double(0.0),
    UseTrackLeadTrackDZconstraint = cms.bool(True),
    smearedPVsigmaY = cms.double(0.0015),
    smearedPVsigmaX = cms.double(0.0015),
    smearedPVsigmaZ = cms.double(0.005),
    CaloRecoTauTagInfoProducer = cms.InputTag("caloRecoTauTagInfoProducer"),
    MatchingConeSize_max = cms.double(0.6)
)


process.eidRobustTight = cms.EDProducer("EleIdCutBasedExtProducer",
    src = cms.InputTag("pixelMatchGsfElectrons"),
    robustEleIDCuts = cms.PSet(
        barrel = cms.vdouble(0.015, 0.0092, 0.02, 0.0025),
        endcap = cms.vdouble(0.018, 0.025, 0.02, 0.004)
    ),
    reducedEndcapRecHitCollection = cms.InputTag("reducedEcalRecHitsEE"),
    tightEleIDCuts = cms.PSet(
        eSeedOverPinMax = cms.vdouble(99999.0, 99999.0, 99999.0, 99999.0, 99999.0, 
            99999.0, 99999.0, 99999.0),
        eSeedOverPinMin = cms.vdouble(0.24, 0.94, 0.11, 0.0, 0.32, 
            0.83, 0.0, 0.0),
        deltaPhiIn = cms.vdouble(0.032, 0.016, 0.0525, 0.09, 0.025, 
            0.035, 0.065, 0.092),
        hOverE = cms.vdouble(0.05, 0.042, 0.045, 0.0, 0.055, 
            0.037, 0.05, 0.0),
        sigmaEtaEta = cms.vdouble(0.0125, 0.011, 0.01, 0.0, 0.0265, 
            0.0252, 0.026, 0.0),
        deltaEtaIn = cms.vdouble(0.0055, 0.003, 0.0065, 0.0, 0.006, 
            0.0055, 0.0075, 0.0)
    ),
    algorithm = cms.string('eIDCB'),
    filter = cms.bool(False),
    looseEleIDCuts = cms.PSet(
        deltaPhiIn = cms.vdouble(0.05, 0.025, 0.053, 0.09, 0.07, 
            0.03, 0.092, 0.092),
        eSeedOverPin = cms.vdouble(0.11, 0.91, 0.11, 0.0, 0.0, 
            0.85, 0.0, 0.0),
        sigmaEtaEta = cms.vdouble(0.014, 0.012, 0.0115, 0.0, 0.0275, 
            0.0265, 0.0265, 0.0),
        deltaEtaIn = cms.vdouble(0.009, 0.0045, 0.0085, 0.0, 0.0105, 
            0.0068, 0.01, 0.0),
        hOverE = cms.vdouble(0.115, 0.1, 0.055, 0.0, 0.145, 
            0.12, 0.15, 0.0)
    ),
    electronQuality = cms.string('robust'),
    threshold = cms.double(0.5),
    reducedBarrelRecHitCollection = cms.InputTag("reducedEcalRecHitsEB")
)


process.jetBProbabilityBJetTagsAOD = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('jetBProbability'),
    tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfosAOD"))
)


process.pfRecoTauDiscriminationByIsolationUsingLeadingPion = cms.EDProducer("PFRecoTauDiscriminationByIsolationUsingLeadingPion",
    ApplyDiscriminationByECALIsolation = cms.bool(True),
    PFTauProducer = cms.InputTag("pfRecoTauProducer"),
    ManipulateTracks_insteadofChargedHadrCands = cms.bool(False),
    TrackerIsolAnnulus_Tracksmaxn = cms.int32(0),
    ApplyDiscriminationByTrackerIsolation = cms.bool(True),
    TrackerIsolAnnulus_Candsmaxn = cms.int32(0),
    ECALIsolAnnulus_Candsmaxn = cms.int32(0)
)


process.eleIsoDepositEcalFromHits = cms.EDProducer("CandIsoDepositProducer",
    src = cms.InputTag("pixelMatchGsfElectrons"),
    MultipleDepositsFlag = cms.bool(False),
    trackType = cms.string('candidate'),
    ExtractorPSet = cms.PSet(
        tryBoth = cms.bool(True),
        intStrip = cms.double(0.0),
        subtractSuperClusterEnergy = cms.bool(False),
        checkIsoInnRBarrel = cms.double(0.0),
        checkIsoExtRBarrel = cms.double(0.01),
        etMin = cms.double(-999.0),
        checkIsoEtaStripBarrel = cms.double(0.0),
        checkIsoEtRecHitEndcap = cms.double(0.3),
        DepositLabel = cms.untracked.string(''),
        detector = cms.string('Ecal'),
        barrelEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        isolationVariable = cms.string('et'),
        checkIsoEtCutEndcap = cms.double(10000.0),
        endcapEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        intRadius = cms.double(0.0),
        energyMin = cms.double(0.08),
        extRadius = cms.double(0.5),
        checkIsoEtCutBarrel = cms.double(10000.0),
        checkIsoEtRecHitBarrel = cms.double(0.08),
        checkIsoInnREndcap = cms.double(0.0),
        minCandEt = cms.double(0.0),
        barrelRecHits = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        ComponentName = cms.string('EgammaRecHitExtractor'),
        endcapRecHits = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        checkIsoExtREndcap = cms.double(0.01),
        checkIsoEtaStripEndcap = cms.double(0.0)
    )
)


process.patHLT2PhotonRelaxed = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltL1NonIsoDoublePhotonDoubleEtFilter","","HLT")
)


process.pfRecoTauDiscriminationByLeadingTrackFindingHighEfficiency = cms.EDProducer("PFRecoTauDiscriminationByLeadingTrackFinding",
    PFTauProducer = cms.InputTag("pfRecoTauProducerHighEfficiency")
)


process.muParamGlobalIsoDepositCalHcal = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
        MultipleDepositsFlag = cms.bool(False),
        MuonTrackRefType = cms.string('track'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        DR_Veto_H = cms.double(0.1),
        Vertex_Constraint_Z = cms.bool(False),
        Threshold_H = cms.double(0.5),
        ComponentName = cms.string('CaloExtractor'),
        Threshold_E = cms.double(0.2),
        DR_Max = cms.double(1.0),
        DR_Veto_E = cms.double(0.07),
        Weight_E = cms.double(0.0),
        Vertex_Constraint_XY = cms.bool(False),
        DepositLabel = cms.untracked.string('EcalPlusHcal'),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        Weight_H = cms.double(1.0)
    )
)


process.L2L3CorJetKT6Calo = cms.EDProducer("CaloJetCorrectionProducer",
    src = cms.InputTag("kt6CaloJets"),
    correctors = cms.vstring('L2L3JetCorrectorKT6Calo')
)


process.muIsoDepositJets = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("muons"),
        MultipleDepositsFlag = cms.bool(False),
        MuonTrackRefType = cms.string('bestTrkSta'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    )
)


process.impactParameterTagInfosAOD = cms.EDProducer("TrackIPProducer",
    maximumTransverseImpactParameter = cms.double(0.2),
    minimumNumberOfHits = cms.int32(8),
    minimumTransverseMomentum = cms.double(1.0),
    primaryVertex = cms.InputTag("offlinePrimaryVertices"),
    maximumLongitudinalImpactParameter = cms.double(17.0),
    jetTracks = cms.InputTag("jetTracksAssociatorAtVertexAOD"),
    minimumNumberOfPixelHits = cms.int32(2),
    jetDirectionUsingTracks = cms.bool(False),
    computeProbabilities = cms.bool(True),
    useTrackQuality = cms.bool(False),
    maximumChiSquared = cms.double(5.0)
)


process.allLayer1Taus = cms.EDProducer("PATTauProducer",
    tauSource = cms.InputTag("allLayer0Taus"),
    tauIDSources = cms.PSet(
        trackIsolation = cms.InputTag("patPFRecoTauDiscriminationByTrackIsolation"),
        ecalIsolation = cms.InputTag("patPFRecoTauDiscriminationByECALIsolation"),
        leadingTrackFinding = cms.InputTag("patPFRecoTauDiscriminationByLeadingTrackFinding"),
        byIsolation = cms.InputTag("patPFRecoTauDiscriminationByIsolation"),
        leadingTrackPtCut = cms.InputTag("patPFRecoTauDiscriminationByLeadingTrackPtCut"),
        againstMuon = cms.InputTag("patPFRecoTauDiscriminationAgainstMuon"),
        againstElectron = cms.InputTag("patPFRecoTauDiscriminationAgainstElectron")
    ),
    addGenJetMatch = cms.bool(True),
    addResolutions = cms.bool(False),
    embedGenJetMatch = cms.bool(False),
    embedIsolationTracks = cms.bool(False),
    embedSignalTracks = cms.bool(False),
    embedLeadTrack = cms.bool(False),
    isoDeposits = cms.PSet(

    ),
    isolation = cms.PSet(

    ),
    trigPrimMatch = cms.VInputTag(cms.InputTag("tauTrigMatchHLT1Tau")),
    genJetMatch = cms.InputTag("tauGenJetMatch"),
    addGenMatch = cms.bool(True),
    efficiencies = cms.PSet(

    ),
    addEfficiencies = cms.bool(False),
    embedGenMatch = cms.bool(False),
    addTauID = cms.bool(True),
    userData = cms.PSet(
        userClasses = cms.PSet(
            src = cms.VInputTag("")
        ),
        userFunctionLabels = cms.vstring(''),
        userFunctions = cms.vstring(''),
        userFloats = cms.PSet(
            src = cms.VInputTag("")
        ),
        userInts = cms.PSet(
            src = cms.VInputTag("")
        )
    ),
    addTrigMatch = cms.bool(True),
    genParticleMatch = cms.InputTag("tauMatch")
)


process.muIsoDepositTk = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("muons"),
        MultipleDepositsFlag = cms.bool(False),
        MuonTrackRefType = cms.string('bestTrkSta'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    )
)


process.patHLT1Tau = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltFilterL3SingleTau","","HLT")
)


process.muParamGlobalIsoDepositTk = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
        MultipleDepositsFlag = cms.bool(False),
        MuonTrackRefType = cms.string('track'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    )
)


process.secondaryVertexTagInfos = cms.EDProducer("SecondaryVertexProducer",
    trackSelection = cms.PSet(
        totalHitsMin = cms.uint32(8),
        jetDeltaRMax = cms.double(0.3),
        qualityClass = cms.string('highPurity'),
        pixelHitsMin = cms.uint32(2),
        sip3dSigMin = cms.double(-99999.9),
        sip3dSigMax = cms.double(99999.9),
        maxDistToAxis = cms.double(0.2),
        sip2dValMax = cms.double(99999.9),
        maxDecayLen = cms.double(99999.9),
        ptMin = cms.double(1.0),
        sip2dSigMax = cms.double(99999.9),
        sip2dSigMin = cms.double(-99999.9),
        sip3dValMax = cms.double(99999.9),
        sip3dValMin = cms.double(-99999.9),
        sip2dValMin = cms.double(-99999.9),
        normChi2Max = cms.double(99999.9)
    ),
    vertexSelection = cms.PSet(
        sortCriterium = cms.string('dist3dError')
    ),
    vertexCuts = cms.PSet(
        distSig3dMax = cms.double(99999.9),
        fracPV = cms.double(0.65),
        distVal2dMax = cms.double(2.5),
        useTrackWeights = cms.bool(True),
        maxDeltaRToJetAxis = cms.double(0.5),
        v0Filter = cms.PSet(
            k0sMassWindow = cms.double(0.05)
        ),
        distSig2dMin = cms.double(3.0),
        multiplicityMin = cms.uint32(2),
        massMax = cms.double(6.5),
        distSig2dMax = cms.double(99999.9),
        distVal3dMax = cms.double(99999.9),
        minimumTrackWeight = cms.double(0.5),
        distVal3dMin = cms.double(-99999.9),
        distVal2dMin = cms.double(0.01),
        distSig3dMin = cms.double(-99999.9)
    ),
    vertexReco = cms.PSet(
        seccut = cms.double(6.0),
        primcut = cms.double(1.8),
        smoothing = cms.bool(False),
        weightthreshold = cms.double(0.001),
        minweight = cms.double(0.5),
        finder = cms.string('avr')
    ),
    useBeamConstraint = cms.bool(True),
    usePVError = cms.bool(True),
    trackIPTagInfos = cms.InputTag("impactParameterTagInfos"),
    trackSort = cms.string('sip3dSig'),
    minimumTrackWeight = cms.double(0.5)
)


process.pfRecoTauProducerHighEfficiency = cms.EDProducer("PFRecoTauProducer",
    MatchingConeMetric = cms.string('DR'),
    HCALIsolConeMetric = cms.string('DR'),
    ECALSignalConeSizeFormula = cms.string('0.15'),
    TrackerIsolConeMetric = cms.string('DR'),
    TrackerSignalConeMetric = cms.string('DR'),
    EcalStripSumE_deltaPhiOverQ_minValue = cms.double(-0.1),
    HCALIsolConeSize_min = cms.double(0.0),
    TrackerSignalConeSizeFormula = cms.string('5.0/ET'),
    HCALSignalConeSize_max = cms.double(0.6),
    MatchingConeSizeFormula = cms.string('0.1'),
    TrackerIsolConeSize_min = cms.double(0.0),
    GammaCand_minPt = cms.double(1.5),
    ElectronPreIDProducer = cms.InputTag("elecpreid"),
    ChargedHadrCandLeadChargedHadrCand_tksmaxDZ = cms.double(0.2),
    TrackerIsolConeSize_max = cms.double(0.6),
    TrackerSignalConeSize_max = cms.double(0.15),
    MatchingConeSize_min = cms.double(0.0),
    TrackerSignalConeSize_min = cms.double(0.07),
    JetPtMin = cms.double(0.0),
    HCALIsolConeSizeFormula = cms.string('0.50'),
    AreaMetric_recoElements_maxabsEta = cms.double(2.5),
    HCALIsolConeSize_max = cms.double(0.6),
    Track_IsolAnnulus_minNhits = cms.uint32(3),
    HCALSignalConeMetric = cms.string('DR'),
    EcalStripSumE_deltaPhiOverQ_maxValue = cms.double(0.5),
    ChargedHadrCand_IsolAnnulus_minNhits = cms.uint32(8),
    PFTauTagInfoProducer = cms.InputTag("pfRecoTauTagInfoProducer"),
    ECALIsolConeMetric = cms.string('DR'),
    ECALIsolConeSizeFormula = cms.string('0.50'),
    UseChargedHadrCandLeadChargedHadrCand_tksDZconstraint = cms.bool(True),
    ECALIsolConeSize_max = cms.double(0.6),
    PVProducer = cms.string('offlinePrimaryVertices'),
    LeadChargedHadrCand_minPt = cms.double(5.0),
    ECALSignalConeMetric = cms.string('DR'),
    TrackLeadTrack_maxDZ = cms.double(0.2),
    Track_minPt = cms.double(1.0),
    ECALSignalConeSize_min = cms.double(0.0),
    EcalStripSumE_minClusEnergy = cms.double(0.1),
    ElecPreIDLeadTkMatch_maxDR = cms.double(0.01),
    EcalStripSumE_deltaEta = cms.double(0.03),
    TrackerIsolConeSizeFormula = cms.string('0.50'),
    HCALSignalConeSize_min = cms.double(0.0),
    ECALSignalConeSize_max = cms.double(0.6),
    HCALSignalConeSizeFormula = cms.string('0.10'),
    DataType = cms.string('RECO'),
    ECALIsolConeSize_min = cms.double(0.0),
    UseTrackLeadTrackDZconstraint = cms.bool(True),
    smearedPVsigmaY = cms.double(0.0015),
    smearedPVsigmaX = cms.double(0.0015),
    smearedPVsigmaZ = cms.double(0.005),
    ChargedHadrCand_minPt = cms.double(1.0),
    MatchingConeSize_max = cms.double(0.6),
    LeadTrack_minPt = cms.double(5.0),
    NeutrHadrCand_minPt = cms.double(1.0)
)


process.selectedLayer1Hemispheres = cms.EDProducer("PATHemisphereProducer",
    patJets = cms.InputTag("selectedLayer1Jets"),
    maxTauEta = cms.double(-1),
    maxPhotonEta = cms.double(5),
    minMuonEt = cms.double(7),
    patMuons = cms.InputTag("selectedLayer1Muons"),
    seedMethod = cms.int32(3),
    patElectrons = cms.InputTag("selectedLayer1Electrons"),
    patMets = cms.InputTag("selectedLayer1METs"),
    maxMuonEta = cms.double(5),
    minTauEt = cms.double(1000000),
    minPhotonEt = cms.double(200000),
    minElectronEt = cms.double(7),
    patPhotons = cms.InputTag("selectedLayer1Photons"),
    combinationMethod = cms.int32(3),
    maxJetEta = cms.double(5),
    maxElectronEta = cms.double(5),
    minJetEt = cms.double(30),
    patTaus = cms.InputTag("selectedLayer1Taus")
)


process.patPFRecoTauDiscriminationByIsolation = cms.EDProducer("PFRecoTauDiscriminationByIsolation",
    ApplyDiscriminationByECALIsolation = cms.bool(True),
    PFTauProducer = cms.InputTag("allLayer0Taus"),
    ManipulateTracks_insteadofChargedHadrCands = cms.bool(False),
    TrackerIsolAnnulus_Tracksmaxn = cms.int32(0),
    ApplyDiscriminationByTrackerIsolation = cms.bool(True),
    TrackerIsolAnnulus_Candsmaxn = cms.int32(0),
    ECALIsolAnnulus_Candsmaxn = cms.int32(0)
)


process.combinedSecondaryVertexMVABJetTags = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('combinedSecondaryVertexMVA'),
    tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfos"), cms.InputTag("secondaryVertexTagInfos"))
)


process.jetProbabilityBJetTagsAOD = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('jetProbability'),
    tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfosAOD"))
)


process.ecalRecHit = cms.EDProducer("EcalRecHitProducer",
    EEuncalibRecHitCollection = cms.InputTag("ecalWeightUncalibRecHit","EcalUncalibRecHitsEE"),
    ChannelStatusToBeExcluded = cms.vint32(),
    EBuncalibRecHitCollection = cms.InputTag("ecalWeightUncalibRecHit","EcalUncalibRecHitsEB"),
    EBrechitCollection = cms.string('EcalRecHitsEB'),
    EErechitCollection = cms.string('EcalRecHitsEE')
)


process.kt6CaloJets = cms.EDProducer("KtJetProducer",
    Active_Area_Repeats = cms.int32(0),
    UE_Subtraction = cms.string('no'),
    Ghost_EtaMax = cms.double(0.0),
    GhostArea = cms.double(1.0),
    Strategy = cms.string('Best'),
    correctInputToSignalVertex = cms.bool(True),
    verbose = cms.untracked.bool(False),
    inputEtMin = cms.double(0.5),
    pvCollection = cms.InputTag("offlinePrimaryVertices"),
    jetPtMin = cms.double(1.0),
    jetType = cms.untracked.string('CaloJet'),
    src = cms.InputTag("towerMaker"),
    inputEMin = cms.double(0.0),
    FJ_ktRParam = cms.double(0.6),
    alias = cms.untracked.string('KT6CaloJet')
)


process.pfRecoTauDiscriminationByIsolationHighEfficiency = cms.EDProducer("PFRecoTauDiscriminationByIsolation",
    ApplyDiscriminationByECALIsolation = cms.bool(True),
    PFTauProducer = cms.InputTag("pfRecoTauProducerHighEfficiency"),
    ManipulateTracks_insteadofChargedHadrCands = cms.bool(False),
    TrackerIsolAnnulus_Tracksmaxn = cms.int32(0),
    ApplyDiscriminationByTrackerIsolation = cms.bool(True),
    TrackerIsolAnnulus_Candsmaxn = cms.int32(0),
    ECALIsolAnnulus_Candsmaxn = cms.int32(0)
)


process.patHLT1MuonIso = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltSingleMuIsoL3IsoFiltered","","HLT")
)


process.gamIsoDepositHcalFromTowers = cms.EDProducer("CandIsoDepositProducer",
    src = cms.InputTag("photons"),
    MultipleDepositsFlag = cms.bool(False),
    trackType = cms.string('candidate'),
    ExtractorPSet = cms.PSet(
        caloTowers = cms.InputTag("towerMaker"),
        ComponentName = cms.string('EgammaTowerExtractor'),
        intRadius = cms.double(0.0),
        extRadius = cms.double(0.6),
        DepositLabel = cms.untracked.string(''),
        etMin = cms.double(-999.0)
    )
)


process.patPFRecoTauDiscriminationAgainstMuon = cms.EDProducer("PFRecoTauDiscriminationAgainstMuon",
    a = cms.double(0.5),
    c = cms.double(0.0),
    b = cms.double(0.5),
    discriminatorOption = cms.string('noSegMatch'),
    PFTauProducer = cms.InputTag("allLayer0Taus")
)


process.jetBProbabilityBJetTags = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('jetBProbability'),
    tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfos"))
)


process.trackCountingHighEffBJetTags = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('trackCounting3D2nd'),
    tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfos"))
)


process.patHLT1MuonNonIso = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltSingleMuNoIsoL3PreFiltered","","HLT")
)


process.combinedSecondaryVertexBJetTagsAOD = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('combinedSecondaryVertex'),
    tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfosAOD"), cms.InputTag("secondaryVertexTagInfosAOD"))
)


process.pfRecoTauDiscriminationByIsolationUsingLeadingPionHighEfficiency = cms.EDProducer("PFRecoTauDiscriminationByIsolationUsingLeadingPion",
    ApplyDiscriminationByECALIsolation = cms.bool(True),
    PFTauProducer = cms.InputTag("pfRecoTauProducerHighEfficiency"),
    ManipulateTracks_insteadofChargedHadrCands = cms.bool(False),
    TrackerIsolAnnulus_Tracksmaxn = cms.int32(0),
    ApplyDiscriminationByTrackerIsolation = cms.bool(True),
    TrackerIsolAnnulus_Candsmaxn = cms.int32(0),
    ECALIsolAnnulus_Candsmaxn = cms.int32(0)
)


process.softElectronBJetTagsAOD = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('softElectron'),
    tagInfos = cms.VInputTag(cms.InputTag("softElectronTagInfosAOD"))
)


process.allLayer1Photons = cms.EDProducer("PATPhotonProducer",
    userData = cms.PSet(
        userClasses = cms.PSet(
            src = cms.VInputTag("")
        ),
        userFunctionLabels = cms.vstring(''),
        userFunctions = cms.vstring(''),
        userFloats = cms.PSet(
            src = cms.VInputTag("")
        ),
        userInts = cms.PSet(
            src = cms.VInputTag("")
        )
    ),
    addGenMatch = cms.bool(True),
    isolation = cms.PSet(
        hcal = cms.PSet(
            src = cms.InputTag("layer0PhotonIsolations","gamIsoDepositHcalFromTowers"),
            deltaR = cms.double(0.4),
            skipDefaultVeto = cms.bool(True),
            vetos = cms.vstring('0.00')
        ),
        tracker = cms.PSet(
            src = cms.InputTag("layer0PhotonIsolations","gamIsoDepositTk"),
            deltaR = cms.double(0.3),
            skipDefaultVeto = cms.bool(True),
            vetos = cms.vstring('0.015', 
                'Threshold(1.0)')
        ),
        user = cms.VPSet(),
        ecal = cms.PSet(
            src = cms.InputTag("layer0PhotonIsolations","gamIsoDepositEcalFromClusts"),
            deltaR = cms.double(0.4),
            skipDefaultVeto = cms.bool(True),
            vetos = cms.vstring('EcalBarrel:0.045', 
                'EcalBarrel:RectangularEtaPhiVeto(-0.01,0.01,-0.5,0.5)', 
                'EcalEndcaps:0.070', 
                'EcalEndcaps:RectangularEtaPhiVeto(-0.02,0.02,-0.5,0.5)')
        )
    ),
    isoDeposits = cms.PSet(
        hcal = cms.InputTag("layer0PhotonIsolations","gamIsoDepositHcalFromTowers"),
        tracker = cms.InputTag("layer0PhotonIsolations","gamIsoDepositTk"),
        ecal = cms.InputTag("layer0PhotonIsolations","gamIsoDepositEcalFromClusts")
    ),
    trigPrimMatch = cms.VInputTag(cms.InputTag("photonTrigMatchHLT1PhotonRelaxed")),
    efficiencies = cms.PSet(

    ),
    embedSuperCluster = cms.bool(True),
    addEfficiencies = cms.bool(False),
    embedGenMatch = cms.bool(False),
    addTrigMatch = cms.bool(True),
    addPhotonID = cms.bool(True),
    photonIDSource = cms.InputTag("layer0PhotonID"),
    photonSource = cms.InputTag("allLayer0Photons"),
    genParticleMatch = cms.InputTag("photonMatch")
)


process.goodTracks = cms.EDProducer("TrackViewCandidateProducer",
    src = cms.InputTag("generalTracks"),
    particleType = cms.string('pi+'),
    cut = cms.string('pt > 10')
)


process.tauGenJets = cms.EDProducer("TauGenJetProducer",
    includeNeutrinos = cms.bool(False),
    GenParticles = cms.InputTag("genParticles"),
    verbose = cms.untracked.bool(False)
)


process.patPFRecoTauDiscriminationByLeadingTrackFinding = cms.EDProducer("PFRecoTauDiscriminationByLeadingTrackFinding",
    PFTauProducer = cms.InputTag("allLayer0Taus")
)


process.L2L3CorJetSC5PF = cms.EDProducer("PFJetCorrectionProducer",
    src = cms.InputTag("sisCone5PFJets"),
    correctors = cms.vstring('L2L3JetCorrectorSC5PF')
)


process.patHLTDoubleEle5SWL1R = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltL1NonIsoHLTNonIsoDoubleElectronEt5TrackIsolFilter","","HLT")
)


process.gamIsoDepositHcalFromHits = cms.EDProducer("CandIsoDepositProducer",
    src = cms.InputTag("photons"),
    MultipleDepositsFlag = cms.bool(False),
    trackType = cms.string('candidate'),
    ExtractorPSet = cms.PSet(
        checkIsoInnRBarrel = cms.double(0.045),
        checkIsoExtRBarrel = cms.double(0.4),
        checkIsoEtCutEndcap = cms.double(7.0),
        etMin = cms.double(-999.0),
        ComponentName = cms.string('EgammaHcalExtractor'),
        endcapEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        checkIsoEtaStripBarrel = cms.double(0.02),
        intRadius = cms.double(0.0),
        checkIsoEtRecHitEndcap = cms.double(0.3),
        extRadius = cms.double(0.5),
        checkIsoEtCutBarrel = cms.double(8.0),
        checkIsoExtREndcap = cms.double(0.4),
        checkIsoEtRecHitBarrel = cms.double(0.08),
        DepositLabel = cms.untracked.string(''),
        checkIsoInnREndcap = cms.double(0.07),
        checkIsoEtaStripEndcap = cms.double(0.02),
        hcalRecHits = cms.InputTag("hbhereco"),
        minCandEt = cms.double(15.0),
        barrelEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEB")
    )
)


process.pfRecoTauDiscriminationAgainstMuonHighEfficiency = cms.EDProducer("PFRecoTauDiscriminationAgainstMuon",
    a = cms.double(0.5),
    c = cms.double(0.0),
    b = cms.double(0.5),
    discriminatorOption = cms.string('noSegMatch'),
    PFTauProducer = cms.InputTag("pfRecoTauProducerHighEfficiency")
)


process.patHLTDoubleIsoMu3 = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("","","HLT")
)


process.gamIsoDepositEcalSCVetoFromClusts = cms.EDProducer("CandIsoDepositProducer",
    src = cms.InputTag("photons"),
    MultipleDepositsFlag = cms.bool(False),
    trackType = cms.string('candidate'),
    ExtractorPSet = cms.PSet(
        ComponentName = cms.string('EgammaEcalExtractor'),
        superClusters = cms.InputTag("egammaSuperClusterMerger"),
        basicClusters = cms.InputTag("egammaBasicClusterMerger"),
        extRadius = cms.double(0.6),
        DepositLabel = cms.untracked.string(''),
        etMin = cms.double(-999.0),
        superClusterMatch = cms.bool(True)
    )
)


process.softMuonByIP3dBJetTags = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('softLeptonByIP3d'),
    tagInfos = cms.VInputTag(cms.InputTag("softMuonTagInfos"))
)


process.softElectronBJetTags = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('softElectron'),
    tagInfos = cms.VInputTag(cms.InputTag("softElectronTagInfos"))
)


process.patHLT1ElectronRelaxed = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltL1NonIsoSingleElectronTrackIsolFilter","","HLT")
)


process.patHLTIsoMu11 = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltSingleMuIsoL3IsoFiltered","","HLT")
)


process.patCandHLT1ElectronStartup = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltL1IsoLargeWindowSingleElectronTrackIsolFilter","","HLT")
)


process.combinedSecondaryVertexMVABJetTagsAOD = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('combinedSecondaryVertexMVA'),
    tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfosAOD"), cms.InputTag("secondaryVertexTagInfosAOD"))
)


process.patHLT1Electron = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltL1IsoSingleElectronTrackIsolFilter","","HLT")
)


process.combinedSecondaryVertexBJetTags = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('combinedSecondaryVertex'),
    tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfos"), cms.InputTag("secondaryVertexTagInfos"))
)


process.ecalPreshowerRecHit = cms.EDProducer("ESRecHitProducer",
    ESrechitCollection = cms.string('EcalRecHitsES'),
    ESdigiCollection = cms.InputTag("ecalPreshowerDigis")
)


process.pfRecoTauProducer = cms.EDProducer("PFRecoTauProducer",
    MatchingConeMetric = cms.string('DR'),
    HCALIsolConeMetric = cms.string('DR'),
    ECALSignalConeSizeFormula = cms.string('0.15'),
    TrackerIsolConeMetric = cms.string('DR'),
    TrackerSignalConeMetric = cms.string('DR'),
    EcalStripSumE_deltaPhiOverQ_minValue = cms.double(-0.1),
    HCALIsolConeSize_min = cms.double(0.0),
    TrackerSignalConeSizeFormula = cms.string('0.07'),
    HCALSignalConeSize_max = cms.double(0.6),
    MatchingConeSizeFormula = cms.string('0.1'),
    TrackerIsolConeSize_min = cms.double(0.0),
    GammaCand_minPt = cms.double(1.5),
    ElectronPreIDProducer = cms.InputTag("elecpreid"),
    ChargedHadrCandLeadChargedHadrCand_tksmaxDZ = cms.double(0.2),
    TrackerIsolConeSize_max = cms.double(0.6),
    TrackerSignalConeSize_max = cms.double(0.6),
    MatchingConeSize_min = cms.double(0.0),
    TrackerSignalConeSize_min = cms.double(0.0),
    JetPtMin = cms.double(0.0),
    HCALIsolConeSizeFormula = cms.string('0.50'),
    AreaMetric_recoElements_maxabsEta = cms.double(2.5),
    HCALIsolConeSize_max = cms.double(0.6),
    Track_IsolAnnulus_minNhits = cms.uint32(3),
    HCALSignalConeMetric = cms.string('DR'),
    EcalStripSumE_deltaPhiOverQ_maxValue = cms.double(0.5),
    ChargedHadrCand_IsolAnnulus_minNhits = cms.uint32(8),
    PFTauTagInfoProducer = cms.InputTag("pfRecoTauTagInfoProducer"),
    ECALIsolConeMetric = cms.string('DR'),
    ECALIsolConeSizeFormula = cms.string('0.50'),
    UseChargedHadrCandLeadChargedHadrCand_tksDZconstraint = cms.bool(True),
    ECALIsolConeSize_max = cms.double(0.6),
    PVProducer = cms.string('offlinePrimaryVertices'),
    LeadChargedHadrCand_minPt = cms.double(5.0),
    ECALSignalConeMetric = cms.string('DR'),
    TrackLeadTrack_maxDZ = cms.double(0.2),
    Track_minPt = cms.double(1.0),
    ECALSignalConeSize_min = cms.double(0.0),
    EcalStripSumE_minClusEnergy = cms.double(0.1),
    ElecPreIDLeadTkMatch_maxDR = cms.double(0.01),
    EcalStripSumE_deltaEta = cms.double(0.03),
    TrackerIsolConeSizeFormula = cms.string('0.50'),
    HCALSignalConeSize_min = cms.double(0.0),
    ECALSignalConeSize_max = cms.double(0.6),
    HCALSignalConeSizeFormula = cms.string('0.10'),
    DataType = cms.string('RECO'),
    ECALIsolConeSize_min = cms.double(0.0),
    UseTrackLeadTrackDZconstraint = cms.bool(True),
    smearedPVsigmaY = cms.double(0.0015),
    smearedPVsigmaX = cms.double(0.0015),
    smearedPVsigmaZ = cms.double(0.005),
    ChargedHadrCand_minPt = cms.double(1.0),
    MatchingConeSize_max = cms.double(0.6),
    LeadTrack_minPt = cms.double(5.0),
    NeutrHadrCand_minPt = cms.double(1.0)
)


process.patHLTDoubleIsoEle10LWL1I = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltL1IsoLargeWindowDoubleElectronTrackIsolFilter","","HLT")
)


process.impactParameterMVABJetTagsAOD = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('impactParameterMVAComputer'),
    tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfosAOD"))
)


process.L2L3CorJetKT4PF = cms.EDProducer("PFJetCorrectionProducer",
    src = cms.InputTag("kt4PFJets"),
    correctors = cms.vstring('L2L3JetCorrectorKT4PF')
)


process.patHLT2jet = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hlt2jet150","","HLT")
)


process.softMuonByPtBJetTags = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('softLeptonByPt'),
    tagInfos = cms.VInputTag(cms.InputTag("softMuonTagInfos"))
)


process.allLayer1Electrons = cms.EDProducer("PATElectronProducer",
    userData = cms.PSet(
        userClasses = cms.PSet(
            src = cms.VInputTag("")
        ),
        userFunctionLabels = cms.vstring(''),
        userFunctions = cms.vstring(''),
        userFloats = cms.PSet(
            src = cms.VInputTag("")
        ),
        userInts = cms.PSet(
            src = cms.VInputTag("")
        )
    ),
    addGenMatch = cms.bool(True),
    electronIDSources = cms.PSet(
        eidTight = cms.InputTag("patElectronIds","eidTight"),
        eidLoose = cms.InputTag("patElectronIds","eidLoose"),
        eidRobustTight = cms.InputTag("patElectronIds","eidRobustTight"),
        eidRobustHighEnergy = cms.InputTag("patElectronIds","eidRobustHighEnergy"),
        eidRobustLoose = cms.InputTag("patElectronIds","eidRobustLoose")
    ),
    embedTrack = cms.bool(False),
    isolation = cms.PSet(
        hcal = cms.PSet(
            src = cms.InputTag("layer0ElectronIsolations","eleIsoDepositHcalFromTowers"),
            deltaR = cms.double(0.4),
            skipDefaultVeto = cms.bool(True),
            vetos = cms.vstring('0.0')
        ),
        tracker = cms.PSet(
            src = cms.InputTag("layer0ElectronIsolations","eleIsoDepositTk"),
            deltaR = cms.double(0.3),
            skipDefaultVeto = cms.bool(True),
            vetos = cms.vstring('0.015', 
                'Threshold(1.0)')
        ),
        user = cms.VPSet(),
        ecal = cms.PSet(
            src = cms.InputTag("layer0ElectronIsolations","eleIsoDepositEcalFromClusts"),
            deltaR = cms.double(0.4),
            skipDefaultVeto = cms.bool(True),
            vetos = cms.vstring('EcalBarrel:0.045', 
                'EcalBarrel:RectangularEtaPhiVeto(-0.01,0.01,-0.5,0.5)', 
                'EcalEndcaps:0.070', 
                'EcalEndcaps:RectangularEtaPhiVeto(-0.02,0.02,-0.5,0.5)')
        )
    ),
    isoDeposits = cms.PSet(
        hcal = cms.InputTag("layer0ElectronIsolations","eleIsoDepositHcalFromTowers"),
        tracker = cms.InputTag("layer0ElectronIsolations","eleIsoDepositTk"),
        ecal = cms.InputTag("layer0ElectronIsolations","eleIsoDepositEcalFromClusts")
    ),
    electronSource = cms.InputTag("allLayer0Electrons"),
    trigPrimMatch = cms.VInputTag(cms.InputTag("electronTrigMatchHLT1ElectronRelaxed"), cms.InputTag("electronTrigMatchCandHLT1ElectronStartup")),
    addElectronID = cms.bool(True),
    reducedEndcapRecHitCollection = cms.InputTag("reducedEcalRecHitsEE"),
    efficiencies = cms.PSet(

    ),
    addEfficiencies = cms.bool(False),
    embedGenMatch = cms.bool(False),
    embedSuperCluster = cms.bool(True),
    addResolutions = cms.bool(False),
    addTrigMatch = cms.bool(True),
    embedGsfTrack = cms.bool(True),
    addElectronShapes = cms.bool(True),
    reducedBarrelRecHitCollection = cms.InputTag("reducedEcalRecHitsEB"),
    genParticleMatch = cms.InputTag("electronMatch")
)


process.muParamGlobalIsoDepositJets = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
        MultipleDepositsFlag = cms.bool(False),
        MuonTrackRefType = cms.string('bestTrkSta'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    )
)


process.L2L3CorJetIC5JPT = cms.EDProducer("CaloJetCorrectionProducer",
    src = cms.InputTag("JetPlusTrackZSPCorJetIcone5"),
    correctors = cms.vstring('L2L3JetCorrectorIC5JPT')
)


process.muIsoDepositCalByAssociatorTowers = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("muons"),
        MultipleDepositsFlag = cms.bool(True),
        MuonTrackRefType = cms.string('bestTrkSta'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    )
)


process.patHLT4jet = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hlt4jet60","","HLT")
)


process.muParamGlobalIsoDepositGsTk = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
        MultipleDepositsFlag = cms.bool(False),
        MuonTrackRefType = cms.string('track'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("ctfGSWithMaterialTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    )
)


process.CATopJetTagger = cms.EDProducer("CATopJetTagger",
    src = cms.InputTag("caTopJetsProducer"),
    verbose = cms.bool(False),
    TopMassMin = cms.double(0.0),
    WMassMax = cms.double(200.0),
    WMassMin = cms.double(0.0),
    MinMassMin = cms.double(0.0),
    TopMass = cms.double(171),
    MinMassMax = cms.double(200.0),
    WMass = cms.double(80.4),
    TopMassMax = cms.double(250.0)
)


process.softMuonNoIPBJetTags = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('softMuonNoIP'),
    tagInfos = cms.VInputTag(cms.InputTag("softMuonTagInfos"))
)


process.pfRecoTauDiscriminationByIsolation = cms.EDProducer("PFRecoTauDiscriminationByIsolation",
    ApplyDiscriminationByECALIsolation = cms.bool(True),
    PFTauProducer = cms.InputTag("pfRecoTauProducer"),
    ManipulateTracks_insteadofChargedHadrCands = cms.bool(False),
    TrackerIsolAnnulus_Tracksmaxn = cms.int32(0),
    ApplyDiscriminationByTrackerIsolation = cms.bool(True),
    TrackerIsolAnnulus_Candsmaxn = cms.int32(0),
    ECALIsolAnnulus_Candsmaxn = cms.int32(0)
)


process.caloRecoTauTagInfoProducer = cms.EDProducer("CaloRecoTauTagInfoProducer",
    tkminTrackerHitsn = cms.int32(8),
    tkminPixelHitsn = cms.int32(2),
    ECALBasicClusterpropagTrack_matchingDRConeSize = cms.double(0.015),
    PVProducer = cms.string('offlinePrimaryVertices'),
    tkminPt = cms.double(1.0),
    BarrelBasicClustersSource = cms.InputTag("hybridSuperClusters","hybridBarrelBasicClusters"),
    ESRecHitsSource = cms.InputTag("ecalPreshowerRecHit","EcalRecHitsES"),
    UsePVconstraint = cms.bool(False),
    EERecHitsSource = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
    EBRecHitsSource = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
    EndcapBasicClustersSource = cms.InputTag("multi5x5BasicClusters","multi5x5EndcapBasicClusters"),
    smearedPVsigmaY = cms.double(0.0015),
    smearedPVsigmaX = cms.double(0.0015),
    ECALBasicClusterminE = cms.double(1.0),
    smearedPVsigmaZ = cms.double(0.005),
    tkPVmaxDZ = cms.double(0.2),
    ECALBasicClustersAroundCaloJet_DRConeSize = cms.double(0.5),
    tkmaxipt = cms.double(0.03),
    tkmaxChi2 = cms.double(100.0),
    CaloJetTracksAssociatorProducer = cms.string('ic5JetTracksAssociatorAtVertex')
)


process.patHLT1Photon = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltL1IsoSinglePhotonTrackIsolFilter","","HLT")
)


process.patHLT2ElectronRelaxed = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hltL1NonIsoDoubleElectronTrackIsolFilter","","HLT")
)


process.patHLT3jet = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hlt3jet85","","HLT")
)


process.eidRobustHighEnergy = cms.EDProducer("EleIdCutBasedExtProducer",
    src = cms.InputTag("pixelMatchGsfElectrons"),
    robustEleIDCuts = cms.PSet(
        barrel = cms.vdouble(0.05, 0.011, 0.09, 0.005),
        endcap = cms.vdouble(0.1, 0.0275, 0.09, 0.007)
    ),
    reducedEndcapRecHitCollection = cms.InputTag("reducedEcalRecHitsEE"),
    tightEleIDCuts = cms.PSet(
        eSeedOverPinMax = cms.vdouble(99999.0, 99999.0, 99999.0, 99999.0, 99999.0, 
            99999.0, 99999.0, 99999.0),
        eSeedOverPinMin = cms.vdouble(0.24, 0.94, 0.11, 0.0, 0.32, 
            0.83, 0.0, 0.0),
        deltaPhiIn = cms.vdouble(0.032, 0.016, 0.0525, 0.09, 0.025, 
            0.035, 0.065, 0.092),
        hOverE = cms.vdouble(0.05, 0.042, 0.045, 0.0, 0.055, 
            0.037, 0.05, 0.0),
        sigmaEtaEta = cms.vdouble(0.0125, 0.011, 0.01, 0.0, 0.0265, 
            0.0252, 0.026, 0.0),
        deltaEtaIn = cms.vdouble(0.0055, 0.003, 0.0065, 0.0, 0.006, 
            0.0055, 0.0075, 0.0)
    ),
    algorithm = cms.string('eIDCB'),
    filter = cms.bool(False),
    looseEleIDCuts = cms.PSet(
        deltaPhiIn = cms.vdouble(0.05, 0.025, 0.053, 0.09, 0.07, 
            0.03, 0.092, 0.092),
        eSeedOverPin = cms.vdouble(0.11, 0.91, 0.11, 0.0, 0.0, 
            0.85, 0.0, 0.0),
        sigmaEtaEta = cms.vdouble(0.014, 0.012, 0.0115, 0.0, 0.0275, 
            0.0265, 0.0265, 0.0),
        deltaEtaIn = cms.vdouble(0.009, 0.0045, 0.0085, 0.0, 0.0105, 
            0.0068, 0.01, 0.0),
        hOverE = cms.vdouble(0.115, 0.1, 0.055, 0.0, 0.145, 
            0.12, 0.15, 0.0)
    ),
    electronQuality = cms.string('robust'),
    threshold = cms.double(0.5),
    reducedBarrelRecHitCollection = cms.InputTag("reducedEcalRecHitsEB")
)


process.patHLT1MET65 = cms.EDProducer("PATTrigProducer",
    triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    filterName = cms.InputTag("hlt1MET65","","HLT")
)


process.pfRecoTauDiscriminationAgainstElectronHighEfficiency = cms.EDProducer("PFRecoTauDiscriminationAgainstElectron",
    ApplyCut_ElectronPreID_2D = cms.bool(True),
    ElecPreID0_HOverPLead_minValue = cms.double(0.05),
    PFTauProducer = cms.InputTag("pfRecoTauProducerHighEfficiency"),
    ApplyCut_ElectronPreID = cms.bool(False),
    ApplyCut_HcalTotOverPLead = cms.bool(False),
    EOverPLead_minValue = cms.double(0.8),
    ElecPreID1_EOverPLead_maxValue = cms.double(0.8),
    HcalMaxOverPLead_minValue = cms.double(0.1),
    ApplyCut_EmFraction = cms.bool(False),
    EmFraction_maxValue = cms.double(0.9),
    ApplyCut_HcalMaxOverPLead = cms.bool(False),
    Hcal3x3OverPLead_minValue = cms.double(0.1),
    ElecPreID1_HOverPLead_minValue = cms.double(0.15),
    ElecPreID0_EOverPLead_maxValue = cms.double(0.95),
    BremsRecoveryEOverPLead_minValue = cms.double(0.8),
    ApplyCut_EcalCrackCut = cms.bool(False),
    EOverPLead_maxValue = cms.double(1.8),
    HcalTotOverPLead_minValue = cms.double(0.1),
    ApplyCut_BremsRecoveryEOverPLead = cms.bool(False),
    ApplyCut_Hcal3x3OverPLead = cms.bool(False),
    ApplyCut_EOverPLead = cms.bool(False),
    BremsRecoveryEOverPLead_maxValue = cms.double(1.8)
)


process.ecalWeightUncalibRecHit = cms.EDProducer("EcalWeightUncalibRecHitProducer",
    EBdigiCollection = cms.InputTag("ecalDigis","ebDigis"),
    EEhitCollection = cms.string('EcalUncalibRecHitsEE'),
    EEdigiCollection = cms.InputTag("ecalDigis","eeDigis"),
    EBhitCollection = cms.string('EcalUncalibRecHitsEB')
)


process.secondaryVertexTagInfosAOD = cms.EDProducer("SecondaryVertexProducer",
    vertexReco = cms.PSet(
        seccut = cms.double(6.0),
        primcut = cms.double(1.8),
        smoothing = cms.bool(False),
        weightthreshold = cms.double(0.001),
        minweight = cms.double(0.5),
        finder = cms.string('avr')
    ),
    vertexSelection = cms.PSet(
        sortCriterium = cms.string('dist3dError')
    ),
    useBeamConstraint = cms.bool(True),
    vertexCuts = cms.PSet(
        distSig3dMax = cms.double(99999.9),
        fracPV = cms.double(0.65),
        distVal2dMax = cms.double(2.5),
        useTrackWeights = cms.bool(True),
        maxDeltaRToJetAxis = cms.double(0.5),
        v0Filter = cms.PSet(
            k0sMassWindow = cms.double(0.05)
        ),
        distSig2dMin = cms.double(3.0),
        multiplicityMin = cms.uint32(2),
        massMax = cms.double(6.5),
        distSig2dMax = cms.double(99999.9),
        distVal3dMax = cms.double(99999.9),
        minimumTrackWeight = cms.double(0.5),
        distVal3dMin = cms.double(-99999.9),
        distVal2dMin = cms.double(0.01),
        distSig3dMin = cms.double(-99999.9)
    ),
    trackIPTagInfos = cms.InputTag("impactParameterTagInfosAOD"),
    minimumTrackWeight = cms.double(0.5),
    usePVError = cms.bool(True),
    trackSelection = cms.PSet(
        totalHitsMin = cms.uint32(8),
        jetDeltaRMax = cms.double(0.3),
        qualityClass = cms.string('highPurity'),
        pixelHitsMin = cms.uint32(2),
        sip3dSigMin = cms.double(-99999.9),
        sip3dSigMax = cms.double(99999.9),
        maxDistToAxis = cms.double(0.2),
        sip2dValMax = cms.double(99999.9),
        maxDecayLen = cms.double(99999.9),
        ptMin = cms.double(1.0),
        sip2dSigMax = cms.double(99999.9),
        sip2dSigMin = cms.double(-99999.9),
        sip3dValMax = cms.double(99999.9),
        sip3dValMin = cms.double(-99999.9),
        sip2dValMin = cms.double(-99999.9),
        normChi2Max = cms.double(99999.9)
    ),
    trackSort = cms.string('sip3dSig')
)


process.eidLoose = cms.EDProducer("EleIdCutBasedExtProducer",
    src = cms.InputTag("pixelMatchGsfElectrons"),
    robustEleIDCuts = cms.PSet(
        barrel = cms.vdouble(0.115, 0.014, 0.09, 0.009),
        endcap = cms.vdouble(0.15, 0.0275, 0.092, 0.0105)
    ),
    reducedEndcapRecHitCollection = cms.InputTag("reducedEcalRecHitsEE"),
    tightEleIDCuts = cms.PSet(
        eSeedOverPinMax = cms.vdouble(99999.0, 99999.0, 99999.0, 99999.0, 99999.0, 
            99999.0, 99999.0, 99999.0),
        eSeedOverPinMin = cms.vdouble(0.24, 0.94, 0.11, 0.0, 0.32, 
            0.83, 0.0, 0.0),
        deltaPhiIn = cms.vdouble(0.032, 0.016, 0.0525, 0.09, 0.025, 
            0.035, 0.065, 0.092),
        hOverE = cms.vdouble(0.05, 0.042, 0.045, 0.0, 0.055, 
            0.037, 0.05, 0.0),
        sigmaEtaEta = cms.vdouble(0.0125, 0.011, 0.01, 0.0, 0.0265, 
            0.0252, 0.026, 0.0),
        deltaEtaIn = cms.vdouble(0.0055, 0.003, 0.0065, 0.0, 0.006, 
            0.0055, 0.0075, 0.0)
    ),
    algorithm = cms.string('eIDCB'),
    filter = cms.bool(False),
    looseEleIDCuts = cms.PSet(
        deltaPhiIn = cms.vdouble(0.05, 0.025, 0.053, 0.09, 0.07, 
            0.03, 0.092, 0.092),
        eSeedOverPin = cms.vdouble(0.11, 0.91, 0.11, 0.0, 0.0, 
            0.85, 0.0, 0.0),
        sigmaEtaEta = cms.vdouble(0.014, 0.012, 0.0115, 0.0, 0.0275, 
            0.0265, 0.0265, 0.0),
        deltaEtaIn = cms.vdouble(0.009, 0.0045, 0.0085, 0.0, 0.0105, 
            0.0068, 0.01, 0.0),
        hOverE = cms.vdouble(0.115, 0.1, 0.055, 0.0, 0.145, 
            0.12, 0.15, 0.0)
    ),
    electronQuality = cms.string('loose'),
    threshold = cms.double(0.5),
    reducedBarrelRecHitCollection = cms.InputTag("reducedEcalRecHitsEB")
)


process.jetCorrFactors = cms.EDProducer("JetCorrFactorsProducer",
    L7udsJetCorrector = cms.string('L7PartonJetCorrectorKT6qJet'),
    L5cJetCorrector = cms.string('none'),
    L2JetCorrector = cms.string('L2RelativeJetCorrectorKT6Calo'),
    L7bJetCorrector = cms.string('L7PartonJetCorrectorKT6bJet'),
    L6JetCorrector = cms.string('none'),
    L5gluonJetCorrector = cms.string('none'),
    L3JetCorrector = cms.string('L3AbsoluteJetCorrectorKT6Calo'),
    L4JetCorrector = cms.string('none'),
    L7cJetCorrector = cms.string('L7PartonJetCorrectorKT6cJet'),
    L5bJetCorrector = cms.string('none'),
    L5udsJetCorrector = cms.string('none'),
    jetSource = cms.InputTag("caTopJetsProducer"),
    L7gluonJetCorrector = cms.string('L7PartonJetCorrectorKT6gJet'),
    L1JetCorrector = cms.string('none')
)


process.horeco = cms.EDFilter("HcalSimpleReconstructor",
    correctionPhaseNS = cms.double(13.0),
    digiLabel = cms.InputTag("hcalDigis"),
    samplesToAdd = cms.int32(4),
    Subdetector = cms.string('HO'),
    correctForTimeslew = cms.bool(True),
    correctForPhaseContainment = cms.bool(True),
    firstSample = cms.int32(4)
)


process.pfRecoTauDiscriminationByLeadingPionPtCut = cms.EDFilter("PFRecoTauDiscriminationByLeadingPionPtCut",
    MinPtLeadingPion = cms.double(5.0),
    PFTauProducer = cms.InputTag("pfRecoTauProducer")
)


process.selectedLayer1Muons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("allLayer1Muons"),
    cut = cms.string('et > 50. & abs(eta) < 2.5 && caloIso < 3.0')
)


process.corMetType1Icone5 = cms.EDFilter("Type1MET",
    inputUncorJetsLabel = cms.string('iterativeCone5CaloJets'),
    jetEMfracLimit = cms.double(0.9),
    metType = cms.string('CaloMET'),
    jetPTthreshold = cms.double(20.0),
    inputUncorMetLabel = cms.string('met'),
    corrector = cms.string('L2L3JetCorrectorIC5Calo')
)


process.patAODBTags = cms.EDFilter("MultipleDiscriminatorsToValueMaps",
    associations = cms.VInputTag("jetBProbabilityBJetTagsAOD", "jetProbabilityBJetTagsAOD", "trackCountingHighPurBJetTagsAOD", "trackCountingHighEffBJetTagsAOD", "impactParameterMVABJetTagsAOD", 
        "simpleSecondaryVertexBJetTagsAOD", "combinedSecondaryVertexBJetTagsAOD", "combinedSecondaryVertexMVABJetTagsAOD", "softElectronBJetTagsAOD", "softMuonBJetTagsAOD", 
        "softMuonNoIPBJetTagsAOD"),
    collection = cms.InputTag("caTopJetsProducer"),
    failSilently = cms.untracked.bool(True)
)


process.eleIsoFromDepsEcalFromClusts = cms.EDFilter("CandIsolatorFromDeposits",
    deposits = cms.VPSet(cms.PSet(
        src = cms.InputTag("eleIsoDepositEcalFromClusts"),
        deltaR = cms.double(0.4),
        weight = cms.string('1'),
        vetos = cms.vstring('EcalBarrel:0.045', 
            'EcalBarrel:RectangularEtaPhiVeto(-0.01,0.01,-0.5,0.5)', 
            'EcalEndcaps:0.070', 
            'EcalEndcaps:RectangularEtaPhiVeto(-0.02,0.02,-0.5,0.5)'),
        skipDefaultVeto = cms.bool(True),
        mode = cms.string('sum')
    ))
)


process.electronTrigMatchHLTDoubleIsoEle10LWL1I = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Electrons"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLTDoubleIsoEle10LWL1I")
)


process.electronTrigMatchHLTDoubleEle5SWL1R = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Electrons"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLTDoubleEle5SWL1R")
)


process.pfRecoTauDiscriminationByLeadingTrackPtCut = cms.EDFilter("PFRecoTauDiscriminationByLeadingTrackPtCut",
    MinPtLeadingTrack = cms.double(5.0),
    PFTauProducer = cms.InputTag("pfRecoTauProducer")
)


process.muonTrigMatchHLTMu11 = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Muons"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLTMu11")
)


process.allLayer0Jets = cms.EDFilter("PATBasicJetCleaner",
    saveAll = cms.string(''),
    jetSource = cms.InputTag("caTopJetsProducer"),
    saveRejected = cms.string(''),
    markItems = cms.bool(True),
    selection = cms.PSet(
        type = cms.string('none')
    ),
    bitsToIgnore = cms.vstring('Overlap/All'),
    removeOverlaps = cms.PSet(
        electrons = cms.PSet(
            deltaR = cms.double(0.3),
            cut = cms.string('pt > 10'),
            flags = cms.vstring('Isolation/Tracker'),
            collection = cms.InputTag("allLayer0Electrons")
        ),
        user = cms.VPSet()
    )
)


process.eleIsoFromDepsTk = cms.EDFilter("CandIsolatorFromDeposits",
    deposits = cms.VPSet(cms.PSet(
        src = cms.InputTag("eleIsoDepositTk"),
        deltaR = cms.double(0.3),
        weight = cms.string('1'),
        vetos = cms.vstring('0.015', 
            'Threshold(1.0)'),
        skipDefaultVeto = cms.bool(True),
        mode = cms.string('sum')
    ))
)


process.ic5JetTracksAssociatorAtVertex = cms.EDFilter("JetTracksAssociatorAtVertex",
    tracks = cms.InputTag("generalTracks"),
    coneSize = cms.double(0.5),
    jets = cms.InputTag("iterativeCone5CaloJets")
)


process.eleIsoFromDepsEcalFromHits = cms.EDFilter("CandIsolatorFromDeposits",
    deposits = cms.VPSet(cms.PSet(
        src = cms.InputTag("eleIsoDepositEcalFromHits"),
        deltaR = cms.double(0.4),
        weight = cms.string('1'),
        vetos = cms.vstring('EcalBarrel:0.045', 
            'EcalBarrel:RectangularEtaPhiVeto(-0.02,0.02,-0.5,0.5)', 
            'EcalBarrel:ThresholdFromTransverse(0.08)', 
            'EcalEndcaps:ThresholdFromTransverse(0.3)', 
            'EcalEndcaps:0.070', 
            'EcalEndcaps:RectangularEtaPhiVeto(-0.02,0.02,-0.5,0.5)'),
        skipDefaultVeto = cms.bool(True),
        mode = cms.string('sum')
    ))
)


process.genParticlesForJets = cms.EDFilter("InputGenJetsParticleSelector",
    src = cms.InputTag("genParticles"),
    ignoreParticleIDs = cms.vuint32(1000022, 2000012, 2000014, 2000016, 1000039, 
        5000039, 4000012, 9900012, 9900014, 9900016, 
        39),
    partonicFinalState = cms.bool(False),
    excludeResonances = cms.bool(True),
    excludeFromResonancePids = cms.vuint32(12, 13, 14, 16),
    tausAsJets = cms.bool(False)
)


process.muonTrigMatchHLTDoubleIsoMu3 = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Muons"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLTDoubleIsoMu3")
)


process.jetTrigMatchHLT2jet = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Jets"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLT2jet")
)


process.patAODElectronIsolations = cms.EDFilter("MultipleIsoDepositsToValueMaps",
    associations = cms.VInputTag(cms.InputTag("eleIsoDepositTk"), cms.InputTag("eleIsoDepositEcalFromClusts"), cms.InputTag("eleIsoDepositHcalFromTowers")),
    collection = cms.InputTag("pixelMatchGsfElectrons")
)


process.pfRecoTauDiscriminationByECALIsolationUsingLeadingPion = cms.EDFilter("PFRecoTauDiscriminationByIsolationUsingLeadingPion",
    ApplyDiscriminationByECALIsolation = cms.bool(True),
    PFTauProducer = cms.InputTag("pfRecoTauProducer"),
    ManipulateTracks_insteadofChargedHadrCands = cms.bool(False),
    TrackerIsolAnnulus_Tracksmaxn = cms.int32(0),
    ApplyDiscriminationByTrackerIsolation = cms.bool(False),
    TrackerIsolAnnulus_Candsmaxn = cms.int32(0),
    ECALIsolAnnulus_Candsmaxn = cms.int32(0)
)


process.pfRecoTauDiscriminationByTrackIsolation = cms.EDFilter("PFRecoTauDiscriminationByIsolation",
    ApplyDiscriminationByECALIsolation = cms.bool(False),
    PFTauProducer = cms.InputTag("pfRecoTauProducer"),
    ManipulateTracks_insteadofChargedHadrCands = cms.bool(False),
    TrackerIsolAnnulus_Tracksmaxn = cms.int32(0),
    ApplyDiscriminationByTrackerIsolation = cms.bool(True),
    TrackerIsolAnnulus_Candsmaxn = cms.int32(0),
    ECALIsolAnnulus_Candsmaxn = cms.int32(0)
)


process.maxLayer1Muons = cms.EDFilter("PATMuonMaxFilter",
    maxNumber = cms.uint32(999999),
    src = cms.InputTag("selectedLayer1Muons")
)


process.photonTrigMatchHLT2Photon = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Photons"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLT2Photon")
)


process.selectedLayer1METs = cms.EDFilter("PATMETSelector",
    src = cms.InputTag("allLayer1METs"),
    cut = cms.string('et > 200.0')
)


process.patPFRecoTauDiscriminationByECALIsolation = cms.EDFilter("PFRecoTauDiscriminationByIsolation",
    ApplyDiscriminationByECALIsolation = cms.bool(True),
    PFTauProducer = cms.InputTag("allLayer0Taus"),
    ManipulateTracks_insteadofChargedHadrCands = cms.bool(False),
    TrackerIsolAnnulus_Tracksmaxn = cms.int32(0),
    ApplyDiscriminationByTrackerIsolation = cms.bool(False),
    TrackerIsolAnnulus_Candsmaxn = cms.int32(0),
    ECALIsolAnnulus_Candsmaxn = cms.int32(0)
)


process.jetTrigMatchHLT1ElectronRelaxed = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Jets"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLT1ElectronRelaxed")
)


process.electronTrigMatchHLT2ElectronRelaxed = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Electrons"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLT2ElectronRelaxed")
)


process.layer0PhotonID = cms.EDFilter("CandValueMapSkimmerPhotonID",
    collection = cms.InputTag("allLayer0Photons"),
    association = cms.InputTag("patAODPhotonID"),
    backrefs = cms.InputTag("allLayer0Photons")
)


process.pfRecoTauDiscriminationByTrackIsolationUsingLeadingPion = cms.EDFilter("PFRecoTauDiscriminationByIsolationUsingLeadingPion",
    ApplyDiscriminationByECALIsolation = cms.bool(False),
    PFTauProducer = cms.InputTag("pfRecoTauProducer"),
    ManipulateTracks_insteadofChargedHadrCands = cms.bool(False),
    TrackerIsolAnnulus_Tracksmaxn = cms.int32(0),
    ApplyDiscriminationByTrackerIsolation = cms.bool(True),
    TrackerIsolAnnulus_Candsmaxn = cms.int32(0),
    ECALIsolAnnulus_Candsmaxn = cms.int32(0)
)


process.gamIsoFromDepsHcalFromTowers = cms.EDFilter("CandIsolatorFromDeposits",
    deposits = cms.VPSet(cms.PSet(
        src = cms.InputTag("gamIsoDepositHcalFromTowers"),
        deltaR = cms.double(0.4),
        weight = cms.string('1'),
        vetos = cms.vstring('0.00'),
        skipDefaultVeto = cms.bool(True),
        mode = cms.string('sum')
    ))
)


process.jetPartons = cms.EDFilter("PartonSelector",
    withLeptons = cms.bool(False),
    withTop = cms.bool(True)
)


process.electronTrigMatchCandHLT1ElectronStartup = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Electrons"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patCandHLT1ElectronStartup")
)


process.AODJetCharge = cms.EDFilter("JetChargeValueMap",
    var = cms.string('Pt'),
    src = cms.InputTag("iterativeCone5CaloJets"),
    jetTracksAssociation = cms.InputTag("patAODJetTracksAssociator"),
    exp = cms.double(1.0)
)


process.countLayer1Leptons = cms.EDFilter("PATLeptonCountFilter",
    maxNumber = cms.uint32(999999),
    countElectrons = cms.bool(True),
    muonSource = cms.InputTag("selectedLayer1Muons"),
    minNumber = cms.uint32(0),
    electronSource = cms.InputTag("selectedLayer1Electrons"),
    tauSource = cms.InputTag("selectedLayer1Taus"),
    countTaus = cms.bool(False),
    countMuons = cms.bool(True)
)


process.jetTrigMatchHLT3jet = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Jets"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLT3jet")
)


process.allLayer0PFJets = cms.EDFilter("PATPFJetCleaner",
    saveAll = cms.string(''),
    jetSource = cms.InputTag("iterativeCone5PFJets"),
    saveRejected = cms.string(''),
    markItems = cms.bool(True),
    selection = cms.PSet(
        type = cms.string('none')
    ),
    bitsToIgnore = cms.vstring('Overlap/All'),
    removeOverlaps = cms.PSet(
        electrons = cms.PSet(
            deltaR = cms.double(0.3),
            cut = cms.string('pt > 10'),
            flags = cms.vstring('Isolation/Tracker'),
            collection = cms.InputTag("allLayer0Electrons")
        ),
        user = cms.VPSet()
    )
)


process.electronTrigMatchHLT1Electron = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Electrons"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLT1Electron")
)


process.jetPartonMatch = cms.EDFilter("MCMatcher",
    src = cms.InputTag("allLayer0Jets"),
    maxDPtRel = cms.double(3.0),
    mcPdgId = cms.vint32(1, 2, 3, 4, 5, 
        6, 21),
    mcStatus = cms.vint32(3),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.8),
    checkCharge = cms.bool(False),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("genParticles")
)


process.allLayer0Muons = cms.EDFilter("PATMuonCleaner",
    saveAll = cms.string(''),
    muonSource = cms.InputTag("muons"),
    saveRejected = cms.string(''),
    bitsToIgnore = cms.vstring('Isolation/All'),
    markItems = cms.bool(True),
    selection = cms.PSet(
        type = cms.string('none')
    ),
    isolation = cms.PSet(
        hcal = cms.PSet(
            src = cms.InputTag("patAODMuonIsolations","muIsoDepositCalByAssociatorTowershcal"),
            deltaR = cms.double(0.3),
            cut = cms.double(2.0)
        ),
        tracker = cms.PSet(
            src = cms.InputTag("patAODMuonIsolations","muIsoDepositTk"),
            deltaR = cms.double(0.3),
            cut = cms.double(2.0)
        ),
        user = cms.VPSet(cms.PSet(
            src = cms.InputTag("patAODMuonIsolations","muIsoDepositCalByAssociatorTowersho"),
            deltaR = cms.double(0.3),
            cut = cms.double(2.0)
        ), 
            cms.PSet(
                src = cms.InputTag("patAODMuonIsolations","muIsoDepositJets"),
                deltaR = cms.double(0.5),
                cut = cms.double(2.0)
            )),
        ecal = cms.PSet(
            src = cms.InputTag("patAODMuonIsolations","muIsoDepositCalByAssociatorTowersecal"),
            deltaR = cms.double(0.3),
            cut = cms.double(2.0)
        )
    )
)


process.layer0PhotonIsolations = cms.EDFilter("CandManyValueMapsSkimmerIsoDeposits",
    associations = cms.VInputTag(cms.InputTag("gamIsoDepositTk"), cms.InputTag("gamIsoDepositEcalFromClusts"), cms.InputTag("gamIsoDepositHcalFromTowers")),
    commonLabel = cms.InputTag("patAODPhotonIsolations"),
    collection = cms.InputTag("allLayer0Photons"),
    backrefs = cms.InputTag("allLayer0Photons")
)


process.pfRecoTauDiscriminationByECALIsolationHighEfficiency = cms.EDFilter("PFRecoTauDiscriminationByIsolation",
    ApplyDiscriminationByECALIsolation = cms.bool(True),
    PFTauProducer = cms.InputTag("pfRecoTauProducerHighEfficiency"),
    ManipulateTracks_insteadofChargedHadrCands = cms.bool(False),
    TrackerIsolAnnulus_Tracksmaxn = cms.int32(0),
    ApplyDiscriminationByTrackerIsolation = cms.bool(False),
    TrackerIsolAnnulus_Candsmaxn = cms.int32(0),
    ECALIsolAnnulus_Candsmaxn = cms.int32(0)
)


process.jetFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("selectedLayer1Jets"),
    minNumber = cms.uint32(1)
)


process.muonTrigMatchHLTDoubleMu3 = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Muons"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLTDoubleMu3")
)


process.photonMatch = cms.EDFilter("MCMatcher",
    src = cms.InputTag("allLayer0Photons"),
    maxDPtRel = cms.double(1.0),
    mcPdgId = cms.vint32(22),
    mcStatus = cms.vint32(1),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    checkCharge = cms.bool(True),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("genParticles")
)


process.layer0JetCorrFactors = cms.EDFilter("JetCorrFactorsValueMapSkimmer",
    collection = cms.InputTag("allLayer0Jets"),
    association = cms.InputTag("jetCorrFactors"),
    backrefs = cms.InputTag("allLayer0Jets")
)


process.jetGenJetMatch = cms.EDFilter("GenJetMatcher",
    src = cms.InputTag("allLayer0Jets"),
    maxDPtRel = cms.double(3.0),
    mcPdgId = cms.vint32(),
    mcStatus = cms.vint32(),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.4),
    checkCharge = cms.bool(False),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("iterativeCone5GenJets")
)


process.tauTrigMatchHLT2TauPixel = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Taus"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLT2TauPixel")
)


process.caloRecoTauDiscriminationByLeadingTrackPtCut = cms.EDFilter("CaloRecoTauDiscriminationByLeadingTrackPtCut",
    MinPtLeadingTrack = cms.double(5.0),
    CaloTauProducer = cms.InputTag("caloRecoTauProducer")
)


process.tauGenJetMatch = cms.EDFilter("GenJetMatcher",
    src = cms.InputTag("allLayer0Taus"),
    maxDPtRel = cms.double(3.0),
    mcPdgId = cms.vint32(),
    mcStatus = cms.vint32(),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.1),
    checkCharge = cms.bool(False),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("tauGenJets")
)


process.maxLayer1Taus = cms.EDFilter("PATTauMaxFilter",
    maxNumber = cms.uint32(999999),
    src = cms.InputTag("selectedLayer1Taus")
)


process.patAODTagInfos = cms.EDFilter("MultipleTagInfosToValueMaps",
    associations = cms.VInputTag("impactParameterTagInfosAOD", "secondaryVertexTagInfosAOD", "softElectronTagInfosAOD", "softMuonTagInfosAOD", cms.InputTag("CATopJetTagger")),
    collection = cms.InputTag("caTopJetsProducer"),
    failSilently = cms.untracked.bool(True)
)


process.patCaloRecoTauDiscriminationByIsolation = cms.EDFilter("CaloRecoTauDiscriminationByIsolation",
    TrackerIsolAnnulus_Tracksmaxn = cms.int32(0),
    CaloTauProducer = cms.string('allLayer0CaloTaus'),
    ApplyDiscriminationByTrackerIsolation = cms.bool(True)
)


process.photonTrigMatchHLT1Photon = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Photons"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLT1Photon")
)


process.patAODPhotonIsolations = cms.EDFilter("MultipleIsoDepositsToValueMaps",
    associations = cms.VInputTag(cms.InputTag("gamIsoDepositTk"), cms.InputTag("gamIsoDepositEcalFromClusts"), cms.InputTag("gamIsoDepositHcalFromTowers")),
    collection = cms.InputTag("photons")
)


process.softMuonTagInfosAOD = cms.EDFilter("SoftLepton",
    refineJetAxis = cms.uint32(0),
    primaryVertex = cms.InputTag("offlinePrimaryVertices"),
    leptons = cms.InputTag("globalMuons"),
    leptonQualityCut = cms.double(0.5),
    jets = cms.InputTag("caTopJetsProducer"),
    leptonDeltaRCut = cms.double(0.4),
    leptonChi2Cut = cms.double(9999.0)
)


process.patElectronIds = cms.EDFilter("CandManyValueMapsSkimmerFloat",
    associations = cms.VInputTag(cms.InputTag("eidRobustLoose"), cms.InputTag("eidRobustTight"), cms.InputTag("eidLoose"), cms.InputTag("eidTight"), cms.InputTag("eidRobustHighEnergy")),
    collection = cms.InputTag("allLayer0Electrons"),
    failSilently = cms.untracked.bool(False),
    backrefs = cms.InputTag("allLayer0Electrons")
)


process.patPFRecoTauDiscriminationByLeadingTrackPtCut = cms.EDFilter("PFRecoTauDiscriminationByLeadingTrackPtCut",
    MinPtLeadingTrack = cms.double(5.0),
    PFTauProducer = cms.InputTag("allLayer0Taus")
)


process.ic5PFJetTracksAssociatorAtVertex = cms.EDFilter("JetTracksAssociatorAtVertex",
    tracks = cms.InputTag("generalTracks"),
    coneSize = cms.double(0.5),
    jets = cms.InputTag("iterativeCone5PFJets")
)


process.caloRecoTauDiscriminationByLeadingTrackFinding = cms.EDFilter("CaloRecoTauDiscriminationByLeadingTrackFinding",
    CaloTauProducer = cms.InputTag("caloRecoTauProducer")
)


process.pfRecoTauDiscriminationByTrackIsolationUsingLeadingPionHighEfficiency = cms.EDFilter("PFRecoTauDiscriminationByIsolationUsingLeadingPion",
    ApplyDiscriminationByECALIsolation = cms.bool(False),
    PFTauProducer = cms.InputTag("pfRecoTauProducerHighEfficiency"),
    ManipulateTracks_insteadofChargedHadrCands = cms.bool(False),
    TrackerIsolAnnulus_Tracksmaxn = cms.int32(0),
    ApplyDiscriminationByTrackerIsolation = cms.bool(True),
    TrackerIsolAnnulus_Candsmaxn = cms.int32(0),
    ECALIsolAnnulus_Candsmaxn = cms.int32(0)
)


process.patAODJetTracksAssociator = cms.EDFilter("JetTracksAssociationValueMap",
    src = cms.InputTag("caTopJetsProducer"),
    tracks = cms.InputTag("jetTracksAssociatorAtVertexAOD"),
    cut = cms.string('')
)


process.metTrigMatchHLT1MET65 = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0METs"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLT1MET65")
)


process.patAODPhotonID = cms.EDFilter("PhotonIDConverter",
    photonID = cms.InputTag("PhotonIDProd","PhotonAssociatedID"),
    src = cms.InputTag("photons")
)


process.minLayer1Electrons = cms.EDFilter("PATElectronMinFilter",
    src = cms.InputTag("selectedLayer1Electrons"),
    minNumber = cms.uint32(0)
)


process.patAODMuonIsolations = cms.EDFilter("MultipleIsoDepositsToValueMaps",
    associations = cms.VInputTag(cms.InputTag("muIsoDepositCalByAssociatorTowers","ecal"), cms.InputTag("muIsoDepositCalByAssociatorTowers","hcal"), cms.InputTag("muIsoDepositCalByAssociatorTowers","ho"), cms.InputTag("muIsoDepositTk"), cms.InputTag("muIsoDepositJets")),
    collection = cms.InputTag("muons")
)


process.muonMatch = cms.EDFilter("MCMatcher",
    src = cms.InputTag("allLayer0Muons"),
    maxDPtRel = cms.double(0.5),
    mcPdgId = cms.vint32(13),
    mcStatus = cms.vint32(1),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.5),
    checkCharge = cms.bool(True),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("genParticles")
)


process.layer0ElectronIsolations = cms.EDFilter("CandManyValueMapsSkimmerIsoDeposits",
    associations = cms.VInputTag(cms.InputTag("eleIsoDepositTk"), cms.InputTag("eleIsoDepositEcalFromClusts"), cms.InputTag("eleIsoDepositHcalFromTowers")),
    commonLabel = cms.InputTag("patAODElectronIsolations"),
    collection = cms.InputTag("allLayer0Electrons"),
    backrefs = cms.InputTag("allLayer0Electrons")
)


process.corMetType1Mcone7 = cms.EDFilter("Type1MET",
    inputUncorJetsLabel = cms.string('midPointCone7CaloJets'),
    jetEMfracLimit = cms.double(0.9),
    metType = cms.string('CaloMET'),
    jetPTthreshold = cms.double(20.0),
    inputUncorMetLabel = cms.string('met'),
    corrector = cms.string('MCJetCorrectorMcone7')
)


process.hbhereco = cms.EDFilter("HcalSimpleReconstructor",
    correctionPhaseNS = cms.double(13.0),
    digiLabel = cms.InputTag("hcalDigis"),
    samplesToAdd = cms.int32(4),
    Subdetector = cms.string('HBHE'),
    correctForTimeslew = cms.bool(True),
    correctForPhaseContainment = cms.bool(True),
    firstSample = cms.int32(4)
)


process.corMetType1Mcone5 = cms.EDFilter("Type1MET",
    inputUncorJetsLabel = cms.string('midPointCone5CaloJets'),
    jetEMfracLimit = cms.double(0.9),
    metType = cms.string('CaloMET'),
    jetPTthreshold = cms.double(20.0),
    inputUncorMetLabel = cms.string('met'),
    corrector = cms.string('MCJetCorrectorMcone5')
)


process.muonTrigMatchHLT1MET65 = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Muons"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLT1MET65")
)


process.allLayer0Electrons = cms.EDFilter("PATElectronCleaner",
    saveAll = cms.string(''),
    saveRejected = cms.string(''),
    bitsToIgnore = cms.vstring('Isolation/All'),
    electronSource = cms.InputTag("pixelMatchGsfElectrons"),
    markItems = cms.bool(True),
    selection = cms.PSet(
        type = cms.string('none')
    ),
    isolation = cms.PSet(
        hcal = cms.PSet(
            src = cms.InputTag("patAODElectronIsolations","eleIsoDepositHcalFromTowers"),
            deltaR = cms.double(0.4),
            skipDefaultVeto = cms.bool(True),
            cut = cms.double(5.0),
            vetos = cms.vstring('0.0')
        ),
        tracker = cms.PSet(
            src = cms.InputTag("patAODElectronIsolations","eleIsoDepositTk"),
            deltaR = cms.double(0.3),
            skipDefaultVeto = cms.bool(True),
            cut = cms.double(3.0),
            vetos = cms.vstring('0.015', 
                'Threshold(1.0)')
        ),
        user = cms.VPSet(),
        ecal = cms.PSet(
            src = cms.InputTag("patAODElectronIsolations","eleIsoDepositEcalFromClusts"),
            deltaR = cms.double(0.4),
            skipDefaultVeto = cms.bool(True),
            cut = cms.double(5.0),
            vetos = cms.vstring('EcalBarrel:0.045', 
                'EcalBarrel:RectangularEtaPhiVeto(-0.01,0.01,-0.5,0.5)', 
                'EcalEndcaps:0.070', 
                'EcalEndcaps:RectangularEtaPhiVeto(-0.02,0.02,-0.5,0.5)')
        )
    ),
    removeDuplicates = cms.bool(True),
    removeOverlaps = cms.PSet(

    )
)


process.muonTrigMatchHLT1MuonNonIso = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Muons"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLT1MuonNonIso")
)


process.jetTracksAssociatorAtVertexAOD = cms.EDFilter("JetTracksAssociatorAtVertex",
    jets = cms.InputTag("caTopJetsProducer"),
    tracks = cms.InputTag("generalTracks"),
    coneSize = cms.double(0.5)
)


process.patCaloRecoTauDiscriminationByLeadingTrackPtCut = cms.EDFilter("CaloRecoTauDiscriminationByLeadingTrackPtCut",
    MinPtLeadingTrack = cms.double(5.0),
    CaloTauProducer = cms.InputTag("allLayer0CaloTaus")
)


process.goodGlobalMuonsForMET = cms.EDFilter("MuonSelector",
    src = cms.InputTag("globalMuonsForMET"),
    cut = cms.string('isGlobalMuon=1 & pt > 10.0 & abs(eta)<2.5 & innerTrack.numberOfValidHits>5 & combinedMuon.qoverpError< 0.5')
)


process.electronTrigMatchHLT1ElectronRelaxed = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Electrons"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLT1ElectronRelaxed")
)


process.maxLayer1Jets = cms.EDFilter("PATJetMaxFilter",
    maxNumber = cms.uint32(999999),
    src = cms.InputTag("selectedLayer1Jets")
)


process.pfRecoTauDiscriminationByLeadingTrackPtCutHighEfficiency = cms.EDFilter("PFRecoTauDiscriminationByLeadingTrackPtCut",
    MinPtLeadingTrack = cms.double(5.0),
    PFTauProducer = cms.InputTag("pfRecoTauProducerHighEfficiency")
)


process.selectedLayer1Photons = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag("allLayer1Photons"),
    cut = cms.string('pt > 0. & abs(eta) < 12.')
)


process.electronTrigMatchHLTEle15LWL1R = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Electrons"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLTEle15LWL1R")
)


process.electronMatch = cms.EDFilter("MCMatcher",
    src = cms.InputTag("allLayer0Electrons"),
    maxDPtRel = cms.double(0.5),
    mcPdgId = cms.vint32(11),
    mcStatus = cms.vint32(1),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.5),
    checkCharge = cms.bool(True),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("genParticles")
)


process.layer0BTags = cms.EDFilter("CandManyValueMapsSkimmerFloat",
    associations = cms.VInputTag("jetBProbabilityBJetTagsAOD", "jetProbabilityBJetTagsAOD", "trackCountingHighPurBJetTagsAOD", "trackCountingHighEffBJetTagsAOD", "impactParameterMVABJetTagsAOD", 
        "simpleSecondaryVertexBJetTagsAOD", "combinedSecondaryVertexBJetTagsAOD", "combinedSecondaryVertexMVABJetTagsAOD", "softElectronBJetTagsAOD", "softMuonBJetTagsAOD", 
        "softMuonNoIPBJetTagsAOD"),
    commonLabel = cms.InputTag("patAODBTags"),
    collection = cms.InputTag("allLayer0Jets"),
    failSilently = cms.untracked.bool(True),
    backrefs = cms.InputTag("allLayer0Jets")
)


process.allLayer0Taus = cms.EDFilter("PATPFTauCleaner",
    tauSource = cms.InputTag("pfRecoTauProducer"),
    saveAll = cms.string(''),
    saveRejected = cms.string(''),
    bitsToIgnore = cms.vstring(),
    markItems = cms.bool(True),
    tauDiscriminatorSource = cms.InputTag("pfRecoTauDiscriminationByIsolation"),
    removeOverlaps = cms.PSet(

    )
)


process.minLayer1Muons = cms.EDFilter("PATMuonMinFilter",
    src = cms.InputTag("selectedLayer1Muons"),
    minNumber = cms.uint32(0)
)


process.gamIsoFromDepsEcalFromHits = cms.EDFilter("CandIsolatorFromDeposits",
    deposits = cms.VPSet(cms.PSet(
        src = cms.InputTag("gamIsoDepositEcalFromHits"),
        deltaR = cms.double(0.4),
        weight = cms.string('1'),
        vetos = cms.vstring('EcalBarrel:0.045', 
            'EcalBarrel:RectangularEtaPhiVeto(-0.02,0.02,-0.5,0.5)', 
            'EcalBarrel:Threshold(0.080)', 
            'EcalEndcaps:0.070', 
            'EcalEndcaps:RectangularEtaPhiVeto(-0.02,0.02,-0.5,0.5)', 
            'EcalEndcaps:Threshold(0.30)'),
        skipDefaultVeto = cms.bool(True),
        mode = cms.string('sum')
    ))
)


process.globalMuonsForMET = cms.EDFilter("MuonSelector",
    src = cms.InputTag("muons"),
    cut = cms.string('isGlobalMuon = 1')
)


process.allLayer0METs = cms.EDFilter("PATCaloMETCleaner",
    markItems = cms.bool(True),
    saveRejected = cms.string(''),
    metSource = cms.InputTag("met"),
    saveAll = cms.string(''),
    bitsToIgnore = cms.vstring()
)


process.muonTrigMatchHLT2MuonNonIso = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Muons"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLT2MuonNonIso")
)


process.patPFRecoTauDiscriminationByTrackIsolation = cms.EDFilter("PFRecoTauDiscriminationByIsolation",
    ApplyDiscriminationByECALIsolation = cms.bool(False),
    PFTauProducer = cms.InputTag("allLayer0Taus"),
    ManipulateTracks_insteadofChargedHadrCands = cms.bool(False),
    TrackerIsolAnnulus_Tracksmaxn = cms.int32(0),
    ApplyDiscriminationByTrackerIsolation = cms.bool(True),
    TrackerIsolAnnulus_Candsmaxn = cms.int32(0),
    ECALIsolAnnulus_Candsmaxn = cms.int32(0)
)


process.minLayer1Taus = cms.EDFilter("PATTauMinFilter",
    src = cms.InputTag("selectedLayer1Taus"),
    minNumber = cms.uint32(0)
)


process.allLayer0Photons = cms.EDFilter("PATPhotonCleaner",
    saveAll = cms.string(''),
    saveRejected = cms.string(''),
    removeElectrons = cms.string('bySeed'),
    bitsToIgnore = cms.vstring('Isolation/All'),
    markItems = cms.bool(True),
    electrons = cms.InputTag("allLayer0Electrons"),
    isolation = cms.PSet(
        hcal = cms.PSet(
            src = cms.InputTag("patAODPhotonIsolations","gamIsoDepositHcalFromTowers"),
            deltaR = cms.double(0.4),
            skipDefaultVeto = cms.bool(True),
            cut = cms.double(5.0),
            vetos = cms.vstring('0.00')
        ),
        tracker = cms.PSet(
            src = cms.InputTag("patAODPhotonIsolations","gamIsoDepositTk"),
            deltaR = cms.double(0.3),
            skipDefaultVeto = cms.bool(True),
            cut = cms.double(3.0),
            vetos = cms.vstring('0.015', 
                'Threshold(1.0)')
        ),
        user = cms.VPSet(),
        ecal = cms.PSet(
            src = cms.InputTag("patAODPhotonIsolations","gamIsoDepositEcalFromClusts"),
            deltaR = cms.double(0.4),
            skipDefaultVeto = cms.bool(True),
            cut = cms.double(5.0),
            vetos = cms.vstring('EcalBarrel:0.045', 
                'EcalBarrel:RectangularEtaPhiVeto(-0.01,0.01,-0.5,0.5)', 
                'EcalEndcaps:0.070', 
                'EcalEndcaps:RectangularEtaPhiVeto(-0.02,0.02,-0.5,0.5)')
        )
    ),
    removeDuplicates = cms.string('bySeed'),
    photonSource = cms.InputTag("photons")
)


process.maxLayer1Electrons = cms.EDFilter("PATElectronMaxFilter",
    maxNumber = cms.uint32(999999),
    src = cms.InputTag("selectedLayer1Electrons")
)


process.softMuonTagInfos = cms.EDFilter("SoftLepton",
    refineJetAxis = cms.uint32(0),
    primaryVertex = cms.InputTag("offlinePrimaryVertices"),
    leptons = cms.InputTag("globalMuons"),
    leptonQualityCut = cms.double(0.5),
    jets = cms.InputTag("iterativeCone5CaloJets"),
    leptonDeltaRCut = cms.double(0.4),
    leptonChi2Cut = cms.double(9999.0)
)


process.selectedLayer1Taus = cms.EDFilter("PATTauSelector",
    src = cms.InputTag("allLayer1Taus"),
    cut = cms.string('pt > 0. & abs(eta) < 12.')
)


process.muonTrigMatchHLTIsoMu11 = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Muons"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLTIsoMu11")
)


process.gamIsoFromDepsTk = cms.EDFilter("CandIsolatorFromDeposits",
    deposits = cms.VPSet(cms.PSet(
        src = cms.InputTag("gamIsoDepositTk"),
        deltaR = cms.double(0.3),
        weight = cms.string('1'),
        vetos = cms.vstring('0.015', 
            'Threshold(1.0)'),
        skipDefaultVeto = cms.bool(True),
        mode = cms.string('sum')
    ))
)


process.caloRecoTauDiscriminationAgainstElectron = cms.EDFilter("CaloRecoTauDiscriminationAgainstElectron",
    ApplyCut_maxleadTrackHCAL3x3hottesthitDEta = cms.bool(False),
    CaloTauProducer = cms.string('caloRecoTauProducer'),
    leadTrack_HCAL3x3hitsEtSumOverPt_minvalue = cms.double(0.1),
    ApplyCut_leadTrackavoidsECALcrack = cms.bool(True),
    maxleadTrackHCAL3x3hottesthitDEta = cms.double(0.1)
)


process.selectedLayer1Electrons = cms.EDFilter("PATElectronSelector",
    src = cms.InputTag("allLayer1Electrons"),
    cut = cms.string('et > 50. & abs(eta) < 2.5 && caloIso < 3.0')
)


process.hfreco = cms.EDFilter("HcalSimpleReconstructor",
    correctionPhaseNS = cms.double(0.0),
    digiLabel = cms.InputTag("hcalDigis"),
    samplesToAdd = cms.int32(1),
    Subdetector = cms.string('HF'),
    correctForTimeslew = cms.bool(False),
    correctForPhaseContainment = cms.bool(False),
    firstSample = cms.int32(3)
)


process.pfRecoTauDiscriminationByTrackIsolationHighEfficiency = cms.EDFilter("PFRecoTauDiscriminationByIsolation",
    ApplyDiscriminationByECALIsolation = cms.bool(False),
    PFTauProducer = cms.InputTag("pfRecoTauProducerHighEfficiency"),
    ManipulateTracks_insteadofChargedHadrCands = cms.bool(False),
    TrackerIsolAnnulus_Tracksmaxn = cms.int32(0),
    ApplyDiscriminationByTrackerIsolation = cms.bool(True),
    TrackerIsolAnnulus_Candsmaxn = cms.int32(0),
    ECALIsolAnnulus_Candsmaxn = cms.int32(0)
)


process.jetTrigMatchHLT4jet = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Jets"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLT4jet")
)


process.softElectronTagInfos = cms.EDFilter("SoftLepton",
    refineJetAxis = cms.uint32(0),
    primaryVertex = cms.InputTag("offlinePrimaryVertices"),
    leptons = cms.InputTag("btagSoftElectrons"),
    leptonQualityCut = cms.double(0.0),
    jets = cms.InputTag("iterativeCone5CaloJets"),
    leptonDeltaRCut = cms.double(0.4),
    leptonChi2Cut = cms.double(9999.0)
)


process.eleIsoFromDepsHcalFromTowers = cms.EDFilter("CandIsolatorFromDeposits",
    deposits = cms.VPSet(cms.PSet(
        src = cms.InputTag("eleIsoDepositHcalFromTowers"),
        deltaR = cms.double(0.4),
        weight = cms.string('1'),
        vetos = cms.vstring('0.0'),
        skipDefaultVeto = cms.bool(True),
        mode = cms.string('sum')
    ))
)


process.pfRecoTauDiscriminationByECALIsolationUsingLeadingPionHighEfficiency = cms.EDFilter("PFRecoTauDiscriminationByIsolationUsingLeadingPion",
    ApplyDiscriminationByECALIsolation = cms.bool(True),
    PFTauProducer = cms.InputTag("pfRecoTauProducerHighEfficiency"),
    ManipulateTracks_insteadofChargedHadrCands = cms.bool(False),
    TrackerIsolAnnulus_Tracksmaxn = cms.int32(0),
    ApplyDiscriminationByTrackerIsolation = cms.bool(False),
    TrackerIsolAnnulus_Candsmaxn = cms.int32(0),
    ECALIsolAnnulus_Candsmaxn = cms.int32(0)
)


process.muonTrigMatchHLT1MuonIso = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Muons"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLT1MuonIso")
)


process.layer0MuonIsolations = cms.EDFilter("CandManyValueMapsSkimmerIsoDeposits",
    associations = cms.VInputTag(cms.InputTag("muIsoDepositCalByAssociatorTowers","ecal"), cms.InputTag("muIsoDepositCalByAssociatorTowers","hcal"), cms.InputTag("muIsoDepositCalByAssociatorTowers","ho"), cms.InputTag("muIsoDepositTk"), cms.InputTag("muIsoDepositJets")),
    commonLabel = cms.InputTag("patAODMuonIsolations"),
    collection = cms.InputTag("allLayer0Muons"),
    backrefs = cms.InputTag("allLayer0Muons")
)


process.gamIsoFromDepsEcalFromClusts = cms.EDFilter("CandIsolatorFromDeposits",
    deposits = cms.VPSet(cms.PSet(
        src = cms.InputTag("gamIsoDepositEcalFromClusts"),
        deltaR = cms.double(0.4),
        weight = cms.string('1'),
        vetos = cms.vstring('EcalBarrel:0.045', 
            'EcalBarrel:RectangularEtaPhiVeto(-0.01,0.01,-0.5,0.5)', 
            'EcalEndcaps:0.070', 
            'EcalEndcaps:RectangularEtaPhiVeto(-0.02,0.02,-0.5,0.5)'),
        skipDefaultVeto = cms.bool(True),
        mode = cms.string('sum')
    ))
)


process.electronTrigMatchHLT2Electron = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Electrons"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLT2Electron")
)


process.egammaSuperClusterMerger = cms.EDFilter("SuperClusterMerger",
    src = cms.VInputTag(cms.InputTag("hybridSuperClusters"), cms.InputTag("multi5x5SuperClusters","multi5x5EndcapSuperClusters"))
)


process.pfRecoTauDiscriminationByECALIsolation = cms.EDFilter("PFRecoTauDiscriminationByIsolation",
    ApplyDiscriminationByECALIsolation = cms.bool(True),
    PFTauProducer = cms.InputTag("pfRecoTauProducer"),
    ManipulateTracks_insteadofChargedHadrCands = cms.bool(False),
    TrackerIsolAnnulus_Tracksmaxn = cms.int32(0),
    ApplyDiscriminationByTrackerIsolation = cms.bool(False),
    TrackerIsolAnnulus_Candsmaxn = cms.int32(0),
    ECALIsolAnnulus_Candsmaxn = cms.int32(0)
)


process.selectedLayer1Jets = cms.EDFilter("PATJetSelector",
    src = cms.InputTag("allLayer1Jets"),
    cut = cms.string('et > 300. & abs(eta) < 5.0')
)


process.electronTrigMatchHLTIsoEle15LWL1I = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Electrons"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLTIsoEle15LWL1I")
)


process.caloRecoTauDiscriminationByIsolation = cms.EDFilter("CaloRecoTauDiscriminationByIsolation",
    TrackerIsolAnnulus_Tracksmaxn = cms.int32(0),
    CaloTauProducer = cms.string('caloRecoTauProducer'),
    ApplyDiscriminationByTrackerIsolation = cms.bool(True)
)


process.tauTrigMatchHLT1Tau = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Taus"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLT1Tau")
)


process.layer0JetCharge = cms.EDFilter("JetChargeValueMap",
    var = cms.string('Pt'),
    src = cms.InputTag("allLayer0Jets"),
    jetTracksAssociation = cms.InputTag("layer0JetTracksAssociator"),
    exp = cms.double(1.0)
)


process.pfRecoTauDiscriminationByLeadingPionPtCutHighEfficiency = cms.EDFilter("PFRecoTauDiscriminationByLeadingPionPtCut",
    MinPtLeadingPion = cms.double(5.0),
    PFTauProducer = cms.InputTag("pfRecoTauProducerHighEfficiency")
)


process.patCaloRecoTauDiscriminationByLeadingTrackFinding = cms.EDFilter("CaloRecoTauDiscriminationByLeadingTrackFinding",
    CaloTauProducer = cms.InputTag("allLayer0CaloTaus")
)


process.softElectronTagInfosAOD = cms.EDFilter("SoftLepton",
    refineJetAxis = cms.uint32(0),
    primaryVertex = cms.InputTag("offlinePrimaryVertices"),
    leptons = cms.InputTag("btagSoftElectrons"),
    leptonQualityCut = cms.double(0.0),
    jets = cms.InputTag("caTopJetsProducer"),
    leptonDeltaRCut = cms.double(0.4),
    leptonChi2Cut = cms.double(9999.0)
)


process.tauTrigMatchHLTLooseIsoTauMET30L1MET = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Taus"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLTLooseIsoTauMET30L1MET")
)


process.goodMuonsforMETCorrection = cms.EDFilter("MuonSelector",
    src = cms.InputTag("muons"),
    cut = cms.string('isGlobalMuon=1 & pt > 10.0 & abs(eta)<2.5 & innerTrack.numberOfValidHits>5 & combinedMuon.qoverpError< 0.5')
)


process.photonTrigMatchHLT2PhotonRelaxed = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Photons"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLT2PhotonRelaxed")
)


process.tauTrigMatchHLTDoubleIsoTauTrk3 = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Taus"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLTDoubleIsoTauTrk3")
)


process.tauMatch = cms.EDFilter("MCMatcher",
    src = cms.InputTag("allLayer0Taus"),
    maxDPtRel = cms.double(999.9),
    mcPdgId = cms.vint32(15),
    mcStatus = cms.vint32(2),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(999.9),
    checkCharge = cms.bool(True),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("genParticles")
)


process.egammaBasicClusterMerger = cms.EDFilter("BasicClusterMerger",
    src = cms.VInputTag(cms.InputTag("hybridSuperClusters","hybridBarrelBasicClusters"), cms.InputTag("multi5x5BasicClusters","multi5x5EndcapBasicClusters"))
)


process.layer0JetTracksAssociator = cms.EDFilter("CandValueMapSkimmerTrackRefs",
    collection = cms.InputTag("allLayer0Jets"),
    association = cms.InputTag("patAODJetTracksAssociator"),
    backrefs = cms.InputTag("allLayer0Jets")
)


process.layer0TagInfos = cms.EDFilter("CandManyValueMapsSkimmerTagInfo",
    associations = cms.VInputTag("impactParameterTagInfosAOD", "secondaryVertexTagInfosAOD", "softElectronTagInfosAOD", "softMuonTagInfosAOD", cms.InputTag("CATopJetTagger")),
    commonLabel = cms.InputTag("patAODTagInfos"),
    collection = cms.InputTag("allLayer0Jets"),
    failSilently = cms.untracked.bool(True),
    backrefs = cms.InputTag("allLayer0Jets")
)


process.minLayer1Jets = cms.EDFilter("PATJetMinFilter",
    src = cms.InputTag("selectedLayer1Jets"),
    minNumber = cms.uint32(0)
)


process.jetPartonAssociation = cms.EDFilter("JetPartonMatcher",
    jets = cms.InputTag("allLayer0Jets"),
    coneSizeToAssociate = cms.double(0.8),
    partons = cms.InputTag("jetPartons"),
    doPriority = cms.bool(True),
    priorityList = cms.vint32(6)
)


process.jetFlavourAssociation = cms.EDFilter("JetFlavourIdentifier",
    srcByReference = cms.InputTag("jetPartonAssociation"),
    physicsDefinition = cms.bool(False),
    definition = cms.int32(4)
)


process.maxLayer1Photons = cms.EDFilter("PATPhotonMaxFilter",
    maxNumber = cms.uint32(999999),
    src = cms.InputTag("selectedLayer1Photons")
)


process.minLayer1Photons = cms.EDFilter("PATPhotonMinFilter",
    src = cms.InputTag("selectedLayer1Photons"),
    minNumber = cms.uint32(0)
)


process.photonTrigMatchHLT1PhotonRelaxed = cms.EDFilter("PATTrigMatcher",
    src = cms.InputTag("allLayer0Photons"),
    maxDPtRel = cms.double(1.0),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.2),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patHLT1PhotonRelaxed")
)


process.printList = cms.EDAnalyzer("ParticleListDrawer",
    src = cms.InputTag("genParticles"),
    maxEventsToPrint = cms.untracked.int32(0)
)


process.out = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('p')
    ),
    outputCommands = cms.untracked.vstring('drop *', 
        'keep recoGenParticles_genParticles_*_*', 
        'keep *_genEventScale_*_*', 
        'keep *_genEventWeight_*_*', 
        'keep *_genEventPdfInfo_*_*', 
        'keep edmTriggerResults_TriggerResults_*_HLT', 
        'keep *_hltTriggerSummaryAOD_*_*', 
        'keep *_offlineBeamSpot_*_*', 
        'keep *_offlinePrimaryVertices_*_*', 
        'keep recoTracks_generalTracks_*_*', 
        'keep *_towerMaker_*_*', 
        'keep *_selectedLayer1Photons_*_*', 
        'keep *_selectedLayer1Electrons_*_*', 
        'keep *_selectedLayer1Muons_*_*', 
        'keep *_selectedLayer1Taus_*_*', 
        'keep *_selectedLayer1Jets_*_*', 
        'keep *_selectedLayer1METs_*_*', 
        'keep patPFParticles_*_*_*', 
        'keep *_selectedLayer1Hemispheres_*_*', 
        'drop *_genParticles_*_*', 
        'keep *_genEventScale_*_*', 
        'drop *_generalTracks_*_*', 
        'keep *_goodTracks_*_*', 
        'drop *_towerMaker_*_*', 
        'drop *_selectedLayer1Taus_*_*', 
        'drop *_selectedLayer1Hemispheres_*_*', 
        'drop *_selectedLayer1Photons_*_*'),
    dropMetaDataForDroppedData = cms.untracked.bool(True),
    verbose = cms.untracked.bool(False),
    fileName = cms.untracked.string('./ca_pat_slim_fastsim_220.root')
)


process.patTrigMatchHLT2ElectronRelaxed = cms.Sequence(process.patHLT2ElectronRelaxed*process.electronTrigMatchHLT2ElectronRelaxed)


process.patLayer0Cleaners = cms.Sequence(process.allLayer0Muons*process.allLayer0Electrons*process.allLayer0Photons*process.allLayer0Taus*process.allLayer0Jets*process.allLayer0METs)


process.patTrigMatchHLT2Electron = cms.Sequence(process.patHLT2Electron*process.electronTrigMatchHLT2Electron)


process.hcalLocalRecoSequence = cms.Sequence(process.hbhereco+process.hfreco+process.horeco)


process.layer1METs = cms.Sequence(process.allLayer1METs*process.selectedLayer1METs)


process.patMCTruth_Jet = cms.Sequence(process.jetPartonMatch+process.jetGenJetMatch)


process.patTrigMatchHLT_Ele15_LW_L1R = cms.Sequence(process.patHLTEle15LWL1R*process.electronTrigMatchHLTEle15LWL1R)


process.patJetFlavourId = cms.Sequence(process.jetPartons*process.jetPartonAssociation*process.jetFlavourAssociation)


process.patTrigMatchHLT1Tau = cms.Sequence(process.patHLT1Tau*process.tauTrigMatchHLT1Tau)


process.btagging = cms.Sequence(process.impactParameterTagInfos*process.jetBProbabilityBJetTags+process.jetProbabilityBJetTags+process.trackCountingHighPurBJetTags+process.trackCountingHighEffBJetTags+process.impactParameterMVABJetTags*process.secondaryVertexTagInfos*process.simpleSecondaryVertexBJetTags+process.combinedSecondaryVertexBJetTags+process.combinedSecondaryVertexMVABJetTags+process.btagSoftElectrons*process.softElectronTagInfos*process.softElectronBJetTags+process.softMuonTagInfos*process.softMuonBJetTags+process.softMuonNoIPBJetTags)


process.patAODBTagging = cms.Sequence(process.patAODBTags*process.patAODTagInfos)


process.patMCTruth_Tau = cms.Sequence(process.tauMatch+process.tauGenJets*process.tauGenJetMatch)


process.patTrigMatchHLT_LooseIsoTau_MET30_L1MET = cms.Sequence(process.patHLTLooseIsoTauMET30L1MET*process.tauTrigMatchHLTLooseIsoTauMET30L1MET)


process.patAODMuonIsolation = cms.Sequence(process.patAODMuonIsolations)


process.patLayer0PhotonIsolation = cms.Sequence(process.layer0PhotonIsolations)


process.PFTauDiscriminationHighEfficiency = cms.Sequence(process.pfRecoTauDiscriminationByIsolationHighEfficiency*process.pfRecoTauDiscriminationByIsolationUsingLeadingPionHighEfficiency*process.pfRecoTauDiscriminationByLeadingTrackFindingHighEfficiency*process.pfRecoTauDiscriminationByLeadingTrackPtCutHighEfficiency*process.pfRecoTauDiscriminationByLeadingPionPtCutHighEfficiency*process.pfRecoTauDiscriminationByTrackIsolationHighEfficiency*process.pfRecoTauDiscriminationByTrackIsolationUsingLeadingPionHighEfficiency*process.pfRecoTauDiscriminationByECALIsolationHighEfficiency*process.pfRecoTauDiscriminationByECALIsolationUsingLeadingPionHighEfficiency*process.pfRecoTauDiscriminationAgainstElectronHighEfficiency*process.pfRecoTauDiscriminationAgainstMuonHighEfficiency)


process.patTrigMatchHLT1MuonNonIso = cms.Sequence(process.patHLT1MuonNonIso*process.muonTrigMatchHLT1MuonNonIso)


process.muIsoDeposits_ParamGlobalMuons = cms.Sequence(process.muParamGlobalIsoDepositTk+process.muParamGlobalIsoDepositCalByAssociatorTowers+process.muParamGlobalIsoDepositJets)


process.patTrigMatchHLT2TauPixel = cms.Sequence(process.patHLT2TauPixel*process.tauTrigMatchHLT2TauPixel)


process.patLayer0JetMETCorrections = cms.Sequence(process.layer0JetCorrFactors)


process.patElectronId = cms.Sequence(process.eidRobustHighEnergy*process.patElectronIds)


process.btaggingJetTagsAOD = cms.Sequence(process.jetBProbabilityBJetTagsAOD+process.jetProbabilityBJetTagsAOD+process.trackCountingHighPurBJetTagsAOD+process.trackCountingHighEffBJetTagsAOD+process.impactParameterMVABJetTagsAOD+process.simpleSecondaryVertexBJetTagsAOD+process.combinedSecondaryVertexBJetTagsAOD+process.combinedSecondaryVertexMVABJetTagsAOD+process.softElectronBJetTagsAOD+process.softMuonBJetTagsAOD+process.softMuonNoIPBJetTagsAOD)


process.eIdSequence = cms.Sequence(process.eidRobustLoose+process.eidRobustTight+process.eidLoose+process.eidTight)


process.patAODJetTracksCharge = cms.Sequence(process.patAODJetTracksAssociator*process.AODJetCharge)


process.muIsoDeposits_ParamGlobalMuonsOld = cms.Sequence(process.muParamGlobalIsoDepositGsTk+process.muParamGlobalIsoDepositCalEcal+process.muParamGlobalIsoDepositCalHcal)


process.patLayer0PhotonID = cms.Sequence(process.layer0PhotonID)


process.patTrigMatchHLT1MET65 = cms.Sequence(process.patHLT1MET65*process.metTrigMatchHLT1MET65+process.muonTrigMatchHLT1MET65)


process.patTrigMatchHLT_IsoMu11 = cms.Sequence(process.patHLTIsoMu11*process.muonTrigMatchHLTIsoMu11)


process.countLayer1Electrons = cms.Sequence(process.minLayer1Electrons+process.maxLayer1Electrons)


process.patTrigMatchHLT3jet = cms.Sequence(process.patHLT3jet*process.jetTrigMatchHLT3jet)


process.patCaloTauDiscrimination = cms.Sequence(process.patCaloRecoTauDiscriminationByIsolation+process.patCaloRecoTauDiscriminationByLeadingTrackFinding+process.patCaloRecoTauDiscriminationByLeadingTrackPtCut)


process.patTrigMatchHLT1ElectronRelaxed = cms.Sequence(process.patHLT1ElectronRelaxed*process.electronTrigMatchHLT1ElectronRelaxed+process.jetTrigMatchHLT1ElectronRelaxed)


process.eleIsoDeposits = cms.Sequence(process.eleIsoDepositTk+process.eleIsoDepositEcalFromHits+process.eleIsoDepositHcalFromHits)


process.patTrigMatchHLT_DoubleMu3 = cms.Sequence(process.patHLTDoubleMu3*process.muonTrigMatchHLTDoubleMu3)


process.patTrigMatchHLT_Mu11 = cms.Sequence(process.patHLTMu11*process.muonTrigMatchHLTMu11)


process.patTrigMatchHLT1PhotonRelaxed = cms.Sequence(process.patHLT1PhotonRelaxed*process.photonTrigMatchHLT1PhotonRelaxed)


process.patTrigMatchCandHLT1ElectronStartup = cms.Sequence(process.patCandHLT1ElectronStartup*process.electronTrigMatchCandHLT1ElectronStartup)


process.patLayer0MuonIsolation = cms.Sequence(process.layer0MuonIsolations)


process.ecalLocalRecoSequence = cms.Sequence(process.ecalWeightUncalibRecHit*process.ecalRecHit+process.ecalPreshowerRecHit)


process.patMCTruth_withoutLeptonPhoton = cms.Sequence(process.patMCTruth_Jet+process.patMCTruth_Tau)


process.btaggingTagInfosAOD = cms.Sequence(process.impactParameterTagInfosAOD+process.secondaryVertexTagInfosAOD+process.softElectronTagInfosAOD+process.softMuonTagInfosAOD)


process.PFTauDiscrimination = cms.Sequence(process.pfRecoTauDiscriminationByIsolation*process.pfRecoTauDiscriminationByIsolationUsingLeadingPion*process.pfRecoTauDiscriminationByLeadingTrackFinding*process.pfRecoTauDiscriminationByLeadingTrackPtCut*process.pfRecoTauDiscriminationByLeadingPionPtCut*process.pfRecoTauDiscriminationByTrackIsolation*process.pfRecoTauDiscriminationByTrackIsolationUsingLeadingPion*process.pfRecoTauDiscriminationByECALIsolation*process.pfRecoTauDiscriminationByECALIsolationUsingLeadingPion*process.pfRecoTauDiscriminationAgainstElectron*process.pfRecoTauDiscriminationAgainstMuon)


process.muIsolation_ParamGlobalMuonsOld = cms.Sequence(process.muIsoDeposits_ParamGlobalMuonsOld)


process.patTrigMatchHLT_DoubleEle5_SW_L1R = cms.Sequence(process.patHLTDoubleEle5SWL1R*process.electronTrigMatchHLTDoubleEle5SWL1R)


process.countLayer1Photons = cms.Sequence(process.minLayer1Photons+process.maxLayer1Photons)


process.patTrigMatchHLT1MuonIso = cms.Sequence(process.patHLT1MuonIso*process.muonTrigMatchHLT1MuonIso)


process.patTrigMatchHLT2Photon = cms.Sequence(process.patHLT2Photon*process.photonTrigMatchHLT2Photon)


process.patTrigMatchHLT1Electron = cms.Sequence(process.patHLT1Electron*process.electronTrigMatchHLT1Electron)


process.patTrigMatchHLT_DoubleIsoMu3 = cms.Sequence(process.patHLTDoubleIsoMu3*process.muonTrigMatchHLTDoubleIsoMu3)


process.patMCTruth_LeptonPhoton = cms.Sequence(process.electronMatch+process.muonMatch+process.photonMatch)


process.eleIsoDepositAOD = cms.Sequence(process.eleIsoDepositTk*process.eleIsoDepositEcalFromClusts*process.eleIsoDepositHcalFromTowers)


process.patLayer0ElectronIsolation = cms.Sequence(process.layer0ElectronIsolations)


process.patLayer0BTagging = cms.Sequence(process.layer0BTags*process.layer0TagInfos)


process.patTrigMatchHLT2jet = cms.Sequence(process.patHLT2jet*process.jetTrigMatchHLT2jet)


process.tautagging = cms.Sequence(process.caloRecoTauTagInfoProducer*process.caloRecoTauProducer*process.caloRecoTauDiscriminationByLeadingTrackFinding*process.caloRecoTauDiscriminationByLeadingTrackPtCut*process.caloRecoTauDiscriminationByIsolation*process.caloRecoTauDiscriminationAgainstElectron)


process.patLayer0JetTracksCharge = cms.Sequence(process.patAODJetTracksAssociator*process.layer0JetTracksAssociator*process.layer0JetCharge)


process.muIsoDeposits_muons = cms.Sequence(process.muIsoDepositTk+process.muIsoDepositCalByAssociatorTowers+process.muIsoDepositJets)


process.layer1Hemispheres = cms.Sequence(process.selectedLayer1Hemispheres)


process.patTrigMatchHLT_IsoEle15_LW_L1I = cms.Sequence(process.patHLTIsoEle15LWL1I*process.electronTrigMatchHLTIsoEle15LWL1I)


process.patAODJetMETCorrections = cms.Sequence(process.jetCorrFactors+process.globalMuonsForMET*process.goodGlobalMuonsForMET*process.corMetType1Icone5*process.corMetType1Icone5Muons)


process.patPFTauDiscrimination = cms.Sequence(process.patPFRecoTauDiscriminationByIsolation+process.patPFRecoTauDiscriminationByLeadingTrackFinding+process.patPFRecoTauDiscriminationByLeadingTrackPtCut+process.patPFRecoTauDiscriminationByTrackIsolation+process.patPFRecoTauDiscriminationByECALIsolation+process.patPFRecoTauDiscriminationAgainstElectron+process.patPFRecoTauDiscriminationAgainstMuon)


process.patAODTauDiscrimination = cms.Sequence(process.caloRecoTauDiscriminationByIsolation*process.pfRecoTauDiscriminationByIsolation)


process.patTrigMatchHLT_DoubleIsoEle10_LW_L1I = cms.Sequence(process.patHLTDoubleIsoEle10LWL1I*process.electronTrigMatchHLTDoubleIsoEle10LWL1I)


process.countLayer1Muons = cms.Sequence(process.minLayer1Muons+process.maxLayer1Muons)


process.patTrigMatchHLT2PhotonRelaxed = cms.Sequence(process.patHLT2PhotonRelaxed*process.photonTrigMatchHLT2PhotonRelaxed)


process.patTrigMatchHLT2MuonNonIso = cms.Sequence(process.patHLT2MuonNonIso*process.muonTrigMatchHLT2MuonNonIso)


process.genJetParticles = cms.Sequence(process.genParticlesForJets)


process.PFTauHighEfficiency = cms.Sequence(process.pfRecoTauProducerHighEfficiency*process.PFTauDiscriminationHighEfficiency)


process.MetType1Corrections = cms.Sequence(process.corMetType1Icone5*process.corMetType1Mcone5*process.corMetType1Mcone7)


process.patMCTruth_withoutTau = cms.Sequence(process.patMCTruth_LeptonPhoton+process.patMCTruth_Jet)


process.patLayer0Cleaners_withoutPFTau = cms.Sequence(process.allLayer0Muons*process.allLayer0Electrons*process.allLayer0Photons*process.allLayer0Jets*process.allLayer0METs)


process.countLayer1Jets = cms.Sequence(process.minLayer1Jets+process.maxLayer1Jets)


process.countLayer1Taus = cms.Sequence(process.minLayer1Taus+process.maxLayer1Taus)


process.patTrigMatchHLT4jet = cms.Sequence(process.patHLT4jet*process.jetTrigMatchHLT4jet)


process.patTrigMatchHLT_DoubleIsoTau_Trk3 = cms.Sequence(process.patHLTDoubleIsoTauTrk3*process.tauTrigMatchHLTDoubleIsoTauTrk3)


process.gamIsoDepositAOD = cms.Sequence(process.gamIsoDepositTk*process.gamIsoDepositEcalFromClusts*process.gamIsoDepositHcalFromTowers)


process.gamIsoDeposits = cms.Sequence(process.gamIsoDepositTk+process.gamIsoDepositEcalFromHits+process.gamIsoDepositHcalFromHits)


process.patTrigMatchHLT1Photon = cms.Sequence(process.patHLT1Photon*process.photonTrigMatchHLT1Photon)


process.layer1Photons = cms.Sequence(process.allLayer1Photons*process.selectedLayer1Photons*process.countLayer1Photons)


process.ecalLocalRecoSequence_nopreshower = cms.Sequence(process.ecalWeightUncalibRecHit*process.ecalRecHit)


process.btaggingAOD = cms.Sequence(process.jetTracksAssociatorAtVertexAOD+process.btaggingTagInfosAOD+process.btaggingJetTagsAOD)


process.patHighLevelReco_withoutPFTau = cms.Sequence(process.patElectronId*process.patJetFlavourId*process.patLayer0ElectronIsolation*process.patLayer0PhotonIsolation*process.patLayer0PhotonID*process.patLayer0MuonIsolation*process.patLayer0BTagging*process.patLayer0JetMETCorrections*process.patLayer0JetTracksCharge)


process.patAODElectronIsolation = cms.Sequence(process.egammaSuperClusterMerger*process.egammaBasicClusterMerger*process.eleIsoDepositAOD*process.patAODElectronIsolations)


process.layer1Muons = cms.Sequence(process.allLayer1Muons*process.selectedLayer1Muons*process.countLayer1Muons)


process.muIsolation_ParamGlobalMuons = cms.Sequence(process.muIsoDeposits_ParamGlobalMuons)


process.layer1Electrons = cms.Sequence(process.allLayer1Electrons*process.selectedLayer1Electrons*process.countLayer1Electrons)


process.calolocalreco = cms.Sequence(process.ecalLocalRecoSequence+process.hcalLocalRecoSequence)


process.patTrigMatch_withoutBTau = cms.Sequence(process.patTrigMatchCandHLT1ElectronStartup+process.patTrigMatchHLT1PhotonRelaxed+process.patTrigMatchHLT1ElectronRelaxed+process.patTrigMatchHLT1MuonNonIso+process.patTrigMatchHLT2jet+process.patTrigMatchHLT1MET65)


process.patMCTruth = cms.Sequence(process.patMCTruth_LeptonPhoton+process.patMCTruth_Jet+process.patMCTruth_Tau)


process.patHighLevelReco = cms.Sequence(process.patHighLevelReco_withoutPFTau*process.patPFTauDiscrimination)


process.patTrigMatch_patTuple_withoutBTau = cms.Sequence(process.patTrigMatchHLT_IsoMu11+process.patTrigMatchHLT_Mu11+process.patTrigMatchHLT_DoubleIsoMu3+process.patTrigMatchHLT_DoubleMu3+process.patTrigMatchHLT_IsoEle15_LW_L1I+process.patTrigMatchHLT_Ele15_LW_L1R+process.patTrigMatchHLT_DoubleIsoEle10_LW_L1I+process.patTrigMatchHLT_DoubleEle5_SW_L1R)


process.layer1Jets = cms.Sequence(process.allLayer1Jets*process.selectedLayer1Jets*process.countLayer1Jets)


process.patAODPhotonIsolation = cms.Sequence(process.gamIsoDepositAOD*process.patAODPhotonIsolations)


process.layer1Taus = cms.Sequence(process.allLayer1Taus*process.selectedLayer1Taus*process.countLayer1Taus)


process.muIsolation_muons = cms.Sequence(process.muIsoDeposits_muons)


process.patBeforeLevel0Reco_withoutPFTau = cms.Sequence(process.patAODTauDiscrimination*process.patAODBTagging*process.patAODElectronIsolation*process.patAODPhotonIsolation*process.patAODPhotonID*process.patAODMuonIsolation*process.patAODJetMETCorrections)


process.PFTau = cms.Sequence(process.ic5PFJetTracksAssociatorAtVertex*process.pfRecoTauTagInfoProducer*process.pfRecoTauProducer*process.PFTauDiscrimination*process.PFTauHighEfficiency*process.PFTauDiscriminationHighEfficiency)


process.muIsolation = cms.Sequence(process.muIsolation_muons)


process.allObjects = cms.Sequence(process.layer1Muons*process.layer1Electrons*process.layer1Taus*process.countLayer1Leptons*process.layer1Photons*process.layer1Jets*process.layer1METs*process.layer1Hemispheres)


process.patTrigMatch_patTuple = cms.Sequence(process.patTrigMatch_patTuple_withoutBTau+process.patTrigMatchHLT_LooseIsoTau_MET30_L1MET+process.patTrigMatchHLT_DoubleIsoTau_Trk3)


process.patLayer0_withoutPFTau_withoutTrigMatch = cms.Sequence(process.patBeforeLevel0Reco_withoutPFTau*process.patLayer0Cleaners_withoutPFTau*process.patHighLevelReco_withoutPFTau*process.patMCTruth_withoutTau)


process.patBeforeLevel0Reco = cms.Sequence(process.patBeforeLevel0Reco_withoutPFTau)


process.patLayer0_patTuple_withoutPFTau = cms.Sequence(process.patLayer0_withoutPFTau_withoutTrigMatch*process.patTrigMatch_patTuple_withoutBTau)


process.patTrigMatch = cms.Sequence(process.patTrigMatch_withoutBTau+process.patTrigMatchHLT1Tau)


process.patLayer0_withoutTrigMatch = cms.Sequence((process.btaggingAOD+process.patBeforeLevel0Reco)*process.patLayer0Cleaners*process.patHighLevelReco*process.patMCTruth)


process.patMuonIsolation = cms.Sequence(process.muIsolation)


process.patLayer1 = cms.Sequence(process.allObjects)


process.patLayer0 = cms.Sequence(process.patLayer0_withoutTrigMatch*process.patTrigMatch)


process.patLayer0_patTuple = cms.Sequence(process.patLayer0_withoutTrigMatch*process.patTrigMatch_patTuple)


process.patLayer0_withoutPFTau = cms.Sequence(process.patLayer0_withoutPFTau_withoutTrigMatch*process.patTrigMatch_withoutBTau)


process.p = cms.Path(process.kt6CaloJets*process.printList*process.goodTracks*process.caTopJetsProducer*process.CATopJetTagger*process.patLayer0*process.patLayer1*process.jetFilter)


process.outpath = cms.EndPath(process.out)


process.MessageLogger = cms.Service("MessageLogger",
    suppressInfo = cms.untracked.vstring(),
    debugs = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    suppressDebug = cms.untracked.vstring(),
    cout = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    cerr_stats = cms.untracked.PSet(
        threshold = cms.untracked.string('WARNING'),
        output = cms.untracked.string('cerr')
    ),
    warnings = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    default = cms.untracked.PSet(

    ),
    statistics = cms.untracked.vstring('cerr_stats'),
    cerr = cms.untracked.PSet(
        INFO = cms.untracked.PSet(
            default = cms.untracked.PSet(
                limit = cms.untracked.int32(0)
            ),
            PATLayer0Summary = cms.untracked.PSet(
                limit = cms.untracked.int32(-1)
            )
        ),
        noTimeStamps = cms.untracked.bool(False),
        FwkReport = cms.untracked.PSet(
            reportEvery = cms.untracked.int32(1000),
            limit = cms.untracked.int32(10000000)
        ),
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000)
        ),
        Root_NoDictionary = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        FwkJob = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        FwkSummary = cms.untracked.PSet(
            reportEvery = cms.untracked.int32(1),
            limit = cms.untracked.int32(10000000)
        ),
        threshold = cms.untracked.string('INFO')
    ),
    FrameworkJobReport = cms.untracked.PSet(
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        FwkJob = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000)
        )
    ),
    suppressWarning = cms.untracked.vstring(),
    errors = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    destinations = cms.untracked.vstring('warnings', 
        'errors', 
        'infos', 
        'debugs', 
        'cout', 
        'cerr'),
    debugModules = cms.untracked.vstring(),
    infos = cms.untracked.PSet(
        Root_NoDictionary = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        placeholder = cms.untracked.bool(True)
    ),
    categories = cms.untracked.vstring('FwkJob', 
        'FwkReport', 
        'FwkSummary', 
        'Root_NoDictionary', 
        'PATLayer0Summary'),
    fwkJobReports = cms.untracked.vstring('FrameworkJobReport')
)


process.TFileService = cms.Service("TFileService",
    fileName = cms.string('histo__ca_2110.root')
)


process.CaloGeometryBuilder = cms.ESProducer("CaloGeometryBuilder",
    SelectedCalos = cms.vstring('HCAL', 
        'ZDC', 
        'EcalBarrel', 
        'EcalEndcap', 
        'EcalPreshower', 
        'TOWER')
)


process.softMuon = cms.ESProducer("MuonTaggerESProducer",
    ipSign = cms.string('any')
)


process.DTGeometryESModule = cms.ESProducer("DTGeometryESModule",
    appendToDataLabel = cms.string(''),
    applyAlignment = cms.bool(True),
    alignmentsLabel = cms.string('')
)


process.VolumeBasedMagneticFieldESProducer = cms.ESProducer("VolumeBasedMagneticFieldESProducer",
    timerOn = cms.untracked.bool(False),
    useParametrizedTrackerField = cms.bool(True),
    label = cms.untracked.string(''),
    version = cms.string('grid_1103l_071212_3_8t'),
    debugBuilder = cms.untracked.bool(False),
    cacheLastVolume = cms.untracked.bool(True)
)


process.siStripGainESProducerforSimulation = cms.ESProducer("SiStripGainESProducer",
    printDebug = cms.untracked.bool(False),
    appendToDataLabel = cms.string('fake'),
    APVGain = cms.string('fakeAPVGain'),
    AutomaticNormalization = cms.bool(False),
    NormalizationFactor = cms.double(1.0)
)


process.CaloTopologyBuilder = cms.ESProducer("CaloTopologyBuilder")


process.SiStripRecHitMatcherESProducer = cms.ESProducer("SiStripRecHitMatcherESProducer",
    ComponentName = cms.string('StandardMatcher'),
    NSigmaInside = cms.double(3.0)
)


process.l1GtStableParameters = cms.ESProducer("L1GtStableParametersTrivialProducer",
    NumberL1IsoEG = cms.uint32(4),
    NumberL1JetCounts = cms.uint32(12),
    UnitLength = cms.int32(8),
    NumberL1ForJet = cms.uint32(4),
    IfCaloEtaNumberBits = cms.uint32(4),
    IfMuEtaNumberBits = cms.uint32(6),
    NumberL1TauJet = cms.uint32(4),
    NumberPsbBoards = cms.int32(7),
    NumberConditionChips = cms.uint32(2),
    NumberL1Mu = cms.uint32(4),
    NumberL1CenJet = cms.uint32(4),
    NumberPhysTriggers = cms.uint32(128),
    PinsOnConditionChip = cms.uint32(96),
    NumberTechnicalTriggers = cms.uint32(64),
    OrderConditionChip = cms.vint32(2, 1),
    NumberPhysTriggersExtended = cms.uint32(64),
    WordLength = cms.int32(64),
    NumberL1NoIsoEG = cms.uint32(4)
)


process.RPCConeBuilder = cms.ESProducer("RPCConeBuilder",
    rollConnLP_17_4 = cms.vint32(0, 0, 0),
    rollConnT_14_4 = cms.vint32(-1, -1, -1),
    rollConnT_14_5 = cms.vint32(-1, -1, -1),
    rollConnT_14_0 = cms.vint32(13, 14, -1),
    rollConnT_14_1 = cms.vint32(13, -1, -1),
    rollConnT_14_2 = cms.vint32(14, 15, -1),
    rollConnT_14_3 = cms.vint32(15, 16, -1),
    rollConnT_12_4 = cms.vint32(-1, -1, -1),
    rollConnT_12_5 = cms.vint32(-1, -1, -1),
    rollConnT_12_2 = cms.vint32(12, 13, -1),
    rollConnT_12_3 = cms.vint32(13, 14, -1),
    rollConnT_12_0 = cms.vint32(10, 11, -1),
    rollConnT_12_1 = cms.vint32(11, -1, -1),
    rollConnLP_12_0 = cms.vint32(1, 1, 0),
    rollConnLP_0_3 = cms.vint32(0, 0, 0),
    rollConnT_0_4 = cms.vint32(-1, -1, -1),
    rollConnT_0_5 = cms.vint32(-1, -1, -1),
    rollConnLP_13_2 = cms.vint32(3, 3, 0),
    rollConnT_0_0 = cms.vint32(-1, -1, -1),
    rollConnLP_7_3 = cms.vint32(6, 6, 0),
    lpSizeTower14 = cms.vint32(72, 8, 40, 24, 0, 
        0),
    lpSizeTower15 = cms.vint32(72, 8, 40, 24, 0, 
        0),
    lpSizeTower16 = cms.vint32(72, 8, 40, 24, 0, 
        0),
    lpSizeTower10 = cms.vint32(72, 8, 40, 24, 0, 
        0),
    rollConnT_0_2 = cms.vint32(-1, -1, -1),
    lpSizeTower12 = cms.vint32(72, 8, 40, 24, 0, 
        0),
    lpSizeTower13 = cms.vint32(72, 8, 40, 24, 0, 
        0),
    rollConnLP_7_1 = cms.vint32(3, -3, 0),
    rollConnLP_8_1 = cms.vint32(0, 0, 0),
    rollConnLP_10_4 = cms.vint32(0, 0, 0),
    rollConnLP_8_0 = cms.vint32(0, 5, 0),
    rollConnLP_8_3 = cms.vint32(4, 0, 0),
    rollConnT_16_2 = cms.vint32(-1, -1, -1),
    rollConnT_16_3 = cms.vint32(-1, -1, -1),
    rollConnT_16_0 = cms.vint32(15, 16, -1),
    rollConnT_16_1 = cms.vint32(15, -1, -1),
    rollConnLP_3_0 = cms.vint32(0, 0, 0),
    rollConnT_16_4 = cms.vint32(-1, -1, -1),
    rollConnT_16_5 = cms.vint32(-1, -1, -1),
    rollConnT_15_5 = cms.vint32(-1, -1, -1),
    rollConnT_15_4 = cms.vint32(-1, -1, -1),
    rollConnLP_6_5 = cms.vint32(4, 0, 0),
    rollConnLP_6_4 = cms.vint32(0, 0, 0),
    rollConnLP_6_3 = cms.vint32(0, 0, 0),
    rollConnLP_6_2 = cms.vint32(0, 0, 0),
    rollConnT_8_2 = cms.vint32(9, -9, -1),
    rollConnLP_6_0 = cms.vint32(0, 0, 0),
    rollConnT_13_5 = cms.vint32(-1, -1, -1),
    rollConnT_13_4 = cms.vint32(-1, -1, -1),
    rollConnT_13_3 = cms.vint32(14, 15, -1),
    rollConnT_13_2 = cms.vint32(13, 14, -1),
    rollConnT_13_1 = cms.vint32(12, -1, -1),
    rollConnT_13_0 = cms.vint32(11, 12, -1),
    rollConnLP_4_1 = cms.vint32(3, 0, 0),
    rollConnLP_4_0 = cms.vint32(1, 1, -5),
    rollConnLP_4_3 = cms.vint32(6, 6, 0),
    rollConnLP_4_2 = cms.vint32(5, 5, 5),
    rollConnLP_4_5 = cms.vint32(4, 4, 0),
    rollConnLP_4_4 = cms.vint32(2, 2, 0),
    rollConnT_10_0 = cms.vint32(8, -1, -1),
    rollConnLP_12_4 = cms.vint32(0, 0, 0),
    rollConnT_4_0 = cms.vint32(4, 5, -6),
    rollConnT_4_1 = cms.vint32(4, -1, -1),
    rollConnT_4_2 = cms.vint32(2, 3, 4),
    rollConnT_4_3 = cms.vint32(2, 3, -1),
    rollConnT_4_4 = cms.vint32(4, 5, -1),
    rollConnT_4_5 = cms.vint32(3, 4, -1),
    rollConnLP_8_5 = cms.vint32(0, 0, 0),
    rollConnLP_8_4 = cms.vint32(0, 0, 0),
    rollConnT_6_4 = cms.vint32(-1, -1, -1),
    rollConnT_6_5 = cms.vint32(6, -1, -1),
    rollConnT_6_2 = cms.vint32(-1, -1, -1),
    rollConnT_6_3 = cms.vint32(-1, -1, -1),
    rollConnT_6_0 = cms.vint32(-1, -1, -1),
    rollConnLP_8_2 = cms.vint32(3, -5, 0),
    rollConnLP_5_0 = cms.vint32(1, 1, 1),
    rollConnLP_9_4 = cms.vint32(0, 0, 0),
    rollConnLP_5_1 = cms.vint32(3, -3, 3),
    rollConnLP_3_1 = cms.vint32(3, 0, 0),
    rollConnLP_16_0 = cms.vint32(1, 1, 0),
    rollConnLP_5_2 = cms.vint32(5, 5, 0),
    rollConnT_15_3 = cms.vint32(16, -1, -1),
    rollConnT_2_1 = cms.vint32(2, -1, -1),
    rollConnLP_2_3 = cms.vint32(6, 6, 0),
    rollConnLP_2_2 = cms.vint32(5, 5, 0),
    rollConnLP_2_1 = cms.vint32(3, 0, 0),
    rollConnLP_2_0 = cms.vint32(1, 1, 1),
    rollConnLP_2_5 = cms.vint32(4, 4, 0),
    rollConnLP_2_4 = cms.vint32(2, 2, 2),
    rollConnT_11_1 = cms.vint32(10, -1, -1),
    rollConnT_11_0 = cms.vint32(10, -1, -1),
    rollConnT_11_3 = cms.vint32(12, 13, -1),
    rollConnT_11_2 = cms.vint32(11, 12, -1),
    rollConnT_11_5 = cms.vint32(-1, -1, -1),
    rollConnT_11_4 = cms.vint32(-1, -1, -1),
    rollConnLP_0_5 = cms.vint32(0, 0, 0),
    rollConnLP_0_4 = cms.vint32(0, 0, 0),
    rollConnT_17_1 = cms.vint32(16, -1, -1),
    rollConnT_17_0 = cms.vint32(16, -1, -1),
    rollConnLP_0_1 = cms.vint32(3, 0, 0),
    lpSizeTower6 = cms.vint32(56, 72, 40, 8, 24, 
        0),
    rollConnT_17_5 = cms.vint32(-1, -1, -1),
    rollConnLP_0_2 = cms.vint32(0, 0, 0),
    rollConnT_8_4 = cms.vint32(-1, -1, -1),
    rollConnLP_14_5 = cms.vint32(0, 0, 0),
    rollConnLP_14_4 = cms.vint32(0, 0, 0),
    rollConnLP_14_3 = cms.vint32(4, 4, 0),
    rollConnLP_14_2 = cms.vint32(3, 3, 0),
    rollConnLP_14_1 = cms.vint32(2, 0, 0),
    rollConnLP_14_0 = cms.vint32(1, 1, 0),
    rollConnT_9_5 = cms.vint32(-1, -1, -1),
    rollConnT_9_4 = cms.vint32(-1, -1, -1),
    rollConnLP_7_4 = cms.vint32(2, 2, 0),
    rollConnLP_7_5 = cms.vint32(4, 0, 0),
    rollConnT_9_1 = cms.vint32(8, -1, -1),
    rollConnT_0_1 = cms.vint32(0, -1, -1),
    rollConnT_9_3 = cms.vint32(10, 11, -1),
    rollConnT_0_3 = cms.vint32(-1, -1, -1),
    rollConnT_7_1 = cms.vint32(7, -7, -1),
    rollConnLP_16_1 = cms.vint32(2, 0, 0),
    rollConnT_15_1 = cms.vint32(14, -1, -1),
    rollConnLP_16_3 = cms.vint32(0, 0, 0),
    rollConnLP_16_2 = cms.vint32(0, 0, 0),
    rollConnLP_16_5 = cms.vint32(0, 0, 0),
    rollConnLP_16_4 = cms.vint32(0, 0, 0),
    rollConnT_15_0 = cms.vint32(14, 15, -1),
    rollConnT_2_2 = cms.vint32(1, 2, -1),
    rollConnT_2_3 = cms.vint32(1, 2, -1),
    rollConnT_2_0 = cms.vint32(2, 3, 4),
    rollConnLP_5_3 = cms.vint32(6, 0, 0),
    rollConnLP_5_4 = cms.vint32(2, 2, 2),
    rollConnLP_5_5 = cms.vint32(4, 0, 0),
    rollConnT_2_4 = cms.vint32(2, 3, 4),
    rollConnT_2_5 = cms.vint32(2, 3, -1),
    rollConnT_8_3 = cms.vint32(10, -1, -1),
    rollConnT_5_1 = cms.vint32(5, -6, 6),
    rollConnT_5_0 = cms.vint32(6, 7, 8),
    rollConnT_5_3 = cms.vint32(4, -1, -1),
    rollConnT_5_2 = cms.vint32(4, 5, -1),
    rollConnT_5_5 = cms.vint32(5, -1, -1),
    rollConnT_5_4 = cms.vint32(5, 6, 7),
    rollConnLP_15_1 = cms.vint32(2, 0, 0),
    rollConnT_9_0 = cms.vint32(7, 8, -1),
    rollEnd = cms.int32(17),
    rollConnLP_17_1 = cms.vint32(2, 0, 0),
    rollConnLP_9_1 = cms.vint32(4, 0, 0),
    hwPlaneEnd = cms.int32(5),
    rollConnLP_10_3 = cms.vint32(4, 4, 0),
    rollConnLP_10_2 = cms.vint32(3, 3, 0),
    rollConnLP_10_1 = cms.vint32(2, 0, 0),
    rollConnLP_10_0 = cms.vint32(3, 0, 0),
    rollConnLP_10_5 = cms.vint32(0, 0, 0),
    towerBeg = cms.int32(0),
    rollConnLP_3_2 = cms.vint32(0, 0, 0),
    rollConnLP_3_3 = cms.vint32(0, 0, 0),
    rollConnT_15_2 = cms.vint32(15, 16, -1),
    rollConnT_8_5 = cms.vint32(-1, -1, -1),
    rollConnLP_6_1 = cms.vint32(0, 0, 0),
    rollConnLP_3_4 = cms.vint32(0, 0, 0),
    rollConnLP_3_5 = cms.vint32(0, 0, 0),
    rollConnLP_12_5 = cms.vint32(0, 0, 0),
    rollConnT_10_1 = cms.vint32(9, -1, -1),
    rollConnT_10_2 = cms.vint32(10, 11, -1),
    rollConnT_10_3 = cms.vint32(11, 12, -1),
    rollConnT_10_4 = cms.vint32(-1, -1, -1),
    rollConnT_10_5 = cms.vint32(-1, -1, -1),
    rollConnLP_12_3 = cms.vint32(4, 4, 0),
    rollConnLP_12_2 = cms.vint32(3, 3, 0),
    rollConnLP_1_4 = cms.vint32(2, 2, -2),
    rollConnLP_1_5 = cms.vint32(4, 4, 0),
    rollBeg = cms.int32(0),
    rollConnLP_1_0 = cms.vint32(1, 1, -1),
    rollConnLP_1_1 = cms.vint32(3, 0, 0),
    rollConnLP_1_2 = cms.vint32(5, 5, 0),
    rollConnLP_1_3 = cms.vint32(6, 6, 0),
    rollConnT_9_2 = cms.vint32(9, -9, 10),
    rollConnLP_9_5 = cms.vint32(0, 0, 0),
    rollConnT_7_5 = cms.vint32(7, -1, -1),
    rollConnT_7_4 = cms.vint32(7, 8, -1),
    rollConnLP_9_0 = cms.vint32(5, 3, 0),
    rollConnT_7_2 = cms.vint32(5, 6, -1),
    rollConnLP_9_2 = cms.vint32(3, -5, 3),
    rollConnT_7_0 = cms.vint32(8, 9, -1),
    rollConnLP_13_0 = cms.vint32(1, 1, 0),
    rollConnLP_12_1 = cms.vint32(2, 0, 0),
    lpSizeTower3 = cms.vint32(72, 56, 8, 40, 40, 
        24),
    rollConnT_1_5 = cms.vint32(0, 1, -1),
    rollConnT_1_4 = cms.vint32(0, 1, -2),
    rollConnLP_17_2 = cms.vint32(0, 0, 0),
    rollConnLP_17_3 = cms.vint32(0, 0, 0),
    rollConnLP_9_3 = cms.vint32(4, 4, 0),
    rollConnLP_17_5 = cms.vint32(0, 0, 0),
    rollConnT_1_3 = cms.vint32(0, 1, -1),
    rollConnT_1_2 = cms.vint32(0, 1, -1),
    rollConnT_1_1 = cms.vint32(1, -1, -1),
    lpSizeTower1 = cms.vint32(72, 56, 8, 40, 40, 
        24),
    rollConnT_7_3 = cms.vint32(4, 5, -1),
    rollConnT_17_3 = cms.vint32(-1, -1, -1),
    rollConnLP_13_5 = cms.vint32(0, 0, 0),
    rollConnLP_7_2 = cms.vint32(5, 5, 0),
    rollConnT_17_2 = cms.vint32(-1, -1, -1),
    rollConnT_3_3 = cms.vint32(-1, -1, -1),
    rollConnT_3_2 = cms.vint32(-1, -1, -1),
    rollConnT_3_1 = cms.vint32(3, -1, -1),
    rollConnT_3_0 = cms.vint32(-1, -1, -1),
    rollConnT_6_1 = cms.vint32(-1, -1, -1),
    rollConnT_3_5 = cms.vint32(-1, -1, -1),
    rollConnT_3_4 = cms.vint32(-1, -1, -1),
    rollConnT_1_0 = cms.vint32(0, 1, -2),
    rollConnLP_17_0 = cms.vint32(1, 0, 0),
    rollConnLP_0_0 = cms.vint32(0, 0, 0),
    rollConnT_8_0 = cms.vint32(-1, 7, -1),
    hwPlaneBeg = cms.int32(0),
    rollConnT_17_4 = cms.vint32(-1, -1, -1),
    rollConnLP_11_2 = cms.vint32(3, 3, 0),
    rollConnLP_11_3 = cms.vint32(4, 4, 0),
    rollConnLP_11_0 = cms.vint32(1, 0, 0),
    rollConnLP_11_1 = cms.vint32(2, 0, 0),
    rollConnLP_11_4 = cms.vint32(0, 0, 0),
    rollConnLP_11_5 = cms.vint32(0, 0, 0),
    rollConnT_8_1 = cms.vint32(-1, -1, -1),
    rollConnLP_7_0 = cms.vint32(1, 1, 0),
    lpSizeTower8 = cms.vint32(72, 24, 40, 8, 0, 
        0),
    lpSizeTower9 = cms.vint32(72, 8, 40, 0, 0, 
        0),
    rollConnLP_13_4 = cms.vint32(0, 0, 0),
    lpSizeTower7 = cms.vint32(72, 56, 40, 8, 24, 
        0),
    lpSizeTower4 = cms.vint32(72, 56, 8, 40, 40, 
        24),
    lpSizeTower5 = cms.vint32(72, 56, 40, 8, 40, 
        24),
    lpSizeTower2 = cms.vint32(72, 56, 8, 40, 40, 
        24),
    rollConnLP_13_1 = cms.vint32(2, 0, 0),
    lpSizeTower0 = cms.vint32(72, 56, 8, 40, 40, 
        24),
    rollConnLP_13_3 = cms.vint32(4, 4, 0),
    rollConnLP_15_0 = cms.vint32(1, 1, 0),
    rollConnLP_15_4 = cms.vint32(0, 0, 0),
    rollConnLP_15_5 = cms.vint32(0, 0, 0),
    rollConnLP_15_2 = cms.vint32(3, 3, 0),
    rollConnLP_15_3 = cms.vint32(4, 0, 0),
    towerEnd = cms.int32(16),
    lpSizeTower11 = cms.vint32(72, 8, 40, 24, 0, 
        0)
)


process.CSCGeometryESModule = cms.ESProducer("CSCGeometryESModule",
    appendToDataLabel = cms.string(''),
    debugV = cms.untracked.bool(False),
    useGangedStripsInME1a = cms.bool(True),
    alignmentsLabel = cms.string(''),
    useOnlyWiresInME1a = cms.bool(False),
    useRealWireGeometry = cms.bool(True),
    useCentreTIOffsets = cms.bool(False),
    applyAlignment = cms.bool(True)
)


process.l1GtTriggerMenuXml = cms.ESProducer("L1GtTriggerMenuXmlProducer",
    VmeXmlFile = cms.string(''),
    DefXmlFile = cms.string('L1Menu2007.xml'),
    TriggerMenuLuminosity = cms.string('lumi1x1032')
)


process.EcalEndcapGeometryEP = cms.ESProducer("EcalEndcapGeometryEP",
    applyAlignment = cms.untracked.bool(False)
)


process.L1MuTriggerScales = cms.ESProducer("L1MuTriggerScalesProducer",
    signedPackingDTEta = cms.bool(True),
    offsetDTEta = cms.int32(32),
    nbinsDTEta = cms.int32(64),
    offsetFwdRPCEta = cms.int32(16),
    signedPackingBrlRPCEta = cms.bool(True),
    maxDTEta = cms.double(1.2),
    nbitPackingFwdRPCEta = cms.int32(6),
    nbinsBrlRPCEta = cms.int32(33),
    nbinsFwdRPCEta = cms.int32(33),
    nbitPackingGMTEta = cms.int32(6),
    minCSCEta = cms.double(0.9),
    nbinsPhi = cms.int32(144),
    nbitPackingPhi = cms.int32(8),
    nbitPackingDTEta = cms.int32(6),
    maxCSCEta = cms.double(2.5),
    nbinsGMTEta = cms.int32(31),
    minDTEta = cms.double(-1.2),
    nbitPackingCSCEta = cms.int32(6),
    signedPackingFwdRPCEta = cms.bool(True),
    offsetBrlRPCEta = cms.int32(16),
    scaleRPCEta = cms.vdouble(-2.1, -1.97, -1.85, -1.73, -1.61, 
        -1.48, -1.36, -1.24, -1.14, -1.04, 
        -0.93, -0.83, -0.72, -0.58, -0.44, 
        -0.27, -0.07, 0.07, 0.27, 0.44, 
        0.58, 0.72, 0.83, 0.93, 1.04, 
        1.14, 1.24, 1.36, 1.48, 1.61, 
        1.73, 1.85, 1.97, 2.1),
    signedPackingPhi = cms.bool(False),
    nbitPackingBrlRPCEta = cms.int32(6),
    nbinsCSCEta = cms.int32(32),
    maxPhi = cms.double(6.2831853),
    minPhi = cms.double(0.0),
    scaleGMTEta = cms.vdouble(0.0, 0.1, 0.2, 0.3, 0.4, 
        0.5, 0.6, 0.7, 0.8, 0.9, 
        1.0, 1.1, 1.2, 1.3, 1.4, 
        1.5, 1.6, 1.7, 1.75, 1.8, 
        1.85, 1.9, 1.95, 2.0, 2.05, 
        2.1, 2.15, 2.2, 2.25, 2.3, 
        2.35, 2.4)
)


process.hcalDetIdAssociator = cms.ESProducer("DetIdAssociatorESProducer",
    ComponentName = cms.string('HcalDetIdAssociator'),
    etaBinSize = cms.double(0.087),
    nEta = cms.int32(70),
    nPhi = cms.int32(72)
)


process.siStripGainESProducer = cms.ESProducer("SiStripGainESProducer",
    printDebug = cms.untracked.bool(False),
    appendToDataLabel = cms.string(''),
    APVGain = cms.string(''),
    AutomaticNormalization = cms.bool(False),
    NormalizationFactor = cms.double(1.0)
)


process.HcalHardcodeGeometryEP = cms.ESProducer("HcalHardcodeGeometryEP",
    applyAlignment = cms.untracked.bool(False)
)


process.RPCGeometryESModule = cms.ESProducer("RPCGeometryESModule",
    compatibiltyWith11 = cms.untracked.bool(True)
)


process.idealForDigiDTGeometry = cms.ESProducer("DTGeometryESModule",
    appendToDataLabel = cms.string('idealForDigi'),
    applyAlignment = cms.bool(False),
    alignmentsLabel = cms.string('fakeForIdeal')
)


process.CaloTowerHardcodeGeometryEP = cms.ESProducer("CaloTowerHardcodeGeometryEP")


process.L1CaloInputScalesProducer = cms.ESProducer("L1CaloInputScalesProducer",
    L1HcalEtThresholds = (cms.vdouble(0.0, 0.7, 0.9, 1.1, 1.2, 1.4, 1.6, 1.8, 1.9, 2.1, 2.3, 2.6, 2.9, 3.2, 3.4, 3.6, 4.0, 4.3, 4.7, 5.0, 5.3, 5.8, 6.3, 6.5, 6.9, 7.4, 7.8, 8.2, 8.8, 9.2, 9.8, 10.3, 10.8, 11.3, 11.5, 11.8, 12.4, 12.8, 13.4, 14.0, 14.4, 14.9, 15.4, 15.9, 16.4, 17.0, 17.5, 17.9, 18.5, 18.9, 19.5, 19.9, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.6, 24.2, 24.9, 25.6, 26.1, 27.0, 27.6, 28.1, 28.9, 29.4, 30.1, 30.9, 31.4, 32.2, 32.7, 33.3, 34.2, 34.7, 35.4, 36.3, 37.0, 37.5, 38.4, 39.2, 39.8, 40.5, 41.4, 42.0, 42.6, 43.5, 44.4, 44.9, 45.5, 46.5, 47.4, 47.9, 48.5, 49.5, 50.4, 51.1, 51.7, 52.5, 53.4, 54.4, 55.0, 55.5, 56.4, 57.4, 58.4, 58.9, 59.4, 60.4, 61.4, 62.2, 63.0, 63.7, 64.4, 65.3, 66.2, 67.2, 67.7, 67.9, 68.4, 69.4, 70.4, 71.4, 72.1, 72.6, 73.4, 74.4, 75.3, 76.2, 76.7, 77.4, 78.3, 79.2, 80.2, 80.9, 81.4, 82.2, 83.2, 84.2, 85.1, 85.6, 86.2, 87.2, 88.1, 89.0, 89.7, 90.3, 91.1, 92.0, 93.0, 93.9, 94.4, 95.0, 96.0, 96.9, 97.9, 98.6, 99.1, 99.9, 100.9, 101.9, 102.7, 103.3, 103.9, 104.9, 105.7, 106.7, 107.4, 108.0, 108.8, 109.7, 110.7, 111.6, 112.1, 112.7, 113.7, 114.6, 115.6, 116.3, 116.8, 117.6, 118.6, 119.5, 120.4, 121.0, 121.6, 122.5, 123.4, 124.4, 125.1, 125.6, 126.4, 127.4, 128.4, 129.3, 130.2, 131.2, 131.7, 132.4, 133.3, 134.2, 135.2, 136.2, 137.0, 138.0, 139.0, 139.9, 140.5, 141.1, 142.0, 142.9, 143.9, 144.8, 145.7, 146.7, 147.7, 148.5, 149.2, 149.9, 150.7, 151.5, 152.5, 153.5, 154.4, 155.3, 156.3, 157.2, 158.0, 158.6, 159.3, 160.2, 161.2, 162.2, 163.0, 164.0, 165.0, 165.9, 166.8, 167.4, 168.0, 168.9, 169.8, 170.8, 171.7, 172.7, 173.6, 174.5, 175.5, 176.1, 176.7, 177.5, 178.5, 179.5, 180.4)+cms.vdouble(180.9, 0.0, 0.7, 0.9, 1.1, 1.2, 1.4, 1.6, 1.8, 1.9, 2.1, 2.3, 2.5, 2.9, 3.2, 3.3, 3.6, 3.9, 4.3, 4.7, 4.9, 5.3, 5.8, 6.2, 6.5, 6.8, 7.4, 7.7, 8.2, 8.7, 9.1, 9.7, 10.2, 10.7, 11.2, 11.4, 11.8, 12.3, 12.7, 13.3, 13.9, 14.3, 14.8, 15.3, 15.8, 16.2, 16.8, 17.4, 17.8, 18.3, 18.8, 19.3, 19.7, 20.4, 20.9, 21.3, 21.9, 22.3, 22.8, 23.4, 24.0, 24.7, 25.4, 25.9, 26.8, 27.4, 27.9, 28.7, 29.2, 29.9, 30.6, 31.2, 31.9, 32.5, 33.1, 34.0, 34.5, 35.1, 36.1, 36.7, 37.2, 38.1, 38.9, 39.5, 40.2, 41.1, 41.7, 42.3, 43.2, 44.1, 44.6, 45.2, 46.2, 47.0, 47.6, 48.2, 49.1, 50.0, 50.7, 51.3, 52.1, 53.0, 54.0, 54.6, 55.1, 56.0, 57.0, 57.9, 58.4, 59.0, 59.9, 60.9, 61.8, 62.6, 63.2, 63.9, 64.8, 65.7, 66.7, 67.2, 67.4, 67.9, 68.9, 69.9, 70.8, 71.5, 72.0, 72.8, 73.8, 74.8, 75.6, 76.2, 76.8, 77.7, 78.6, 79.6, 80.3, 80.8, 81.6, 82.6, 83.5, 84.4, 84.9, 85.6, 86.5, 87.4, 88.4, 89.1, 89.6, 90.4, 91.3, 92.3, 93.2, 93.7, 94.3, 95.3, 96.2, 97.1, 97.8, 98.4, 99.2, 100.1, 101.1, 102.0, 102.5, 103.1, 104.1, 105.0, 105.9, 106.6, 107.1, 107.9, 108.9, 109.9, 110.7, 111.3, 111.9, 112.8, 113.7, 114.7, 115.4, 115.9, 116.7, 117.7, 118.6, 119.5, 120.0, 120.7, 121.6, 122.5, 123.5, 124.2, 124.7, 125.5, 126.5, 127.4, 128.3, 129.3, 130.2, 130.8, 131.4, 132.3, 133.2, 134.2, 135.1, 136.0, 137.0, 137.9, 138.8, 139.4, 140.1, 140.9, 141.8, 142.8, 143.7, 144.6, 145.6, 146.5, 147.4, 148.1, 148.7, 149.5, 150.4, 151.4, 152.3, 153.2, 154.2, 155.1, 156.0, 156.8, 157.4, 158.1, 159.0, 160.0, 160.9, 161.8, 162.8, 163.7, 164.6, 165.5, 166.1, 166.7, 167.6, 168.6, 169.5, 170.4, 171.4, 172.3, 173.2, 174.2, 174.8, 175.3, 176.2, 177.2, 178.1)+cms.vdouble(179.0, 179.5, 0.0, 0.7, 0.9, 1.0, 1.2, 1.4, 1.6, 1.7, 1.9, 2.1, 2.2, 2.5, 2.9, 3.1, 3.3, 3.5, 3.9, 4.2, 4.6, 4.8, 5.2, 5.7, 6.1, 6.4, 6.7, 7.3, 7.6, 8.0, 8.6, 9.0, 9.6, 10.0, 10.5, 11.1, 11.2, 11.6, 12.1, 12.5, 13.1, 13.7, 14.1, 14.6, 15.0, 15.6, 16.0, 16.6, 17.1, 17.5, 18.1, 18.5, 19.0, 19.5, 20.1, 20.6, 21.0, 21.5, 22.0, 22.5, 23.1, 23.7, 24.4, 25.0, 25.5, 26.4, 27.0, 27.5, 28.3, 28.8, 29.5, 30.2, 30.7, 31.5, 32.0, 32.6, 33.5, 34.0, 34.6, 35.5, 36.1, 36.7, 37.5, 38.3, 38.9, 39.6, 40.5, 41.1, 41.7, 42.5, 43.4, 43.9, 44.5, 45.5, 46.3, 46.9, 47.5, 48.4, 49.3, 50.0, 50.6, 51.3, 52.2, 53.2, 53.8, 54.3, 55.2, 56.1, 57.1, 57.6, 58.1, 59.0, 60.0, 60.9, 61.6, 62.2, 62.9, 63.8, 64.7, 65.7, 66.2, 66.4, 66.9, 67.9, 68.8, 69.8, 70.5, 71.0, 71.8, 72.7, 73.7, 74.5, 75.0, 75.6, 76.6, 77.5, 78.4, 79.1, 79.6, 80.4, 81.3, 82.3, 83.2, 83.7, 84.3, 85.2, 86.1, 87.1, 87.7, 88.3, 89.0, 90.0, 90.9, 91.8, 92.3, 92.9, 93.9, 94.7, 95.7, 96.4, 96.9, 97.7, 98.6, 99.6, 100.5, 101.0, 101.6, 102.5, 103.4, 104.3, 105.0, 105.6, 106.3, 107.3, 108.2, 109.1, 109.6, 110.2, 111.2, 112.0, 113.0, 113.7, 114.2, 115.0, 115.9, 116.9, 117.7, 118.3, 118.9, 119.8, 120.7, 121.6, 122.3, 122.8, 123.6, 124.6, 125.5, 126.4, 127.3, 128.3, 128.8, 129.4, 130.4, 131.2, 132.2, 133.1, 134.0, 134.9, 135.9, 136.8, 137.4, 138.0, 138.8, 139.7, 140.6, 141.6, 142.5, 143.4, 144.4, 145.2, 145.9, 146.5, 147.3, 148.2, 149.1, 150.1, 150.9, 151.9, 152.8, 153.7, 154.5, 155.1, 155.8, 156.6, 157.6, 158.5, 159.4, 160.4, 161.3, 162.2, 163.0, 163.6, 164.2, 165.1, 166.1, 167.0, 167.9, 168.8, 169.8, 170.6, 171.6, 172.2, 172.7, 173.6, 174.5)+cms.vdouble(175.5, 176.4, 176.9, 0.0, 0.7, 0.8, 1.0, 1.2, 1.4, 1.5, 1.7, 1.9, 2.0, 2.2, 2.5, 2.8, 3.0, 3.2, 3.5, 3.8, 4.1, 4.5, 4.7, 5.1, 5.6, 6.0, 6.3, 6.6, 7.1, 7.4, 7.9, 8.4, 8.8, 9.4, 9.8, 10.3, 10.8, 11.0, 11.3, 11.8, 12.3, 12.9, 13.4, 13.8, 14.3, 14.7, 15.2, 15.6, 16.2, 16.7, 17.2, 17.7, 18.1, 18.6, 19.0, 19.6, 20.1, 20.5, 21.1, 21.5, 22.0, 22.6, 23.2, 23.8, 24.4, 24.9, 25.8, 26.4, 26.9, 27.6, 28.2, 28.8, 29.5, 30.0, 30.8, 31.3, 31.9, 32.7, 33.2, 33.8, 34.7, 35.3, 35.8, 36.7, 37.5, 38.0, 38.7, 39.6, 40.2, 40.8, 41.6, 42.4, 43.0, 43.5, 44.5, 45.3, 45.8, 46.4, 47.3, 48.2, 48.9, 49.5, 50.2, 51.1, 52.0, 52.6, 53.1, 53.9, 54.9, 55.8, 56.3, 56.8, 57.7, 58.7, 59.5, 60.3, 60.9, 61.6, 62.4, 63.3, 64.3, 64.8, 64.9, 65.4, 66.4, 67.3, 68.2, 68.9, 69.4, 70.2, 71.1, 72.0, 72.9, 73.4, 74.0, 74.9, 75.8, 76.7, 77.4, 77.9, 78.6, 79.6, 80.5, 81.3, 81.8, 82.4, 83.4, 84.2, 85.1, 85.8, 86.3, 87.1, 88.0, 88.9, 89.8, 90.3, 90.9, 91.8, 92.7, 93.6, 94.3, 94.8, 95.5, 96.5, 97.4, 98.2, 98.8, 99.3, 100.3, 101.1, 102.1, 102.7, 103.2, 104.0, 104.9, 105.9, 106.7, 107.2, 107.8, 108.7, 109.6, 110.5, 111.2, 111.7, 112.5, 113.4, 114.3, 115.2, 115.7, 116.3, 117.2, 118.0, 119.0, 119.6, 120.1, 120.9, 121.8, 122.8, 123.6, 124.5, 125.5, 126.0, 126.6, 127.5, 128.3, 129.3, 130.2, 131.1, 132.0, 132.9, 133.8, 134.3, 134.9, 135.8, 136.6, 137.6, 138.5, 139.3, 140.3, 141.2, 142.0, 142.7, 143.3, 144.1, 144.9, 145.8, 146.8, 147.6, 148.6, 149.5, 150.3, 151.1, 151.7, 152.4, 153.2, 154.1, 155.1, 155.9, 156.8, 157.8, 158.6, 159.5, 160.1, 160.6, 161.5, 162.4, 163.4, 164.2, 165.1, 166.1, 166.9, 167.8, 168.4, 168.9, 169.8)+cms.vdouble(170.7, 171.6, 172.5, 173.0, 0.0, 0.7, 0.8, 1.0, 1.1, 1.3, 1.5, 1.6, 1.8, 2.0, 2.1, 2.4, 2.7, 3.0, 3.1, 3.4, 3.7, 4.0, 4.4, 4.6, 4.9, 5.4, 5.8, 6.1, 6.4, 6.9, 7.2, 7.6, 8.1, 8.5, 9.1, 9.5, 10.0, 10.5, 10.7, 11.0, 11.5, 11.9, 12.5, 13.0, 13.4, 13.9, 14.3, 14.8, 15.2, 15.8, 16.3, 16.7, 17.2, 17.6, 18.1, 18.5, 19.1, 19.5, 20.0, 20.4, 20.9, 21.4, 21.9, 22.5, 23.2, 23.7, 24.2, 25.0, 25.6, 26.1, 26.9, 27.3, 28.0, 28.7, 29.2, 29.9, 30.4, 31.0, 31.8, 32.3, 32.9, 33.8, 34.3, 34.8, 35.6, 36.4, 37.0, 37.6, 38.4, 39.0, 39.6, 40.4, 41.2, 41.7, 42.3, 43.2, 44.0, 44.5, 45.1, 46.0, 46.8, 47.5, 48.0, 48.8, 49.6, 50.5, 51.1, 51.6, 52.4, 53.3, 54.2, 54.7, 55.2, 56.1, 57.0, 57.8, 58.6, 59.1, 59.8, 60.6, 61.5, 62.4, 62.9, 63.1, 63.6, 64.5, 65.4, 66.3, 66.9, 67.4, 68.2, 69.1, 70.0, 70.8, 71.3, 71.9, 72.8, 73.6, 74.5, 75.1, 75.6, 76.4, 77.3, 78.2, 79.0, 79.5, 80.1, 81.0, 81.8, 82.7, 83.4, 83.9, 84.6, 85.5, 86.4, 87.2, 87.7, 88.3, 89.2, 90.0, 90.9, 91.6, 92.1, 92.8, 93.7, 94.6, 95.4, 95.9, 96.5, 97.4, 98.2, 99.1, 99.8, 100.3, 101.0, 101.9, 102.8, 103.6, 104.1, 104.7, 105.6, 106.4, 107.3, 108.0, 108.5, 109.2, 110.1, 111.0, 111.9, 112.3, 112.9, 113.8, 114.6, 115.6, 116.2, 116.7, 117.4, 118.3, 119.2, 120.1, 121.0, 121.9, 122.4, 122.9, 123.8, 124.7, 125.6, 126.5, 127.3, 128.2, 129.1, 129.9, 130.5, 131.1, 131.9, 132.7, 133.6, 134.5, 135.3, 136.2, 137.1, 138.0, 138.6, 139.2, 139.9, 140.8, 141.7, 142.6, 143.4, 144.3, 145.2, 146.0, 146.8, 147.3, 148.0, 148.8, 149.7, 150.6, 151.4, 152.3, 153.2, 154.1, 154.9, 155.5, 156.0, 156.9, 157.8, 158.7, 159.5, 160.4, 161.3, 162.1, 163.0, 163.6, 164.1)+cms.vdouble(164.9, 165.8, 166.7, 167.5, 168.0, 0.0, 0.6, 0.8, 1.0, 1.1, 1.3, 1.4, 1.6, 1.7, 1.9, 2.1, 2.3, 2.6, 2.9, 3.0, 3.2, 3.6, 3.9, 4.2, 4.4, 4.8, 5.2, 5.6, 5.9, 6.2, 6.7, 7.0, 7.4, 7.8, 8.2, 8.8, 9.2, 9.7, 10.1, 10.3, 10.6, 11.1, 11.5, 12.0, 12.5, 12.9, 13.4, 13.8, 14.3, 14.7, 15.2, 15.7, 16.1, 16.6, 17.0, 17.4, 17.8, 18.4, 18.9, 19.3, 19.7, 20.1, 20.6, 21.2, 21.7, 22.3, 22.9, 23.4, 24.2, 24.7, 25.2, 25.9, 26.4, 27.0, 27.7, 28.1, 28.8, 29.3, 29.9, 30.7, 31.1, 31.7, 32.6, 33.1, 33.6, 34.4, 35.1, 35.7, 36.3, 37.1, 37.6, 38.2, 39.0, 39.8, 40.3, 40.8, 41.7, 42.5, 43.0, 43.5, 44.4, 45.2, 45.8, 46.4, 47.1, 47.9, 48.7, 49.3, 49.8, 50.6, 51.4, 52.3, 52.8, 53.3, 54.1, 55.0, 55.8, 56.5, 57.1, 57.7, 58.5, 59.4, 60.2, 60.7, 60.9, 61.3, 62.2, 63.1, 64.0, 64.6, 65.1, 65.8, 66.7, 67.5, 68.3, 68.8, 69.3, 70.2, 71.0, 71.9, 72.5, 73.0, 73.7, 74.6, 75.4, 76.2, 76.7, 77.3, 78.1, 78.9, 79.8, 80.4, 80.9, 81.6, 82.5, 83.4, 84.2, 84.6, 85.2, 86.1, 86.9, 87.7, 88.4, 88.8, 89.6, 90.4, 91.3, 92.1, 92.6, 93.1, 94.0, 94.8, 95.7, 96.3, 96.8, 97.5, 98.4, 99.2, 100.0, 100.5, 101.0, 101.9, 102.7, 103.6, 104.2, 104.7, 105.4, 106.3, 107.1, 107.9, 108.4, 109.0, 109.8, 110.6, 111.5, 112.1, 112.6, 113.3, 114.2, 115.1, 115.9, 116.7, 117.6, 118.1, 118.6, 119.5, 120.3, 121.2, 122.0, 122.8, 123.7, 124.6, 125.4, 125.9, 126.5, 127.3, 128.1, 128.9, 129.8, 130.6, 131.5, 132.4, 133.1, 133.8, 134.3, 135.0, 135.8, 136.7, 137.6, 138.4, 139.2, 140.1, 140.9, 141.6, 142.2, 142.8, 143.6, 144.5, 145.3, 146.1, 147.0, 147.9, 148.7, 149.5, 150.0, 150.6, 151.4, 152.2, 153.1, 153.9, 154.8, 155.7, 156.4, 157.3, 157.9)+cms.vdouble(158.3, 159.1, 160.0, 160.9, 161.7, 162.2, 0.0, 0.6, 0.8, 0.9, 1.1, 1.2, 1.4, 1.5, 1.7, 1.8, 2.0, 2.2, 2.5, 2.7, 2.9, 3.1, 3.4, 3.7, 4.0, 4.3, 4.6, 5.0, 5.4, 5.6, 5.9, 6.4, 6.7, 7.1, 7.5, 7.9, 8.4, 8.8, 9.3, 9.7, 9.9, 10.2, 10.6, 11.0, 11.6, 12.0, 12.4, 12.8, 13.2, 13.7, 14.1, 14.6, 15.1, 15.4, 15.9, 16.3, 16.7, 17.1, 17.6, 18.1, 18.5, 18.9, 19.3, 19.8, 20.3, 20.8, 21.4, 22.0, 22.4, 23.2, 23.7, 24.2, 24.9, 25.3, 25.9, 26.5, 27.0, 27.7, 28.1, 28.7, 29.4, 29.9, 30.4, 31.2, 31.8, 32.2, 33.0, 33.7, 34.2, 34.8, 35.6, 36.1, 36.6, 37.4, 38.2, 38.6, 39.1, 40.0, 40.7, 41.2, 41.7, 42.6, 43.3, 43.9, 44.5, 45.2, 45.9, 46.8, 47.3, 47.7, 48.5, 49.3, 50.2, 50.6, 51.1, 51.9, 52.8, 53.5, 54.2, 54.7, 55.3, 56.1, 56.9, 57.8, 58.2, 58.4, 58.8, 59.7, 60.5, 61.3, 62.0, 62.4, 63.1, 63.9, 64.8, 65.5, 66.0, 66.5, 67.4, 68.1, 68.9, 69.6, 70.0, 70.7, 71.5, 72.4, 73.1, 73.6, 74.1, 75.0, 75.7, 76.5, 77.2, 77.6, 78.3, 79.1, 80.0, 80.7, 81.2, 81.7, 82.6, 83.3, 84.2, 84.8, 85.2, 85.9, 86.7, 87.6, 88.3, 88.8, 89.3, 90.2, 90.9, 91.8, 92.4, 92.8, 93.5, 94.3, 95.2, 95.9, 96.4, 96.9, 97.8, 98.5, 99.4, 100.0, 100.4, 101.1, 101.9, 102.8, 103.5, 104.0, 104.5, 105.4, 106.1, 107.0, 107.6, 108.0, 108.7, 109.5, 110.4, 111.1, 112.0, 112.8, 113.3, 113.8, 114.6, 115.4, 116.2, 117.1, 117.8, 118.7, 119.5, 120.3, 120.8, 121.3, 122.1, 122.8, 123.7, 124.5, 125.3, 126.1, 126.9, 127.7, 128.3, 128.9, 129.5, 130.3, 131.1, 132.0, 132.7, 133.6, 134.4, 135.2, 135.8, 136.4, 137.0, 137.7, 138.6, 139.4, 140.2, 141.0, 141.8, 142.6, 143.4, 143.9, 144.4, 145.2, 146.0, 146.9, 147.6, 148.5, 149.3, 150.1, 150.9)+cms.vdouble(151.4, 151.9, 152.6, 153.5, 154.3, 155.1, 155.5, 0.0, 0.6, 0.7, 0.9, 1.0, 1.2, 1.3, 1.5, 1.6, 1.7, 1.9, 2.1, 2.4, 2.6, 2.8, 3.0, 3.3, 3.6, 3.8, 4.1, 4.4, 4.8, 5.1, 5.4, 5.7, 6.1, 6.4, 6.7, 7.2, 7.5, 8.0, 8.4, 8.8, 9.3, 9.4, 9.7, 10.2, 10.5, 11.0, 11.5, 11.8, 12.3, 12.6, 13.1, 13.4, 13.9, 14.4, 14.7, 15.2, 15.5, 16.0, 16.3, 16.8, 17.3, 17.6, 18.1, 18.4, 18.9, 19.4, 19.9, 20.4, 21.0, 21.4, 22.1, 22.6, 23.1, 23.7, 24.1, 24.7, 25.3, 25.7, 26.4, 26.8, 27.3, 28.1, 28.5, 29.0, 29.8, 30.3, 30.7, 31.5, 32.1, 32.6, 33.2, 33.9, 34.4, 34.9, 35.7, 36.4, 36.8, 37.3, 38.1, 38.9, 39.3, 39.8, 40.6, 41.3, 41.9, 42.4, 43.1, 43.8, 44.6, 45.1, 45.5, 46.3, 47.1, 47.9, 48.3, 48.7, 49.5, 50.3, 51.0, 51.7, 52.2, 52.8, 53.5, 54.3, 55.1, 55.5, 55.7, 56.1, 56.9, 57.7, 58.5, 59.1, 59.5, 60.2, 61.0, 61.8, 62.5, 62.9, 63.4, 64.2, 65.0, 65.8, 66.3, 66.8, 67.4, 68.2, 69.0, 69.8, 70.2, 70.7, 71.5, 72.2, 73.0, 73.6, 74.0, 74.7, 75.5, 76.3, 77.0, 77.4, 77.9, 78.7, 79.5, 80.3, 80.8, 81.3, 81.9, 82.7, 83.5, 84.3, 84.7, 85.2, 86.0, 86.7, 87.5, 88.1, 88.5, 89.2, 90.0, 90.8, 91.5, 91.9, 92.4, 93.2, 94.0, 94.8, 95.3, 95.8, 96.4, 97.2, 98.0, 98.8, 99.2, 99.7, 100.5, 101.2, 102.0, 102.6, 103.0, 103.7, 104.5, 105.3, 106.0, 106.8, 107.6, 108.0, 108.5, 109.3, 110.1, 110.9, 111.7, 112.4, 113.2, 114.0, 114.7, 115.2, 115.7, 116.4, 117.2, 118.0, 118.8, 119.5, 120.3, 121.1, 121.8, 122.4, 122.9, 123.6, 124.3, 125.1, 125.9, 126.6, 127.4, 128.2, 128.9, 129.6, 130.1, 130.7, 131.4, 132.2, 133.0, 133.7, 134.5, 135.3, 136.0, 136.8, 137.3, 137.8, 138.5, 139.3, 140.1, 140.8, 141.6, 142.4, 143.1)+cms.vdouble(143.9, 144.4, 144.9, 145.6, 146.4, 147.2, 147.9, 148.4, 0.0, 0.6, 0.7, 0.8, 1.0, 1.1, 1.2, 1.4, 1.5, 1.7, 1.8, 2.0, 2.3, 2.5, 2.6, 2.8, 3.1, 3.4, 3.6, 3.9, 4.1, 4.5, 4.9, 5.1, 5.4, 5.8, 6.1, 6.4, 6.8, 7.2, 7.6, 8.0, 8.4, 8.8, 8.9, 9.2, 9.6, 10.0, 10.5, 10.9, 11.2, 11.6, 12.0, 12.4, 12.7, 13.2, 13.6, 14.0, 14.4, 14.7, 15.1, 15.5, 16.0, 16.4, 16.7, 17.1, 17.5, 17.9, 18.4, 18.9, 19.4, 19.9, 20.3, 21.0, 21.5, 21.9, 22.5, 22.9, 23.5, 24.0, 24.4, 25.0, 25.5, 25.9, 26.6, 27.0, 27.5, 28.3, 28.8, 29.2, 29.9, 30.5, 31.0, 31.5, 32.2, 32.7, 33.2, 33.9, 34.5, 35.0, 35.4, 36.2, 36.9, 37.3, 37.8, 38.5, 39.2, 39.8, 40.3, 40.9, 41.6, 42.3, 42.8, 43.2, 43.9, 44.7, 45.4, 45.8, 46.2, 47.0, 47.8, 48.4, 49.1, 49.5, 50.1, 50.8, 51.5, 52.3, 52.7, 52.8, 53.3, 54.0, 54.8, 55.5, 56.1, 56.5, 57.1, 57.9, 58.6, 59.3, 59.7, 60.2, 61.0, 61.7, 62.4, 63.0, 63.4, 64.0, 64.8, 65.5, 66.2, 66.6, 67.1, 67.8, 68.5, 69.3, 69.8, 70.3, 70.9, 71.6, 72.4, 73.1, 73.5, 74.0, 74.7, 75.4, 76.2, 76.7, 77.1, 77.8, 78.5, 79.3, 80.0, 80.4, 80.9, 81.6, 82.3, 83.1, 83.6, 84.0, 84.6, 85.4, 86.2, 86.8, 87.3, 87.7, 88.5, 89.2, 89.9, 90.5, 90.9, 91.5, 92.3, 93.0, 93.7, 94.1, 94.6, 95.4, 96.1, 96.8, 97.4, 97.8, 98.4, 99.2, 99.9, 100.6, 101.4, 102.1, 102.5, 103.0, 103.8, 104.5, 105.2, 106.0, 106.7, 107.4, 108.2, 108.9, 109.3, 109.8, 110.5, 111.2, 112.0, 112.7, 113.4, 114.2, 114.9, 115.6, 116.2, 116.6, 117.3, 117.9, 118.7, 119.5, 120.1, 120.9, 121.7, 122.3, 123.0, 123.4, 124.0, 124.7, 125.4, 126.2, 126.9, 127.6, 128.4, 129.1, 129.8, 130.3, 130.7, 131.4, 132.2, 132.9, 133.6, 134.4, 135.1)+cms.vdouble(135.8, 136.6, 137.1, 137.5, 138.2, 138.9, 139.7, 140.4, 140.8, 0.0, 0.5, 0.7, 0.8, 0.9, 1.0, 1.2, 1.3, 1.4, 1.6, 1.7, 1.9, 2.1, 2.3, 2.5, 2.7, 2.9, 3.2, 3.4, 3.6, 3.9, 4.3, 4.6, 4.8, 5.1, 5.5, 5.7, 6.0, 6.4, 6.8, 7.2, 7.5, 7.9, 8.3, 8.5, 8.7, 9.1, 9.4, 9.9, 10.3, 10.6, 11.0, 11.3, 11.7, 12.0, 12.5, 12.9, 13.2, 13.6, 13.9, 14.3, 14.6, 15.1, 15.5, 15.8, 16.2, 16.5, 16.9, 17.4, 17.8, 18.3, 18.8, 19.2, 19.8, 20.3, 20.7, 21.3, 21.6, 22.2, 22.7, 23.1, 23.7, 24.1, 24.5, 25.2, 25.5, 26.0, 26.7, 27.2, 27.6, 28.2, 28.8, 29.3, 29.8, 30.4, 30.9, 31.3, 32.0, 32.6, 33.0, 33.5, 34.2, 34.8, 35.2, 35.7, 36.4, 37.1, 37.6, 38.0, 38.6, 39.3, 40.0, 40.4, 40.8, 41.5, 42.2, 42.9, 43.3, 43.7, 44.4, 45.1, 45.8, 46.3, 46.8, 47.3, 48.0, 48.7, 49.4, 49.8, 49.9, 50.3, 51.0, 51.7, 52.5, 53.0, 53.4, 54.0, 54.7, 55.4, 56.0, 56.4, 56.9, 57.6, 58.2, 59.0, 59.5, 59.9, 60.5, 61.2, 61.9, 62.5, 62.9, 63.4, 64.1, 64.7, 65.5, 66.0, 66.4, 67.0, 67.7, 68.4, 69.0, 69.4, 69.9, 70.6, 71.2, 72.0, 72.5, 72.9, 73.5, 74.2, 74.9, 75.5, 75.9, 76.4, 77.1, 77.7, 78.5, 79.0, 79.4, 80.0, 80.7, 81.4, 82.0, 82.4, 82.9, 83.6, 84.2, 85.0, 85.5, 85.9, 86.5, 87.2, 87.9, 88.5, 88.9, 89.4, 90.1, 90.7, 91.5, 92.0, 92.4, 93.0, 93.7, 94.4, 95.0, 95.8, 96.5, 96.9, 97.3, 98.0, 98.7, 99.4, 100.1, 100.8, 101.5, 102.2, 102.8, 103.3, 103.7, 104.4, 105.0, 105.8, 106.5, 107.1, 107.8, 108.6, 109.2, 109.7, 110.2, 110.8, 111.4, 112.1, 112.8, 113.5, 114.2, 114.9, 115.6, 116.2, 116.6, 117.1, 117.8, 118.5, 119.2, 119.9, 120.6, 121.3, 121.9, 122.6, 123.1, 123.5, 124.2, 124.9, 125.6, 126.2, 127.0)+cms.vdouble(127.7, 128.3, 129.0, 129.5, 129.9, 130.5, 131.2, 132.0, 132.6, 133.0, 0.0, 0.5, 0.6, 0.7, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.3, 2.5, 2.8, 3.0, 3.2, 3.4, 3.7, 4.0, 4.3, 4.5, 4.8, 5.1, 5.4, 5.7, 6.1, 6.4, 6.8, 7.1, 7.5, 7.8, 8.0, 8.2, 8.6, 8.9, 9.3, 9.7, 10.0, 10.3, 10.6, 11.0, 11.3, 11.7, 12.1, 12.4, 12.8, 13.1, 13.5, 13.8, 14.2, 14.6, 14.9, 15.2, 15.5, 15.9, 16.3, 16.8, 17.2, 17.7, 18.0, 18.7, 19.1, 19.4, 20.0, 20.4, 20.9, 21.3, 21.7, 22.3, 22.6, 23.1, 23.7, 24.0, 24.5, 25.1, 25.6, 25.9, 26.5, 27.1, 27.5, 28.0, 28.6, 29.0, 29.5, 30.1, 30.7, 31.1, 31.5, 32.2, 32.8, 33.1, 33.6, 34.2, 34.9, 35.3, 35.8, 36.3, 36.9, 37.6, 38.0, 38.4, 39.0, 39.7, 40.4, 40.7, 41.1, 41.8, 42.4, 43.1, 43.6, 44.0, 44.5, 45.1, 45.8, 46.5, 46.8, 47.0, 47.3, 48.0, 48.7, 49.4, 49.8, 50.2, 50.8, 51.4, 52.1, 52.7, 53.1, 53.5, 54.2, 54.8, 55.5, 56.0, 56.3, 56.9, 57.5, 58.2, 58.8, 59.2, 59.6, 60.3, 60.9, 61.6, 62.1, 62.4, 63.0, 63.7, 64.3, 64.9, 65.3, 65.7, 66.4, 67.0, 67.7, 68.2, 68.6, 69.1, 69.8, 70.5, 71.1, 71.4, 71.9, 72.5, 73.1, 73.8, 74.3, 74.7, 75.2, 75.9, 76.6, 77.2, 77.5, 78.0, 78.6, 79.3, 79.9, 80.4, 80.8, 81.3, 82.0, 82.7, 83.3, 83.7, 84.1, 84.8, 85.4, 86.0, 86.5, 86.9, 87.5, 88.1, 88.8, 89.4, 90.1, 90.8, 91.1, 91.6, 92.2, 92.8, 93.5, 94.2, 94.8, 95.5, 96.1, 96.8, 97.2, 97.6, 98.2, 98.8, 99.5, 100.2, 100.8, 101.5, 102.1, 102.7, 103.2, 103.7, 104.2, 104.8, 105.5, 106.2, 106.8, 107.5, 108.1, 108.7, 109.3, 109.7, 110.2, 110.8, 111.5, 112.2, 112.8, 113.4, 114.1, 114.7, 115.3, 115.8, 116.2, 116.8, 117.5, 118.2, 118.8)+cms.vdouble(119.4, 120.1, 120.7, 121.4, 121.8, 122.2, 122.8, 123.5, 124.2, 124.8, 125.1, 0.0, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.3, 1.4, 1.5, 1.7, 1.9, 2.1, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.8, 4.1, 4.2, 4.5, 4.8, 5.0, 5.3, 5.7, 6.0, 6.4, 6.7, 7.0, 7.3, 7.5, 7.7, 8.0, 8.3, 8.7, 9.1, 9.3, 9.7, 10.0, 10.3, 10.6, 11.0, 11.4, 11.6, 12.0, 12.3, 12.6, 12.9, 13.3, 13.6, 13.9, 14.3, 14.6, 14.9, 15.3, 15.7, 16.2, 16.6, 16.9, 17.5, 17.9, 18.2, 18.7, 19.1, 19.5, 20.0, 20.4, 20.9, 21.2, 21.6, 22.2, 22.5, 22.9, 23.6, 24.0, 24.3, 24.9, 25.4, 25.8, 26.3, 26.8, 27.2, 27.6, 28.2, 28.8, 29.1, 29.5, 30.2, 30.7, 31.1, 31.5, 32.1, 32.7, 33.1, 33.5, 34.1, 34.6, 35.3, 35.7, 36.0, 36.6, 37.2, 37.8, 38.2, 38.5, 39.2, 39.8, 40.4, 40.9, 41.3, 41.7, 42.3, 42.9, 43.6, 43.9, 44.0, 44.4, 45.0, 45.6, 46.3, 46.7, 47.1, 47.6, 48.2, 48.8, 49.4, 49.8, 50.2, 50.8, 51.4, 52.0, 52.5, 52.8, 53.3, 53.9, 54.6, 55.2, 55.5, 55.9, 56.5, 57.1, 57.7, 58.2, 58.5, 59.1, 59.7, 60.3, 60.9, 61.2, 61.6, 62.3, 62.8, 63.5, 63.9, 64.3, 64.8, 65.4, 66.0, 66.6, 67.0, 67.4, 68.0, 68.6, 69.2, 69.7, 70.0, 70.5, 71.1, 71.8, 72.4, 72.7, 73.1, 73.7, 74.3, 74.9, 75.4, 75.7, 76.3, 76.9, 77.5, 78.1, 78.4, 78.8, 79.5, 80.0, 80.7, 81.1, 81.5, 82.0, 82.6, 83.2, 83.8, 84.4, 85.1, 85.4, 85.8, 86.5, 87.0, 87.7, 88.3, 88.9, 89.5, 90.1, 90.7, 91.1, 91.5, 92.1, 92.6, 93.3, 93.9, 94.5, 95.1, 95.7, 96.3, 96.8, 97.2, 97.7, 98.3, 98.9, 99.5, 100.1, 100.7, 101.4, 101.9, 102.5, 102.9, 103.3, 103.9, 104.5, 105.1, 105.7, 106.3, 107.0, 107.6, 108.1, 108.5, 108.9, 109.5, 110.1, 110.8)+cms.vdouble(111.3, 112.0, 112.6, 113.2, 113.8, 114.2, 114.5, 115.1, 115.8, 116.4, 117.0, 117.3, 0.0, 0.4, 0.5, 0.6, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.6, 1.8, 1.9, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.5, 3.8, 4.0, 4.2, 4.5, 4.7, 5.0, 5.3, 5.6, 5.9, 6.2, 6.5, 6.9, 7.0, 7.2, 7.5, 7.8, 8.1, 8.5, 8.7, 9.1, 9.3, 9.6, 9.9, 10.3, 10.6, 10.9, 11.2, 11.5, 11.8, 12.1, 12.4, 12.8, 13.0, 13.3, 13.6, 13.9, 14.3, 14.7, 15.1, 15.5, 15.8, 16.3, 16.7, 17.0, 17.5, 17.8, 18.3, 18.7, 19.0, 19.5, 19.8, 20.2, 20.7, 21.1, 21.4, 22.0, 22.4, 22.7, 23.3, 23.7, 24.1, 24.5, 25.1, 25.4, 25.8, 26.4, 26.9, 27.2, 27.6, 28.2, 28.7, 29.0, 29.4, 30.0, 30.5, 31.0, 31.3, 31.8, 32.4, 32.9, 33.3, 33.6, 34.2, 34.8, 35.4, 35.7, 36.0, 36.6, 37.2, 37.7, 38.2, 38.6, 39.0, 39.5, 40.1, 40.7, 41.0, 41.1, 41.5, 42.1, 42.6, 43.2, 43.7, 44.0, 44.5, 45.1, 45.6, 46.2, 46.5, 46.9, 47.5, 48.0, 48.6, 49.0, 49.3, 49.8, 50.4, 51.0, 51.5, 51.9, 52.2, 52.8, 53.4, 53.9, 54.4, 54.7, 55.2, 55.8, 56.4, 56.9, 57.2, 57.6, 58.2, 58.7, 59.3, 59.7, 60.1, 60.5, 61.1, 61.7, 62.3, 62.6, 62.9, 63.5, 64.1, 64.7, 65.1, 65.4, 65.9, 66.5, 67.1, 67.6, 67.9, 68.3, 68.9, 69.4, 70.0, 70.4, 70.8, 71.3, 71.8, 72.4, 73.0, 73.3, 73.7, 74.3, 74.8, 75.4, 75.8, 76.1, 76.6, 77.2, 77.8, 78.3, 78.9, 79.5, 79.8, 80.2, 80.8, 81.3, 81.9, 82.5, 83.0, 83.6, 84.2, 84.8, 85.1, 85.5, 86.0, 86.6, 87.2, 87.8, 88.3, 88.9, 89.5, 90.0, 90.4, 90.8, 91.3, 91.8, 92.4, 93.0, 93.5, 94.1, 94.7, 95.3, 95.7, 96.1, 96.5, 97.1, 97.7, 98.3, 98.8, 99.4, 100.0, 100.5, 101.0, 101.4, 101.8, 102.3, 102.9)+cms.vdouble(103.5, 104.0, 104.6, 105.2, 105.8, 106.3, 106.7, 107.0, 107.6, 108.2, 108.8, 109.3, 109.6, 0.0, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.6, 1.8, 1.9, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.3, 3.5, 3.7, 3.9, 4.2, 4.4, 4.6, 4.9, 5.2, 5.5, 5.8, 6.1, 6.4, 6.5, 6.7, 7.0, 7.2, 7.6, 7.9, 8.1, 8.4, 8.7, 9.0, 9.2, 9.6, 9.9, 10.1, 10.4, 10.7, 11.0, 11.2, 11.6, 11.9, 12.1, 12.4, 12.7, 13.0, 13.3, 13.7, 14.1, 14.4, 14.7, 15.2, 15.6, 15.9, 16.3, 16.6, 17.0, 17.4, 17.7, 18.2, 18.5, 18.8, 19.3, 19.6, 20.0, 20.5, 20.9, 21.2, 21.7, 22.1, 22.5, 22.9, 23.4, 23.7, 24.1, 24.6, 25.1, 25.4, 25.7, 26.3, 26.8, 27.1, 27.4, 28.0, 28.5, 28.9, 29.2, 29.7, 30.2, 30.7, 31.1, 31.4, 31.9, 32.4, 32.9, 33.2, 33.5, 34.1, 34.6, 35.1, 35.6, 35.9, 36.3, 36.8, 37.4, 37.9, 38.2, 38.3, 38.6, 39.2, 39.7, 40.3, 40.7, 41.0, 41.4, 42.0, 42.5, 43.0, 43.3, 43.7, 44.2, 44.7, 45.3, 45.7, 46.0, 46.4, 47.0, 47.5, 48.0, 48.3, 48.7, 49.2, 49.7, 50.3, 50.7, 51.0, 51.4, 52.0, 52.5, 53.0, 53.3, 53.7, 54.2, 54.7, 55.3, 55.7, 56.0, 56.4, 57.0, 57.5, 58.0, 58.3, 58.7, 59.2, 59.7, 60.3, 60.7, 61.0, 61.4, 62.0, 62.5, 63.0, 63.3, 63.7, 64.2, 64.7, 65.2, 65.6, 65.9, 66.4, 66.9, 67.5, 68.0, 68.3, 68.6, 69.2, 69.7, 70.2, 70.6, 70.9, 71.4, 71.9, 72.5, 73.0, 73.5, 74.1, 74.4, 74.7, 75.3, 75.8, 76.3, 76.9, 77.4, 77.9, 78.5, 79.0, 79.3, 79.7, 80.2, 80.7, 81.2, 81.8, 82.3, 82.8, 83.4, 83.9, 84.3, 84.6, 85.1, 85.6, 86.1, 86.7, 87.2, 87.7, 88.3, 88.8, 89.2, 89.6, 90.0, 90.5, 91.0, 91.6, 92.1, 92.6, 93.2, 93.7, 94.2, 94.5, 94.9, 95.4)+cms.vdouble(95.9, 96.5, 96.9, 97.5, 98.0, 98.5, 99.1, 99.4, 99.7, 100.2, 100.8, 101.3, 101.8, 102.1, 0.0, 0.4, 0.5, 0.6, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5, 1.7, 1.8, 1.9, 2.1, 2.3, 2.5, 2.6, 2.8, 3.1, 3.3, 3.4, 3.6, 3.9, 4.1, 4.3, 4.6, 4.8, 5.2, 5.4, 5.7, 5.9, 6.0, 6.2, 6.5, 6.7, 7.1, 7.3, 7.6, 7.8, 8.1, 8.4, 8.6, 8.9, 9.2, 9.4, 9.7, 9.9, 10.2, 10.4, 10.8, 11.0, 11.3, 11.6, 11.8, 12.1, 12.4, 12.7, 13.1, 13.4, 13.7, 14.2, 14.5, 14.8, 15.2, 15.5, 15.8, 16.2, 16.5, 16.9, 17.2, 17.5, 18.0, 18.2, 18.6, 19.1, 19.4, 19.7, 20.1, 20.6, 20.9, 21.3, 21.7, 22.0, 22.4, 22.8, 23.3, 23.6, 23.9, 24.4, 24.9, 25.2, 25.5, 26.0, 26.5, 26.8, 27.1, 27.6, 28.0, 28.5, 28.9, 29.1, 29.6, 30.1, 30.6, 30.9, 31.2, 31.7, 32.2, 32.7, 33.1, 33.4, 33.8, 34.2, 34.8, 35.3, 35.5, 35.6, 35.9, 36.4, 36.9, 37.5, 37.8, 38.1, 38.5, 39.0, 39.5, 40.0, 40.3, 40.6, 41.1, 41.6, 42.1, 42.5, 42.7, 43.2, 43.7, 44.2, 44.6, 44.9, 45.2, 45.8, 46.2, 46.7, 47.1, 47.4, 47.8, 48.3, 48.8, 49.3, 49.6, 49.9, 50.4, 50.9, 51.4, 51.7, 52.0, 52.4, 53.0, 53.5, 53.9, 54.2, 54.5, 55.0, 55.5, 56.0, 56.4, 56.7, 57.1, 57.6, 58.1, 58.6, 58.8, 59.2, 59.7, 60.1, 60.7, 61.0, 61.3, 61.7, 62.2, 62.7, 63.2, 63.5, 63.8, 64.3, 64.8, 65.3, 65.7, 65.9, 66.4, 66.9, 67.4, 67.8, 68.4, 68.9, 69.1, 69.5, 70.0, 70.4, 71.0, 71.5, 71.9, 72.4, 73.0, 73.4, 73.7, 74.1, 74.5, 75.0, 75.5, 76.0, 76.5, 77.0, 77.5, 78.0, 78.3, 78.7, 79.1, 79.5, 80.1, 80.6, 81.0, 81.5, 82.1, 82.5, 82.9, 83.3, 83.6, 84.1, 84.6, 85.1, 85.6, 86.1, 86.6, 87.1, 87.5, 87.9, 88.2)+cms.vdouble(88.6, 89.2, 89.7, 90.1, 90.6, 91.1, 91.6, 92.1, 92.4, 92.7, 93.2, 93.7, 94.2, 94.7, 95.0, 0.0, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.9, 1.0, 1.1, 1.2, 1.4, 1.5, 1.6, 1.8, 1.9, 2.1, 2.3, 2.4, 2.6, 2.8, 3.1, 3.2, 3.4, 3.6, 3.8, 4.0, 4.3, 4.5, 4.8, 5.0, 5.3, 5.5, 5.6, 5.8, 6.0, 6.2, 6.5, 6.8, 7.0, 7.3, 7.5, 7.7, 8.0, 8.3, 8.5, 8.7, 9.0, 9.2, 9.5, 9.7, 10.0, 10.2, 10.5, 10.7, 10.9, 11.2, 11.5, 11.8, 12.1, 12.4, 12.7, 13.1, 13.4, 13.7, 14.1, 14.3, 14.7, 15.0, 15.3, 15.7, 15.9, 16.2, 16.7, 16.9, 17.2, 17.7, 18.0, 18.3, 18.7, 19.1, 19.4, 19.7, 20.1, 20.4, 20.8, 21.2, 21.6, 21.9, 22.2, 22.6, 23.1, 23.3, 23.6, 24.1, 24.5, 24.9, 25.2, 25.6, 26.0, 26.5, 26.8, 27.0, 27.5, 27.9, 28.4, 28.7, 28.9, 29.4, 29.9, 30.3, 30.7, 31.0, 31.3, 31.8, 32.2, 32.7, 33.0, 33.1, 33.3, 33.8, 34.3, 34.7, 35.1, 35.3, 35.7, 36.2, 36.7, 37.1, 37.4, 37.7, 38.1, 38.6, 39.0, 39.4, 39.7, 40.0, 40.5, 41.0, 41.4, 41.7, 42.0, 42.4, 42.9, 43.4, 43.7, 44.0, 44.3, 44.8, 45.3, 45.7, 46.0, 46.3, 46.8, 47.2, 47.7, 48.0, 48.3, 48.6, 49.1, 49.6, 50.0, 50.3, 50.6, 51.1, 51.5, 52.0, 52.3, 52.6, 53.0, 53.4, 53.9, 54.3, 54.6, 54.9, 55.4, 55.8, 56.3, 56.6, 56.9, 57.3, 57.7, 58.2, 58.6, 58.9, 59.2, 59.7, 60.1, 60.6, 60.9, 61.2, 61.6, 62.0, 62.5, 62.9, 63.4, 63.9, 64.1, 64.4, 64.9, 65.4, 65.8, 66.3, 66.7, 67.2, 67.7, 68.1, 68.4, 68.7, 69.1, 69.6, 70.0, 70.5, 71.0, 71.4, 71.9, 72.3, 72.7, 73.0, 73.4, 73.8, 74.3, 74.7, 75.2, 75.6, 76.1, 76.5, 76.9, 77.2, 77.6, 78.0, 78.5, 79.0, 79.4, 79.9, 80.3, 80.8, 81.2, 81.5)+cms.vdouble(81.8, 82.2, 82.7, 83.2, 83.6, 84.1, 84.6, 85.0, 85.5, 85.8, 86.0, 86.4, 86.9, 87.4, 87.8, 88.1, 0.0, 0.3, 0.4, 0.5, 0.6, 0.6, 0.7, 0.8, 0.9, 1.0, 1.0, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 2.0, 2.1, 2.2, 2.4, 2.6, 2.8, 3.0, 3.1, 3.3, 3.5, 3.7, 3.9, 4.1, 4.4, 4.6, 4.9, 5.1, 5.2, 5.3, 5.6, 5.8, 6.1, 6.3, 6.5, 6.7, 6.9, 7.2, 7.4, 7.7, 7.9, 8.1, 8.3, 8.5, 8.8, 9.0, 9.2, 9.5, 9.7, 9.9, 10.1, 10.4, 10.6, 10.9, 11.2, 11.5, 11.8, 12.2, 12.4, 12.7, 13.0, 13.3, 13.6, 13.9, 14.2, 14.5, 14.8, 15.0, 15.4, 15.7, 15.9, 16.4, 16.7, 16.9, 17.3, 17.7, 17.9, 18.3, 18.7, 18.9, 19.2, 19.6, 20.0, 20.3, 20.5, 21.0, 21.4, 21.6, 21.9, 22.3, 22.7, 23.0, 23.3, 23.7, 24.1, 24.5, 24.8, 25.0, 25.4, 25.9, 26.3, 26.6, 26.8, 27.2, 27.7, 28.1, 28.4, 28.7, 29.0, 29.4, 29.9, 30.3, 30.5, 30.6, 30.9, 31.3, 31.7, 32.2, 32.5, 32.7, 33.1, 33.5, 34.0, 34.4, 34.6, 34.9, 35.3, 35.7, 36.2, 36.5, 36.7, 37.1, 37.5, 38.0, 38.4, 38.6, 38.9, 39.3, 39.7, 40.1, 40.5, 40.7, 41.1, 41.5, 41.9, 42.3, 42.6, 42.9, 43.3, 43.7, 44.1, 44.5, 44.7, 45.0, 45.5, 45.9, 46.3, 46.6, 46.8, 47.3, 47.7, 48.1, 48.4, 48.7, 49.0, 49.5, 49.9, 50.3, 50.6, 50.8, 51.3, 51.7, 52.1, 52.4, 52.7, 53.0, 53.5, 53.9, 54.3, 54.5, 54.8, 55.3, 55.7, 56.1, 56.4, 56.7, 57.0, 57.4, 57.9, 58.3, 58.7, 59.2, 59.4, 59.7, 60.1, 60.5, 61.0, 61.4, 61.8, 62.2, 62.7, 63.1, 63.3, 63.6, 64.0, 64.4, 64.9, 65.3, 65.7, 66.1, 66.6, 67.0, 67.3, 67.6, 67.9, 68.3, 68.8, 69.2, 69.6, 70.0, 70.5, 70.9, 71.2, 71.5, 71.8, 72.2, 72.7, 73.1, 73.5, 74.0, 74.4, 74.8, 75.2)+cms.vdouble(75.5, 75.7, 76.1, 76.6, 77.0, 77.4, 77.9, 78.3, 78.7, 79.1, 79.4, 79.7, 80.1, 80.5, 80.9, 81.3, 81.6, 0.0, 0.3, 0.4, 0.4, 0.5, 0.6, 0.7, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.7, 1.8, 2.0, 2.1, 2.2, 2.4, 2.6, 2.7, 2.9, 3.1, 3.2, 3.4, 3.6, 3.8, 4.1, 4.3, 4.5, 4.7, 4.8, 4.9, 5.2, 5.3, 5.6, 5.8, 6.0, 6.2, 6.4, 6.6, 6.8, 7.1, 7.3, 7.5, 7.7, 7.9, 8.1, 8.3, 8.6, 8.8, 9.0, 9.2, 9.4, 9.6, 9.8, 10.1, 10.4, 10.7, 10.9, 11.2, 11.5, 11.7, 12.1, 12.3, 12.6, 12.9, 13.1, 13.4, 13.6, 13.9, 14.3, 14.5, 14.7, 15.1, 15.4, 15.6, 16.0, 16.3, 16.6, 16.9, 17.3, 17.5, 17.8, 18.1, 18.5, 18.7, 19.0, 19.4, 19.8, 20.0, 20.2, 20.6, 21.0, 21.3, 21.6, 21.9, 22.3, 22.7, 22.9, 23.1, 23.5, 23.9, 24.3, 24.5, 24.8, 25.2, 25.6, 26.0, 26.3, 26.5, 26.8, 27.2, 27.6, 28.0, 28.2, 28.3, 28.5, 28.9, 29.3, 29.7, 30.0, 30.3, 30.6, 31.0, 31.4, 31.8, 32.0, 32.3, 32.7, 33.0, 33.4, 33.7, 33.9, 34.3, 34.7, 35.1, 35.5, 35.7, 35.9, 36.3, 36.7, 37.1, 37.4, 37.6, 38.0, 38.4, 38.8, 39.1, 39.4, 39.6, 40.0, 40.4, 40.8, 41.1, 41.3, 41.7, 42.1, 42.5, 42.8, 43.1, 43.3, 43.7, 44.1, 44.5, 44.8, 45.0, 45.3, 45.7, 46.1, 46.5, 46.7, 47.0, 47.4, 47.8, 48.2, 48.5, 48.7, 49.0, 49.4, 49.8, 50.2, 50.4, 50.7, 51.1, 51.5, 51.9, 52.2, 52.4, 52.7, 53.1, 53.5, 53.9, 54.3, 54.7, 54.9, 55.2, 55.6, 56.0, 56.4, 56.8, 57.1, 57.5, 57.9, 58.3, 58.6, 58.8, 59.2, 59.6, 60.0, 60.4, 60.7, 61.2, 61.6, 61.9, 62.2, 62.5, 62.8, 63.2, 63.6, 64.0, 64.4, 64.8, 65.2, 65.5, 65.9, 66.1, 66.4, 66.8, 67.2, 67.6, 68.0, 68.4, 68.8, 69.2)+cms.vdouble(69.5, 69.8, 70.0, 70.4, 70.8, 71.2, 71.6, 72.0, 72.4, 72.8, 73.2, 73.4, 73.6, 74.0, 74.4, 74.8, 75.2, 75.4, 0.0, 0.3, 0.3, 0.4, 0.5, 0.5, 0.6, 0.7, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.7, 1.8, 1.9, 2.0, 2.2, 2.4, 2.5, 2.7, 2.9, 3.0, 3.2, 3.4, 3.5, 3.8, 3.9, 4.2, 4.4, 4.4, 4.6, 4.8, 4.9, 5.2, 5.4, 5.5, 5.8, 5.9, 6.1, 6.3, 6.5, 6.7, 6.9, 7.1, 7.3, 7.5, 7.7, 7.9, 8.1, 8.3, 8.5, 8.6, 8.8, 9.1, 9.3, 9.6, 9.8, 10.0, 10.4, 10.6, 10.8, 11.1, 11.3, 11.6, 11.9, 12.1, 12.4, 12.6, 12.8, 13.2, 13.4, 13.6, 14.0, 14.2, 14.4, 14.8, 15.1, 15.3, 15.6, 15.9, 16.2, 16.4, 16.7, 17.1, 17.3, 17.5, 17.9, 18.2, 18.4, 18.7, 19.1, 19.4, 19.7, 19.9, 20.2, 20.6, 20.9, 21.2, 21.4, 21.7, 22.1, 22.5, 22.7, 22.9, 23.2, 23.6, 24.0, 24.3, 24.5, 24.8, 25.1, 25.5, 25.9, 26.1, 26.1, 26.3, 26.7, 27.1, 27.5, 27.7, 27.9, 28.3, 28.6, 29.0, 29.3, 29.5, 29.8, 30.2, 30.5, 30.9, 31.1, 31.3, 31.7, 32.0, 32.4, 32.7, 32.9, 33.2, 33.6, 33.9, 34.3, 34.5, 34.8, 35.1, 35.4, 35.8, 36.1, 36.4, 36.6, 37.0, 37.3, 37.7, 38.0, 38.2, 38.5, 38.8, 39.2, 39.6, 39.8, 40.0, 40.4, 40.7, 41.1, 41.4, 41.6, 41.9, 42.2, 42.6, 43.0, 43.2, 43.4, 43.8, 44.1, 44.5, 44.8, 45.0, 45.3, 45.6, 46.0, 46.4, 46.6, 46.8, 47.2, 47.5, 47.9, 48.2, 48.4, 48.7, 49.0, 49.4, 49.8, 50.1, 50.5, 50.7, 51.0, 51.3, 51.7, 52.0, 52.4, 52.8, 53.1, 53.5, 53.8, 54.1, 54.3, 54.7, 55.0, 55.4, 55.8, 56.1, 56.5, 56.8, 57.2, 57.5, 57.7, 58.0, 58.3, 58.7, 59.1, 59.4, 59.8, 60.2, 60.5, 60.8, 61.1, 61.3, 61.7, 62.0, 62.4, 62.8, 63.1, 63.5)+cms.vdouble(63.9, 64.2, 64.4, 64.7, 65.0, 65.4, 65.8, 66.1, 66.5, 66.8, 67.2, 67.6, 67.8, 68.0, 68.3, 68.7, 69.1, 69.4, 69.6, 0.0, 0.3, 0.3, 0.4, 0.4, 0.5, 0.6, 0.6, 0.7, 0.8, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.7, 1.8, 1.9, 2.1, 2.2, 2.3, 2.4, 2.6, 2.8, 2.9, 3.1, 3.3, 3.5, 3.6, 3.8, 4.0, 4.1, 4.2, 4.4, 4.6, 4.8, 5.0, 5.1, 5.3, 5.5, 5.7, 5.8, 6.0, 6.2, 6.4, 6.6, 6.7, 6.9, 7.1, 7.3, 7.5, 7.6, 7.8, 8.0, 8.2, 8.4, 8.6, 8.9, 9.1, 9.3, 9.6, 9.8, 10.0, 10.3, 10.5, 10.7, 11.0, 11.1, 11.4, 11.6, 11.8, 12.1, 12.3, 12.6, 12.9, 13.1, 13.3, 13.6, 13.9, 14.1, 14.4, 14.7, 14.9, 15.1, 15.4, 15.8, 15.9, 16.2, 16.5, 16.8, 17.0, 17.2, 17.6, 17.9, 18.1, 18.4, 18.6, 19.0, 19.3, 19.5, 19.7, 20.0, 20.4, 20.7, 20.9, 21.1, 21.4, 21.8, 22.1, 22.4, 22.6, 22.9, 23.2, 23.5, 23.9, 24.0, 24.1, 24.3, 24.6, 25.0, 25.3, 25.6, 25.8, 26.1, 26.4, 26.7, 27.1, 27.2, 27.5, 27.8, 28.1, 28.5, 28.7, 28.9, 29.2, 29.5, 29.9, 30.2, 30.4, 30.6, 31.0, 31.3, 31.6, 31.9, 32.1, 32.3, 32.7, 33.0, 33.3, 33.5, 33.7, 34.1, 34.4, 34.8, 35.0, 35.2, 35.5, 35.8, 36.2, 36.5, 36.7, 36.9, 37.2, 37.5, 37.9, 38.1, 38.3, 38.6, 39.0, 39.3, 39.6, 39.8, 40.0, 40.4, 40.7, 41.0, 41.3, 41.5, 41.8, 42.1, 42.4, 42.8, 42.9, 43.2, 43.5, 43.8, 44.2, 44.4, 44.6, 44.9, 45.2, 45.6, 45.9, 46.2, 46.6, 46.8, 47.0, 47.3, 47.7, 48.0, 48.3, 48.7, 49.0, 49.4, 49.7, 49.9, 50.1, 50.4, 50.7, 51.1, 51.4, 51.7, 52.1, 52.4, 52.7, 53.0, 53.2, 53.5, 53.8, 54.2, 54.5, 54.8, 55.2, 55.5, 55.8, 56.1, 56.3, 56.6, 56.9, 57.2, 57.6, 57.9, 58.2)+cms.vdouble(58.6, 58.9, 59.2, 59.4, 59.6, 60.0, 60.3, 60.7, 61.0, 61.3, 61.7, 62.0, 62.3, 62.5, 62.7, 63.0, 63.4, 63.7, 64.0, 64.2, 0.0, 0.2, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.3, 1.4, 1.6, 1.8, 2.0, 2.1, 2.4, 2.5, 2.7, 2.8, 3.1, 3.4, 3.6, 3.7, 3.8, 4.0, 4.3, 4.6, 4.8, 5.0, 5.1, 5.4, 5.7, 5.9, 6.1, 6.3, 6.6, 6.9, 7.0, 7.2, 7.5, 7.8, 8.1, 8.5, 8.8, 9.1, 9.5, 9.8, 10.2, 10.5, 10.8, 11.1, 11.5, 11.9, 12.2, 12.7, 13.1, 13.5, 13.9, 14.3, 14.7, 15.1, 15.5, 15.9, 16.5, 16.8, 17.3, 17.7, 18.1, 18.7, 19.1, 19.4, 20.0, 20.5, 20.9, 21.4, 21.9, 22.1, 22.4, 22.9, 23.4, 23.7, 24.3, 24.8, 25.1, 25.7, 26.2, 26.6, 27.1, 27.6, 28.0, 28.5, 29.1, 29.4, 29.9, 30.4, 30.8, 31.3, 31.9, 32.2, 32.6, 33.3, 33.6, 34.0, 34.7, 35.0, 35.4, 36.1, 36.4, 36.8, 37.4, 37.8, 38.2, 38.8, 39.2, 39.6, 40.2, 40.7, 41.1, 41.6, 42.2, 42.7, 43.1, 43.6, 44.2, 44.8, 45.5, 45.9, 46.2, 46.9, 47.5, 48.1, 48.6, 48.9, 49.5, 50.1, 50.8, 51.4, 51.7, 52.2, 52.8, 53.4, 54.1, 54.4, 54.8, 55.5, 56.1, 56.7, 57.2, 57.6, 58.1, 58.8, 59.4, 60.0, 60.4, 60.8, 61.4, 62.0, 62.7, 63.3, 63.8, 64.2, 64.7, 65.3, 66.0, 66.6, 67.2, 67.9, 68.3, 68.6, 69.3, 69.9, 70.5, 71.2, 71.8, 72.4, 72.7, 73.2, 73.8, 74.5, 75.1, 75.7, 76.4, 76.8, 77.2, 77.8, 78.3, 79.0, 79.6, 80.2, 80.9, 81.5, 81.9, 82.3, 82.9, 83.5, 84.2, 84.8, 85.4, 86.1, 86.7, 87.4, 87.7, 88.1, 88.7, 89.4, 90.0, 90.6, 91.3, 91.9, 92.6, 93.2, 93.6, 93.9, 94.6, 95.2, 95.8, 96.5, 97.1, 97.8, 98.4, 99.0, 99.7, 100.1, 100.4, 101.0, 101.7, 102.3, 103.0, 103.6, 104.2, 104.9, 105.5, 106.1, 106.8)+cms.vdouble(107.2, 107.6, 108.2, 108.8, 109.4, 110.1, 110.7, 111.3, 112.0, 112.6, 113.2, 113.8, 114.3, 114.5, 114.8, 115.3, 116.0, 116.6, 117.2, 117.9, 118.2, 0.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.3, 2.4, 2.6, 2.9, 3.1, 3.3, 3.4, 3.5, 3.6, 3.9, 4.2, 4.4, 4.5, 4.7, 5.0, 5.2, 5.4, 5.5, 5.8, 6.0, 6.3, 6.4, 6.6, 6.9, 7.1, 7.4, 7.8, 8.0, 8.3, 8.7, 8.9, 9.3, 9.6, 9.9, 10.1, 10.5, 10.9, 11.2, 11.6, 11.9, 12.4, 12.7, 13.0, 13.4, 13.8, 14.1, 14.5, 15.0, 15.4, 15.8, 16.2, 16.5, 17.1, 17.4, 17.7, 18.3, 18.7, 19.1, 19.6, 20.0, 20.2, 20.4, 21.0, 21.4, 21.7, 22.2, 22.6, 23.0, 23.5, 24.0, 24.3, 24.8, 25.2, 25.5, 26.0, 26.6, 26.9, 27.3, 27.8, 28.1, 28.6, 29.1, 29.5, 29.8, 30.4, 30.7, 31.1, 31.7, 32.0, 32.4, 32.9, 33.3, 33.6, 34.2, 34.6, 34.9, 35.5, 35.8, 36.2, 36.7, 37.2, 37.5, 38.0, 38.5, 39.0, 39.4, 39.8, 40.4, 41.0, 41.5, 41.9, 42.2, 42.8, 43.4, 44.0, 44.4, 44.7, 45.2, 45.8, 46.4, 46.9, 47.2, 47.7, 48.2, 48.8, 49.4, 49.7, 50.1, 50.7, 51.3, 51.8, 52.3, 52.6, 53.1, 53.7, 54.3, 54.8, 55.2, 55.5, 56.1, 56.7, 57.3, 57.9, 58.3, 58.6, 59.1, 59.7, 60.3, 60.9, 61.4, 62.0, 62.4, 62.7, 63.3, 63.9, 64.5, 65.0, 65.6, 66.1, 66.5, 66.9, 67.5, 68.0, 68.6, 69.2, 69.8, 70.2, 70.5, 71.1, 71.6, 72.2, 72.7, 73.3, 73.9, 74.5, 74.9, 75.2, 75.8, 76.3, 76.9, 77.5, 78.1, 78.7, 79.2, 79.8, 80.1, 80.5, 81.1, 81.7, 82.2, 82.8, 83.4, 84.0, 84.6, 85.1, 85.5, 85.8, 86.4, 87.0, 87.6, 88.2, 88.7, 89.3, 89.9, 90.5, 91.1, 91.4, 91.7, 92.3, 92.9, 93.5, 94.1, 94.6, 95.2, 95.8, 96.4, 97.0)+cms.vdouble(97.6, 97.9, 98.3, 98.8, 99.4, 100.0, 100.6, 101.1, 101.7, 102.3, 102.9, 103.5, 104.0, 104.4, 104.6, 104.9, 105.4, 105.9, 106.5, 107.1, 107.7, 108.0, 0.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.0, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.1, 2.2, 2.3, 2.6, 2.8, 3.0, 3.1, 3.1, 3.3, 3.5, 3.8, 4.0, 4.1, 4.2, 4.5, 4.7, 4.9, 5.0, 5.2, 5.4, 5.7, 5.8, 6.0, 6.2, 6.4, 6.7, 7.0, 7.2, 7.5, 7.8, 8.1, 8.4, 8.6, 8.9, 9.2, 9.5, 9.8, 10.1, 10.4, 10.8, 11.2, 11.4, 11.8, 12.1, 12.5, 12.8, 13.1, 13.6, 13.9, 14.3, 14.6, 14.9, 15.4, 15.7, 16.0, 16.5, 16.9, 17.2, 17.7, 18.1, 18.2, 18.4, 18.9, 19.3, 19.6, 20.1, 20.4, 20.7, 21.2, 21.6, 21.9, 22.4, 22.8, 23.1, 23.5, 24.0, 24.3, 24.6, 25.1, 25.4, 25.8, 26.3, 26.6, 26.9, 27.5, 27.7, 28.1, 28.6, 28.9, 29.2, 29.7, 30.0, 30.4, 30.9, 31.2, 31.6, 32.0, 32.4, 32.7, 33.2, 33.6, 33.9, 34.3, 34.8, 35.2, 35.6, 35.9, 36.5, 37.0, 37.5, 37.8, 38.1, 38.7, 39.2, 39.7, 40.1, 40.4, 40.8, 41.4, 41.9, 42.4, 42.7, 43.0, 43.6, 44.1, 44.6, 44.9, 45.2, 45.8, 46.3, 46.8, 47.2, 47.5, 47.9, 48.5, 49.0, 49.5, 49.8, 50.1, 50.7, 51.2, 51.7, 52.2, 52.6, 53.0, 53.4, 53.9, 54.4, 55.0, 55.5, 56.0, 56.3, 56.6, 57.1, 57.7, 58.2, 58.7, 59.2, 59.7, 60.0, 60.4, 60.9, 61.4, 62.0, 62.5, 63.0, 63.3, 63.7, 64.2, 64.6, 65.2, 65.7, 66.2, 66.7, 67.3, 67.6, 67.9, 68.4, 68.9, 69.4, 70.0, 70.5, 71.0, 71.5, 72.1, 72.4, 72.7, 73.2, 73.7, 74.3, 74.8, 75.3, 75.8, 76.4, 76.9, 77.2, 77.5, 78.0, 78.5, 79.1, 79.6, 80.1, 80.6, 81.2, 81.7, 82.2, 82.6, 82.8, 83.4, 83.9, 84.4, 84.9, 85.5, 86.0, 86.5, 87.0)+cms.vdouble(87.6, 88.1, 88.4, 88.7, 89.2, 89.7, 90.3, 90.8, 91.3, 91.8, 92.4, 92.9, 93.4, 93.9, 94.3, 94.5, 94.7, 95.1, 95.7, 96.2, 96.7, 97.2, 97.5, 0.0, 0.2, 0.3, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.8, 0.9, 1.1, 1.2, 1.3, 1.4, 1.6, 1.7, 1.9, 2.0, 2.1, 2.3, 2.5, 2.6, 2.7, 2.8, 2.9, 3.1, 3.3, 3.5, 3.6, 3.8, 4.0, 4.2, 4.3, 4.5, 4.6, 4.8, 5.0, 5.2, 5.3, 5.5, 5.7, 5.9, 6.2, 6.4, 6.7, 7.0, 7.2, 7.5, 7.7, 7.9, 8.1, 8.4, 8.7, 9.0, 9.3, 9.6, 9.9, 10.2, 10.5, 10.8, 11.1, 11.4, 11.7, 12.1, 12.3, 12.7, 13.0, 13.3, 13.7, 14.0, 14.2, 14.7, 15.1, 15.3, 15.7, 16.1, 16.2, 16.4, 16.8, 17.2, 17.4, 17.9, 18.2, 18.4, 18.9, 19.2, 19.5, 19.9, 20.3, 20.5, 20.9, 21.3, 21.6, 21.9, 22.3, 22.6, 22.9, 23.4, 23.7, 24.0, 24.4, 24.7, 25.0, 25.4, 25.7, 26.0, 26.5, 26.7, 27.0, 27.5, 27.8, 28.1, 28.5, 28.8, 29.1, 29.5, 29.8, 30.1, 30.5, 31.0, 31.3, 31.6, 32.0, 32.4, 32.9, 33.4, 33.7, 33.9, 34.4, 34.9, 35.3, 35.7, 35.9, 36.3, 36.8, 37.3, 37.7, 37.9, 38.3, 38.8, 39.2, 39.7, 39.9, 40.2, 40.7, 41.2, 41.6, 42.0, 42.3, 42.7, 43.1, 43.6, 44.0, 44.3, 44.6, 45.1, 45.5, 46.0, 46.5, 46.8, 47.1, 47.5, 48.0, 48.4, 48.9, 49.4, 49.8, 50.1, 50.4, 50.8, 51.3, 51.8, 52.2, 52.7, 53.1, 53.4, 53.7, 54.2, 54.7, 55.1, 55.6, 56.1, 56.3, 56.6, 57.1, 57.5, 58.0, 58.4, 58.9, 59.4, 59.8, 60.1, 60.4, 60.8, 61.3, 61.8, 62.2, 62.7, 63.2, 63.6, 64.1, 64.4, 64.7, 65.1, 65.6, 66.1, 66.5, 67.0, 67.5, 67.9, 68.4, 68.7, 68.9, 69.4, 69.9, 70.3, 70.8, 71.3, 71.7, 72.2, 72.7, 73.1, 73.4, 73.7, 74.2, 74.6, 75.1, 75.6, 76.0, 76.5, 77.0)+cms.vdouble(77.4, 77.9, 78.4, 78.7, 78.9, 79.4, 79.8, 80.3, 80.8, 81.2, 81.7, 82.2, 82.6, 83.1, 83.5, 83.9, 84.0, 84.2, 84.6, 85.1, 85.6, 86.0, 86.5, 86.7, 0.0, 0.1, 0.2, 0.3, 0.4, 0.4, 0.5, 0.6, 0.7, 0.7, 0.8, 0.9, 1.0, 1.1, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 2.0, 2.2, 2.3, 2.4, 2.4, 2.6, 2.7, 2.9, 3.1, 3.2, 3.3, 3.5, 3.7, 3.8, 3.9, 4.0, 4.2, 4.4, 4.5, 4.6, 4.8, 5.0, 5.2, 5.4, 5.6, 5.8, 6.1, 6.3, 6.5, 6.7, 6.9, 7.1, 7.4, 7.6, 7.8, 8.1, 8.4, 8.7, 8.9, 9.1, 9.4, 9.7, 9.9, 10.2, 10.5, 10.8, 11.1, 11.4, 11.6, 12.0, 12.2, 12.4, 12.8, 13.1, 13.4, 13.7, 14.0, 14.1, 14.3, 14.7, 15.0, 15.2, 15.6, 15.9, 16.1, 16.5, 16.8, 17.0, 17.4, 17.7, 17.9, 18.2, 18.6, 18.8, 19.1, 19.5, 19.7, 20.0, 20.4, 20.7, 20.9, 21.3, 21.5, 21.8, 22.2, 22.4, 22.7, 23.1, 23.3, 23.6, 24.0, 24.2, 24.5, 24.9, 25.1, 25.4, 25.8, 26.1, 26.3, 26.6, 27.0, 27.4, 27.6, 27.9, 28.3, 28.7, 29.1, 29.4, 29.6, 30.0, 30.4, 30.8, 31.1, 31.3, 31.7, 32.1, 32.5, 32.9, 33.1, 33.4, 33.8, 34.2, 34.6, 34.9, 35.1, 35.5, 35.9, 36.3, 36.6, 36.9, 37.2, 37.6, 38.0, 38.4, 38.7, 38.9, 39.3, 39.7, 40.2, 40.6, 40.9, 41.1, 41.5, 41.9, 42.3, 42.7, 43.1, 43.5, 43.7, 44.0, 44.4, 44.8, 45.2, 45.6, 46.0, 46.4, 46.6, 46.9, 47.3, 47.7, 48.1, 48.5, 48.9, 49.2, 49.4, 49.8, 50.2, 50.6, 51.0, 51.4, 51.8, 52.2, 52.5, 52.7, 53.1, 53.5, 53.9, 54.3, 54.7, 55.1, 55.6, 56.0, 56.2, 56.4, 56.8, 57.3, 57.7, 58.1, 58.5, 58.9, 59.3, 59.7, 60.0, 60.2, 60.6, 61.0, 61.4, 61.8, 62.2, 62.6, 63.0, 63.4, 63.8, 64.1, 64.3, 64.7, 65.1, 65.5, 66.0, 66.4, 66.8)+cms.vdouble(67.2, 67.6, 68.0, 68.4, 68.7, 68.9, 69.3, 69.7, 70.1, 70.5, 70.9, 71.3, 71.7, 72.1, 72.5, 72.9, 73.2, 73.4, 73.5, 73.9, 74.3, 74.7, 75.1, 75.5, 75.7, 0.0, 0.1, 0.2, 0.3, 0.3, 0.4, 0.4, 0.5, 0.6, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.4, 1.5, 1.7, 1.9, 2.0, 2.0, 2.1, 2.2, 2.3, 2.5, 2.6, 2.7, 2.8, 3.0, 3.1, 3.2, 3.3, 3.4, 3.6, 3.7, 3.8, 3.9, 4.1, 4.3, 4.4, 4.6, 4.8, 5.0, 5.2, 5.3, 5.5, 5.7, 5.9, 6.0, 6.3, 6.5, 6.7, 6.9, 7.1, 7.4, 7.6, 7.8, 8.0, 8.3, 8.4, 8.7, 9.0, 9.2, 9.4, 9.7, 9.9, 10.2, 10.4, 10.6, 10.9, 11.2, 11.4, 11.7, 11.9, 12.0, 12.2, 12.5, 12.8, 13.0, 13.3, 13.5, 13.7, 14.0, 14.3, 14.5, 14.8, 15.1, 15.3, 15.5, 15.8, 16.0, 16.3, 16.6, 16.8, 17.0, 17.4, 17.6, 17.8, 18.1, 18.3, 18.6, 18.9, 19.1, 19.3, 19.7, 19.9, 20.1, 20.4, 20.6, 20.9, 21.2, 21.4, 21.6, 21.9, 22.2, 22.4, 22.7, 23.0, 23.3, 23.5, 23.8, 24.1, 24.5, 24.8, 25.0, 25.2, 25.6, 25.9, 26.2, 26.5, 26.7, 27.0, 27.3, 27.7, 28.0, 28.2, 28.5, 28.8, 29.1, 29.5, 29.7, 29.9, 30.2, 30.6, 30.9, 31.2, 31.4, 31.7, 32.0, 32.4, 32.7, 32.9, 33.1, 33.5, 33.8, 34.2, 34.5, 34.8, 35.0, 35.3, 35.6, 36.0, 36.3, 36.7, 37.0, 37.2, 37.4, 37.8, 38.1, 38.5, 38.8, 39.2, 39.5, 39.7, 39.9, 40.3, 40.6, 41.0, 41.3, 41.7, 41.9, 42.1, 42.4, 42.7, 43.1, 43.4, 43.8, 44.1, 44.5, 44.7, 44.9, 45.2, 45.6, 45.9, 46.3, 46.6, 46.9, 47.3, 47.6, 47.8, 48.1, 48.4, 48.7, 49.1, 49.4, 49.8, 50.1, 50.5, 50.8, 51.0, 51.2, 51.6, 51.9, 52.3, 52.6, 53.0, 53.3, 53.7, 54.0, 54.4, 54.6, 54.8, 55.1, 55.5, 55.8, 56.1, 56.5)+cms.vdouble(56.8, 57.2, 57.5, 57.9, 58.2, 58.4, 58.7, 59.0, 59.3, 59.7, 60.0, 60.4, 60.7, 61.1, 61.4, 61.8, 62.1, 62.3, 62.5, 62.6, 62.9, 63.2, 63.6, 63.9, 64.3, 64.5, 0.0, 0.1, 0.3, 0.4, 0.5, 0.7, 0.8, 0.9, 1.1, 1.2, 1.3, 1.5, 1.6, 1.7, 1.9, 2.0, 2.1, 2.3, 2.4, 2.5, 2.7, 2.8, 2.9, 3.1, 3.2, 3.4, 3.6, 3.8, 4.1, 4.4, 4.6, 4.8, 5.0, 5.2, 5.6, 6.0, 6.2, 6.4, 6.8, 7.2, 7.4, 7.8, 8.2, 8.5, 9.0, 9.3, 9.8, 10.2, 10.3, 10.6, 11.1, 11.4, 11.8, 12.2, 12.5, 13.0, 13.3, 13.8, 14.2, 14.5, 15.0, 15.3, 15.7, 16.1, 16.5, 17.0, 17.3, 17.8, 18.1, 18.5, 19.0, 19.4, 19.8, 20.3, 20.9, 21.4, 22.0, 22.5, 22.9, 23.5, 24.0, 24.6, 25.1, 25.5, 26.2, 26.6, 27.1, 27.7, 28.1, 28.8, 29.3, 29.8, 30.5, 31.2, 31.7, 32.2, 32.9, 33.4, 33.9, 34.6, 35.3, 35.7, 36.3, 37.1, 37.7, 38.1, 38.7, 39.5, 40.2, 40.7, 41.2, 41.9, 42.7, 43.2, 43.6, 44.4, 45.2, 45.9, 46.4, 46.8, 47.6, 48.4, 49.1, 49.6, 50.1, 50.8, 51.5, 52.3, 52.9, 53.1, 53.5, 54.1, 54.9, 55.7, 56.2, 56.7, 57.4, 58.1, 58.9, 59.5, 60.0, 60.6, 61.3, 62.1, 62.8, 63.3, 63.8, 64.5, 65.3, 66.1, 66.5, 67.0, 67.7, 68.5, 69.4, 69.8, 70.2, 71.0, 71.8, 72.5, 73.0, 73.4, 74.2, 75.0, 75.7, 76.3, 76.7, 77.4, 78.2, 78.9, 79.5, 80.0, 80.6, 81.4, 82.2, 82.8, 83.3, 83.8, 84.6, 85.4, 86.1, 86.6, 87.0, 87.8, 88.6, 89.3, 89.8, 90.3, 91.1, 91.8, 92.5, 93.1, 93.5, 94.2, 94.9, 95.8, 96.4, 96.8, 97.4, 98.2, 99.0, 99.8, 100.5, 101.2, 101.7, 102.2, 103.0, 103.7, 104.5, 105.3, 106.1, 106.8, 107.5, 108.1, 108.6, 109.3, 110.0, 110.8, 111.6, 112.3, 113.0, 113.8, 114.6, 115.1, 115.5, 116.3, 117.1, 117.9, 118.6)+cms.vdouble(119.3, 120.1, 120.9, 121.5, 121.9, 122.6, 123.4, 124.2, 124.9, 125.6, 126.4, 127.2, 128.0, 128.4, 128.9, 129.7, 130.5, 131.2, 131.9, 132.7, 133.5, 134.2, 134.8, 135.3, 136.0, 136.7, 137.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 3.9, 4.1, 4.4, 4.7, 4.8, 5.0, 5.3, 5.6, 5.8, 6.1, 6.4, 6.6, 7.0, 7.3, 7.6, 8.0, 8.1, 8.3, 8.6, 8.9, 9.2, 9.5, 9.8, 10.1, 10.4, 10.8, 11.1, 11.4, 11.7, 12.0, 12.3, 12.6, 12.9, 13.2, 13.5, 13.9, 14.1, 14.4, 14.8, 15.2, 15.5, 15.8, 16.3, 16.7, 17.2, 17.6, 17.9, 18.4, 18.7, 19.2, 19.6, 19.9, 20.5, 20.8, 21.2, 21.6, 22.0, 22.5, 22.9, 23.3, 23.8, 24.4, 24.7, 25.1, 25.7, 26.1, 26.5, 27.0, 27.6, 27.9, 28.3, 28.9, 29.4, 29.8, 30.2, 30.8, 31.4, 31.7, 32.2, 32.7, 33.3, 33.7, 34.1, 34.7, 35.3, 35.8, 36.2, 36.6, 37.2, 37.8, 38.3, 38.7, 39.1, 39.6, 40.2, 40.8, 41.3, 41.4, 41.7, 42.3, 42.8, 43.5, 43.9, 44.2, 44.8, 45.3, 46.0, 46.4, 46.8, 47.3, 47.9, 48.5, 49.0, 49.4, 49.8, 50.4, 51.0, 51.6, 51.9, 52.3, 52.9, 53.5, 54.1, 54.5, 54.8, 55.4, 56.0, 56.6, 57.0, 57.3, 57.9, 58.5, 59.1, 59.5, 59.9, 60.4, 61.0, 61.6, 62.1, 62.5, 62.9, 63.5, 64.1, 64.6, 65.0, 65.4, 66.1, 66.6, 67.2, 67.6, 67.9, 68.6, 69.1, 69.7, 70.1, 70.5, 71.1, 71.7, 72.2, 72.7, 73.0, 73.5, 74.1, 74.7, 75.2, 75.6, 76.1, 76.6, 77.3, 77.9, 78.5, 79.0, 79.3, 79.8, 80.4, 81.0, 81.5, 82.2, 82.8, 83.4, 83.9, 84.4, 84.7, 85.3, 85.9, 86.5, 87.1, 87.7, 88.2, 88.9, 89.4, 89.8, 90.2, 90.7, 91.4, 92.0)+cms.vdouble(92.6, 93.2, 93.8, 94.4, 94.8, 95.1, 95.7, 96.3, 96.9, 97.5, 98.1, 98.7, 99.3, 99.9, 100.2, 100.6, 101.2, 101.8, 102.4, 103.0, 103.6, 104.2, 104.8, 105.2, 105.6, 106.1, 106.7, 107.0, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 25.0, 25.5, 26.0, 26.5, 27.0, 27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0, 31.5, 32.0, 32.5, 33.0, 33.5, 34.0, 34.5, 35.0, 35.5, 36.0, 36.5, 37.0, 37.5, 38.0, 38.5, 39.0, 39.5, 40.0, 40.5, 41.0, 41.5, 42.0, 42.5, 43.0, 43.5, 44.0, 44.5, 45.0, 45.5, 46.0, 46.5, 47.0, 47.5, 48.0, 48.5, 49.0, 49.5, 50.0, 50.5, 51.0, 51.5, 52.0, 52.5, 53.0, 53.5, 54.0, 54.5, 55.0, 55.5, 56.0, 56.5, 57.0, 57.5, 58.0, 58.5, 59.0, 59.5, 60.0, 60.5, 61.0, 61.5, 62.0, 62.5, 63.0, 63.5, 64.0, 64.5, 65.0, 65.5, 66.0, 66.5, 67.0, 67.5, 68.0, 68.5, 69.0, 69.5, 70.0, 70.5, 71.0, 71.5, 72.0, 72.5, 73.0, 73.5, 74.0, 74.5, 75.0, 75.5, 76.0, 76.5, 77.0, 77.5, 78.0, 78.5, 79.0, 79.5, 80.0, 80.5, 81.0, 81.5, 82.0, 82.5, 83.0, 83.5, 84.0, 84.5, 85.0, 85.5, 86.0, 86.5, 87.0, 87.5, 88.0, 88.5, 89.0, 89.5, 90.0, 90.5, 91.0, 91.5, 92.0, 92.5, 93.0, 93.5, 94.0, 94.5, 95.0, 95.5, 96.0, 96.5, 97.0, 97.5, 98.0, 98.5, 99.0, 99.5, 100.0, 100.5, 101.0, 101.5, 102.0, 102.5, 103.0, 103.5, 104.0, 104.5, 105.0, 105.5, 106.0, 106.5, 107.0, 107.5, 108.0, 108.5, 109.0, 109.5, 110.0, 110.5, 111.0, 111.5, 112.0, 112.5, 113.0)+cms.vdouble(113.5, 114.0, 114.5, 115.0, 115.5, 116.0, 116.5, 117.0, 117.5, 118.0, 118.5, 119.0, 119.5, 120.0, 120.5, 121.0, 121.5, 122.0, 122.5, 123.0, 123.5, 124.0, 124.5, 125.0, 125.5, 126.0, 126.5, 127.0, 127.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 25.0, 25.5, 26.0, 26.5, 27.0, 27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0, 31.5, 32.0, 32.5, 33.0, 33.5, 34.0, 34.5, 35.0, 35.5, 36.0, 36.5, 37.0, 37.5, 38.0, 38.5, 39.0, 39.5, 40.0, 40.5, 41.0, 41.5, 42.0, 42.5, 43.0, 43.5, 44.0, 44.5, 45.0, 45.5, 46.0, 46.5, 47.0, 47.5, 48.0, 48.5, 49.0, 49.5, 50.0, 50.5, 51.0, 51.5, 52.0, 52.5, 53.0, 53.5, 54.0, 54.5, 55.0, 55.5, 56.0, 56.5, 57.0, 57.5, 58.0, 58.5, 59.0, 59.5, 60.0, 60.5, 61.0, 61.5, 62.0, 62.5, 63.0, 63.5, 64.0, 64.5, 65.0, 65.5, 66.0, 66.5, 67.0, 67.5, 68.0, 68.5, 69.0, 69.5, 70.0, 70.5, 71.0, 71.5, 72.0, 72.5, 73.0, 73.5, 74.0, 74.5, 75.0, 75.5, 76.0, 76.5, 77.0, 77.5, 78.0, 78.5, 79.0, 79.5, 80.0, 80.5, 81.0, 81.5, 82.0, 82.5, 83.0, 83.5, 84.0, 84.5, 85.0, 85.5, 86.0, 86.5, 87.0, 87.5, 88.0, 88.5, 89.0, 89.5, 90.0, 90.5, 91.0, 91.5, 92.0, 92.5, 93.0, 93.5, 94.0, 94.5, 95.0, 95.5, 96.0, 96.5, 97.0, 97.5, 98.0, 98.5, 99.0, 99.5, 100.0, 100.5, 101.0, 101.5, 102.0, 102.5, 103.0, 103.5, 104.0, 104.5, 105.0, 105.5, 106.0, 106.5, 107.0, 107.5, 108.0, 108.5, 109.0, 109.5, 110.0, 110.5, 111.0, 111.5, 112.0, 112.5)+cms.vdouble(113.0, 113.5, 114.0, 114.5, 115.0, 115.5, 116.0, 116.5, 117.0, 117.5, 118.0, 118.5, 119.0, 119.5, 120.0, 120.5, 121.0, 121.5, 122.0, 122.5, 123.0, 123.5, 124.0, 124.5, 125.0, 125.5, 126.0, 126.5, 127.0, 127.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 25.0, 25.5, 26.0, 26.5, 27.0, 27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0, 31.5, 32.0, 32.5, 33.0, 33.5, 34.0, 34.5, 35.0, 35.5, 36.0, 36.5, 37.0, 37.5, 38.0, 38.5, 39.0, 39.5, 40.0, 40.5, 41.0, 41.5, 42.0, 42.5, 43.0, 43.5, 44.0, 44.5, 45.0, 45.5, 46.0, 46.5, 47.0, 47.5, 48.0, 48.5, 49.0, 49.5, 50.0, 50.5, 51.0, 51.5, 52.0, 52.5, 53.0, 53.5, 54.0, 54.5, 55.0, 55.5, 56.0, 56.5, 57.0, 57.5, 58.0, 58.5, 59.0, 59.5, 60.0, 60.5, 61.0, 61.5, 62.0, 62.5, 63.0, 63.5, 64.0, 64.5, 65.0, 65.5, 66.0, 66.5, 67.0, 67.5, 68.0, 68.5, 69.0, 69.5, 70.0, 70.5, 71.0, 71.5, 72.0, 72.5, 73.0, 73.5, 74.0, 74.5, 75.0, 75.5, 76.0, 76.5, 77.0, 77.5, 78.0, 78.5, 79.0, 79.5, 80.0, 80.5, 81.0, 81.5, 82.0, 82.5, 83.0, 83.5, 84.0, 84.5, 85.0, 85.5, 86.0, 86.5, 87.0, 87.5, 88.0, 88.5, 89.0, 89.5, 90.0, 90.5, 91.0, 91.5, 92.0, 92.5, 93.0, 93.5, 94.0, 94.5, 95.0, 95.5, 96.0, 96.5, 97.0, 97.5, 98.0, 98.5, 99.0, 99.5, 100.0, 100.5, 101.0, 101.5, 102.0, 102.5, 103.0, 103.5, 104.0, 104.5, 105.0, 105.5, 106.0, 106.5, 107.0, 107.5, 108.0, 108.5, 109.0, 109.5, 110.0, 110.5, 111.0, 111.5, 112.0)+cms.vdouble(112.5, 113.0, 113.5, 114.0, 114.5, 115.0, 115.5, 116.0, 116.5, 117.0, 117.5, 118.0, 118.5, 119.0, 119.5, 120.0, 120.5, 121.0, 121.5, 122.0, 122.5, 123.0, 123.5, 124.0, 124.5, 125.0, 125.5, 126.0, 126.5, 127.0, 127.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 25.0, 25.5, 26.0, 26.5, 27.0, 27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0, 31.5, 32.0, 32.5, 33.0, 33.5, 34.0, 34.5, 35.0, 35.5, 36.0, 36.5, 37.0, 37.5, 38.0, 38.5, 39.0, 39.5, 40.0, 40.5, 41.0, 41.5, 42.0, 42.5, 43.0, 43.5, 44.0, 44.5, 45.0, 45.5, 46.0, 46.5, 47.0, 47.5, 48.0, 48.5, 49.0, 49.5, 50.0, 50.5, 51.0, 51.5, 52.0, 52.5, 53.0, 53.5, 54.0, 54.5, 55.0, 55.5, 56.0, 56.5, 57.0, 57.5, 58.0, 58.5, 59.0, 59.5, 60.0, 60.5, 61.0, 61.5, 62.0, 62.5, 63.0, 63.5, 64.0, 64.5, 65.0, 65.5, 66.0, 66.5, 67.0, 67.5, 68.0, 68.5, 69.0, 69.5, 70.0, 70.5, 71.0, 71.5, 72.0, 72.5, 73.0, 73.5, 74.0, 74.5, 75.0, 75.5, 76.0, 76.5, 77.0, 77.5, 78.0, 78.5, 79.0, 79.5, 80.0, 80.5, 81.0, 81.5, 82.0, 82.5, 83.0, 83.5, 84.0, 84.5, 85.0, 85.5, 86.0, 86.5, 87.0, 87.5, 88.0, 88.5, 89.0, 89.5, 90.0, 90.5, 91.0, 91.5, 92.0, 92.5, 93.0, 93.5, 94.0, 94.5, 95.0, 95.5, 96.0, 96.5, 97.0, 97.5, 98.0, 98.5, 99.0, 99.5, 100.0, 100.5, 101.0, 101.5, 102.0, 102.5, 103.0, 103.5, 104.0, 104.5, 105.0, 105.5, 106.0, 106.5, 107.0, 107.5, 108.0, 108.5, 109.0, 109.5, 110.0, 110.5, 111.0, 111.5)+cms.vdouble(112.0, 112.5, 113.0, 113.5, 114.0, 114.5, 115.0, 115.5, 116.0, 116.5, 117.0, 117.5, 118.0, 118.5, 119.0, 119.5, 120.0, 120.5, 121.0, 121.5, 122.0, 122.5, 123.0, 123.5, 124.0, 124.5, 125.0, 125.5, 126.0, 126.5, 127.0, 127.5)),
    L1EcalEtThresholdsNegativeEta = (cms.vdouble(0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625)+cms.vdouble(119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375)+cms.vdouble(119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125)+cms.vdouble(118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625)+cms.vdouble(118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875)+cms.vdouble(117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875)+cms.vdouble(117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25)+cms.vdouble(116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125)+cms.vdouble(116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125)+cms.vdouble(115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375)+cms.vdouble(115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375)+cms.vdouble(114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625)+cms.vdouble(114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375)+cms.vdouble(113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875)+cms.vdouble(113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5)+cms.vdouble(112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125)+cms.vdouble(112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625)+cms.vdouble(112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375)+cms.vdouble(111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625)+cms.vdouble(111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625)+cms.vdouble(110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875)+cms.vdouble(110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875)+cms.vdouble(109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75)+cms.vdouble(109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125)+cms.vdouble(108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125)+cms.vdouble(108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375)+cms.vdouble(107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875)+cms.vdouble(107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625)+cms.vdouble(106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125)),
    L1EcalEtThresholdsPositiveEta = (cms.vdouble(0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625)+cms.vdouble(119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375)+cms.vdouble(119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125)+cms.vdouble(118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625)+cms.vdouble(118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875)+cms.vdouble(117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875)+cms.vdouble(117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25)+cms.vdouble(116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125)+cms.vdouble(116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125)+cms.vdouble(115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375)+cms.vdouble(115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375)+cms.vdouble(114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625)+cms.vdouble(114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375)+cms.vdouble(113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875)+cms.vdouble(113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5)+cms.vdouble(112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125)+cms.vdouble(112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625)+cms.vdouble(112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375)+cms.vdouble(111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625)+cms.vdouble(111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625)+cms.vdouble(110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875)+cms.vdouble(110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875)+cms.vdouble(109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75)+cms.vdouble(109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125)+cms.vdouble(108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125)+cms.vdouble(108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375)+cms.vdouble(107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875)+cms.vdouble(107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625)+cms.vdouble(106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125))
)


process.l1RPCHwConfig = cms.ESProducer("RPCTriggerHwConfig",
    disableCrates = cms.vint32(),
    enableTowers = cms.vint32(),
    enableCrates = cms.vint32(),
    disableAll = cms.bool(False),
    lastBX = cms.int32(0),
    firstBX = cms.int32(0),
    disableTowers = cms.vint32()
)


process.TrackerDigiGeometryESModule = cms.ESProducer("TrackerDigiGeometryESModule",
    appendToDataLabel = cms.string(''),
    fromDDD = cms.bool(True),
    applyAlignment = cms.bool(True),
    alignmentsLabel = cms.string('')
)


process.ecalDetIdAssociator = cms.ESProducer("DetIdAssociatorESProducer",
    ComponentName = cms.string('EcalDetIdAssociator'),
    etaBinSize = cms.double(0.02),
    nEta = cms.int32(300),
    nPhi = cms.int32(360)
)


process.muonDetIdAssociator = cms.ESProducer("DetIdAssociatorESProducer",
    ComponentName = cms.string('MuonDetIdAssociator'),
    etaBinSize = cms.double(0.125),
    nEta = cms.int32(48),
    nPhi = cms.int32(48)
)


process.EcalBarrelGeometryEP = cms.ESProducer("EcalBarrelGeometryEP",
    applyAlignment = cms.untracked.bool(False)
)


process.l1GtTriggerMaskVetoAlgoTrig = cms.ESProducer("L1GtTriggerMaskVetoAlgoTrigTrivialProducer",
    TriggerMask = cms.vuint32(0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0)
)


process.TransientTrackBuilderESProducer = cms.ESProducer("TransientTrackBuilderESProducer",
    ComponentName = cms.string('TransientTrackBuilder')
)


process.l1GtTriggerMaskVetoTechTrig = cms.ESProducer("L1GtTriggerMaskVetoTechTrigTrivialProducer",
    TriggerMask = cms.vuint32(0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0)
)


process.l1CSCTFConfig = cms.ESProducer("CSCTFConfigProducer",
    registersSP9 = cms.vstring('CSR_LQE F1 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_KFL SP MA 0x0000 # Kill no fiber link', 
        'CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    registersSP8 = cms.vstring('CSR_LQE F1 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_KFL SP MA 0x0000 # Kill no fiber link', 
        'CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    registersSP1 = cms.vstring('CSR_LQE F1 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_KFL SP MA 0x0000 # Kill no fiber link', 
        'CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    registersSP3 = cms.vstring('CSR_LQE F1 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_KFL SP MA 0x0000 # Kill no fiber link', 
        'CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    registersSP2 = cms.vstring('CSR_LQE F1 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_KFL SP MA 0x0000 # Kill no fiber link', 
        'CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    registersSP5 = cms.vstring('CSR_LQE F1 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_KFL SP MA 0x0000 # Kill no fiber link', 
        'CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    registersSP4 = cms.vstring('CSR_LQE F1 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_KFL SP MA 0x0000 # Kill no fiber link', 
        'CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    registersSP7 = cms.vstring('CSR_LQE F1 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_KFL SP MA 0x0000 # Kill no fiber link', 
        'CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    registersSP6 = cms.vstring('CSR_LQE F1 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_KFL SP MA 0x0000 # Kill no fiber link', 
        'CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    registersSP11 = cms.vstring('CSR_LQE F1 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_KFL SP MA 0x0000 # Kill no fiber link', 
        'CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    registersSP10 = cms.vstring('CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    registersSP12 = cms.vstring('CSR_LQE F1 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_KFL SP MA 0x0000 # Kill no fiber link', 
        'CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    ptLUT_path = cms.string(''),
    alignment = cms.vdouble(0.0, 0.0, 0.0, 0.0, 0.0, 
        0.0, 0.0, 0.0, 0.0, 0.0, 
        0.0, 0.0, 0.0, 0.0, 0.0, 
        0.0)
)


process.dttfluts = cms.ESProducer("DTTrackFinderConfig")


process.l1GtParameters = cms.ESProducer("L1GtParametersTrivialProducer",
    EvmActiveBoards = cms.uint32(65535),
    DaqActiveBoards = cms.uint32(65535),
    BstLengthBytes = cms.uint32(30),
    TotalBxInEvent = cms.int32(3)
)


process.l1CaloScales = cms.ESProducer("L1ScalesTrivialProducer",
    L1CaloEmEtScaleLSB = cms.double(0.5),
    L1CaloRegionEtScaleLSB = cms.double(0.5),
    L1CaloJetThresholds = cms.vdouble(0.0, 10.0, 12.0, 14.0, 15.0, 
        18.0, 20.0, 22.0, 24.0, 25.0, 
        28.0, 30.0, 32.0, 35.0, 37.0, 
        40.0, 45.0, 50.0, 55.0, 60.0, 
        65.0, 70.0, 75.0, 80.0, 85.0, 
        90.0, 100.0, 110.0, 120.0, 125.0, 
        130.0, 140.0, 150.0, 160.0, 170.0, 
        175.0, 180.0, 190.0, 200.0, 215.0, 
        225.0, 235.0, 250.0, 275.0, 300.0, 
        325.0, 350.0, 375.0, 400.0, 425.0, 
        450.0, 475.0, 500.0, 525.0, 550.0, 
        575.0, 600.0, 625.0, 650.0, 675.0, 
        700.0, 725.0, 750.0, 775.0),
    L1CaloEmThresholds = cms.vdouble(0.0, 1.0, 2.0, 3.0, 4.0, 
        5.0, 6.0, 7.0, 8.0, 9.0, 
        10.0, 11.0, 12.0, 13.0, 14.0, 
        15.0, 16.0, 17.0, 18.0, 19.0, 
        20.0, 21.0, 22.0, 23.0, 24.0, 
        25.0, 26.0, 27.0, 28.0, 29.0, 
        30.0, 31.0, 32.0, 33.0, 34.0, 
        35.0, 36.0, 37.0, 38.0, 39.0, 
        40.0, 41.0, 42.0, 43.0, 44.0, 
        45.0, 46.0, 47.0, 48.0, 49.0, 
        50.0, 51.0, 52.0, 53.0, 54.0, 
        55.0, 56.0, 57.0, 58.0, 59.0, 
        60.0, 61.0, 62.0, 63.0)
)


process.l1GtPrescaleFactorsAlgoTrig = cms.ESProducer("L1GtPrescaleFactorsAlgoTrigTrivialProducer",
    PrescaleFactorsSet = cms.VPSet(cms.PSet(
        PrescaleFactors = cms.vint32(1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1)
    ), 
        cms.PSet(
            PrescaleFactors = cms.vint32(1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1)
        ))
)


process.SteppingHelixPropagatorAny = cms.ESProducer("SteppingHelixPropagatorESProducer",
    NoErrorPropagation = cms.bool(False),
    PropagationDirection = cms.string('anyDirection'),
    useMatVolumes = cms.bool(True),
    useTuningForL2Speed = cms.bool(False),
    useIsYokeFlag = cms.bool(True),
    endcapShiftInZNeg = cms.double(0.0),
    SetVBFPointer = cms.bool(False),
    AssumeNoMaterial = cms.bool(False),
    returnTangentPlane = cms.bool(True),
    useInTeslaFromMagField = cms.bool(False),
    VBFName = cms.string('VolumeBasedMagneticField'),
    useEndcapShiftsInZ = cms.bool(False),
    sendLogWarning = cms.bool(False),
    ComponentName = cms.string('SteppingHelixPropagatorAny'),
    debug = cms.bool(False),
    ApplyRadX0Correction = cms.bool(True),
    useMagVolumes = cms.bool(True),
    endcapShiftInZPos = cms.double(0.0)
)


process.combinedSecondaryVertex = cms.ESProducer("CombinedSecondaryVertexESProducer",
    useTrackWeights = cms.bool(True),
    pseudoMultiplicityMin = cms.uint32(2),
    correctVertexMass = cms.bool(True),
    trackSelection = cms.PSet(
        totalHitsMin = cms.uint32(0),
        jetDeltaRMax = cms.double(0.3),
        qualityClass = cms.string('highPurity'),
        pixelHitsMin = cms.uint32(0),
        sip3dSigMin = cms.double(-99999.9),
        sip3dSigMax = cms.double(99999.9),
        maxDistToAxis = cms.double(0.07),
        sip2dValMax = cms.double(99999.9),
        maxDecayLen = cms.double(5),
        ptMin = cms.double(0.0),
        sip2dSigMax = cms.double(99999.9),
        sip2dSigMin = cms.double(-99999.9),
        sip3dValMax = cms.double(99999.9),
        sip3dValMin = cms.double(-99999.9),
        sip2dValMin = cms.double(-99999.9),
        normChi2Max = cms.double(99999.9)
    ),
    pseudoVertexV0Filter = cms.PSet(
        k0sMassWindow = cms.double(0.05)
    ),
    charmCut = cms.double(1.5),
    vertexFlip = cms.bool(False),
    minimumTrackWeight = cms.double(0.5),
    trackPairV0Filter = cms.PSet(
        k0sMassWindow = cms.double(0.03)
    ),
    trackMultiplicityMin = cms.uint32(3),
    trackPseudoSelection = cms.PSet(
        totalHitsMin = cms.uint32(0),
        jetDeltaRMax = cms.double(0.3),
        qualityClass = cms.string('highPurity'),
        pixelHitsMin = cms.uint32(0),
        sip3dSigMin = cms.double(-99999.9),
        sip3dSigMax = cms.double(99999.9),
        maxDistToAxis = cms.double(0.07),
        sip2dValMax = cms.double(99999.9),
        maxDecayLen = cms.double(5),
        ptMin = cms.double(0.0),
        sip2dSigMax = cms.double(99999.9),
        sip2dSigMin = cms.double(2.0),
        sip3dValMax = cms.double(99999.9),
        sip3dValMin = cms.double(-99999.9),
        sip2dValMin = cms.double(-99999.9),
        normChi2Max = cms.double(99999.9)
    ),
    trackSort = cms.string('sip2dSig'),
    trackFlip = cms.bool(False),
    calibrationRecords = cms.vstring('CombinedSVRecoVertex', 
        'CombinedSVPseudoVertex', 
        'CombinedSVNoVertex'),
    useCategories = cms.bool(True),
    categoryVariableName = cms.string('vertexCategory')
)


process.softMuonNoIP = cms.ESProducer("MuonTaggerNoIPESProducer",
    ipSign = cms.string('any')
)


process.trackCounting3D3rd = cms.ESProducer("TrackCountingESProducer",
    deltaR = cms.double(-1.0),
    maximumDistanceToJetAxis = cms.double(0.07),
    impactParameterType = cms.int32(0),
    trackQualityClass = cms.string('any'),
    maximumDecayLength = cms.double(5.0),
    nthTrack = cms.int32(3)
)


process.l1GtPrescaleFactorsTechTrig = cms.ESProducer("L1GtPrescaleFactorsTechTrigTrivialProducer",
    PrescaleFactorsSet = cms.VPSet(cms.PSet(
        PrescaleFactors = cms.vint32(1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1)
    ), 
        cms.PSet(
            PrescaleFactors = cms.vint32(1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1)
        ))
)


process.hoDetIdAssociator = cms.ESProducer("DetIdAssociatorESProducer",
    ComponentName = cms.string('HODetIdAssociator'),
    etaBinSize = cms.double(0.087),
    nEta = cms.int32(30),
    nPhi = cms.int32(72)
)


process.trackCounting3D2nd = cms.ESProducer("TrackCountingESProducer",
    deltaR = cms.double(-1.0),
    maximumDistanceToJetAxis = cms.double(0.07),
    impactParameterType = cms.int32(0),
    trackQualityClass = cms.string('any'),
    maximumDecayLength = cms.double(5.0),
    nthTrack = cms.int32(2)
)


process.RCTConfigProducers = cms.ESProducer("RCTConfigProducers",
    eGammaHCalScaleFactors = cms.vdouble(1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0),
    eMaxForFGCut = cms.double(50.0),
    noiseVetoHB = cms.bool(False),
    jscQuietThresholdEndcap = cms.uint32(3),
    hOeCut = cms.double(0.05),
    eGammaECalScaleFactors = cms.vdouble(1.0, 1.01, 1.02, 1.02, 1.02, 
        1.06, 1.04, 1.04, 1.05, 1.09, 
        1.1, 1.1, 1.15, 1.2, 1.27, 
        1.29, 1.32, 1.52, 1.52, 1.48, 
        1.4, 1.32, 1.26, 1.21, 1.17, 
        1.15, 1.15, 1.15),
    eMinForHoECut = cms.double(3.0),
    jscQuietThresholdBarrel = cms.uint32(3),
    jetMETHCalScaleFactors = cms.vdouble(1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0),
    jetMETECalScaleFactors = cms.vdouble(1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0),
    hActivityCut = cms.double(3.0),
    noiseVetoHEplus = cms.bool(False),
    eicIsolationThreshold = cms.uint32(3),
    jetMETLSB = cms.double(0.5),
    eActivityCut = cms.double(3.0),
    eMinForFGCut = cms.double(3.0),
    eGammaLSB = cms.double(0.5),
    eMaxForHoECut = cms.double(60.0),
    hMinForHoECut = cms.double(3.0),
    noiseVetoHEminus = cms.bool(False)
)


process.EcalElectronicsMappingBuilder = cms.ESProducer("EcalElectronicsMappingBuilder",
    MapFile = cms.untracked.string('Geometry/EcalMapping/data/EEMap.txt')
)


process.StripCPEfromTrackAngleESProducer = cms.ESProducer("StripCPEfromTrackAngleESProducer",
    ComponentName = cms.string('StripCPEfromTrackAngle')
)


process.softLeptonByPt = cms.ESProducer("LeptonTaggerByPtESProducer",
    ipSign = cms.string('any')
)


process.l1csctpconf = cms.ESProducer("L1CSCTriggerPrimitivesConfigProducer",
    alctParam = cms.PSet(
        alctAccelMode = cms.uint32(1),
        alctTrigMode = cms.uint32(3),
        alctDriftDelay = cms.uint32(3),
        alctNplanesHitAccelPretrig = cms.uint32(2),
        alctL1aWindowWidth = cms.uint32(5),
        alctNplanesHitPattern = cms.uint32(4),
        alctNplanesHitAccelPattern = cms.uint32(4),
        alctFifoTbins = cms.uint32(16),
        alctNplanesHitPretrig = cms.uint32(2),
        alctFifoPretrig = cms.uint32(10)
    ),
    isTMB07 = cms.bool(True),
    clctParamMTCC2 = cms.PSet(
        clctDriftDelay = cms.uint32(2),
        clctMinSeparation = cms.uint32(10),
        clctPidThreshPretrig = cms.uint32(2),
        clctFifoTbins = cms.uint32(12),
        clctNplanesHitPretrig = cms.uint32(4),
        clctHitPersist = cms.uint32(6),
        clctFifoPretrig = cms.uint32(7),
        clctNplanesHitPattern = cms.uint32(1)
    ),
    isMTCC = cms.bool(False),
    clctParam = cms.PSet(
        clctDriftDelay = cms.uint32(2),
        clctMinSeparation = cms.uint32(10),
        clctPidThreshPretrig = cms.uint32(2),
        clctFifoTbins = cms.uint32(12),
        clctNplanesHitPretrig = cms.uint32(2),
        clctHitPersist = cms.uint32(6),
        clctFifoPretrig = cms.uint32(7),
        clctNplanesHitPattern = cms.uint32(4)
    ),
    alctParamMTCC2 = cms.PSet(
        alctAccelMode = cms.uint32(0),
        alctTrigMode = cms.uint32(2),
        alctDriftDelay = cms.uint32(2),
        alctNplanesHitAccelPretrig = cms.uint32(2),
        alctL1aWindowWidth = cms.uint32(7),
        alctNplanesHitPattern = cms.uint32(4),
        alctNplanesHitAccelPattern = cms.uint32(4),
        alctFifoTbins = cms.uint32(16),
        alctNplanesHitPretrig = cms.uint32(2),
        alctFifoPretrig = cms.uint32(10)
    )
)


process.GlobalTrackingGeometryESProducer = cms.ESProducer("GlobalTrackingGeometryESProducer")


process.EcalLaserCorrectionService = cms.ESProducer("EcalLaserCorrectionService")


process.L1GctConfigProducers = cms.ESProducer("L1GctConfigProducers",
    JetFinderCentralJetSeed = cms.uint32(1),
    CalibrationStyle = cms.string('ORCAStyle'),
    HfLutBitCountThresholds = cms.vuint32(1, 2, 3, 4, 5, 
        6, 7),
    HfLutEtSumThresholds = cms.vuint32(2, 4, 6, 8, 10, 
        12, 14),
    L1CaloHtScaleLsbInGeV = cms.double(1.0),
    PowerSeriesCoefficients = cms.PSet(
        nonTauJetCalib10 = cms.vdouble(1.0),
        nonTauJetCalib1 = cms.vdouble(1.0),
        tauJetCalib0 = cms.vdouble(1.0),
        nonTauJetCalib5 = cms.vdouble(1.0),
        nonTauJetCalib7 = cms.vdouble(1.0),
        nonTauJetCalib2 = cms.vdouble(1.0),
        nonTauJetCalib8 = cms.vdouble(1.0),
        nonTauJetCalib9 = cms.vdouble(1.0),
        nonTauJetCalib4 = cms.vdouble(1.0),
        nonTauJetCalib3 = cms.vdouble(1.0),
        tauJetCalib4 = cms.vdouble(1.0),
        tauJetCalib5 = cms.vdouble(1.0),
        tauJetCalib6 = cms.vdouble(1.0),
        nonTauJetCalib0 = cms.vdouble(1.0),
        nonTauJetCalib6 = cms.vdouble(1.0),
        tauJetCalib1 = cms.vdouble(1.0),
        tauJetCalib2 = cms.vdouble(1.0),
        tauJetCalib3 = cms.vdouble(1.0)
    ),
    JetFinderForwardJetSeed = cms.uint32(1),
    OrcaStyleCoefficients = cms.PSet(
        tauJetCalib0 = cms.vdouble(47.4, -20.7, 0.7922, 9.53e-05),
        nonTauJetCalib1 = cms.vdouble(49.4, -22.5, 0.7867, 9.6e-05),
        nonTauJetCalib10 = cms.vdouble(9.3, 1.3, 0.2719, 0.003418),
        tauJetCalib3 = cms.vdouble(49.3, -22.9, 0.7331, 0.0001221),
        tauJetCalib1 = cms.vdouble(49.4, -22.5, 0.7867, 9.6e-05),
        tauJetCalib4 = cms.vdouble(48.2, -24.5, 0.7706, 0.000128),
        nonTauJetCalib8 = cms.vdouble(13.1, -4.5, 0.7071, 7.26e-05),
        nonTauJetCalib9 = cms.vdouble(12.4, -3.8, 0.6558, 0.000489),
        tauJetCalib2 = cms.vdouble(47.1, -22.2, 0.7645, 0.0001209),
        tauJetCalib5 = cms.vdouble(42.0, -23.9, 0.7945, 0.0001458),
        nonTauJetCalib2 = cms.vdouble(47.1, -22.2, 0.7645, 0.0001209),
        nonTauJetCalib3 = cms.vdouble(49.3, -22.9, 0.7331, 0.0001221),
        tauJetCalib6 = cms.vdouble(33.8, -22.1, 0.8202, 0.0001403),
        nonTauJetCalib0 = cms.vdouble(47.4, -20.7, 0.7922, 9.53e-05),
        nonTauJetCalib6 = cms.vdouble(33.8, -22.1, 0.8202, 0.0001403),
        nonTauJetCalib7 = cms.vdouble(17.1, -6.6, 0.6958, 6.88e-05),
        nonTauJetCalib4 = cms.vdouble(48.2, -24.5, 0.7706, 0.000128),
        nonTauJetCalib5 = cms.vdouble(42.0, -23.9, 0.7945, 0.0001458)
    ),
    ConvertEtValuesToEnergy = cms.bool(False),
    jetCounterSetup = cms.PSet(
        jetCountersNegativeWheel = cms.VPSet(cms.PSet(
            cutDescriptionList = cms.vstring('JC_minRank_1')
        ), 
            cms.PSet(
                cutDescriptionList = cms.vstring('JC_minRank_1', 
                    'JC_centralEta_6')
            ), 
            cms.PSet(
                cutDescriptionList = cms.vstring('JC_minRank_11')
            ), 
            cms.PSet(
                cutDescriptionList = cms.vstring('JC_minRank_11', 
                    'JC_centralEta_6')
            ), 
            cms.PSet(
                cutDescriptionList = cms.vstring('JC_minRank_19')
            )),
        jetCountersPositiveWheel = cms.VPSet(cms.PSet(
            cutDescriptionList = cms.vstring('JC_minRank_1')
        ), 
            cms.PSet(
                cutDescriptionList = cms.vstring('JC_minRank_1', 
                    'JC_centralEta_6')
            ), 
            cms.PSet(
                cutDescriptionList = cms.vstring('JC_minRank_11')
            ), 
            cms.PSet(
                cutDescriptionList = cms.vstring('JC_minRank_11', 
                    'JC_centralEta_6')
            ), 
            cms.PSet(
                cutDescriptionList = cms.vstring('JC_minRank_19')
            ))
    ),
    PiecewiseCubicCoefficients = cms.PSet(
        tauJetCalib0 = cms.vdouble(500.0, 100.0, 17.7409, 0.351901, -0.000701462, 
            5.77204e-07, 5.0, 0.720604, 1.25179, -0.0150777, 
            7.13711e-05),
        nonTauJetCalib1 = cms.vdouble(500.0, 100.0, 20.0549, 0.321867, -0.00064901, 
            5.50042e-07, 5.0, 1.30465, 1.2774, -0.0159193, 
            7.64496e-05),
        nonTauJetCalib10 = cms.vdouble(150.0, 80.0, 1.70475, -0.142171, 0.00104963, 
            -1.62214e-05, 5.0, 1.70475, -0.142171, 0.00104963, 
            -1.62214e-05),
        tauJetCalib3 = cms.vdouble(500.0, 100.0, 27.7822, 0.155986, -0.000266441, 
            6.69814e-08, 5.0, 2.64613, 1.30745, -0.0180964, 
            8.83567e-05),
        tauJetCalib1 = cms.vdouble(500.0, 100.0, 20.0549, 0.321867, -0.00064901, 
            5.50042e-07, 5.0, 1.30465, 1.2774, -0.0159193, 
            7.64496e-05),
        tauJetCalib4 = cms.vdouble(500.0, 100.0, 26.6384, 0.0567369, -0.000416292, 
            2.60929e-07, 5.0, 2.63299, 1.16558, -0.0170351, 
            7.95703e-05),
        nonTauJetCalib8 = cms.vdouble(250.0, 150.0, 1.38861, 0.0362661, 0.0, 
            0.0, 5.0, 1.87993, 0.0329907, 0.0, 
            0.0),
        nonTauJetCalib9 = cms.vdouble(200.0, 80.0, 35.0095, -0.669677, 0.00208498, 
            -1.50554e-06, 5.0, 3.16074, -0.114404, 0.0, 
            0.0),
        tauJetCalib2 = cms.vdouble(500.0, 100.0, 24.3454, 0.257989, -0.000450184, 
            3.09951e-07, 5.0, 2.1034, 1.32441, -0.0173659, 
            8.50669e-05),
        tauJetCalib5 = cms.vdouble(500.0, 100.0, 29.5396, 0.001137, -0.000145232, 
            6.91445e-08, 5.0, 4.16752, 1.08477, -0.016134, 
            7.69652e-05),
        nonTauJetCalib2 = cms.vdouble(500.0, 100.0, 24.3454, 0.257989, -0.000450184, 
            3.09951e-07, 5.0, 2.1034, 1.32441, -0.0173659, 
            8.50669e-05),
        nonTauJetCalib3 = cms.vdouble(500.0, 100.0, 27.7822, 0.155986, -0.000266441, 
            6.69814e-08, 5.0, 2.64613, 1.30745, -0.0180964, 
            8.83567e-05),
        tauJetCalib6 = cms.vdouble(500.0, 100.0, 30.1405, -0.14281, 0.000555849, 
            -7.52446e-07, 5.0, 4.79283, 0.672125, -0.00879174, 
            3.65776e-05),
        nonTauJetCalib0 = cms.vdouble(500.0, 100.0, 17.7409, 0.351901, -0.000701462, 
            5.77204e-07, 5.0, 0.720604, 1.25179, -0.0150777, 
            7.13711e-05),
        nonTauJetCalib6 = cms.vdouble(500.0, 100.0, 30.1405, -0.14281, 0.000555849, 
            -7.52446e-07, 5.0, 4.79283, 0.672125, -0.00879174, 
            3.65776e-05),
        nonTauJetCalib7 = cms.vdouble(300.0, 80.0, 30.2715, -0.539688, 0.00499898, 
            -1.2204e-05, 5.0, 1.97284, 0.0610729, 0.00671548, 
            -7.22583e-05),
        nonTauJetCalib4 = cms.vdouble(500.0, 100.0, 26.6384, 0.0567369, -0.000416292, 
            2.60929e-07, 5.0, 2.63299, 1.16558, -0.0170351, 
            7.95703e-05),
        nonTauJetCalib5 = cms.vdouble(500.0, 100.0, 29.5396, 0.001137, -0.000145232, 
            6.91445e-08, 5.0, 4.16752, 1.08477, -0.016134, 
            7.69652e-05)
    ),
    L1CaloJetZeroSuppressionThresholdInGeV = cms.double(5.0)
)


process.softElectron = cms.ESProducer("ElectronTaggerESProducer",
    ipSign = cms.string('any')
)


process.softLeptonByIP3d = cms.ESProducer("LeptonTaggerByIPESProducer",
    use3d = cms.bool(True),
    ipSign = cms.string('any')
)


process.jetProbability = cms.ESProducer("JetProbabilityESProducer",
    deltaR = cms.double(0.3),
    maximumDistanceToJetAxis = cms.double(0.07),
    impactParameterType = cms.int32(0),
    trackQualityClass = cms.string('any'),
    trackIpSign = cms.int32(1),
    minimumProbability = cms.double(0.005),
    maximumDecayLength = cms.double(5.0)
)


process.ZdcHardcodeGeometryEP = cms.ESProducer("ZdcHardcodeGeometryEP",
    applyAlignment = cms.untracked.bool(False)
)


process.l1GtTriggerMaskAlgoTrig = cms.ESProducer("L1GtTriggerMaskAlgoTrigTrivialProducer",
    TriggerMask = cms.vuint32(0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0)
)


process.rpcconf = cms.ESProducer("RPCTriggerConfig",
    filedir = cms.untracked.string('L1Trigger/RPCTrigger/data/Eff90PPT12/'),
    PACsPerTower = cms.untracked.int32(12)
)


process.EcalTrigTowerConstituentsMapBuilder = cms.ESProducer("EcalTrigTowerConstituentsMapBuilder",
    MapFile = cms.untracked.string('Geometry/EcalMapping/data/EndCap_TTMap.txt')
)


process.idealForDigiCSCGeometry = cms.ESProducer("CSCGeometryESModule",
    appendToDataLabel = cms.string('idealForDigi'),
    debugV = cms.untracked.bool(False),
    useGangedStripsInME1a = cms.bool(True),
    alignmentsLabel = cms.string('fakeForIdeal'),
    useOnlyWiresInME1a = cms.bool(False),
    useRealWireGeometry = cms.bool(True),
    useCentreTIOffsets = cms.bool(False),
    applyAlignment = cms.bool(False)
)


process.hcal_db_producer = cms.ESProducer("HcalDbProducer",
    file = cms.untracked.string(''),
    dump = cms.untracked.vstring('')
)


process.simpleSecondaryVertex = cms.ESProducer("SimpleSecondaryVertexESProducer",
    useSignificance = cms.bool(True),
    unBoost = cms.bool(False),
    use3d = cms.bool(True)
)


process.caloDetIdAssociator = cms.ESProducer("DetIdAssociatorESProducer",
    ComponentName = cms.string('CaloDetIdAssociator'),
    etaBinSize = cms.double(0.087),
    nEta = cms.int32(70),
    nPhi = cms.int32(72)
)


process.siStripQualityESProducer = cms.ESProducer("SiStripQualityESProducer",
    appendToDataLabel = cms.string(''),
    ThresholdForReducedGranularity = cms.double(0.3),
    ReduceGranularity = cms.bool(True),
    ListOfRecordToMerge = cms.VPSet(cms.PSet(
        record = cms.string('SiStripDetCablingRcd'),
        tag = cms.string('')
    ), 
        cms.PSet(
            record = cms.string('SiStripBadChannelRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('SiStripBadFiberRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('SiStripBadModuleRcd'),
            tag = cms.string('')
        ))
)


process.ParametrizedMagneticFieldProducer = cms.ESProducer("ParametrizedMagneticFieldProducer",
    version = cms.string('OAE_1103l_071212'),
    parameters = cms.PSet(
        BValue = cms.string('3_8T')
    ),
    label = cms.untracked.string('parametrizedField')
)


process.HcalTopologyIdealEP = cms.ESProducer("HcalTopologyIdealEP")


process.sistripconn = cms.ESProducer("SiStripConnectivity")


process.idealForDigiTrackerGeometry = cms.ESProducer("TrackerDigiGeometryESModule",
    appendToDataLabel = cms.string('idealForDigi'),
    fromDDD = cms.bool(True),
    applyAlignment = cms.bool(False),
    alignmentsLabel = cms.string('fakeForIdeal')
)


process.L1MuGMTScales = cms.ESProducer("L1MuGMTScalesProducer",
    minDeltaPhi = cms.double(-0.1963495),
    signedPackingDeltaPhi = cms.bool(True),
    maxOvlEtaDT = cms.double(1.3),
    nbitPackingOvlEtaCSC = cms.int32(4),
    scaleReducedEtaDT = cms.vdouble(0.0, 0.22, 0.27, 0.58, 0.77, 
        0.87, 0.92, 1.24, 1.3),
    scaleReducedEtaFwdRPC = cms.vdouble(1.04, 1.24, 1.36, 1.48, 1.61, 
        1.73, 1.85, 1.97, 2.1),
    nbitPackingOvlEtaFwdRPC = cms.int32(4),
    nbinsDeltaEta = cms.int32(15),
    minOvlEtaCSC = cms.double(0.9),
    scaleReducedEtaCSC = cms.vdouble(0.9, 1.06, 1.26, 1.46, 1.66, 
        1.86, 2.06, 2.26, 2.5),
    nbinsOvlEtaFwdRPC = cms.int32(7),
    nbitPackingReducedEta = cms.int32(4),
    scaleOvlEtaRPC = cms.vdouble(0.72, 0.83, 0.93, 1.04, 1.14, 
        1.24, 1.36, 1.48),
    signedPackingDeltaEta = cms.bool(True),
    nbinsOvlEtaDT = cms.int32(7),
    offsetDeltaPhi = cms.int32(4),
    nbinsReducedEta = cms.int32(8),
    nbitPackingDeltaPhi = cms.int32(3),
    offsetDeltaEta = cms.int32(7),
    nbitPackingOvlEtaBrlRPC = cms.int32(4),
    nbinsDeltaPhi = cms.int32(8),
    nbinsOvlEtaBrlRPC = cms.int32(7),
    minDeltaEta = cms.double(-0.3),
    maxDeltaPhi = cms.double(0.1527163),
    maxOvlEtaCSC = cms.double(1.25),
    scaleReducedEtaBrlRPC = cms.vdouble(0.0, 0.06, 0.25, 0.41, 0.54, 
        0.7, 0.83, 0.93, 1.04),
    nbinsOvlEtaCSC = cms.int32(7),
    nbitPackingDeltaEta = cms.int32(4),
    maxDeltaEta = cms.double(0.3),
    minOvlEtaDT = cms.double(0.73125),
    nbitPackingOvlEtaDT = cms.int32(4)
)


process.l1GtTriggerMaskTechTrig = cms.ESProducer("L1GtTriggerMaskTechTrigTrivialProducer",
    TriggerMask = cms.vuint32(0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0)
)


process.TrackerGeometricDetESModule = cms.ESProducer("TrackerGeometricDetESModule",
    fromDDD = cms.bool(True)
)


process.l1CaloGeometry = cms.ESProducer("L1CaloGeometryProd",
    gctEtaBinBoundaries = cms.vdouble(0.0, 0.348, 0.695, 1.044, 1.392, 
        1.74, 2.172, 3.0, 3.5, 4.0, 
        4.5, 5.0),
    numberGctEmJetPhiBins = cms.uint32(18),
    numberGctEtSumPhiBins = cms.uint32(72),
    gctEmJetPhiBinOffset = cms.double(-0.5),
    numberGctForwardEtaBinsPerHalf = cms.uint32(4),
    gctEtSumPhiBinOffset = cms.double(0.0),
    numberGctCentralEtaBinsPerHalf = cms.uint32(7),
    etaSignBitOffset = cms.uint32(8)
)


process.L1MuGMTParameters = cms.ESProducer("L1MuGMTParametersProducer",
    MergeMethodSRKFwd = cms.string('takeCSC'),
    SubsystemMask = cms.uint32(0),
    HaloOverwritesMatchedFwd = cms.bool(True),
    PhiWeight_barrel = cms.double(1.0),
    MergeMethodISOSpecialUseANDBrl = cms.bool(True),
    HaloOverwritesMatchedBrl = cms.bool(True),
    CDLConfigWordbRPCCSC = cms.uint32(16),
    IsolationCellSizeEta = cms.int32(2),
    MergeMethodEtaFwd = cms.string('Special'),
    EtaPhiThreshold_COU = cms.double(0.127),
    EtaWeight_barrel = cms.double(0.028),
    MergeMethodMIPBrl = cms.string('Special'),
    EtaPhiThreshold_barrel = cms.double(0.062),
    IsolationCellSizePhi = cms.int32(2),
    MergeMethodChargeBrl = cms.string('takeDT'),
    VersionSortRankEtaQLUT = cms.uint32(2),
    MergeMethodPtBrl = cms.string('byMinPt'),
    CaloTrigger = cms.bool(True),
    MergeMethodPtFwd = cms.string('byMinPt'),
    PropagatePhi = cms.bool(False),
    EtaWeight_endcap = cms.double(0.13),
    MergeMethodEtaBrl = cms.string('Special'),
    CDLConfigWordfRPCDT = cms.uint32(1),
    CDLConfigWordDTCSC = cms.uint32(2),
    MergeMethodChargeFwd = cms.string('takeCSC'),
    DoOvlRpcAnd = cms.bool(False),
    EtaWeight_COU = cms.double(0.316),
    MergeMethodISOSpecialUseANDFwd = cms.bool(True),
    MergeMethodMIPFwd = cms.string('Special'),
    MergeMethodPhiBrl = cms.string('takeDT'),
    EtaPhiThreshold_endcap = cms.double(0.062),
    CDLConfigWordCSCDT = cms.uint32(3),
    MergeMethodMIPSpecialUseANDFwd = cms.bool(False),
    MergeMethodPhiFwd = cms.string('takeCSC'),
    MergeMethodISOFwd = cms.string('Special'),
    PhiWeight_COU = cms.double(1.0),
    MergeMethodISOBrl = cms.string('Special'),
    PhiWeight_endcap = cms.double(1.0),
    SortRankOffsetBrl = cms.uint32(10),
    MergeMethodSRKBrl = cms.string('takeDT'),
    MergeMethodMIPSpecialUseANDBrl = cms.bool(False),
    SortRankOffsetFwd = cms.uint32(10)
)


process.impactParameterMVAComputer = cms.ESProducer("GenericMVAJetTagESProducer",
    useCategories = cms.bool(False),
    calibrationRecord = cms.string('ImpactParameterMVA')
)


process.combinedSecondaryVertexMVA = cms.ESProducer("CombinedSecondaryVertexESProducer",
    useTrackWeights = cms.bool(True),
    pseudoMultiplicityMin = cms.uint32(2),
    correctVertexMass = cms.bool(True),
    trackSelection = cms.PSet(
        totalHitsMin = cms.uint32(0),
        jetDeltaRMax = cms.double(0.3),
        qualityClass = cms.string('highPurity'),
        pixelHitsMin = cms.uint32(0),
        sip3dSigMin = cms.double(-99999.9),
        sip3dSigMax = cms.double(99999.9),
        maxDistToAxis = cms.double(0.07),
        sip2dValMax = cms.double(99999.9),
        maxDecayLen = cms.double(5),
        ptMin = cms.double(0.0),
        sip2dSigMax = cms.double(99999.9),
        sip2dSigMin = cms.double(-99999.9),
        sip3dValMax = cms.double(99999.9),
        sip3dValMin = cms.double(-99999.9),
        sip2dValMin = cms.double(-99999.9),
        normChi2Max = cms.double(99999.9)
    ),
    pseudoVertexV0Filter = cms.PSet(
        k0sMassWindow = cms.double(0.05)
    ),
    charmCut = cms.double(1.5),
    vertexFlip = cms.bool(False),
    minimumTrackWeight = cms.double(0.5),
    trackPairV0Filter = cms.PSet(
        k0sMassWindow = cms.double(0.03)
    ),
    trackMultiplicityMin = cms.uint32(3),
    trackPseudoSelection = cms.PSet(
        totalHitsMin = cms.uint32(0),
        jetDeltaRMax = cms.double(0.3),
        qualityClass = cms.string('highPurity'),
        pixelHitsMin = cms.uint32(0),
        sip3dSigMin = cms.double(-99999.9),
        sip3dSigMax = cms.double(99999.9),
        maxDistToAxis = cms.double(0.07),
        sip2dValMax = cms.double(99999.9),
        maxDecayLen = cms.double(5),
        ptMin = cms.double(0.0),
        sip2dSigMax = cms.double(99999.9),
        sip2dSigMin = cms.double(2.0),
        sip3dValMax = cms.double(99999.9),
        sip3dValMin = cms.double(-99999.9),
        sip2dValMin = cms.double(-99999.9),
        normChi2Max = cms.double(99999.9)
    ),
    trackSort = cms.string('sip2dSig'),
    trackFlip = cms.bool(False),
    calibrationRecords = cms.vstring('CombinedSVMVARecoVertex', 
        'CombinedSVMVAPseudoVertex', 
        'CombinedSVMVANoVertex'),
    useCategories = cms.bool(True),
    categoryVariableName = cms.string('vertexCategory')
)


process.L1MuTriggerPtScale = cms.ESProducer("L1MuTriggerPtScaleProducer",
    nbitPackingPt = cms.int32(5),
    scalePt = cms.vdouble(-1.0, 0.0, 1.5, 2.0, 2.5, 
        3.0, 3.5, 4.0, 4.5, 5.0, 
        6.0, 7.0, 8.0, 10.0, 12.0, 
        14.0, 16.0, 18.0, 20.0, 25.0, 
        30.0, 35.0, 40.0, 45.0, 50.0, 
        60.0, 70.0, 80.0, 90.0, 100.0, 
        120.0, 140.0, 1000000.0),
    signedPackingPt = cms.bool(False),
    nbinsPt = cms.int32(32)
)


process.EcalPreshowerGeometryEP = cms.ESProducer("EcalPreshowerGeometryEP",
    applyAlignment = cms.untracked.bool(False)
)


process.jetBProbability = cms.ESProducer("JetBProbabilityESProducer",
    deltaR = cms.double(-1.0),
    maximumDistanceToJetAxis = cms.double(0.07),
    impactParameterType = cms.int32(0),
    trackQualityClass = cms.string('any'),
    trackIpSign = cms.int32(1),
    minimumProbability = cms.double(0.005),
    numberOfBTracks = cms.uint32(4),
    maximumDecayLength = cms.double(5.0)
)


process.MuonNumberingInitialization = cms.ESProducer("MuonNumberingInitialization")


process.fakeForIdealAlignment = cms.ESProducer("FakeAlignmentProducer",
    appendToDataLabel = cms.string('fakeForIdeal')
)


process.l1GtBoardMaps = cms.ESProducer("L1GtBoardMapsTrivialProducer",
    ActiveBoardsDaqRecord = cms.vint32(-1, 0, 1, 2, 3, 
        4, 5, 6, 7, 8, 
        -1, -1),
    CableToPsbMap = cms.vint32(0, 0, 0, 0, 1, 
        1, 1, 1, 2, 2, 
        2, 2, 3, 3, 3, 
        3, 4, 4, 4, 4, 
        5, 5, 5, 5, 6, 
        6, 6, 6),
    BoardPositionDaqRecord = cms.vint32(1, 2, 3, 4, 5, 
        6, 7, 8, 9, 10, 
        -1, -1),
    BoardPositionEvmRecord = cms.vint32(1, 3, -1, -1, -1, 
        -1, -1, -1, -1, -1, 
        2, -1),
    BoardList = cms.vstring('GTFE', 
        'FDL', 
        'PSB', 
        'PSB', 
        'PSB', 
        'PSB', 
        'PSB', 
        'PSB', 
        'PSB', 
        'GMT', 
        'TCS', 
        'TIM'),
    CableList = cms.vstring('Free', 
        'Free', 
        'Free', 
        'TechTr', 
        'IsoEGQ', 
        'NoIsoEGQ', 
        'CenJetQ', 
        'ForJetQ', 
        'TauJetQ', 
        'ESumsQ', 
        'HfQ', 
        'Free', 
        'Free', 
        'Free', 
        'Free', 
        'Free', 
        'MQF4', 
        'MQF3', 
        'MQB2', 
        'MQB1', 
        'MQF8', 
        'MQF7', 
        'MQB6', 
        'MQB5', 
        'MQF12', 
        'MQF11', 
        'MQB10', 
        'MQB9'),
    BoardHexNameMap = cms.vint32(0, 253, 187, 187, 187, 
        187, 187, 187, 187, 221, 
        204, 173),
    ActiveBoardsEvmRecord = cms.vint32(-1, 1, -1, -1, -1, 
        -1, -1, -1, -1, -1, 
        0, -1),
    BoardSlotMap = cms.vint32(17, 10, 9, 13, 14, 
        15, 19, 20, 21, 18, 
        7, 16),
    BoardIndex = cms.vint32(0, 0, 0, 1, 2, 
        3, 4, 5, 6, 0, 
        0, 0)
)


process.L1DTConfig = cms.ESProducer("DTConfigTrivialProducer",
    DTTPGMap = cms.untracked.PSet(
        wh0st2se11 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se10 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se12 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st1se4 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se12 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se11 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se10 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se1 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se2 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st3se4 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se4 = cms.untracked.vint32(72, 48, 72, 18),
        whm2st1se8 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se9 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se1 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st2se6 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st1se12 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se10 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se11 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st2se12 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se1 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st1se3 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se2 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st3se3 = cms.untracked.vint32(72, 48, 72, 18),
        whm1st1se7 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st2se2 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st1se6 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st4se8 = cms.untracked.vint32(92, 0, 92, 23),
        whm1st3se11 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st2se9 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se8 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st3se10 = cms.untracked.vint32(72, 58, 72, 18),
        whm1st3se5 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st2se4 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se7 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st3se6 = cms.untracked.vint32(72, 58, 72, 18),
        whm1st3se1 = cms.untracked.vint32(72, 58, 72, 18),
        whm1st1se9 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st2se3 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st3se2 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st4se14 = cms.untracked.vint32(60, 0, 60, 15),
        whm2st4se13 = cms.untracked.vint32(72, 0, 72, 18),
        whm2st4se12 = cms.untracked.vint32(92, 0, 92, 23),
        whm2st4se11 = cms.untracked.vint32(48, 0, 48, 12),
        whm2st4se10 = cms.untracked.vint32(60, 0, 60, 15),
        whm2st1se6 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se10 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se11 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se12 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se7 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st3se7 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st4se9 = cms.untracked.vint32(48, 0, 48, 12),
        whm2st4se8 = cms.untracked.vint32(92, 0, 92, 23),
        whm1st4se12 = cms.untracked.vint32(92, 0, 92, 23),
        whm1st4se13 = cms.untracked.vint32(72, 0, 72, 18),
        whm1st4se10 = cms.untracked.vint32(60, 0, 60, 15),
        whm1st4se11 = cms.untracked.vint32(48, 0, 48, 12),
        whm2st4se3 = cms.untracked.vint32(96, 0, 96, 24),
        whm2st4se2 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st4se14 = cms.untracked.vint32(60, 0, 60, 15),
        whm2st3se8 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se9 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se6 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se7 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se4 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se5 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se2 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se3 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se1 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se12 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se11 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se10 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st1se12 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se10 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se11 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st4se6 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st4se7 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st4se4 = cms.untracked.vint32(72, 0, 72, 18),
        wh1st4se5 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st4se2 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st2se12 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se11 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se10 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st3se3 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se2 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se1 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se7 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se6 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se5 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st4se9 = cms.untracked.vint32(48, 0, 48, 12),
        whm1st1se3 = cms.untracked.vint32(50, 48, 50, 13),
        whm1st1se2 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se1 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st2se8 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st2se9 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st1se5 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se4 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st2se4 = cms.untracked.vint32(60, 48, 60, 15),
        wh1st2se5 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st2se6 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st2se7 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st2se1 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st2se2 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st4se8 = cms.untracked.vint32(92, 0, 92, 23),
        wh2st3se9 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st1se8 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st4se7 = cms.untracked.vint32(96, 0, 96, 24),
        whm2st4se6 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st4se4 = cms.untracked.vint32(72, 0, 72, 18),
        whm2st4se5 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st1se8 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se7 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se4 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st4se4 = cms.untracked.vint32(72, 0, 72, 18),
        wh2st1se2 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se3 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se1 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se1 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se2 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se3 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se4 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se5 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se8 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se9 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st4se1 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se3 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se2 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se5 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se4 = cms.untracked.vint32(72, 0, 72, 18),
        wh2st4se7 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se6 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st4se3 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se8 = cms.untracked.vint32(92, 0, 92, 23),
        wh0st4se1 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st4se7 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st4se6 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st4se5 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st4se4 = cms.untracked.vint32(72, 0, 72, 18),
        wh0st3se10 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se11 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se12 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st4se11 = cms.untracked.vint32(48, 0, 48, 12),
        wh2st4se10 = cms.untracked.vint32(60, 0, 60, 15),
        wh2st4se13 = cms.untracked.vint32(72, 0, 72, 18),
        wh2st4se12 = cms.untracked.vint32(92, 0, 92, 23),
        wh2st4se14 = cms.untracked.vint32(60, 0, 60, 15),
        wh1st1se5 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st4se1 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st4se2 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st4se3 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st2se12 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st4se5 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st2se10 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st4se7 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st4se8 = cms.untracked.vint32(92, 0, 92, 23),
        whm1st4se9 = cms.untracked.vint32(48, 0, 48, 12),
        whm1st2se11 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st3se6 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se7 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se4 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se5 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se2 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se3 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se1 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se7 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st1se5 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st3se8 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se9 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st1se6 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se8 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se9 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st3se12 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se10 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se11 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st1se11 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se10 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se12 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st2se11 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se5 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se4 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se7 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se6 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se1 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se3 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se2 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se9 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se8 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st4se6 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st1se5 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st2se6 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se7 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se4 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se5 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se2 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se3 = cms.untracked.vint32(60, 48, 60, 15),
        whm1st2se1 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se8 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se9 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se7 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se6 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se5 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se4 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se3 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se2 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se1 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st1se7 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st2se9 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se8 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st4se13 = cms.untracked.vint32(72, 0, 72, 18),
        wh0st1se6 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st4se11 = cms.untracked.vint32(48, 0, 48, 12),
        wh0st4se10 = cms.untracked.vint32(60, 0, 60, 15),
        whm1st3se12 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st4se14 = cms.untracked.vint32(60, 0, 60, 15),
        whm2st1se3 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st4se9 = cms.untracked.vint32(48, 0, 48, 12),
        wh1st4se10 = cms.untracked.vint32(60, 0, 60, 15),
        wh1st4se11 = cms.untracked.vint32(48, 0, 48, 12),
        wh1st4se12 = cms.untracked.vint32(92, 0, 92, 23),
        wh1st4se13 = cms.untracked.vint32(72, 0, 72, 18),
        wh1st4se14 = cms.untracked.vint32(60, 0, 60, 15),
        wh1st1se4 = cms.untracked.vint32(50, 48, 50, 13),
        wh1st1se7 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se6 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se9 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st3se10 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st2se3 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st3se11 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se12 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st4se12 = cms.untracked.vint32(92, 0, 92, 23),
        wh1st3se9 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se8 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st4se9 = cms.untracked.vint32(48, 0, 48, 12),
        wh1st3se8 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st4se2 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st3se1 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se2 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se3 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se4 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se5 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se6 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st4se3 = cms.untracked.vint32(96, 0, 96, 24),
        whm2st4se1 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st4se1 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st2se10 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se11 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se10 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se12 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se5 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st3se9 = cms.untracked.vint32(72, 58, 72, 18),
        whm1st3se8 = cms.untracked.vint32(72, 58, 72, 18)
    ),
    DTTPGParameters = cms.PSet(
        SectCollParameters = cms.PSet(
            SCCSP5 = cms.int32(0),
            SCCSP2 = cms.int32(0),
            SCCSP3 = cms.int32(0),
            SCECF4 = cms.bool(False),
            SCCSP1 = cms.int32(0),
            SCECF2 = cms.bool(False),
            SCECF3 = cms.bool(False),
            SCCSP4 = cms.int32(0),
            SCECF1 = cms.bool(False),
            Debug = cms.untracked.bool(False)
        ),
        Debug = cms.untracked.bool(False),
        TUParameters = cms.PSet(
            TracoParameters = cms.PSet(
                SPRGCOMP = cms.int32(2),
                FHTMSK = cms.int32(0),
                DD = cms.int32(18),
                SSLMSK = cms.int32(0),
                LVALIDIFH = cms.int32(0),
                Debug = cms.untracked.int32(0),
                FSLMSK = cms.int32(0),
                SHTPRF = cms.int32(1),
                SHTMSK = cms.int32(0),
                TRGENB3 = cms.int32(1),
                SHISM = cms.int32(0),
                IBTIOFF = cms.int32(0),
                KPRGCOM = cms.int32(255),
                KRAD = cms.int32(0),
                FLTMSK = cms.int32(0),
                LTS = cms.int32(0),
                SLTMSK = cms.int32(0),
                FPRGCOMP = cms.int32(2),
                TRGENB9 = cms.int32(1),
                TRGENB8 = cms.int32(1),
                FHTPRF = cms.int32(1),
                LTF = cms.int32(0),
                TRGENB1 = cms.int32(1),
                TRGENB0 = cms.int32(1),
                FHISM = cms.int32(0),
                TRGENB2 = cms.int32(1),
                TRGENB5 = cms.int32(1),
                TRGENB4 = cms.int32(1),
                TRGENB7 = cms.int32(1),
                TRGENB6 = cms.int32(1),
                TRGENB15 = cms.int32(1),
                TRGENB14 = cms.int32(1),
                TRGENB11 = cms.int32(1),
                TRGENB10 = cms.int32(1),
                TRGENB13 = cms.int32(1),
                TRGENB12 = cms.int32(1),
                REUSEO = cms.int32(1),
                REUSEI = cms.int32(1),
                BTIC = cms.int32(32)
            ),
            TSPhiParameters = cms.PSet(
                TSMNOE1 = cms.bool(True),
                TSMNOE2 = cms.bool(False),
                TSSMSK1 = cms.int32(312),
                TSTREN9 = cms.bool(True),
                TSTREN8 = cms.bool(True),
                TSTREN11 = cms.bool(True),
                TSTREN3 = cms.bool(True),
                TSTREN2 = cms.bool(True),
                TSTREN1 = cms.bool(True),
                TSTREN0 = cms.bool(True),
                TSTREN7 = cms.bool(True),
                TSTREN6 = cms.bool(True),
                TSTREN5 = cms.bool(True),
                TSTREN4 = cms.bool(True),
                TSSCCE1 = cms.bool(True),
                TSSCCE2 = cms.bool(False),
                TSMCCE2 = cms.bool(False),
                TSTREN19 = cms.bool(True),
                TSMCCE1 = cms.bool(True),
                TSTREN17 = cms.bool(True),
                TSTREN16 = cms.bool(True),
                TSTREN15 = cms.bool(True),
                TSTREN14 = cms.bool(True),
                TSTREN13 = cms.bool(True),
                TSTREN12 = cms.bool(True),
                TSSMSK2 = cms.int32(312),
                TSTREN10 = cms.bool(True),
                TSMMSK2 = cms.int32(312),
                TSMMSK1 = cms.int32(312),
                TSMHSP = cms.int32(1),
                TSSNOE2 = cms.bool(False),
                TSSNOE1 = cms.bool(True),
                TSSCGS2 = cms.bool(True),
                TSSCCEC = cms.bool(False),
                TSMCCEC = cms.bool(False),
                TSMHTE2 = cms.bool(False),
                Debug = cms.untracked.bool(False),
                TSSHTE2 = cms.bool(False),
                TSMCGS1 = cms.bool(True),
                TSMCGS2 = cms.bool(True),
                TSSHTE1 = cms.bool(True),
                TSTREN22 = cms.bool(True),
                TSSNOEC = cms.bool(False),
                TSTREN20 = cms.bool(True),
                TSTREN21 = cms.bool(True),
                TSMGS1 = cms.int32(1),
                TSMGS2 = cms.int32(1),
                TSSHTEC = cms.bool(False),
                TSMWORD = cms.int32(255),
                TSMHTEC = cms.bool(False),
                TSSCGS1 = cms.bool(True),
                TSTREN23 = cms.bool(True),
                TSSGS2 = cms.int32(1),
                TSMNOEC = cms.bool(False),
                TSSGS1 = cms.int32(1),
                TSTREN18 = cms.bool(True),
                TSMHTE1 = cms.bool(True)
            ),
            TSThetaParameters = cms.PSet(
                Debug = cms.untracked.bool(False)
            ),
            Debug = cms.untracked.bool(False),
            DIGIOFFSET = cms.int32(500),
            SINCROTIME = cms.int32(0),
            BtiParameters = cms.PSet(
                KACCTHETA = cms.int32(1),
                WEN8 = cms.int32(1),
                ACH = cms.int32(1),
                DEAD = cms.int32(31),
                ACL = cms.int32(2),
                PTMS20 = cms.int32(1),
                Debug = cms.untracked.int32(0),
                PTMS22 = cms.int32(1),
                PTMS23 = cms.int32(1),
                PTMS24 = cms.int32(1),
                PTMS25 = cms.int32(1),
                PTMS26 = cms.int32(1),
                PTMS27 = cms.int32(1),
                PTMS28 = cms.int32(1),
                PTMS29 = cms.int32(1),
                SET = cms.int32(7),
                RON = cms.bool(True),
                WEN2 = cms.int32(1),
                LL = cms.int32(2),
                LH = cms.int32(21),
                WEN3 = cms.int32(1),
                RE43 = cms.int32(2),
                WEN0 = cms.int32(1),
                RL = cms.int32(42),
                WEN1 = cms.int32(1),
                RH = cms.int32(61),
                LTS = cms.int32(3),
                CH = cms.int32(41),
                CL = cms.int32(22),
                PTMS15 = cms.int32(1),
                PTMS14 = cms.int32(1),
                PTMS17 = cms.int32(1),
                PTMS16 = cms.int32(1),
                PTMS11 = cms.int32(1),
                PTMS10 = cms.int32(1),
                PTMS13 = cms.int32(1),
                PTMS12 = cms.int32(1),
                XON = cms.bool(False),
                WEN7 = cms.int32(1),
                WEN4 = cms.int32(1),
                WEN5 = cms.int32(1),
                PTMS19 = cms.int32(1),
                PTMS18 = cms.int32(1),
                PTMS31 = cms.int32(0),
                PTMS30 = cms.int32(0),
                PTMS5 = cms.int32(1),
                PTMS4 = cms.int32(1),
                PTMS7 = cms.int32(1),
                PTMS6 = cms.int32(1),
                PTMS1 = cms.int32(0),
                PTMS0 = cms.int32(0),
                PTMS3 = cms.int32(0),
                WEN6 = cms.int32(1),
                PTMS2 = cms.int32(0),
                PTMS9 = cms.int32(1),
                PTMS8 = cms.int32(1),
                ST43 = cms.int32(42),
                AC2 = cms.int32(3),
                AC1 = cms.int32(0),
                KMAX = cms.int32(64),
                PTMS21 = cms.int32(1)
            )
        )
    )
)


process.L2L3JetCorrectorKT6Calo = cms.ESSource("JetCorrectionServiceChain",
    correctors = cms.vstring('L2RelativeJetCorrectorKT6Calo', 
        'L3AbsoluteJetCorrectorKT6Calo'),
    label = cms.string('L2L3JetCorrectorKT6Calo')
)


process.L1MuCSCPtLutRcdSrc = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuCSCPtLutRcd'),
    firstValid = cms.vuint32(1)
)


process.L3JetCorrectorSC7Calo = cms.ESSource("L3AbsoluteCorrectionService",
    tagName = cms.string('Winter09_L3Absolute_SC7Calo'),
    label = cms.string('L3AbsoluteJetCorrectorSC7Calo')
)


process.l1CaloGeomRecordSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1CaloGeometryRecord'),
    firstValid = cms.vuint32(1)
)


process.L2L3JetCorrectorIC5PF = cms.ESSource("JetCorrectionServiceChain",
    correctors = cms.vstring('L2RelativeJetCorrectorIC5PF', 
        'L3AbsoluteJetCorrectorIC5PF'),
    label = cms.string('L2L3JetCorrectorIC5PF')
)


process.rpcconesrc = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1RPCConeBuilderRcd'),
    firstValid = cms.vuint32(1)
)


process.siStripGainFakeESSource = cms.ESSource("SiStripGainFakeESSource",
    appendToDataLabel = cms.string('fakeAPVGain'),
    file = cms.FileInPath('CalibTracker/SiStripCommon/data/SiStripDetInfo.dat')
)


process.emrcdsrc = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1EmEtScaleRcd'),
    firstValid = cms.vuint32(1)
)


process.l1GctChanMaskRecords = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GctChannelMaskRcd'),
    firstValid = cms.vuint32(1)
)


process.L3JetCorrectorKT6PF = cms.ESSource("L3PFAbsoluteCorrectionService",
    tagName = cms.string('Winter09_L3Absolute_KT6PF'),
    label = cms.string('L3AbsoluteJetCorrectorKT6PF')
)


process.qualut = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuDTQualPatternLutRcd'),
    firstValid = cms.vuint32(1)
)


process.L7PartonJetCorrectorIC5qJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('qJ'),
    tagName = cms.string('L7parton_IC5_080921'),
    label = cms.string('L7PartonJetCorrectorIC5qJet')
)


process.L2L3JetCorrectorIC5JPT = cms.ESSource("JetCorrectionServiceChain",
    correctors = cms.vstring('L2RelativeJetCorrectorIC5JPT', 
        'L3AbsoluteJetCorrectorIC5JPT'),
    label = cms.string('L2L3JetCorrectorIC5JPT')
)


process.L1MuTriggerScalesRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuTriggerScalesRcd'),
    firstValid = cms.vuint32(1)
)


process.L1GtTriggerMaskVetoTechTrigRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GtTriggerMaskVetoTechTrigRcd'),
    firstValid = cms.vuint32(1)
)


process.L3JetCorrectorSC7PF = cms.ESSource("L3PFAbsoluteCorrectionService",
    tagName = cms.string('Winter09_L3Absolute_SC7PF'),
    label = cms.string('L3AbsoluteJetCorrectorSC7PF')
)


process.L2JetCorrectorSC7PF = cms.ESSource("L2RelativeCorrectionService",
    tagName = cms.string('Winter09_L2Relative_SC7PF'),
    label = cms.string('L2RelativeJetCorrectorSC7PF')
)


process.L1MuTriggerPtScaleRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuTriggerPtScaleRcd'),
    firstValid = cms.vuint32(1)
)


process.l1CaloHcalScaleRecord = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1CaloHcalScaleRcd'),
    firstValid = cms.vuint32(1)
)


process.L3JetCorrectorIC5PF = cms.ESSource("L3PFAbsoluteCorrectionService",
    tagName = cms.string('Winter09_L3Absolute_IC5PF'),
    label = cms.string('L3AbsoluteJetCorrectorIC5PF')
)


process.L7PartonJetCorrectorIC5gJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('gJ'),
    tagName = cms.string('L7parton_IC5_080921'),
    label = cms.string('L7PartonJetCorrectorIC5gJet')
)


process.DTFakeVDriftESProducer = cms.ESSource("DTFakeVDriftESProducer",
    reso = cms.double(0.05),
    vDrift = cms.double(0.00543)
)


process.L3JetCorrectorKT4Calo = cms.ESSource("L3AbsoluteCorrectionService",
    tagName = cms.string('Winter09_L3Absolute_KT4Calo'),
    label = cms.string('L3AbsoluteJetCorrectorKT4Calo')
)


process.L7PartonJetCorrectorKT4tTop = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('tT'),
    tagName = cms.string('L7parton_KT4_080921'),
    label = cms.string('L7PartonJetCorrectorKT4tTop')
)


process.rpcconfsrc = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1RPCConfigRcd'),
    firstValid = cms.vuint32(1)
)


process.GlobalTag = cms.ESSource("PoolDBESSource",
    DBParameters = cms.PSet(
        authenticationPath = cms.untracked.string('.'),
        enableReadOnlySessionOnUpdateConnection = cms.untracked.bool(False),
        idleConnectionCleanupPeriod = cms.untracked.int32(10),
        messageLevel = cms.untracked.int32(0),
        enablePoolAutomaticCleanUp = cms.untracked.bool(False),
        enableConnectionSharing = cms.untracked.bool(True),
        connectionRetrialTimeOut = cms.untracked.int32(60),
        connectionTimeOut = cms.untracked.int32(60),
        connectionRetrialPeriod = cms.untracked.int32(10)
    ),
    BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
    connect = cms.string('frontier://FrontierProd/CMS_COND_21X_GLOBALTAG'),
    globaltag = cms.string('IDEAL_V11::All')
)


process.BTagRecord = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('JetTagComputerRecord'),
    firstValid = cms.vuint32(1)
)


process.L7PartonJetCorrectorIC5tTop = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('tT'),
    tagName = cms.string('L7parton_IC5_080921'),
    label = cms.string('L7PartonJetCorrectorIC5tTop')
)


process.L1GtTriggerMaskVetoAlgoTrigRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GtTriggerMaskVetoAlgoTrigRcd'),
    firstValid = cms.vuint32(1)
)


process.L2L3JetCorrectorKT4PF = cms.ESSource("JetCorrectionServiceChain",
    correctors = cms.vstring('L2RelativeJetCorrectorKT4PF', 
        'L3AbsoluteJetCorrectorKT4PF'),
    label = cms.string('L2L3JetCorrectorKT4PF')
)


process.rpchwconfsrc = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1RPCHwConfigRcd'),
    firstValid = cms.vuint32(1)
)


process.L1TriggerKeyRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1TriggerKeyRcd'),
    firstValid = cms.vuint32(1)
)


process.l1RctParamsRecords = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1RCTParametersRcd'),
    firstValid = cms.vuint32(1)
)


process.L7PartonJetCorrectorSC5bTop = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('bT'),
    tagName = cms.string('L7parton_SC5_080921'),
    label = cms.string('L7PartonJetCorrectorSC5bTop')
)


process.L2L3JetCorrectorSC7PF = cms.ESSource("JetCorrectionServiceChain",
    correctors = cms.vstring('L2RelativeJetCorrectorSC7PF', 
        'L3AbsoluteJetCorrectorSC7PF'),
    label = cms.string('L2L3JetCorrectorSC7PF')
)


process.cscBadChambers = cms.ESSource("PoolDBESSource",
    DBParameters = cms.PSet(
        authenticationMethod = cms.untracked.uint32(1),
        authenticationPath = cms.untracked.string('/afs/cern.ch/cms/DB/conddb')
    ),
    timetype = cms.string('runnumber'),
    toGet = cms.VPSet(cms.PSet(
        record = cms.string('CSCBadChambersRcd'),
        tag = cms.string('CSCBadChambers_realCal')
    )),
    connect = cms.string('sqlite_fip:CondCore/SQLiteData/data/BadChambers.db')
)


process.XMLIdealGeometryESSource = cms.ESSource("XMLIdealGeometryESSource",
    geomXMLFiles = cms.vstring('Geometry/CMSCommonData/data/materials.xml', 
        'Geometry/CMSCommonData/data/rotations.xml', 
        'Geometry/CMSCommonData/data/normal/cmsextent.xml', 
        'Geometry/CMSCommonData/data/cms.xml', 
        'Geometry/CMSCommonData/data/cmsMother.xml', 
        'Geometry/CMSCommonData/data/cmsTracker.xml', 
        'Geometry/CMSCommonData/data/caloBase.xml', 
        'Geometry/CMSCommonData/data/cmsCalo.xml', 
        'Geometry/CMSCommonData/data/muonBase.xml', 
        'Geometry/CMSCommonData/data/cmsMuon.xml', 
        'Geometry/CMSCommonData/data/mgnt.xml', 
        'Geometry/CMSCommonData/data/beampipe.xml', 
        'Geometry/CMSCommonData/data/cmsBeam.xml', 
        'Geometry/CMSCommonData/data/muonMB.xml', 
        'Geometry/CMSCommonData/data/muonMagnet.xml', 
        'Geometry/TrackerCommonData/data/pixfwdMaterials.xml', 
        'Geometry/TrackerCommonData/data/pixfwdCommon.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq1x2.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq1x5.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq2x3.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq2x4.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq2x5.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPanelBase.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPanel.xml', 
        'Geometry/TrackerCommonData/data/pixfwdBlade.xml', 
        'Geometry/TrackerCommonData/data/pixfwdNipple.xml', 
        'Geometry/TrackerCommonData/data/pixfwdDisk.xml', 
        'Geometry/TrackerCommonData/data/pixfwdCylinder.xml', 
        'Geometry/TrackerCommonData/data/pixfwd.xml', 
        'Geometry/TrackerCommonData/data/pixbarmaterial.xml', 
        'Geometry/TrackerCommonData/data/pixbarladder.xml', 
        'Geometry/TrackerCommonData/data/pixbarladderfull.xml', 
        'Geometry/TrackerCommonData/data/pixbarladderhalf.xml', 
        'Geometry/TrackerCommonData/data/pixbarlayer.xml', 
        'Geometry/TrackerCommonData/data/pixbarlayer0.xml', 
        'Geometry/TrackerCommonData/data/pixbarlayer1.xml', 
        'Geometry/TrackerCommonData/data/pixbarlayer2.xml', 
        'Geometry/TrackerCommonData/data/pixbar.xml', 
        'Geometry/TrackerCommonData/data/tibtidcommonmaterial.xml', 
        'Geometry/TrackerCommonData/data/tibmaterial.xml', 
        'Geometry/TrackerCommonData/data/tibmodpar.xml', 
        'Geometry/TrackerCommonData/data/tibmodule0.xml', 
        'Geometry/TrackerCommonData/data/tibmodule0a.xml', 
        'Geometry/TrackerCommonData/data/tibmodule0b.xml', 
        'Geometry/TrackerCommonData/data/tibmodule2.xml', 
        'Geometry/TrackerCommonData/data/tibstringpar.xml', 
        'Geometry/TrackerCommonData/data/tibstring0ll.xml', 
        'Geometry/TrackerCommonData/data/tibstring0lr.xml', 
        'Geometry/TrackerCommonData/data/tibstring0ul.xml', 
        'Geometry/TrackerCommonData/data/tibstring0ur.xml', 
        'Geometry/TrackerCommonData/data/tibstring0.xml', 
        'Geometry/TrackerCommonData/data/tibstring1ll.xml', 
        'Geometry/TrackerCommonData/data/tibstring1lr.xml', 
        'Geometry/TrackerCommonData/data/tibstring1ul.xml', 
        'Geometry/TrackerCommonData/data/tibstring1ur.xml', 
        'Geometry/TrackerCommonData/data/tibstring1.xml', 
        'Geometry/TrackerCommonData/data/tibstring2ll.xml', 
        'Geometry/TrackerCommonData/data/tibstring2lr.xml', 
        'Geometry/TrackerCommonData/data/tibstring2ul.xml', 
        'Geometry/TrackerCommonData/data/tibstring2ur.xml', 
        'Geometry/TrackerCommonData/data/tibstring2.xml', 
        'Geometry/TrackerCommonData/data/tibstring3ll.xml', 
        'Geometry/TrackerCommonData/data/tibstring3lr.xml', 
        'Geometry/TrackerCommonData/data/tibstring3ul.xml', 
        'Geometry/TrackerCommonData/data/tibstring3ur.xml', 
        'Geometry/TrackerCommonData/data/tibstring3.xml', 
        'Geometry/TrackerCommonData/data/tiblayerpar.xml', 
        'Geometry/TrackerCommonData/data/tiblayer0.xml', 
        'Geometry/TrackerCommonData/data/tiblayer1.xml', 
        'Geometry/TrackerCommonData/data/tiblayer2.xml', 
        'Geometry/TrackerCommonData/data/tiblayer3.xml', 
        'Geometry/TrackerCommonData/data/tib.xml', 
        'Geometry/TrackerCommonData/data/tidmaterial.xml', 
        'Geometry/TrackerCommonData/data/tidmodpar.xml', 
        'Geometry/TrackerCommonData/data/tidmodule0.xml', 
        'Geometry/TrackerCommonData/data/tidmodule0r.xml', 
        'Geometry/TrackerCommonData/data/tidmodule0l.xml', 
        'Geometry/TrackerCommonData/data/tidmodule1.xml', 
        'Geometry/TrackerCommonData/data/tidmodule1r.xml', 
        'Geometry/TrackerCommonData/data/tidmodule1l.xml', 
        'Geometry/TrackerCommonData/data/tidmodule2.xml', 
        'Geometry/TrackerCommonData/data/tidringpar.xml', 
        'Geometry/TrackerCommonData/data/tidring0.xml', 
        'Geometry/TrackerCommonData/data/tidring0f.xml', 
        'Geometry/TrackerCommonData/data/tidring0b.xml', 
        'Geometry/TrackerCommonData/data/tidring1.xml', 
        'Geometry/TrackerCommonData/data/tidring1f.xml', 
        'Geometry/TrackerCommonData/data/tidring1b.xml', 
        'Geometry/TrackerCommonData/data/tidring2.xml', 
        'Geometry/TrackerCommonData/data/tid.xml', 
        'Geometry/TrackerCommonData/data/tidf.xml', 
        'Geometry/TrackerCommonData/data/tidb.xml', 
        'Geometry/TrackerCommonData/data/tibtidservices.xml', 
        'Geometry/TrackerCommonData/data/tibtidservicesf.xml', 
        'Geometry/TrackerCommonData/data/tibtidservicesb.xml', 
        'Geometry/TrackerCommonData/data/tobmaterial.xml', 
        'Geometry/TrackerCommonData/data/tobmodpar.xml', 
        'Geometry/TrackerCommonData/data/tobmodule0.xml', 
        'Geometry/TrackerCommonData/data/tobmodule2.xml', 
        'Geometry/TrackerCommonData/data/tobmodule4.xml', 
        'Geometry/TrackerCommonData/data/tobrodpar.xml', 
        'Geometry/TrackerCommonData/data/tobrod0c.xml', 
        'Geometry/TrackerCommonData/data/tobrod0l.xml', 
        'Geometry/TrackerCommonData/data/tobrod0h.xml', 
        'Geometry/TrackerCommonData/data/tobrod0.xml', 
        'Geometry/TrackerCommonData/data/tobrod1l.xml', 
        'Geometry/TrackerCommonData/data/tobrod1h.xml', 
        'Geometry/TrackerCommonData/data/tobrod1.xml', 
        'Geometry/TrackerCommonData/data/tobrod2c.xml', 
        'Geometry/TrackerCommonData/data/tobrod2l.xml', 
        'Geometry/TrackerCommonData/data/tobrod2h.xml', 
        'Geometry/TrackerCommonData/data/tobrod2.xml', 
        'Geometry/TrackerCommonData/data/tobrod3l.xml', 
        'Geometry/TrackerCommonData/data/tobrod3h.xml', 
        'Geometry/TrackerCommonData/data/tobrod3.xml', 
        'Geometry/TrackerCommonData/data/tobrod4c.xml', 
        'Geometry/TrackerCommonData/data/tobrod4l.xml', 
        'Geometry/TrackerCommonData/data/tobrod4h.xml', 
        'Geometry/TrackerCommonData/data/tobrod4.xml', 
        'Geometry/TrackerCommonData/data/tobrod5l.xml', 
        'Geometry/TrackerCommonData/data/tobrod5h.xml', 
        'Geometry/TrackerCommonData/data/tobrod5.xml', 
        'Geometry/TrackerCommonData/data/tob.xml', 
        'Geometry/TrackerCommonData/data/tecmaterial.xml', 
        'Geometry/TrackerCommonData/data/tecmodpar.xml', 
        'Geometry/TrackerCommonData/data/tecmodule0.xml', 
        'Geometry/TrackerCommonData/data/tecmodule0r.xml', 
        'Geometry/TrackerCommonData/data/tecmodule0s.xml', 
        'Geometry/TrackerCommonData/data/tecmodule1.xml', 
        'Geometry/TrackerCommonData/data/tecmodule1r.xml', 
        'Geometry/TrackerCommonData/data/tecmodule1s.xml', 
        'Geometry/TrackerCommonData/data/tecmodule2.xml', 
        'Geometry/TrackerCommonData/data/tecmodule3.xml', 
        'Geometry/TrackerCommonData/data/tecmodule4.xml', 
        'Geometry/TrackerCommonData/data/tecmodule4r.xml', 
        'Geometry/TrackerCommonData/data/tecmodule4s.xml', 
        'Geometry/TrackerCommonData/data/tecmodule5.xml', 
        'Geometry/TrackerCommonData/data/tecmodule6.xml', 
        'Geometry/TrackerCommonData/data/tecpetpar.xml', 
        'Geometry/TrackerCommonData/data/tecring0.xml', 
        'Geometry/TrackerCommonData/data/tecring1.xml', 
        'Geometry/TrackerCommonData/data/tecring2.xml', 
        'Geometry/TrackerCommonData/data/tecring3.xml', 
        'Geometry/TrackerCommonData/data/tecring4.xml', 
        'Geometry/TrackerCommonData/data/tecring5.xml', 
        'Geometry/TrackerCommonData/data/tecring6.xml', 
        'Geometry/TrackerCommonData/data/tecring0f.xml', 
        'Geometry/TrackerCommonData/data/tecring1f.xml', 
        'Geometry/TrackerCommonData/data/tecring2f.xml', 
        'Geometry/TrackerCommonData/data/tecring3f.xml', 
        'Geometry/TrackerCommonData/data/tecring4f.xml', 
        'Geometry/TrackerCommonData/data/tecring5f.xml', 
        'Geometry/TrackerCommonData/data/tecring6f.xml', 
        'Geometry/TrackerCommonData/data/tecring0b.xml', 
        'Geometry/TrackerCommonData/data/tecring1b.xml', 
        'Geometry/TrackerCommonData/data/tecring2b.xml', 
        'Geometry/TrackerCommonData/data/tecring3b.xml', 
        'Geometry/TrackerCommonData/data/tecring4b.xml', 
        'Geometry/TrackerCommonData/data/tecring5b.xml', 
        'Geometry/TrackerCommonData/data/tecring6b.xml', 
        'Geometry/TrackerCommonData/data/tecpetalf.xml', 
        'Geometry/TrackerCommonData/data/tecpetalb.xml', 
        'Geometry/TrackerCommonData/data/tecpetal0.xml', 
        'Geometry/TrackerCommonData/data/tecpetal0f.xml', 
        'Geometry/TrackerCommonData/data/tecpetal0b.xml', 
        'Geometry/TrackerCommonData/data/tecpetal3.xml', 
        'Geometry/TrackerCommonData/data/tecpetal3f.xml', 
        'Geometry/TrackerCommonData/data/tecpetal3b.xml', 
        'Geometry/TrackerCommonData/data/tecpetal6f.xml', 
        'Geometry/TrackerCommonData/data/tecpetal6b.xml', 
        'Geometry/TrackerCommonData/data/tecpetal8f.xml', 
        'Geometry/TrackerCommonData/data/tecpetal8b.xml', 
        'Geometry/TrackerCommonData/data/tecwheel.xml', 
        'Geometry/TrackerCommonData/data/tecwheela.xml', 
        'Geometry/TrackerCommonData/data/tecwheelb.xml', 
        'Geometry/TrackerCommonData/data/tecwheelc.xml', 
        'Geometry/TrackerCommonData/data/tecwheeld.xml', 
        'Geometry/TrackerCommonData/data/tecwheel6.xml', 
        'Geometry/TrackerCommonData/data/tecservices.xml', 
        'Geometry/TrackerCommonData/data/tecbackplate.xml', 
        'Geometry/TrackerCommonData/data/tec.xml', 
        'Geometry/TrackerCommonData/data/trackermaterial.xml', 
        'Geometry/TrackerCommonData/data/tracker.xml', 
        'Geometry/TrackerCommonData/data/trackerpixbar.xml', 
        'Geometry/TrackerCommonData/data/trackerpixfwd.xml', 
        'Geometry/TrackerCommonData/data/trackertibtidservices.xml', 
        'Geometry/TrackerCommonData/data/trackertib.xml', 
        'Geometry/TrackerCommonData/data/trackertid.xml', 
        'Geometry/TrackerCommonData/data/trackertob.xml', 
        'Geometry/TrackerCommonData/data/trackertec.xml', 
        'Geometry/TrackerCommonData/data/trackerbulkhead.xml', 
        'Geometry/TrackerCommonData/data/trackerother.xml', 
        'Geometry/EcalCommonData/data/eregalgo.xml', 
        'Geometry/EcalCommonData/data/ebalgo.xml', 
        'Geometry/EcalCommonData/data/ebcon.xml', 
        'Geometry/EcalCommonData/data/ebrot.xml', 
        'Geometry/EcalCommonData/data/eecon.xml', 
        'Geometry/EcalCommonData/data/eefixed.xml', 
        'Geometry/EcalCommonData/data/eehier.xml', 
        'Geometry/EcalCommonData/data/eealgo.xml', 
        'Geometry/EcalCommonData/data/escon.xml', 
        'Geometry/EcalCommonData/data/esalgo.xml', 
        'Geometry/EcalCommonData/data/eeF.xml', 
        'Geometry/EcalCommonData/data/eeB.xml', 
        'Geometry/HcalCommonData/data/hcalrotations.xml', 
        'Geometry/HcalCommonData/data/hcalalgo.xml', 
        'Geometry/HcalCommonData/data/hcalbarrelalgo.xml', 
        'Geometry/HcalCommonData/data/hcalendcapalgo.xml', 
        'Geometry/HcalCommonData/data/hcalouteralgo.xml', 
        'Geometry/HcalCommonData/data/hcalforwardalgo.xml', 
        'Geometry/HcalCommonData/data/hcalforwardfibre.xml', 
        'Geometry/HcalCommonData/data/hcalforwardmaterial.xml', 
        'Geometry/MuonCommonData/data/mbCommon.xml', 
        'Geometry/MuonCommonData/data/mb1.xml', 
        'Geometry/MuonCommonData/data/mb2.xml', 
        'Geometry/MuonCommonData/data/mb3.xml', 
        'Geometry/MuonCommonData/data/mb4.xml', 
        'Geometry/MuonCommonData/data/muonYoke.xml', 
        'Geometry/MuonCommonData/data/mf.xml', 
        'Geometry/ForwardCommonData/data/forward.xml', 
        'Geometry/ForwardCommonData/data/forwardshield.xml', 
        'Geometry/ForwardCommonData/data/brmrotations.xml', 
        'Geometry/ForwardCommonData/data/brm.xml', 
        'Geometry/ForwardCommonData/data/totemMaterials.xml', 
        'Geometry/ForwardCommonData/data/totemRotations.xml', 
        'Geometry/ForwardCommonData/data/totemt1.xml', 
        'Geometry/ForwardCommonData/data/totemt2.xml', 
        'Geometry/ForwardCommonData/data/ionpump.xml', 
        'Geometry/MuonCommonData/data/muonNumbering.xml', 
        'Geometry/TrackerCommonData/data/trackerStructureTopology.xml', 
        'Geometry/TrackerSimData/data/trackersens.xml', 
        'Geometry/TrackerRecoData/data/trackerRecoMaterial.xml', 
        'Geometry/EcalSimData/data/ecalsens.xml', 
        'Geometry/HcalCommonData/data/hcalsens.xml', 
        'Geometry/HcalSimData/data/CaloUtil.xml', 
        'Geometry/MuonSimData/data/muonSens.xml', 
        'Geometry/DTGeometryBuilder/data/dtSpecsFilter.xml', 
        'Geometry/CSCGeometryBuilder/data/cscSpecsFilter.xml', 
        'Geometry/CSCGeometryBuilder/data/cscSpecs.xml', 
        'Geometry/RPCGeometryBuilder/data/RPCSpecs.xml', 
        'Geometry/ForwardCommonData/data/brmsens.xml', 
        'Geometry/HcalSimData/data/HcalProdCuts.xml', 
        'Geometry/EcalSimData/data/EcalProdCuts.xml', 
        'Geometry/TrackerSimData/data/trackerProdCuts.xml', 
        'Geometry/TrackerSimData/data/trackerProdCutsBEAM.xml', 
        'Geometry/MuonSimData/data/muonProdCuts.xml', 
        'Geometry/CMSCommonData/data/FieldParameters.xml'),
    rootNodeName = cms.string('cms:OCMS')
)


process.L3JetCorrectorIC5JPT = cms.ESSource("L3AbsoluteCorrectionService",
    tagName = cms.string('Winter09_L3Absolute_IC5JPT'),
    label = cms.string('L3AbsoluteJetCorrectorIC5JPT')
)


process.SiStripPedestalsFakeESSource = cms.ESSource("SiStripPedestalsFakeESSource",
    HighThValue = cms.double(5.0),
    printDebug = cms.untracked.bool(False),
    PedestalsValue = cms.uint32(30),
    file = cms.FileInPath('CalibTracker/SiStripCommon/data/SiStripDetInfo.dat'),
    LowThValue = cms.double(2.0)
)


process.L7PartonJetCorrectorIC5cJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('cJ'),
    tagName = cms.string('L7parton_IC5_080921'),
    label = cms.string('L7PartonJetCorrectorIC5cJet')
)


process.L2JetCorrectorSC7Calo = cms.ESSource("L2RelativeCorrectionService",
    tagName = cms.string('Winter09_L2Relative_SC7Calo'),
    label = cms.string('L2RelativeJetCorrectorSC7Calo')
)


process.L3JetCorrectorSC5Calo = cms.ESSource("L3AbsoluteCorrectionService",
    tagName = cms.string('Winter09_L3Absolute_SC5Calo'),
    label = cms.string('L3AbsoluteJetCorrectorSC5Calo')
)


process.L2JetCorrectorSC5PF = cms.ESSource("L2RelativeCorrectionService",
    tagName = cms.string('Winter09_L2Relative_SC5PF'),
    label = cms.string('L2RelativeJetCorrectorSC5PF')
)


process.L7PartonJetCorrectorIC5bTop = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('bT'),
    tagName = cms.string('L7parton_IC5_080921'),
    label = cms.string('L7PartonJetCorrectorIC5bTop')
)


process.L7PartonJetCorrectorKT6cTop = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('cT'),
    tagName = cms.string('L7parton_KT6_080921'),
    label = cms.string('L7PartonJetCorrectorKT6cTop')
)


process.L7PartonJetCorrectorIC5jJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('jJ'),
    tagName = cms.string('L7parton_IC5_080921'),
    label = cms.string('L7PartonJetCorrectorIC5jJet')
)


process.L7PartonJetCorrectorKT4cJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('cJ'),
    tagName = cms.string('L7parton_KT4_080921'),
    label = cms.string('L7PartonJetCorrectorKT4cJet')
)


process.eegeom = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('EcalMappingRcd'),
    firstValid = cms.vuint32(1)
)


process.l1GctConfigRecords = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GctHfLutSetupRcd'),
    firstValid = cms.vuint32(1)
)


process.etalut = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuDTEtaPatternLutRcd'),
    firstValid = cms.vuint32(1)
)


process.L1GtStableParametersRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GtStableParametersRcd'),
    firstValid = cms.vuint32(1)
)


process.dttfpar = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuDTTFParametersRcd'),
    firstValid = cms.vuint32(1)
)


process.L2L3JetCorrectorIC5Calo = cms.ESSource("JetCorrectionServiceChain",
    correctors = cms.vstring('L2RelativeJetCorrectorIC5Calo', 
        'L3AbsoluteJetCorrectorIC5Calo'),
    label = cms.string('L2L3JetCorrectorIC5Calo')
)


process.L2JetCorrectorSC5Calo = cms.ESSource("L2RelativeCorrectionService",
    tagName = cms.string('Winter09_L2Relative_SC5Calo'),
    label = cms.string('L2RelativeJetCorrectorSC5Calo')
)


process.L7PartonJetCorrectorSC5tTop = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('tT'),
    tagName = cms.string('L7parton_SC5_080921'),
    label = cms.string('L7PartonJetCorrectorSC5tTop')
)


process.L7PartonJetCorrectorKT6qJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('qJ'),
    tagName = cms.string('L7parton_KT6_080921'),
    label = cms.string('L7PartonJetCorrectorKT6qJet')
)


process.L7PartonJetCorrectorIC5cTop = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('cT'),
    tagName = cms.string('L7parton_IC5_080921'),
    label = cms.string('L7PartonJetCorrectorIC5cTop')
)


process.L1GtTriggerMaskAlgoTrigRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GtTriggerMaskAlgoTrigRcd'),
    firstValid = cms.vuint32(1)
)


process.L2JetCorrectorKT4Calo = cms.ESSource("L2RelativeCorrectionService",
    tagName = cms.string('Winter09_L2Relative_KT4Calo'),
    label = cms.string('L2RelativeJetCorrectorKT4Calo')
)


process.L7PartonJetCorrectorSC5cTop = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('cT'),
    tagName = cms.string('L7parton_SC5_080921'),
    label = cms.string('L7PartonJetCorrectorSC5cTop')
)


process.L7PartonJetCorrectorKT6jJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('jJ'),
    tagName = cms.string('L7parton_KT6_080921'),
    label = cms.string('L7PartonJetCorrectorKT6jJet')
)


process.L7PartonJetCorrectorKT4cTop = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('cT'),
    tagName = cms.string('L7parton_KT4_080921'),
    label = cms.string('L7PartonJetCorrectorKT4cTop')
)


process.L1GtTriggerMaskTechTrigRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GtTriggerMaskTechTrigRcd'),
    firstValid = cms.vuint32(1)
)


process.HepPDTESSource = cms.ESSource("HepPDTESSource",
    pdtFileName = cms.FileInPath('SimGeneral/HepPDTESSource/data/pythiaparticle.tbl')
)


process.L1MuCSCAlignmentRcdSrc = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuCSCTFAlignmentRcd'),
    firstValid = cms.vuint32(1)
)


process.L1GtPrescaleFactorsTechTrigRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GtPrescaleFactorsTechTrigRcd'),
    firstValid = cms.vuint32(1)
)


process.L7PartonJetCorrectorSC5cJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('cJ'),
    tagName = cms.string('L7parton_SC5_080921'),
    label = cms.string('L7PartonJetCorrectorSC5cJet')
)


process.L7PartonJetCorrectorSC7bTop = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('bT'),
    tagName = cms.string('L7parton_SC7_080921'),
    label = cms.string('L7PartonJetCorrectorSC7bTop')
)


process.L2JetCorrectorKT6Calo = cms.ESSource("L2RelativeCorrectionService",
    tagName = cms.string('Winter09_L2Relative_KT6Calo'),
    label = cms.string('L2RelativeJetCorrectorKT6Calo')
)


process.L3JetCorrectorIC5Calo = cms.ESSource("L3AbsoluteCorrectionService",
    tagName = cms.string('Winter09_L3Absolute_IC5Calo'),
    label = cms.string('L3AbsoluteJetCorrectorIC5Calo')
)


process.L1GtPrescaleFactorsAlgoTrigRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GtPrescaleFactorsAlgoTrigRcd'),
    firstValid = cms.vuint32(1)
)


process.L7PartonJetCorrectorKT6cJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('cJ'),
    tagName = cms.string('L7parton_KT6_080921'),
    label = cms.string('L7PartonJetCorrectorKT6cJet')
)


process.L7PartonJetCorrectorSC7qTop = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('qT'),
    tagName = cms.string('L7parton_SC7_080921'),
    label = cms.string('L7PartonJetCorrectorSC7qTop')
)


process.L1GtBoardMapsRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GtBoardMapsRcd'),
    firstValid = cms.vuint32(1)
)


process.L7PartonJetCorrectorIC5bJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('bJ'),
    tagName = cms.string('L7parton_IC5_080921'),
    label = cms.string('L7PartonJetCorrectorIC5bJet')
)


process.L7PartonJetCorrectorKT4qJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('qJ'),
    tagName = cms.string('L7parton_KT4_080921'),
    label = cms.string('L7PartonJetCorrectorKT4qJet')
)


process.L1GtTriggerMenuRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GtTriggerMenuRcd'),
    firstValid = cms.vuint32(1)
)


process.L2JetCorrectorIC5JPT = cms.ESSource("L2RelativeCorrectionService",
    tagName = cms.string('Winter09_L2Relative_IC5JPT'),
    label = cms.string('L2RelativeJetCorrectorIC5JPT')
)


process.L7PartonJetCorrectorKT6bJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('bJ'),
    tagName = cms.string('L7parton_KT6_080921'),
    label = cms.string('L7PartonJetCorrectorKT6bJet')
)


process.L2L3JetCorrectorKT6PF = cms.ESSource("JetCorrectionServiceChain",
    correctors = cms.vstring('L2RelativeJetCorrectorKT6PF', 
        'L3AbsoluteJetCorrectorKT6PF'),
    label = cms.string('L2L3JetCorrectorKT6PF')
)


process.L3JetCorrectorKT6Calo = cms.ESSource("L3AbsoluteCorrectionService",
    tagName = cms.string('Winter09_L3Absolute_KT6Calo'),
    label = cms.string('L3AbsoluteJetCorrectorKT6Calo')
)


process.L7PartonJetCorrectorKT4bTop = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('bT'),
    tagName = cms.string('L7parton_KT4_080921'),
    label = cms.string('L7PartonJetCorrectorKT4bTop')
)


process.L3JetCorrectorKT4PF = cms.ESSource("L3PFAbsoluteCorrectionService",
    tagName = cms.string('Winter09_L3Absolute_KT4PF'),
    label = cms.string('L3AbsoluteJetCorrectorKT4PF')
)


process.es_hardcode = cms.ESSource("HcalHardcodeCalibrations",
    toGet = cms.untracked.vstring('GainWidths', 
        'channelQuality', 
        'ZSThresholds')
)


process.L1MuGMTParametersRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuGMTParametersRcd'),
    firstValid = cms.vuint32(1)
)


process.magfield = cms.ESSource("XMLIdealGeometryESSource",
    geomXMLFiles = cms.vstring('Geometry/CMSCommonData/data/normal/cmsextent.xml', 
        'Geometry/CMSCommonData/data/cms.xml', 
        'Geometry/CMSCommonData/data/cmsMagneticField.xml', 
        'MagneticField/GeomBuilder/data/MagneticFieldVolumes_1103l.xml'),
    rootNodeName = cms.string('cmsMagneticField:MAGF')
)


process.L7PartonJetCorrectorSC7tTop = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('tT'),
    tagName = cms.string('L7parton_SC7_080921'),
    label = cms.string('L7PartonJetCorrectorSC7tTop')
)


process.L1GtParametersRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GtParametersRcd'),
    firstValid = cms.vuint32(1)
)


process.L7PartonJetCorrectorSC7cTop = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('cT'),
    tagName = cms.string('L7parton_SC7_080921'),
    label = cms.string('L7PartonJetCorrectorSC7cTop')
)


process.L2JetCorrectorIC5Calo = cms.ESSource("L2RelativeCorrectionService",
    tagName = cms.string('Winter09_L2Relative_IC5Calo'),
    label = cms.string('L2RelativeJetCorrectorIC5Calo')
)


process.L2JetCorrectorKT4PF = cms.ESSource("L2RelativeCorrectionService",
    tagName = cms.string('Winter09_L2Relative_KT4PF'),
    label = cms.string('L2RelativeJetCorrectorKT4PF')
)


process.L7PartonJetCorrectorSC7qJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('qJ'),
    tagName = cms.string('L7parton_SC7_080921'),
    label = cms.string('L7PartonJetCorrectorSC7qJet')
)


process.L7PartonJetCorrectorKT4jJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('jJ'),
    tagName = cms.string('L7parton_KT4_080921'),
    label = cms.string('L7PartonJetCorrectorKT4jJet')
)


process.L3JetCorrectorSC5PF = cms.ESSource("L3PFAbsoluteCorrectionService",
    tagName = cms.string('Winter09_L3Absolute_SC5PF'),
    label = cms.string('L3AbsoluteJetCorrectorSC5PF')
)


process.L1MuGMTScalesRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuGMTScalesRcd'),
    firstValid = cms.vuint32(1)
)


process.siStripLAFakeESSourceforSimulation = cms.ESSource("SiStripLAFakeESSource",
    appendToDataLabel = cms.string('fake'),
    TemperatureError = cms.double(10.0),
    Temperature = cms.double(297.0),
    HoleRHAllParameter = cms.double(0.7),
    ChargeMobility = cms.double(480.0),
    HoleBeta = cms.double(1.213),
    HoleSaturationVelocity = cms.double(8370000.0),
    file = cms.FileInPath('CalibTracker/SiStripCommon/data/SiStripDetInfo.dat'),
    AppliedVoltage = cms.double(150.0)
)


process.L7PartonJetCorrectorKT4bJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('bJ'),
    tagName = cms.string('L7parton_KT4_080921'),
    label = cms.string('L7PartonJetCorrectorKT4bJet')
)


process.L2JetCorrectorIC5PF = cms.ESSource("L2RelativeCorrectionService",
    tagName = cms.string('Winter09_L2Relative_IC5PF'),
    label = cms.string('L2RelativeJetCorrectorIC5PF')
)


process.l1GctJcNegParsRecords = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GctJetCounterNegativeEtaRcd'),
    firstValid = cms.vuint32(1)
)


process.L7PartonJetCorrectorSC7gJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('gJ'),
    tagName = cms.string('L7parton_SC7_080921'),
    label = cms.string('L7PartonJetCorrectorSC7gJet')
)


process.L1MuCSCTFConfigurationRcdSrc = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuCSCTFConfigurationRcd'),
    firstValid = cms.vuint32(1)
)


process.L2L3JetCorrectorSC5PF = cms.ESSource("JetCorrectionServiceChain",
    correctors = cms.vstring('L2RelativeJetCorrectorSC5PF', 
        'L3AbsoluteJetCorrectorSC5PF'),
    label = cms.string('L2L3JetCorrectorSC5PF')
)


process.L2L3JetCorrectorSC5Calo = cms.ESSource("JetCorrectionServiceChain",
    correctors = cms.vstring('L2RelativeJetCorrectorSC5Calo', 
        'L3AbsoluteJetCorrectorSC5Calo'),
    label = cms.string('L2L3JetCorrectorSC5Calo')
)


process.siStripBadChannelFakeESSource = cms.ESSource("SiStripBadChannelFakeESSource",
    appendToDataLabel = cms.string('')
)


process.L7PartonJetCorrectorSC7bJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('bJ'),
    tagName = cms.string('L7parton_SC7_080921'),
    label = cms.string('L7PartonJetCorrectorSC7bJet')
)


process.l1csctpconfsrc = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('CSCL1TPParametersRcd'),
    firstValid = cms.vuint32(0)
)


process.L1TriggerKeyListRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1TriggerKeyListRcd'),
    firstValid = cms.vuint32(1)
)


process.L7PartonJetCorrectorIC5qTop = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('qT'),
    tagName = cms.string('L7parton_IC5_080921'),
    label = cms.string('L7PartonJetCorrectorIC5qTop')
)


process.jetrcdsrc = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1JetEtScaleRcd'),
    firstValid = cms.vuint32(1)
)


process.L7PartonJetCorrectorKT6gJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('gJ'),
    tagName = cms.string('L7parton_KT6_080921'),
    label = cms.string('L7PartonJetCorrectorKT6gJet')
)


process.L7PartonJetCorrectorSC5qTop = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('qT'),
    tagName = cms.string('L7parton_SC5_080921'),
    label = cms.string('L7PartonJetCorrectorSC5qTop')
)


process.L7PartonJetCorrectorSC7cJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('cJ'),
    tagName = cms.string('L7parton_SC7_080921'),
    label = cms.string('L7PartonJetCorrectorSC7cJet')
)


process.L7PartonJetCorrectorKT4qTop = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('qT'),
    tagName = cms.string('L7parton_KT4_080921'),
    label = cms.string('L7PartonJetCorrectorKT4qTop')
)


process.l1CaloEcalScaleRecord = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1CaloEcalScaleRcd'),
    firstValid = cms.vuint32(1)
)


process.L2L3JetCorrectorSC7Calo = cms.ESSource("JetCorrectionServiceChain",
    correctors = cms.vstring('L2RelativeJetCorrectorSC7Calo', 
        'L3AbsoluteJetCorrectorSC7Calo'),
    label = cms.string('L2L3JetCorrectorSC7Calo')
)


process.philut = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuDTPhiLutRcd'),
    firstValid = cms.vuint32(1)
)


process.l1GctJcPosParsRecords = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GctJetCounterPositiveEtaRcd'),
    firstValid = cms.vuint32(1)
)


process.L2JetCorrectorKT6PF = cms.ESSource("L2RelativeCorrectionService",
    tagName = cms.string('Winter09_L2Relative_KT6PF'),
    label = cms.string('L2RelativeJetCorrectorKT6PF')
)


process.L7PartonJetCorrectorSC5qJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('qJ'),
    tagName = cms.string('L7parton_SC5_080921'),
    label = cms.string('L7PartonJetCorrectorSC5qJet')
)


process.extlut = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuDTExtLutRcd'),
    firstValid = cms.vuint32(1)
)


process.L7PartonJetCorrectorKT6qTop = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('qT'),
    tagName = cms.string('L7parton_KT6_080921'),
    label = cms.string('L7PartonJetCorrectorKT6qTop')
)


process.l1GctParamsRecords = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GctJetFinderParamsRcd'),
    firstValid = cms.vuint32(1)
)


process.rcdsrc = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('DTConfigManagerRcd'),
    firstValid = cms.vuint32(1)
)


process.L7PartonJetCorrectorSC5jJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('jJ'),
    tagName = cms.string('L7parton_SC5_080921'),
    label = cms.string('L7PartonJetCorrectorSC5jJet')
)


process.L7PartonJetCorrectorKT6tTop = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('tT'),
    tagName = cms.string('L7parton_KT6_080921'),
    label = cms.string('L7PartonJetCorrectorKT6tTop')
)


process.L7PartonJetCorrectorSC5gJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('gJ'),
    tagName = cms.string('L7parton_SC5_080921'),
    label = cms.string('L7PartonJetCorrectorSC5gJet')
)


process.siStripBadModuleFakeESSource = cms.ESSource("SiStripBadModuleFakeESSource",
    appendToDataLabel = cms.string('')
)


process.L7PartonJetCorrectorSC5bJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('bJ'),
    tagName = cms.string('L7parton_SC5_080921'),
    label = cms.string('L7PartonJetCorrectorSC5bJet')
)


process.ptalut = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuDTPtaLutRcd'),
    firstValid = cms.vuint32(1)
)


process.l1RctMaskRcds = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1RCTChannelMaskRcd'),
    firstValid = cms.vuint32(1)
)


process.L2L3JetCorrectorKT4Calo = cms.ESSource("JetCorrectionServiceChain",
    correctors = cms.vstring('L2RelativeJetCorrectorKT4Calo', 
        'L3AbsoluteJetCorrectorKT4Calo'),
    label = cms.string('L2L3JetCorrectorKT4Calo')
)


process.siStripBadFiberFakeESSource = cms.ESSource("SiStripBadFiberFakeESSource",
    appendToDataLabel = cms.string('')
)


process.L7PartonJetCorrectorKT6bTop = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('bT'),
    tagName = cms.string('L7parton_KT6_080921'),
    label = cms.string('L7PartonJetCorrectorKT6bTop')
)


process.L7PartonJetCorrectorSC7jJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('jJ'),
    tagName = cms.string('L7parton_SC7_080921'),
    label = cms.string('L7PartonJetCorrectorSC7jJet')
)


process.L7PartonJetCorrectorKT4gJet = cms.ESSource("L7PartonCorrectionService",
    section = cms.string('gJ'),
    tagName = cms.string('L7parton_KT4_080921'),
    label = cms.string('L7PartonJetCorrectorKT4gJet')
)


process.prefer("GlobalTag")

process.prefer("magfield")

process.GamIsoEcalFromClustsExtractorBlock = cms.PSet(
    ComponentName = cms.string('EgammaEcalExtractor'),
    superClusters = cms.InputTag("egammaSuperClusterMerger"),
    basicClusters = cms.InputTag("egammaBasicClusterMerger"),
    extRadius = cms.double(0.6),
    DepositLabel = cms.untracked.string(''),
    etMin = cms.double(-999.0),
    superClusterMatch = cms.bool(False)
)

process.MIsoTrackExtractorBlock = cms.PSet(
    Diff_z = cms.double(0.2),
    inputTrackCollection = cms.InputTag("generalTracks"),
    BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
    ComponentName = cms.string('TrackExtractor'),
    DR_Max = cms.double(1.0),
    Diff_r = cms.double(0.1),
    Chi2Prob_Min = cms.double(-1.0),
    DR_Veto = cms.double(0.01),
    NHits_Min = cms.uint32(0),
    Chi2Ndof_Max = cms.double(1e+64),
    Pt_Min = cms.double(-1.0),
    DepositLabel = cms.untracked.string(''),
    BeamlineOption = cms.string('BeamSpotFromEvent')
)

process.TSPhiParametersBlock = cms.PSet(
    TSPhiParameters = cms.PSet(
        TSMNOE1 = cms.bool(True),
        TSMNOE2 = cms.bool(False),
        TSSMSK1 = cms.int32(312),
        TSTREN9 = cms.bool(True),
        TSTREN8 = cms.bool(True),
        TSTREN11 = cms.bool(True),
        TSTREN3 = cms.bool(True),
        TSTREN2 = cms.bool(True),
        TSTREN1 = cms.bool(True),
        TSTREN0 = cms.bool(True),
        TSTREN7 = cms.bool(True),
        TSTREN6 = cms.bool(True),
        TSTREN5 = cms.bool(True),
        TSTREN4 = cms.bool(True),
        TSSCCE1 = cms.bool(True),
        TSSCCE2 = cms.bool(False),
        TSMCCE2 = cms.bool(False),
        TSTREN19 = cms.bool(True),
        TSMCCE1 = cms.bool(True),
        TSTREN17 = cms.bool(True),
        TSTREN16 = cms.bool(True),
        TSTREN15 = cms.bool(True),
        TSTREN14 = cms.bool(True),
        TSTREN13 = cms.bool(True),
        TSTREN12 = cms.bool(True),
        TSSMSK2 = cms.int32(312),
        TSTREN10 = cms.bool(True),
        TSMMSK2 = cms.int32(312),
        TSMMSK1 = cms.int32(312),
        TSMHSP = cms.int32(1),
        TSSNOE2 = cms.bool(False),
        TSSNOE1 = cms.bool(True),
        TSSCGS2 = cms.bool(True),
        TSSCCEC = cms.bool(False),
        TSMCCEC = cms.bool(False),
        TSMHTE2 = cms.bool(False),
        Debug = cms.untracked.bool(False),
        TSSHTE2 = cms.bool(False),
        TSMCGS1 = cms.bool(True),
        TSMCGS2 = cms.bool(True),
        TSSHTE1 = cms.bool(True),
        TSTREN22 = cms.bool(True),
        TSSNOEC = cms.bool(False),
        TSTREN20 = cms.bool(True),
        TSTREN21 = cms.bool(True),
        TSMGS1 = cms.int32(1),
        TSMGS2 = cms.int32(1),
        TSSHTEC = cms.bool(False),
        TSMWORD = cms.int32(255),
        TSMHTEC = cms.bool(False),
        TSSCGS1 = cms.bool(True),
        TSTREN23 = cms.bool(True),
        TSSGS2 = cms.int32(1),
        TSMNOEC = cms.bool(False),
        TSSGS1 = cms.int32(1),
        TSTREN18 = cms.bool(True),
        TSMHTE1 = cms.bool(True)
    )
)

process.EleIsoHcalFromTowersExtractorBlock = cms.PSet(
    caloTowers = cms.InputTag("towerMaker"),
    ComponentName = cms.string('EgammaTowerExtractor'),
    intRadius = cms.double(0.0),
    extRadius = cms.double(0.6),
    DepositLabel = cms.untracked.string(''),
    etMin = cms.double(-999.0)
)

process.MIsoDepositParamGlobalViewMultiIOBlock = cms.PSet(
    ExtractForCandidate = cms.bool(False),
    inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
    MultipleDepositsFlag = cms.bool(True),
    MuonTrackRefType = cms.string('bestTrkSta'),
    InputType = cms.string('MuonCollection')
)

process.MIsoTrackAssociatorDefault = cms.PSet(
    TrackAssociatorParameterBlock = cms.PSet(
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(9999.0),
            dREcal = cms.double(9999.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(True),
            dREcalPreselection = cms.double(0.05),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(True),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.2),
            useMuon = cms.bool(True),
            useCalo = cms.bool(False),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(True)
        )
    ),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(1.0),
        dREcal = cms.double(1.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(False),
        dREcalPreselection = cms.double(1.0),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(False),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(1.0),
        useMuon = cms.bool(False),
        useCalo = cms.bool(True),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(False)
    )
)

process.TSThetaParametersBlock = cms.PSet(
    TSThetaParameters = cms.PSet(
        Debug = cms.untracked.bool(False)
    )
)

process.MIsoJetExtractorBlock = cms.PSet(
    TrackAssociatorParameterBlock = cms.PSet(
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(9999.0),
            dREcal = cms.double(9999.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(True),
            dREcalPreselection = cms.double(0.05),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(True),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.2),
            useMuon = cms.bool(True),
            useCalo = cms.bool(False),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(True)
        )
    ),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(0.5),
        dREcal = cms.double(0.5),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(False),
        dREcalPreselection = cms.double(0.5),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(False),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.5),
        useMuon = cms.bool(False),
        useCalo = cms.bool(True),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(False)
    ),
    PrintTimeReport = cms.untracked.bool(False),
    ExcludeMuonVeto = cms.bool(True),
    ComponentName = cms.string('JetExtractor'),
    DR_Max = cms.double(1.0),
    PropagatorName = cms.string('SteppingHelixPropagatorAny'),
    JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
    DR_Veto = cms.double(0.1),
    Threshold = cms.double(5.0)
)

process.MIsoTrackAssociatorTowers = cms.PSet(
    TrackAssociatorParameterBlock = cms.PSet(
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(9999.0),
            dREcal = cms.double(9999.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(True),
            dREcalPreselection = cms.double(0.05),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(True),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.2),
            useMuon = cms.bool(True),
            useCalo = cms.bool(False),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(True)
        )
    ),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(1.0),
        dREcal = cms.double(1.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(False),
        dREcalPreselection = cms.double(1.0),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(False),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(1.0),
        useMuon = cms.bool(False),
        useCalo = cms.bool(True),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(False)
    )
)

process.MIsoDepositParamGlobalViewIOBlock = cms.PSet(
    ExtractForCandidate = cms.bool(False),
    inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
    MultipleDepositsFlag = cms.bool(False),
    MuonTrackRefType = cms.string('bestTrkSta'),
    InputType = cms.string('MuonCollection')
)

process.MIsoDepositGlobalMultiIOBlock = cms.PSet(
    ExtractForCandidate = cms.bool(False),
    inputMuonCollection = cms.InputTag("globalMuons"),
    MultipleDepositsFlag = cms.bool(True),
    MuonTrackRefType = cms.string('track'),
    InputType = cms.string('TrackCollection')
)

process.FastjetParameters = cms.PSet(

)

process.EleIsoEcalSCVetoFromClustsExtractorBlock = cms.PSet(
    ComponentName = cms.string('EgammaEcalExtractor'),
    superClusters = cms.InputTag("egammaSuperClusterMerger"),
    basicClusters = cms.InputTag("egammaBasicClusterMerger"),
    extRadius = cms.double(0.6),
    DepositLabel = cms.untracked.string(''),
    etMin = cms.double(-999.0),
    superClusterMatch = cms.bool(True)
)

process.GamIsoHcalFromHitsExtractorBlock = cms.PSet(
    checkIsoInnRBarrel = cms.double(0.045),
    minCandEt = cms.double(15.0),
    checkIsoExtRBarrel = cms.double(0.4),
    checkIsoEtCutEndcap = cms.double(7.0),
    ComponentName = cms.string('EgammaHcalExtractor'),
    endcapEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
    checkIsoEtaStripBarrel = cms.double(0.02),
    intRadius = cms.double(0.0),
    checkIsoEtRecHitEndcap = cms.double(0.3),
    extRadius = cms.double(0.5),
    checkIsoEtCutBarrel = cms.double(8.0),
    checkIsoExtREndcap = cms.double(0.4),
    checkIsoEtRecHitBarrel = cms.double(0.08),
    DepositLabel = cms.untracked.string(''),
    checkIsoInnREndcap = cms.double(0.07),
    checkIsoEtaStripEndcap = cms.double(0.02),
    hcalRecHits = cms.InputTag("hbhereco"),
    etMin = cms.double(-999.0),
    barrelEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEB")
)

process.EleIsoEcalFromClustsExtractorBlock = cms.PSet(
    ComponentName = cms.string('EgammaEcalExtractor'),
    superClusters = cms.InputTag("egammaSuperClusterMerger"),
    basicClusters = cms.InputTag("egammaBasicClusterMerger"),
    extRadius = cms.double(0.6),
    DepositLabel = cms.untracked.string(''),
    etMin = cms.double(-999.0),
    superClusterMatch = cms.bool(False)
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

process.j2tParametersVX = cms.PSet(
    tracks = cms.InputTag("generalTracks"),
    coneSize = cms.double(0.5)
)

process.DTTPGParametersBlock = cms.PSet(
    DTTPGParameters = cms.PSet(
        SectCollParameters = cms.PSet(
            SCCSP5 = cms.int32(0),
            SCCSP2 = cms.int32(0),
            SCCSP3 = cms.int32(0),
            SCECF4 = cms.bool(False),
            SCCSP1 = cms.int32(0),
            SCECF2 = cms.bool(False),
            SCECF3 = cms.bool(False),
            SCCSP4 = cms.int32(0),
            SCECF1 = cms.bool(False),
            Debug = cms.untracked.bool(False)
        ),
        Debug = cms.untracked.bool(False),
        TUParameters = cms.PSet(
            TracoParameters = cms.PSet(
                SPRGCOMP = cms.int32(2),
                FHTMSK = cms.int32(0),
                DD = cms.int32(18),
                SSLMSK = cms.int32(0),
                LVALIDIFH = cms.int32(0),
                Debug = cms.untracked.int32(0),
                FSLMSK = cms.int32(0),
                SHTPRF = cms.int32(1),
                SHTMSK = cms.int32(0),
                TRGENB3 = cms.int32(1),
                SHISM = cms.int32(0),
                IBTIOFF = cms.int32(0),
                KPRGCOM = cms.int32(255),
                KRAD = cms.int32(0),
                FLTMSK = cms.int32(0),
                LTS = cms.int32(0),
                SLTMSK = cms.int32(0),
                FPRGCOMP = cms.int32(2),
                TRGENB9 = cms.int32(1),
                TRGENB8 = cms.int32(1),
                FHTPRF = cms.int32(1),
                LTF = cms.int32(0),
                TRGENB1 = cms.int32(1),
                TRGENB0 = cms.int32(1),
                FHISM = cms.int32(0),
                TRGENB2 = cms.int32(1),
                TRGENB5 = cms.int32(1),
                TRGENB4 = cms.int32(1),
                TRGENB7 = cms.int32(1),
                TRGENB6 = cms.int32(1),
                TRGENB15 = cms.int32(1),
                TRGENB14 = cms.int32(1),
                TRGENB11 = cms.int32(1),
                TRGENB10 = cms.int32(1),
                TRGENB13 = cms.int32(1),
                TRGENB12 = cms.int32(1),
                REUSEO = cms.int32(1),
                REUSEI = cms.int32(1),
                BTIC = cms.int32(32)
            ),
            TSPhiParameters = cms.PSet(
                TSMNOE1 = cms.bool(True),
                TSMNOE2 = cms.bool(False),
                TSSMSK1 = cms.int32(312),
                TSTREN9 = cms.bool(True),
                TSTREN8 = cms.bool(True),
                TSTREN11 = cms.bool(True),
                TSTREN3 = cms.bool(True),
                TSTREN2 = cms.bool(True),
                TSTREN1 = cms.bool(True),
                TSTREN0 = cms.bool(True),
                TSTREN7 = cms.bool(True),
                TSTREN6 = cms.bool(True),
                TSTREN5 = cms.bool(True),
                TSTREN4 = cms.bool(True),
                TSSCCE1 = cms.bool(True),
                TSSCCE2 = cms.bool(False),
                TSMCCE2 = cms.bool(False),
                TSTREN19 = cms.bool(True),
                TSMCCE1 = cms.bool(True),
                TSTREN17 = cms.bool(True),
                TSTREN16 = cms.bool(True),
                TSTREN15 = cms.bool(True),
                TSTREN14 = cms.bool(True),
                TSTREN13 = cms.bool(True),
                TSTREN12 = cms.bool(True),
                TSSMSK2 = cms.int32(312),
                TSTREN10 = cms.bool(True),
                TSMMSK2 = cms.int32(312),
                TSMMSK1 = cms.int32(312),
                TSMHSP = cms.int32(1),
                TSSNOE2 = cms.bool(False),
                TSSNOE1 = cms.bool(True),
                TSSCGS2 = cms.bool(True),
                TSSCCEC = cms.bool(False),
                TSMCCEC = cms.bool(False),
                TSMHTE2 = cms.bool(False),
                Debug = cms.untracked.bool(False),
                TSSHTE2 = cms.bool(False),
                TSMCGS1 = cms.bool(True),
                TSMCGS2 = cms.bool(True),
                TSSHTE1 = cms.bool(True),
                TSTREN22 = cms.bool(True),
                TSSNOEC = cms.bool(False),
                TSTREN20 = cms.bool(True),
                TSTREN21 = cms.bool(True),
                TSMGS1 = cms.int32(1),
                TSMGS2 = cms.int32(1),
                TSSHTEC = cms.bool(False),
                TSMWORD = cms.int32(255),
                TSMHTEC = cms.bool(False),
                TSSCGS1 = cms.bool(True),
                TSTREN23 = cms.bool(True),
                TSSGS2 = cms.int32(1),
                TSMNOEC = cms.bool(False),
                TSSGS1 = cms.int32(1),
                TSTREN18 = cms.bool(True),
                TSMHTE1 = cms.bool(True)
            ),
            TSThetaParameters = cms.PSet(
                Debug = cms.untracked.bool(False)
            ),
            Debug = cms.untracked.bool(False),
            DIGIOFFSET = cms.int32(500),
            SINCROTIME = cms.int32(0),
            BtiParameters = cms.PSet(
                KACCTHETA = cms.int32(1),
                WEN8 = cms.int32(1),
                ACH = cms.int32(1),
                DEAD = cms.int32(31),
                ACL = cms.int32(2),
                PTMS20 = cms.int32(1),
                Debug = cms.untracked.int32(0),
                PTMS22 = cms.int32(1),
                PTMS23 = cms.int32(1),
                PTMS24 = cms.int32(1),
                PTMS25 = cms.int32(1),
                PTMS26 = cms.int32(1),
                PTMS27 = cms.int32(1),
                PTMS28 = cms.int32(1),
                PTMS29 = cms.int32(1),
                SET = cms.int32(7),
                RON = cms.bool(True),
                WEN2 = cms.int32(1),
                LL = cms.int32(2),
                LH = cms.int32(21),
                WEN3 = cms.int32(1),
                RE43 = cms.int32(2),
                WEN0 = cms.int32(1),
                RL = cms.int32(42),
                WEN1 = cms.int32(1),
                RH = cms.int32(61),
                LTS = cms.int32(3),
                CH = cms.int32(41),
                CL = cms.int32(22),
                PTMS15 = cms.int32(1),
                PTMS14 = cms.int32(1),
                PTMS17 = cms.int32(1),
                PTMS16 = cms.int32(1),
                PTMS11 = cms.int32(1),
                PTMS10 = cms.int32(1),
                PTMS13 = cms.int32(1),
                PTMS12 = cms.int32(1),
                XON = cms.bool(False),
                WEN7 = cms.int32(1),
                WEN4 = cms.int32(1),
                WEN5 = cms.int32(1),
                PTMS19 = cms.int32(1),
                PTMS18 = cms.int32(1),
                PTMS31 = cms.int32(0),
                PTMS30 = cms.int32(0),
                PTMS5 = cms.int32(1),
                PTMS4 = cms.int32(1),
                PTMS7 = cms.int32(1),
                PTMS6 = cms.int32(1),
                PTMS1 = cms.int32(0),
                PTMS0 = cms.int32(0),
                PTMS3 = cms.int32(0),
                WEN6 = cms.int32(1),
                PTMS2 = cms.int32(0),
                PTMS9 = cms.int32(1),
                PTMS8 = cms.int32(1),
                ST43 = cms.int32(42),
                AC2 = cms.int32(3),
                AC1 = cms.int32(0),
                KMAX = cms.int32(64),
                PTMS21 = cms.int32(1)
            )
        )
    )
)

process.KtJetParameters = cms.PSet(
    Strategy = cms.string('Best')
)

process.MIsoTrackAssociatorJets = cms.PSet(
    TrackAssociatorParameterBlock = cms.PSet(
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(9999.0),
            dREcal = cms.double(9999.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(True),
            dREcalPreselection = cms.double(0.05),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(True),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.2),
            useMuon = cms.bool(True),
            useCalo = cms.bool(False),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(True)
        )
    ),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(0.5),
        dREcal = cms.double(0.5),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(False),
        dREcalPreselection = cms.double(0.5),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(False),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.5),
        useMuon = cms.bool(False),
        useCalo = cms.bool(True),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(False)
    )
)

process.MIsoDepositParamGlobalIOBlock = cms.PSet(
    ExtractForCandidate = cms.bool(False),
    inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
    MultipleDepositsFlag = cms.bool(False),
    MuonTrackRefType = cms.string('track'),
    InputType = cms.string('MuonCollection')
)

process.GamIsoTrackExtractorBlock = cms.PSet(
    BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
    DR_Max = cms.double(0.4),
    NHits_Min = cms.uint32(0),
    checkIsoInnRBarrel = cms.double(0.045),
    checkIsoExtRBarrel = cms.double(0.4),
    checkIsoEtaStripBarrel = cms.double(0.02),
    checkIsoEtRecHitEndcap = cms.double(0.3),
    Pt_Min = cms.double(-1.0),
    DepositLabel = cms.untracked.string(''),
    barrelEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
    Diff_z = cms.double(0.2),
    inputTrackCollection = cms.InputTag("generalTracks"),
    checkIsoEtCutEndcap = cms.double(7.0),
    endcapEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
    Diff_r = cms.double(0.1),
    Chi2Prob_Min = cms.double(-1.0),
    DR_Veto = cms.double(0.0),
    checkIsoEtCutBarrel = cms.double(8.0),
    Chi2Ndof_Max = cms.double(1e+64),
    checkIsoEtRecHitBarrel = cms.double(0.08),
    checkIsoInnREndcap = cms.double(0.07),
    BeamlineOption = cms.string('BeamSpotFromEvent'),
    minCandEt = cms.double(15.0),
    ComponentName = cms.string('EgammaTrackExtractor'),
    checkIsoExtREndcap = cms.double(0.4),
    checkIsoEtaStripEndcap = cms.double(0.02)
)

process.CaloJetParameters = cms.PSet(
    correctInputToSignalVertex = cms.bool(True),
    verbose = cms.untracked.bool(False),
    jetPtMin = cms.double(1.0),
    pvCollection = cms.InputTag("offlinePrimaryVertices"),
    inputEtMin = cms.double(0.5),
    jetType = cms.untracked.string('CaloJet'),
    src = cms.InputTag("towerMaker"),
    inputEMin = cms.double(0.0)
)

process.GamIsoHcalFromTowersExtractorBlock = cms.PSet(
    caloTowers = cms.InputTag("towerMaker"),
    ComponentName = cms.string('EgammaTowerExtractor'),
    intRadius = cms.double(0.0),
    extRadius = cms.double(0.6),
    DepositLabel = cms.untracked.string(''),
    etMin = cms.double(-999.0)
)

process.MIsoTrackExtractorGsBlock = cms.PSet(
    Diff_z = cms.double(0.2),
    inputTrackCollection = cms.InputTag("ctfGSWithMaterialTracks"),
    BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
    ComponentName = cms.string('TrackExtractor'),
    DR_Max = cms.double(1.0),
    Diff_r = cms.double(0.1),
    Chi2Prob_Min = cms.double(-1.0),
    DR_Veto = cms.double(0.01),
    NHits_Min = cms.uint32(0),
    Chi2Ndof_Max = cms.double(1e+64),
    Pt_Min = cms.double(-1.0),
    DepositLabel = cms.untracked.string(''),
    BeamlineOption = cms.string('BeamSpotFromEvent')
)

process.MIsoCaloExtractorHLTBlock = cms.PSet(
    DR_Veto_H = cms.double(0.1),
    Vertex_Constraint_Z = cms.bool(False),
    Threshold_H = cms.double(0.5),
    ComponentName = cms.string('CaloExtractor'),
    Threshold_E = cms.double(0.2),
    DR_Max = cms.double(1.0),
    DR_Veto_E = cms.double(0.07),
    Weight_E = cms.double(1.5),
    Vertex_Constraint_XY = cms.bool(False),
    DepositLabel = cms.untracked.string('EcalPlusHcal'),
    CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
    Weight_H = cms.double(1.0)
)

process.patEventContent = cms.PSet(
    outputCommands = cms.untracked.vstring('drop *', 
        'keep recoGenParticles_genParticles_*_*', 
        'keep *_genEventScale_*_*', 
        'keep *_genEventWeight_*_*', 
        'keep *_genEventPdfInfo_*_*', 
        'keep edmTriggerResults_TriggerResults_*_HLT', 
        'keep *_hltTriggerSummaryAOD_*_*', 
        'keep *_offlineBeamSpot_*_*', 
        'keep *_offlinePrimaryVertices_*_*', 
        'keep recoTracks_generalTracks_*_*', 
        'keep *_towerMaker_*_*', 
        'keep *_selectedLayer1Photons_*_*', 
        'keep *_selectedLayer1Electrons_*_*', 
        'keep *_selectedLayer1Muons_*_*', 
        'keep *_selectedLayer1Taus_*_*', 
        'keep *_selectedLayer1Jets_*_*', 
        'keep *_selectedLayer1METs_*_*', 
        'keep patPFParticles_*_*_*', 
        'keep *_selectedLayer1Hemispheres_*_*', 
        'drop *_genParticles_*_*', 
        'keep *_genEventScale_*_*', 
        'drop *_generalTracks_*_*', 
        'keep *_goodTracks_*_*', 
        'drop *_towerMaker_*_*', 
        'drop *_selectedLayer1Taus_*_*', 
        'drop *_selectedLayer1Hemispheres_*_*', 
        'drop *_selectedLayer1Photons_*_*')
)

process.EleIsoEcalFromHitsExtractorBlock = cms.PSet(
    tryBoth = cms.bool(True),
    intStrip = cms.double(0.0),
    subtractSuperClusterEnergy = cms.bool(False),
    checkIsoInnRBarrel = cms.double(0.0),
    checkIsoExtRBarrel = cms.double(0.01),
    etMin = cms.double(-999.0),
    checkIsoEtaStripBarrel = cms.double(0.0),
    checkIsoEtRecHitEndcap = cms.double(0.3),
    DepositLabel = cms.untracked.string(''),
    detector = cms.string('Ecal'),
    barrelEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
    isolationVariable = cms.string('et'),
    checkIsoEtCutEndcap = cms.double(10000.0),
    endcapEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
    intRadius = cms.double(0.0),
    energyMin = cms.double(0.08),
    extRadius = cms.double(0.5),
    checkIsoEtCutBarrel = cms.double(10000.0),
    checkIsoEtRecHitBarrel = cms.double(0.08),
    checkIsoInnREndcap = cms.double(0.0),
    minCandEt = cms.double(0.0),
    barrelRecHits = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
    ComponentName = cms.string('EgammaRecHitExtractor'),
    endcapRecHits = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
    checkIsoExtREndcap = cms.double(0.01),
    checkIsoEtaStripEndcap = cms.double(0.0)
)

process.MIsoTrackExtractorCtfBlock = cms.PSet(
    Diff_z = cms.double(0.2),
    inputTrackCollection = cms.InputTag("generalTracks"),
    BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
    ComponentName = cms.string('TrackExtractor'),
    DR_Max = cms.double(1.0),
    Diff_r = cms.double(0.1),
    Chi2Prob_Min = cms.double(-1.0),
    DR_Veto = cms.double(0.01),
    NHits_Min = cms.uint32(0),
    Chi2Ndof_Max = cms.double(1e+64),
    Pt_Min = cms.double(-1.0),
    DepositLabel = cms.untracked.string(''),
    BeamlineOption = cms.string('BeamSpotFromEvent')
)

process.MIsoTrackAssociatorHits = cms.PSet(
    TrackAssociatorParameterBlock = cms.PSet(
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(9999.0),
            dREcal = cms.double(9999.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(True),
            dREcalPreselection = cms.double(0.05),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(True),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.2),
            useMuon = cms.bool(True),
            useCalo = cms.bool(False),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(True)
        )
    ),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(1.0),
        dREcal = cms.double(1.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(1.0),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(1.0),
        useMuon = cms.bool(False),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    )
)

process.trackSelectionBlock = cms.PSet(
    trackSelection = cms.PSet(
        totalHitsMin = cms.uint32(0),
        jetDeltaRMax = cms.double(0.3),
        qualityClass = cms.string('highPurity'),
        pixelHitsMin = cms.uint32(0),
        sip3dSigMin = cms.double(-99999.9),
        sip3dSigMax = cms.double(99999.9),
        maxDistToAxis = cms.double(0.07),
        sip2dValMax = cms.double(99999.9),
        maxDecayLen = cms.double(5),
        ptMin = cms.double(0.0),
        sip2dSigMax = cms.double(99999.9),
        sip2dSigMin = cms.double(-99999.9),
        sip3dValMax = cms.double(99999.9),
        sip3dValMin = cms.double(-99999.9),
        sip2dValMin = cms.double(-99999.9),
        normChi2Max = cms.double(99999.9)
    )
)

process.CATopJetParameters = cms.PSet(
    ptBins = cms.vdouble(500, 800, 1300),
    sumEtEtaCut = cms.double(3.0),
    subjetColl = cms.string('caTopSubJets'),
    ptFracBins = cms.vdouble(0.1, 0.05, 0.05),
    rBins = cms.vdouble(0.8, 0.6, 0.4),
    algorithm = cms.int32(1),
    etFrac = cms.double(0.7),
    useMaxTower = cms.bool(False),
    nCellBins = cms.vint32(1, 1, 1),
    centralEtaCut = cms.double(2.5),
    debugLevel = cms.untracked.int32(0),
    useAdjacency = cms.bool(False)
)

process.patLayer1EventContent = cms.PSet(
    outputCommands = cms.untracked.vstring('keep recoGenParticles_genParticles_*_*', 
        'keep *_genEventScale_*_*', 
        'keep *_genEventWeight_*_*', 
        'keep *_genEventPdfInfo_*_*', 
        'keep edmTriggerResults_TriggerResults_*_HLT', 
        'keep *_hltTriggerSummaryAOD_*_*', 
        'keep *_offlineBeamSpot_*_*', 
        'keep *_offlinePrimaryVertices_*_*', 
        'keep recoTracks_generalTracks_*_*', 
        'keep *_towerMaker_*_*', 
        'keep *_selectedLayer1Photons_*_*', 
        'keep *_selectedLayer1Electrons_*_*', 
        'keep *_selectedLayer1Muons_*_*', 
        'keep *_selectedLayer1Taus_*_*', 
        'keep *_selectedLayer1Jets_*_*', 
        'keep *_selectedLayer1METs_*_*', 
        'keep patPFParticles_*_*_*', 
        'keep *_selectedLayer1Hemispheres_*_*')
)

process.MIsoCaloExtractorByAssociatorHitsBlock = cms.PSet(
    TrackAssociatorParameterBlock = cms.PSet(
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(9999.0),
            dREcal = cms.double(9999.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(True),
            dREcalPreselection = cms.double(0.05),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(True),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.2),
            useMuon = cms.bool(True),
            useCalo = cms.bool(False),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(True)
        )
    ),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(1.0),
        dREcal = cms.double(1.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(1.0),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(1.0),
        useMuon = cms.bool(False),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    PropagatorName = cms.string('SteppingHelixPropagatorAny'),
    NoiseTow_EB = cms.double(0.04),
    Noise_EE = cms.double(0.1),
    PrintTimeReport = cms.untracked.bool(False),
    DR_Veto_E = cms.double(0.07),
    NoiseTow_EE = cms.double(0.15),
    Threshold_HO = cms.double(0.1),
    ComponentName = cms.string('CaloExtractorByAssociator'),
    Noise_HO = cms.double(0.2),
    DR_Max = cms.double(1.0),
    Noise_EB = cms.double(0.025),
    Threshold_E = cms.double(0.025),
    Noise_HB = cms.double(0.2),
    UseRecHitsFlag = cms.bool(True),
    Threshold_H = cms.double(0.1),
    DR_Veto_H = cms.double(0.1),
    DepositLabel = cms.untracked.string('Cal'),
    Noise_HE = cms.double(0.2),
    DR_Veto_HO = cms.double(0.1),
    DepositInstanceLabels = cms.vstring('ecal', 
        'hcal', 
        'ho')
)

process.GamIsoEcalSCVetoFromClustsExtractorBlock = cms.PSet(
    ComponentName = cms.string('EgammaEcalExtractor'),
    superClusters = cms.InputTag("egammaSuperClusterMerger"),
    basicClusters = cms.InputTag("egammaBasicClusterMerger"),
    extRadius = cms.double(0.6),
    DepositLabel = cms.untracked.string(''),
    etMin = cms.double(-999.0),
    superClusterMatch = cms.bool(True)
)

process.CondDBSetup = cms.PSet(
    DBParameters = cms.PSet(
        authenticationPath = cms.untracked.string('.'),
        enableReadOnlySessionOnUpdateConnection = cms.untracked.bool(False),
        idleConnectionCleanupPeriod = cms.untracked.int32(10),
        messageLevel = cms.untracked.int32(0),
        enablePoolAutomaticCleanUp = cms.untracked.bool(False),
        enableConnectionSharing = cms.untracked.bool(True),
        connectionRetrialTimeOut = cms.untracked.int32(60),
        connectionTimeOut = cms.untracked.int32(60),
        connectionRetrialPeriod = cms.untracked.int32(10)
    )
)

process.trackPseudoSelectionBlock = cms.PSet(
    trackPseudoSelection = cms.PSet(
        totalHitsMin = cms.uint32(0),
        jetDeltaRMax = cms.double(0.3),
        qualityClass = cms.string('highPurity'),
        pixelHitsMin = cms.uint32(0),
        sip3dSigMin = cms.double(-99999.9),
        sip3dSigMax = cms.double(99999.9),
        maxDistToAxis = cms.double(0.07),
        sip2dValMax = cms.double(99999.9),
        maxDecayLen = cms.double(5),
        ptMin = cms.double(0.0),
        sip2dSigMax = cms.double(99999.9),
        sip2dSigMin = cms.double(2.0),
        sip3dValMax = cms.double(99999.9),
        sip3dValMin = cms.double(-99999.9),
        sip2dValMin = cms.double(-99999.9),
        normChi2Max = cms.double(99999.9)
    )
)

process.EleIsoHcalFromHitsExtractorBlock = cms.PSet(
    checkIsoInnRBarrel = cms.double(0.0),
    minCandEt = cms.double(0.0),
    checkIsoExtRBarrel = cms.double(0.01),
    checkIsoEtCutEndcap = cms.double(10000.0),
    ComponentName = cms.string('EgammaHcalExtractor'),
    endcapEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
    checkIsoEtaStripBarrel = cms.double(0.0),
    intRadius = cms.double(0.0),
    checkIsoEtRecHitEndcap = cms.double(0.3),
    extRadius = cms.double(0.5),
    checkIsoEtCutBarrel = cms.double(10000.0),
    checkIsoExtREndcap = cms.double(0.01),
    checkIsoEtRecHitBarrel = cms.double(0.08),
    DepositLabel = cms.untracked.string(''),
    checkIsoInnREndcap = cms.double(0.0),
    checkIsoEtaStripEndcap = cms.double(0.0),
    hcalRecHits = cms.InputTag("hbhereco"),
    etMin = cms.double(-999.0),
    barrelEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEB")
)

process.jcSetup1 = cms.PSet(
    jetCountersNegativeWheel = cms.VPSet(cms.PSet(
        cutDescriptionList = cms.vstring('JC_minRank_1')
    ), 
        cms.PSet(
            cutDescriptionList = cms.vstring('JC_minRank_1', 
                'JC_centralEta_6')
        ), 
        cms.PSet(
            cutDescriptionList = cms.vstring('JC_minRank_11')
        ), 
        cms.PSet(
            cutDescriptionList = cms.vstring('JC_minRank_11', 
                'JC_centralEta_6')
        ), 
        cms.PSet(
            cutDescriptionList = cms.vstring('JC_minRank_19')
        )),
    jetCountersPositiveWheel = cms.VPSet(cms.PSet(
        cutDescriptionList = cms.vstring('JC_minRank_1')
    ), 
        cms.PSet(
            cutDescriptionList = cms.vstring('JC_minRank_1', 
                'JC_centralEta_6')
        ), 
        cms.PSet(
            cutDescriptionList = cms.vstring('JC_minRank_11')
        ), 
        cms.PSet(
            cutDescriptionList = cms.vstring('JC_minRank_11', 
                'JC_centralEta_6')
        ), 
        cms.PSet(
            cutDescriptionList = cms.vstring('JC_minRank_19')
        ))
)

process.TracoParametersBlock = cms.PSet(
    TracoParameters = cms.PSet(
        SPRGCOMP = cms.int32(2),
        FHTMSK = cms.int32(0),
        DD = cms.int32(18),
        SSLMSK = cms.int32(0),
        LVALIDIFH = cms.int32(0),
        Debug = cms.untracked.int32(0),
        FSLMSK = cms.int32(0),
        SHTPRF = cms.int32(1),
        SHTMSK = cms.int32(0),
        TRGENB3 = cms.int32(1),
        SHISM = cms.int32(0),
        IBTIOFF = cms.int32(0),
        KPRGCOM = cms.int32(255),
        KRAD = cms.int32(0),
        FLTMSK = cms.int32(0),
        LTS = cms.int32(0),
        SLTMSK = cms.int32(0),
        FPRGCOMP = cms.int32(2),
        TRGENB9 = cms.int32(1),
        TRGENB8 = cms.int32(1),
        FHTPRF = cms.int32(1),
        LTF = cms.int32(0),
        TRGENB1 = cms.int32(1),
        TRGENB0 = cms.int32(1),
        FHISM = cms.int32(0),
        TRGENB2 = cms.int32(1),
        TRGENB5 = cms.int32(1),
        TRGENB4 = cms.int32(1),
        TRGENB7 = cms.int32(1),
        TRGENB6 = cms.int32(1),
        TRGENB15 = cms.int32(1),
        TRGENB14 = cms.int32(1),
        TRGENB11 = cms.int32(1),
        TRGENB10 = cms.int32(1),
        TRGENB13 = cms.int32(1),
        TRGENB12 = cms.int32(1),
        REUSEO = cms.int32(1),
        REUSEI = cms.int32(1),
        BTIC = cms.int32(32)
    )
)

process.combinedSecondaryVertexCommon = cms.PSet(
    trackPseudoSelection = cms.PSet(
        totalHitsMin = cms.uint32(0),
        jetDeltaRMax = cms.double(0.3),
        qualityClass = cms.string('highPurity'),
        pixelHitsMin = cms.uint32(0),
        sip3dSigMin = cms.double(-99999.9),
        sip3dSigMax = cms.double(99999.9),
        maxDistToAxis = cms.double(0.07),
        sip2dValMax = cms.double(99999.9),
        maxDecayLen = cms.double(5),
        ptMin = cms.double(0.0),
        sip2dSigMax = cms.double(99999.9),
        sip2dSigMin = cms.double(2.0),
        sip3dValMax = cms.double(99999.9),
        sip3dValMin = cms.double(-99999.9),
        sip2dValMin = cms.double(-99999.9),
        normChi2Max = cms.double(99999.9)
    ),
    trackSelection = cms.PSet(
        totalHitsMin = cms.uint32(0),
        jetDeltaRMax = cms.double(0.3),
        qualityClass = cms.string('highPurity'),
        pixelHitsMin = cms.uint32(0),
        sip3dSigMin = cms.double(-99999.9),
        sip3dSigMax = cms.double(99999.9),
        maxDistToAxis = cms.double(0.07),
        sip2dValMax = cms.double(99999.9),
        maxDecayLen = cms.double(5),
        ptMin = cms.double(0.0),
        sip2dSigMax = cms.double(99999.9),
        sip2dSigMin = cms.double(-99999.9),
        sip3dValMax = cms.double(99999.9),
        sip3dValMin = cms.double(-99999.9),
        sip2dValMin = cms.double(-99999.9),
        normChi2Max = cms.double(99999.9)
    ),
    useTrackWeights = cms.bool(True),
    pseudoMultiplicityMin = cms.uint32(2),
    correctVertexMass = cms.bool(True),
    trackPairV0Filter = cms.PSet(
        k0sMassWindow = cms.double(0.03)
    ),
    charmCut = cms.double(1.5),
    vertexFlip = cms.bool(False),
    minimumTrackWeight = cms.double(0.5),
    pseudoVertexV0Filter = cms.PSet(
        k0sMassWindow = cms.double(0.05)
    ),
    trackMultiplicityMin = cms.uint32(3),
    trackSort = cms.string('sip2dSig'),
    trackFlip = cms.bool(False)
)

process.MIsoDepositViewIOBlock = cms.PSet(
    ExtractForCandidate = cms.bool(False),
    inputMuonCollection = cms.InputTag("muons"),
    MultipleDepositsFlag = cms.bool(False),
    MuonTrackRefType = cms.string('bestTrkSta'),
    InputType = cms.string('MuonCollection')
)

process.vertexTrackSelectionBlock = cms.PSet(
    trackSelection = cms.PSet(
        totalHitsMin = cms.uint32(8),
        jetDeltaRMax = cms.double(0.3),
        qualityClass = cms.string('highPurity'),
        pixelHitsMin = cms.uint32(2),
        sip3dSigMin = cms.double(-99999.9),
        sip3dSigMax = cms.double(99999.9),
        maxDistToAxis = cms.double(0.2),
        sip2dValMax = cms.double(99999.9),
        maxDecayLen = cms.double(99999.9),
        ptMin = cms.double(1.0),
        sip2dSigMax = cms.double(99999.9),
        sip2dSigMin = cms.double(-99999.9),
        sip3dValMax = cms.double(99999.9),
        sip3dValMin = cms.double(-99999.9),
        sip2dValMin = cms.double(-99999.9),
        normChi2Max = cms.double(99999.9)
    )
)

process.FastjetNoPU = cms.PSet(
    Active_Area_Repeats = cms.int32(0),
    GhostArea = cms.double(1.0),
    Ghost_EtaMax = cms.double(0.0),
    UE_Subtraction = cms.string('no')
)

process.TUParamsBlock = cms.PSet(
    Debug = cms.untracked.bool(False),
    DIGIOFFSET = cms.int32(500),
    SINCROTIME = cms.int32(0)
)

process.MIsoDepositViewMultiIOBlock = cms.PSet(
    ExtractForCandidate = cms.bool(False),
    inputMuonCollection = cms.InputTag("muons"),
    MultipleDepositsFlag = cms.bool(True),
    MuonTrackRefType = cms.string('bestTrkSta'),
    InputType = cms.string('MuonCollection')
)

process.EleIsoTrackExtractorBlock = cms.PSet(
    BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
    DR_Max = cms.double(0.4),
    NHits_Min = cms.uint32(0),
    checkIsoInnRBarrel = cms.double(0.0),
    checkIsoExtRBarrel = cms.double(0.01),
    checkIsoEtaStripBarrel = cms.double(0.0),
    checkIsoEtRecHitEndcap = cms.double(0.3),
    Pt_Min = cms.double(-1.0),
    DepositLabel = cms.untracked.string(''),
    barrelEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
    Diff_z = cms.double(0.2),
    inputTrackCollection = cms.InputTag("generalTracks"),
    checkIsoEtCutEndcap = cms.double(10000.0),
    endcapEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
    Diff_r = cms.double(0.1),
    Chi2Prob_Min = cms.double(-1.0),
    DR_Veto = cms.double(0.0),
    checkIsoEtCutBarrel = cms.double(10000.0),
    Chi2Ndof_Max = cms.double(1e+64),
    checkIsoEtRecHitBarrel = cms.double(0.08),
    checkIsoInnREndcap = cms.double(0.0),
    BeamlineOption = cms.string('BeamSpotFromEvent'),
    minCandEt = cms.double(0.0),
    ComponentName = cms.string('EgammaTrackExtractor'),
    checkIsoExtREndcap = cms.double(0.01),
    checkIsoEtaStripEndcap = cms.double(0.0)
)

process.BtiParametersBlock = cms.PSet(
    BtiParameters = cms.PSet(
        KACCTHETA = cms.int32(1),
        WEN8 = cms.int32(1),
        ACH = cms.int32(1),
        DEAD = cms.int32(31),
        ACL = cms.int32(2),
        PTMS20 = cms.int32(1),
        Debug = cms.untracked.int32(0),
        PTMS22 = cms.int32(1),
        PTMS23 = cms.int32(1),
        PTMS24 = cms.int32(1),
        PTMS25 = cms.int32(1),
        PTMS26 = cms.int32(1),
        PTMS27 = cms.int32(1),
        PTMS28 = cms.int32(1),
        PTMS29 = cms.int32(1),
        SET = cms.int32(7),
        RON = cms.bool(True),
        WEN2 = cms.int32(1),
        LL = cms.int32(2),
        LH = cms.int32(21),
        WEN3 = cms.int32(1),
        RE43 = cms.int32(2),
        WEN0 = cms.int32(1),
        RL = cms.int32(42),
        WEN1 = cms.int32(1),
        RH = cms.int32(61),
        LTS = cms.int32(3),
        CH = cms.int32(41),
        CL = cms.int32(22),
        PTMS15 = cms.int32(1),
        PTMS14 = cms.int32(1),
        PTMS17 = cms.int32(1),
        PTMS16 = cms.int32(1),
        PTMS11 = cms.int32(1),
        PTMS10 = cms.int32(1),
        PTMS13 = cms.int32(1),
        PTMS12 = cms.int32(1),
        XON = cms.bool(False),
        WEN7 = cms.int32(1),
        WEN4 = cms.int32(1),
        WEN5 = cms.int32(1),
        PTMS19 = cms.int32(1),
        PTMS18 = cms.int32(1),
        PTMS31 = cms.int32(0),
        PTMS30 = cms.int32(0),
        PTMS5 = cms.int32(1),
        PTMS4 = cms.int32(1),
        PTMS7 = cms.int32(1),
        PTMS6 = cms.int32(1),
        PTMS1 = cms.int32(0),
        PTMS0 = cms.int32(0),
        PTMS3 = cms.int32(0),
        WEN6 = cms.int32(1),
        PTMS2 = cms.int32(0),
        PTMS9 = cms.int32(1),
        PTMS8 = cms.int32(1),
        ST43 = cms.int32(42),
        AC2 = cms.int32(3),
        AC1 = cms.int32(0),
        KMAX = cms.int32(64),
        PTMS21 = cms.int32(1)
    )
)

process.TrackAssociatorParameters = cms.PSet(
    muonMaxDistanceSigmaX = cms.double(0.0),
    muonMaxDistanceSigmaY = cms.double(0.0),
    CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
    dRHcal = cms.double(9999.0),
    dREcal = cms.double(9999.0),
    CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
    useEcal = cms.bool(True),
    dREcalPreselection = cms.double(0.05),
    HORecHitCollectionLabel = cms.InputTag("horeco"),
    dRMuon = cms.double(9999.0),
    crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
    propagateAllDirections = cms.bool(True),
    muonMaxDistanceX = cms.double(5.0),
    muonMaxDistanceY = cms.double(5.0),
    useHO = cms.bool(True),
    accountForTrajectoryChangeCalo = cms.bool(False),
    DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
    EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
    dRHcalPreselection = cms.double(0.2),
    useMuon = cms.bool(True),
    useCalo = cms.bool(False),
    EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
    dRMuonPreselection = cms.double(0.2),
    truthMatch = cms.bool(False),
    HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
    useHcal = cms.bool(True)
)

process.MIsoCaloExtractorEcalBlock = cms.PSet(
    DR_Veto_H = cms.double(0.1),
    Vertex_Constraint_Z = cms.bool(False),
    Threshold_H = cms.double(0.5),
    ComponentName = cms.string('CaloExtractor'),
    Threshold_E = cms.double(0.2),
    DR_Max = cms.double(1.0),
    DR_Veto_E = cms.double(0.07),
    Weight_E = cms.double(1.0),
    Vertex_Constraint_XY = cms.bool(False),
    DepositLabel = cms.untracked.string('EcalPlusHcal'),
    CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
    Weight_H = cms.double(0.0)
)

process.MIsoCaloExtractorHcalBlock = cms.PSet(
    DR_Veto_H = cms.double(0.1),
    Vertex_Constraint_Z = cms.bool(False),
    Threshold_H = cms.double(0.5),
    ComponentName = cms.string('CaloExtractor'),
    Threshold_E = cms.double(0.2),
    DR_Max = cms.double(1.0),
    DR_Veto_E = cms.double(0.07),
    Weight_E = cms.double(0.0),
    Vertex_Constraint_XY = cms.bool(False),
    DepositLabel = cms.untracked.string('EcalPlusHcal'),
    CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
    Weight_H = cms.double(1.0)
)

process.patEventSelection = cms.PSet(
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('p')
    )
)

process.FastjetWithPU = cms.PSet(
    Active_Area_Repeats = cms.int32(5),
    GhostArea = cms.double(0.01),
    Ghost_EtaMax = cms.double(6.0),
    UE_Subtraction = cms.string('yes')
)

process.MIsoDepositParamGlobalMultiIOBlock = cms.PSet(
    ExtractForCandidate = cms.bool(False),
    inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
    MultipleDepositsFlag = cms.bool(True),
    MuonTrackRefType = cms.string('track'),
    InputType = cms.string('MuonCollection')
)

process.DTTPGMapBlock = cms.PSet(
    DTTPGMap = cms.untracked.PSet(
        wh0st2se11 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se10 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se12 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st1se4 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se12 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se11 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se10 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se1 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se2 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st3se4 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se4 = cms.untracked.vint32(72, 48, 72, 18),
        whm2st1se8 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se9 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se1 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st2se6 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st1se12 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se10 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se11 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st2se12 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se1 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st1se3 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se2 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st3se3 = cms.untracked.vint32(72, 48, 72, 18),
        whm1st1se7 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st2se2 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st1se6 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st4se8 = cms.untracked.vint32(92, 0, 92, 23),
        whm1st3se11 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st2se9 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se8 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st3se10 = cms.untracked.vint32(72, 58, 72, 18),
        whm1st3se5 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st2se4 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se7 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st3se6 = cms.untracked.vint32(72, 58, 72, 18),
        whm1st3se1 = cms.untracked.vint32(72, 58, 72, 18),
        whm1st1se9 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st2se3 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st3se2 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st4se14 = cms.untracked.vint32(60, 0, 60, 15),
        whm2st4se13 = cms.untracked.vint32(72, 0, 72, 18),
        whm2st4se12 = cms.untracked.vint32(92, 0, 92, 23),
        whm2st4se11 = cms.untracked.vint32(48, 0, 48, 12),
        whm2st4se10 = cms.untracked.vint32(60, 0, 60, 15),
        whm2st1se6 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se10 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se11 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se12 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se7 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st3se7 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st4se9 = cms.untracked.vint32(48, 0, 48, 12),
        whm2st4se8 = cms.untracked.vint32(92, 0, 92, 23),
        whm1st4se12 = cms.untracked.vint32(92, 0, 92, 23),
        whm1st4se13 = cms.untracked.vint32(72, 0, 72, 18),
        whm1st4se10 = cms.untracked.vint32(60, 0, 60, 15),
        whm1st4se11 = cms.untracked.vint32(48, 0, 48, 12),
        whm2st4se3 = cms.untracked.vint32(96, 0, 96, 24),
        whm2st4se2 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st4se14 = cms.untracked.vint32(60, 0, 60, 15),
        whm2st3se8 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se9 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se6 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se7 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se4 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se5 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se2 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se3 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se1 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se12 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se11 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se10 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st1se12 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se10 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se11 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st4se6 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st4se7 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st4se4 = cms.untracked.vint32(72, 0, 72, 18),
        wh1st4se5 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st4se2 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st2se12 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se11 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se10 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st3se3 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se2 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se1 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se7 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se6 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se5 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st4se9 = cms.untracked.vint32(48, 0, 48, 12),
        whm1st1se3 = cms.untracked.vint32(50, 48, 50, 13),
        whm1st1se2 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se1 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st2se8 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st2se9 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st1se5 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se4 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st2se4 = cms.untracked.vint32(60, 48, 60, 15),
        wh1st2se5 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st2se6 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st2se7 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st2se1 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st2se2 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st4se8 = cms.untracked.vint32(92, 0, 92, 23),
        wh2st3se9 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st1se8 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st4se7 = cms.untracked.vint32(96, 0, 96, 24),
        whm2st4se6 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st4se4 = cms.untracked.vint32(72, 0, 72, 18),
        whm2st4se5 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st1se8 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se7 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se4 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st4se4 = cms.untracked.vint32(72, 0, 72, 18),
        wh2st1se2 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se3 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se1 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se1 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se2 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se3 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se4 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se5 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se8 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se9 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st4se1 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se3 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se2 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se5 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se4 = cms.untracked.vint32(72, 0, 72, 18),
        wh2st4se7 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se6 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st4se3 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se8 = cms.untracked.vint32(92, 0, 92, 23),
        wh0st4se1 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st4se7 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st4se6 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st4se5 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st4se4 = cms.untracked.vint32(72, 0, 72, 18),
        wh0st3se10 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se11 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se12 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st4se11 = cms.untracked.vint32(48, 0, 48, 12),
        wh2st4se10 = cms.untracked.vint32(60, 0, 60, 15),
        wh2st4se13 = cms.untracked.vint32(72, 0, 72, 18),
        wh2st4se12 = cms.untracked.vint32(92, 0, 92, 23),
        wh2st4se14 = cms.untracked.vint32(60, 0, 60, 15),
        wh1st1se5 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st4se1 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st4se2 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st4se3 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st2se12 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st4se5 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st2se10 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st4se7 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st4se8 = cms.untracked.vint32(92, 0, 92, 23),
        whm1st4se9 = cms.untracked.vint32(48, 0, 48, 12),
        whm1st2se11 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st3se6 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se7 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se4 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se5 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se2 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se3 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se1 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se7 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st1se5 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st3se8 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se9 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st1se6 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se8 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se9 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st3se12 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se10 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se11 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st1se11 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se10 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se12 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st2se11 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se5 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se4 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se7 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se6 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se1 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se3 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se2 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se9 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se8 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st4se6 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st1se5 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st2se6 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se7 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se4 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se5 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se2 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se3 = cms.untracked.vint32(60, 48, 60, 15),
        whm1st2se1 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se8 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se9 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se7 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se6 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se5 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se4 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se3 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se2 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se1 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st1se7 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st2se9 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se8 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st4se13 = cms.untracked.vint32(72, 0, 72, 18),
        wh0st1se6 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st4se11 = cms.untracked.vint32(48, 0, 48, 12),
        wh0st4se10 = cms.untracked.vint32(60, 0, 60, 15),
        whm1st3se12 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st4se14 = cms.untracked.vint32(60, 0, 60, 15),
        whm2st1se3 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st4se9 = cms.untracked.vint32(48, 0, 48, 12),
        wh1st4se10 = cms.untracked.vint32(60, 0, 60, 15),
        wh1st4se11 = cms.untracked.vint32(48, 0, 48, 12),
        wh1st4se12 = cms.untracked.vint32(92, 0, 92, 23),
        wh1st4se13 = cms.untracked.vint32(72, 0, 72, 18),
        wh1st4se14 = cms.untracked.vint32(60, 0, 60, 15),
        wh1st1se4 = cms.untracked.vint32(50, 48, 50, 13),
        wh1st1se7 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se6 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se9 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st3se10 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st2se3 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st3se11 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se12 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st4se12 = cms.untracked.vint32(92, 0, 92, 23),
        wh1st3se9 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se8 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st4se9 = cms.untracked.vint32(48, 0, 48, 12),
        wh1st3se8 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st4se2 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st3se1 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se2 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se3 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se4 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se5 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se6 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st4se3 = cms.untracked.vint32(96, 0, 96, 24),
        whm2st4se1 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st4se1 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st2se10 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se11 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se10 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se12 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se5 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st3se9 = cms.untracked.vint32(72, 58, 72, 18),
        whm1st3se8 = cms.untracked.vint32(72, 58, 72, 18)
    )
)

process.SectCollParametersBlock = cms.PSet(
    SectCollParameters = cms.PSet(
        SCCSP5 = cms.int32(0),
        SCCSP2 = cms.int32(0),
        SCCSP3 = cms.int32(0),
        SCECF4 = cms.bool(False),
        SCCSP1 = cms.int32(0),
        SCECF2 = cms.bool(False),
        SCECF3 = cms.bool(False),
        SCCSP4 = cms.int32(0),
        SCECF1 = cms.bool(False),
        Debug = cms.untracked.bool(False)
    )
)

process.MIsoDepositGlobalIOBlock = cms.PSet(
    ExtractForCandidate = cms.bool(False),
    inputMuonCollection = cms.InputTag("globalMuons"),
    MultipleDepositsFlag = cms.bool(False),
    MuonTrackRefType = cms.string('track'),
    InputType = cms.string('TrackCollection')
)

process.GenJetParameters = cms.PSet(
    src = cms.InputTag("genParticlesForJets"),
    verbose = cms.untracked.bool(False),
    jetPtMin = cms.double(5.0),
    inputEtMin = cms.double(0.0),
    jetType = cms.untracked.string('GenJet'),
    inputEMin = cms.double(0.0)
)

process.MIsoCaloExtractorByAssociatorTowersBlock = cms.PSet(
    TrackAssociatorParameterBlock = cms.PSet(
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(9999.0),
            dREcal = cms.double(9999.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(True),
            dREcalPreselection = cms.double(0.05),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(True),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.2),
            useMuon = cms.bool(True),
            useCalo = cms.bool(False),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(True)
        )
    ),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(1.0),
        dREcal = cms.double(1.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(False),
        dREcalPreselection = cms.double(1.0),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(False),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(1.0),
        useMuon = cms.bool(False),
        useCalo = cms.bool(True),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(False)
    ),
    PropagatorName = cms.string('SteppingHelixPropagatorAny'),
    NoiseTow_EB = cms.double(0.04),
    Noise_EE = cms.double(0.1),
    PrintTimeReport = cms.untracked.bool(False),
    DR_Veto_E = cms.double(0.07),
    NoiseTow_EE = cms.double(0.15),
    Threshold_HO = cms.double(0.5),
    ComponentName = cms.string('CaloExtractorByAssociator'),
    Noise_HO = cms.double(0.2),
    DR_Max = cms.double(1.0),
    Noise_EB = cms.double(0.025),
    Threshold_E = cms.double(0.2),
    Noise_HB = cms.double(0.2),
    UseRecHitsFlag = cms.bool(False),
    Threshold_H = cms.double(0.5),
    DR_Veto_H = cms.double(0.1),
    DepositLabel = cms.untracked.string('Cal'),
    Noise_HE = cms.double(0.2),
    DR_Veto_HO = cms.double(0.1),
    DepositInstanceLabels = cms.vstring('ecal', 
        'hcal', 
        'ho')
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

process.vertexRecoBlock = cms.PSet(
    vertexReco = cms.PSet(
        seccut = cms.double(6.0),
        primcut = cms.double(1.8),
        smoothing = cms.bool(False),
        weightthreshold = cms.double(0.001),
        minweight = cms.double(0.5),
        finder = cms.string('avr')
    )
)

process.vertexSelectionBlock = cms.PSet(
    vertexSelection = cms.PSet(
        sortCriterium = cms.string('dist3dError')
    )
)

process.GamIsoEcalFromHitsExtractorBlock = cms.PSet(
    tryBoth = cms.bool(True),
    intStrip = cms.double(0.0),
    subtractSuperClusterEnergy = cms.bool(False),
    checkIsoInnRBarrel = cms.double(0.045),
    checkIsoExtRBarrel = cms.double(0.4),
    etMin = cms.double(-999.0),
    checkIsoEtaStripBarrel = cms.double(0.02),
    checkIsoEtRecHitEndcap = cms.double(0.3),
    DepositLabel = cms.untracked.string(''),
    detector = cms.string('Ecal'),
    barrelEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
    isolationVariable = cms.string('et'),
    checkIsoEtCutEndcap = cms.double(7.0),
    endcapEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
    intRadius = cms.double(0.0),
    energyMin = cms.double(0.08),
    extRadius = cms.double(0.5),
    checkIsoEtCutBarrel = cms.double(8.0),
    checkIsoEtRecHitBarrel = cms.double(0.08),
    checkIsoInnREndcap = cms.double(0.07),
    minCandEt = cms.double(15.0),
    barrelRecHits = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
    ComponentName = cms.string('EgammaRecHitExtractor'),
    endcapRecHits = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
    checkIsoExtREndcap = cms.double(0.4),
    checkIsoEtaStripEndcap = cms.double(0.02)
)

process.TrackAssociatorParameterBlock = cms.PSet(
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    )
)

process.vertexCutsBlock = cms.PSet(
    vertexCuts = cms.PSet(
        distSig3dMax = cms.double(99999.9),
        fracPV = cms.double(0.65),
        distVal2dMax = cms.double(2.5),
        useTrackWeights = cms.bool(True),
        maxDeltaRToJetAxis = cms.double(0.5),
        v0Filter = cms.PSet(
            k0sMassWindow = cms.double(0.05)
        ),
        distSig2dMin = cms.double(3.0),
        multiplicityMin = cms.uint32(2),
        massMax = cms.double(6.5),
        distSig2dMax = cms.double(99999.9),
        distVal3dMax = cms.double(99999.9),
        minimumTrackWeight = cms.double(0.5),
        distVal3dMin = cms.double(-99999.9),
        distVal2dMin = cms.double(0.01),
        distSig3dMin = cms.double(-99999.9)
    )
)


