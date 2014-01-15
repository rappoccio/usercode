################################################################################
# A nice review of fitting with binned templates, can be found here:
# http://hepunx.rl.ac.uk/~adye/thesis/html/node51.html
################################################################################

import numpy as np
import matplotlib.pylab as plt
import lichen.lichen as lch
import lichen.pdfs as pdfs
import lichen.iminuit_fitting_utilities as fitutils
import lichen.plotting_utilities as plotutils

import scipy.stats as stats

from datetime import datetime,timedelta

import iminuit as minuit

################################################################################
# Fit function.
################################################################################
def fitfunc(data,p,parnames,params_dict):

    pn = parnames

    flag = p[pn.index('flag')]

    template0 = data[1]
    template1 = data[2]

    num0 = p[pn.index('num0')]
    num1 = p[pn.index('num1')]

    ############################################################################
    # Calc
    ############################################################################

    tot_pdf = (num0*template0[1] + num1*template1[1])

    return tot_pdf







################################################################################
# Extended maximum likelihood function for minuit, normalized already.
################################################################################
def emlf_normalized_minuit(data,p,parnames,params_dict):

    flag = p[parnames.index('flag')]

    num_tot = 0.0
    for name in parnames:
        if 'num' in name:
            num_tot += p[parnames.index(name)]

    tot_pdf = fitfunc(data,p,parnames,params_dict)

    y = data[0][1]
    likelihood_func = (-y*np.log(tot_pdf)).sum()

    ret = likelihood_func + num_tot

    return ret

################################################################################



################################################################################
# Set up a figure for future plotting.
################################################################################

fig0 = plt.figure(figsize=(12,4),dpi=100)
ax00 = fig0.add_subplot(1,2,1)
ax01 = fig0.add_subplot(1,2,2)

################################################################################
# Generate the fitting templates
################################################################################

mu = 2.0
sigma = 0.2
ngen = 100000
nbins = 100
ranges = [0.0, 5.0]

data = np.random.normal(mu,sigma,ngen)
h,xpts,ypts,xpts_err,ypts_err = lch.hist_err(data,bins=nbins,range=ranges,axes=ax00)

norm = float(sum(ypts))
template0 = [xpts.copy(),ypts.copy()/norm]

yexp = stats.expon(loc=0.0,scale=6.0)
data = yexp.rvs(ngen)
data = data[data<ranges[1]]

h,xpts,ypts,xpts_err,ypts_err = lch.hist_err(data,bins=nbins,range=ranges,axes=ax01)

norm = float(sum(ypts))
template1 = [xpts.copy(),ypts.copy()/norm]

print template0
print template1

ax00.set_xlim(ranges[0],ranges[1])
ax01.set_xlim(ranges[0],ranges[1])

################################################################################
# Generate the data.
################################################################################

data = np.random.normal(mu,sigma,100)

nsig = len(data)

yexp = stats.expon(loc=0.0,scale=6.0)
bkg = yexp.rvs(400)
bkg = bkg[bkg<ranges[1]]
data = np.append(data,bkg)

nbkg = len(bkg)

fig1 = plt.figure(figsize=(12,4),dpi=100)
ax10 = fig1.add_subplot(1,2,1)
ax11 = fig1.add_subplot(1,2,2)

h,xpts,ypts,xpts_err,ypts_err = lch.hist_err(data,bins=nbins,range=ranges,axes=ax10)
h,xpts,ypts,xpts_err,ypts_err = lch.hist_err(data,bins=nbins,range=ranges,axes=ax11)
ax10.set_xlim(ranges[0],ranges[1])
ax11.set_xlim(ranges[0],ranges[1])

data = [xpts.copy(),ypts.copy()]

ndata = sum(ypts)

############################################################################
# Declare the fit parameters
############################################################################
params_dict = {}
params_dict['flag'] = {'fix':True,'start_val':0}
params_dict['var_x'] = {'fix':True,'start_val':0,'limits':(ranges[0],ranges[1])}
params_dict['num0'] = {'fix':False,'start_val':100,'limits':(0,ndata),'error':1}
params_dict['num1'] = {'fix':False,'start_val':200,'limits':(0,ndata),'error':1}

params_names,kwd = fitutils.dict2kwd(params_dict)

kwd['errordef'] = 0.5

data_and_pdfs = [data,template0,template1]

f = fitutils.Minuit_FCN([data_and_pdfs],params_dict,emlf_normalized_minuit)

m = minuit.Minuit(f,**kwd)

# For maximum likelihood method.
m.errordef = 0.5

# Up the tolerance.
#m.tol = 1.0

m.migrad()
m.hesse()

values = m.values

print "nsig: ",nsig
print "nbkg: ",nbkg


ax11.set_xlim(ranges[0],ranges[1])
ax11.plot(template0[0],values['num0']*template0[1],'g-',linewidth=3)
ax11.plot(template1[0],values['num1']*template1[1],'r-',linewidth=3)
ax11.plot(template1[0],values['num1']*template1[1]+values['num0']*template0[1],'b-',linewidth=3)

ax10.set_xlim(ranges[0],ranges[1])
#ax10.plot(template0[0],values['num0']*template0[1],'r',ls='steps',fill=True)
binwidth = template0[0][1]-template0[0][0]
ax10.bar(template0[0]-binwidth/2.0,values['num0']*template0[1]+values['num1']*template1[1],color='b',width=binwidth,edgecolor='b')
ax10.bar(template0[0]-binwidth/2.0,values['num1']*template1[1],color='r',width=binwidth,edgecolor='r')


plt.show()
