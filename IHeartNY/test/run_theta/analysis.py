from ROOT import *

def histfilter( hname ) :
    return True

def muplusjets(files, infilter, signal, mcstat):
    model = build_model_from_rootfile(files, histogram_filter=infilter, include_mc_uncertainties = mcstat)
    model.fill_histogram_zerobins()
    model.set_signal_processes(signal)
    for p in model.processes:
        model.add_lognormal_uncertainty('lumi', math.log(1.026), p)
        #model.add_lognormal_uncertainty('subjet_scalefactor', math.log(1.084), p)


    #model.add_lognormal_uncertainty('ttbar_rate', math.log(1.15), 'ttbar')
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

    if type == 'ttbar_xs' :

        model = muplusjets(
            files=[#'normalized_mujets_ptMET3_subtracted_from_ptMET1.root', 'normalized_mujets_ptMET5_subtracted_from_ptMET3.root',
                   'normalized_mujets_vtxMass6_subtracted_from_vtxMass5.root',
                   'normalized_mujets_vtxMass6.root'],
            infilter=histfilter,
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

    print model
    return model



# Code introduced by theta_driver

# Building the statistical model
args = {'type': 'ttbar_xs'}

model = build_model(**args)


model_summary(model, all_nominal_templates=True, shape_templates=True) 

parameters = model.get_parameters(['TTbar'])
print parameters

print '------------- MLE RESULTS ---------------'

args = {}

results1 = mle(model, input='toys:1.', n=10 , with_covariance=True, **args)
results2 = mle(model, input='data', n=1 , with_covariance=True, **args)

print results2


print '------------- PL RESULTS ---------------'


args = {}

results3 = pl_interval(model, input='toys:1.', n=10 ,  **args)
results4 = pl_interval(model, input='data', n=1 , **args)

print results4



report.write_html('htmlout')
