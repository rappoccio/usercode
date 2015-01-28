#include "makeHists.h"

#include "TStyle.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TLatex.h"
#include "THStack.h"

#include <iostream>


void setStyle() {

  gStyle->SetOptTitle(0);
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(0);
  gStyle->SetOptStat(000000);
  
  gStyle->SetTitleFont(43);
  gStyle->SetTitleFont(43, "XYZ");
  gStyle->SetTitleSize(30, "XYZ");
  gStyle->SetTitleOffset(2.0, "X");
  gStyle->SetTitleOffset(1.25, "Y");
  gStyle->SetLabelFont(43, "XYZ");
  gStyle->SetLabelSize(20, "XYZ");

}

void myText(Double_t x,Double_t y,Color_t color,char const *text) {
  TLatex l;
  l.SetTextSize(0.05); 
  l.SetTextFont(42); 
  l.SetNDC();
  l.SetTextColor(color);
  l.DrawLatex(x,y,text);
}
void mySmallText(Double_t x,Double_t y,Color_t color,char const *text) {
  TLatex l;
  l.SetTextSize(0.042); 
  l.SetTextFont(42); 
  l.SetNDC();
  l.SetTextColor(color);
  l.DrawLatex(x,y,text);
}


// -------------------------------------------------------------------------------------
// make pretty plots
// -------------------------------------------------------------------------------------

