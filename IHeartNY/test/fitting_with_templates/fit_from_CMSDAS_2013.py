import sys
import ROOT
import numpy as np
from ROOT import RooFit,RooStats

ROOT.gSystem.SetIncludePath('-I$ROOFITSYS/include')

ROOT.gStyle.SetOptStat(111111)
#ROOT.gStyle.SetOptStat(0)

################################################################################
pWs = ROOT.RooWorkspace("myWS")

################################################################################
x = ROOT.RooRealVar ("x","Secondary vertex mass (GeV)",0,5.0)
getattr(pWs,'import')(x)
xframe = x.frame(150)
xframe.SetTitle("")

luminosity = 5695.503 # pb-1

muon_trigger_eff = 0.965
btagging_eff = 0.97 

#pWs.factory("xsec[0,0,0.1]")
#pWs.factory("lumi_nom[5695.503, 4000.0, 6000.0]")
#pWs.factory("lumi_kappa[1.045]")
#pWs.factory("CEXPR::alpha_lumi('pow(lumi_kappa,beta_lumi)',lumi_kappa,beta_lumi[0,-5,5])")
#pWs.factory("prod::lumi(lumi_nom,alpha_lumi)")
################################################################################

samples = ['ttbar','t','tbar','wjets','qcd','mu']
samples_label = ['t#bar{t}','Single-Top','#bar{t}',"W#rightarrow#mu#nu",'QCD','data']
fcolor = [ROOT.kRed+1, ROOT.kMagenta, ROOT.kMagenta, ROOT.kGreen-3,ROOT.kYellow,ROOT.kWhite]
ngen = [6923750.0, 3758227.0, 1935072.0, 57709905.0]
n_pct_err = [0.0, 100.0, 100.0, 100.0]
xsec = [227.0,56.4*3,30.7*3,36257.2]

files = []
hists = []
rdhist = []
rhpdf  = []

hs = ROOT.THStack("hs","Stacked")

ndata = 0

efficiency = []

rooadd_string = ""
pdfs = ROOT.RooArgList()
npdfs = ROOT.RooArgList()
npdfs_list = []

for i,sample in enumerate(samples):
    
    name = "CMSDAS_root_files/%s_skim_plots.root" % (sample)
    
    print name
    files.append(ROOT.TFile(name))

    # These work
    files[i].ls()
    hists.append(files[i].Get("secvtxMass_btag_maxpt_njets4"))

    hists[i].Rebin(2)

    titlename = "%s sample" % (sample)
    hists[i].GetXaxis().SetTitle("Secondary vertex mass (passing selection criteria) GeV/c^{2}")
    hists[i].GetYaxis().SetTitle("# Entries")
    hists[i].SetFillColor(fcolor[i])
    hists[i].SetTitle(titlename)
    '''
    if i==5:
        hists[i].Draw("e")
        ndata = hists[i].GetEntries()
    else:
        hists[i].Draw()
    '''

    if i<4:
        efficiency.append(hists[i].GetEntries()/ngen[i])

    #ROOT.gPad.Update()

    rdhistname = "%s_roodatahist" % (sample)
    rdhist.append(ROOT.RooDataHist(rdhistname,rdhistname,ROOT.RooArgList(x),hists[i]))

    ############################################################################
    # If i==5, import the data that we will be fitting
    ############################################################################
    if i==5:
        getattr(pWs,'import')(rdhist[i])

    rdpdfname = "%s_roohistpdf" % (sample)
    rhpdf.append(ROOT.RooHistPdf(rdpdfname,rdpdfname,ROOT.RooArgSet(x),rdhist[i]))

    getattr(pWs,'import')(rhpdf[i])


    npdfname = "num%s" % (sample)
    print npdfname
    npdftitle = "# %s events" % (sample)
    npdfs_list.append(ROOT.RooRealVar(npdfname,npdftitle,1000))
    #npdfs.Print()

    if i<5:
        pdfs.add(rhpdf[i])
        npdfs.add(npdfs_list[i])
        rooadd_string += "%s" % (rdpdfname)
        if i<4:
            rooadd_string  += " + "

