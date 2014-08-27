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
    if hname == None or 'NNPDF' in hname or 'MSTW' in hname : #or 'pdf' in hname or 'scale' in hname :
        return False
    else :
        return True


####################################################################################
# Here is where we build the model for theta
####################################################################################
def muplusjets(files, infilter, signal, mcstat, ex_to_in):
    if ex_to_in != None : 
        model = build_model_from_rootfile(files, histogram_filter=infilter, include_mc_uncertainties = mcstat, root_hname_to_convention = ex_to_in)
    else :
        model = build_model_from_rootfile(files, histogram_filter=infilter, include_mc_uncertainties = mcstat)
    model.fill_histogram_zerobins()
    model.set_signal_processes(signal)
    for p in model.processes:
        model.add_lognormal_uncertainty('lumi', math.log(1.026), p)
        #model.add_lognormal_uncertainty('subjet_scalefactor', math.log(1.084), p)


    #model.add_lognormal_uncertainty('ttbar_rate', math.log(1.15), 'ttbar')
    model.add_lognormal_uncertainty('rate_st', math.log(1.5), 'SingleTop')
    model.add_lognormal_uncertainty('rate_vjets', math.log(1.5), 'WJets')
    model.add_lognormal_uncertainty('rate_nonsemi', math.log(1.5), 'TTbar_nonSemiLep')
    model.add_lognormal_uncertainty('rate_qcd', math.log(1.5), 'QCD')

    #    model.add_asymmetric_lognormal_uncertainty('scale_vjets', -math.log(1.577), math.log(0.710), 'WJets', obs)
    #    model.add_asymmetric_lognormal_uncertainty('matching_vjets', -math.log(1.104), math.log(1.052), 'WJets', obs)


    ## if muflag:
    ##     for obs in ['mu_0btag_mttbar']:
    ##         for proc in ('wc', 'wb'):
    ##             model.add_asymmetric_lognormal_uncertainty('scale_vjets', -math.log(1.577), math.log(0.710), proc, obs)
    ##             model.add_asymmetric_lognormal_uncertainty('matching_vjets', -math.log(1.104), math.log(1.052), proc, obs)
    ##     for obs in ['mu_1btag_mttbar']:
    ##         for proc in ('wc', 'wb', 'wlight'):
    ##             model.add_asymmetric_lognormal_uncertainty('scale_vjets', -math.log(1.577), math.log(0.710), proc, obs)
    ##             model.add_asymmetric_lognormal_uncertainty('matching_vjets', -math.log(1.104), math.log(1.052), proc, obs)

    ## if eflag:
    ##     for obs in ['el_0btag_mttbar']:
    ##         for proc in ('wc', 'wb'):
    ##             model.add_asymmetric_lognormal_uncertainty('scale_vjets', -math.log(1.584), math.log(0.690), proc, obs)
    ##             model.add_asymmetric_lognormal_uncertainty('matching_vjets', -math.log(1.0447), math.log(1.0706), proc, obs)
    ##         for proc in model.processes:
    ##             model.add_lognormal_uncertainty('elid_rate', math.log(1.05), proc, obs)            
    ##     for obs in ['el_1btag_mttbar']:
    ##         for proc in ('wc', 'wb', 'wlight'):
    ##             model.add_asymmetric_lognormal_uncertainty('scale_vjets', -math.log(1.584), math.log(0.690), proc, obs)
    ##             model.add_asymmetric_lognormal_uncertainty('matching_vjets', -math.log(1.0447), math.log(1.0706), proc, obs)
    ##         for proc in model.processes:
    ##             model.add_lognormal_uncertainty('elid_rate', math.log(1.05), proc, obs)
    
    return model


import exceptions