void makePlots(TString var, int cut, int cut2=0, bool doElectron=false, TString pdfdir="CT10_nom") {


  TString syst = "nom";


  TH1::AddDirectory(kFALSE); 
  setStyle();

  if ( !((cut==4 && cut2==6) || (cut==6 && cut2==7) || (cut==7 && cut2==0))) { 
    std::cout << "Not a valid option! Syntax is: " << std::endl
	      << "> makePlots(TString var, int cut, int cut2)" << std::endl
	      << "where (cut, cut2) = (4,6) or (6,7) or (7,0). Exiting..." << std::endl;
    return;
  }
 
  TString hist = var;
  hist += cut;
  TString hist2 = var;
  hist2 += cut2;

  // read QCD normalization
  std::pair<double, double> qcdnorm = getQCDnorm(cut, doElectron);
  double nqcd = qcdnorm.first;
  double err_qcd = qcdnorm.second; 
  
  // get histograms
  SummedHist* wjets = getWJets( syst, hist, doElectron  );
  SummedHist* singletop = getSingleTop( syst, hist, doElectron  );
  SummedHist* ttbar = getTTbar( syst, hist, doElectron, pdfdir  );
  SummedHist* ttbar_nonSemiLep = getTTbarNonSemiLep( syst, hist, doElectron, pdfdir  );
  SummedHist* qcd = getQCD( hist, doElectron );
  
  SummedHist* wjets2;
  SummedHist* singletop2;
  SummedHist* ttbar2;
  SummedHist* ttbar_nonSemiLep2;
  SummedHist* qcd2;
  if (cut2>0) {
    wjets2 = getWJets( syst, hist2, doElectron  );
    singletop2 = getSingleTop( syst, hist2, doElectron  );
    ttbar2 = getTTbar( syst, hist2, doElectron, pdfdir  );
    ttbar_nonSemiLep2 = getTTbarNonSemiLep( syst, hist2, doElectron, pdfdir  );
    qcd2 = getQCD( hist2, doElectron );
  }

  TString filepath;
  if (use2D && doElectron) filepath = "histfiles/2Dhist_el/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
  else if (use2D) filepath = "histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  else filepath = "histfiles/SingleMu_iheartNY_V1_mu_Run2012_nom.root";

  TFile* dataFile = TFile::Open(filepath);
  TH1F* h_data = (TH1F*) dataFile->Get( hist );
  h_data->SetName(hist + "__DATA");

  TH1F* h_data2;
  if (cut2>0) {
    h_data2 = (TH1F*) dataFile->Get( hist2 );
    h_data2->SetName(hist + "__DATA_2");
  } 
 

  // -------------------------------------------------------------------------------------
  // do the subtraction ?
  if (cut2>0) {
    wjets->hist() ->Add(wjets2->hist(), -1);
    singletop->hist() ->Add(singletop2->hist(), -1);
    ttbar->hist() ->Add(ttbar2->hist(), -1);
    ttbar_nonSemiLep->hist() ->Add(ttbar_nonSemiLep2->hist(), -1);
    qcd->hist() ->Add(qcd2->hist(), -1);
    h_data->Add(h_data2, -1);
  }

  // -------------------------------------------------------------------------------------
  // get the TH1F versions

  TH1F* h_qcd = (TH1F*) qcd->hist();
  TH1F* h_wjets = (TH1F*) wjets->hist();
  TH1F* h_ttbar = (TH1F*) ttbar->hist();
  TH1F* h_ttbar_nonSemiLep = (TH1F*) ttbar_nonSemiLep->hist();
  TH1F* h_singletop = (TH1F*) singletop->hist();

  // ------------------------------------------------------------------------------------
  // Normalize the QCD histogram
  h_qcd->Scale(nqcd / h_qcd->GetSum());

  // -------------------------------------------------------------------------------------
  // various hist plotting edits

  // rebinning
  float rebin = 1;
  TString newtitle;
  if (var=="etaLep"){
    rebin = 2;
    newtitle = "Muons / 0.2";
  }
  else if (var=="etaAbsLep"){
    rebin = 2;
    newtitle = "Muons / 0.1";
  }
  else if (hist=="hadtop_mass6" || hist=="hadtop_mass7" || hist=="leptop_mass4") {
    rebin = 2;
    newtitle = "Events / 10 GeV";
  }
  else if (hist=="leptop_mass6" || hist=="leptop_mass7") {
    rebin = 4;
    newtitle = "Events / 20 GeV";
  }
  else if (hist=="hadtop_pt4") {
    rebin = 2;
    newtitle = "Events / 10 GeV";
  }
  else if (hist=="hadtop_pt6" || hist=="hadtop_pt7" || var=="leptop_pt") {
    rebin = 4;
    newtitle = "Events / 20 GeV";
  }
  else if (hist=="hadtop_y6" || hist=="hadtop_y7" || hist=="leptop_y6" || hist=="leptop_y7") {
    rebin = 2;
    newtitle = "Events / 0.2";
  }
  else if (var=="ht") {
    rebin = 5;
    newtitle = "Events / 50 GeV";
  }
  else if (var=="lepMET") {
    rebin = 10;
    newtitle = "Events / 40 GeV";
  }
  else if (var=="ptLep") {
    rebin = 2;
    newtitle = "Muons / 10 GeV";
  }
  else if (hist=="ptMET4") {
    rebin = 5;
    newtitle = "Events / 10 GeV";
  }
  else if (hist=="ptMET6" || hist=="ptMET7") {
    rebin = 10;
    newtitle = "Events / 20 GeV";
  }
  else if (hist=="vtxMass7") {
    rebin = 2;
    newtitle = "Events / 0.2 GeV";
  }
  else if (var.Contains("wboson_")) {
    rebin = 3;
    newtitle = "Events / 30 GeV";
  }

  if (rebin > 0) {
    h_data->Rebin(rebin);
    h_data->GetYaxis()->SetTitle(newtitle);
    h_qcd->Rebin(rebin);
    h_ttbar->Rebin(rebin);
    h_ttbar_nonSemiLep->Rebin(rebin);
    h_singletop->Rebin(rebin);
    h_wjets->Rebin(rebin);
  }


  h_data->SetLineWidth(1);
  h_data->SetMarkerStyle(20);

  // axis ranges
  if (var=="csv1LepJet" || var=="csv2LepJet") h_data->SetAxisRange(0,1.05,"X");
  if (hist=="hadtop_mass3" || hist=="hadtop_mass4") h_data->SetAxisRange(0,250,"X");
  if (hist=="hadtop_pt3") h_data->SetAxisRange(150,700,"X");
  if (hist=="hadtop_pt4") h_data->SetAxisRange(350,900,"X");
  if (hist=="hadtop_pt6" || hist=="hadtop_pt7") h_data->SetAxisRange(350,1200,"X");
  if (var=="hadtop_y" || var=="leptop_y") h_data->SetAxisRange(-3,3,"X");
  if (hist=="ht3" || hist=="htLep3") h_data->SetAxisRange(0,1400,"X");
  if ( (var=="ht" || var=="htLep") && (cut==4||cut==6||cut==7) ) h_data->SetAxisRange(0,2500,"X");
  if (hist=="pt1LepJet2") h_data->SetAxisRange(0,250,"X");
  if (hist=="ptLep0" || hist=="ptLep1" || hist=="ptLep2") h_data->SetAxisRange(0,200,"X");
  if (hist=="ptMET0" || hist=="ptMET1" || hist=="ptMET2") h_data->SetAxisRange(0,200,"X");

  if (var=="etaAbsLep") h_data->GetXaxis()->SetTitle("Muon |#eta|");

  // legend
  TLegend* leg;
  if (var.Contains("csv")) leg = new TLegend(0.59,0.56,0.84,0.9);
  else leg = new TLegend(0.67,0.56,0.92,0.9);
  leg->SetBorderSize(0);
  leg->SetFillStyle(0);
  leg->SetTextFont(42);
  leg->SetTextSize(0.05);
  leg->AddEntry(h_data, "Data", "pel");
  leg->AddEntry(h_ttbar, "t#bar{t} Signal", "f");
  leg->AddEntry(h_ttbar_nonSemiLep, "t#bar{t} Other", "f");
  leg->AddEntry(h_singletop, "Single Top", "f");
  leg->AddEntry(h_wjets, "W #rightarrow #mu#nu", "f");
  leg->AddEntry(h_qcd, "QCD" , "f");


  // create stack & summed histogram for ratio plot
  THStack* h_stack = new THStack();    
  h_stack->Add(h_qcd);
  h_stack->Add(h_wjets);
  h_stack->Add(h_singletop);
  h_stack->Add(h_ttbar_nonSemiLep);
  h_stack->Add(h_ttbar);

  TH1F* h_totalbkg = (TH1F*) h_qcd->Clone("totalbkg_"+hist); 
  h_totalbkg->Add(h_ttbar);
  h_totalbkg->Add(h_ttbar_nonSemiLep);
  h_totalbkg->Add(h_wjets);
  h_totalbkg->Add(h_singletop);

  TH1F* h_ratio = (TH1F*) h_data->Clone("ratio_"+hist);
  h_ratio->Sumw2();
  h_ratio->Divide(h_totalbkg);

  // automatically set y-range
  float max = h_totalbkg->GetMaximum();
  if ( (h_data->GetMaximum() + h_data->GetBinError(h_data->GetMaximumBin())) > max)
    max = (h_data->GetMaximum() + h_data->GetBinError(h_data->GetMaximumBin()));
  if (var.Contains("etaAbs") || var=="lepMET" || var=="leptop_mass") 
    max = max*1.2;
  else if (var.Contains("eta") || var.Contains("_y") || var.Contains("wboson_"))
    max = max*1.4;
  h_data->SetAxisRange(0,max*1.05,"Y");


  // -------------------------------------------------------------------------------------
  // plotting!

  TCanvas* c = new TCanvas("c_"+hist,"c_"+hist,200,10,900,800);
  TPad* p1 = new TPad("datamcp1_"+hist,"datamcp1_"+hist,0.0,0.3,1.0,0.97);
  p1->SetTopMargin(0.05);
  p1->SetBottomMargin(0.05);
  p1->SetNumber(1);
  TPad* p2 = new TPad("datamcp2_"+hist,"datamcp2_"+hist,0.0,0.00,1.0,0.3);
  p2->SetNumber(2);
  p2->SetTopMargin(0.05);
  p2->SetBottomMargin(0.40);

  c->cd();
  p1->Draw();
  p1->cd();


  h_data->UseCurrentStyle();
  h_data->GetXaxis()->SetLabelSize(24);
  h_data->GetYaxis()->SetLabelSize(24);
  h_data->Draw("lep");
  h_stack->Draw("hist,same");
  h_data->Draw("lep,same");
  h_data->Draw("lep,same,axis");

  leg->Draw();

  if (var.Contains("csv")) {
    myText(0.40,0.81,1,"#intLdt = 19.7 fb^{-1}");
    myText(0.40,0.72,1,"#sqrt{s} = 8 TeV");
  }
  else {
    myText(0.48,0.81,1,"#intLdt = 19.7 fb^{-1}");
    myText(0.48,0.72,1,"#sqrt{s} = 8 TeV");
  }


  // plot ratio part
  c->cd();
  p2->Draw();
  p2->cd();
  p2->SetGridy();
  h_ratio->UseCurrentStyle();
  h_ratio->Draw("lep");
  h_ratio->SetMaximum(2.0);
  h_ratio->SetMinimum(0.0);
  h_ratio->GetYaxis()->SetNdivisions(2,4,0,false);
  h_ratio->GetYaxis()->SetTitle("Data/MC");
  h_ratio->GetXaxis()->SetTitle(h_data->GetXaxis()->GetTitle());
  h_ratio->GetXaxis()->SetTitleOffset( 4.0 );
  h_ratio->GetXaxis()->SetLabelSize(24);
  h_ratio->GetYaxis()->SetLabelSize(24);

  // save output
  TString outname;
  if (use2D && doElectron) outname = "Plots/el_"+pdfdir+"_";
  else if (use2D) outname = "Plots/mu_"+pdfdir+"_";
  else outname = "Plots/mu_relIso_"+pdfdir+"_";

  if (cut2==0) {
    c->SaveAs(outname+hist+"_prefit.png");
    c->SaveAs(outname+hist+"_prefit.pdf");
  }
  else {
    c->SaveAs(outname+hist2+"_subtracted_from_"+hist+"_prefit.png");
    c->SaveAs(outname+hist2+"_subtracted_from_"+hist+"_prefit.pdf");
  }


  // -------------------------------------------------------------------------------------
  // finally print event counts!

  float err_tt = 0;
  float err_tt_nonsemilep = 0;
  float err_singletop = 0;
  float err_wjets = 0;

  for (int ib=0; ib<h_ttbar->GetNbinsX(); ib++) {
    err_tt += h_ttbar->GetBinError(ib+1)*h_ttbar->GetBinError(ib+1);
    err_tt_nonsemilep += h_ttbar_nonSemiLep->GetBinError(ib+1)*h_ttbar_nonSemiLep->GetBinError(ib+1);
    err_singletop += h_singletop->GetBinError(ib+1)*h_singletop->GetBinError(ib+1);
    err_wjets += h_wjets->GetBinError(ib+1)*h_wjets->GetBinError(ib+1);
  }

  err_tt = sqrt(err_tt);
  err_tt_nonsemilep = sqrt(err_tt_nonsemilep);
  err_singletop = sqrt(err_singletop);
  err_wjets = sqrt(err_wjets);

  float err_tot = err_tt*err_tt + err_tt_nonsemilep*err_tt_nonsemilep + err_singletop*err_singletop + err_wjets*err_wjets + err_qcd*err_qcd;
  err_tot = sqrt(err_tot);

  float err_tot_dn = err_tot;
  float err_qcd_dn = err_qcd;
  if (cut==7) { //manual fix for down QCD error
    if (nqcd < err_qcd) {err_qcd_dn = nqcd;}
    err_tot_dn = err_tt*err_tt + err_tt_nonsemilep*err_tt_nonsemilep + err_singletop*err_singletop + err_wjets*err_wjets + err_qcd_dn*err_qcd_dn;
    err_tot_dn = sqrt(err_tot_dn);
  }


  std::cout << std::endl << "-------------------------------------------------------------------------------------" << std::endl;
  if (doElectron) std::cout << "*** electron+jets channel *** " << std::endl;
  else std::cout << "*** muon+jets channel *** " << std::endl;
  std::cout << "PDF: " << pdfdir << std::endl;
  if (cut2==0) std::cout << "hist: " << hist << std::endl;
  else std::cout << "hist: " << hist2 << "_subtracted_from_" << hist << std::endl;
  std::cout << "-------------------------------------------------------------------------------------" << std::endl;
  std::cout << "QCD        = " << h_qcd->GetSum() << " + " << err_qcd << " / - " << err_qcd_dn << std::endl;
  std::cout << "ttbar      = " << h_ttbar->GetSum() << " +/- " << err_tt << std::endl;
  std::cout << "ttbar (non-semilep) = " << h_ttbar_nonSemiLep->GetSum() << " +/- " << err_tt_nonsemilep << std::endl;
  std::cout << "single top = " << h_singletop->GetSum() << " +/- " << err_singletop << std::endl;
  std::cout << "W+jets     = " << h_wjets->GetSum() << " +/- " << err_wjets << std::endl;
  std::cout << "total background = " << h_totalbkg->GetSum() << " + " << err_tot << " / - " << err_tot_dn << std::endl << std::endl;
  std::cout << "data = " << h_data->GetSum() << std::endl << std::endl;
  std::cout << "(bkg - data)/data = " << (h_totalbkg->GetSum()-h_data->GetSum())/h_data->GetSum()*100.0 << " % " << std::endl;
  std::cout << "-------------------------------------------------------------------------------------" << std::endl << std::endl;


}



