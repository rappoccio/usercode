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

void plotOne(TString what);

void SetPlotStyle();
void mySmallText(Double_t x,Double_t y,Color_t color,char *text); 
void myItalicText(Double_t x,Double_t y,Color_t color,char *text); 


void plotTruth() {

  count();

  const int n = 6;
  TString what[n] = { "ttbar_mass_all",  "ttbar_pt_all",
		      "hadtop_mass_all", "hadtop_pt_all",
		      "leptop_mass_all", "leptop_pt_all" };

  for (int i=0; i<n; i++) {
    plotOne(what[i]);
  }

}

void count() {

  // full truth ntuples
  TFile* f1 = new TFile("ttbar_max700.root");
  TFile* f2 = new TFile("ttbar_700to1000.root");
  TFile* f3 = new TFile("ttbar_1000toInf.root");
  TH1F* h1 = (TH1F*) f1->Get("hadtop_pt_pt400");
  TH1F* h2 = (TH1F*) f2->Get("hadtop_pt_pt400");
  TH1F* h3 = (TH1F*) f3->Get("hadtop_pt_pt400");
  h1->Sumw2();
  h2->Sumw2();
  h3->Sumw2();

  // ntuples with selection
  TFile* ff1 = new TFile("histfiles_CT10_nom/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_2Dcut_nom_notrig.root");
  TFile* ff2 = new TFile("histfiles_CT10_nom/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_2Dcut_nom_notrig.root");
  TFile* ff3 = new TFile("histfiles_CT10_nom/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_2Dcut_nom_notrig.root");
  //TFile* ff1 = new TFile("histfiles_CT10_nom/2Dhists/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_2Dcut_nom.root");
  //TFile* ff2 = new TFile("histfiles_CT10_nom/2Dhists/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_2Dcut_nom.root");
  //TFile* ff3 = new TFile("histfiles_CT10_nom/2Dhists/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_2Dcut_nom.root");
  TH1F* hh1 = (TH1F*) ff1->Get("ptGenTop");
  TH1F* hh2 = (TH1F*) ff2->Get("ptGenTop");
  TH1F* hh3 = (TH1F*) ff3->Get("ptGenTop");
  hh1->Sumw2();
  hh2->Sumw2();
  hh3->Sumw2();


  float ttbar_xs = 245.8*1000;
  float lumi = 19.7;

  float n_ttbar1 = 21675970.;
  float n_ttbar2 = 3082812.;
  float n_ttbar3 = 1249111.;

  float eff_ttbar1 = 1.0;
  float eff_ttbar2 = 0.074;
  float eff_ttbar3 = 0.015;

  h1->Scale(ttbar_xs*lumi*eff_ttbar1/n_ttbar1);
  h2->Scale(ttbar_xs*lumi*eff_ttbar2/n_ttbar2);
  h3->Scale(ttbar_xs*lumi*eff_ttbar3/n_ttbar3);

  hh1->Scale(ttbar_xs*lumi*eff_ttbar1/n_ttbar1);
  hh2->Scale(ttbar_xs*lumi*eff_ttbar2/n_ttbar2);
  hh3->Scale(ttbar_xs*lumi*eff_ttbar3/n_ttbar3);

  float n_pt400 = h1->GetSum()+h2->GetSum()+h3->GetSum();

  float nold_pt400 = hh1->GetSum()-hh1->GetBinContent(0)-hh1->GetBinContent(1)+
    hh2->GetSum()-hh2->GetBinContent(0)-hh2->GetBinContent(1)+
    hh3->GetSum()-hh3->GetBinContent(0)-hh3->GetBinContent(1);

  cout << endl << "semilep ttbar with hadtop > 400 GeV (full truth ntuples): " << n_pt400 << endl;
  cout << "semilep ttbar with hadtop > 400 GeV (no-trigger ntuples): " << nold_pt400 << endl << endl;

}

