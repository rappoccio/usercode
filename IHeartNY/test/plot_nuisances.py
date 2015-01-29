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
    #    ttbar_list = {'TTbar': {'jer': [(1.2634690276100087, 0.7154450170103156)], 'toptag': [(0.27068285735354075, 0.41726700957069179)], 'btag': [(-0.046314668882932869, 0.9520655129035247)], 'beta_signal': [(0.71574813043861485, 0.097633605379017885)], 'jec': [(0.97617168292539547, 0.43744260802119128)], 'rate_vjets': [(-0.69780289015768782, 0.21368980995097114)], '__nll': [-32815.839342991312], 'lumi': [(-0.092056224095428255, 1.0058140793232841)], 'rate_qcd': [(-0.099389386086757819, 0.57484490447730974)], 'rate_st': [(-0.66296759910477965, 0.85342994255468763)]}}
    ttbar_list = {'TTbar': {'jer': [(1.4021640440889553, 0.71297313410252494)], 'toptag': [(0.44082071840368325, 0.43283844846045627)], 'btag': [(0.023110133188328094, 0.95213853005869864)], 'beta_signal': [(0.6784555521468385, 0.095066402062898958)], 'jec': [(0.75454182597001185, 0.44305413767355539)], 'rate_vjets': [(-0.49962057195622106, 0.21881632855211317)], '__nll': [-35105.764310247738], 'lumi': [(-0.095008293439509409, 1.0077743618940598)], 'rate_qcd': [(-0.20899499522929152, 0.34895037506818294)], 'rate_st': [(-0.88403121787851013, 0.83361316581940426)]}}

### MSTW
if pdfname=="MSTW_nom": 
    #    ttbar_list = {'TTbar': {'jer': [(1.2475494656099031, 0.71432911505903096)], 'toptag': [(0.26727540171602299, 0.41838946215795791)], 'btag': [(-0.04866679289260796, 0.95204120481842947)], 'beta_signal': [(0.70733347424465087, 0.096748254039217496)], 'jec': [(0.96895790585476438, 0.43321278876157526)], 'rate_vjets': [(-0.68375913056841131, 0.21179983153015378)], '__nll': [-32815.709184116859], 'lumi': [(-0.091159638570187468, 1.0058096333509952)], 'rate_qcd': [(-0.088892032811905095, 0.57391601002000048)], 'rate_st': [(-0.67142092173403156, 0.85278496269054094)]}}
    ttbar_list = {'TTbar': {'jer': [(1.3831450046370117, 0.71183591047229167)], 'toptag': [(0.44291010218367227, 0.43475506546609965)], 'btag': [(0.015788555197682911, 0.95242420454120635)], 'beta_signal': [(0.66884784229298844, 0.094138412966220053)], 'jec': [(0.74561398849245475, 0.44187674106872465)], 'rate_vjets': [(-0.48375219933277008, 0.21743468221583589)], '__nll': [-35105.620911006503], 'lumi': [(-0.09361805842933886, 1.0077751985836814)], 'rate_qcd': [(-0.19925180943422485, 0.34736360504362496)], 'rate_st': [(-0.88727497379381215, 0.83337694160792908)]}}

