from ROOT import *
from array import array

gStyle.SetOptStat(000000)
gStyle.SetPadTickX(1);
gStyle.SetPadTickY(1);


pdfnames = ["CT10_nom_qcd", "CT10_pdfup_qcd", "CT10_pdfdown_qcd"]
channels = ["mu", "el", "comb"]

### THESE BELOW ARE FOR EXTERNALIZE LUMINOSITY & B-TAGGING !!! ###

for pdfname in pdfnames :
    for ich in channels :
        
        # ---------------------------------- muon only fit ----------------------------------
        if pdfname=="CT10_nom_qcd" and ich=="mu": 
            ttbar_list =  {'TTbar': {'jer': [(0.76082263797137306, 0.80476350343085834)], 'toptag': [(0.65036555779541927, 0.43047203868575395)], 'beta_signal': [(0.64786212443587576, 0.088263437238547238)], 'jec': [(0.60647859069807564, 0.66659408633467443)], 'rate_vjets': [(-0.2395793318057311, 0.16004208973182379)], 'rate_mu_qcd': [(-0.21453226923387672, 0.34369412964747731)], 'rate_st': [(-0.67653959679468512, 0.87876638962490161)]}}

        if pdfname=="CT10_pdfup_qcd" and ich=="mu": 
            ttbar_list =  {'TTbar': {'jer': [(0.66932149576545752, 0.80151848810695114)], 'toptag': [(0.55624043150677493, 0.43902696930634239)], 'beta_signal': [(0.52686871790544587, 0.074313355104996814)], 'jec': [(0.53709802224918612, 0.67451131013829302)], 'rate_vjets': [(-0.29918065084088419, 0.16880691247656379)], 'rate_mu_qcd': [(-0.13753522081015032, 0.32193629161410514)], 'rate_st': [(-0.64453720367111089, 0.88418228183817194)]}}
            
        if pdfname=="CT10_pdfdown_qcd" and ich=="mu": 
            ttbar_list =  {'TTbar': {'jer': [(0.80685828678732285, 0.80277503063360944)], 'toptag': [(0.73868029977492577, 0.42213026231723738)], 'beta_signal': [(0.77545878131542612, 0.10237482510182538)], 'jec': [(0.63385360641216537, 0.66175654281871343)], 'rate_vjets': [(-0.19100415758715933, 0.15453800801072862)], 'rate_mu_qcd': [(-0.29336149064193962, 0.36518316137322143)], 'rate_st': [(-0.71414149666166926, 0.87358317622866066)]}}
            
        # ---------------------------------- electron only fit ----------------------------------
        if pdfname=="CT10_nom_qcd" and ich=="el": 
            ttbar_list =  {'TTbar': {'rate_el_qcd': [(0.030879452845862469, 0.37712401616722752)], 'jer': [(-1.6573688721324418, 0.72964952673026573)], 'toptag': [(-0.15942596127739614, 0.29046554655515827)], 'beta_signal': [(0.81681446511923306, 0.0850863517907956)], 'jec': [(0.50462880390499099, 0.50461105568495335)], 'rate_vjets': [(0.33860574697835955, 0.20648107167430141)], 'rate_st': [(-0.12435929204405712, 0.92054471615130196)]}}

        if pdfname=="CT10_pdfup_qcd" and ich=="el": 
            ttbar_list =  {'TTbar': {'rate_el_qcd': [(-0.029475128608773892, 0.39150452869843383)], 'jer': [(-1.5292484802422726, 0.72853456085795298)], 'toptag': [(-0.26490181383539563, 0.30270360421885562)], 'beta_signal': [(0.67619211946369173, 0.075213406820911044)], 'jec': [(0.49124589678824443, 0.50847713024237595)], 'rate_vjets': [(0.28394193705962495, 0.22287706633671123)], 'rate_st': [(0.028589698029544818, 0.93737436512131156)]}}

        if pdfname=="CT10_pdfdown_qcd" and ich=="el": 
            ttbar_list =  {'TTbar': {'rate_el_qcd': [(0.084263578867942418, 0.36473162124915487)], 'jer': [(-1.7633300871948145, 0.73209335644676699)], 'toptag': [(-0.068325281089529705, 0.28285807755392484)], 'beta_signal': [(0.96790787131355649, 0.096346780209462968)], 'jec': [(0.51036043874994919, 0.50386527514520496)], 'rate_vjets': [(0.36824847468599492, 0.19732447595265684)], 'rate_st': [(-0.22565343466080884, 0.90964048901929595)]}}

        # ---------------------------------- combined fit ----------------------------------
        if pdfname=="CT10_nom_qcd" and ich=="comb": 
            ttbar_list =  {'TTbar': {'rate_el_qcd': [(0.75902833924527646, 0.17140705338827447)], 'jer': [(0.77124413194032715, 0.59042944114787477)], 'toptag': [(-0.34263877906274109, 0.19805688696142928)], 'beta_signal': [(0.87851982531950723, 0.064923793640532246)], 'jec': [(0.91480615796515896, 0.54599707127061026)], 'rate_vjets': [(-0.2375505965375857, 0.14031427174950126)], 'rate_mu_qcd': [(-1.8863481843998335, 0.4451048285412621)], 'rate_st': [(-0.040270514898540284, 0.91255716590020275)]}}
            
        if pdfname=="CT10_pdfup_qcd" and ich=="comb": 
            ttbar_list =  {'TTbar': {'rate_el_qcd': [(0.7458320636823188, 0.17287056218598806)], 'jer': [(0.73355969286239842, 0.61575778632592926)], 'toptag': [(-0.51923633089419929, 0.20461980685246628)], 'beta_signal': [(0.74501364574441609, 0.059329436283324211)], 'jec': [(0.86845701937508168, 0.53855351411518715)], 'rate_vjets': [(-0.35501868187956059, 0.15448015208508023)], 'rate_mu_qcd': [(-1.8966114261113189, 0.44664813174760493)], 'rate_st': [(0.17758376762979117, 0.93324030916124423)]}}
            
        if pdfname=="CT10_pdfdown_qcd" and ich=="comb": 
            ttbar_list =  {'TTbar': {'rate_el_qcd': [(0.77343856168741953, 0.16915822113393633)], 'jer': [(0.79324766808440506, 0.57048561964529876)], 'toptag': [(-0.19161809512873029, 0.19424998186308476)], 'beta_signal': [(1.0204911510946757, 0.071540411557591166)], 'jec': [(0.92862460885783926, 0.53734364759973052)], 'rate_vjets': [(-0.16362384249024167, 0.13099653466972161)], 'rate_mu_qcd': [(-1.9061301831290027, 0.4476159238093611)], 'rate_st': [(-0.18403241507511409, 0.89433106682540053)]}}
            

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
		name = "N(el-QCD)"
            if systematic=="rate_mu_qcd":
		name = "N(mu-QCD)"
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


