

for ibin in range(0,len(ptBins)-1) :
    response = ROOT.RooUnfoldResponse(60, 0., 300., 60, 0., 300.)
    response.SetName('response_pt' + str(ibin))
    response_Groom = []
    for igroom in range(0,len(ak7GroomObj)):
        res = ROOT.RooUnfoldResponse(60, 0., 300., 60, 0., 300.)
        res.SetName('response_pt' + str(ibin) + '_Groom' + str(igroom) )
        response_Groom.append( res )
    responses.append(response)
    responses_Groom.append( response_Groom )



for ievent in events :

    response = responses[indexForTheseKinematics]
    response_Groom = responses_Groom[indexForTheseKinematics]

    leadingJet = jets[0]
    observedDist.Fill( leadingJet.M() )
    matchedGrooms = []
    igroom = 0
    for groom in grooms :
        groomedJet = findMatchedTo(leadingJet, groom )
        observedDistGroom[igroom].Fill( groomedJet.M() )
        matchedGrooms.append(groomedJet)
        igroom += 1
        
    if isMC :
        matchedGen = findMatchedTo( leadingJet, genJets )
        response.Fill( leadingJet.M(), matchedGen.M() )
        igroom = 0
        for matchedGroom in matchedGrooms :
            response_Groom[igroom].Fill( matchedGroom.M(), matchedGen.M() )
            igroom += 1
        leadingGen = genJets[0]
        trueDist.Fill( leadingGen.M() )