// -------------------------------------------------------------------------------------
// make post-fit plots
// -------------------------------------------------------------------------------------

void makePosteriorPlots(TString what, bool doElectron=false, TString pdfdir="CT10_nom") {

  TH1::AddDirectory(kFALSE); 
  setStyle();


  // read MC histograms
  TFile* fMC;
  if (doElectron) fMC = new TFile("run_theta/histos-el-mle-2d-"+pdfdir+".root");
  else fMC = new TFile("run_theta/histos-mle-2d-"+pdfdir+".root");

  TH1F* h_qcd = (TH1F*) fMC->Get(what+"__QCD");
  TH1F* h_wjets = (TH1F*) fMC->Get(what+"__WJets");
  TH1F* h_ttbar = (TH1F*) fMC->Get(what+"__TTbar");
  TH1F* h_singletop = (TH1F*) fMC->Get(what+"__SingleTop");

  // Construct post-fit ttbar
  // Get pre-fit plots needed
  TFile* fPre;
  TH1F* h_pre_ttbar;
  TH1F* h_pre_ttbar_nonSemiLep;
  if (what == "etaAbsLep4") {
    if (doElectron) fPre = TFile::Open("NormalizedHists_"+pdfdir+"/normalized2d_mujets_etaAbsLep6_subtracted_from_etaAbsLep4.root");
    else fPre = TFile::Open("NormalizedHists_"+pdfdir+"/normalized2d_eljets_etaAbsLep6_subtracted_from_etaAbsLep4.root");
    h_pre_ttbar = (TH1F*) fPre->Get(what+"__TTbar");
    h_pre_ttbar_nonSemiLep = (TH1F*) fPre->Get(what+"__TTbar_nonSemiLep");
  }
  if (what == "etaAbsLep6") {
    if (doElectron) fPre = TFile::Open("NormalizedHists_"+pdfdir+"/normalized2d_eljets_etaAbsLep7_subtracted_from_etaAbsLep6.root");
    else fPre = TFile::Open("NormalizedHists_"+pdfdir+"/normalized2d_mujets_etaAbsLep7_subtracted_from_etaAbsLep6.root");
    h_pre_ttbar = (TH1F*) fPre->Get(what+"__TTbar");
    h_pre_ttbar_nonSemiLep = (TH1F*) fPre->Get(what+"__TTbar_nonSemiLep");
  }
  if (what == "vtxMass7") {
    if (doElectron) fPre = TFile::Open("NormalizedHists_"+pdfdir+"/normalized2d_eljets_vtxMass7.root");
    else fPre = TFile::Open("NormalizedHists_"+pdfdir+"/normalized2d_mujets_vtxMass7.root");
    h_pre_ttbar = (TH1F*) fPre->Get(what+"__TTbar");
    h_pre_ttbar_nonSemiLep = (TH1F*) fPre->Get(what+"__TTbar_nonSemiLep");
  }

  float postPreRatio = h_ttbar->Integral() / h_pre_ttbar->Integral();
  // post-fit nonSemiLep is pre-fit nonSemiLep scaled by post/pre fit ratio
  TH1F* h_ttbar_nonSemiLep = (TH1F*) h_pre_ttbar_nonSemiLep->Clone();
  h_ttbar_nonSemiLep->Scale(postPreRatio);
  // post-fit semiLep is post-fit total with post-fit nonSemiLep subtracted
  TH1F* h_ttbar_semiLep = (TH1F*) h_ttbar->Clone();
  h_ttbar_semiLep->Add(h_ttbar_nonSemiLep, -1);

  // read data histogram 
  TString filepath;
  if (use2D && doElectron) filepath = "histfiles/2Dhist_el/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
  else if (use2D) filepath = "histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  else filepath = "histfiles/SingleMu_iheartNY_V1_mu_Run2012_nom.root";

  TFile* dataFile = TFile::Open(filepath);
  TH1F* h_data = (TH1F*) dataFile->Get( what );
  h_data->SetName(what + "__DATA");

  if (what=="etaAbsLep4") {
    TH1F* h_data2 = (TH1F*) dataFile->Get("etaAbsLep6");
    h_data->Add(h_data2,-1);
  }
  else if (what=="etaAbsLep6") {
    TH1F* h_data2 = (TH1F*) dataFile->Get("etaAbsLep7");
    h_data->Add(h_data2,-1);
  }


  // -------------------------------------------------------------------------------------
  // various hist plotting edits

  h_qcd->SetFillColor(kYellow);
  h_wjets->SetFillColor(kGreen-3);
  h_singletop->SetFillColor(6);
  h_ttbar_semiLep->SetFillColor(kRed+1);
  h_ttbar_nonSemiLep->SetFillColor(kRed-7);

  h_qcd->SetLineColor(1);
  h_wjets->SetLineColor(1);
  h_singletop->SetLineColor(1);
  h_ttbar_semiLep->SetLineColor(1);
  h_ttbar_nonSemiLep->SetLineColor(1);


  // rebinning
  float rebin = 1;
  TString newtitle;
  if (what.Contains("etaAbsLep")) {
    rebin = 2;
    newtitle = "Muons / 0.1";
  }
  else if (what=="hadtop_pt6" || what=="hadtop_pt7") {
    rebin = 4;
    newtitle = "Events / 20 GeV";
  }
  else if (what=="vtxMass7") {
    rebin = 2;
    newtitle = "Events / 0.2 GeV";
  }

  if (rebin > 0) {
    h_data->Rebin(rebin);
    h_data->GetYaxis()->SetTitle(newtitle);
    h_qcd->Rebin(rebin);
    h_ttbar_semiLep->Rebin(rebin);
    h_ttbar_nonSemiLep->Rebin(rebin);
    h_singletop->Rebin(rebin);
    h_wjets->Rebin(rebin);
  }


  h_data->SetLineWidth(1);
  h_data->SetMarkerStyle(20);

  // axis ranges
  if (what=="hadtop_pt6" || what=="hadtop_pt7") h_data->SetAxisRange(350,1200,"X");
  if (what.Contains("etaAbsLep")) h_data->GetXaxis()->SetTitle("Muon |#eta|");

  // legend
  TLegend* leg = new TLegend(0.67,0.56,0.92,0.9);
  leg->SetBorderSize(0);
  leg->SetFillStyle(0);
  leg->SetTextFont(42);
  leg->SetTextSize(0.05);
  leg->AddEntry(h_data, "Data", "pel");
  leg->AddEntry(h_ttbar_semiLep, "t#bar{t} Signal", "f");
  leg->AddEntry(h_ttbar_nonSemiLep, "t#bar{t} Other", "f");
  leg->AddEntry(h_singletop, "Single Top", "f");
  leg->AddEntry(h_wjets, "W #rightarrow #mu#nu", "f");
  leg->AddEntry(h_qcd, "QCD" , "f");


  // create stack & summed histogram for ratio plot
  THStack* h_stack = new THStack();    
  h_stack->Add(h_qcd);
  h_stack->Add(h_wjets);
  h_stack->Add(h_singletop);
  h_stack->Add(h_ttbar_nonSemiLep);
  h_stack->Add(h_ttbar_semiLep);

  TH1F* h_totalbkg = (TH1F*) h_qcd->Clone("totalbkg_"+what); 
  h_totalbkg->Add(h_ttbar_semiLep);
  h_totalbkg->Add(h_ttbar_nonSemiLep);
  h_totalbkg->Add(h_wjets);
  h_totalbkg->Add(h_singletop);

  TH1F* h_ratio = (TH1F*) h_data->Clone("ratio_"+what);
  h_ratio->Sumw2();
  h_ratio->Divide(h_totalbkg);

  // automatically set y-range
  float max = h_totalbkg->GetMaximum();
  if ( (h_data->GetMaximum() + h_data->GetBinError(h_data->GetMaximumBin())) > max)
    max = (h_data->GetMaximum() + h_data->GetBinError(h_data->GetMaximumBin()));
  if (what.Contains("etaAbs")) max = max*1.2;
  h_data->SetAxisRange(0,max*1.05,"Y");


  // -------------------------------------------------------------------------------------
  // plotting!

  TCanvas* c = new TCanvas("c_"+what,"c_"+what,200,10,900,800);
  TPad* p1 = new TPad("datamcp1_"+what,"datamcp1_"+what,0.0,0.3,1.0,0.97);
  p1->SetTopMargin(0.05);
  p1->SetBottomMargin(0.05);
  p1->SetNumber(1);
  TPad* p2 = new TPad("datamcp2_"+what,"datamcp2_"+what,0.0,0.00,1.0,0.3);
  p2->SetNumber(2);
  p2->SetTopMargin(0.05);
  p2->SetBottomMargin(0.40);

  c->cd();
  p1->Draw();
  p1->cd();


  h_data->UseCurrentStyle();
  h_data->GetXaxis()->SetLabelSize(24);
  h_data->GetYaxis()->SetLabelSize(24);
  h_data->Draw("lep");
  h_stack->Draw("hist,same");
  h_data->Draw("lep,same");
  h_data->Draw("lep,same,axis");

  leg->Draw();

  //mySmallText(0.14,0.96,1,"Posterior fit distributions");
  //myText(0.48,0.81,1,"#intLdt = 19.7 fb^{-1}");
  //myText(0.48,0.72,1,"#sqrt{s} = 8 TeV");
  
  myText(0.45,0.86,1,"CMS Preliminary");
  myText(0.45,0.75,1,"#intLdt = 19.7 fb^{-1}");
  myText(0.45,0.66,1,"#sqrt{s} = 8 TeV");

  // plot ratio part
  c->cd();
  p2->Draw();
  p2->cd();
  p2->SetGridy();
  h_ratio->UseCurrentStyle();
  h_ratio->Draw("lep");
  h_ratio->SetMaximum(2.0);
  h_ratio->SetMinimum(0.0);
  h_ratio->GetYaxis()->SetNdivisions(2,4,0,false);
  h_ratio->GetYaxis()->SetTitle("Data/MC");
  h_ratio->GetXaxis()->SetTitle(h_data->GetXaxis()->GetTitle());
  h_ratio->GetXaxis()->SetTitleOffset( 4.0 );
  h_ratio->GetXaxis()->SetLabelSize(24);
  h_ratio->GetYaxis()->SetLabelSize(24);

  // save output
  TString outname;
  if (use2D && doElectron) outname = "Plots/el_"+pdfdir+"_";
  else if (use2D) outname = "Plots/mu_"+pdfdir+"_";
  else outname = "Plots/mu_relIso_"+pdfdir+"_";

  c->SaveAs(outname+what+"_postfit.png");
  c->SaveAs(outname+what+"_postfit.pdf");

}

