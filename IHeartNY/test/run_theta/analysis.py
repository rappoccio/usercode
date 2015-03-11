from ROOT import *

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

    print hname
    
    if hname == None or 'TTbar_semiLep' in hname or 'TTbar_nonSemiLep' in hname:
        return False
    else :
        return True


####################################################################################
# Here is where we build the model for theta
####################################################################################

def lepplusjets(files, infilter, signal, mcstat, elflag=False, muflag=False):

    model = build_model_from_rootfile(files, histogram_filter=infilter, include_mc_uncertainties = mcstat)
    model.fill_histogram_zerobins()
    model.set_signal_processes(signal)
    for p in model.processes:
        print "DEBUG: model.process = " + p
        if (p == 'QCD') or (p == 'ElQCD') or (p == 'MuQCD'): 
            print "DEBUG: model.process = QCD"
            continue
        model.add_lognormal_uncertainty('lumi', math.log(1.026), p)
        
    model.add_lognormal_uncertainty('rate_st', math.log(1.5), 'SingleTop')
    model.add_lognormal_uncertainty('rate_vjets', math.log(1.5), 'WJets')
    #model.add_lognormal_uncertainty('rate_qcd', math.log(2.0), 'QCD')

    ## muon+jets channel
    if muflag:
        print "DEBUG: muon+jets channel considered"
        for obs in ['mu_vtxMass7', 'mu_etaAbsLep6', 'mu_etaAbsLep4']:
            model.add_lognormal_uncertainty('rate_mu_qcd', math.log(2.0), 'QCD' , obs)

    ## electron+jets channel 
    if elflag:
        print "DEBUG: electron+jets channel considered"
        for obs in ['el_vtxMass7', 'el_etaAbsLep6', 'el_etaAbsLep4']:
            model.add_lognormal_uncertainty('rate_el_qcd', math.log(2.0), 'QCD' , obs)
    
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
            muflag = True,
            elflag = True
        )

    ## other cases not defined
    else:
        raise exceptions.ValueError('Type %s is undefined' % type)

    return model



####################################################################################
# Here is the "main" part of the script. 
####################################################################################

useMLE = True
usePL = False

# Building the statistical model :
infilter = histfilter

dirs = ['CT10_nom', 
        'CT10_pdfup', 
        'CT10_pdfdown',
        'MSTW_nom', 
        'MSTW_pdfup', 
        'MSTW_pdfdown',
        'NNPDF_nom', 
        'NNPDF_pdfup', 
        'NNPDF_pdfdown',
        'scaleup', 
        'scaledown'
    ]

## muon channel ('mu') / electron channel ('el') / combined ('comb')
channel = 'comb'

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

    args = {'type': 'ttbar_xs_'+channel,
            'mcstat': True,
            'infilter': infilter,
            'indir': idir,
            'elflag': elflag,
            'muflag': muflag}
    
    model = build_model(**args)
        
    parameters = model.get_parameters(['TTbar'])


    if ivar == 0 :
        model_summary(model)


    ###########################################################################
    ## Maximum likelihood estimate technique
    ###########################################################################
    
    if useMLE == True :        

        print '------------- MLE RESULTS ' + idir + ' ' + channel + ' channel ---------------'

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
        plot(pdbs, 'bs', 'ntoys', 'ThetaPlots/beta_signal_' + idir + '_' + channel + '.pdf')
        
        pdd = plotdata()
        pdd.histogram(delta_bs, 0.0, 1.0, 100, include_uoflow = True)
        plot(pdd, 'dbs', 'ntoys', 'ThetaPlots/delta_beta_signal_' + idir + '_' + channel + '.pdf')
        
        pdp = plotdata()
        pdp.histogram(pulls, -5.0, 5.0, 100, include_uoflow = True)
        plot(pdp, 'pull', 'ntoys', 'ThetaPlots/pull_' + idir + '_' + channel + '.pdf')
        

        # to write the data to a file, use e.g.:
        pdp.write_txt('ThetaPlots/pull_' + idir + '_' + channel + '.txt')

        # to write it to a root file:
        write_histograms_to_rootfile({'pull': pdp.histo(), 'bs': pdbs.histo(), 'delta_bs': pdd.histo()}, 'ThetaPlots/pulldists_mle_' + idir + '_' + channel + '.root')


        results2 = mle(model, input='data', n=1, with_covariance = True)


        print results2
        ivals = results2['TTbar']
        for ikey, ival in ivals.iteritems() :
            if ikey != "__nll" and ikey != "__cov":
                print '{0:20s} : {1:6.2f} +- {2:6.2f}'.format(
                    ikey, ival[0][0], ival[0][1]
                )

        parameters = model.get_parameters(['TTbar'])
        print parameters

        parameter_values = {}
        for p in parameters :
            parameter_values[p] = results2['TTbar'][p][0][0]
        histos = evaluate_prediction(model, parameter_values, include_signal = True)
        write_histograms_to_rootfile(histos, 'histos-mle-2d-' + idir + '_' + channel + '.root')
        
        if idir == "CT10_nom" :
            report.write_html('htmlout_'+channel)

            
    ###########################################################################
    ## Profile likelihood technique
    ###########################################################################

    if usePL == True :

        print '------------- PL RESULTS ' + idir + ' ' + channel + ' channel ---------------'

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
        plot(pdbs, 'bs', 'ntoys', 'ThetaPlots/pl_beta_signal_' + idir + '_' + channel + '.pdf')

        pdd = plotdata()
        pdd.histogram(delta_bs, 0.0, 1.0, 100, include_uoflow = True)
        plot(pdd, 'dbs', 'ntoys', 'ThetaPlots/pl_delta_beta_signal_' + idir + '_' + channel + '.pdf')

        pdp = plotdata()
        pdp.histogram(pulls, -5.0, 5.0, 100, include_uoflow = True)
        plot(pdp, 'pull', 'ntoys', 'ThetaPlots/pl_pull_' + idir + '_' + channel + '.pdf')


        # to write the data to a file, use e.g.:
        pdd.write_txt('ThetaPlots/pl_dbs_' + idir + '_' + channel + '.txt')
        pdp.write_txt('ThetaPlots/pl_pull_' + idir + '_' + channel + '.txt')

        # to write it to a root file:
        write_histograms_to_rootfile({'pull': pdp.histo(), 'bs': pdbs.histo(), 'delta_bs': pdd.histo()}, 'ThetaPlots/pulldists_pl_' + idir + '_' + channel + '.root')

        
        results4 = pl_interval(model, input='data', n=1 , **args)

        print results4
        
        if idir == "CT10_nom" : 
            report.write_html('htmlout_'+channel)
