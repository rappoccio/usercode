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


void plotToys(TString channel, TString syst="CT10_nom") {
  
  SetPlotStyle();

  TString ext = "_nobtag_nolumi";

  TFile* f = new TFile("run_theta/ThetaPlots/pulldists_mle_"+syst+"_"+channel+ext+".root"); 

  TH1F* h_pull = (TH1F*) f->Get("pull");
  TH1F* h_dbs  = (TH1F*) f->Get("delta_bs");


  TCanvas c;
  h_pull->SetLineColor(1);
  h_pull->SetLineWidth(2);
  h_pull->Rebin(2);
  h_pull->GetYaxis()->SetTitleSize(0.052);
  h_pull->GetXaxis()->SetTitleSize(0.052);
  h_pull->GetYaxis()->SetLabelSize(0.045);
  h_pull->GetXaxis()->SetLabelSize(0.045);
  h_pull->GetYaxis()->SetTitleOffset(1.0);
  h_pull->GetYaxis()->SetTitle("# pseudo experiments");
  h_pull->GetXaxis()->SetTitle("Pull");
  h_pull->Draw();

  mySmallText(0.22,0.84,1,"Pull = (1 - #beta_{signal})/#sigma(#beta_{signal})");
  mySmallText(0.22,0.74,1,"Extracted from 1000");
  mySmallText(0.22,0.69,1,"pseudo experiments.");
  
  float mean = h_pull->GetMean();
  float rms = h_pull->GetRMS();

  char ctxt[500];
  sprintf(ctxt,"Mean = %.2f",mean);
  mySmallText(0.22,0.59,1,ctxt);
  sprintf(ctxt,"RMS = %.2f",rms);
  mySmallText(0.22,0.54,1,ctxt);

  c.SaveAs("pull_"+syst+"_"+channel+ext+".png");
  c.SaveAs("pull_"+syst+"_"+channel+ext+".pdf");


  h_dbs->SetLineColor(1);
  h_dbs->SetLineWidth(2);
  h_dbs->GetYaxis()->SetTitleSize(0.052);
  h_dbs->GetXaxis()->SetTitleSize(0.052);
  h_dbs->GetYaxis()->SetLabelSize(0.045);
  h_dbs->GetXaxis()->SetLabelSize(0.045);
  h_dbs->SetAxisRange(0,0.5,"X");
  h_dbs->GetYaxis()->SetTitleOffset(1.0);
  h_dbs->GetYaxis()->SetTitle("# pseudo experiments");
  h_dbs->GetXaxis()->SetTitle("#sigma(#beta_{signal})");
  h_dbs->Draw();

  mySmallText(0.5,0.82,1,"A priori measurement uncertainty");
  mySmallText(0.5,0.77,1,"from 1000 pseudo experiments.");

  float mean = h_dbs->GetMean();
  float rms = h_dbs->GetRMS();

  char ctxt[500];
  sprintf(ctxt,"Mean = %.2f, RMS = %.2f",mean,rms);
  mySmallText(0.5,0.67,1,ctxt);

  c.SaveAs("delta_beta_signal_"+syst+"_"+channel+ext+".png");
  c.SaveAs("delta_beta_signal_"+syst+"_"+channel+ext+".pdf");

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
  //gStyle->SetPadTopMargin(0.05);
  //gStyle->SetPadRightMargin(0.05);
  //gStyle->SetPadBottomMargin(0.16);
  //gStyle->SetPadLeftMargin(0.16);

  gStyle->SetPadTopMargin(0.07);
  gStyle->SetPadRightMargin(0.05);
  gStyle->SetPadBottomMargin(0.16);
  gStyle->SetPadLeftMargin(0.18);
  
  // set title offsets (for axis label)
  gStyle->SetTitleXOffset(1.4);
  gStyle->SetTitleYOffset(1.2);
  
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
  Double_t tsize = 0.04;
  TLatex l;
  l.SetTextSize(tsize); 
  l.SetNDC();
  l.SetTextColor(color);
  l.DrawLatex(x,y,text);
}