cms.Sequence(goodOfflinePrimaryVertices+
pfPileUpPFlow+
pfNoPileUpPFlow+
pfPileUpIsoPFlow+
pfNoPileUpIsoPFlow+
pfAllNeutralHadronsPFlow+
pfAllChargedHadronsPFlow+
pfAllPhotonsPFlow+
pfAllChargedParticlesPFlow+
pfPileUpAllChargedParticlesPFlow+
pfAllNeutralHadronsAndPhotonsPFlow+
pfSelectedPhotonsPFlow+
phPFIsoDepositChargedPFlow+
phPFIsoDepositChargedAllPFlow+
phPFIsoDepositGammaPFlow+
phPFIsoDepositNeutralPFlow+
phPFIsoDepositPUPFlow+
phPFIsoValueCharged03PFlow+
phPFIsoValueChargedAll03PFlow+
phPFIsoValueGamma03PFlow+
phPFIsoValueNeutral03PFlow+
phPFIsoValuePU03PFlow+
phPFIsoValueCharged04PFlow+
phPFIsoValueChargedAll04PFlow+
phPFIsoValueGamma04PFlow+
phPFIsoValueNeutral04PFlow+
phPFIsoValuePU04PFlow+
pfIsolatedPhotonsPFlow+
pfAllMuonsPFlow+
pfMuonsFromVertexPFlow+
pfSelectedMuonsPFlow+
muPFIsoDepositChargedPFlow+
muPFIsoDepositChargedAllPFlow+
muPFIsoDepositGammaPFlow+
muPFIsoDepositNeutralPFlow+
muPFIsoDepositPUPFlow+
muPFIsoValueCharged03PFlow+
muPFIsoValueChargedAll03PFlow+
muPFIsoValueGamma03PFlow+
muPFIsoValueNeutral03PFlow+
muPFIsoValueGammaHighThreshold03PFlow+
muPFIsoValueNeutralHighThreshold03PFlow+
muPFIsoValuePU03PFlow+
muPFIsoValueCharged04PFlow+
muPFIsoValueChargedAll04PFlow+
muPFIsoValueGamma04PFlow+
muPFIsoValueNeutral04PFlow+
muPFIsoValueGammaHighThreshold04PFlow+
muPFIsoValueNeutralHighThreshold04PFlow+
muPFIsoValuePU04PFlow+
pfIsolatedMuonsPFlow+
pfMuonsPFlow+
pfNoMuonPFlow+
pfAllElectronsPFlow+
pfElectronsFromVertexPFlow+
pfSelectedElectronsPFlow+
elPFIsoDepositChargedPFlow+
elPFIsoDepositChargedAllPFlow+
elPFIsoDepositGammaPFlow+
elPFIsoDepositNeutralPFlow+
elPFIsoDepositPUPFlow+
elPFIsoValueCharged03PFlow+
elPFIsoValueChargedAll03PFlow+
elPFIsoValueGamma03PFlow+
elPFIsoValueNeutral03PFlow+
elPFIsoValuePU03PFlow+
elPFIsoValueCharged04PFlow+
elPFIsoValueChargedAll04PFlow+
elPFIsoValueGamma04PFlow+
elPFIsoValueNeutral04PFlow+
elPFIsoValuePU04PFlow+
pfIsolatedElectronsPFlow+
pfElectronsPFlow+
pfNoElectronPFlow+
kt6PFJets+
pfJetsPFlow+
pfNoJetPFlow+
pfJetTracksAssociatorAtVertexPFlow+
pfTauPFJets08RegionPFlow+
pfTauPileUpVerticesPFlow+
pfTauTagInfoProducerPFlow+
pfJetsPiZerosPFlow+
pfJetsLegacyTaNCPiZerosPFlow+
pfJetsLegacyHPSPiZerosPFlow+
pfTausBasePFlow+
hpsSelectionDiscriminatorPFlow+
hpsPFTauProducerSansRefsPFlow+
hpsPFTauProducerPFlow+
pfTausBaseDiscriminationByDecayModeFindingPFlow+
pfTausBaseDiscriminationByLooseCombinedIsolationDBSumPtCorrPFlow+
pfTausPFlow+
pfNoTauPFlow+
pfMETPFlow+
patElectronsPFlow+
patMuonsPFlow+
pfPileUpIsoPFlow+
pfNoPileUpIsoPFlow+
pfAllNeutralHadronsPFlow+
pfAllChargedHadronsPFlow+
pfAllPhotonsPFlow+
pfAllChargedParticlesPFlow+
pfPileUpAllChargedParticlesPFlow+
pfAllNeutralHadronsAndPhotonsPFlow+
tauIsoDepositPFCandidatesPFlow+
tauIsoDepositPFChargedHadronsPFlow+
tauIsoDepositPFNeutralHadronsPFlow+
tauIsoDepositPFGammasPFlow+
hpsPFTauDiscriminationByDecayModeFindingPFlow+
hpsPFTauDiscriminationByVLooseChargedIsolationPFlow+
hpsPFTauDiscriminationByLooseChargedIsolationPFlow+
hpsPFTauDiscriminationByMediumChargedIsolationPFlow+
hpsPFTauDiscriminationByTightChargedIsolationPFlow+
hpsPFTauDiscriminationByVLooseIsolationPFlow+
hpsPFTauDiscriminationByLooseIsolationPFlow+
hpsPFTauDiscriminationByMediumIsolationPFlow+
hpsPFTauDiscriminationByTightIsolationPFlow+
hpsPFTauDiscriminationByVLooseIsolationDBSumPtCorrPFlow+
hpsPFTauDiscriminationByLooseIsolationDBSumPtCorrPFlow+
hpsPFTauDiscriminationByMediumIsolationDBSumPtCorrPFlow+
hpsPFTauDiscriminationByTightIsolationDBSumPtCorrPFlow+
hpsPFTauDiscriminationByRawCombinedIsolationDBSumPtCorrPFlow+
hpsPFTauDiscriminationByRawChargedIsolationDBSumPtCorrPFlow+
hpsPFTauDiscriminationByRawGammaIsolationDBSumPtCorrPFlow+
hpsPFTauDiscriminationByVLooseCombinedIsolationDBSumPtCorrPFlow+
hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorrPFlow+
hpsPFTauDiscriminationByMediumCombinedIsolationDBSumPtCorrPFlow+
hpsPFTauDiscriminationByTightCombinedIsolationDBSumPtCorrPFlow+
hpsPFTauDiscriminationByLooseElectronRejectionPFlow+
hpsPFTauDiscriminationByMediumElectronRejectionPFlow+
hpsPFTauDiscriminationByTightElectronRejectionPFlow+
hpsPFTauDiscriminationByMVAElectronRejectionPFlow+
hpsPFTauDiscriminationByLooseMuonRejectionPFlow+
hpsPFTauDiscriminationByMediumMuonRejectionPFlow+
hpsPFTauDiscriminationByTightMuonRejectionPFlow+
patTausPFlow+
kt6PFJetsPFlow+
patJetCorrFactorsPFlow+
kt6PFJetsAK5PFCHSPFlow+
patJetCorrFactorsAK5PFCHSPFlow+
kt6PFJetsAK5PFcorrPFlow+
patJetCorrFactorsAK5PFcorrPFlow+
jetTracksAssociatorAtVertexPFlow+
impactParameterTagInfosAODPFlow+
secondaryVertexTagInfosAODPFlow+
softMuonTagInfosAODPFlow+
jetBProbabilityBJetTagsAODPFlow+
jetProbabilityBJetTagsAODPFlow+
trackCountingHighPurBJetTagsAODPFlow+
trackCountingHighEffBJetTagsAODPFlow+
simpleSecondaryVertexHighEffBJetTagsAODPFlow+
simpleSecondaryVertexHighPurBJetTagsAODPFlow+
combinedSecondaryVertexBJetTagsAODPFlow+
combinedSecondaryVertexMVABJetTagsAODPFlow+
softMuonBJetTagsAODPFlow+
softMuonByPtBJetTagsAODPFlow+
softMuonByIP3dBJetTagsAODPFlow+
patJetChargePFlow+
patJetsPFlow+
patJetsAK5PFCHSPFlow+
patJetsAK5UnPFCHSPFlow+
patJetsAK5PFcorrPFlow+
patJetsAK5UnPFcorrPFlow+
patMETsPFlow+
patMETsPFPFlow+
patPFParticlesPFlow+
patCandidateSummaryPFlow+
selectedPatElectronsPFlow+
selectedPatMuonsPFlow+
selectedPatTausPFlow+
selectedPatJetsPFlow+
selectedPatJetsAK5PFCHSPFlow+
selectedPatJetsAK5UnPFCHSPFlow+
selectedPatJetsAK5PFcorrPFlow+
selectedPatJetsAK5UnPFcorrPFlow+
selectedPatPFParticlesPFlow+
selectedPatCandidateSummaryPFlow+
countPatElectronsPFlow+
countPatMuonsPFlow+
countPatTausPFlow+
countPatLeptonsPFlow+
countPatJetsPFlow+
countPatPFParticlesPFlow)