################################################################################
# Calculate the number of events coming from each contributing process
################################################################################
ncontributions = []
for i,x in enumerate(xsec):
    ncontributions.append(luminosity*x*efficiency[i])
    print luminosity,x,efficiency[i],ncontributions[i]


ncontributions.append(4235.99) # Derived from data, QCD stuff

ncontributions[1] = 635.094 # From the COUNTING group! single t
ncontributions[2] = 361.837 # From the COUNTING group! single tbar
ncontributions[3] = 2240.79 # From the COUNTING group! wjets

print "Contributions: "
for s,n in zip(samples[0:5],ncontributions):
    print "%-10s: %f" % (s,n)
print "%-10s: %f" % ("data",hists[5].GetEntries())

ncontrib_pct_err = []
ncontrib_pct_err.append(1.0) # ttbar, WON'T BE USED
ncontrib_pct_err.append(20.0) # t
ncontrib_pct_err.append(20.0) # tbar
ncontrib_pct_err.append(20.0) # wjets
ncontrib_pct_err.append(110.0) # qcd
#ncontrib_pct_err.append(1.0) # qcd
################################################################################
# Start creating the fit paramters in the Workspace
################################################################################
sum_string = ""
model_string = ""
for i,sample in enumerate(samples):
    if i<5:
        name = "n%s_nom[%f, 5.0, 40000.0]" % (sample,ncontributions[i])
        pWs.factory(name)
        kappa_err = (ncontrib_pct_err[i]/100.0) + 1 # 10% err would be 1.10
        print "kappa_err: ",kappa_err
        name = "n%s_kappa[%f]" % (sample,kappa_err);
        pWs.factory(name)
        name = "cexpr::alpha_n%s('pow(n%s_kappa,beta_n%s)',n%s_kappa,beta_n%s[0,-5,5])" % (sample,sample,sample,sample,sample)
        pWs.factory(name)
        name = "prod::n%s(n%s_nom,alpha_n%s)" % (sample,sample,sample)
        pWs.factory(name)
        name = "Gaussian::constr_n%s(beta_n%s,glob_n%s[0,-5,5],1)" % (sample,sample,sample)
        pWs.factory(name)
        if i==0: # ttbar
            model_string += "n%s_nom*%s_roohistpdf" % (sample,sample)
            model_string += ","
        elif i>0 and i<5:
            model_string += "n%s*%s_roohistpdf" % (sample,sample)
            #model_string += "n%s_nom*%s_roohistpdf" % (sample,sample)
            #model_string += "constr_n%s*%s_roohistpdf" % (sample,sample)
            model_string += ","

################################################################################
# Run the fit
################################################################################
#tot_pdf = RooAddPdf("tot_pdf","sig_temp + bkg_temp", RooArgList(sig_temp, bkg_temp), RooArgList(nsig, nbkg))
print "PDFs"
print pdfs
pdfs.Print()
print "nPDFs"
print npdfs
npdfs.Print()
print rooadd_string
#tot_pdf = ROOT.RooAddPdf("tot_pdf",rooadd_string,pdfs,npdfs)
print "Created tot_pdf!"

################################################################################
# Add the model PDF to the workspace
################################################################################
#pWs.factory("SUM::model(nttbar*ttbar_roohistpdf,nqcd*qcd_roohistpdf)")
name = "SUM::model(%s)" % (model_string)
pWs.factory(name)
print name
print "Created the model to which we will be fitting........."

############################################################################
# Data
############################################################################
# create set of observables (will need it for datasets and ModelConfig later)
pObs = pWs.var("x"); # get the pointer to the observable
obs = ROOT.RooArgSet("observables");
obs.add(pObs);
print "Added the observables....................."


################################################################################
# Create the list of global observables
################################################################################
globalObs = ROOT.RooArgSet ("global_obs");
for i,sample in enumerate(samples):
    if i<5 and i!=0:
        #name = "glob_n%s" % (sample)
        name = "n%s_nom" % (sample)
        globalObs.add( pWs.var(name) );