// -------------------------------------------------------------------------------------
// print post-fit latex table
// -------------------------------------------------------------------------------------

void makeTable(bool doElectron=false, TString pdfdir="CT10_nom") {

  TString what[3] = {"etaAbsLep4","etaAbsLep6","vtxMass7"};

  // post-fit file
  TFile* fMC;
  if (doElectron) fMC = new TFile("run_theta/histos-el-mle-2d-"+pdfdir+".root");
  else fMC = new TFile("run_theta/histos-mle-2d-"+pdfdir+".root");

  // post-fit relative errors (from theta_output.txt)
  float fiterr_tt = 0.10/0.72;
  float fiterr_singletop = (0.5*0.86)/(1.0-0.5*0.66);
  float fiterr_wjets = (0.5*0.21)/(1.0-0.5*0.7);
  float fiterr_qcd = (0.5*0.57)/(1.0-0.5*0.1);

  // pre-fit & data files
  TFile* fDATA[3];
  if (doElectron) {
    fDATA[0] = new TFile("NormalizedHists_"+pdfdir+"/normalized2d_mujets_etaAbsLep6_subtracted_from_etaAbsLep4.root");
    fDATA[1] = new TFile("NormalizedHists_"+pdfdir+"/normalized2d_mujets_etaAbsLep7_subtracted_from_etaAbsLep6.root");
    fDATA[2] = new TFile("NormalizedHists_"+pdfdir+"/normalized2d_mujets_vtxMass7.root");
  }
  else {
    fDATA[0] = new TFile("NormalizedHists_"+pdfdir+"/normalized2d_eljets_etaAbsLep6_subtracted_from_etaAbsLep4.root");
    fDATA[1] = new TFile("NormalizedHists_"+pdfdir+"/normalized2d_eljets_etaAbsLep7_subtracted_from_etaAbsLep6.root");
    fDATA[2] = new TFile("NormalizedHists_"+pdfdir+"/normalized2d_eljets_vtxMass7.root");
  }

  TH1F* h_pre_qcd[3];
  TH1F* h_pre_wjets[3];
  TH1F* h_pre_ttbar[3];
  TH1F* h_pre_ttbar_semiLep[3];
  TH1F* h_pre_ttbar_nonSemiLep[3];
  TH1F* h_pre_singletop[3];
  TH1F* h_pre_total[3];

  TH1F* h_qcd[3];
  TH1F* h_wjets[3];
  TH1F* h_ttbar[3];
  TH1F* h_ttbar_semiLep[3];
  TH1F* h_ttbar_nonSemiLep[3];
  TH1F* h_singletop[3];
  TH1F* h_total[3];

  TH1F* h_data[3];

  // errors for pre-fit table
  float err_tt_semiLep[3] = {0};
  float err_tt_nonsemilep[3] = {0};
  float err_singletop[3] = {0};
  float err_wjets[3] = {0};
  float err_tot_up[3] = {0};
  float err_tot_dn[3] = {0};


  // read QCD error
  std::pair<double, double> qcdnorm4 = getQCDnorm(4, doElectron);
  std::pair<double, double> qcdnorm6 = getQCDnorm(6, doElectron);
  std::pair<double, double> qcdnorm7 = getQCDnorm(7, doElectron);
  double err_qcd_up[3];
  double err_qcd_dn[3];
  err_qcd_up[0] = qcdnorm4.second; 
  err_qcd_dn[0] = err_qcd_up[0];
  err_qcd_up[1] = qcdnorm6.second; 
  err_qcd_dn[1] = err_qcd_up[1];
  err_qcd_up[2] = qcdnorm7.second; 
  err_qcd_dn[2] = qcdnorm7.first;
  

  // get histograms
  for (int i=0; i<3; i++) {

    // post-fit values
    h_qcd[i]   = (TH1F*) fMC->Get(what[i]+"__QCD");
    h_wjets[i] = (TH1F*) fMC->Get(what[i]+"__WJets");
    h_ttbar[i] = (TH1F*) fMC->Get(what[i]+"__TTbar");
    h_singletop[i] = (TH1F*) fMC->Get(what[i]+"__SingleTop");

    // data
    h_data[i] = (TH1F*) fDATA[i]->Get(what[i]+"__DATA");

    //pre-fit values
    h_pre_qcd[i]   = (TH1F*) fDATA[i]->Get(what[i]+"__QCD");
    h_pre_wjets[i] = (TH1F*) fDATA[i]->Get(what[i]+"__WJets");
    h_pre_ttbar[i] = (TH1F*) fDATA[i]->Get(what[i]+"__TTbar");
    h_pre_ttbar_semiLep[i] = (TH1F*) fDATA[i]->Get(what[i]+"__TTbar_semiLep");
    h_pre_ttbar_nonSemiLep[i] = (TH1F*) fDATA[i]->Get(what[i]+"__TTbar_nonSemiLep");
    h_pre_singletop[i] = (TH1F*) fDATA[i]->Get(what[i]+"__SingleTop");

    //Construct post-fit ttbar
    float postPreRatio = h_ttbar[i]->Integral() / h_pre_ttbar[i]->Integral();
    // post-fit nonSemiLep is pre-fit nonSemiLep scaled by post/pre fit ratio
    h_ttbar_nonSemiLep[i] = (TH1F*) h_pre_ttbar_nonSemiLep[i]->Clone();
    h_ttbar_nonSemiLep[i]->Scale(postPreRatio);
    // post-fit semiLep is post-fit total with post-fit nonSemiLep subtracted
    h_ttbar_semiLep[i] = (TH1F*) h_ttbar[i]->Clone();
    h_ttbar_semiLep[i]->Add(h_ttbar_nonSemiLep[i], -1);

    h_total[i] = (TH1F*) h_qcd[i]->Clone(what[i]+"_total");
    h_total[i]->Add(h_wjets[i]);
    h_total[i]->Add(h_ttbar[i]);
    h_total[i]->Add(h_singletop[i]);

    h_pre_total[i] = (TH1F*) h_pre_qcd[i]->Clone(what[i]+"_pre_total");
    h_pre_total[i]->Add(h_pre_wjets[i]);
    h_pre_total[i]->Add(h_pre_ttbar[i]);
    h_pre_total[i]->Add(h_pre_singletop[i]);

    // error on pre-fit counts
    for (int ib=0; ib<h_pre_ttbar[i]->GetNbinsX(); ib++) {
      err_tt_semiLep[i]    += h_pre_ttbar_semiLep[i]->GetBinError(ib+1)*h_pre_ttbar_semiLep[i]->GetBinError(ib+1);
      err_tt_nonsemilep[i] += h_pre_ttbar_nonSemiLep[i]->GetBinError(ib+1)*h_pre_ttbar_nonSemiLep[i]->GetBinError(ib+1);
      err_singletop[i]     += h_pre_singletop[i]->GetBinError(ib+1)*h_pre_singletop[i]->GetBinError(ib+1);
      err_wjets[i]         += h_pre_wjets[i]->GetBinError(ib+1)*h_pre_wjets[i]->GetBinError(ib+1);
    }

    err_tt_semiLep[i]    = sqrt(err_tt_semiLep[i]);
    err_tt_nonsemilep[i] = sqrt(err_tt_nonsemilep[i]);
    err_singletop[i]     = sqrt(err_singletop[i]);
    err_wjets[i]         = sqrt(err_wjets[i]);
    
    err_tot_up[i] = err_tt_semiLep[i]*err_tt_semiLep[i] + err_tt_nonsemilep[i]*err_tt_nonsemilep[i] + err_singletop[i]*err_singletop[i] + err_wjets[i]*err_wjets[i] + err_qcd_up[i]*err_qcd_up[i];
    err_tot_up[i] = sqrt(err_tot_up[i]);
    err_tot_dn[i] = err_tt_semiLep[i]*err_tt_semiLep[i] + err_tt_nonsemilep[i]*err_tt_nonsemilep[i] + err_singletop[i]*err_singletop[i] + err_wjets[i]*err_wjets[i] + err_qcd_dn[i]*err_qcd_dn[i];
    err_tot_dn[i] = sqrt(err_tot_dn[i]);
  }

  std::cout << std::endl << "--------------------------------------------------" << std::endl;
  if (doElectron) std::cout << "*** electron+jets channel ***" << std::endl;
  else std::cout << "*** muon+jets channel ***" << std::endl;
  std::cout << "PDF set: " << pdfdir << std::endl;
  std::cout << "---------------------------" << std::endl;
  std::cout << "Pre-fit results" << std::endl;
  std::cout << "---------------------------" << std::endl;
  std::cout << "\\ttbar (signal)      & " << h_pre_ttbar_semiLep[0]->Integral() << " $\\pm$ " << err_tt_semiLep[0] << " & " << 
    h_pre_ttbar_semiLep[1]->Integral() << " $\\pm$ " << err_tt_semiLep[1] << " & " << 
    h_pre_ttbar_semiLep[2]->Integral() << " $\\pm$ " << err_tt_semiLep[2] << " \\\\ " << std::endl;
  std::cout << "\\ttbar (non-semilep) & " << h_pre_ttbar_nonSemiLep[0]->Integral() << " $\\pm$ " << err_tt_nonsemilep[0] << " & " << 
    h_pre_ttbar_nonSemiLep[1]->Integral() << " $\\pm$ " << err_tt_nonsemilep[1] << " & " << 
    h_pre_ttbar_nonSemiLep[2]->Integral() << " $\\pm$ " << err_tt_nonsemilep[2] << " \\\\ " << std::endl;
  std::cout << "Single top           & " << h_pre_singletop[0]->Integral() << " $\\pm$ " << err_singletop[0] << " & " << 
    h_pre_singletop[1]->Integral() << " $\\pm$ " << err_singletop[1] << " & " << 
    h_pre_singletop[2]->Integral() << " $\\pm$ " << err_singletop[2] << " \\\\ " << std::endl;
  std::cout << "W+jets               & " << h_pre_wjets[0]->Integral() << " $\\pm$ " << err_wjets[0] << " & " << 
    h_pre_wjets[1]->Integral() << " $\\pm$ " << err_wjets[1] << " & " << 
    h_pre_wjets[2]->Integral() << " $\\pm$ " << err_wjets[2] << " \\\\ " << std::endl;
  std::cout << "QCD                  & " << h_pre_qcd[0]->Integral() << " $\\pm$ " << err_qcd_up[0] << " & " << 
    h_pre_qcd[1]->Integral() << " $\\pm$ " << err_qcd_up[1] << " & " << 
    h_pre_qcd[2]->Integral() << " $^{+" << err_qcd_up[2] << "}_{-" << err_qcd_dn[2] << "}$ \\\\ " << std::endl;
  std::cout << "\\hline" << std::endl;
  std::cout << "Total                & " << h_pre_total[0]->Integral() << " $\\pm$ " << err_tot_up[0] << " & " << 
    h_pre_total[1]->Integral() << " $\\pm$ " << err_tot_up[1] << " & " << 
    h_pre_total[2]->Integral() << " $^{+" << err_tot_up[2] << "}_{-" << err_tot_dn[2] << "}$ \\\\ " << std::endl;
  std::cout << "\\hline \\hline" << std::endl;
  std::cout << "Data                 & " << h_data[0]->Integral() << " & " << h_data[1]->Integral() << " & " << h_data[2]->Integral() << " \\\\ " << std::endl;

  std::cout << "---------------------------" << std::endl;
  std::cout << "Post-fit results" << std::endl;
  std::cout << "---------------------------" << std::endl;
  std::cout << "\\ttbar (signal)      & " << h_ttbar_semiLep[0]->Integral() << " $\\pm$ " << h_ttbar_semiLep[0]->Integral()*fiterr_tt
	    << " & " << h_ttbar_semiLep[1]->Integral() << " $\\pm$ " << h_ttbar_semiLep[1]->Integral()*fiterr_tt
	    << " & " << h_ttbar_semiLep[2]->Integral() << " $\\pm$ " << h_ttbar_semiLep[2]->Integral()*fiterr_tt << " \\\\ " << std::endl;
  std::cout << "\\ttbar (non-semilep) & " << h_ttbar_nonSemiLep[0]->Integral() << " $\\pm$ " << h_ttbar_nonSemiLep[0]->Integral()*fiterr_tt
	    << " & " << h_ttbar_nonSemiLep[1]->Integral() << " $\\pm$ " << h_ttbar_nonSemiLep[1]->Integral()*fiterr_tt
	    << " & " << h_ttbar_nonSemiLep[2]->Integral() << " $\\pm$ " << h_ttbar_nonSemiLep[2]->Integral()*fiterr_tt << " \\\\ " << std::endl;
  std::cout << "Single top           & " << h_singletop[0]->Integral() << " $\\pm$ " << h_singletop[0]->Integral()*fiterr_singletop
	    << " & " << h_singletop[1]->Integral() << " $\\pm$ " << h_singletop[1]->Integral()*fiterr_singletop
	    << " & " << h_singletop[2]->Integral() << " $\\pm$ " << h_singletop[2]->Integral()*fiterr_singletop << " \\\\ " << std::endl;
  std::cout << "W+jets               & " << h_wjets[0]->Integral() << " $\\pm$ " << h_wjets[0]->Integral()*fiterr_wjets
	    << " & " << h_wjets[1]->Integral() << " $\\pm$ " << h_wjets[1]->Integral()*fiterr_wjets
	    << " & " << h_wjets[2]->Integral() << " $\\pm$ " << h_wjets[2]->Integral()*fiterr_wjets << " \\\\ " << std::endl;
  std::cout << "QCD                  & " << h_qcd[0]->Integral() << " $\\pm$ " << h_qcd[0]->Integral()*fiterr_qcd
	    << " & " << h_qcd[1]->Integral() << " $\\pm$ " << h_qcd[1]->Integral()*fiterr_qcd
	    << " & " << h_qcd[2]->Integral() << " $\\pm$ " << h_qcd[2]->Integral()*fiterr_qcd << " \\\\ " << std::endl;
  std::cout << "\\hline" << std::endl;
  std::cout << "Total                & " << h_total[0]->Integral() << " & "  << h_total[1]->Integral() << " & "  << h_total[2]->Integral() << " \\\\ " << std::endl;
  std::cout << "\\hline \\hline" << std::endl;
  std::cout << "Data                 & " << h_data[0]->Integral() << " & " << h_data[1]->Integral() << " & " << h_data[2]->Integral() << " \\\\ " << std::endl;



}


