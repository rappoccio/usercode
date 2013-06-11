from ROOT import fabs,TLorentzVector
import math

def massbV(Vjets, vjet_vector, jets, bjet_vector, nBtags, nBtags_remove):
    #reconstruct b' mass if a bjet and a Vjet lies in opposite hemisphere,
    #if not then form the mass between any fartherest jet and V-jet.
    pair= []
    vj = 0
    
    for vjet in Vjets:
        # require at least one b-tag jet
        if len(set(nBtags) - set(nBtags_remove)) == 0: continue        
        vjet_vector.SetPtEtaPhiM( vjet.pt(), vjet.eta(), vjet.phi(), vjet.mass() )
        
        far_bjet_p4 = None
        far_jet_p4  = None 
        dR_max_bV  = 0.0
        dR_max_jV  = 0.0
        
        for jetid, jet in enumerate(jets) :
            if jet.pt() <= 30: continue
            bjet_vector.SetPtEtaPhiM( jet.pt(), jet.eta(), jet.phi(), jet.mass() )
            dR = bjet_vector.DeltaR(vjet_vector)
    
            # max dR b/w jets and V-jets
            if dR > dR_max_jV:
                dR_max_jV = dR
                far_jet_p4 = bjet_vector

            # max dR b/w bjets and V-jets  
            if jetid in nBtags and jetid not in nBtags_remove:
                if dR > dR_max_bV:
                    dR_max_bV = dR
                    far_bjet_p4 = bjet_vector

        bV_Mass = 0.
        if far_bjet_p4:
            if dR_max_bV > 1.5: 
                bV_Mass = (far_bjet_p4+vjet_vector).M()
            elif far_jet_p4 != far_bjet_p4 and dR_max_jV > 1.5: 
                bV_Mass = (far_jet_p4+vjet_vector).M()
        
        pair.append((vj, bV_Mass))
        vj = vj + 1

    return pair

def VTag_SF(nVtags,variation):
    
    VTag_SF_nominal = 1.0
    VTag_SF_up = 1.0
    VTag_SF_dn = 1.0
    
    if nVtags == 1:
        VTag_SF_nominal = 0.951
        VTag_SF_up = 1.03 * VTag_SF_nominal
        VTag_SF_dn = 0.97 * VTag_SF_nominal      
    elif nVtags == 2:
        VTag_SF_nominal = 0.951
        VTag_SF_up = 1.06 * VTag_SF_nominal
        VTag_SF_dn = 0.94 * VTag_SF_nominal
    elif nVtags >= 3:
        VTag_SF_nominal = 0.951
        VTag_SF_up = 1.09 * VTag_SF_nominal
        VTag_SF_dn = 0.91 * VTag_SF_nominal

    if variation == 0: return VTag_SF_nominal
    elif variation == 1: return VTag_SF_up
    elif variation == -1: return VTag_SF_dn
    
def passPreTrigMVA(lep):
    myTrigPresel = False

    if fabs(lep.superCluster().eta()) < 1.479: 
        if (lep.sigmaIetaIeta() < 0.014 and \
            lep.hadronicOverEm() < 0.15 and \
            lep.dr03TkSumPt()/lep.ecalDrivenMomentum().pt() < 0.2 and \
            lep.dr03EcalRecHitSumEt()/lep.ecalDrivenMomentum().pt() < 0.2 and \
            lep.dr03HcalTowerSumEt()/lep.ecalDrivenMomentum().pt() < 0.2 and \
            lep.gsfTrack().trackerExpectedHitsInner().numberOfLostHits() == 0):
            myTrigPresel = True
    else :
        if (lep.sigmaIetaIeta() < 0.035 and \
            lep.hadronicOverEm() < 0.10 and \
            lep.dr03TkSumPt()/lep.ecalDrivenMomentum().pt() < 0.2 and \
            lep.dr03EcalRecHitSumEt()/lep.ecalDrivenMomentum().pt() < 0.2 and \
            lep.dr03HcalTowerSumEt()/lep.ecalDrivenMomentum().pt() < 0.2 and \
            lep.gsfTrack().trackerExpectedHitsInner().numberOfLostHits() == 0):
            myTrigPresel = True
  
    return myTrigPresel

    
def isVTagged(ca8jet):
    pt = ca8jet.pt()    
    mass = ca8jet.mass()
    subjet1M = ca8jet.daughter(0).mass() 
    subjet2M = ca8jet.daughter(1).mass()
    mu = max(subjet1M,subjet2M) / ca8jet.correctedJet("Uncorrected").mass()    
    if mu < 0.4 and (mass < 150 and mass > 50) and pt > 200:
    #if (mass < 150 and mass > 50) and pt > 200:    
        return True
    else:
        return False
    