void plotOne(TString what) {

  SetPlotStyle();

  bool logscale = false; 


  TFile* f1 = new TFile("ttbar_max700.root");
  TFile* f2 = new TFile("ttbar_700to1000.root");
  TFile* f3 = new TFile("ttbar_1000toInf.root");
  TH1F* h1 = (TH1F*) f1->Get(what);
  TH1F* h2 = (TH1F*) f2->Get(what);
  TH1F* h3 = (TH1F*) f3->Get(what);

  h1->Sumw2();
  h2->Sumw2();
  h3->Sumw2();

  float ttbar_xs = 245.8;
  float lumi = 19.7*1000;

  float n_ttbar1 = 21675970.;
  float n_ttbar2 = 3082812.;
  float n_ttbar3 = 1249111.;

  float eff_ttbar1 = 1.0;
  float eff_ttbar2 = 0.074;
  float eff_ttbar3 = 0.015;

  h1->Scale(ttbar_xs*lumi*eff_ttbar1/n_ttbar1);
  h2->Scale(ttbar_xs*lumi*eff_ttbar2/n_ttbar2);
  h3->Scale(ttbar_xs*lumi*eff_ttbar3/n_ttbar3);


  h1->SetFillColor(kYellow-9);
  h2->SetFillColor(kRed);
  h3->SetFillColor(kMagenta+3);


  TH1F* h_dummy = (TH1F*) h1->Clone("dummy");
  h_dummy->SetLineColor(0);
  h_dummy->SetFillColor(0);
  h_dummy->SetMarkerColor(0);
  h_dummy->GetYaxis()->SetTitleOffset(1.1);


  if (what.Contains("ttbar_mass")) {
    h_dummy->GetXaxis()->SetTitle("Mass(t#bar{t}) [GeV]");
    h_dummy->GetYaxis()->SetTitle("Events / 10 GeV");
  }
  else if (what.Contains("ttbar_pt")) {
    h_dummy->GetXaxis()->SetTitle("p_{T}(t#bar{t}) [GeV]");
    h_dummy->GetYaxis()->SetTitle("Events / 5 GeV");
  }
  else if (what.Contains("hadtop_mass")) {
    h_dummy->GetXaxis()->SetTitle("Mass(hadronic top) [GeV]");
    h_dummy->GetYaxis()->SetTitle("Events / 1 GeV");
    h_dummy->SetAxisRange(50,300,"X");
    logscale = true;
  }
  else if (what.Contains("hadtop_pt")) {
    h_dummy->GetXaxis()->SetTitle("p_{T}(hadronic top) [GeV]");
    h_dummy->GetYaxis()->SetTitle("Events / 5 GeV");
  }
  else if (what.Contains("leptop_mass")) {
    h_dummy->GetXaxis()->SetTitle("Mass(leptonic top) [GeV]");
    h_dummy->GetYaxis()->SetTitle("Events / 1 GeV");
    h_dummy->SetAxisRange(50,300,"X");
    logscale = true;
  }
  else if (what.Contains("leptop_pt")) {
    h_dummy->GetXaxis()->SetTitle("p_{T}(leptonic top) [GeV]");
    h_dummy->GetYaxis()->SetTitle("Events / 5 GeV");
  }

  THStack* hs = new THStack();
  hs->Add(h1);
  hs->Add(h2);
  hs->Add(h3);

  float max = hs->GetMaximum();
  if (logscale) h_dummy->SetAxisRange(1,max*1.5,"Y");
  else h_dummy->SetAxisRange(0,max*1.05,"Y");


  TCanvas c;
  if (logscale) gPad->SetLogy();
  h_dummy->Draw("hist");
  hs->Draw("hist,same");
  h_dummy->Draw("same,axis");


  TLegend* l = new TLegend(0.6,0.65,0.85,0.9);
  l->SetFillStyle(0);
  l->SetBorderSize(0);
  l->SetFillColor(0);
  l->SetTextSize(0.04);
  l->AddEntry(h1,"m(t#bar{t}) < 700 GeV","f");
  l->AddEntry(h2,"700 < m(t#bar{t}) < 1000 GeV","f");
  l->AddEntry(h3,"m(t#bar{t}) > 1000 GeV","f");
  l->SetTextFont(42);
  l->Draw();	

  c.SaveAs("truth_"+what+".png");
  
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


