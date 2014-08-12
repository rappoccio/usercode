from ROOT import *

ttbar_list ={'TTbar': {'jer': [(1.2342191328419947, 0.7332580281852713)], 'scale': [(-0.90510367585246565, 0.2351704275758307)], 'toptag': [(0.26637372767240897, 0.42444059008426788)], 'btag': [(-0.21762775130959922, 0.96258702027805443)], 'rate_nonsemi': [(-0.29504515765628375, 0.93024289410176142)], 'beta_signal': [(0.71964974794636705, 0.13079477316713328)], 'pdf_CT10': [(1.0256718591825607, 0.62222833192039284)], 'jec': [(0.83840926267940474, 0.47239217499141795)], 'rate_vjets': [(-0.83886380136997141, 0.23407436694213674)], '__nll': [-32822.081213499223], 'lumi': [(-0.1302216969853946, 1.0053623124085842)], 'rate_qcd': [(-0.22913447743421822, 0.56351881705809892)], 'rate_st': [(-0.70675026896178317, 0.85180072374726723)]}}



signal_list = ttbar_list['TTbar']

nuisances = TGraphErrors()
gr1sig = TGraphErrors()
gr2sig = TGraphErrors()

nPoint = -1
for systematic in sorted(signal_list.keys()):

	if systematic is '__nll' or systematic is "beta_signal":
		continue

	nPoint += 1

	print systematic, signal_list[systematic][0][0], signal_list[systematic][0][1]


	nuisances.SetPoint(nPoint, signal_list[systematic][0][0], nPoint+0.5)
	nuisances.SetPointError(nPoint, signal_list[systematic][0][1], 0)

	gr1sig.SetPoint(nPoint, 0, nPoint)
	gr1sig.SetPointError(nPoint, 1, 1)
	
	gr2sig.SetPoint(nPoint, 0, nPoint)
	gr2sig.SetPointError(nPoint, 2, 1)
	





c1 = TCanvas("c1", "c1", 600, 800)
c1.Draw()
c1.SetLeftMargin(0.15)

gr2sig.SetLineWidth(0)
gr1sig.SetLineWidth(0)
gr2sig.SetLineColor(kYellow)
gr1sig.SetLineColor(kGreen)
gr2sig.SetFillStyle(1001)
gr2sig.SetFillColor(kYellow)

gr2sig.Draw("A5")
gr2sig.GetYaxis().Set(nPoint+1, 0, nPoint+1)
gr2sig.GetXaxis().Set(10,-4.5,4.5)

nBin = 0
for systematic in sorted(signal_list.keys()):
	if systematic is '__nll' or systematic is 'beta_signal':
		continue
	gr2sig.GetYaxis().SetBinLabel(nBin+1, systematic)
	nBin += 1

gr2sig.GetXaxis().SetTitle("Post-Fit Nuisance Parameter Value (#sigma)")
gr2sig.GetYaxis().SetTitle("Nuisance Parameter")
gr2sig.GetYaxis().SetTitleOffset(3)

gr1sig.SetFillStyle(1001)
gr1sig.SetFillColor(kGreen)
gr1sig.Draw("5 same")

nuisances.SetMarkerStyle(21)
nuisances.Draw("P same")
gPad.RedrawAxis()

label = TLatex()
label.SetNDC(1)

c1.Print("nuisances.pdf")
c1.Print("nuisances.png")