// -------------------------------------------------------------------------------------
// make theta histograms without subtracting
// -------------------------------------------------------------------------------------

void makeTheta_single(TString var, int cut, bool doElectron=false, TString pdfdir="CT10_nom") {
  
  TH1::AddDirectory(kFALSE); 
  setStyle();

  if ( !(cut==7) ) {
    std::cout << "Not a valid option! Syntax is: " << std::endl
	      << "> makeTheta_single(TString var, int cut)" << std::endl
	      << "where cut == 7. Exiting..." << std::endl;
    return;
  }
 
  TString hist = var;
  hist += cut;


  // read QCD normalization
  std::pair<double, double> qcdnorm = getQCDnorm(cut, doElectron);
  double nqcd = qcdnorm.first;
  //double qcd_err = qcdnorm.second; 


  // systematics for ttbar, non-semilep ttbar, single top, W+jets
  const int nSYST = 9;
  TString name_syst[nSYST] = {"nom", "jecdn", "jecup", "jerdn", "jerup", 
			      "btagdn", "btagup", "toptagdn", "toptagup"};
  SummedHist* wjets[nSYST];
  SummedHist* singletop[nSYST];
  SummedHist* ttbar_semiLep[nSYST];
  SummedHist* ttbar_nonSemiLep[nSYST];
  TH1F* ttbar[nSYST];

  for (int is=0; is<nSYST; is++) {
    wjets[is]     = getWJets( name_syst[is], hist, doElectron );
    singletop[is] = getSingleTop( name_syst[is], hist, doElectron );
    ttbar_semiLep[is]     = getTTbar( name_syst[is], hist, doElectron, pdfdir );
    ttbar_nonSemiLep[is] = getTTbarNonSemiLep( name_syst[is], hist, doElectron, pdfdir );

    // do the ttbar combination
    ttbar[is] = (TH1F*) ttbar_semiLep[is]->hist()->Clone();
    ttbar[is]->Add(ttbar_nonSemiLep[is]->hist());
    TString tempname = hist + "__TTbar";
    adjustThetaName( tempname, name_syst[is] );
    ttbar[is]->SetName(tempname);
  }

  // QCD
  SummedHist* qcd = getQCD( hist, doElectron );
  

  // data
  TString filepath;
  if (use2D && doElectron) filepath = "histfiles/2Dhist_el/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
  else if (use2D) filepath = "histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  else filepath = "histfiles/SingleMu_iheartNY_V1_mu_Run2012_nom.root";

  TFile* dataFile = TFile::Open(filepath);
  TH1F* data = (TH1F*) dataFile->Get( hist );
  data->SetName(hist + "__DATA");
  


  // write the histograms to a file
  TString outname;
  if (use2D && doElectron) outname = "NormalizedHists_" + pdfdir + "/normalized2d_eljets_"+hist+".root";
  else if (use2D) outname = "NormalizedHists_" + pdfdir + "/normalized2d_mujets_"+hist+".root";
  else outname = "NormalizedHists_" + pdfdir + "/normalized_mujets_"+hist+".root";

  TFile* fout = new TFile(outname, "RECREATE");

  fout->cd();

  for (int is=0; is<nSYST; is++) {
    wjets[is]->hist()->Write();
    singletop[is]->hist()->Write();
    ttbar_semiLep[is]->hist()->Write();
    ttbar_nonSemiLep[is]->hist()->Write();
    ttbar[is]->Write();
  }

  TH1F* h_qcd = qcd->hist();
  h_qcd->Scale(nqcd / h_qcd->GetSum());
  h_qcd->Write();
  data->Write();

  fout->Close();

}


