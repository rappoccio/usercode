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


// -------------------------------------------------------------------------------------
// make pretty plots
// -------------------------------------------------------------------------------------

void makePlots_single(TString var, int cut, TString pdfdir="_CT10") {
  
  TH1::AddDirectory(kFALSE); 
  setStyle();

  if ( !(cut==3||cut==4||cut==6||cut==7) ) {
    std::cout << "Not a valid option! Syntax is: " << std::endl
	      << "> makePlots_single(TString var, int cut)" << std::endl
	      << "where cut == 3,4,6,7. Exiting..." << std::endl;
    return;
  }
 
  TString hist = var;
  hist += cut;

  // read QCD normalization
  std::pair<double, double> qcdnorm = getQCDnorm(cut);
  double nqcd = qcdnorm.first;
  double err_qcd = qcdnorm.second; 


  // get histograms
  SummedHist* wjets = getWJets( "nom", hist  );
  SummedHist* singletop = getSingleTop( "nom", hist  );
  SummedHist* ttbar = getTTbar( "nom", hist, pdfdir  );
  SummedHist* ttbar_nonSemiLep = getTTbarNonSemiLep( "nom", hist, pdfdir  );
  SummedHist* qcd = getQCD( hist, nqcd );

  TString filepath;
  if (use2D) filepath = "histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  else filepath = "histfiles/SingleMu_iheartNY_V1_mu_Run2012_nom.root";

  TFile* dataFile = TFile::Open(filepath);
  TH1F* h_data = (TH1F*) dataFile->Get( hist );
  h_data->SetName(hist + "__DATA");
  

  // -------------------------------------------------------------------------------------
  // get the TH1F versions

  TH1F* h_qcd = (TH1F*) qcd->hist();
  TH1F* h_wjets = (TH1F*) wjets->hist();
  TH1F* h_ttbar = (TH1F*) ttbar->hist();
  TH1F* h_ttbar_nonSemiLep = (TH1F*) ttbar_nonSemiLep->hist();
  TH1F* h_singletop = (TH1F*) singletop->hist();


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
    newtitle = "Events / 10 GeV";
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
  h_data->SetMarkerStyle(8);

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
  if (use2D) outname = "NicePlots/normalized2d_nom_mujets_";
  else outname = "NicePlots/normalized_nom_mujets_";

  c->SaveAs(outname+hist+".png");
  c->SaveAs(outname+hist+".eps");
  c->SaveAs(outname+hist+".pdf");


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
    if (use2D) err_qcd_dn = 11.0;
    else err_qcd_dn = 1.0;
    err_tot_dn = err_tt*err_tt + err_tt_nonsemilep*err_tt_nonsemilep + err_singletop*err_singletop + err_wjets*err_wjets + err_qcd_dn*err_qcd_dn;
    err_tot_dn = sqrt(err_tot_dn);
  }

  std::cout << std::endl << "-------------------------------------------------------------------------------------" << std::endl;
  std::cout << "hist: " << hist << std::endl;
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
// make theta histograms without subtracting
// -------------------------------------------------------------------------------------

void makeTheta_single(TString var, int cut, TString pdfdir="_CT10") {
  
  TH1::AddDirectory(kFALSE); 
  setStyle();

  if ( !(cut==3||cut==4||cut==6||cut==7) ) {
    std::cout << "Not a valid option! Syntax is: " << std::endl
	      << "> makeTheta_single(TString var, int cut)" << std::endl
	      << "where cut == 3,4,6,7. Exiting..." << std::endl;
    return;
  }
 
  TString hist = var;
  hist += cut;


  // read QCD normalization
  std::pair<double, double> qcdnorm = getQCDnorm(cut);
  double nqcd = qcdnorm.first;
  //double qcd_err = qcdnorm.second; 


  // systematics for ttbar, non-semilep ttbar, single top, W+jets
  const int nSYST = 9;
  TString name_syst[nSYST] = {"nom", "jecdn", "jecup", "jerdn", "jerup", 
			      "btagdn", "btagup", "toptagdn", "toptagup"};
  SummedHist* wjets[nSYST];
  SummedHist* singletop[nSYST];
  SummedHist* ttbar[nSYST];
  SummedHist* ttbar_nonSemiLep[nSYST];

  for (int is=0; is<nSYST; is++) {
    wjets[is]     = getWJets( name_syst[is], hist  );
    singletop[is] = getSingleTop( name_syst[is], hist  );
    ttbar[is]     = getTTbar( name_syst[is], hist, pdfdir  );
    ttbar_nonSemiLep[is] = getTTbarNonSemiLep( name_syst[is], hist, pdfdir  );
  }

  // QCD
  SummedHist* qcd = getQCD( hist, nqcd );


  // data
  TString filepath;
  if (use2D) filepath = "histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
  else filepath = "histfiles/SingleMu_iheartNY_V1_mu_Run2012_nom.root";

  TFile* dataFile = TFile::Open(filepath);
  TH1F* data = (TH1F*) dataFile->Get( hist );
  data->SetName(hist + "__DATA");
  

  // write the histograms to a file
  TString outname;
  if (use2D) outname = "NormalizedHists/normalized2d_mujets_"+hist+".root";
  else outname = "NormalizedHists/normalized_mujets_"+hist+".root";

  TFile* fout = new TFile(outname, "RECREATE");

  fout->cd();

  for (int is=0; is<nSYST; is++) {
    wjets[is]->hist()->Write();
    singletop[is]->hist()->Write();
    ttbar[is]->hist()->Write();
    ttbar_nonSemiLep[is]->hist()->Write();
  }

  qcd->hist()->Write();
  data->Write();

  fout->Close();

}


