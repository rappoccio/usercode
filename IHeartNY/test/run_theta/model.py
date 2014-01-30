def filterqcd( hname ) :
    if 'QCD' not in hname :
        return True
    else :
        return False

def muplusjets(files, infilter, signal, mcstat):
    model = build_model_from_rootfile(files, histogram_filter=infilter, include_mc_uncertainties = mcstat)
    model.fill_histogram_zerobins()
    model.set_signal_processes(signal)
    for p in model.processes:
        model.add_lognormal_uncertainty('lumi', math.log(1.044), p)
        model.add_lognormal_uncertainty('subjet_scalefactor', math.log(1.084), p)


    #model.add_lognormal_uncertainty('ttbar_rate', math.log(1.15), 'ttbar')
    model.add_lognormal_uncertainty('st_rate', math.log(1.5), 'SingleTop')
    model.add_lognormal_uncertainty('st_rate', math.log(1.5), 'SingleTop')


    model.add_lognormal_uncertainty('rate_vjets', math.log(1.5), 'WJets')
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


def build_model(type, jet1 = None, mcstat = True):

    print '-------------------------'
    print 'Hello from build_model!'
    print '-------------------------'

    model = None

    if True :

        model = muplusjets(
            files=['normalized_mujets_vtxMass.root'],
            infilter=filterqcd,
            signal='TTbar',
            mcstat=mcstat
        )

    else:

        raise exceptions.ValueError('Type %s is undefined' % type)

    for p in model.distribution.get_parameters():
        d = model.distribution.get_distribution(p)
        if d['typ'] == 'gauss' and d['mean'] == 0.0 and d['width'] == 1.0:
            model.distribution.set_distribution_parameters(p, range = [-5.0, 5.0])
        #if 'rate' in p:
        #    if d['typ'] == 'gauss' and d['mean'] == 0.0 and d['width'] == 1.0:
        #        model.distribution.set_distribution_parameters(p, range = [-5.0, 5.0])
        #else:
        #    if d['typ'] == 'gauss' and d['mean'] == 0.0 and d['width'] == 1.0:
        #        model.distribution.set_distribution_parameters(p, range = [-0.0, 0.0])

    return model