### NNPDF
if pdfname=="NNPDF_nom": 
    #    ttbar_list = {'TTbar': {'jer': [(1.181749181769957, 0.74355532106225719)], 'toptag': [(0.54106867495477318, 0.42463376487957738)], 'btag': [(0.075940226230036795, 0.95638779613291447)], 'beta_signal': [(0.68112168688682373, 0.088902280750787654)], 'jec': [(1.1883611311326503, 0.5285907478660874)], 'rate_vjets': [(-0.69620893373378101, 0.23142750022465985)], '__nll': [-32813.951594629631], 'lumi': [(-0.076355213658798202, 1.0057981737141126)], 'rate_qcd': [(0.18138025981738409, 0.50054733405116836)], 'rate_st': [(-0.6919734714632032, 0.84803113526866325)]}}
    ttbar_list = {'TTbar': {'jer': [(1.3237907302728831, 0.71405232496156001)], 'toptag': [(0.66176468123872256, 0.42991882487381328)], 'btag': [(0.11894463432246677, 0.9536720281241633)], 'beta_signal': [(0.65834529355408344, 0.086315506198508807)], 'jec': [(0.91153133162189148, 0.41887603820468949)], 'rate_vjets': [(-0.49356943431379674, 0.20552879582901146)], '__nll': [-35104.880097524896], 'lumi': [(-0.090686713508109751, 1.0078157651585835)], 'rate_qcd': [(-0.067849937137559255, 0.30193562283569275)], 'rate_st': [(-0.90890124365374503, 0.82973097866033951)]}}
    
### CT10 scaleup
if pdfname=="scaleup": 
    #    ttbar_list = {'TTbar': {'jer': [(1.1749990511414792, 0.70951877608903646)], 'toptag': [(-0.022171940537548909, 0.40782510471193084)], 'btag': [(-0.22694182110564304, 0.94414560037031481)], 'beta_signal': [(0.76802813853040819, 0.10887152161939173)], 'jec': [(0.79975281419491573, 0.40405124459401809)], 'rate_vjets': [(-0.63431521498066523, 0.20693611867951947)], '__nll': [-32822.795541606029], 'lumi': [(-0.097880234266536012, 1.0058116695518613)], 'rate_qcd': [(-0.24789683249649383, 0.62405983181233848)], 'rate_st': [(-0.66691350436846197, 0.85629053455313942)]}}
    ttbar_list = {'TTbar': {'jer': [(1.0080785710013995, 0.65529620543632683)], 'toptag': [(0.89262324881250721, 0.49167762022412803)], 'btag': [(-0.75210151306493755, 1.0023532854190274)], 'beta_signal': [(0.61664062729499913, 0.093906310019273964)], 'jec': [(0.48104095657692592, 0.45666321135782034)], 'rate_vjets': [(-0.27754430907826988, 0.21811131705478579)], '__nll': [-35112.452787982555], 'lumi': [(-0.066661243130817976, 1.0079287924970242)], 'rate_qcd': [(0.084785893936720078, 0.27824068695081566)], 'rate_st': [(-0.81352044962596859, 0.84107544890068253)]}}
    
### CT10 scaledown
if pdfname=="scaledown": 
    #    ttbar_list = {'TTbar': {'jer': [(0.99439571964408702, 0.66472726756040013)], 'toptag': [(0.9344652764792446, 0.40838263899966459)], 'btag': [(0.12849103897623868, 0.95293161222459155)], 'beta_signal': [(0.72749104262748654, 0.08687019148691133)], 'jec': [(0.79725663302899119, 0.37283707227988105)], 'rate_vjets': [(-0.54921717314293472, 0.19550504416315628)], '__nll': [-32811.12732859121], 'lumi': [(-0.06014002966935663, 1.0057513872571326)], 'rate_qcd': [(0.34656585147120078, 0.45538512397969333)], 'rate_st': [(-0.75220156031293106, 0.84551081793920335)]}}
    ttbar_list = {'TTbar': {'jer': [(0.84375194115480712, 0.59225808580414696)], 'toptag': [(1.7449621158260771, 0.44222424362800844)], 'btag': [(-0.37627513510485389, 0.98281783886542151)], 'beta_signal': [(0.61305008799363736, 0.07384717100024063)], 'jec': [(0.54745531187103991, 0.40309404969730783)], 'rate_vjets': [(-0.26152384659610772, 0.20119311876511989)], '__nll': [-35102.443796813335], 'lumi': [(-0.061705526826668883, 1.0079352844065472)], 'rate_qcd': [(0.24733812646832734, 0.22025668336698653)], 'rate_st': [(-0.86281125482974896, 0.83040678687066671)]}}

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


