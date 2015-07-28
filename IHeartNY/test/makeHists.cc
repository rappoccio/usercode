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
  //else if (do_qcd) mydir += "_qcd";  // --> this is now the default! 

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
    if (doElectron) filepath = "histfiles/qcd_el/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
    else filepath = "histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
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
  else if (var.Contains("hadtop_eta")){
    rebin = 2;
    newtitle = "Events / 0.2";
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
  else if (var.Contains("htLep")){
    rebin = rebinHTlep;
    newtitle = "Events / 40 GeV";
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

  if (use2D && doElectron) outname = "Plots/el_"+mydir+extName+"_";
  else if (use2D) outname = "Plots/mu_"+mydir+extName+"_";
  else outname = "Plots/mu_relIso_"+mydir+extName+"_";

  if (postfit) {

    TString namecomb = "";
    if (combined) namecomb = "_combined";

    if (cut==6 && cut2==0){
      c->SaveAs(outname+hist+"_inc"+namecomb+"_postfit.png");
      c->SaveAs(outname+hist+"_inc"+namecomb+"_postfit.pdf");
    }
    else {
      c->SaveAs(outname+hist+namecomb+"_postfit.png");
      c->SaveAs(outname+hist+namecomb+"_postfit.pdf");
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
  //else if (do_qcd) mydir += "_qcd"; // --> this is now the default!

  // read MC histograms
  TFile* fMC;
  if (combined) {
    if (ptbin == "") fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_comb"+extName+".root");
    else if (separate) fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_comb"+extName+"_"+ptbin+"bin.root");
    else fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_comb"+extName+"_2bin.root");
  }
  else if (doElectron) {
    if (ptbin == "") fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_el"+extName+".root");
    else if (separate) fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_el"+extName+"_"+ptbin+"bin.root");
    else fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_el"+extName+"_2bin.root");
  }
  else {
    if (ptbin == "") fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_mu"+extName+".root");
    else if (separate) fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_mu"+extName+"_"+ptbin+"bin.root");
    else fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_mu"+extName+"_2bin.root");
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

  if (what == "htLep4") {
    if (doElectron) fPre = TFile::Open("NormalizedHists_"+mydir+"/normalized2d_eljets_htLep6"+ptbin+"_subtracted_from_htLep4"+ptbin+append+".root");
    else fPre = TFile::Open("NormalizedHists_"+mydir+"/normalized2d_mujets_htLep6"+ptbin+"_subtracted_from_htLep4"+ptbin+append+".root");
    h_pre_ttbar = (TH1F*) fPre->Get(channel+what+ptbin+"__TTbar");
    h_pre_ttbar_nonSemiLep = (TH1F*) fPre->Get(channel+what+ptbin+"__TTbar_nonSemiLep");
  }

  if (what == "htLep6") {
    if (doElectron) fPre = TFile::Open("NormalizedHists_"+mydir+"/normalized2d_eljets_htLep7"+ptbin+"_subtracted_from_htLep6"+ptbin+append+".root");
    else fPre = TFile::Open("NormalizedHists_"+mydir+"/normalized2d_mujets_htLep7"+ptbin+"_subtracted_from_htLep6"+ptbin+append+".root");
    h_pre_ttbar = (TH1F*) fPre->Get(channel+what+ptbin+"__TTbar");
    h_pre_ttbar_nonSemiLep = (TH1F*) fPre->Get(channel+what+ptbin+"__TTbar_nonSemiLep");
  }

  if (what == "htLep7") {
    if (doElectron) fPre = TFile::Open("NormalizedHists_"+mydir+"/normalized2d_eljets_htLep7"+ptbin+append+".root");
    else fPre = TFile::Open("NormalizedHists_"+mydir+"/normalized2d_mujets_htLep7"+ptbin+append+".root");
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
    if (doElectron) filepath = "histfiles/qcd_el/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
    else filepath = "histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
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

  else if (what=="htLep4") {
    TH1F* h_data2 = (TH1F*) dataFile->Get("htLep6"+ptbin);
    h_data->Add(h_data2,-1);
  }
  else if (what=="htLep6") {
    TH1F* h_data2 = (TH1F*) dataFile->Get("htLep7"+ptbin);
    h_data->Add(h_data2,-1);
  }

  if (what.Contains("etaAbsLep")) h_data->Rebin(rebinEta);
  if (what.Contains("vtxMass")) h_data->Rebin(rebinSVM);
  if (what.Contains("htLep")) h_data->Rebin(rebinHTlep);

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
  if (use2D && doElectron) outname = "Plots/el_"+mydir+extName+"_";
  else if (use2D) outname = "Plots/mu_"+mydir+extName+"_";
  else outname = "Plots/mu_relIso_"+mydir+extName+"_";

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
  if (useHTlep == "6" || useHTlep == "46" || useHTlep == "467") {
    what[1] = "htLep6";
  }
  if (useHTlep == "46" || useHTlep == "467"){
    what[0] = "htLep4";
  }
  if (useHTlep == "467") what[2] = "htLep7";
  if (do_htlep150qcd) what[0] = "etaAbsLep5";

  TString mydir = pdfdir;
  if (do_htlep150qcd) mydir = "htlep150qcd";
  else if (do_met50qcd) mydir = "met50qcd";
  //else if (do_qcd) mydir += "_qcd"; // --> this is now the default

  // post-fit file
  TFile* fMC;
  if (combined) {
    if (ptbin == "") fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_comb"+extName+".root");
    else if (separate) fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_comb"+extName+"_"+ptbin+"bin.root");
    else fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_comb"+extName+"_2bin.root");
  }
  else if (doElectron) {
    if (ptbin == "") fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_el"+extName+".root");
    else if (separate) fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_el"+extName+"_"+ptbin+"bin.root");
    else fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_el"+extName+"_2bin.root");
  }
  else {
    if (ptbin == "") fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_mu"+extName+".root");
    else if (separate) fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_mu"+extName+"_"+ptbin+"bin.root");
    else fMC = new TFile("run_theta/histos-mle-2d-"+mydir+"_mu"+extName+"_2bin.root");
  }
  if (fMC->IsOpen()) cout << "fMC exists." << endl;

  TString channel = "mu_";
  if (doElectron) channel = "el_";

  // -------------------------------------------------------------------------------------
  // post-fit relative errors

  // -------------------------------------------------------------------------------------
  // these are the current default version! 
  // -------------------------------------------------------------------------------------

  float fiterrors_mu_extLumi_extBtag[11][5] = {
    {0.13623799557, 0.588013259541, 0.0896067390956, 0.190280435213, 0}, // bkg error for CT10_nom
    {0.141047195591, 0.584563234787, 0.0970293967236, 0.172037540546, 0}, // bkg error for CT10_pdfup
    {0.13201839681, 0.592757087347, 0.0846483545142, 0.209374249831, 0}, // bkg error for CT10_pdfdown
    {0.136654966326, 0.589173345724, 0.0880843814416, 0.188347196546, 0}, // bkg error for MSTW_nom
    {0.138961814824, 0.58798341699, 0.0881657981411, 0.174282317016, 0}, // bkg error for MSTW_pdfup
    {0.134224586658, 0.59296525239, 0.0831164994984, 0.195891932211, 0}, // bkg error for MSTW_pdfdown
    {0.130503514562, 0.595436400976, 0.0870571804119, 0.157450123033, 0}, // bkg error for NNPDF_nom
    {0.135198342114, 0.588280316998, 0.0919980761697, 0.152869682499, 0}, // bkg error for NNPDF_pdfup
    {0.124032832097, 0.574155316422, 0.083228620927, 0.156804230287, 0}, // bkg error for NNPDF_pdfdown
    {0.136621242877, 0.585878298604, 0.0813713702842, 0.228854103339, 0}, // bkg error for scaleup
    {0.132321463273, 0.58477773733, 0.102224845937, 0.156264820702, 0}, // bkg error for scaledown
  };
  float fiterrors_el_extLumi_extBtag[11][5] = {
    {0.104168517361, 0.488891930375, 0.088292381878, 0, 0.185694929179}, // bkg error for CT10_nom
    {0.111230824282, 0.462081793096, 0.0975843837009, 0, 0.198637175933}, // bkg error for CT10_pdfup
    {0.0995412715042, 0.506136119673, 0.0833208500129, 0, 0.174993040682}, // bkg error for CT10_pdfdown
    {0.104896323332, 0.487690699466, 0.0866648199766, 0, 0.189066564151}, // bkg error for MSTW_nom
    {0.108943871217, 0.471114685485, 0.0874028863754, 0, 0.196842972481}, // bkg error for MSTW_pdfup
    {0.10236371942, 0.50114712153, 0.0812027187363, 0, 0.188747056115}, // bkg error for MSTW_pdfdown
    {0.102410543364, 0.496088356318, 0.083502864763, 0, 0.183884335303}, // bkg error for NNPDF_nom
    {0.108646998903, 0.467279359104, 0.0925967028263, 0, 0.195067048014}, // bkg error for NNPDF_pdfup
    {0.0988421728534, 0.510857094608, 0.0822526946667, 0, 0.176028402388}, // bkg error for NNPDF_pdfdown
    {0.0979624945502, 0.515321474438, 0.073779724345, 0, 0.167480450102}, // bkg error for scaleup
    {0.108398956294, 0.532045553364, 0.0700946366173, 0, 0.160976337304}, // bkg error for scaledown
  };
  float fiterrors_comb_extLumi_extBtag[11][5] = {
    {0.0739013415172, 0.465465869686, 0.078490070614, 0.432458085567, 0.0621258763276}, // bkg error for CT10_nom
    {0.0796353685898, 0.428566892826, 0.090950911035, 0.435103553405, 0.0629574417432}, // bkg error for CT10_pdfup
    {0.0701039019112, 0.488312009939, 0.0708568064238, 0.43711151761, 0.0609922366663}, // bkg error for CT10_pdfdown
    {0.0745127436608, 0.460054651877, 0.0764168758694, 0.435410180448, 0.0618880632933}, // bkg error for MSTW_nom
    {0.0782341493623, 0.432058563547, 0.0779329246619, 0.436988306562, 0.0620284244625}, // bkg error for MSTW_pdfup
    {0.072211010775, 0.473627797319, 0.0674083582713, 0.447188106768, 0.0617511371678}, // bkg error for MSTW_pdfdown
    {0.0738939001901, 0.454166222516, 0.0746672442105, 0.391636328584, 0.0623970784146}, // bkg error for NNPDF_nom
    {0.0799710972846, 0.407393972095, 0.0851276557633, 0.41958715279, 0.0621094398969}, // bkg error for NNPDF_pdfup
    {0.0718589728601, 0.43754562125, 0.0685572372873, 0.390909528978, 0.0636112129686}, // bkg error for NNPDF_pdfdown
    {0.072912219575, 0.452157721558, 0.0662276523962, 0.432030158382, 0.0534507144485}, // bkg error for scaleup
    {0.07805843213, 0.417980831055, 0.0681304415129, 0.467189896857, 0.0503790440233}, // bkg error for scaledown
  };


  // -------------------------------------------------------------------------------------
  // only externalize luminosity

  float fiterrors_mu_extLumi[11][5] = {
    {0.139728638053, 0.587758962716, 0.089614488774, 0.187493775092, 0}, // bkg error for CT10_nom
    {0.146261274645, 0.584641476542, 0.0976914685997, 0.171916043978, 0}, // bkg error for CT10_pdfup
    {0.13447618083, 0.593129000686, 0.0845506908215, 0.204370908917, 0}, // bkg error for CT10_pdfdown
    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0}, //MSTW
    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0}, //NNPDF
    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0},                     //scale up/down
  };
  float fiterrors_el_extLumi[11][5] = {
    {0.107666308332, 0.495241251931, 0.0917709728859, 0, 0.183676945237}, // bkg error for CT10_nom_qcd
    {0.116569466624, 0.47313994249, 0.104417472918, 0, 0.194897773826}, // bkg error for CT10_pdfup_qcd
    {0.102142467713, 0.509762513298, 0.085377199899, 0, 0.174015328632}, // bkg error for CT10_pdfdown_qcd
    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0}, //MSTW
    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0}, //NNPDF
    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0},                     //scale up/down
  };
  float fiterrors_comb_extLumi[11][5] = {
    {0.0764013719724, 0.505962238523, 0.0842880123265, 0.439347847736, 0.0619944601817}, // bkg error for CT10_nom_qcd
    {0.0813135217986, 0.500461926923, 0.103051404796, 0.446697276192, 0.0626115646919}, // bkg error for CT10_pdfup_qcd
    {0.0726738136535, 0.51324228625, 0.0738902940207, 0.44270007131, 0.0611051275899}, // bkg error for CT10_pdfdown_qcd
    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0}, //MSTW
    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0}, //NNPDF
    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0},                     //scale up/down
  };

  // -------------------------------------------------------------------------------------
  // externalize top-tagging 

  float fiterrors_mu_extToptag[11][5] = {
    {0.0561587568931, 0.589002459596, 0.100211854509, 0.223323968988, 0}, // bkg error for CT10_nom_qcd
    {0.0563348122246, 0.584710188569, 0.107073480288, 0.185129543141, 0}, // bkg error for CT10_pdfup_qcd
    {0.0560203026138, 0.596297304913, 0.0953582983249, 0.267864192571, 0}, // bkg error for CT10_pdfdown_qcd
    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0}, //MSTW
    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0}, //NNPDF
    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0},                     //scale up/down
  };
  float fiterrors_el_extToptag[11][5] = {
    {0.0615881259521, 0.470818523792, 0.0700865322464, 0, 0.186913150011}, // bkg error for CT10_nom_qcd
    {0.0619700611052, 0.434503189393, 0.0714167296073, 0, 0.210923257856}, // bkg error for CT10_pdfup_qcd
    {0.0613754790889, 0.495154654305, 0.0700257546827, 0, 0.168050590124}, // bkg error for CT10_pdfdown_qcd
    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0}, //MSTW
    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0}, //NNPDF
    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0},                     //scale up/down
  };
  float fiterrors_comb_extToptag[11][5] = {
    {0.0470788662116, 0.330338932452, 0.0763185781885, 0.408165436954, 0.0636613443404}, // bkg error for CT10_nom_qcd
    {0.0477913605204, 0.2538074885, 0.0818792661251, 0.404294975895, 0.0653129387711}, // bkg error for CT10_pdfup_qcd
    {0.0465130684786, 0.403477108666, 0.0727925792178, 0.421859706648, 0.0620597380683}, // bkg error for CT10_pdfdown_qcd
    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0}, //MSTW
    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0}, //NNPDF
    {0, 0, 0, 0, 0},    {0, 0, 0, 0, 0},                     //scale up/down
  };

  // -------------------------------------------------------------------------------------
  // 2-bin fit

  float fiterrors_mu_extLumi_extBtag_2ptbin[3][5] = {
    {0.144185754146, 0.595267795985, 0.0851145280679, 0.220851193806, 0}, // bkg error for CT10_nom_qcd, low pt(top) bin
    {0.220346227202, 0.48123544188, 0.187707517336, 0.309229966385, 0}, // bkg error for CT10_nom_qcd, high pt(top) bin
    {0.12390394931, 0.506892618336, 0.0853467823414, 0.295793355281, 0}, // bkg error for CT10_nom_qcd, 2 pt(top) bins
  };
  float fiterrors_el_extLumi_extBtag_2ptbin[3][5] = {
    {0.0975309532275, 0.546273272155, 0.130447887546, 0, 0.161579223668}, // bkg error for CT10_nom_qcd, low pt(top) bin
    {0.240678135538, 0.490308567282, 0.144964487797, 0, 0.122943005108}, // bkg error for CT10_nom_qcd, high pt(top) bin
    {0.0926825163495, 0.474877499166, 0.0858181578576, 0, 0.136737870038}, // bkg error for CT10_nom_qcd, 2 pt(top) bins
  };
  float fiterrors_comb_extLumi_extBtag_2ptbin[3][5] = {
    {0.0723820309327, 0.541472047842, 0.0812303488497, 0.497657367747, 0.071454738068}, // bkg error for CT10_nom_qcd, low pt(top) bin
    {0.15197539398, 0.413081154581, 0.166243158779, 0.287880837398, 0.0662488489516}, // bkg error for CT10_nom_qcd, high pt(top) bin
    {0.0672259798079, 0.457061060254, 0.0674990374532, 0.46003974723, 0.0660621052319}, // bkg error for CT10_nom_qcd, 2 pt(top) bins
  };


  cout << "PDF = " << mydir << endl;

  TString pdfs[11] = {"CT10_nom","CT10_pdfup","CT10_pdfdown",
		      "MSTW_nom","MSTW_pdfup","MSTW_pdfdown",
		      "NNPDF_nom","NNPDF_pdfup","NNPDF_pdfdown",
		      "scaleup","scaledown"};
  int thispdf = -1;
  for (int ipdf=0; ipdf<11; ipdf++) {
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
  

  // -------------------------------------------------------------------------------------
  // electron-only fits
  if (doElectron && !combined) {

    if (ptbin == "" && extBtag && extLumi) {
      fiterr_tt = fiterrors_el_extLumi_extBtag[thispdf][0];
      fiterr_singletop = fiterrors_el_extLumi_extBtag[thispdf][1];
      fiterr_wjets = fiterrors_el_extLumi_extBtag[thispdf][2];
      fiterr_qcd = fiterrors_el_extLumi_extBtag[thispdf][4];
    }
    else if (ptbin == "" && extLumi) {
      fiterr_tt = fiterrors_el_extLumi[thispdf][0];
      fiterr_singletop = fiterrors_el_extLumi[thispdf][1];
      fiterr_wjets = fiterrors_el_extLumi[thispdf][2];
      fiterr_qcd = fiterrors_el_extLumi[thispdf][4];
    }
    else if (ptbin == "" && extToptag) {
      fiterr_tt = fiterrors_el_extToptag[thispdf - 13][0];
      fiterr_singletop = fiterrors_el_extToptag[thispdf - 13][1];
      fiterr_wjets = fiterrors_el_extToptag[thispdf - 13][2];
      fiterr_qcd = fiterrors_el_extToptag[thispdf - 13][4];
    }

    else if (ptbin == "Low" && extLumi && extBtag) {
      fiterr_tt = fiterrors_el_extLumi_extBtag_2ptbin[0][0];
      fiterr_singletop = fiterrors_el_extLumi_extBtag_2ptbin[0][1];
      fiterr_wjets = fiterrors_el_extLumi_extBtag_2ptbin[0][2];
      fiterr_qcd = fiterrors_el_extLumi_extBtag_2ptbin[0][4];
    }
    else if (ptbin == "High" && extLumi && extBtag) {
      fiterr_tt = fiterrors_el_extLumi_extBtag_2ptbin[1][0];
      fiterr_singletop = fiterrors_el_extLumi_extBtag_2ptbin[1][1];
      fiterr_wjets = fiterrors_el_extLumi_extBtag_2ptbin[1][2];
      fiterr_qcd = fiterrors_el_extLumi_extBtag_2ptbin[1][4];
    }
    else if (ptbin == "2" && extLumi && extBtag) {
      fiterr_tt = fiterrors_el_extLumi_extBtag_2ptbin[2][0];
      fiterr_singletop = fiterrors_el_extLumi_extBtag_2ptbin[2][1];
      fiterr_wjets = fiterrors_el_extLumi_extBtag_2ptbin[2][2];
      fiterr_qcd = fiterrors_el_extLumi_extBtag_2ptbin[2][4];
    }
  }

  // -------------------------------------------------------------------------------------
  // electron channel but combined fit
  else if (doElectron) {
    if (ptbin == "" && extLumi && extBtag) {
      fiterr_tt = fiterrors_comb_extLumi_extBtag[thispdf][0];
      fiterr_singletop = fiterrors_comb_extLumi_extBtag[thispdf][1];
      fiterr_wjets = fiterrors_comb_extLumi_extBtag[thispdf][2];
      fiterr_qcd = fiterrors_comb_extLumi_extBtag[thispdf][4];
    }
    else if (ptbin == "" && extLumi) {
      fiterr_tt = fiterrors_comb_extLumi[thispdf][0];
      fiterr_singletop = fiterrors_comb_extLumi[thispdf][1];
      fiterr_wjets = fiterrors_comb_extLumi[thispdf][2];
      fiterr_qcd = fiterrors_comb_extLumi[thispdf][4];
    }
    else if (ptbin == "" && extToptag) {
      fiterr_tt = fiterrors_comb_extToptag[thispdf][0];
      fiterr_singletop = fiterrors_comb_extToptag[thispdf][1];
      fiterr_wjets = fiterrors_comb_extToptag[thispdf][2];
      fiterr_qcd = fiterrors_comb_extToptag[thispdf][4];
    }

    else if (ptbin == "Low" && extLumi && extBtag) {
      fiterr_tt = fiterrors_comb_extLumi_extBtag_2ptbin[0][0];
      fiterr_singletop = fiterrors_comb_extLumi_extBtag_2ptbin[0][1];
      fiterr_wjets = fiterrors_comb_extLumi_extBtag_2ptbin[0][2];
      fiterr_qcd = fiterrors_comb_extLumi_extBtag_2ptbin[0][4];
    }
    else if (ptbin == "High" && extLumi && extBtag) {
      fiterr_tt = fiterrors_comb_extLumi_extBtag_2ptbin[1][0];
      fiterr_singletop = fiterrors_comb_extLumi_extBtag_2ptbin[1][1];
      fiterr_wjets = fiterrors_comb_extLumi_extBtag_2ptbin[1][2];
      fiterr_qcd = fiterrors_comb_extLumi_extBtag_2ptbin[1][4];
    }
    else if (ptbin == "2" && extLumi && extBtag) {
      fiterr_tt = fiterrors_comb_extLumi_extBtag_2ptbin[2][0];
      fiterr_singletop = fiterrors_comb_extLumi_extBtag_2ptbin[2][1];
      fiterr_wjets = fiterrors_comb_extLumi_extBtag_2ptbin[2][2];
      fiterr_qcd = fiterrors_comb_extLumi_extBtag_2ptbin[2][4];
    }
  }

  // -------------------------------------------------------------------------------------
  // muon-only fit
  else if (!doElectron && !combined) {
    if (ptbin == "" && extLumi && extBtag){
      fiterr_tt = fiterrors_mu_extLumi_extBtag[thispdf][0];
      fiterr_singletop = fiterrors_mu_extLumi_extBtag[thispdf][1];
      fiterr_wjets = fiterrors_mu_extLumi_extBtag[thispdf][2];
      fiterr_qcd = fiterrors_mu_extLumi_extBtag[thispdf][3];
    }
    else if (ptbin == "" && extLumi){
      fiterr_tt = fiterrors_mu_extLumi[thispdf][0];
      fiterr_singletop = fiterrors_mu_extLumi[thispdf][1];
      fiterr_wjets = fiterrors_mu_extLumi[thispdf][2];
      fiterr_qcd = fiterrors_mu_extLumi[thispdf][3];
    }
    else if (ptbin == "" && extToptag){
      fiterr_tt = fiterrors_mu_extToptag[thispdf][0];
      fiterr_singletop = fiterrors_mu_extToptag[thispdf][1];
      fiterr_wjets = fiterrors_mu_extToptag[thispdf][2];
      fiterr_qcd = fiterrors_mu_extToptag[thispdf][3];
    }

    else if (ptbin == "Low" && extLumi && extBtag) {
      fiterr_tt = fiterrors_mu_extLumi_extBtag_2ptbin[0][0];
      fiterr_singletop = fiterrors_mu_extLumi_extBtag_2ptbin[0][1];
      fiterr_wjets = fiterrors_mu_extLumi_extBtag_2ptbin[0][2];
      fiterr_qcd = fiterrors_mu_extLumi_extBtag_2ptbin[0][3];
    }
    else if (ptbin == "High" && extLumi && extBtag) {
      fiterr_tt = fiterrors_mu_extLumi_extBtag_2ptbin[1][0];
      fiterr_singletop = fiterrors_mu_extLumi_extBtag_2ptbin[1][1];
      fiterr_wjets = fiterrors_mu_extLumi_extBtag_2ptbin[1][2];
      fiterr_qcd = fiterrors_mu_extLumi_extBtag_2ptbin[1][3];
    }
    else if (ptbin == "2" && extLumi && extBtag) {
      fiterr_tt = fiterrors_mu_extLumi_extBtag_2ptbin[2][0];
      fiterr_singletop = fiterrors_mu_extLumi_extBtag_2ptbin[2][1];
      fiterr_wjets = fiterrors_mu_extLumi_extBtag_2ptbin[2][2];
      fiterr_qcd = fiterrors_mu_extLumi_extBtag_2ptbin[2][3];
    }
  }

  // -------------------------------------------------------------------------------------
  // muon channel but combined fit
  else {
    if (ptbin == "" && extLumi && extBtag) {
      fiterr_tt = fiterrors_comb_extLumi_extBtag[thispdf][0];
      fiterr_singletop = fiterrors_comb_extLumi_extBtag[thispdf][1];
      fiterr_wjets = fiterrors_comb_extLumi_extBtag[thispdf][2];
      fiterr_qcd = fiterrors_comb_extLumi_extBtag[thispdf][3];
    }
    else if (ptbin == "" && extLumi) {
      fiterr_tt = fiterrors_comb_extLumi[thispdf][0];
      fiterr_singletop = fiterrors_comb_extLumi[thispdf][1];
      fiterr_wjets = fiterrors_comb_extLumi[thispdf][2];
      fiterr_qcd = fiterrors_comb_extLumi[thispdf][3];
    }
    else if (ptbin == "" && extToptag) {
      fiterr_tt = fiterrors_comb_extToptag[thispdf][0];
      fiterr_singletop = fiterrors_comb_extToptag[thispdf][1];
      fiterr_wjets = fiterrors_comb_extToptag[thispdf][2];
      fiterr_qcd = fiterrors_comb_extToptag[thispdf][3];
    }

    else if (ptbin == "Low" && extLumi && extBtag) {
      fiterr_tt = fiterrors_comb_extLumi_extBtag_2ptbin[0][0];
      fiterr_singletop = fiterrors_comb_extLumi_extBtag_2ptbin[0][1];
      fiterr_wjets = fiterrors_comb_extLumi_extBtag_2ptbin[0][2];
      fiterr_qcd = fiterrors_comb_extLumi_extBtag_2ptbin[0][3];
    }
    else if (ptbin == "High" && extLumi && extBtag) {
      fiterr_tt = fiterrors_comb_extLumi_extBtag_2ptbin[1][0];
      fiterr_singletop = fiterrors_comb_extLumi_extBtag_2ptbin[1][1];
      fiterr_wjets = fiterrors_comb_extLumi_extBtag_2ptbin[1][2];
      fiterr_qcd = fiterrors_comb_extLumi_extBtag_2ptbin[1][3];
    }
    else if (ptbin == "2" && extLumi && extBtag) {
      fiterr_tt = fiterrors_comb_extLumi_extBtag_2ptbin[2][0];
      fiterr_singletop = fiterrors_comb_extLumi_extBtag_2ptbin[2][1];
      fiterr_wjets = fiterrors_comb_extLumi_extBtag_2ptbin[2][2];
      fiterr_qcd = fiterrors_comb_extLumi_extBtag_2ptbin[2][3];
    }
  }

  TString append = "";
  if (half) {append = "_half";}

  // pre-fit & data files
  TFile* fDATA[3];
  
  if (doElectron) {
    fDATA[0] = new TFile("NormalizedHists_"+mydir+"/normalized2d_eljets_etaAbsLep6"+ptbin+"_subtracted_from_etaAbsLep4"+ptbin+append+".root");
    fDATA[1] = new TFile("NormalizedHists_"+mydir+"/normalized2d_eljets_etaAbsLep7"+ptbin+"_subtracted_from_etaAbsLep6"+ptbin+append+".root");
    fDATA[2] = new TFile("NormalizedHists_"+mydir+"/normalized2d_eljets_vtxMass7"+ptbin+append+".root");

    if (useHTlep == "467" || useHTlep == "46" || useHTlep == "6") fDATA[1] = new TFile("NormalizedHists_"+mydir+"/normalized2d_eljets_htLep7"+ptbin+"_subtracted_from_htLep6"+ptbin+append+".root");
    if (useHTlep == "467" || useHTlep == "46") fDATA[0] = new TFile("NormalizedHists_"+mydir+"/normalized2d_eljets_htLep6"+ptbin+"_subtracted_from_htLep4"+ptbin+append+".root");
    if (useHTlep == "467") fDATA[2] = new TFile("NormalizedHists_"+mydir+"/normalized2d_eljets_htLep7"+ptbin+append+".root");
    if (do_htlep150qcd) fDATA[0] = new TFile("NormalizedHists_"+mydir+"/normalized2d_eljets_etaAbsLep6"+ptbin+"_subtracted_from_etaAbsLep5"+ptbin+append+".root");
  }
  
  else {
    fDATA[0] = new TFile("NormalizedHists_"+mydir+"/normalized2d_mujets_etaAbsLep6"+ptbin+"_subtracted_from_etaAbsLep4"+ptbin+append+".root");
    fDATA[1] = new TFile("NormalizedHists_"+mydir+"/normalized2d_mujets_etaAbsLep7"+ptbin+"_subtracted_from_etaAbsLep6"+ptbin+append+".root");
    fDATA[2] = new TFile("NormalizedHists_"+mydir+"/normalized2d_mujets_vtxMass7"+ptbin+append+".root");

    if (useHTlep == "6" || useHTlep == "46" || useHTlep == "467") fDATA[1] = new TFile("NormalizedHists_"+mydir+"/normalized2d_mujets_htLep7"+ptbin+"_subtracted_from_htLep6"+ptbin+append+".root");
    if (useHTlep == "46" || useHTlep == "467") fDATA[0] = new TFile("NormalizedHists_"+mydir+"/normalized2d_mujets_htLep6"+ptbin+"_subtracted_from_htLep4"+ptbin+append+".root");
    if (useHTlep == "467") fDATA[2] = new TFile("NormalizedHists_"+mydir+"/normalized2d_mujets_htLep7"+ptbin+append+".root");
    if (do_htlep150qcd) fDATA[0] = new TFile("NormalizedHists_"+mydir+"/normalized2d_mujets_etaAbsLep6"+ptbin+"_subtracted_from_etaAbsLep5"+ptbin+append+".root");
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
  //else if (do_qcd) mydir += "_qcd"; // --> this is now the default!
 
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
    wjets[is]->hist()->Rebin(rebinAll[2]);
    singletop[is]->hist()->Rebin(rebinAll[2]);
    ttbar_semiLep[is]->hist()->Rebin(rebinAll[2]);
    ttbar_nonSemiLep[is]->hist()->Rebin(rebinAll[2]);
    ttbar[is]->Rebin(rebinAll[2]);  
  }

  // QCD
  SummedHist* qcd = getQCD( hist, doElectron, ptbin );
  qcd->hist()->Rebin(rebinAll[2]);    

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
    if (doElectron) filepath = "histfiles/qcd_el/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
    else filepath = "histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  }

  TFile* dataFile = TFile::Open(filepath);
  TH1F* data = (TH1F*) dataFile->Get( hist );
  data->SetName(channel + hist + "__DATA");
  data->Rebin(rebinAll[2]);  

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
  //else if (do_qcd) mydir += "_qcd"; // --> this is now the default!
 
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
      wjets[is][ih]->hist()->Rebin(rebinAll[ih]);
      singletop[is][ih]->hist()->Rebin(rebinAll[ih]);
      ttbar_semiLep[is][ih]->hist()->Rebin(rebinAll[ih]);
      ttbar_nonSemiLep[is][ih]->hist()->Rebin(rebinAll[ih]);
      ttbar[is][ih]->Rebin(rebinAll[ih]); 
    }
  }

  // QCD
  SummedHist* qcd[2];
  qcd[0] = getQCD( hist[0], doElectron, ptbin );
  qcd[1] = getQCD( hist[1], doElectron, ptbin );
  qcd[0]->hist()->Rebin(rebinAll[0]);
  qcd[1]->hist()->Rebin(rebinAll[1]);

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
    if (doElectron) filepath = "histfiles/qcd_el/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root";
    else filepath = "histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  }

  TFile* dataFile = TFile::Open(filepath);

  TH1F* data[2];
  data[0] = (TH1F*) dataFile->Get( hist[0] );
  data[0]->SetName(channel + hist[0] + "__DATA");
  data[0]->Rebin(rebinAll[0]);
  data[1] = (TH1F*) dataFile->Get( hist[1] );
  data[1]->SetName(channel + hist[1] + "__DATA_2");
  data[1]->Rebin(rebinAll[1]);
  
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