################################################################################
# create set of parameters of interest (POI)
################################################################################
poi = ROOT.RooArgSet("poi");
#poi.add( pWs.var("glob_nttbar") );
poi.add( pWs.var("nttbar_nom") );
#poi.add( pWs.var("beta_nttbar") );

################################################################################
# create set of nuisance parameters
################################################################################
nuis = ROOT.RooArgSet("nuis");
nuis.add( pWs.var("beta_nqcd") );
nuis.add( pWs.var("beta_nt") );
nuis.add( pWs.var("beta_ntbar") );
nuis.add( pWs.var("beta_nwjets") );


sbHypo = RooStats.ModelConfig("SbHypo");
sbHypo.SetWorkspace( pWs );
sbHypo.SetPdf(pWs.pdf("model"))
sbHypo.SetObservables( obs );
sbHypo.SetGlobalObservables( globalObs );
sbHypo.SetParametersOfInterest( poi );
sbHypo.SetNuisanceParameters( nuis );

pWs.var("beta_nttbar").setConstant(False);
pWs.var("beta_nqcd").setConstant(False);
pWs.var("beta_nwjets").setConstant(False);
pWs.var("beta_nt").setConstant(False);
pWs.var("beta_ntbar").setConstant(False);

pWs.var("nwjets_nom").setConstant(True);
pWs.var("nt_nom").setConstant(True);
pWs.var("ntbar_nom").setConstant(True);
pWs.var("nqcd_nom").setConstant(True);

fixed = ROOT.RooArgSet ("fixed");
fixed.add( pWs.var("nwjets_nom") );
fixed.add( pWs.var("nt_nom") );
fixed.add( pWs.var("ntbar_nom") );

#sbHypo.Print()
#pWs.Print()

pNll = sbHypo.GetPdf().createNLL(rdhist[5]);
print "Created the pNll"
pProfile = pNll.createProfile( globalObs ); # do not profile global observables
print "Created the pProfile"
pProfile.getVal()
pProfile.Print("v"); 

sbHypo.Print()
pWs.Print()

pWs.allVars().Print("v")
pWs.allFunctions().Print("v")
pWs.allPdfs().Print("v")

################################################################################
# Print the results
################################################################################
c1 = ROOT.TCanvas("c1","c1")
c1.Divide(1,1)
c1.cd(1)
legend = ROOT.TLegend(0.65,0.6,0.9,0.9)
rdhist[5].plotOn(xframe)
#pWs.pdf("model").plotOn(xframe,RooFit.LineColor(ROOT.kBlue))
pWs.pdf("model").plotOn(xframe,RooFit.Components("qcd_roohistpdf,wjets_roohistpdf,tbar_roohistpdf,ttbar_roohistpdf,t_roohistpdf"),RooFit.LineColor(ROOT.kBlack),RooFit.DrawOption("F"),RooFit.FillColor(fcolor[0]),RooFit.LineWidth(5))
pWs.pdf("model").plotOn(xframe,RooFit.Components("qcd_roohistpdf,wjets_roohistpdf,tbar_roohistpdf,t_roohistpdf"),RooFit.LineColor(ROOT.kBlack),RooFit.DrawOption("LF"),RooFit.FillColor(fcolor[2]))
pWs.pdf("model").plotOn(xframe,RooFit.Components("qcd_roohistpdf,wjets_roohistpdf"),RooFit.LineColor(ROOT.kBlack),RooFit.DrawOption("LF"),RooFit.FillColor(fcolor[3]))
pWs.pdf("model").plotOn(xframe,RooFit.Components("qcd_roohistpdf"),RooFit.LineColor(ROOT.kBlack),RooFit.DrawOption("LF"),RooFit.FillColor(fcolor[4]))
rdhist[5].plotOn(xframe)
xframe.Draw()

legend.AddEntry(rdhist[5],samples_label[i],"p")
for i in range(0,len(samples)):
    if i<5:
        if i!=2:
            legend.AddEntry(hists[i],samples_label[i],"f")

legend.SetFillColor(ROOT.kWhite);
legend.Draw("same")

