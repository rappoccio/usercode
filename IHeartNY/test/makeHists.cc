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

void makePlots(TString var, int cut, int cut2=0, bool doElectron=false, TString ptbin = "", TString pdfdir="CT10_nom", bool postfit=false, bool combined=false) {

  TString mydir = pdfdir;
  if (do_htlep150qcd) mydir = "htlep150qcd";
  else if (do_met50qcd) mydir = "met50qcd";
  else if (do_qcd) mydir = "qcd";

  TString syst = "nom";

  TH1::AddDirectory(kFALSE); 
  setStyle();

  if ( !((cut==4 && cut2==6) || (cut==5 && cut2==6) || (cut==6 && cut2==7) || (cut==7 && cut2==0) || (cut==6 && cut2==0))) { 
    std::cout << "Not a valid option! Syntax is: " << std::endl
	      << "> makePlots(TString var, int cut, int cut2)" << std::endl
	      << "where (cut, cut2) = (4,6) or (5,6) or (6,7) or (7,0) or (6,0). Exiting..." << std::endl;
    return;
  }

  TString hist = var;
  hist += cut;
  hist += ptbin;
  TString hist2 = var;
  hist2 += cut2;
  hist2 += ptbin;

  // read QCD normalization
  std::pair<double, double> qcdnorm = getQCDnorm(cut, doElectron, ptbin);
  double nqcd = qcdnorm.first;
  double err_qcd = qcdnorm.second; 

  if (cut==6 && cut2==0) {
    std::pair<double, double> qcdnorm2 = getQCDnorm(7, doElectron, ptbin);
    double nqcd2 = qcdnorm2.first;
    //double err_qcd2 = qcdnorm2.second; 
    nqcd += nqcd2;
  }

  // get histograms
  SummedHist* wjets = getWJets( syst, hist, doElectron, ptbin );
  SummedHist* singletop = getSingleTop( syst, hist, doElectron, ptbin );
  SummedHist* ttbar = getTTbar( syst, hist, doElectron, ptbin, pdfdir );
  SummedHist* ttbar_nonSemiLep = getTTbarNonSemiLep( syst, hist, doElectron, ptbin, pdfdir  );
  SummedHist* qcd = getQCD( hist, doElectron, ptbin );
  
  SummedHist* wjets2;
  SummedHist* singletop2;
  SummedHist* ttbar2;
  SummedHist* ttbar_nonSemiLep2;
  SummedHist* qcd2;
  if (cut2>0) {
    wjets2 = getWJets( syst, hist2, doElectron, ptbin );
    singletop2 = getSingleTop( syst, hist2, doElectron, ptbin );
    ttbar2 = getTTbar( syst, hist2, doElectron, ptbin, pdfdir  );
    ttbar_nonSemiLep2 = getTTbarNonSemiLep( syst, hist2, doElectron, ptbin, pdfdir  );
    qcd2 = getQCD( hist2, doElectron, ptbin );
  }

  TString filepath;
  if (use2D && doElectron) filepath = "histfiles/2Dhist_el/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
  else if (use2D) filepath = "histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  else filepath = "histfiles/SingleMu_iheartNY_V1_mu_Run2012_nom.root";

  if (do_htlep150qcd) {
    if (doElectron) filepath = "histfiles_htlep150qcd/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
    else filepath = "histfiles_htlep150/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  }
  else if (do_met50qcd) {
    if (doElectron) filepath = "histfiles_met50qcd/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
    else filepath = "histfiles_met50qcd/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  }
  else if (do_qcd) {
    if (doElectron) filepath = "histfiles_qcd/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
    else filepath = "histfiles_qcd/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  }

  TFile* dataFile = TFile::Open(filepath);
  TH1F* h_data = (TH1F*) dataFile->Get( hist );
  TString channel = "mu_";
  if (doElectron) channel = "el_";
  h_data->SetName(channel + hist + "__DATA");

  TH1F* h_data2;
  if (cut2>0) {
    h_data2 = (TH1F*) dataFile->Get( hist2 );
    h_data2->SetName(channel + hist + "__DATA_2");
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

  // ------------------------------------------------------------------------------------
  // Rescale to post-fit normalizations if making post-fit plots
  if (postfit) {
    // get ratios
    float ttbarRatio = getPostPreRatio(doElectron, ptbin, mydir, combined, "ttbar", cut, cut2);
    float singletopRatio = getPostPreRatio(doElectron, ptbin, mydir, combined, "singletop", cut, cut2);
    float wjetsRatio = getPostPreRatio(doElectron, ptbin, mydir, combined, "wjets", cut, cut2);
    float qcdRatio = getPostPreRatio(doElectron, ptbin, mydir, combined, "qcd", cut, cut2);
    
    // And now use post/pre fit ratio to rescale
    h_ttbar->Scale(ttbarRatio);
    h_ttbar_nonSemiLep->Scale(ttbarRatio);
    h_singletop->Scale(singletopRatio);
    h_wjets->Scale(wjetsRatio);
    h_qcd->Scale(qcdRatio);
  }

  // -------------------------------------------------------------------------------------
  // various hist plotting edits

  // rebinning
  float rebin = 1;
  TString newtitle;
  if (var=="etaLep"){
    rebin = 2;
    if (doElectron) newtitle = "Electrons / 0.2";
    else newtitle = "Muons / 0.2";
  }
  else if (var.Contains("etaAbsLep")){
    rebin = rebinEta;
    if (doElectron) newtitle = "Electrons / 0.1";
    else newtitle = "Muons / 0.1";
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
    rebin = 5;
    newtitle = "Events / 25 GeV";
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
    if (doElectron) newtitle = "Electrons / 10 GeV";
    else newtitle = "Muons / 10 GeV";
  }
  else if (hist=="ptMET4") {
    rebin = 5;
    newtitle = "Events / 10 GeV";
  }
  else if (hist=="ptMET6" || hist=="ptMET7") {
    rebin = 10;
    newtitle = "Events / 20 GeV";
  }
  else if (hist.Contains("vtxMass")) {
    rebin = rebinSVM;
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

  if (var=="etaAbsLep" && doElectron) h_data->GetXaxis()->SetTitle("Electron |#eta|");
  else if (var=="etaAbsLep") h_data->GetXaxis()->SetTitle("Muon |#eta|");

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
  if (var.Contains("etaAbs") && doElectron) 
    max = max*1.4;
  else if (var.Contains("etaAbs") || var=="lepMET" || var=="leptop_mass") 
    max = max*1.2;
  else if (var.Contains("eta") && doElectron)
    max = max*1.8;
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

  if (use2D && doElectron) outname = "Plots/el_"+mydir+"_";
  else if (use2D) outname = "Plots/mu_"+mydir+"_";
  else outname = "Plots/mu_relIso_"+mydir+"_";

  if (postfit) {
    if (cut==6 && cut2==0){
      c->SaveAs(outname+hist+"_inc_postfit.png");
      c->SaveAs(outname+hist+"_inc_postfit.pdf");
    }
    else {
      c->SaveAs(outname+hist+"_postfit.png");
      c->SaveAs(outname+hist+"_postfit.pdf");
    }
  }
  else {
    if (cut2==0) {
      c->SaveAs(outname+hist+"_prefit.png");
      c->SaveAs(outname+hist+"_prefit.pdf");
    }
    else {
      c->SaveAs(outname+hist2+"_subtracted_from_"+hist+"_prefit.png");
      c->SaveAs(outname+hist2+"_subtracted_from_"+hist+"_prefit.pdf");
    }
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

void makePosteriorPlots(TString what, bool doElectron=false, TString ptbin = "", TString pdfdir="CT10_nom", bool combined=false, bool half = false, bool separate = false) {

  TH1::AddDirectory(kFALSE); 
  setStyle();

  TString mydir = pdfdir;
  if (do_htlep150qcd) mydir = "htlep150qcd";
  else if (do_met50qcd) mydir = "met50qcd";
  else if (do_qcd) mydir = "qcd";

  // read MC histograms
  TFile* fMC;
  if (combined) {
    if (ptbin == "") fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_comb.root");
    else if (separate) fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_comb_"+ptbin+"bin.root");
    else fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_comb_2bin.root");
  }
  else if (doElectron) {
    if (ptbin == "") fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_el.root");
    else if (separate) fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_el_"+ptbin+"bin.root");
    else fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_el_2bin.root");
  }
  else {
    if (ptbin == "") fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_mu.root");
    else if (separate) fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_mu_"+ptbin+"bin.root");
    else fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_mu_2bin.root");
  }
  
  TString channel = "mu_";
  if (doElectron) channel = "el_";

  TH1F* h_qcd = (TH1F*) fMC->Get(channel+what+ptbin+"__QCD");
  TH1F* h_wjets = (TH1F*) fMC->Get(channel+what+ptbin+"__WJets");
  TH1F* h_ttbar = (TH1F*) fMC->Get(channel+what+ptbin+"__TTbar");
  TH1F* h_singletop = (TH1F*) fMC->Get(channel+what+ptbin+"__SingleTop");


  // Construct post-fit ttbar
  // Get pre-fit plots needed
  TFile* fPre;
  TH1F* h_pre_ttbar;
  TH1F* h_pre_ttbar_nonSemiLep;

  TString append = "";
  if (half) {append = "_half";}

  if (what == "etaAbsLep4") {
    if (doElectron) fPre = TFile::Open("NormalizedHists_"+mydir+"/normalized2d_eljets_etaAbsLep6"+ptbin+"_subtracted_from_etaAbsLep4"+ptbin+append+".root");
    else fPre = TFile::Open("NormalizedHists_"+mydir+"/normalized2d_mujets_etaAbsLep6"+ptbin+"_subtracted_from_etaAbsLep4"+ptbin+append+".root");
    h_pre_ttbar = (TH1F*) fPre->Get(channel+what+ptbin+"__TTbar");
    h_pre_ttbar_nonSemiLep = (TH1F*) fPre->Get(channel+what+ptbin+"__TTbar_nonSemiLep");
  }

  if (what == "etaAbsLep5") {
    if (doElectron) fPre = TFile::Open("NormalizedHists_"+mydir+"/normalized2d_eljets_etaAbsLep6"+ptbin+"_subtracted_from_etaAbsLep5"+ptbin+append+".root");
    else fPre = TFile::Open("NormalizedHists_"+mydir+"/normalized2d_mujets_etaAbsLep6"+ptbin+"_subtracted_from_etaAbsLep5"+ptbin+append+".root");
    h_pre_ttbar = (TH1F*) fPre->Get(channel+what+ptbin+"__TTbar");
    h_pre_ttbar_nonSemiLep = (TH1F*) fPre->Get(channel+what+ptbin+"__TTbar_nonSemiLep");
  }

  if (what == "etaAbsLep6") {
    if (doElectron) fPre = TFile::Open("NormalizedHists_"+mydir+"/normalized2d_eljets_etaAbsLep7"+ptbin+"_subtracted_from_etaAbsLep6"+ptbin+append+".root");
    else fPre = TFile::Open("NormalizedHists_"+mydir+"/normalized2d_mujets_etaAbsLep7"+ptbin+"_subtracted_from_etaAbsLep6"+ptbin+append+".root");
    h_pre_ttbar = (TH1F*) fPre->Get(channel+what+ptbin+"__TTbar");
    h_pre_ttbar_nonSemiLep = (TH1F*) fPre->Get(channel+what+ptbin+"__TTbar_nonSemiLep");
  }

  if (what == "vtxMass7") {
    if (doElectron) fPre = TFile::Open("NormalizedHists_"+mydir+"/normalized2d_eljets_vtxMass7"+ptbin+append+".root");
    else fPre = TFile::Open("NormalizedHists_"+mydir+"/normalized2d_mujets_vtxMass7"+ptbin+append+".root");
    h_pre_ttbar = (TH1F*) fPre->Get(channel+what+ptbin+"__TTbar");
    h_pre_ttbar_nonSemiLep = (TH1F*) fPre->Get(channel+what+ptbin+"__TTbar_nonSemiLep");
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

  if (do_htlep150qcd) {
    if (doElectron) filepath = "histfiles_htlep150qcd/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
    else filepath = "histfiles_htlep150/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  }
  else if (do_met50qcd) {
    if (doElectron) filepath = "histfiles_met50qcd/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
    else filepath = "histfiles_met50qcd/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  }
  else if (do_qcd) {
    if (doElectron) filepath = "histfiles_qcd/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
    else filepath = "histfiles_qcd/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  }

  TFile* dataFile = TFile::Open(filepath);
  TH1F* h_data = (TH1F*) dataFile->Get( what+ptbin );
  h_data->SetName(channel + what + ptbin + "__DATA");

  if (what=="etaAbsLep4" || what=="etaAbsLep5") {
    TH1F* h_data2 = (TH1F*) dataFile->Get("etaAbsLep6"+ptbin);
    h_data->Add(h_data2,-1);
  }
  else if (what=="etaAbsLep6") {
    TH1F* h_data2 = (TH1F*) dataFile->Get("etaAbsLep7"+ptbin);
    h_data->Add(h_data2,-1);
  }

  if (what.Contains("etaAbsLep")) h_data->Rebin(rebinEta);
  if (what.Contains("vtxMass")) h_data->Rebin(rebinSVM);

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

  h_data->SetLineWidth(1);
  h_data->SetMarkerStyle(20);

  // axis ranges
  if (what.Contains("etaAbsLep") && doElectron) h_data->GetXaxis()->SetTitle("Electron |#eta|");
  else if (what.Contains("etaAbsLep")) h_data->GetXaxis()->SetTitle("Muon |#eta|");

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
  cout << "Number of bins in data hist: " << h_ratio->GetNbinsX() << endl;
  cout << "Number of bins in bkg hist:  " << h_totalbkg->GetNbinsX() << endl;
  h_ratio->Divide(h_totalbkg);

  // automatically set y-range
  float max = h_totalbkg->GetMaximum();
  if ( (h_data->GetMaximum() + h_data->GetBinError(h_data->GetMaximumBin())) > max)
    max = (h_data->GetMaximum() + h_data->GetBinError(h_data->GetMaximumBin()));
  if (what.Contains("etaAbs") && doElectron) max = max*1.4;
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
  if (use2D && doElectron) outname = "Plots/el_"+mydir+"_";
  else if (use2D) outname = "Plots/mu_"+mydir+"_";
  else outname = "Plots/mu_relIso_"+mydir+"_";

  if (combined) {
    c->SaveAs(outname+what+ptbin+"_combined_postfit.png");
    c->SaveAs(outname+what+ptbin+"_combined_postfit.pdf");
  }
  else {
    c->SaveAs(outname+what+ptbin+"_postfit.png");
    c->SaveAs(outname+what+ptbin+"_postfit.pdf");
  }


}

// -------------------------------------------------------------------------------------
// print post-fit latex table
// -------------------------------------------------------------------------------------
void makeTable(bool doElectron=false, TString ptbin = "", TString pdfdir="CT10_nom", bool combined=false, bool half = false, bool separate = false) {

  TString what[3] = {"etaAbsLep4","etaAbsLep6","vtxMass7"};
  if (do_htlep150qcd) what[0] = "etaAbsLep5";

  TString mydir = pdfdir;
  if (do_htlep150qcd) mydir = "htlep150qcd";
  else if (do_met50qcd) mydir = "met50qcd";
  else if (do_qcd) mydir = "qcd";

  // post-fit file
  TFile* fMC;
  if (combined) {
    if (ptbin == "") fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_comb.root");
    else if (separate) fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_comb_"+ptbin+"bin.root");
    else fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_comb_2bin.root");
  }
  else if (doElectron) {
    if (ptbin == "") fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_el.root");
    else if (separate) fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_el_"+ptbin+"bin.root");
    else fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_el_2bin.root");
  }
  else {
    if (ptbin == "") fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_mu.root");
    else if (separate) fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_mu_"+ptbin+"bin.root");
    else fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_mu_2bin.root");
  }
  if (fMC->IsOpen()) cout << "fMC exists." << endl;

  TString channel = "mu_";
  if (doElectron) channel = "el_";

  // -------------------------------------------------------------------------------------
  // post-fit relative errors

  float fiterrors_mu[14][5] = { 
    //{0.136178123407, 0.601654603004, 0.107520601458, 0.189270027384, 0}, // bkg error for CT10_nom
    {0.134833771366, 0.589591484549, 0.0903075025146, 0.192926881092, 0}, // bkg error for CT10_nom, rebin2
    {0.143531426537, 0.598861647354, 0.118749010228, 0.17877006537, 0}, // bkg error for CT10_pdfup
    {0.130687667319, 0.605431130473, 0.101669245525, 0.201031298083, 0}, // bkg error for CT10_pdfdown
    {0.136783615402, 0.602547816426, 0.106699756697, 0.187132367989, 0}, // bkg error for MSTW_nom
    {0.140163559205, 0.601482716006, 0.105191778271, 0.178049366831, 0}, // bkg error for MSTW_pdfup
    {0.133399760853, 0.607158012514, 0.100233756792, 0.187022124435, 0}, // bkg error for MSTW_pdfdown
    {0.128775723625, 0.60633215304, 0.100101491409, 0.147944135982, 0}, // bkg error for NNPDF_nom
    {0.137692548323, 0.599663471177, 0.109630997391, 0.157640524812, 0}, // bkg error for NNPDF_pdfup
    {0.11497450265, 0.221847501289, 0.0987162898554, 0.102294968977, 0}, // bkg error for NNPDF_pdfdown
    {0.138847207632, 0.600972713537, 0.0909056536277, 0.254303726506, 0}, // bkg error for scaleup
    {0.128661027311, 0.619019648158, 0.106169998694, 0.144190709959, 0}, // bkg error for scaledown
    {0.150840299166, 0.580282203849, 0.112694931383, 0.115630776147, 0}, // bkg error for htlep150qcd, rebin2
    {0.113860903688, 0.519957519596, 0.111445745701, 0.277144566273, 0}, // bkg error for met50qcd, rebin2
    {0.142308035867, 0.605517180963, 0.107221545724, 0.171248812895, 0}, // bkg error for qcd, rebin2
  };

  float fiterrors_el[14][5] = { 
    //{0.0957933770128, 0.59028339844, 0.0472103974875, 0, 0.0794465593408}, // bkg error for CT10_nom
    {0.0915689893828, 0.589524196093, 0.0434118764149, 0, 0.0936672929441}, // bkg error for CT10_nom, rebin2
    {0.100258813306, 0.5829512792, 0.0491497479426, 0, 0.084463841562}, // bkg error for CT10_pdfup
    {0.0926329596172, 0.596707635175, 0.0460935658625, 0, 0.0781396612839}, // bkg error for CT10_pdfdown
    {0.0962764471065, 0.589462016388, 0.0465616436282, 0, 0.082966625466}, // bkg error for MSTW_nom
    {0.0990736949562, 0.580679994577, 0.0466003409818, 0, 0.0836971538139}, // bkg error for MSTW_pdfup
    {0.0942208210793, 0.592406547832, 0.0450632277318, 0, 0.07921780037}, // bkg error for MSTW_pdfdown
    {0.0946070692168, 0.591418070077, 0.0459171485167, 0, 0.0790261287167}, // bkg error for NNPDF_nom
    {0.0985517967114, 0.581767527745, 0.0484473989458, 0, 0.0802515066205}, // bkg error for NNPDF_pdfup
    {0.0924543854678, 0.599885485855, 0.0456366491384, 0, 0.0784735227221}, // bkg error for NNPDF_pdfdown
    {0.0931884714793, 0.572624704637, 0.0431043866965, 0, 0.078917635113}, // bkg error for scaleup
    {0.0948258962343, 0.570246409386, 0.0455002470189, 0, 0.0793221134465}, // bkg error for scaledown
    {0.124257831545, 0.453711536078, 0.109832396368, 0, 0.248553564316}, // bkg error for htlep150qcd, rebin2
    {0.107660903977, 0.51702094822, 0.0703718085366, 0, 0.356673438468}, // bkg error for met50qcd, rebin2
    {0.107740627952, 0.4421410844, 0.106870033597, 0, 0.117778031187}, // bkg error for qcd, rebin2
  };

  float fiterrors_comb[14][5] = {
    //{0.0721611675654, 0.591773485402, 0.06841616483, 0.639678706759, 0.0338012148088}, // bkg error for CT10_nom
    {0.0706994856803, 0.536838090537, 0.0560114073749, 0.666940896433, 0.0349182297444}, // bkg error for CT10_nom, rebin2
    {0.0759518444195, 0.58172119931, 0.0802638564576, 0.641348470177, 0.0337331527381}, // bkg error for CT10_pdfup
    {0.0694391184851, 0.60146043244, 0.0613154280035, 0.638477452069, 0.0337121836834}, // bkg error for CT10_pdfdown
    {0.0738743748088, 0.59171420035, 0.0657888916686, 0.602812188588, 0.0332891372117}, // bkg error for MSTW_nom
    {0.0749048121725, 0.581192580521, 0.0678101767718, 0.646875533048, 0.0336765128127}, // bkg error for MSTW_pdfup
    {0.0710567974537, 0.593266406591, 0.0595421597412, 0.643082922652, 0.0338992750817}, // bkg error for MSTW_pdfdown
    {0.072021892116, 0.573476242875, 0.0628321989737, 0.622733591949, 0.0343979197871}, // bkg error for NNPDF_nom
    {0.0758762718894, 0.56574133453, 0.0736357609411, 0.638645227605, 0.0338018165753}, // bkg error for NNPDF_pdfup
    {0.0742645332462, 0.112166670243, 0.0557335662488, 0.571708316278, 0.0349474470452}, // bkg error for NNPDF_pdfdown
    {0.0726118366479, 0.564493383356, 0.0566161939509, 0.665990785481, 0.0322017813192}, // bkg error for scaleup
    {0.0754581112506, 0.527287398678, 0.0613378760194, 0.657640817449, 0.0319922330817}, // bkg error for scaledown
    {0.0797793432868, 0.436673982919, 0.117476264232, 0.479697791925, 0.0676021303369}, // bkg error for htlep150qcd, rebin2
    {0.0777933806133, 0.472702127417, 0.0831352554973, 0.566704700279, 0.0932475666115}, // bkg error for met50qcd, rebin2
    {0.0759080952546, 0.502342636381, 0.0989305408165, 0.351178483059, 0.055901103397}, // bkg error for qcd, rebin2
  };

  float fiterrors_mu_2ptbin[3][5] = {
    {0.153410569218, 0.598937742677, 0.0921718236121, 0.199318659013, 0}, // bkg error for qcd, rebin2, Low pt(top) bin
    {0.230492312482, 0.476344069781, 0.18863020012, 0.301444715873, 0}, // bkg error for qcd, rebin2, High pt(top) bin
    {0.137690466395, 0.501412830187, 0.0949918112146, 0.28190079064, 0}, // bkg error for qcd, rebin2, 2 pt(top) bins
  };

  float fiterrors_el_2ptbin[3][5] = {
    {0.106755944098, 0.546974887111, 0.138810247851, 0, 0.164205434212}, // bkg error for qcd, rebin2, Low pt(top) bin
    {0.250142036318, 0.486119993791, 0.143680218105, 0, 0.124425736415}, // bkg error for qcd, rebin2, High pt(top) bin
    {0.102892639303, 0.478512779649, 0.0957950113209, 0, 0.137517557153}, // bkg error for qcd, rebin2, 2 pt(top) bins
  };

  float fiterrors_comb_2ptbin[3][5] = {
    {0.0809715225269, 0.566120896293, 0.097587110604, 0.501370440187, 0.0713407774204}, // bkg error for qcd, rebin2, Low pt(top) bin
    {0.164614561913, 0.406930486902, 0.170859948591, 0.286234154767, 0.066887070246}, // bkg error for qcd, rebin2, High pt(top) bin
    {0.0769810174487, 0.489022966152, 0.0828255065459, 0.466077480054, 0.0660274098057}, // bkg error for qcd, rebin2, 2 pt(top) bins
  };


  TString pdfs[14] = {"CT10_nom","CT10_pdfup","CT10_pdfdown",
		      "MSTW_nom","MSTW_pdfup","MSTW_pdfdown",
		      "NNPDF_nom","NNPDF_pdfup","NNPDF_pdfdown",
		      "scaleup","scaledown","htlep150qcd","met50qcd","qcd"};
  int thispdf = -1;
  for (int ipdf=0; ipdf<14; ipdf++) {
    if (mydir == pdfs[ipdf]) {
      thispdf = ipdf;
      break;
    }
  }
  if (thispdf == -1) {
    cout << "UNKNOWN PDF! exiting..." << endl;
    return;
  }

  float fiterr_tt = 0;
  float fiterr_singletop = 0;
  float fiterr_wjets = 0;
  float fiterr_qcd = 0;

  if (doElectron && !combined) {
    if (ptbin == "") {
      fiterr_tt = fiterrors_el[thispdf][0];
      fiterr_singletop = fiterrors_el[thispdf][1];
      fiterr_wjets = fiterrors_el[thispdf][2];
      fiterr_qcd = fiterrors_el[thispdf][4];
    }
    else if (ptbin == "Low") {
      fiterr_tt = fiterrors_el_2ptbin[0][0];
      fiterr_singletop = fiterrors_el_2ptbin[0][1];
      fiterr_wjets = fiterrors_el_2ptbin[0][2];
      fiterr_qcd = fiterrors_el_2ptbin[0][4];
    }
    else if (ptbin == "High") {
      fiterr_tt = fiterrors_el_2ptbin[1][0];
      fiterr_singletop = fiterrors_el_2ptbin[1][1];
      fiterr_wjets = fiterrors_el_2ptbin[1][2];
      fiterr_qcd = fiterrors_el_2ptbin[1][4];
    }
    else if (ptbin == "2") {
      fiterr_tt = fiterrors_el_2ptbin[2][0];
      fiterr_singletop = fiterrors_el_2ptbin[2][1];
      fiterr_wjets = fiterrors_el_2ptbin[2][2];
      fiterr_qcd = fiterrors_el_2ptbin[2][4];
    }
  }
  else if (doElectron) {
    if (ptbin == "") {
      fiterr_tt = fiterrors_comb[thispdf][0];
      fiterr_singletop = fiterrors_comb[thispdf][1];
      fiterr_wjets = fiterrors_comb[thispdf][2];
      fiterr_qcd = fiterrors_comb[thispdf][4];
    }
    else if (ptbin == "Low") {
      fiterr_tt = fiterrors_comb_2ptbin[0][0];
      fiterr_singletop = fiterrors_comb_2ptbin[0][1];
      fiterr_wjets = fiterrors_comb_2ptbin[0][2];
      fiterr_qcd = fiterrors_comb_2ptbin[0][4];
    }
    else if (ptbin == "High") {
      fiterr_tt = fiterrors_comb_2ptbin[1][0];
      fiterr_singletop = fiterrors_comb_2ptbin[1][1];
      fiterr_wjets = fiterrors_comb_2ptbin[1][2];
      fiterr_qcd = fiterrors_comb_2ptbin[1][4];
    }
    else if (ptbin == "2") {
      fiterr_tt = fiterrors_comb_2ptbin[2][0];
      fiterr_singletop = fiterrors_comb_2ptbin[2][1];
      fiterr_wjets = fiterrors_comb_2ptbin[2][2];
      fiterr_qcd = fiterrors_comb_2ptbin[2][4];
    }
  }
  else if (!doElectron && !combined) {
    if (ptbin == ""){
      fiterr_tt = fiterrors_mu[thispdf][0];
      fiterr_singletop = fiterrors_mu[thispdf][1];
      fiterr_wjets = fiterrors_mu[thispdf][2];
      fiterr_qcd = fiterrors_mu[thispdf][3];
    }
    else if (ptbin == "Low") {
      fiterr_tt = fiterrors_mu_2ptbin[0][0];
      fiterr_singletop = fiterrors_mu_2ptbin[0][1];
      fiterr_wjets = fiterrors_mu_2ptbin[0][2];
      fiterr_qcd = fiterrors_mu_2ptbin[0][3];
    }
    else if (ptbin == "High") {
      fiterr_tt = fiterrors_mu_2ptbin[1][0];
      fiterr_singletop = fiterrors_mu_2ptbin[1][1];
      fiterr_wjets = fiterrors_mu_2ptbin[1][2];
      fiterr_qcd = fiterrors_mu_2ptbin[1][3];
    }
    else if (ptbin == "2") {
      fiterr_tt = fiterrors_mu_2ptbin[2][0];
      fiterr_singletop = fiterrors_mu_2ptbin[2][1];
      fiterr_wjets = fiterrors_mu_2ptbin[2][2];
      fiterr_qcd = fiterrors_mu_2ptbin[2][3];
    }
  }
  else {
    if (ptbin == "") {
      fiterr_tt = fiterrors_comb[thispdf][0];
      fiterr_singletop = fiterrors_comb[thispdf][1];
      fiterr_wjets = fiterrors_comb[thispdf][2];
      fiterr_qcd = fiterrors_comb[thispdf][3];
    }
    else if (ptbin == "Low") {
      fiterr_tt = fiterrors_comb_2ptbin[0][0];
      fiterr_singletop = fiterrors_comb_2ptbin[0][1];
      fiterr_wjets = fiterrors_comb_2ptbin[0][2];
      fiterr_qcd = fiterrors_comb_2ptbin[0][3];
    }
    else if (ptbin == "High") {
      fiterr_tt = fiterrors_comb_2ptbin[1][0];
      fiterr_singletop = fiterrors_comb_2ptbin[1][1];
      fiterr_wjets = fiterrors_comb_2ptbin[1][2];
      fiterr_qcd = fiterrors_comb_2ptbin[1][3];
    }
    else if (ptbin == "2") {
      fiterr_tt = fiterrors_comb_2ptbin[2][0];
      fiterr_singletop = fiterrors_comb_2ptbin[2][1];
      fiterr_wjets = fiterrors_comb_2ptbin[2][2];
      fiterr_qcd = fiterrors_comb_2ptbin[2][3];
    }
  }

  TString append = "";
  if (half) {append = "_half";}

  // pre-fit & data files
  TFile* fDATA[3];
  if (doElectron) {
    if (do_htlep150qcd) fDATA[0] = new TFile("NormalizedHists_"+mydir+"/normalized2d_eljets_etaAbsLep6"+ptbin+"_subtracted_from_etaAbsLep5"+ptbin+append+".root");
    else fDATA[0] = new TFile("NormalizedHists_"+mydir+"/normalized2d_eljets_etaAbsLep6"+ptbin+"_subtracted_from_etaAbsLep4"+ptbin+append+".root");
    fDATA[1] = new TFile("NormalizedHists_"+mydir+"/normalized2d_eljets_etaAbsLep7"+ptbin+"_subtracted_from_etaAbsLep6"+ptbin+append+".root");
    fDATA[2] = new TFile("NormalizedHists_"+mydir+"/normalized2d_eljets_vtxMass7"+ptbin+append+".root");
  }
  else {
    if (do_htlep150qcd) fDATA[0] = new TFile("NormalizedHists_"+mydir+"/normalized2d_mujets_etaAbsLep6"+ptbin+"_subtracted_from_etaAbsLep5"+ptbin+append+".root");
    else fDATA[0] = new TFile("NormalizedHists_"+mydir+"/normalized2d_mujets_etaAbsLep6"+ptbin+"_subtracted_from_etaAbsLep4"+ptbin+append+".root");
    fDATA[1] = new TFile("NormalizedHists_"+mydir+"/normalized2d_mujets_etaAbsLep7"+ptbin+"_subtracted_from_etaAbsLep6"+ptbin+append+".root");
    fDATA[2] = new TFile("NormalizedHists_"+mydir+"/normalized2d_mujets_vtxMass7"+ptbin+append+".root");
  }

  for (int ii = 0; ii < 3; ii++){
    if (fDATA[ii]->IsOpen()) cout << "fDATA[" << ii << "] exists." << endl;
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
  std::pair<double, double> qcdnorm4 = getQCDnorm(4, doElectron, ptbin);
  std::pair<double, double> qcdnorm6 = getQCDnorm(6, doElectron, ptbin);
  std::pair<double, double> qcdnorm7 = getQCDnorm(7, doElectron, ptbin);
  double err_qcd_up[3];
  double err_qcd_dn[3];
  if (do_htlep150qcd) {
    std::pair<double, double> qcdnorm5 = getQCDnorm(5, doElectron, ptbin);
    err_qcd_up[0] = qcdnorm5.second; 
  }
  else err_qcd_up[0] = qcdnorm4.second; 
  err_qcd_dn[0] = err_qcd_up[0];
  err_qcd_up[1] = qcdnorm6.second; 
  err_qcd_dn[1] = err_qcd_up[1];
  err_qcd_up[2] = qcdnorm7.second; 
  if (err_qcd_up[2] > qcdnorm7.first) err_qcd_dn[2] = qcdnorm7.first;
  else err_qcd_dn[2] = err_qcd_up[2];

  // get histograms
  for (int i=0; i<3; i++) {

    // post-fit values
    h_qcd[i]   = (TH1F*) fMC->Get(channel+what[i]+ptbin+"__QCD");
    h_wjets[i] = (TH1F*) fMC->Get(channel+what[i]+ptbin+"__WJets");
    h_ttbar[i] = (TH1F*) fMC->Get(channel+what[i]+ptbin+"__TTbar");
    h_singletop[i] = (TH1F*) fMC->Get(channel+what[i]+ptbin+"__SingleTop");

    // data
    h_data[i] = (TH1F*) fDATA[i]->Get(channel+what[i]+ptbin+"__DATA");

    //pre-fit values
    h_pre_qcd[i]   = (TH1F*) fDATA[i]->Get(channel+what[i]+ptbin+"__QCD");
    h_pre_wjets[i] = (TH1F*) fDATA[i]->Get(channel+what[i]+ptbin+"__WJets");
    h_pre_ttbar[i] = (TH1F*) fDATA[i]->Get(channel+what[i]+ptbin+"__TTbar");
    h_pre_ttbar_semiLep[i] = (TH1F*) fDATA[i]->Get(channel+what[i]+ptbin+"__TTbar_semiLep");
    h_pre_ttbar_nonSemiLep[i] = (TH1F*) fDATA[i]->Get(channel+what[i]+ptbin+"__TTbar_nonSemiLep");
    h_pre_singletop[i] = (TH1F*) fDATA[i]->Get(channel+what[i]+ptbin+"__SingleTop");

    //Construct post-fit ttbar
    float postPreRatio = h_ttbar[i]->Integral() / h_pre_ttbar[i]->Integral();
    // post-fit nonSemiLep is pre-fit nonSemiLep scaled by post/pre fit ratio
    h_ttbar_nonSemiLep[i] = (TH1F*) h_pre_ttbar_nonSemiLep[i]->Clone();
    h_ttbar_nonSemiLep[i]->Scale(postPreRatio);
    // post-fit semiLep is post-fit total with post-fit nonSemiLep subtracted
    h_ttbar_semiLep[i] = (TH1F*) h_ttbar[i]->Clone();
    h_ttbar_semiLep[i]->Add(h_ttbar_nonSemiLep[i], -1);

    h_total[i] = (TH1F*) h_qcd[i]->Clone(what[i]+ptbin+"_total");
    h_total[i]->Add(h_wjets[i]);
    h_total[i]->Add(h_ttbar[i]);
    h_total[i]->Add(h_singletop[i]);

    h_pre_total[i] = (TH1F*) h_pre_qcd[i]->Clone(what[i]+ptbin+"_pre_total");
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
  std::cout << "PDF set: " << mydir << std::endl;
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


  TString outblaj = "";
  if (doElectron) outblaj = " and options.lepType == \"ele\" ";
  else outblaj = " and options.lepType == \"muon\" ";


  // 1toptag+1btag (nom, up, dn) + 1toptag+>=0btag (nom, up, dn) 
  std::cout << std::endl << "---------------------------------------------------------------------------------" << std::endl;
  std::cout << "For copying to unfolding script!" << std::endl;
  std::cout << "(background counts: 1toptag+1btag (nom, up, dn), 1toptag+>=0btag (nom, up, dn))" << std::endl;
  std::cout << "---------------------------------------------------------------------------------" << std::endl;
  std::cout << "if options.pdf == \"" << mydir << "\"" << outblaj << ":   #unfold" << std::endl;
  std::cout << "    n_ttbarnonsemilep = ["
	    << h_ttbar_nonSemiLep[2]->Integral() << ", " << h_ttbar_nonSemiLep[2]->Integral()*(1+fiterr_tt) << ", " << h_ttbar_nonSemiLep[2]->Integral()*(1-fiterr_tt) << ", "
	    << (h_ttbar_nonSemiLep[1]->Integral()+h_ttbar_nonSemiLep[2]->Integral()) << ", " 
	    << (h_ttbar_nonSemiLep[1]->Integral()+h_ttbar_nonSemiLep[2]->Integral())*(1+fiterr_tt) << ", " 
	    << (h_ttbar_nonSemiLep[1]->Integral()+h_ttbar_nonSemiLep[2]->Integral())*(1-fiterr_tt) << "]   #unfold" << std::endl;
  std::cout << "    n_wjets           = ["
	    << h_wjets[2]->Integral() << ", " << h_wjets[2]->Integral()*(1+fiterr_wjets) << ", " << h_wjets[2]->Integral()*(1-fiterr_wjets) << ", "
	    << (h_wjets[1]->Integral()+h_wjets[2]->Integral()) << ", " 
	    << (h_wjets[1]->Integral()+h_wjets[2]->Integral())*(1+fiterr_wjets) << ", " 
	    << (h_wjets[1]->Integral()+h_wjets[2]->Integral())*(1-fiterr_wjets) << "]   #unfold" << std::endl;
  std::cout << "    n_singletop       = ["
	    << h_singletop[2]->Integral() << ", " << h_singletop[2]->Integral()*(1+fiterr_singletop) << ", " << h_singletop[2]->Integral()*(1-fiterr_singletop) << ", "
	    << (h_singletop[1]->Integral()+h_singletop[2]->Integral()) << ", " 
	    << (h_singletop[1]->Integral()+h_singletop[2]->Integral())*(1+fiterr_singletop) << ", " 
	    << (h_singletop[1]->Integral()+h_singletop[2]->Integral())*(1-fiterr_singletop) << "]   #unfold" << std::endl;
  std::cout << "    n_qcd             = ["
	    << h_qcd[2]->Integral() << ", " << h_qcd[2]->Integral()*(1+fiterr_qcd) << ", " << h_qcd[2]->Integral()*(1-fiterr_qcd) << ", "
	    << (h_qcd[1]->Integral()+h_qcd[2]->Integral()) << ", " 
	    << (h_qcd[1]->Integral()+h_qcd[2]->Integral())*(1+fiterr_qcd) << ", " 
	    << (h_qcd[1]->Integral()+h_qcd[2]->Integral())*(1-fiterr_qcd) << "]   #unfold" << std::endl;
  std::cout << "---------------------------------------------------------------------------------" << std::endl << std::endl;
  
}


// -------------------------------------------------------------------------------------
// make theta histograms without subtracting
// -------------------------------------------------------------------------------------

void makeTheta_single(TString var, int cut, TString ptbin, bool doElectron=false, TString pdfdir="CT10_nom", bool half = false) {
  
  TH1::AddDirectory(kFALSE); 
  setStyle();

  if ( !(cut==7) ) {
    std::cout << "Not a valid option! Syntax is: " << std::endl
	      << "> makeTheta_single(TString var, int cut)" << std::endl
	      << "where cut == 7. Exiting..." << std::endl;
    return;
  }

  TString mydir = pdfdir;
  if (do_htlep150qcd) mydir = "htlep150qcd";
  else if (do_met50qcd) mydir = "met50qcd";
  else if (do_qcd) mydir = "qcd";
 
  TString hist = var;
  hist += cut;
  hist += ptbin;


  // read QCD normalization
  std::pair<double, double> qcdnorm = getQCDnorm(cut, doElectron, ptbin, half);
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

  TString channel = "mu_";
  if (doElectron) channel = "el_";

  for (int is=0; is<nSYST; is++) {
    wjets[is]     = getWJets( name_syst[is], hist, doElectron, ptbin );
    singletop[is] = getSingleTop( name_syst[is], hist, doElectron, ptbin );
    ttbar_semiLep[is]     = getTTbar( name_syst[is], hist, doElectron, ptbin, pdfdir );
    ttbar_nonSemiLep[is] = getTTbarNonSemiLep( name_syst[is], hist, doElectron, ptbin, pdfdir );

    // do the ttbar combination
    ttbar[is] = (TH1F*) ttbar_semiLep[is]->hist()->Clone();
    ttbar[is]->Add(ttbar_nonSemiLep[is]->hist());

    TString tempname = channel + hist + "__TTbar";
    adjustThetaName( tempname, name_syst[is], ptbin );
    ttbar[is]->SetName(tempname);

    // Do rebinning
    wjets[is]->hist()->Rebin(rebinSVM);
    singletop[is]->hist()->Rebin(rebinSVM);
    ttbar_semiLep[is]->hist()->Rebin(rebinSVM);
    ttbar_nonSemiLep[is]->hist()->Rebin(rebinSVM);
    ttbar[is]->Rebin(rebinSVM);  
  }

  // QCD
  SummedHist* qcd = getQCD( hist, doElectron, ptbin );
  qcd->hist()->Rebin(rebinSVM);    

  // data
  TString filepath;
  if (use2D && doElectron) filepath = "histfiles/2Dhist_el/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
  else if (use2D) filepath = "histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  else filepath = "histfiles/SingleMu_iheartNY_V1_mu_Run2012_nom.root";

  if (do_htlep150qcd) {
    if (doElectron) filepath = "histfiles_htlep150qcd/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
    else filepath = "histfiles_htlep150/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  }
  else if (do_met50qcd) {
    if (doElectron) filepath = "histfiles_met50qcd/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
    else filepath = "histfiles_met50qcd/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  }
  else if (do_qcd) {
    if (doElectron) filepath = "histfiles_qcd/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
    else filepath = "histfiles_qcd/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  }

  TFile* dataFile = TFile::Open(filepath);
  TH1F* data = (TH1F*) dataFile->Get( hist );
  data->SetName(channel + hist + "__DATA");
  data->Rebin(rebinSVM);  

  // write the histograms to a file
  TString outname;
  TString append = "";
  if (half) {append = "_half";}

  if (use2D && doElectron) outname = "NormalizedHists_" + mydir + "/normalized2d_eljets_"+hist+append+".root";
  else if (use2D) outname = "NormalizedHists_" + mydir + "/normalized2d_mujets_"+hist+append+".root";
  else outname = "NormalizedHists_" + mydir + "/normalized_mujets_"+hist+append+".root";
  

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

void makeTheta_subtract(TString var, int cut1, int cut2, TString ptbin, bool doElectron=false, TString pdfdir="_CT10_nom", bool half = false) {

  TH1::AddDirectory(kFALSE); 
  setStyle();

  if ( !((cut1==4 && cut2==6) || (cut1==5 && cut2==6) || (cut1==6 && cut2==7)) ) {
    std::cout << "Not a valid option! Syntax is: " << std::endl
	      << "> makeTheta_subtract(TString var, int cut1, int cut2)" << std::endl
	      << "where (cut1, cut2) = (4,6) or (6,7). Exiting..." << std::endl;
    return;
  }

  TString mydir = pdfdir;
  if (do_htlep150qcd) mydir = "htlep150qcd";
  else if (do_met50qcd) mydir = "met50qcd";
  else if (do_qcd) mydir = "qcd";
 
  TString hist[2] = {var, var};
  hist[0] += cut1;
  hist[1] += cut2;
  hist[0] += ptbin;
  hist[1] += ptbin;

  // read QCD normalization
  std::pair<double, double> qcdnorm = getQCDnorm(cut1, doElectron, ptbin, half);
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

  TString channel = "mu_";
  if (doElectron) channel = "el_";

  for (int ih=0; ih<2; ih++) {
    for (int is=0; is<nSYST; is++) {
      wjets[is][ih]     = getWJets( name_syst[is], hist[ih], doElectron, ptbin );
      singletop[is][ih] = getSingleTop( name_syst[is], hist[ih], doElectron, ptbin );
      ttbar_semiLep[is][ih]     = getTTbar( name_syst[is], hist[ih], doElectron, ptbin, pdfdir );
      ttbar_nonSemiLep[is][ih] = getTTbarNonSemiLep( name_syst[is], hist[ih], doElectron, ptbin, pdfdir );

      ttbar[is][ih] = (TH1F*) ttbar_semiLep[is][ih]->hist()->Clone();
      ttbar[is][ih]->Add(ttbar_nonSemiLep[is][ih]->hist());
      TString tempname = channel + hist[ih] + "__TTbar";
      adjustThetaName( tempname, name_syst[is], ptbin );
      ttbar[is][ih]->SetName(tempname);

      // Do rebinning
      wjets[is][ih]->hist()->Rebin(rebinEta);
      singletop[is][ih]->hist()->Rebin(rebinEta);
      ttbar_semiLep[is][ih]->hist()->Rebin(rebinEta);
      ttbar_nonSemiLep[is][ih]->hist()->Rebin(rebinEta);
      ttbar[is][ih]->Rebin(rebinEta); 
    }
  }

  // QCD
  SummedHist* qcd[2];
  qcd[0] = getQCD( hist[0], doElectron, ptbin );
  qcd[1] = getQCD( hist[1], doElectron, ptbin );
  qcd[0]->hist()->Rebin(rebinEta);
  qcd[1]->hist()->Rebin(rebinEta);

  // data
  TString filepath;
  if (use2D && doElectron) filepath = "histfiles/2Dhist_el/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
  else if (use2D) filepath = "histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  else filepath = "histfiles/SingleMu_iheartNY_V1_mu_Run2012_nom.root";

  if (do_htlep150qcd) {
    if (doElectron) filepath = "histfiles_htlep150qcd/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
    else filepath = "histfiles_htlep150/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  }
  else if (do_met50qcd) {
    if (doElectron) filepath = "histfiles_met50qcd/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
    else filepath = "histfiles_met50qcd/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  }
  else if (do_qcd) {
    if (doElectron) filepath = "histfiles_qcd/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
    else filepath = "histfiles_qcd/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  }

  TFile* dataFile = TFile::Open(filepath);

  TH1F* data[2];
  data[0] = (TH1F*) dataFile->Get( hist[0] );
  data[0]->SetName(channel + hist[0] + "__DATA");
  data[0]->Rebin(rebinEta);
  data[1] = (TH1F*) dataFile->Get( hist[1] );
  data[1]->SetName(channel + hist[1] + "__DATA_2");
  data[1]->Rebin(rebinEta);
  
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
  TString append = "";
  if (half) {append = "_half";}

  if (use2D && doElectron) outname = "NormalizedHists_" + mydir + "/normalized2d_eljets_"+hist[1]+"_subtracted_from_"+hist[0]+append+".root";
  else if (use2D) outname = "NormalizedHists_" + mydir + "/normalized2d_mujets_"+hist[1]+"_subtracted_from_"+hist[0]+append+".root";
  else outname = "NormalizedHists_" + mydir + "/normalized_mujets_"+hist[1]+"_subtracted_from_"+hist[0]+append+".root";
  

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