def isBTagged(ak5jet, isdata, isbTag, jetFlavor):
    bjet=0
    if isdata:
         if ak5jet.bDiscriminator('combinedSecondaryVertexBJetTags') >=0.679 :
             bjet=1
    else:
        if isbTag == "OutOfBox" :
            if (ak5jet.userInt('btagRegular') & 1) == 1 :
                bjet=1
        elif isbTag == "" :
            if (ak5jet.userInt('btagRegular') & 2) == 2 :
                bjet=1
        elif isbTag =="BTagSFupHF" :
            if (jetFlavor == 5 or jetFlavor == 4) :
                if (ak5jet.userInt('btagRegular') & 4) == 4 :
                    bjet=1
            else:
                if (ak5jet.userInt('btagRegular') & 2) == 2 :
                    bjet=1
        elif isbTag =="BTagSFupLF" :
            if (jetFlavor == 5 or jetFlavor == 4) :
                if (ak5jet.userInt('btagRegular') & 2) == 2 :
                    bjet=1
            else:
                if (ak5jet.userInt('btagRegular') & 4) == 4 :
                    bjet=1
        elif isbTag =="BTagSFdownHF" :
            if (jetFlavor == 5 or jetFlavor == 4) :
                if (ak5jet.userInt('btagRegular') & 8) == 8 :
                    bjet=1
            else:
                if (ak5jet.userInt('btagRegular') & 2) == 2 :
                    bjet=1
        elif isbTag =="BTagSFdownLF" :
            if (jetFlavor == 5 or jetFlavor == 4) :
                if (ak5jet.userInt('btagRegular') & 2) == 2 :
                    bjet=1
            else:
                if (ak5jet.userInt('btagRegular') & 8) == 8 :
                    bjet=1
    if bjet==1:
        return True
    else:
        return False

'''
def isBTagged(ak5jet, isdata, isbTag):
    bjet=0
    if isdata:
        if ak5jet.bDiscriminator('combinedSecondaryVertexBJetTags') >= 0.679 :
             bjet=1
    else:
        if isbTag == "OutOfBox" :
            if (ak5jet.userInt('btagRegular') & 1) == 1 :
                bjet=1
        elif isbTag == "" :
            if (ak5jet.userInt('btagRegular') & 2) == 2 :
                bjet=1
        elif isbTag =="BTagSFup" :
            if (ak5jet.userInt('btagRegular') & 4) == 4 :
                bjet=1
        elif isbTag =="BTagSFdown" :
            if (ak5jet.userInt('btagRegular') & 8) == 8 :
                bjet=1
    if bjet==1:
        return True
    else:
        return False
'''
def isTightMu(lep, PVz):
    isPF      =  lep.isPFMuon()
    isGlob    =  lep.isGlobalMuon()
    if isPF and isGlob:    
        normChi2  =  lep.globalTrack().normalizedChi2()
        trkLayers =  lep.track().hitPattern().trackerLayersWithMeasurement()
        mVMuHits  =  lep.globalTrack().hitPattern().numberOfValidMuonHits()
        dB        =  fabs( lep.dB() )
        diffVz    =  fabs( lep.vertex().z() - PVz )
        mPixHits  =  lep.innerTrack().hitPattern().numberOfValidPixelHits()
        matchStat =  lep.numberOfMatchedStations()
    
    if(isPF and isGlob and normChi2<10 and trkLayers>5 and mVMuHits>0 and dB<0.2 and diffVz<0.5 and mPixHits>0 and matchStat >1):
        return True
    else:
        return False
    
def deltaR( eta1, phi1, eta2, phi2):
    deta = eta1 - eta2
    dphi = phi1 - phi2
    if dphi >= math.pi: dphi -= 2*math.pi
    elif dphi < -math.pi: dphi += 2*math.pi
    return math.sqrt(deta*deta + dphi*dphi)

def smear_factor(eta, variation):
    abseta = abs(eta)
    smear_nominal = 0.0
    smear_up = 0.0
    smear_down = 0.0

    if abseta <= 0.5:
                smear_nominal = 0.052
                smear_up = 0.115
                smear_down = 0.0
    elif abseta <= 1.1:
                smear_nominal = 0.057
                smear_up = 0.114
                smear_down = 0.001
    elif abseta <= 1.7:
                smear_nominal = 0.096
                smear_up = 0.161
                smear_down = 0.032
    elif abseta <= 2.3:
                smear_nominal = 0.134
                smear_up = 0.228
                smear_down = 0.042
    elif abseta < 5.0:
                smear_nominal = 0.288
                smear_up = 0.488
                smear_down = 0.089

    if variation == 0: return smear_nominal
    elif variation == 1: return smear_up
    elif variation == -1: return smear_down
    