title = ";%s ;Number of events" % (hists[5].GetEntries())
#xframe.SetTitle(title);
xframe.GetXaxis().SetTitleSize(.058);
xframe.GetXaxis().SetTitleOffset(.75);
xframe.GetYaxis().SetTitleSize(.049);
xframe.GetXaxis().SetLabelSize(.05);
xframe.GetYaxis().SetLabelSize(.038);
xframe.GetYaxis().SetTitleOffset(1.11);
ROOT.gStyle.SetOptStat(0);

#Set text for above graph
text1 = ROOT.TLatex(3.570061,23.08044,"CMS DAS");
text1.SetNDC();
text1.SetTextAlign(13);
text1.SetX(0.1);
text1.SetY(0.948);
text1.SetTextFont(42);
text1.SetTextSizePixels(24);
text1.Draw();

text2 = ROOT.TLatex(3.570061,23.08044,"5.7 fb^{-1} at #sqrt{s} = 8 TeV");
text2.SetNDC();
text2.SetTextAlign(13);
text2.SetX(0.62);
text2.SetY(0.956);
text2.SetTextFont(42);
text2.SetTextSizePixels(24);
text2.Draw();

################################################################################
# Get the systematic errors (pct!)
################################################################################
lumi_frac_err = 0.04

sys_err = []
sys_err.append(0.029/0.965) # Muon trigger efficiency
sys_err.append(0.03/0.97) # b-tag efficiency
sys_err.append(0.05) # jet-energy scale
sys_err.append(0.034) # lepton ID/reco/trigger
sys_err.append(0.025) # pileup
sys_err.append(0.034) # PDF
sys_err.append(0.02) # renormalization and factorization scale
sys_err.append(0.02) # matching threshold
sys_err.append(0.02) # ISR and FSR

tot_sys_pct = 0.0
for se in sys_err:
    tot_sys_pct += (se*se)

tot_sys_pct = np.sqrt(tot_sys_pct)

################################################################################
# Get the final numbers
################################################################################
nttbar_from_fit = pWs.var("nttbar_nom").getVal()
nttbar_err = pWs.var("nttbar_nom").getError()
nttbar_from_template = ncontributions[0]
print nttbar_from_fit,nttbar_from_template,nttbar_err

mc_xsec = 227.0
xsec_ttbar = mc_xsec*(nttbar_from_fit/nttbar_from_template)*muon_trigger_eff*btagging_eff
pct_err = nttbar_err/nttbar_from_fit

#text_string = "#sigma(p#bar{p} #rightarrow t#bar{t}) = %4.0f #pm %2.0f(stat) #pm %2.0f(sys) #pm %2.0f(lumi) pb^{-1}" % (xsec_ttbar,xsec_ttbar*pct_err,xsec_ttbar*tot_sys_pct,xsec_ttbar*lumi_frac_err)
#text3 = ROOT.TPaveText(2.0,400.0,5.0,600.0,"NDC")
text3 = ROOT.TPaveText(0.65, 0.25, 0.98, 0.55,"NDC")
text_string = "#sigma(pp #rightarrow t#bar{t}) = %4.0f pb" % (xsec_ttbar)
text3.AddText(text_string)
text_string = "#pm %2.0f(stat)" % (xsec_ttbar*pct_err)
text3.AddText(text_string)
text_string = "#pm %2.0f(sys)" % (xsec_ttbar*tot_sys_pct)
text3.AddText(text_string)
text_string = "#pm %2.0f(lumi)" % (xsec_ttbar*lumi_frac_err)
text3.AddText(text_string)
#text3 = ROOT.TLatex(3.570061,23.08044,text_string)
#text3.SetNDC();
#text3.SetTextAlign(13);
#text3.SetX(0.48);
#text3.SetY(0.55);
text3.SetTextFont(42);
text3.SetTextSizePixels(24);
text3.SetTextColor(0)
text3.SetFillColor(1)
text3.SetBorderSize(0)
text3.Draw();


ROOT.gPad.Update()

c1.SaveAs("xsec_fit.png")



################################################################################
if __name__=="__main__":
    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = raw_input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]




