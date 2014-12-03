from ROOT import *
from array import array

gStyle.SetOptStat(000000)
gStyle.SetPadTickX(1);
gStyle.SetPadTickY(1);

pdfname = "CT10_nom"
#pdfname = "MSTW_nom"
#pdfname = "NNPDF_nom"
#pdfname = "scaleup"
#pdfname = "scaledown"


### CT10
if pdfname=="CT10_nom": 
    ttbar_list = {'TTbar': {'jer': [(1.2634690276100087, 0.7154450170103156)], 'toptag': [(0.27068285735354075, 0.41726700957069179)], 'btag': [(-0.046314668882932869, 0.9520655129035247)], 'beta_signal': [(0.71574813043861485, 0.097633605379017885)], 'jec': [(0.97617168292539547, 0.43744260802119128)], 'rate_vjets': [(-0.69780289015768782, 0.21368980995097114)], '__nll': [-32815.839342991312], 'lumi': [(-0.092056224095428255, 1.0058140793232841)], 'rate_qcd': [(-0.099389386086757819, 0.57484490447730974)], 'rate_st': [(-0.66296759910477965, 0.85342994255468763)]}}

### MSTW
if pdfname=="MSTW_nom": 
    ttbar_list = {'TTbar': {'jer': [(1.2475494656099031, 0.71432911505903096)], 'toptag': [(0.26727540171602299, 0.41838946215795791)], 'btag': [(-0.04866679289260796, 0.95204120481842947)], 'beta_signal': [(0.70733347424465087, 0.096748254039217496)], 'jec': [(0.96895790585476438, 0.43321278876157526)], 'rate_vjets': [(-0.68375913056841131, 0.21179983153015378)], '__nll': [-32815.709184116859], 'lumi': [(-0.091159638570187468, 1.0058096333509952)], 'rate_qcd': [(-0.088892032811905095, 0.57391601002000048)], 'rate_st': [(-0.67142092173403156, 0.85278496269054094)]}}

### NNPDF
if pdfname=="NNPDF_nom": 
    ttbar_list = {'TTbar': {'jer': [(1.181749181769957, 0.74355532106225719)], 'toptag': [(0.54106867495477318, 0.42463376487957738)], 'btag': [(0.075940226230036795, 0.95638779613291447)], 'beta_signal': [(0.68112168688682373, 0.088902280750787654)], 'jec': [(1.1883611311326503, 0.5285907478660874)], 'rate_vjets': [(-0.69620893373378101, 0.23142750022465985)], '__nll': [-32813.951594629631], 'lumi': [(-0.076355213658798202, 1.0057981737141126)], 'rate_qcd': [(0.18138025981738409, 0.50054733405116836)], 'rate_st': [(-0.6919734714632032, 0.84803113526866325)]}}

### CT10 scaleup
if pdfname=="scaleup": 
    ttbar_list = {'TTbar': {'jer': [(1.1749990511414792, 0.70951877608903646)], 'toptag': [(-0.022171940537548909, 0.40782510471193084)], 'btag': [(-0.22694182110564304, 0.94414560037031481)], 'beta_signal': [(0.76802813853040819, 0.10887152161939173)], 'jec': [(0.79975281419491573, 0.40405124459401809)], 'rate_vjets': [(-0.63431521498066523, 0.20693611867951947)], '__nll': [-32822.795541606029], 'lumi': [(-0.097880234266536012, 1.0058116695518613)], 'rate_qcd': [(-0.24789683249649383, 0.62405983181233848)], 'rate_st': [(-0.66691350436846197, 0.85629053455313942)]}}

### CT10 scaledown
if pdfname=="scaledown": 
    ttbar_list = {'TTbar': {'jer': [(0.99439571964408702, 0.66472726756040013)], 'toptag': [(0.9344652764792446, 0.40838263899966459)], 'btag': [(0.12849103897623868, 0.95293161222459155)], 'beta_signal': [(0.72749104262748654, 0.08687019148691133)], 'jec': [(0.79725663302899119, 0.37283707227988105)], 'rate_vjets': [(-0.54921717314293472, 0.19550504416315628)], '__nll': [-32811.12732859121], 'lumi': [(-0.06014002966935663, 1.0057513872571326)], 'rate_qcd': [(0.34656585147120078, 0.45538512397969333)], 'rate_st': [(-0.75220156031293106, 0.84551081793920335)]}}


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
c1 = TCanvas("c1", "c1", 600, 800)
c1.Draw()
c1.SetLeftMargin(0.25)
c1.SetRightMargin(0.15)

gr2sig.SetLineWidth(0)
gr1sig.SetLineWidth(0)
gr2sig.SetLineColor(kYellow)
gr1sig.SetLineColor(kGreen)
gr2sig.SetFillStyle(1001)
gr2sig.SetFillColor(kYellow)

dummy = TH2F("dummy",";Post-fit nuisance parameter value (#sigma); ",10,-3,3,8,0,8)
dummy.GetYaxis().SetTitleOffset(3)
dummy.GetYaxis().SetLabelSize(0.045)
dummy.GetXaxis().SetTitleSize(0.04)

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

c1.Print("nuisances_"+pdfname+".pdf")
c1.Print("nuisances_"+pdfname+".png")


