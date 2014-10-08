from ROOT import *
from array import array

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
	if systematic is '__nll' or systematic is 'beta_signal' or systematic is '__cov':
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


