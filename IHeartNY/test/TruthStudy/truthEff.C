#include "TROOT.h"
#include "TStyle.h"
#include "TLatex.h"
#include "TFile.h"
#include "TTree.h"
#include "TChain.h"
#include "TBranch.h"
#include "TLeaf.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TH1.h"
#include "TH2.h"
#include "TF1.h"
#include "TProfile.h"
#include "TProfile2D.h"
#include "TMath.h"

#include <iostream>
#include <string>
#include <vector>

using namespace std;


void SetPlotStyle();
void mySmallText(Double_t x,Double_t y,Color_t color,char *text); 
void myItalicText(Double_t x,Double_t y,Color_t color,char *text); 


void truthEff() {

  SetPlotStyle();

  // full truth samlpes (aka denominator)
  TFile* f_true0    = new TFile("ttbar_max700.root");
  TFile* f_true700  = new TFile("ttbar_700to1000.root");
  TFile* f_true1000 = new TFile("ttbar_1000toInf.root");

  TH1F* h_true0    = (TH1F*) f_true0->Get("hadtop_pt_pt400");
  TH1F* h_true700  = (TH1F*) f_true700->Get("hadtop_pt_pt400");
  TH1F* h_true1000 = (TH1F*) f_true1000->Get("hadtop_pt_pt400");
  h_true0->Sumw2();
  h_true700->Sumw2();
  h_true1000->Sumw2();

  // default samples with trigger (aka numerator) 
  TFile* f_trig0    = new TFile("../histfiles_CT10_nom/2Dhists/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_2Dcut_nom.root");
  TFile* f_trig700  = new TFile("../histfiles_CT10_nom/2Dhists/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_2Dcut_nom.root");
  TFile* f_trig1000 = new TFile("../histfiles_CT10_nom/2Dhists/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_2Dcut_nom.root");

  TH1F* h_trig0    = (TH1F*) f_trig0->Get("ptGenTop");
  TH1F* h_trig700  = (TH1F*) f_trig700->Get("ptGenTop");
  TH1F* h_trig1000 = (TH1F*) f_trig1000->Get("ptGenTop");
  h_trig0->Sumw2();
  h_trig700->Sumw2();
  h_trig1000->Sumw2();


  // normalize to be able to switch together the three mass ranges
  float ttbar_xs = 245.8;
  float lumi = 19.7*1000;

  float n_ttbar0 = 21675970.;
  float n_ttbar700 = 3082812.;
  float n_ttbar1000 = 1249111.;

  float eff_ttbar0 = 1.0;
  float eff_ttbar700 = 0.074;
  float eff_ttbar1000 = 0.015;

  h_true0->Scale(ttbar_xs*lumi*eff_ttbar0/n_ttbar0);
  h_true700->Scale(ttbar_xs*lumi*eff_ttbar700/n_ttbar700);
  h_true1000->Scale(ttbar_xs*lumi*eff_ttbar1000/n_ttbar1000);
  h_true0->Add(h_true700);
  h_true0->Add(h_true1000);

  h_trig0->Scale(ttbar_xs*lumi*eff_ttbar0/n_ttbar0);
  h_trig700->Scale(ttbar_xs*lumi*eff_ttbar700/n_ttbar700);
  h_trig1000->Scale(ttbar_xs*lumi*eff_ttbar1000/n_ttbar1000);
  h_trig0->Add(h_trig700);
  h_trig0->Add(h_trig1000);


  float ptbins[7] = {300.0,400.0,500.0,600.0,700.0,800.0,1300.0};

  TH1F* h_true = (TH1F*) h_trig0->Clone("trig");
  h_true->Clear();


  for (int ibb=0; ibb<6; ibb++) {
    
    float bin_content = 0.0;
    float bin_error = 0.0;

    for (int ib=1; ib<(int)h_true0->GetNbinsX(); ib++) {

      if (h_true0->GetBinLowEdge(ib) >= ptbins[ibb] && h_true0->GetBinLowEdge(ib+1) <= ptbins[ibb+1]) {
	bin_content += h_true0->GetBinContent(ib);
	bin_error += h_true0->GetBinError(ib)*h_true0->GetBinError(ib);
      }      	
    }
    
    bin_error = sqrt(bin_error);

    h_true->SetBinContent(ibb+1, bin_content);
    h_true->SetBinError(ibb+1, bin_error);

  }

  TH1F* h_sf = (TH1F*) h_true->Clone("eff");
  h_sf->Clear();
  h_sf->Divide(h_true,h_trig0,1.0,1.0,"B");

  h_sf->GetYaxis()->SetTitleOffset(1.1);
  h_sf->GetYaxis()->SetTitle("Scale factor");

  TCanvas c;
  h_sf->SetAxisRange(1.0,1.5,"Y");
  h_sf->Draw("lep");

  mySmallText(0.22,0.36,1,"Scale factor");
  mySmallText(0.22,0.30,1,"(events passing trigger vs all semileptonic t#bar{t} #rightarrow #mu+jets)");

  for (int i=1; (int)i<h_sf->GetNbinsX()+1; i++) {
    cout << "SF [" << h_sf->GetBinLowEdge(i) << "," << h_sf->GetBinLowEdge(i+1) 
	 << "]: " << h_sf->GetBinContent(i) << " +/- " << h_sf->GetBinError(i) << endl;
  }

  c.SaveAs("truth_eff.png");
  c.SaveAs("truth_eff.eps");
  
}