####################################################################################
# Here is where the constructed model is declared to theta
####################################################################################
def build_model(type, indir='', mcstat = True, ex_to_in = None, infilter = None):
    model = None

    
    if type == 'ttbar_xs' :

        model = muplusjets(
            files=[#'normalized_mujets_ptMET3_subtracted_from_ptMET1.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep6_subtracted_from_etaAbsLep4.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_etaAbsLep7_subtracted_from_etaAbsLep6.root',
                   'NormalizedHists_' + indir + '/normalized2d_mujets_vtxMass7.root'],
            infilter=infilter,
            signal='TTbar',
            mcstat=mcstat,
            ex_to_in=ex_to_in
        )

    else:

        raise exceptions.ValueError('Type %s is undefined' % type)

    #for p in model.distribution.get_parameters():
    #    d = model.distribution.get_distribution(p)
    #    if d['typ'] == 'gauss' and d['mean'] == 0.0 and d['width'] == 1.0:
    #        model.distribution.set_distribution_parameters(p, range = [-5.0, 5.0])
        #if 'rate' in p:
        #    if d['typ'] == 'gauss' and d['mean'] == 0.0 and d['width'] == 1.0:
        #        model.distribution.set_distribution_parameters(p, range = [-5.0, 5.0])
        #else:
        #    if d['typ'] == 'gauss' and d['mean'] == 0.0 and d['width'] == 1.0:
        #        model.distribution.set_distribution_parameters(p, range = [-0.0, 0.0])

    return model



####################################################################################
# Here is the "main" part of the script. 
####################################################################################



useMLE = True
usePL = False

# Building the statistical model :
infilter = histfilter

dirs = ['CT10_nom', 'CT10_pdfup', 'CT10_pdfdown',
        'MSTW_nom', 'MSTW_pdfup', 'MSTW_pdfdown',
        'NNPDF_nom', 'NNPDF_pdfup', 'NNPDF_pdfdown',
        'scaleup', 'scaledown']

ivar = -1
for idir in dirs :
    ivar += 1

    args = {'type': 'ttbar_xs',
            'mcstat':False,
            'infilter':infilter,
            'indir':idir}

    model = build_model(**args)

    #model_summary(model, all_nominal_templates=True, shape_templates=True) 

    parameters = model.get_parameters(['TTbar'])


    if ivar == 0 :
        model_summary(model)

    if useMLE == True :        

        print '------------- MLE RESULTS ' + idir + ' ---------------'

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
        plot(pdbs, 'bs', 'ntoys', 'beta_signal_' + idir + '.pdf')

        pdd = plotdata()
        pdd.histogram(delta_bs, 0.0, 1.0, 100, include_uoflow = True)
        plot(pdd, 'dbs', 'ntoys', 'delta_beta_signal_' + idir + '.pdf')

        pdp = plotdata()
        pdp.histogram(pulls, -5.0, 5.0, 100, include_uoflow = True)
        plot(pdp, 'pull', 'ntoys', 'pull_' + idir + '.pdf')


        # to write the data to a file, use e.g.:
        pdp.write_txt('pull_' + idir + '.txt')

        # to write it to a root file:
        write_histograms_to_rootfile({'pull': pdp.histo(), 'bs': pdbs.histo(), 'delta_bs': pdd.histo()}, 'pulldists_mle_' + idir + '.root')


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
        write_histograms_to_rootfile(histos, 'histos-mle-2d-' + idir + '.root')
        
        if idir == "CT10_nom" :
            report.write_html('htmlout')
            
    if usePL == True :

        print '------------- PL RESULTS ' + idir + ' ---------------'


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
        plot(pdbs, 'bs', 'ntoys', 'pl_beta_signal_' + idir + '.pdf')

        pdd = plotdata()
        pdd.histogram(delta_bs, 0.0, 1.0, 100, include_uoflow = True)
        plot(pdd, 'dbs', 'ntoys', 'pl_delta_beta_signal_' + idir + '.pdf')

        pdp = plotdata()
        pdp.histogram(pulls, -5.0, 5.0, 100, include_uoflow = True)
        plot(pdp, 'pull', 'ntoys', 'pl_pull_' + idir + '.pdf')


        # to write the data to a file, use e.g.:
        pdd.write_txt('pl_dbs_' + idir + '.txt')
        pdp.write_txt('pl_pull_' + idir + '.txt')

        # to write it to a root file:
        write_histograms_to_rootfile({'pull': pdp.histo(), 'bs': pdbs.histo(), 'delta_bs': pdd.histo()}, 'pulldists_pl_' + idir + '.root')

        
        results4 = pl_interval(model, input='data', n=1 , **args)

        print results4
        
        if idir == "CT10_nom" : 
            report.write_html('htmlout')
