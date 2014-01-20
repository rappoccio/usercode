import numpy as np
import matplotlib.pylab as plt
import lichen.lichen as lch
import lichen.pdfs as pdfs
import lichen.iminuit_fitting_utilities as fitutils
import lichen.plotting_utilities as plotutils
import matplotlib.colors as colors

import scipy.stats as stats

from datetime import datetime,timedelta

import iminuit as minuit

# Binned likelihood fitting
# http://hepunx.rl.ac.uk/~adye/thesis/html/node51.html

luminosity = 5695.503 # pb-1

mc_xsec = 227.0

muon_trigger_eff = 0.965
btagging_eff = 0.97

muon_btag_eff_prod = muon_trigger_eff*btagging_eff

samples = ['ttbar','t','tbar','wjets','qcd','mu']
samples_label = [r'$t\bar{t}$',r'single-$t$',r'single-$\bar{t}$',r"$W$+jets",r'QCD',r'data']

kRedp1 = (0.80,0,0)
kMagenta = (1.0,0.0,1.0)
kGreenm3 = (0.2,0.8,0.2)
kYellow = (1.0,1.0,0.0)
fcolor = [kRedp1, kMagenta, kMagenta, kGreenm3,kYellow]

# What is this?
ngen = [6923750.0, 3758227.0, 1935072.0, 57709905.0, 100000000.0] # The last is just a dummy value
n_pct_err = [0.0, 100.0, 100.0, 100.0]
xsec_mc = [227.0, 56.4*3, 30.7*3, 36257.2]
pct_uncertainty = [100.0,20.0,20.0,20.0,110.0]


# First guess at the contributions. Do we use this?
#first_guess = [0.0,0.0,0.0,0.0,0.0]
#first_guess[0] = 16165.289 # ttbar, what's left over
#first_guess[1] = 635.094 # From the COUNTING group! single t
#first_guess[2] = 361.837 # From the COUNTING group! single tbar
#first_guess[3] = 2240.79 # From the COUNTING group! wjets
#first_guess[4] = 4235.99 # Derived from data, QCD stuff

first_guess = []
first_guess.append([]) # njets = 0
first_guess.append([1958.87,13779.1/2, 13779.1/2, 60893.0, 17119.8]) # njets = 1
first_guess.append([11705.5,17155.0/2, 17155.0/2, 17531.1, 12111.7]) # njets = 2
first_guess.append([22655.6,8262.75/2, 8262.75/2, 4360.26, 5084.18]) # njets = 3
#first_guess.append([18927.9,984.944/2, 984.944/2, 746.164, 1427.61]) # njets = 4
first_guess.append([18927.9,635, 361, 2240.0, 4235.99]) # njets = 4, from CMS DAS
first_guess.append([7420.38,180.444/2, 180.444/2, 91.322, 0.001]) # njets = 5
first_guess.append([2941.43,28.312/2, 28.312/2, 27.282, 0.000]) # njets = 6

nominal = []
uncert = []
efficiency = []
for njets in range(0,7):
    nominal.append([])
    uncert.append([])
    efficiency.append([])
    for i,n in enumerate(first_guess[njets]):
        num = n
        if n<10:
            num = 10
        nominal[njets].append(num)
        #uncert[njets].append(np.sqrt(num))
        uncert[njets].append(num*pct_uncertainty[i]/100.0)
        efficiency[njets].append(num/ngen[i])

print first_guess
print nominal
print uncert

njets_min = 4
njets_max = 4

################################################################################
# Xsec to n-events
################################################################################
def xsec_to_n(xsec,lumi,mcx,eff,random_effs):

    n_from_template = lumi*mcx*eff
    n = (xsec*n_from_template)/(mcx*random_effs)

    return n

################################################################################
# Fit function.
################################################################################
def fitfunc(nums,templates):

    tot_pdf = np.zeros(len(templates[0][1]))
    #print nums
    #print templates
    #norm = sum(nums)
    #print "IN FITFUNC CALL:"
    for n,t in zip(nums,templates):
        #n /= norm
        #print n
        #print t[1]
        tot_pdf += n*t[1] # Use the y-values
        #print tot_pdf
    #tot_pdf /= ntot # DO I NEED THIS?
    #print nums

    return tot_pdf