// -------------------------------------------------------------------------------------
// make histograms, subtract one from another
// -------------------------------------------------------------------------------------

void makeTheta_subtract(TString var, int cut1, int cut2, TString pdfdir="_CT10") {

  TH1::AddDirectory(kFALSE); 
  setStyle();

  if ( !(cut1==3||cut1==4||cut1==6||cut1==7) ||
       !(cut2==3||cut2==4||cut2==6||cut2==7) ||
       cut2 <= cut1 ) {
    std::cout << "Not a valid option! Syntax is: " << std::endl
	      << "> makeTheta_subtract(TString var, int cut1, int cut2)" << std::endl
	      << "where cut1/2 == 3,4,6,7 and cut1 < cut2. Exiting..." << std::endl;
    return;
  }
 
  TString hist[2] = {var, var};
  hist[0] += cut1;
  hist[1] += cut2;


  // read QCD normalization
  std::pair<double, double> qcdnorm1 = getQCDnorm(cut1);
  std::pair<double, double> qcdnorm2 = getQCDnorm(cut2);
  double nqcd[2] = {qcdnorm1.first, qcdnorm2.first};
  //double qcd_err[2] = {qcdnorm1.second, qcdnorm2.second};

	
  // systematics for ttbar, non-semilep ttbar, single top, W+jets
  const int nSYST = 9;
  TString name_syst[nSYST] = {"nom", "jecdn", "jecup", "jerdn", "jerup", 
			      "btagdn", "btagup", "toptagdn", "toptagup"};

  
  SummedHist* wjets[nSYST][2];
  SummedHist* singletop[nSYST][2];
  SummedHist* ttbar[nSYST][2];
  SummedHist* ttbar_nonSemiLep[nSYST][2];

  for (int ih=0; ih<2; ih++) {
    for (int is=0; is<nSYST; is++) {
      wjets[is][ih]     = getWJets( name_syst[is], hist[ih] );
      singletop[is][ih] = getSingleTop( name_syst[is], hist[ih] );
      ttbar[is][ih]     = getTTbar( name_syst[is], hist[ih], pdfdir );
      ttbar_nonSemiLep[is][ih] = getTTbarNonSemiLep( name_syst[is], hist[ih], pdfdir );
    }
  }

  // QCD
  SummedHist* qcd[2];
  qcd[0] = getQCD( hist[0], nqcd[0] );
  qcd[1] = getQCD( hist[1], nqcd[1] );


  // data
  TString filepath;
  if (use2D) filepath = "histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root";
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
    ttbar[is][0]->hist() ->Add(ttbar[is][1]->hist(), -1);
    ttbar_nonSemiLep[is][0]->hist() ->Add(ttbar_nonSemiLep[is][1]->hist(), -1);
  }
  qcd[0]->hist() ->Add(qcd[1]->hist(), -1);
  data[0]->Add(data[1], -1);


  // write the histograms to a file
  TString outname;
  if (use2D) outname = "NormalizedHists/normalized2d_mujets_"+hist[1]+"_subtracted_from_"+hist[0]+".root";
  else outname = "NormalizedHists/normalized_mujets_"+hist[1]+"_subtracted_from_"+hist[0]+".root";

  TFile* fout = new TFile(outname, "RECREATE");

  fout->cd();

  for (int is=0; is<nSYST; is++) {
    wjets[is][0]->hist()->Write();
    singletop[is][0]->hist()->Write();
    ttbar[is][0]->hist()->Write();
    ttbar_nonSemiLep[is][0]->hist()->Write();
  }

  qcd[0]->hist()->Write();
  data[0]->Write();

  fout->Close();


}