// -------------------------------------------------------------------------------------
// make histograms, subtract one from another
// -------------------------------------------------------------------------------------

void makeTheta_subtract(TString var, int cut1, int cut2, bool doElectron=false, TString pdfdir="_CT10_nom") {

  TH1::AddDirectory(kFALSE); 
  setStyle();

  if ( !((cut1==4 && cut2==6) || (cut1==6 && cut2==7)) ) {
    std::cout << "Not a valid option! Syntax is: " << std::endl
	      << "> makeTheta_subtract(TString var, int cut1, int cut2)" << std::endl
	      << "where (cut1, cut2) = (4,6) or (6,7). Exiting..." << std::endl;
    return;
  }
 
  TString hist[2] = {var, var};
  hist[0] += cut1;
  hist[1] += cut2;


  // read QCD normalization
  std::pair<double, double> qcdnorm = getQCDnorm(cut1, doElectron);
  double nqcd = qcdnorm.first;
  //double qcd_err = qcdnorm.second;

	
  // systematics for ttbar, non-semilep ttbar, single top, W+jets
  const int nSYST = 9;
  TString name_syst[nSYST] = {"nom", "jecdn", "jecup", "jerdn", "jerup", 
			      "btagdn", "btagup", "toptagdn", "toptagup"};

  
  SummedHist* wjets[nSYST][2];
  SummedHist* singletop[nSYST][2];
  SummedHist* ttbar_semiLep[nSYST][2];
  SummedHist* ttbar_nonSemiLep[nSYST][2];
  TH1F* ttbar[nSYST][2];

  for (int ih=0; ih<2; ih++) {
    for (int is=0; is<nSYST; is++) {
      wjets[is][ih]     = getWJets( name_syst[is], hist[ih], doElectron );
      singletop[is][ih] = getSingleTop( name_syst[is], hist[ih], doElectron );
      ttbar_semiLep[is][ih]     = getTTbar( name_syst[is], hist[ih], doElectron, pdfdir );
      ttbar_nonSemiLep[is][ih] = getTTbarNonSemiLep( name_syst[is], hist[ih], doElectron, pdfdir );

      ttbar[is][ih] = (TH1F*) ttbar_semiLep[is][ih]->hist()->Clone();
      ttbar[is][ih]->Add(ttbar_nonSemiLep[is][ih]->hist());
      TString tempname = hist[ih] + "__TTbar";
      adjustThetaName( tempname, name_syst[is] );
      ttbar[is][ih]->SetName(tempname);
    }
  }

  // QCD
  SummedHist* qcd[2];
  qcd[0] = getQCD( hist[0], doElectron );
  qcd[1] = getQCD( hist[1], doElectron );


  // data
  TString filepath;
  if (use2D && doElectron) filepath = "histfiles/2Dhist_el/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
  else if (use2D) filepath = "histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  else filepath = "histfiles/SingleMu_iheartNY_V1_mu_Run2012_nom.root";

  TFile* dataFile = TFile::Open(filepath);

  TH1F* data[2];
  data[0] = (TH1F*) dataFile->Get( hist[0] );
  data[0]->SetName(hist[0] + "__DATA");
  data[1] = (TH1F*) dataFile->Get( hist[1] );
  data[1]->SetName(hist[1] + "__DATA_2");

  
  // do the subtraction
  for (int is=0; is<nSYST; is++) {
    wjets[is][0]->hist() ->Add(wjets[is][1]->hist(), -1);
    singletop[is][0]->hist() ->Add(singletop[is][1]->hist(), -1);
    ttbar_semiLep[is][0]->hist() ->Add(ttbar_semiLep[is][1]->hist(), -1);
    ttbar_nonSemiLep[is][0]->hist() ->Add(ttbar_nonSemiLep[is][1]->hist(), -1);
    // do the ttbar combination
    ttbar[is][0]->Add(ttbar[is][1], -1);
  }
  qcd[0]->hist() ->Add(qcd[1]->hist(), -1);
  qcd[0]->hist()->Scale(nqcd / qcd[0]->hist()->GetSum());
  data[0]->Add(data[1], -1);


  // write the histograms to a file
  TString outname;
  if (use2D && doElectron) outname = "NormalizedHists_" + pdfdir + "/normalized2d_eljets_"+hist[1]+"_subtracted_from_"+hist[0]+".root";
  else if (use2D) outname = "NormalizedHists_" + pdfdir + "/normalized2d_mujets_"+hist[1]+"_subtracted_from_"+hist[0]+".root";
  else outname = "NormalizedHists_" + pdfdir + "/normalized_mujets_"+hist[1]+"_subtracted_from_"+hist[0]+".root";

  TFile* fout = new TFile(outname, "RECREATE");

  fout->cd();

  for (int is=0; is<nSYST; is++) {
    wjets[is][0]->hist()->Write();
    singletop[is][0]->hist()->Write();
    ttbar_semiLep[is][0]->hist()->Write();
    ttbar_nonSemiLep[is][0]->hist()->Write();
    ttbar[is][0]->Write();
  }

  qcd[0]->hist()->Write();
  data[0]->Write();

  fout->Close();


}