################################################################################
# Extended maximum likelihood function for minuit, normalized already.
################################################################################
def emlf_normalized_minuit(data_and_pdfs,p,parnames,params_dict):

    data = data_and_pdfs[0]
    templates = data_and_pdfs[1]

    flag = p[parnames.index('flag')]

    tot_from_ttbar = 0

    tot_pdf = 0.0
    likelihood_func = 0.0
    for j in range(njets_min,njets_max+1):
        nums = []
        
        for i,s in enumerate(samples[0:-1]):
            if i==0: # ttbar
                nttbar = xsec_to_n(p[parnames.index('xsec_ttbar')],luminosity,mc_xsec,efficiency[j][i],muon_btag_eff_prod)
                nums.append(nttbar)
                tot_from_ttbar += nttbar
            else:
                name = "num_%s_njets%d" % (s,j)
                nums.append(p[parnames.index(name)])

        tot_pdf = fitfunc(nums,templates[j-njets_min])
        y = data[j-njets_min][1]

        likelihood_func += (-y[y>0]*np.log(tot_pdf[y>0])).sum()

    ############################################################################
    # Calculate the total number of events, as determined by the fit.
    # This is used in the function to minimize.
    ############################################################################
    num_tot = 0.0
    for name in parnames:
        if 'num' in name and 'ttbar' not in name:
            num_tot += p[parnames.index(name)]
    # Handle the ttbar separately
    num_tot += tot_from_ttbar

    #print "num_tot: ",num_tot
    #ret = likelihood_func - fitutils.pois(num_tot,ndata)
    #num_tot = num00 + num10
    ret = likelihood_func + num_tot
    #print "ret: ",ret,likelihood_func,num_tot
    for j in range(njets_min,njets_max+1):
        for i,s in enumerate(samples[0:-1]):
            name = "num_%s_njets%d" % (s,j)
            n = p[parnames.index(name)]
            name = "nominal_%s_njets%d" % (s,j)
            n0 = p[parnames.index(name)]
            name = "uncert_%s_njets%d" % (s,j)
            sigma = p[parnames.index(name)]

            #print n,n0,sigma
            #gaussian_constraint = ((n-n0)**2)/(2*(sigma**2)) #- np.log(n)
            gaussian_constraint = ((n-n0)**2)/(2*(sigma**2)) 
            #print "gc: ",gaussian_constraint
            ret += gaussian_constraint
    #print "ret: ",ret

    return ret

################################################################################




################################################################################
# Generate the fitting templates
################################################################################

#nbins = 100
ranges = [0.0, 5.0]

################################################################################
# Read in the data.
################################################################################
data = []
for j in range(njets_min,njets_max+1):
    infilename = "templates_for_iminuit_fit_CMSDAS/output_mu_njets%d.dat" % (j)
    infile = open(infilename,'rb')

    content = np.array(infile.read().split()).astype('float')
    index = np.arange(0,len(content),2)
    x = content[index]
    y = content[index+1]

    #'''
    # Rebin
    print "nbins: ",len(x)
    index = np.arange(0,len(x),2)
    tempx = (x[index]+x[index+1])/2.0
    tempy = (y[index]+y[index+1])
    x = tempx
    y = tempy
    #'''

    data.append([x.copy(),y.copy()])
    #plt.figure()
    #plt.plot(x,y,'bo',ls='steps')

################################################################################
# Read in the templates.
################################################################################
templates = []
for j in range(njets_min,njets_max+1):
    templates.append([])
    for i,s in enumerate(samples[0:-1]):
        infilename = "templates_for_iminuit_fit_CMSDAS/output_%s_njets%d.dat" % (s,j)
        infile = open(infilename,'rb')

        content = np.array(infile.read().split()).astype('float')
        index = np.arange(0,len(content),2)
        x = content[index]
        y = content[index+1]

        #'''
        # Rebin
        print "nbins: ",len(x)
        index = np.arange(0,len(x),2)
        tempx = (x[index]+x[index+1])/2.0
        tempy = (y[index]+y[index+1])
        x = tempx
        y = tempy
        #'''

        norm = float(sum(y))
        print j,i,norm
        templates[j-njets_min].append([x.copy(),y.copy()/norm])
        efficiency[j][i] = norm/ngen[i]
        print infilename,sum(y)
        #plt.figure()
        #plt.plot(x,y,'ro',ls='steps')

#plt.show()
#exit()

ndata = []
for d in data:
    ndata.append(float(sum(d[1])))

print "ndata: "
print ndata
#exit()
############################################################################
# Declare the fit parameters
############################################################################
params_dict = {}
params_dict['flag'] = {'fix':True,'start_val':0}
params_dict['var_x'] = {'fix':True,'start_val':0,'limits':(ranges[0],ranges[1])}
params_dict['ntemplates'] = {'fix':True,'start_val':5,'limits':(1,10)}
params_dict['xsec_ttbar'] = {'fix':False,'start_val':227,'limits':(100,1000)}