#SF for HLT_Mu40
def muonTrig_SF(eta, pt):    
    abseta = abs(eta)
    SF = 1.0
    if abseta >= 0.0 and abseta < 0.90:
        if pt >= 40.   and pt < 50.  : SF = 0.9771
        elif pt >= 50. and pt < 60.  : SF = 0.9748
        elif pt >= 60. and pt < 90.  : SF = 0.9736
        elif pt >= 90. and pt < 140. : SF = 0.9658
        elif pt >= 140. and pt < 500.: SF = 0.9840
        else: SF = 0.9840    
    elif abseta >= 0.90 and abseta < 1.2:
        if pt >= 40.   and pt < 50.  : SF = 0.9626
        elif pt >= 50. and pt < 60.  : SF = 0.9570
        elif pt >= 60. and pt < 90.  : SF = 0.9528
        elif pt >= 90. and pt < 140. : SF = 0.9504
        elif pt >= 140. and pt < 500.: SF = 1.0088
        else: SF = 1.0088    
    elif abseta >= 1.2 and abseta < 2.1:
        if pt >= 40.   and pt < 50.  : SF = 0.9930
        elif pt >= 50. and pt < 60.  : SF = 0.9894
        elif pt >= 60. and pt < 90.  : SF = 0.9827
        elif pt >= 90. and pt < 140. : SF = 0.9908
        elif pt >= 140. and pt < 500.: SF = 0.9970
        else: SF = 0.9970    
    return SF

# SF for muon ID (Tight && relIso <0.12)
def muonID_SF(eta, pt):
    abseta = abs(eta)
    SF = 1.0
    if abseta >= 0.0 and abseta < 0.90:
        if pt >= 40.   and pt < 50.  : SF = 0.9866
        elif pt >= 50. and pt < 60.  : SF = 0.9866
        elif pt >= 60. and pt < 90.  : SF = 0.9895
        elif pt >= 90. and pt < 140. : SF = 1.0049
        elif pt >= 140. and pt < 300.: SF = 1.0283
        elif pt >= 300. and pt < 500.: SF = 1.0198
        else: SF = 1.0198    
    elif abseta >= 0.90 and abseta < 1.2:
        if pt >= 40.   and pt < 50.  : SF = 0.9878
        elif pt >= 50. and pt < 60.  : SF = 0.9900
        elif pt >= 60. and pt < 90.  : SF = 0.9855
        elif pt >= 90. and pt < 140. : SF = 1.0115
        elif pt >= 140. and pt < 300.: SF = 0.9525
        elif pt >= 300. and pt < 500.: SF = 1.0078
        else: SF = 1.0078
    elif abseta >= 1.2 and abseta < 2.1:
        if pt >= 40.   and pt < 50.  : SF = 0.9995
        elif pt >= 50. and pt < 60.  : SF = 0.9988
        elif pt >= 60. and pt < 90.  : SF = 0.9946
        elif pt >= 90. and pt < 140. : SF = 1.0191
        elif pt >= 140. and pt < 300.: SF = 1.0164
        elif pt >= 300. and pt < 500.: SF = 0.6173
        else: SF = 0.6173
    return SF

# SF for HLT_Ele27_WP80
def electronTrig_SF(eta, pt):    
    abseta = abs(eta)
    SF = 1.0
    if abseta >= 0.0 and abseta < 0.80:
        if pt >= 20. and pt < 30.:
            SF = 0.695
        elif pt >= 30. and pt < 40.:
            SF = 0.984
        elif pt >= 40. and pt < 50.:
            SF = 0.999
        elif pt > 50. and pt < 200.:
            SF = 0.999
        else: SF = 0.999    
    elif abseta >= 0.80 and abseta < 1.48:
        if pt >= 20. and pt < 30.:
            SF = 0.462
        elif pt >= 30. and pt < 40.:
            SF = 0.967
        elif pt >= 40. and pt < 50.:
            SF = 0.983
        elif pt > 50. and pt < 200.:
            SF = 0.988
        else: SF = 0.988    
    elif abseta >= 1.48 and abseta < 2.50:
        if pt >= 20. and pt < 30.:
            SF = 0.804
        elif pt >= 30. and pt < 40.:
            SF = 0.991
        elif pt >= 40. and pt < 50.:
            SF = 1.018
        elif pt > 50. and pt < 200.:
            SF = 0.977
        else: SF = 0.977    
    return SF

# SF for electron ID (MVA >0.9 && relIso <0.1)
def electronID_SF(eta, pt):
    abseta = abs(eta)
    SF = 1.0
    if abseta >= 0.0 and abseta < 0.80:
        if pt >= 20. and pt < 30.:
            SF = 0.972
        elif pt >= 30. and pt < 40.:
            SF = 0.950
        elif pt >= 40. and pt < 50.:
            SF = 0.966
        elif pt > 50. and pt < 200.:
            SF = 0.961
        else: SF = 0.961    
    elif abseta >= 0.80 and abseta < 1.48:
        if pt >= 20. and pt < 30.:
            SF = 0.928
        elif pt >= 30. and pt < 40.:
            SF = 0.957
        elif pt >= 40. and pt < 50.:
            SF = 0.961
        elif pt > 50. and pt < 200.:
            SF = 0.963
        else: SF = 0.963    
    elif abseta >= 1.48 and abseta < 2.50:
        if pt >= 20. and pt < 30.:
            SF = 0.834
        elif pt >= 30. and pt < 40.:
            SF = 0.922
        elif pt >= 40. and pt < 50.:
            SF = 0.941
        elif pt > 50. and pt < 200.:
            SF = 0.971
        else: SF = 0.971    
    return SF
