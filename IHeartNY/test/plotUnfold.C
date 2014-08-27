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


void plotUnfold() {

  SetPlotStyle();


  // ---------------------------------------------------------------------------------------------------------------
  // get files & histograms
  
  const int nSYST = 13;
  TString name_syst[nSYST] = {"CT10_nom_2Dcut_nom",
			      "scaleup_2Dcut_nom",
			      "scaledown_2Dcut_nom",
			      "CT10_pdfup_2Dcut_nom",
			      "CT10_pdfdown_2Dcut_nom",
			      "CT10_nom_2Dcut_jecup",
			      "CT10_nom_2Dcut_jecdn",
			      "CT10_nom_2Dcut_jerup",
			      "CT10_nom_2Dcut_jerdn",			      
			      "CT10_nom_2Dcut_btagup",
			      "CT10_nom_2Dcut_btagdn",
			      "CT10_nom_2Dcut_toptagup",
			      "CT10_nom_2Dcut_toptagdn",

  };

  TFile* f_syst[nSYST];
  TH1F* h_unfolded[nSYST];
  TH1F* h_true;
  TH1F* h_measured;

  cout << "Getting files and hists" << endl;

  for (int is=0; is<nSYST; is++) {
    cout << "getting UnfoldingPlots/unfold_" << name_syst[is] << ".root" <<endl;
    f_syst[is] = new TFile("UnfoldingPlots/unfold_"+name_syst[is]+".root");
    
    if (is==0) {
      h_true = (TH1F*) f_syst[is]->Get("pt_genTop")->Clone();
      h_measured = (TH1F*) f_syst[is]->Get("ptRecoTop")->Clone();
    }

    h_unfolded[is] = (TH1F*) f_syst[is]->Get("UnfoldedData")->Clone();
    h_unfolded[is]->SetName("UnfoldedData_"+name_syst[is]);
  }

  TH1F* h_dummy = (TH1F*) h_measured->Clone("dummy");
  h_dummy->Reset();


  // ----------------------------------------------------------------------------------------------------------------
  // colors and stuff

  h_measured->SetLineColor(1);
  h_measured->SetMarkerColor(1);
  h_measured->SetMarkerStyle(24);
  
  h_true->SetLineColor(2);

  h_unfolded[0]->SetLineColor(1);
  h_unfolded[0]->SetMarkerColor(1);
  h_unfolded[0]->SetMarkerStyle(8);


  float tmp_max = 0;


  // ----------------------------------------------------------------------------------------------------------------
  // systematics for ratio plot
  cout << "Making ratio plots" << endl;
  TH1F* h_systEXP_up = (TH1F*) h_measured->Clone("syst_up_exp");
  TH1F* h_systEXP_dn = (TH1F*) h_measured->Clone("syst_dn_exp");
  h_systEXP_up->Reset();
  h_systEXP_dn->Reset();

  TH1F* h_systTH_up = (TH1F*) h_measured->Clone("syst_up_th");
  TH1F* h_systTH_dn = (TH1F*) h_measured->Clone("syst_dn_th");
  h_systTH_up->Reset();
  h_systTH_dn->Reset();

  float count[nSYST] = {0};
  float sig[nSYST] = {0};

  for (int i=0; i<h_unfolded[0]->GetNbinsX()+1; i++) {
  
    for (int is=0; is<nSYST; is++) {
      count[is] = 0;
      sig[is] = 0;

      count[is] = h_unfolded[is]->GetBinContent(i+1);
      sig[is]   = h_unfolded[is]->GetBinError(i+1);
    }

    cout << "Accessing event counts" << endl;
    float this_systEXP_up = 0;
    this_systEXP_up += (count[5]-count[0])*(count[5]-count[0]);
    this_systEXP_up += (count[7]-count[0])*(count[7]-count[0]);
    this_systEXP_up += (count[9]-count[0])*(count[9]-count[0]);
    this_systEXP_up += (count[11]-count[0])*(count[11]-count[0]);
    this_systEXP_up += sig[0]*sig[0];
    this_systEXP_up = sqrt(this_systEXP_up);

    float this_systEXP_dn = 0;
    this_systEXP_dn += (count[6]-count[0])*(count[6]-count[0]);
    this_systEXP_dn += (count[8]-count[0])*(count[8]-count[0]);
    this_systEXP_dn += (count[10]-count[0])*(count[10]-count[0]);
    this_systEXP_dn += (count[12]-count[0])*(count[12]-count[0]);
    this_systEXP_dn += sig[0]*sig[0];
    this_systEXP_dn = sqrt(this_systEXP_dn);

    float this_systTH_up = 0;
    this_systTH_up += (count[1]-count[0])*(count[1]-count[0]);
    this_systTH_up += (count[3]-count[0])*(count[3]-count[0]);
    this_systTH_up = sqrt(this_systEXP_up);

    float this_systTH_dn = 0;
    this_systTH_dn += (count[2]-count[0])*(count[2]-count[0]);
    this_systTH_dn += (count[4]-count[0])*(count[4]-count[0]);
    this_systTH_dn = sqrt(this_systEXP_dn);

    float upEXP = count[0] + this_systEXP_up;
    float dnEXP = count[0] - this_systEXP_dn;

    h_systEXP_up->SetBinContent(i+1,upEXP);
    h_systEXP_dn->SetBinContent(i+1,dnEXP);  

    float upTH = count[0] + this_systTH_up;
    float dnTH = count[0] - this_systTH_dn;

    h_systTH_up->SetBinContent(i+1,upTH);
    h_systTH_dn->SetBinContent(i+1,dnTH);  
    cout << ".... done" << endl;
  }

  cout << "Done with all bins" << endl;

  h_dummy->GetXaxis()->SetTitle("p_{T} [GeV]");
  h_dummy->GetYaxis()->SetTitle("d#sigma / dp_{T} [fb / GeV]");
  h_dummy->SetAxisRange(400,1400,"X");
  h_dummy->SetAxisRange(0,30,"Y");



  cout << "Making ratio plots" << endl;
  // ----------------------------------------------------------------------------------------------------------------
  // RATIO PLOTS !!!!!!!
  // ----------------------------------------------------------------------------------------------------------------

  Float_t f_textSize=0.057;
  gStyle->SetPadLeftMargin(0.12);
  gStyle->SetPadRightMargin(0.1);
  gStyle->SetTextSize(f_textSize);
  gStyle->SetLabelSize(f_textSize,"x");
  gStyle->SetTitleSize(f_textSize,"x");
  gStyle->SetLabelSize(f_textSize,"y");
  gStyle->SetTitleSize(f_textSize,"y");
  gStyle->SetOptStat(0);
  
  TCanvas *c = new TCanvas("c", "", 700, 625);
  
  float ratio_size = 0.35;
  
  TPad* p1 = new TPad("p1","p1",0,ratio_size+0.0,1,1);
  p1->SetBottomMargin(0.04);
  p1->SetLeftMargin(0.13);
  p1->SetRightMargin(0.075);
  
  TPad* p2 = new TPad("p2","p2",0,0,1,ratio_size-0.0);
  p2->SetTopMargin(0.00);
  p2->SetBottomMargin(0.4);
  p2->SetLeftMargin(0.13);
  p2->SetRightMargin(0.075);
  
  p1->Draw();
  p2->Draw();
  
  h_dummy->GetYaxis()->SetTitleSize(0.065);    
  h_dummy->GetYaxis()->SetTitleOffset(0.7);
  h_dummy->GetYaxis()->SetLabelSize(0.054);
    
  h_dummy->GetXaxis()->SetTitleSize(0);
  h_dummy->GetXaxis()->SetLabelSize(0);
  
  p1->cd();
  
  
  /*
  // asymmetric errors for data
  TGraphAsymmErrors* gr = new TGraphAsymmErrors(h_count);
  for (int i=0; i<h_count->GetNbinsX(); i++) {
    gr->SetPointEYhigh(i, 0.5 + sqrt(h_count->GetBinContent(i+1) + 0.25) );
    gr->SetPointEYlow (i,-0.5 + sqrt(h_count->GetBinContent(i+1) + 0.25) );
    if (h_count->GetBinContent(i+1) == 0) gr->SetPoint(i,h_count->GetBinCenter(i+1),-1);
  }
  gr->SetMarkerStyle(8);
  */
  cout << "Plotting stuff" << endl;
  h_dummy->Draw("hist");
  h_true->Draw("hist,same");
  h_unfolded[0]->Draw("hist,ep,same");
  //gr->Draw("ep,same");
  h_dummy->Draw("hist,axis,same"); 
    
  TH1F* h_exp = new TH1F("exp","",1,0,1);
  h_exp->SetMarkerSize(0);
  h_exp->SetFillColor(18);
  h_exp->SetLineColor(18);
  h_exp->SetFillStyle(1001);

  // ----------------------------------------------------------------------------------------------------------------
  TLegend* leg = new TLegend(0.45,0.6,0.9,0.9);  
  leg->AddEntry(h_true,"Generated","l");
  leg->AddEntry(h_unfolded[0],"Unfolded MC: Closure test","pel");
  leg->AddEntry(h_exp,"Experimental uncertainties","f");
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetTextSize(0.05);
  leg->SetTextFont(42);
  leg->Draw();

  

  // ----------------------------------------------------------------------------------------------------------------
  // making ratio part of plot
  
  TString baselab = h_unfolded[0]->GetName();
  TH1F* h_ratio    = (TH1F*) h_unfolded[0]->Clone(baselab+"_ratio");
  TH1F* h_ratioEXP_up = (TH1F*) h_systEXP_up->Clone(baselab+"_ratioEXP_up");
  TH1F* h_ratioEXP_dn = (TH1F*) h_systEXP_dn->Clone(baselab+"_ratioEXP_dn");

  TH1F* h_ratioTH_up = (TH1F*) h_systTH_up->Clone(baselab+"_ratioTH_up");
  TH1F* h_ratioTH_dn = (TH1F*) h_systTH_dn->Clone(baselab+"_ratioTH_dn");
  
  h_ratio->Divide(h_true);
  h_ratioEXP_up->Divide(h_true);
  h_ratioEXP_dn->Divide(h_true);
  h_ratioTH_up->Divide(h_true);
  h_ratioTH_dn->Divide(h_true);
    
  /*
  // asymmetric errors for data
  TGraphAsymmErrors* grr = new TGraphAsymmErrors(h_ratio);
  float valup = 0;
  float valdn = 0;
  float sigup_high = 0;
  float sigup_low  = 0;
  float sigdn = 0;
  float err_high = 0;
  float err_low  = 0;
  for (int i=0; i<h_count->GetNbinsX(); i++) {
    valup = h_count->GetBinContent(i+1);
    valdn = h_bkg->GetBinContent(i+1);
    sigup_high =  0.5 + sqrt(h_count->GetBinContent(i+1) + 0.25);
    sigup_low  = -0.5 + sqrt(h_count->GetBinContent(i+1) + 0.25);
    sigdn = h_bkg->GetBinError(i+1);
    if (valup==0 || valdn==0) {
      err_high = 0;
      err_low  = 0;
    }
    else {
      err_high = valup/valdn*sqrt(sigup_high*sigup_high/valup/valup + sigdn*sigdn/valdn/valdn);
      err_low  = valup/valdn*sqrt(sigup_low*sigup_low/valup/valup + sigdn*sigdn/valdn/valdn);
    }
    grr->SetPointEYhigh(i, err_high);
    grr->SetPointEYlow(i, err_low);    
    if (h_count->GetBinContent(i+1) == 0) grr->SetPoint(i,h_count->GetBinCenter(i+1),-1);
    if (h_ratio->GetBinContent(i+1) > 2.5) h_ratio->SetBinContent(i+1,0);
  }
  grr->SetMarkerStyle(8);
  */
  
  
  // ----------------------------------------------------------------------------------------------------------------
  TH1F* blaEXP = (TH1F*) h_ratioEXP_up->Clone("blaEXP");
  blaEXP->Reset();
  for (int i=0; i<blaEXP->GetNbinsX(); i++) {
    float up = h_ratioEXP_up->GetBinContent(i+1);
    float dn = h_ratioEXP_dn->GetBinContent(i+1);
    
    blaEXP->SetBinContent(i+1,(up-dn)/2+dn);
    blaEXP->SetBinError(i+1,(up-dn)/2);
  }

  TH1F* blaTH = (TH1F*) h_ratioTH_up->Clone("blaTH");
  blaTH->Reset();
  for (int i=0; i<blaTH->GetNbinsX(); i++) {
    float up = h_ratioTH_up->GetBinContent(i+1);
    float dn = h_ratioTH_dn->GetBinContent(i+1);
    
    blaTH->SetBinContent(i+1,(up-dn)/2+dn);
    blaTH->SetBinError(i+1,(up-dn)/2);
  }

  /*
  TH1F* bla2 = bla->Clone("bla2");
  bla->SetMarkerSize(0);
  bla2->SetMarkerSize(0);
  bla->SetFillColor(16);
  bla2->SetFillColor(18);
  bla2->SetFillStyle(1001);
  bla->SetFillStyle(3004);
  */
  blaEXP->SetMarkerSize(0);
  blaEXP->SetFillColor(18);
  blaEXP->SetFillStyle(1001);

  blaTH->SetMarkerSize(0);
  blaTH->SetFillColor(2);
  blaTH->SetFillStyle(3353);

  TH1F* line = new TH1F("line",";;",1,400,1400);
  line->SetBinContent(1,1.0);
  line->SetLineColor(1);
  line->SetLineStyle(2);
  line->SetLineWidth(0.5);
  
    
  p2->cd();
  
  h_ratio->GetXaxis()->SetTitleSize(0.12);
  h_ratio->GetXaxis()->SetLabelSize(0.12);
  h_ratio->GetYaxis()->SetLabelSize(0.1);
  h_ratio->GetYaxis()->SetTitle("Measured / True");
  h_ratio->GetYaxis()->SetTitleSize(0.12);
  h_ratio->GetYaxis()->SetTitleOffset(0.7);
  h_ratio->GetYaxis()->SetNdivisions(505);
  //h_ratio->GetYaxis()->SetNdivisions(510);
  h_ratio->GetYaxis()->SetTitleOffset(0.38);
  h_ratio->GetXaxis()->SetTitleOffset(1.2);
  
  h_ratio->SetAxisRange(0.0,2.0,"Y");
  h_ratio->Draw("ep,hist");
  //grr->Draw("p,same");
  line->Draw("same");
  //grr->Draw("p,same");
  //bla2->Draw("same,e2");
  blaEXP->Draw("same,e3");
  blaTH->Draw("same,e3");
  line->Draw("same");
  h_ratio->Draw("pe,same,hist");
  //grr->Draw("p,same");
  h_ratio->Draw("same,axis");
  
  p1->cd();
    
  
  c->SaveAs("unfoldWithError.png");
  c->SaveAs("unfoldWithError.eps");
  c->SaveAs("unfoldWithError.pdf");

  
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
  /*
  gStyle->SetPadTopMargin(0.05);
  gStyle->SetPadRightMargin(0.05);
  gStyle->SetPadBottomMargin(0.16);
  gStyle->SetPadLeftMargin(0.16);
  */
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
  Double_t tsize=0.044;
  TLatex l;
  l.SetTextSize(tsize); 
  l.SetNDC();
  l.SetTextColor(color);
  l.DrawLatex(x,y,text);
}
