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


void accEff() {

  SetPlotStyle();
  
  /*
  TFile* f1 = new TFile("../histfiles_CT10_nom/2Dhists/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_2Dcut_nom.root");
  TFile* f2 = new TFile("../histfiles_CT10_nom/2Dhists/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_2Dcut_nom.root");
  TFile* f3 = new TFile("../histfiles_CT10_nom/2Dhists/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_2Dcut_nom.root");
  */

  ///*
  TFile* f1 = new TFile("ttbar_max700.root");
  TFile* f2 = new TFile("ttbar_700to1000.root");
  TFile* f3 = new TFile("ttbar_1000toInf.root");
  //*/

  //TString num = "ptRecoTop_passRecoParton";
  //TString den = "ptRecoTop_passReco";
  //TString num = "ptGenTop_passRecoParton";
  //TString den = "ptGenTop_passParton";

  // *** acceptance correction for "_pt400", reco to particle unfolding, (i.e. passParticle & passReco / passReco) ***
  //TString num = "ptRecoTop_passRecoParticle";
  //TString den = "ptRecoTop_passReco";

  // *** acceptance correction for "_pt400", particle to parton unfolding, (i.e. passParticle & passParton / passParticle) ***
  TString num = "ptPartTop_passParticleParton";
  TString den = "ptPartTop_passParticle";

  // *** acceptance correction for "_full" two-step unfolding (i.e. passParticleLoose & passReco / passReco) ***
  //TString num = "ptRecoTop_2step";
  //TString den = "ptRecoTop";


  TH1F* hnum1 = (TH1F*) f1->Get(num);
  TH1F* hnum2 = (TH1F*) f2->Get(num);
  TH1F* hnum3 = (TH1F*) f3->Get(num);
  hnum1->Sumw2();
  hnum2->Sumw2();
  hnum3->Sumw2();

  TH1F* hden1 = (TH1F*) f1->Get(den);
  TH1F* hden2 = (TH1F*) f2->Get(den);
  TH1F* hden3 = (TH1F*) f3->Get(den);
  hden1->Sumw2();
  hden2->Sumw2();
  hden3->Sumw2();

  hnum1->Scale(245.8*1000.*19.7/21675970.); 
  hnum2->Scale(245.8*1000.*0.074*19.7/3082812.); 
  hnum3->Scale(245.8*1000.*0.015*19.7/1249111.); 

  hden1->Scale(245.8*1000.*19.7/21675970.); 
  hden2->Scale(245.8*1000.*0.074*19.7/3082812.); 
  hden3->Scale(245.8*1000.*0.015*19.7/1249111.); 

  hnum1->Add(hnum2);
  hnum1->Add(hnum3);

  hden1->Add(hden2);
  hden1->Add(hden3);


  TH1F* heff = (TH1F*) hnum1->Clone("efficiency");
  heff->Reset();
  heff->Divide(hnum1, hden1, 1.0, 1.0, "B");

  heff->SetTitleOffset(1.1, "X");
  heff->SetTitleOffset(1.2, "Y");

  heff->GetYaxis()->SetTitle("Acceptance correction");
  heff->SetAxisRange(0.0,1.0,"Y");
  //heff->SetAxisRange(0.6,1.05,"Y");
  //heff->SetAxisRange(0.9,1.01,"Y");

  for (int i=1; i<heff->GetNbinsX()+1; i++) {
    cout << "accCorr [" << heff->GetBinLowEdge(i) << "," << heff->GetBinLowEdge(i+1) 
	   << "]: " << heff->GetBinContent(i) << " +/- " << heff->GetBinError(i) << endl;
  }


  TCanvas c;
  heff->Draw("ep");

  /*
  TLegend* leg = new TLegend(0.6,0.7,0.8,0.9);
  leg->SetBorderSize(0);
  leg->SetFillStyle(0);
  leg->SetTextFont(42);
  leg->SetTextSize(0.04);
  leg->AddEntry(h1, "CT10 nominal", "lep");
  leg->AddEntry(hup1, "CT10 PDF up", "lep");
  leg->AddEntry(hdn1, "CT10 PDF down", "lep");
  leg->Draw();
  */

  mySmallText(0.22,0.42,1,"Acceptance correction factor");
  //mySmallText(0.22,0.36,1,"(events passing full selection + loose particle-level cuts");
  mySmallText(0.22,0.36,1,"(events passing full selection + particle-level cuts");
  mySmallText(0.22,0.30,1,"vs events passing full selection)");
  //mySmallText(0.22,0.36,1,"(events passing particle-level & parton selection");
  //mySmallText(0.22,0.30,1,"vs events passing particle-level selection)");

  c.SaveAs("acceptanceCorr.png");
  c.SaveAs("acceptanceCorr.eps");

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