cms.Path(pfPileUpPFlow+
pfNoPileUpPFlow+
pfPileUpIsoPFlow+
pfNoPileUpIsoPFlow+
pfAllNeutralHadronsPFlow+
pfAllChargedHadronsPFlow+
pfAllPhotonsPFlow+
pfAllChargedParticlesPFlow+
pfPileUpAllChargedParticlesPFlow+
pfAllNeutralHadronsAndPhotonsPFlow+
pfSelectedPhotonsPFlow+
phPFIsoDepositChargedPFlow+
phPFIsoDepositChargedAllPFlow+
phPFIsoDepositGammaPFlow+
phPFIsoDepositNeutralPFlow+
phPFIsoDepositPUPFlow+
phPFIsoValueCharged03PFlow+
phPFIsoValueChargedAll03PFlow+
phPFIsoValueGamma03PFlow+
phPFIsoValueNeutral03PFlow+
phPFIsoValuePU03PFlow+
phPFIsoValueCharged04PFlow+
phPFIsoValueChargedAll04PFlow+
phPFIsoValueGamma04PFlow+
phPFIsoValueNeutral04PFlow+
phPFIsoValuePU04PFlow+
pfIsolatedPhotonsPFlow+
pfAllMuonsPFlow+
pfMuonsFromVertexPFlow+
pfSelectedMuonsPFlow+
muPFIsoDepositChargedPFlow+
muPFIsoDepositChargedAllPFlow+
muPFIsoDepositGammaPFlow+
muPFIsoDepositNeutralPFlow+
muPFIsoDepositPUPFlow+
muPFIsoValueCharged03PFlow+
muPFIsoValueChargedAll03PFlow+
muPFIsoValueGamma03PFlow+
muPFIsoValueNeutral03PFlow+
muPFIsoValueGammaHighThreshold03PFlow+
muPFIsoValueNeutralHighThreshold03PFlow+
muPFIsoValuePU03PFlow+
muPFIsoValueCharged04PFlow+
muPFIsoValueChargedAll04PFlow+
muPFIsoValueGamma04PFlow+
muPFIsoValueNeutral04PFlow+
muPFIsoValueGammaHighThreshold04PFlow+
muPFIsoValueNeutralHighThreshold04PFlow+
muPFIsoValuePU04PFlow+
pfIsolatedMuonsPFlow+
pfMuonsPFlow+
pfNoMuonPFlow+
pfAllElectronsPFlow+
pfElectronsFromVertexPFlow+
pfSelectedElectronsPFlow+
elPFIsoDepositChargedPFlow+
elPFIsoDepositChargedAllPFlow+
elPFIsoDepositGammaPFlow+
elPFIsoDepositNeutralPFlow+
elPFIsoDepositPUPFlow+
elPFIsoValueCharged03PFlow+
elPFIsoValueChargedAll03PFlow+
elPFIsoValueGamma03PFlow+
elPFIsoValueNeutral03PFlow+
elPFIsoValuePU03PFlow+
elPFIsoValueCharged04PFlow+
elPFIsoValueChargedAll04PFlow+
elPFIsoValueGamma04PFlow+
elPFIsoValueNeutral04PFlow+
elPFIsoValuePU04PFlow+
pfIsolatedElectronsPFlow+
pfElectronsPFlow+
pfNoElectronPFlow+
pfJetsPFlow+
pfNoJetPFlow+
pfJetTracksAssociatorAtVertexPFlow+
pfTauPFJets08RegionPFlow+
pfTauPileUpVerticesPFlow+
pfTauTagInfoProducerPFlow+
pfJetsPiZerosPFlow+
pfJetsLegacyTaNCPiZerosPFlow+
pfJetsLegacyHPSPiZerosPFlow+
pfTausBasePFlow+
hpsSelectionDiscriminatorPFlow+
hpsPFTauProducerSansRefsPFlow+
hpsPFTauProducerPFlow+
pfTausBaseDiscriminationByDecayModeFindingPFlow+
pfTausBaseDiscriminationByLooseCombinedIsolationDBSumPtCorrPFlow+
pfTausPFlow+
pfNoTauPFlow+
pfMETPFlow+
electronMatchPFlow+
patElectronsPFlow+
muonMatchPFlow+
patMuonsPFlow+
pfPileUpIsoPFlow+
pfNoPileUpIsoPFlow+
pfAllNeutralHadronsPFlow+
pfAllChargedHadronsPFlow+
pfAllPhotonsPFlow+
pfAllChargedParticlesPFlow+
pfPileUpAllChargedParticlesPFlow+
pfAllNeutralHadronsAndPhotonsPFlow+
tauIsoDepositPFCandidatesPFlow+
tauIsoDepositPFChargedHadronsPFlow+
tauIsoDepositPFNeutralHadronsPFlow+
tauIsoDepositPFGammasPFlow+
tauMatchPFlow+
tauGenJetsPFlow+
tauGenJetsSelectorAllHadronsPFlow+
tauGenJetMatchPFlow+
hpsPFTauDiscriminationByDecayModeFindingPFlow+
hpsPFTauDiscriminationByVLooseChargedIsolationPFlow+
hpsPFTauDiscriminationByLooseChargedIsolationPFlow+
hpsPFTauDiscriminationByMediumChargedIsolationPFlow+
hpsPFTauDiscriminationByTightChargedIsolationPFlow+
hpsPFTauDiscriminationByVLooseIsolationPFlow+
hpsPFTauDiscriminationByLooseIsolationPFlow+
hpsPFTauDiscriminationByMediumIsolationPFlow+
hpsPFTauDiscriminationByTightIsolationPFlow+
hpsPFTauDiscriminationByVLooseIsolationDBSumPtCorrPFlow+
hpsPFTauDiscriminationByLooseIsolationDBSumPtCorrPFlow+
hpsPFTauDiscriminationByMediumIsolationDBSumPtCorrPFlow+
hpsPFTauDiscriminationByTightIsolationDBSumPtCorrPFlow+
hpsPFTauDiscriminationByRawCombinedIsolationDBSumPtCorrPFlow+
hpsPFTauDiscriminationByRawChargedIsolationDBSumPtCorrPFlow+
hpsPFTauDiscriminationByRawGammaIsolationDBSumPtCorrPFlow+
hpsPFTauDiscriminationByVLooseCombinedIsolationDBSumPtCorrPFlow+
hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorrPFlow+
hpsPFTauDiscriminationByMediumCombinedIsolationDBSumPtCorrPFlow+
hpsPFTauDiscriminationByTightCombinedIsolationDBSumPtCorrPFlow+
hpsPFTauDiscriminationByLooseElectronRejectionPFlow+
hpsPFTauDiscriminationByMediumElectronRejectionPFlow+
hpsPFTauDiscriminationByTightElectronRejectionPFlow+
hpsPFTauDiscriminationByMVAElectronRejectionPFlow+
hpsPFTauDiscriminationByLooseMuonRejectionPFlow+
hpsPFTauDiscriminationByMediumMuonRejectionPFlow+
hpsPFTauDiscriminationByTightMuonRejectionPFlow+
patTausPFlow+
photonMatchPFlow+
kt6PFJetsPFlow+
patJetCorrFactorsPFlow+
jetTracksAssociatorAtVertexPFlow+
impactParameterTagInfosAODPFlow+
secondaryVertexTagInfosAODPFlow+
softMuonTagInfosAODPFlow+
jetBProbabilityBJetTagsAODPFlow+
jetProbabilityBJetTagsAODPFlow+
trackCountingHighPurBJetTagsAODPFlow+
trackCountingHighEffBJetTagsAODPFlow+
simpleSecondaryVertexHighEffBJetTagsAODPFlow+
simpleSecondaryVertexHighPurBJetTagsAODPFlow+
combinedSecondaryVertexBJetTagsAODPFlow+
combinedSecondaryVertexMVABJetTagsAODPFlow+
softMuonBJetTagsAODPFlow+
softMuonByPtBJetTagsAODPFlow+
softMuonByIP3dBJetTagsAODPFlow+
patJetChargePFlow+
patJetPartonMatchPFlow+
genParticlesForJetsNoNu+
iterativeCone5GenJetsNoNu+
ak5GenJetsNoNu+
ak7GenJetsNoNu+
patJetGenJetMatchPFlow+
patJetPartonsPFlow+
patJetPartonAssociationPFlow+
patJetFlavourAssociationPFlow+
patJetsPFlow+
patMETsPFlow+
patPFParticlesPFlow+
patCandidateSummaryPFlow+
selectedPatElectronsPFlow+
selectedPatMuonsPFlow+
selectedPatTausPFlow+
selectedPatJetsPFlow+
selectedPatPFParticlesPFlow+
selectedPatCandidateSummaryPFlow+
countPatElectronsPFlow+
countPatMuonsPFlow+
countPatTausPFlow+
countPatLeptonsPFlow+
countPatJetsPFlow+
countPatPFParticlesPFlow+
electronMatch+
patElectrons+
muonMatch+
patMuons+
pfPileUpIso+
pfNoPileUpIso+
pfAllNeutralHadrons+
pfAllChargedHadrons+
pfAllPhotons+
pfAllChargedParticles+
pfPileUpAllChargedParticles+
pfAllNeutralHadronsAndPhotons+
tauIsoDepositPFCandidates+
tauIsoDepositPFChargedHadrons+
tauIsoDepositPFNeutralHadrons+
tauIsoDepositPFGammas+
tauMatch+
tauGenJets+
tauGenJetsSelectorAllHadrons+
tauGenJetMatch+
patTaus+
photonMatch+
patPhotons+
patJetCorrFactors+
patJetCharge+
patJetPartonMatch+
patJetGenJetMatch+
patJetPartons+
patJetPartonAssociation+
patJetFlavourAssociation+
patJets+
caloJetMETcorr+
muonCaloMETcorr+
caloType1CorrectedMet+
caloType1p2CorrectedMet+
kt6PFJets+
ak5PFJets+
pfCandsNotInJet+
pfJetMETcorr+
pfCandMETcorr+
pfchsMETcorr+
pfType1CorrectedMet+
pfType1p2CorrectedMet+
patMETs+
patCandidateSummary+
selectedPatElectrons+
selectedPatMuons+
selectedPatTaus+
selectedPatPhotons+
selectedPatJets+
selectedPatCandidateSummary+
cleanPatMuons+
cleanPatElectrons+
cleanPatPhotons+
cleanPatTaus+
cleanPatJets+
cleanPatCandidateSummary+
countPatElectrons+
countPatMuons+
countPatTaus+
countPatLeptons+
countPatPhotons+
countPatJets)
