from ROOT import *
from array import array

gStyle.SetOptStat(000000)
gStyle.SetPadTickX(1);
gStyle.SetPadTickY(1);


pdfnames = ["CT10_nom"]
channels = ["mu", "el", "comb"]

### THESE BELOW ARE FOR EXTERNALIZE LUMINOSITY & B-TAGGING !!! ###

for pdfname in pdfnames :
    for ich in channels :
        
        # ---------------------------------- muon only fit ----------------------------------
        if pdfname=="CT10_nom" and ich=="mu": 
            ttbar_list =  {'TTbar': {'jer': [(-0.77931890856180608, 0.81379560066648449)], 'toptag': [(0.6586858782193673, 0.42264512674567578)], 'beta_signal': [(0.630509396567833, 0.08514554491771853)], 'jec': [(0.44891077651424083, 0.69065833212011452)], 'rate_vjets': [(-0.18463233344196356, 0.1584170171215516)],'rate_mu_qcd': [(-0.22277428912753183, 0.34284884262195719)], 'rate_st': [(-0.70576430421703817, 0.87482163919247879)]}}
            
        # ---------------------------------- electron only fit ----------------------------------
        if pdfname=="CT10_nom" and ich=="el": 
            ttbar_list =  {'TTbar': {'rate_el_qcd': [(0.15306695019446323, 0.33966491614145411)], 'jer': [(-0.51376501102572847, 0.75526244620785532)], 'toptag': [(-0.22781280603180115, 0.29187707455261386)], 'beta_signal': [(0.80157092866860924, 0.084991846467460164)], 'jec': [(0.53515872408527554, 0.49815591863927)], 'rate_vjets': [(0.21755889743461135, 0.19477485749322437)],'rate_st': [(-0.027741507842472882, 0.93025709323689132)]}}

        # ---------------------------------- combined fit ----------------------------------
        if pdfname=="CT10_nom" and ich=="comb": 
            ttbar_list =  {'TTbar': {'rate_el_qcd': [(0.75507761232084658, 0.16951151257831024)], 'jer': [(-0.71573407998317395, 0.72878463501301527)], 'toptag': [(-0.35829830091598502, 0.19519173702041726)], 'beta_signal': [(0.8661089420811392, 0.064419949034970059)], 'jec': [(0.87167877275330352, 0.50280662601445003)], 'rate_vjets': [(-0.19474147684252824, 0.13674273389086858)],'rate_mu_qcd': [(-2.0377931263756026, 0.46911426924780941)], 'rate_st': [(-0.077712270117586607, 0.91421697492568721)]}}
            

        signal_list = ttbar_list['TTbar']

        nuisances = TGraphErrors()
        gr1sig = TGraphErrors()
        gr2sig = TGraphErrors()

        nPoint = -1
        for systematic in sorted(signal_list.keys()):

            if systematic is '__nll' or systematic is "beta_signal" or systematic is '__cov':
                continue
            nPoint += 1
	
            print systematic, signal_list[systematic][0][0], signal_list[systematic][0][1]

            nuisances.SetPoint(nPoint, signal_list[systematic][0][0], nPoint+0.5)
            nuisances.SetPointError(nPoint, signal_list[systematic][0][1], 0)

            gr1sig.SetPoint(nPoint, 0, nPoint)
            gr1sig.SetPointError(nPoint, 1, 1)	
            gr2sig.SetPoint(nPoint, 0, nPoint)
            gr2sig.SetPointError(nPoint, 2, 1)
	

        # tcanvas
        c1 = TCanvas("c1", "c1", 500, 600)
        c1.Draw()
        c1.SetLeftMargin(0.25)
        c1.SetRightMargin(0.10)
        c1.SetTopMargin(0.05)
        c1.SetBottomMargin(0.13)

        gr2sig.SetLineWidth(0)
        gr1sig.SetLineWidth(0)
        gr2sig.SetLineColor(kYellow)
        gr1sig.SetLineColor(kGreen)
        gr2sig.SetFillStyle(1001)
        gr2sig.SetFillColor(kYellow)

        nbins = 8-2
        if (ich=="comb"):
            nbins = 9-2
        dummy = TH2F("dummy",";Post-fit nuisance parameter value (#sigma); ",10,-3,3,nbins,0,nbins)
        dummy.GetYaxis().SetTitleOffset(3)
        dummy.GetYaxis().SetLabelSize(0.055)
        dummy.GetXaxis().SetTitleSize(0.045)
        
        nBin = 0
        for systematic in sorted(signal_list.keys()):
            if systematic is '__nll' or systematic is 'beta_signal' or systematic is '__cov':
		continue
	
            if systematic is "toptag":
		name = "Top-tagging"
            if systematic=="btag":
		name = "b-tagging"
            if systematic=="lumi":
		name = "Luminosity"
            if systematic=="jec":
		name = "JEC"
            if systematic=="jer":
		name = "JER"
            if systematic=="rate_qcd":
		name = "N(QCD)"
            if systematic=="rate_el_qcd":
		name = "N(el QCD)"
            if systematic=="rate_mu_qcd":
		name = "N(mu QCD)"
            if systematic=="rate_st":
		name = "N(single top)"
            if systematic=="rate_vjets":
		name = "N(W+jets)"

            dummy.GetYaxis().SetBinLabel(nBin+1, name)
            nBin += 1


        dummy.Draw()
        gr2sig.Draw("5 same")

        gr1sig.SetFillStyle(1001)
        gr1sig.SetFillColor(kGreen)
        gr1sig.Draw("5 same")

        nuisances.SetMarkerStyle(21)
        nuisances.Draw("P same")

        dummy.Draw("same,axis")

        c1.Print("nuisances_"+pdfname+"_"+ich+"_extlumibtag.pdf")
        c1.Print("nuisances_"+pdfname+"_"+ich+"_extlumibtag.png")


