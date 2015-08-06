from ROOT import *

####################################################################################
## which nuisance parameters? 

extBtag = True
extLumi = True
extJet = False
extTopTag = False

extName = ""
if extBtag:
    extName += "_nobtag"
if extLumi:
    extName += "_nolumi"
if extJet:
    extName += "_nojet"
if extTopTag:
    extName += "_notoptag"

qcdUnc = 10000.0

####################################################################################
# We have to externalize the PDF and Q2 uncertainties.
# This is done by skipping them in the nominal variations,
# but then re-running with "nominal" set to "PDF up", "PDF down", etc, respectively.
# Thus, for each running (nominal, pdfup, pdfdown, scaleup, scaledown), there is
# a histogram filter to get rid of unwanted bits, and a histname modifier that
# changes the name to the appropriate one when recentering on the externalized
# "up" and "down" variations. 
####################################################################################

def histfilter( hname ) :

    if hname == None or 'TTbar_semiLep' in hname or 'TTbar_nonSemiLep' in hname:
        return False
    elif extBtag and 'btag' in hname:  ## remove b-tagging nuisance parameter
        return False
    elif extJet and ('jer' in hname or 'jec' in hname):  ## remove JER/JEC nuisance parameter
        return False
    elif extTopTag and 'toptag' in hname: ## fix top tagging nuisance parameter
        return False
    else :
        return True


####################################################################################
# Here is where we build the model for theta
####################################################################################

