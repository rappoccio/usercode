#include "makeThetaInputs.h"

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
    //gStyle->SetTitleFontSize(0.05);
  gStyle->SetTitleFont(43, "XYZ");
  gStyle->SetTitleSize(30, "XYZ");
  gStyle->SetTitleOffset(2.0, "X");
  gStyle->SetTitleOffset(1.25, "Y");
  gStyle->SetLabelFont(43, "XYZ");
  gStyle->SetLabelSize(20, "XYZ");
}


void makeThetaInputs() {

  setStyle();

  double nqcd = 384.1; 
  TString var = "ht4";
  TString title = ";H_{T} (GeV);Events";



  SummedHist * wjets_nom     = getWJets( "nom", var );
  SummedHist * singletop_nom = getSingleTop( "nom", var );
  SummedHist * ttbar_nom     = getTTbar("nom", var );
  SummedHist * ttbar_nonSemiLep_nom     = getTTbarNonSemiLep("nom", var );

  SummedHist * wjets_btagdn     = getWJets( "btagdn", var );
  SummedHist * singletop_btagdn = getSingleTop( "btagdn", var );
  SummedHist * ttbar_btagdn     = getTTbar("btagdn", var );  
  SummedHist * ttbar_nonSemiLep_btagdn     = getTTbarNonSemiLep("btagdn", var );

  SummedHist * wjets_btagup     = getWJets( "btagup", var );
  SummedHist * singletop_btagup = getSingleTop( "btagup", var );
  SummedHist * ttbar_btagup     = getTTbar("btagup", var );  
  SummedHist * ttbar_nonSemiLep_btagup     = getTTbarNonSemiLep("btagup", var );

  SummedHist * wjets_jecdn     = getWJets( "jecdn", var );
  SummedHist * singletop_jecdn = getSingleTop( "jecdn", var );
  SummedHist * ttbar_jecdn     = getTTbar("jecdn", var );  
  SummedHist * ttbar_nonSemiLep_jecdn     = getTTbarNonSemiLep("jecdn", var );

  SummedHist * wjets_jecup     = getWJets( "jecup", var );
  SummedHist * singletop_jecup = getSingleTop( "jecup", var );
  SummedHist * ttbar_jecup     = getTTbar("jecup", var );  
  SummedHist * ttbar_nonSemiLep_jecup     = getTTbarNonSemiLep("jecup", var );

  SummedHist * wjets_jerdn     = getWJets( "jerdn", var );
  SummedHist * singletop_jerdn = getSingleTop( "jerdn", var );
  SummedHist * ttbar_jerdn     = getTTbar("jerdn", var );  
  SummedHist * ttbar_nonSemiLep_jerdn     = getTTbarNonSemiLep("jerdn", var );

  SummedHist * wjets_jerup     = getWJets( "jerup", var );
  SummedHist * singletop_jerup = getSingleTop( "jerup", var );
  SummedHist * ttbar_jerup     = getTTbar("jerup", var );  
  SummedHist * ttbar_nonSemiLep_jerup     = getTTbarNonSemiLep("jerup", var );

  SummedHist * wjets_toptagdn     = getWJets( "toptagdn", var );
  SummedHist * singletop_toptagdn = getSingleTop( "toptagdn", var );
  SummedHist * ttbar_toptagdn     = getTTbar("toptagdn", var );  
  SummedHist * ttbar_nonSemiLep_toptagdn     = getTTbarNonSemiLep("toptagdn", var );

  SummedHist * wjets_toptagup     = getWJets( "toptagup", var );
  SummedHist * singletop_toptagup = getSingleTop( "toptagup", var );
  SummedHist * ttbar_toptagup     = getTTbar("toptagup", var );  
  SummedHist * ttbar_nonSemiLep_toptagup     = getTTbarNonSemiLep("toptagup", var );

  SummedHist * ttbar_pdfup_CT10     = getTTbar("pdfup_CT10", var );  
  SummedHist * ttbar_pdfdn_CT10     = getTTbar("pdfdn_CT10", var );  

  SummedHist * ttbar_pdfup_MSTW     = getTTbar("pdfup_MSTW", var );  
  SummedHist * ttbar_pdfdn_MSTW     = getTTbar("pdfdn_MSTW", var );  

  SummedHist * ttbar_pdfup_NNPDF     = getTTbar("pdfup_NNPDF", var );  
  SummedHist * ttbar_pdfdn_NNPDF     = getTTbar("pdfdn_NNPDF", var );  


  SummedHist * ttbar_scaleup     = getTTbar("scaleup_nom", var );  
  SummedHist * ttbar_scaledown     = getTTbar("scaledown_nom", var );  

  SummedHist * qcd = getQCD( var, nqcd );
  
  TFile * dataFile = TFile::Open("histfiles/SingleMu_iheartNY_V1_mu_Run2012_nom.root");
  TH1F * data = (TH1F*)dataFile->Get( var );
  data->SetName( var + "__DATA" );

  TString outname ("normalized_mujets_");
  outname += var; outname += ".root";
  TFile * fout = new TFile( outname.Data() , "RECREATE");

  fout->cd();

  wjets_nom->hist()->Write();
  singletop_nom->hist()->Write();
  ttbar_nom->hist()->Write();
  ttbar_nonSemiLep_nom->hist()->Write();

  wjets_btagdn->hist()->Write();
  singletop_btagdn->hist()->Write();
  ttbar_btagdn->hist()->Write();
  ttbar_nonSemiLep_btagdn->hist()->Write();

  wjets_btagup->hist()->Write();
  singletop_btagup->hist()->Write();
  ttbar_btagup->hist()->Write();
  ttbar_nonSemiLep_btagup->hist()->Write();

  wjets_toptagdn->hist()->Write();
  singletop_toptagdn->hist()->Write();
  ttbar_toptagdn->hist()->Write();
  ttbar_nonSemiLep_toptagdn->hist()->Write();

  wjets_toptagup->hist()->Write();
  singletop_toptagup->hist()->Write();
  ttbar_toptagup->hist()->Write();
  ttbar_nonSemiLep_toptagup->hist()->Write();


  wjets_jecdn->hist()->Write();
  singletop_jecdn->hist()->Write();
  ttbar_jecdn->hist()->Write();
  ttbar_nonSemiLep_jecdn->hist()->Write();

  wjets_jecup->hist()->Write();
  singletop_jecup->hist()->Write();
  ttbar_jecup->hist()->Write();
  ttbar_nonSemiLep_jecup->hist()->Write();

  wjets_jerdn->hist()->Write();
  singletop_jerdn->hist()->Write();
  ttbar_jerdn->hist()->Write();
  ttbar_nonSemiLep_jerdn->hist()->Write();

  wjets_jerup->hist()->Write();
  singletop_jerup->hist()->Write();
  ttbar_jerup->hist()->Write();
  ttbar_nonSemiLep_jerup->hist()->Write();


  
  ttbar_pdfup_CT10->hist()->Write();
  ttbar_pdfdn_CT10->hist()->Write();

  ttbar_pdfup_MSTW->hist()->Write();
  ttbar_pdfdn_MSTW->hist()->Write();

  ttbar_pdfup_NNPDF->hist()->Write();
  ttbar_pdfdn_NNPDF->hist()->Write();


  ttbar_scaleup->hist()->Write();
  ttbar_scaledown->hist()->Write();

  qcd->hist()->Write();

  data->Write();



  fout->Close();
  
}