for i,s in enumerate(samples[0:-1]):
    for j in range(njets_min,njets_max+1):
        nd = ndata[j-njets_min]

        name = "num_%s_njets%d" % (s,j)
        if s=='ttbar':
            params_dict[name] = {'fix':True,'start_val':first_guess[j][i],'limits':(0,nd)}
        else:
            params_dict[name] = {'fix':False,'start_val':first_guess[j][i],'limits':(0,nd)}

        #'''
        name = "nominal_%s_njets%d" % (s,j)
        if s=='ttbar':
            params_dict[name] = {'fix':True,'start_val':nominal[j][i],'limits':(0,nd)}
        else:
            params_dict[name] = {'fix':True,'start_val':nominal[j][i],'limits':(0,nd)}

        name = "uncert_%s_njets%d" % (s,j)
        if s=='ttbar':
            params_dict[name] = {'fix':True,'start_val':uncert[j][i],'limits':(0,nd)}
        else:
            params_dict[name] = {'fix':True,'start_val':uncert[j][i],'limits':(0,nd)}
        #'''


params_names,kwd = fitutils.dict2kwd(params_dict)
kwd['errordef'] = 0.5 # For maximum likelihood method
#kwd['print_level'] = 1

data_and_pdfs = [data,templates]

f = fitutils.Minuit_FCN([data_and_pdfs],params_dict,emlf_normalized_minuit)

m = minuit.Minuit(f,**kwd)
#m.tol = 100

m.migrad(ncall=10000)
print "RUNNING HESSE"
m.hesse()

#m.minos()

values = m.values
errors = m.errors

################################################################################
# Set up a figure for plotting.
################################################################################

#fig0 = plt.figure(figsize=(9,6),dpi=100)
#ax00 = fig0.add_subplot(2,2,1)
#ax01 = fig0.add_subplot(2,2,2)
#ax02 = fig0.add_subplot(2,2,3)
#ax03 = fig0.add_subplot(2,2,4)

'''
ax11.set_xlim(ranges[0],ranges[1])
ax00.plot(template0[0],values['num0']*template0[1],'g-',linewidth=3)
ax00.plot(template1[0],values['num1']*template1[1],'r-',linewidth=3)
ax00.plot(template1[0],values['num1']*template1[1]+values['num0']*template0[1],'b-',linewidth=3)
'''

binwidth = templates[0][0][0][1]-templates[0][0][0][0]

#ax00.set_xlim(ranges[0],ranges[1])
#ax00.plot(data[0][0],data[0][1],'ko')

#ax01.set_xlim(ranges[0],ranges[1])
#ax01.plot(data[1][0],data[1][1],'ko')

for j in range(njets_min,njets_max+1):
    plt.figure(figsize=(9,6),dpi=100)
    plt.xlim(ranges[0],ranges[1])
    plt.errorbar(data[j-njets_min][0],data[j-njets_min][1],yerr=np.sqrt(data[j-njets_min][1]),fmt='ko',label=samples_label[-1])

    for i,s in enumerate(samples[0:-1]):
        tempx = templates[j-njets_min][i][0]-binwidth/2.0
        tempy = np.zeros(len(templates[0][0][1]))
        for k in range(i,5):
            if k==0: # ttbar
                nttbar = xsec_to_n(values['xsec_ttbar'],luminosity,mc_xsec,efficiency[j][k],muon_btag_eff_prod)
                tempy += nttbar*templates[j-njets_min][k][1]
            else:
                name = "num_%s_njets%d" % (samples[k],j)
                tempy += values[name]*templates[j-njets_min][k][1]
        plt.bar(tempx,tempy,color=fcolor[i],width=binwidth,edgecolor=fcolor[i],label=samples_label[i])
        #plt.figure()
        #plt.bar(templates[j-njets_min][i][0]-binwidth/2.0,values[name]*templates[j-njets_min][i][1],color='b',width=binwidth,edgecolor='b')
    plt.legend()

    plt.xlabel('Secondary vertex mass (GeV)')
    plt.ylabel('Events / 0.067 GeV')
    plt.title(r'5.7 fb$^{-1}$ at $\sqrt{s} = 8$ TeV')
    name = "xsec_fit_iminuit_min%d_max%d_njets%d.png" % (njets_min,njets_max,j)
    plt.savefig(name)

for j in range(njets_min,njets_max+1):
    nums = []
    for i,s in enumerate(samples[0:-1]):
        name = "num_%s_njets%d" % (s,j)
        print "%-16s: %10.3f +\- %6.3f" % (name, values[name], errors[name])


print "ndata: "
print ndata
for e in efficiency:
    print e

print "xsec: ",values['xsec_ttbar']
'''
for j in range(njets_min,njets_max+1):
    nttbar_from_template = luminosity*mc_xsec*efficiency[j][0]
    name = "num_%s_njets%d" % ('ttbar',j)
    ttxsec = mc_xsec*(values[name]/nttbar_from_template)*muon_trigger_eff*btagging_eff
    print "ttxsec: %f" % (ttxsec)
'''


plt.show()