def lepplusjets(files, infilter, signal, mcstat, nptbin, fittype='', elflag=False, muflag=False):

    model = build_model_from_rootfile(files, histogram_filter=infilter, include_mc_uncertainties = mcstat)
    model.fill_histogram_zerobins()
    model.set_signal_processes(signal)
    if extLumi == False:
        for p in model.processes: 
            if (p == 'QCD') or (p == 'ElQCD') or (p == 'MuQCD'): 
                continue
            model.add_lognormal_uncertainty('lumi', math.log(1.026), p)
        
    model.add_lognormal_uncertainty('rate_st', math.log(1.5), 'SingleTop')
    model.add_lognormal_uncertainty('rate_vjets', math.log(1.5), 'WJets')

    ## muon+jets channel
    if muflag:
        print "DEBUG: muon+jets channel considered"
        if nptbin == '1' :
            if fittype == '' or fittype == 'htLep6' or fittype == '2temp0t' or fittype == '2temp46' or fittype == 'etaAbsLep4only':
                model.add_lognormal_uncertainty('rate_mu_qcd', math.log(qcdUnc), 'QCD' , 'mu_etaAbsLep4')
            if fittype == 'htLep46' or fittype == 'htLep467' or fittype == '2temp0t' or fittype == '2temp46' or fittype == 'htLep4only':
                model.add_lognormal_uncertainty('rate_mu_qcd', math.log(qcdUnc), 'QCD' , 'mu_htLep4')
            if fittype == '' or fittype == '2temp46' or fittype == 'etaAbsLep6only':
                model.add_lognormal_uncertainty('rate_mu_qcd', math.log(qcdUnc), 'QCD' , 'mu_etaAbsLep6')
            if fittype == 'htLep6' or fittype == 'htLep46' or fittype == 'htLep467' or fittype == '2temp0t' or fittype == '2temp46' or fittype == 'htLep6only':
                model.add_lognormal_uncertainty('rate_mu_qcd', math.log(qcdUnc), 'QCD' , 'mu_htLep6')
            if fittype == '' or fittype == 'htLep6' or fittype == 'htLep46' or fittype == '2temp0t' or fittype == '2temp46' or fittype == 'vtxMass7only':
                model.add_lognormal_uncertainty('rate_mu_qcd', math.log(qcdUnc), 'QCD' , 'mu_vtxMass7')
            if fittype == 'htLep467' or fittype == 'htLep7only':
                model.add_lognormal_uncertainty('rate_mu_qcd', math.log(qcdUnc), 'QCD', 'mu_htLep7')
        if nptbin == '2' :
            for obs in ['mu_vtxMass7Low', 'mu_htLep6Low', 'mu_etaAbsLep4Low',
                        'mu_vtxMass7High', 'mu_htLep6High', 'mu_etaAbsLep4High']:
                model.add_lognormal_uncertainty('rate_mu_qcd', math.log(qcdUnc), 'QCD' , obs)
        if nptbin == 'Low' :
            for obs in ['mu_vtxMass7Low', 'mu_htLep6Low', 'mu_etaAbsLep4Low']:
                model.add_lognormal_uncertainty('rate_mu_qcd', math.log(qcdUnc), 'QCD' , obs)
        if nptbin == 'High' :
            for obs in ['mu_vtxMass7High', 'mu_htLep6High', 'mu_etaAbsLep4High']:
                model.add_lognormal_uncertainty('rate_mu_qcd', math.log(qcdUnc), 'QCD' , obs)

    ## electron+jets channel 
    if elflag:
        print "DEBUG: electron+jets channel considered"
        if nptbin == '1' :
            if fittype == '' or fittype == 'htLep6' or fittype == '2temp0t' or fittype == '2temp46' or fittype == 'etaAbsLep4only':
                model.add_lognormal_uncertainty('rate_el_qcd', math.log(qcdUnc), 'QCD' , 'el_etaAbsLep4')
            if fittype == 'htLep46' or fittype == 'htLep467' or fittype == '2temp0t' or fittype == '2temp46' or fittype == 'htLep4only':
                model.add_lognormal_uncertainty('rate_el_qcd', math.log(qcdUnc), 'QCD' , 'el_htLep4')
            if fittype == '' or fittype == '2temp46' or fittype == 'etaAbsLep6only':
                model.add_lognormal_uncertainty('rate_el_qcd', math.log(qcdUnc), 'QCD' , 'el_etaAbsLep6')
            if fittype == 'htLep6' or fittype == 'htLep46' or fittype == 'htLep467' or fittype == '2temp0t' or fittype == '2temp46' or fittype == 'htLep6only':
                model.add_lognormal_uncertainty('rate_el_qcd', math.log(qcdUnc), 'QCD' , 'el_htLep6')
            if fittype == '' or fittype == 'htLep6' or fittype == 'htLep46' or fittype == '2temp0t' or fittype == '2temp46' or fittype == 'vtxMass7only':
                model.add_lognormal_uncertainty('rate_el_qcd', math.log(qcdUnc), 'QCD' , 'el_vtxMass7')
            if fittype == 'htLep467' or fittype == 'htLep7only':
                model.add_lognormal_uncertainty('rate_el_qcd', math.log(qcdUnc), 'QCD', 'el_htLep7')
        if nptbin == '2' :
            for obs in ['el_vtxMass7Low', 'el_htLep6Low', 'el_etaAbsLep4Low',
                        'el_vtxMass7High', 'el_htLep6High', 'el_etaAbsLep4High']:
                model.add_lognormal_uncertainty('rate_el_qcd', math.log(qcdUnc), 'QCD' , obs)
        if nptbin == 'Low' :
            for obs in ['el_vtxMass7Low', 'el_htLep6Low', 'el_etaAbsLep4Low']:
                model.add_lognormal_uncertainty('rate_el_qcd', math.log(qcdUnc), 'QCD' , obs)
        if nptbin == 'High' :
            for obs in ['el_vtxMass7High', 'el_htLep6High', 'el_etaAbsLep4High']:
                model.add_lognormal_uncertainty('rate_el_qcd', math.log(qcdUnc), 'QCD' , obs)
    
    return model


import exceptions

####################################################################################
# Here is where the constructed model is declared to theta
####################################################################################