void SetPlotStyle() {

  // from ATLAS plot style macro

  // use plain black on white colors
  gStyle->SetFrameBorderMode(0);
  gStyle->SetFrameFillColor(0);
  gStyle->SetCanvasBorderMode(0);
  gStyle->SetCanvasColor(0);
  gStyle->SetPadBorderMode(0);
  gStyle->SetPadColor(0);
  gStyle->SetStatColor(0);
  gStyle->SetHistLineColor(1);

  gStyle->SetPalette(1);

  // set the paper & margin sizes
  gStyle->SetPaperSize(20,26);
  gStyle->SetPadTopMargin(0.05);
  gStyle->SetPadRightMargin(0.05);
  gStyle->SetPadBottomMargin(0.16);
  gStyle->SetPadLeftMargin(0.16);

  // set title offsets (for axis label)
  gStyle->SetTitleXOffset(1.4);
  gStyle->SetTitleYOffset(1.4);

  // use large fonts
  gStyle->SetTextFont(42);
  gStyle->SetTextSize(0.05);
  gStyle->SetLabelFont(42,"x");
  gStyle->SetTitleFont(42,"x");
  gStyle->SetLabelFont(42,"y");
  gStyle->SetTitleFont(42,"y");
  gStyle->SetLabelFont(42,"z");
  gStyle->SetTitleFont(42,"z");
  gStyle->SetLabelSize(0.05,"x");
  gStyle->SetTitleSize(0.05,"x");
  gStyle->SetLabelSize(0.05,"y");
  gStyle->SetTitleSize(0.05,"y");
  gStyle->SetLabelSize(0.05,"z");
  gStyle->SetTitleSize(0.05,"z");

  // use bold lines and markers
  gStyle->SetMarkerStyle(20);
  gStyle->SetMarkerSize(1.2);
  gStyle->SetHistLineWidth(2.);
  gStyle->SetLineStyleString(2,"[12 12]");

  // get rid of error bar caps
  gStyle->SetEndErrorSize(0.);

  // do not display any of the standard histogram decorations
  gStyle->SetOptTitle(0);
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(0);

  // put tick marks on top and RHS of plots
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);

}


void mySmallText(Double_t x,Double_t y,Color_t color,char *text) {
  Double_t tsize=0.044;
  TLatex l;
  l.SetTextSize(tsize); 
  l.SetNDC();
  l.SetTextColor(color);
  l.DrawLatex(x,y,text);
}
void myItalicText(Double_t x,Double_t y,Color_t color,char *text) {
  Double_t tsize=0.044;
  TLatex l;
  l.SetTextFont(52);
  l.SetTextSize(tsize); 
  l.SetNDC();
  l.SetTextColor(color);
  l.DrawLatex(x,y,text);
}