def build_model(type, indir='', mcstat = True, infilter = None, elflag=False, muflag=False):

    model = None

    ## muon+jets channel ONLY
    if type == 'ttbar_xs_mu' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep6_subtracted_from_etaAbsLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep7_subtracted_from_etaAbsLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_vtxMass7.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = '',
            muflag = True    
        )

    elif type == 'ttbar_xs_mu_htLep6' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep6_subtracted_from_etaAbsLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_htLep7_subtracted_from_htLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_vtxMass7.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'htLep6',
            muflag = True    
        )

    elif type == 'ttbar_xs_mu_htLep46' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_htLep6_subtracted_from_htLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_htLep7_subtracted_from_htLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_vtxMass7.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'htLep46',
            muflag = True    
        )

    elif type == 'ttbar_xs_mu_htLep467' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_htLep6_subtracted_from_htLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_htLep7_subtracted_from_htLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_htLep7.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'htLep467',
            muflag = True    
        )

    elif type == 'ttbar_xs_mu_2temp0t' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep6_subtracted_from_etaAbsLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_htLep6_subtracted_from_htLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_htLep7_subtracted_from_htLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_vtxMass7.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = '2temp0t',
            muflag = True    
        )

    elif type == 'ttbar_xs_mu_2temp46' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep6_subtracted_from_etaAbsLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_htLep6_subtracted_from_htLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep7_subtracted_from_etaAbsLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_htLep7_subtracted_from_htLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_vtxMass7.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = '2temp46',
            muflag = True    
        )

    elif type == 'ttbar_xs_mu_etaAbsLep4only' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep6_subtracted_from_etaAbsLep4.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'etaAbsLep4only',
            muflag = True    
        )

    elif type == 'ttbar_xs_mu_htLep4only' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_htLep6_subtracted_from_htLep4.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'htLep4only',
            muflag = True    
        )

    elif type == 'ttbar_xs_mu_etaAbsLep6only' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep7_subtracted_from_etaAbsLep6.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'etaAbsLep6only',
            muflag = True    
        )

    elif type == 'ttbar_xs_mu_htLep6only' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_htLep7_subtracted_from_htLep6.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'htLep6only',
            muflag = True    
        )
        
    elif type == 'ttbar_xs_mu_vtxMass7only' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_vtxMass7.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'vtxMass7only',
            muflag = True    
        )

    ## muon+jets channel ONLY
    elif type == 'ttbar_xs_mu_2bin' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep6Low_subtracted_from_etaAbsLep4Low.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep7Low_subtracted_from_etaAbsLep6Low.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_vtxMass7Low.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep6High_subtracted_from_etaAbsLep4High.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep7High_subtracted_from_etaAbsLep6High.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_vtxMass7High.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '2',
            muflag = True    
        )

    elif type == 'ttbar_xs_mu_Lowbin' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep6Low_subtracted_from_etaAbsLep4Low.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep7Low_subtracted_from_etaAbsLep6Low.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_vtxMass7Low.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = 'Low',
            muflag = True    
        )

    elif type == 'ttbar_xs_mu_Highbin' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep6High_subtracted_from_etaAbsLep4High.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep7High_subtracted_from_etaAbsLep6High.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_vtxMass7High.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = 'High',
            muflag = True    
        )
        
    ## electron+jets channel ONLY
    elif type == 'ttbar_xs_el' :

        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep6_subtracted_from_etaAbsLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep7_subtracted_from_etaAbsLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_vtxMass7.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = '',
            elflag = True
        )

    elif type == 'ttbar_xs_el_htLep6' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep6_subtracted_from_etaAbsLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_htLep7_subtracted_from_htLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_vtxMass7.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'htLep6',
            elflag = True    
        )

    elif type == 'ttbar_xs_el_htLep46' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_eljets_htLep6_subtracted_from_htLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_htLep7_subtracted_from_htLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_vtxMass7.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'htLep46',
            elflag = True    
        )

    elif type == 'ttbar_xs_el_htLep467' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_eljets_htLep6_subtracted_from_htLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_htLep7_subtracted_from_htLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_htLep7.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'htLep467',
            elflag = True    
        )

    elif type == 'ttbar_xs_el_2temp0t' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep6_subtracted_from_etaAbsLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_htLep6_subtracted_from_htLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_htLep7_subtracted_from_htLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_vtxMass7.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = '2temp0t',
            elflag = True    
        )

    elif type == 'ttbar_xs_el_2temp46' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep6_subtracted_from_etaAbsLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_htLep6_subtracted_from_htLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep7_subtracted_from_etaAbsLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_htLep7_subtracted_from_htLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_vtxMass7.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = '2temp46',
            elflag = True    
        )

    elif type == 'ttbar_xs_el_etaAbsLep4only' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep6_subtracted_from_etaAbsLep4.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'etaAbsLep4only',
            elflag = True    
        )

    elif type == 'ttbar_xs_el_htLep4only' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_eljets_htLep6_subtracted_from_htLep4.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'htLep4only',
            elflag = True    
        )

    elif type == 'ttbar_xs_el_etaAbsLep6only' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep7_subtracted_from_etaAbsLep6.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'etaAbsLep6only',
            elflag = True    
        )

    elif type == 'ttbar_xs_el_htLep6only' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_eljets_htLep7_subtracted_from_htLep6.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'htLep6only',
            elflag = True    
        )
        
    elif type == 'ttbar_xs_el_vtxMass7only' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_eljets_vtxMass7.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'vtxMass7only',
            elflag = True    
        )

    elif type == 'ttbar_xs_el_2bin' :

        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep6Low_subtracted_from_etaAbsLep4Low.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep7Low_subtracted_from_etaAbsLep6Low.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_vtxMass7Low.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep6High_subtracted_from_etaAbsLep4High.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep7High_subtracted_from_etaAbsLep6High.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_vtxMass7High.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '2',
            elflag = True
        )

    elif type == 'ttbar_xs_el_Lowbin' :

        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep6Low_subtracted_from_etaAbsLep4Low.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep7Low_subtracted_from_etaAbsLep6Low.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_vtxMass7Low.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = 'Low',
            elflag = True
        )

    elif type == 'ttbar_xs_el_Highbin' :

        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep6High_subtracted_from_etaAbsLep4High.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep7High_subtracted_from_etaAbsLep6High.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_vtxMass7High.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = 'High',
            elflag = True
        )

    ## COMBINED lepton+jets channel
    elif type == 'ttbar_xs_comb' :

        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep6_subtracted_from_etaAbsLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep7_subtracted_from_etaAbsLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_vtxMass7.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep6_subtracted_from_etaAbsLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep7_subtracted_from_etaAbsLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_vtxMass7.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            muflag = True,
            elflag = True
        )

    elif type == 'ttbar_xs_comb_htLep6' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep6_subtracted_from_etaAbsLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_htLep7_subtracted_from_htLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_vtxMass7.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep6_subtracted_from_etaAbsLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_htLep7_subtracted_from_htLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_vtxMass7.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'htLep6',
            muflag = True,
            elflag = True
        )

    elif type == 'ttbar_xs_comb_htLep46' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_htLep6_subtracted_from_htLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_htLep7_subtracted_from_htLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_vtxMass7.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_htLep6_subtracted_from_htLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_htLep7_subtracted_from_htLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_vtxMass7.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'htLep46',
            muflag = True,
            elflag = True
        )

    elif type == 'ttbar_xs_comb_htLep467' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_htLep6_subtracted_from_htLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_htLep7_subtracted_from_htLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_htLep7.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_htLep6_subtracted_from_htLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_htLep7_subtracted_from_htLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_htLep7.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'htLep467',
            muflag = True,
            elflag = True
        )

    elif type == 'ttbar_xs_comb_2temp0t' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep6_subtracted_from_etaAbsLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_htLep6_subtracted_from_htLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_htLep7_subtracted_from_htLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_vtxMass7.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep6_subtracted_from_etaAbsLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_htLep6_subtracted_from_htLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_htLep7_subtracted_from_htLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_vtxMass7.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = '2temp0t',
            muflag = True,
            elflag = True
        )

    elif type == 'ttbar_xs_comb_2temp46' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep6_subtracted_from_etaAbsLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_htLep6_subtracted_from_htLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep7_subtracted_from_etaAbsLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_htLep7_subtracted_from_htLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_vtxMass7.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep6_subtracted_from_etaAbsLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_htLep6_subtracted_from_htLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep7_subtracted_from_etaAbsLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_htLep7_subtracted_from_htLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_vtxMass7.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = '2temp46',
            muflag = True,
            elflag = True
        )

    elif type == 'ttbar_xs_comb_etaAbsLep4only' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep6_subtracted_from_etaAbsLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep6_subtracted_from_etaAbsLep4.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'etaAbsLep4only',
            muflag = True,
            elflag = True
        )

    elif type == 'ttbar_xs_comb_htLep4only' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_htLep6_subtracted_from_htLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_htLep6_subtracted_from_htLep4.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'htLep4only',
            muflag = True,
            elflag = True
        )

    elif type == 'ttbar_xs_comb_etaAbsLep6only' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep7_subtracted_from_etaAbsLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep7_subtracted_from_etaAbsLep6.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'etaAbsLep6only',
            muflag = True,
            elflag = True
        )

    elif type == 'ttbar_xs_comb_htLep6only' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_htLep7_subtracted_from_htLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_htLep7_subtracted_from_htLep6.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'htLep6only',
            muflag = True,
            elflag = True
        )
        
    elif type == 'ttbar_xs_comb_vtxMass7only' :
        
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_mujets_vtxMass7.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_vtxMass7.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '1',
            fittype = 'vtxMass7only',
            muflag = True,
            elflag = True
        )
        
    elif type == 'ttbar_xs_comb_2bin' :

        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep6Low_subtracted_from_etaAbsLep4Low.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep7Low_subtracted_from_etaAbsLep6Low.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_vtxMass7Low.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep6Low_subtracted_from_etaAbsLep4Low.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep7Low_subtracted_from_etaAbsLep6Low.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_vtxMass7Low.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep6High_subtracted_from_etaAbsLep4High.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep7High_subtracted_from_etaAbsLep6High.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_vtxMass7High.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep6High_subtracted_from_etaAbsLep4High.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep7High_subtracted_from_etaAbsLep6High.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_vtxMass7High.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = '2',
            muflag = True,
            elflag = True
        )

    elif type == 'ttbar_xs_comb_Lowbin' :
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep6Low_subtracted_from_etaAbsLep4Low.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep7Low_subtracted_from_etaAbsLep6Low.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_vtxMass7Low.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep6Low_subtracted_from_etaAbsLep4Low.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep7Low_subtracted_from_etaAbsLep6Low.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_vtxMass7Low.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = 'Low',
            muflag = True,
            elflag = True
        )

    elif type == 'ttbar_xs_comb_Highbin' :
        model = lepplusjets(
            files=['NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep6High_subtracted_from_etaAbsLep4High.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_etaAbsLep7High_subtracted_from_etaAbsLep6High.root',
                   'NormalizedHists_' + indir + '/normalized2d_eljets_vtxMass7High.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep6High_subtracted_from_etaAbsLep4High.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep7High_subtracted_from_etaAbsLep6High.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_vtxMass7High.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            nptbin = 'High',
            muflag = True,
            elflag = True
        )

    ## other cases not defined
    else:
        raise exceptions.ValueError('Type %s is undefined' % type)

    return model


####################################################################################
# theta modification options
####################################################################################

opts = Options()
opts.set('minimizer', 'minuit_tolerance_factor', '1000')
opts.set('minimizer', 'strategy', 'robust')


####################################################################################
# Here is the "main" part of the script. 
####################################################################################

useMLE = True
usePL = False

# Building the statistical model :
infilter = histfilter

dirs = [
    #'CT10_nom',
    #'CT10_pdfup', 
    #'CT10_pdfdown',
    #'MSTW_nom', 
    #'MSTW_pdfup', 
    #'MSTW_pdfdown',
    #'NNPDF_nom', 
    #'NNPDF_pdfup', 
    #'NNPDF_pdfdown',
    #'scaleup', 
    #'scaledown'
    'MG'
]

## muon channel ('mu') / electron channel ('el') / combined ('comb')
channel = 'comb'

## # pt bins
nptbin = '1'

## for output file/plot names
binname = ''
if nptbin != '1':
    binname = '_'+nptbin+'bin'

fittype = ''

fitname = ''
if fittype != '':
    fitname = '_'+fittype

elflag = False
muflag = False
if channel == 'el':
    elflag = True
elif channel == 'mu':
    muflag = True
elif channel == 'comb':
    elflag = True
    muflag = True
else:
    print "INVALID CHANNEL OPTION!"
    raise exceptions.ValueError('chosen channel is undefined!')


ivar = -1
for idir in dirs :
    ivar += 1

    args = {'type': 'ttbar_xs_'+channel+binname+fitname,
            'mcstat': False,
            'infilter': infilter,
            'indir': idir,
            'elflag': elflag,
            'muflag': muflag}
    
    print "Building for ttbar_xs_"+channel+binname+fitname
    
    model = build_model(**args)
        
    parameters = model.get_parameters(['TTbar'])


    if ivar == 0 :
        model_summary(model)

    
    ###########################################################################
    ## Maximum likelihood estimate technique
    ###########################################################################
    
    if useMLE == True :        

        print '------------- MLE RESULTS ' + idir + ' ' + channel + ' channel ' + nptbin + 'bin ' + fittype + ' ---------------'

        results1 = mle(model, input='toys:1.', n=1000)

        bs = []
        delta_bs = []
        pulls = []

        for b, db in results1['TTbar']['beta_signal']:
            bs.append(b)
            delta_bs.append(db)
            pulls.append((1 - b)/db)

        pdbs = plotdata()
        pdbs.histogram(bs, 0.0, 2.0, 100, include_uoflow = True)
        plot(pdbs, 'bs', 'ntoys', 'ThetaPlots/beta_signal_' + idir + '_' + channel + extName + binname + fitname + '.pdf')
        
        pdd = plotdata()
        pdd.histogram(delta_bs, 0.0, 1.0, 100, include_uoflow = True)
        plot(pdd, 'dbs', 'ntoys', 'ThetaPlots/delta_beta_signal_' + idir + '_' + channel + extName + binname + fitname + '.pdf')
        
        pdp = plotdata()
        pdp.histogram(pulls, -5.0, 5.0, 100, include_uoflow = True)
        plot(pdp, 'pull', 'ntoys', 'ThetaPlots/pull_' + idir + '_' + channel + extName + binname + fitname + '.pdf')
        

        # to write it to a root file:
        write_histograms_to_rootfile({'pull': pdp.histo(), 'bs': pdbs.histo(), 'delta_bs': pdd.histo()}, 'ThetaPlots/pulldists_mle_' + idir + '_' + channel + extName + binname + fitname + '.root')


        #results2 = mle(model, input='data', n=1, with_covariance = True)
        results2 = mle(model, input='data', n=1, with_covariance = True, options=opts)

        print results2
        ivals = results2['TTbar']

        my_tt_err = 0
        my_wj_err = 0
        my_st_err = 0
        my_eqcd_err = 0
        my_muqcd_err = 0
        my_toptag = 0
        my_toptag_err = 0
        my_toptagLow = 0
        my_toptagLow_err = 0
        my_toptagHigh = 0
        my_toptagHigh_err = 0

        for ikey, ival in ivals.iteritems() :
            if ikey != "__nll" and ikey != "__cov":
                print '{0:20s} : {1:6.2f} +- {2:6.2f}'.format(
                    ikey, ival[0][0], ival[0][1]
                )

            ## for printing out resulting relative uncertainty for each background source 
            if ikey == "beta_signal":
                my_tt_err = ival[0][1] / ival[0][0]
            elif ikey == "toptag":
                my_toptag = ival[0][0]
                my_toptag_err = ival[0][1]
            elif ikey == "toptagLow":
                my_toptagLow = ival[0][0]
                my_toptagLow_err = ival[0][1]
            elif ikey == "toptagHigh":
                my_toptagHigh = ival[0][0]
                my_toptagHigh_err = ival[0][1]
            elif ikey == "rate_st":
                if (ival[0][0] > 0): 
                    my_st_err = 0.5*ival[0][1] / (1.0+0.5*ival[0][0])
                else:
                    my_st_err = 0.5*ival[0][1] * (1.0-0.5*ival[0][0])
            elif ikey == "rate_vjets":
                if (ival[0][0] > 0): 
                    my_wj_err = 0.5*ival[0][1] / (1.0+0.5*ival[0][0])
                else:
                    my_wj_err = 0.5*ival[0][1] * (1.0-0.5*ival[0][0])
            elif ikey == "rate_mu_qcd":
                if (ival[0][0] > 0): 
                    my_muqcd_err = 0.5*ival[0][1] / (1.0+0.5*ival[0][0])
                else:
                    my_muqcd_err = 0.5*ival[0][1] * (1.0-0.5*ival[0][0])
            elif ikey == "rate_el_qcd":
                if (ival[0][0] > 0): 
                    my_eqcd_err = 0.5*ival[0][1] / (1.0+0.5*ival[0][0])
                else:
                    my_eqcd_err = 0.5*ival[0][1] * (1.0-0.5*ival[0][0])
                        
                    
        print "    {"+str(my_tt_err)+", "+str(my_st_err)+", "+str(my_wj_err)+", "+str(my_muqcd_err)+", "+str(my_eqcd_err)+"}, // bkg error for "+idir
        toptag_post = (1.0 + 0.25*my_toptag) 
        toptagLow_post = (1.0 + 0.25*my_toptagLow) 
        toptagHigh_post = (1.0 + 0.25*my_toptagHigh) 

        if channel=="mu":
            if nptbin == '1':
                print "if options.pdf == \"" + idir + "\" and options.lepType == \"muon\" : toptag_post = " + str(toptag_post)
            if nptbin == 'Low':
                print "if options.pdf == \"" + idir + "\" and options.lepType == \"muon\" : toptagLow_post = " + str(toptagLow_post)
            if nptbin == 'High':
                print "if options.pdf == \"" + idir + "\" and options.lepType == \"muon\" : toptagHigh_post = " + str(toptagHigh_post)
            if nptbin == '2':
                print "if options.pdf == \"" + idir + "\" and options.lepType == \"muon\" : toptagLow_post = " + str(toptagLow_post)
                print "if options.pdf == \"" + idir + "\" and options.lepType == \"muon\" : toptagHigh_post = " + str(toptagHigh_post)
        elif channel=="el":
            if nptbin == '1':
                print "if options.pdf == \"" + idir + "\" and options.lepType == \"ele\" : toptag_post = "+ str(toptag_post)
            if nptbin == 'Low':
                print "if options.pdf == \"" + idir + "\" and options.lepType == \"ele\" : toptagLow_post = "+ str(toptagLow_post)
            if nptbin == 'High':
                print "if options.pdf == \"" + idir + "\" and options.lepType == \"ele\" : toptagHigh_post = "+ str(toptagHigh_post)
            if nptbin == '2':
                print "if options.pdf == \"" + idir + "\" and options.lepType == \"ele\" : toptagLow_post = "+ str(toptagLow_post)
                print "if options.pdf == \"" + idir + "\" and options.lepType == \"ele\" : toptagHigh_post = "+ str(toptagHigh_post)
        else:
            if nptbin == '1':
                print "if options.pdf == \"" + idir + "\" and options.lepType == \"comb\" : toptag_post = "+ str(toptag_post)
            if nptbin == 'Low':
                print "if options.pdf == \"" + idir + "\" and options.lepType == \"comb\" : toptagLow_post = "+ str(toptagLow_post)
            if nptbin == 'High':
                print "if options.pdf == \"" + idir + "\" and options.lepType == \"comb\" : toptagHigh_post = "+ str(toptagHigh_post)
            if nptbin == '2':
                print "if options.pdf == \"" + idir + "\" and options.lepType == \"comb\" : toptagLow_post = "+ str(toptagLow_post)
                print "if options.pdf == \"" + idir + "\" and options.lepType == \"comb\" : toptagHigh_post = "+ str(toptagHigh_post)

        parameters = model.get_parameters(['TTbar'])
        print parameters

        parameter_values = {}
        for p in parameters :
            parameter_values[p] = results2['TTbar'][p][0][0]
        histos = evaluate_prediction(model, parameter_values, include_signal = True)
        write_histograms_to_rootfile(histos, 'histos-mle-2d-' + idir + '_' + channel + extName + binname + fitname + '.root')
        
        ## option to print html output file
        #if idir == "CT10_nom" :
        #    report.write_html('htmlout_'+channel)

            
    ###########################################################################
    ## Profile likelihood technique
    ###########################################################################

    if usePL == True :

        print '------------- PL RESULTS ' + idir + ' ' + channel + ' channel ' + nptbin + 'bin ' + fittype + ' ---------------'

        args = {}

        results3 = pl_interval(model, input='toys:1.', n=1000 ,  **args)

        bs = []
        delta_bs = []
        pulls = []

        for ival in results3['TTbar'][0.0] :
            bs.append( ival )
        ii = 0
        for ival in results3['TTbar'][0.68268949213708585] :
            delta_bs.append( 0.5 * ( abs( bs[ii] - ival[0] ) + abs(ival[1] - bs[ii])  ) )
            ii += 1
            
        for ii in xrange(len(bs)) :
            pulls.append( (1 - bs[ii]) / delta_bs[ii] )
            
        pdbs = plotdata()
        pdbs.histogram(bs, 0.0, 2.0, 100, include_uoflow = True)
        plot(pdbs, 'bs', 'ntoys', 'ThetaPlots/pl_beta_signal_' + idir + '_' + channel + extName + binname + fitname + '.pdf')

        pdd = plotdata()
        pdd.histogram(delta_bs, 0.0, 1.0, 100, include_uoflow = True)
        plot(pdd, 'dbs', 'ntoys', 'ThetaPlots/pl_delta_beta_signal_' + idir + '_' + channel + extName + binname + fitname + '.pdf')

        pdp = plotdata()
        pdp.histogram(pulls, -5.0, 5.0, 100, include_uoflow = True)
        plot(pdp, 'pull', 'ntoys', 'ThetaPlots/pl_pull_' + idir + '_' + channel + extName + binname + fitname + '.pdf')


        # to write the data to a file, use e.g.:
        pdd.write_txt('ThetaPlots/pl_dbs_' + idir + '_' + channel + extName + binname + fitname + '.txt')
        pdp.write_txt('ThetaPlots/pl_pull_' + idir + '_' + channel + extName + binname + fitname + '.txt')

        # to write it to a root file:
        write_histograms_to_rootfile({'pull': pdp.histo(), 'bs': pdbs.histo(), 'delta_bs': pdd.histo()}, 'ThetaPlots/pulldists_pl_' + idir + '_' + channel + extName + binname + fitname + '.root')

        
        results4 = pl_interval(model, input='data', n=1 , **args)

        print results4

        ## option to print html output file
        #if idir == "CT10_nom" : 
        #    report.write_html('htmlout_'+channel)
