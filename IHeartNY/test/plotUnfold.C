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
void mySmallText(Double_t x,Double_t y,Color_t color,Double_t tsize,char *text); 
void plot(TString channel, bool wobtag, bool do2step);

void plotUnfold() {

  cout << " bla " << endl;

  plot("muon",true,true);
  /*plot("muon",false,false);
  plot("muon",false,true);
  plot("muon",true,false);*/

  plot("ele",true,true);
  /*plot("ele",false,false);
  plot("ele",false,true);
  plot("ele",true,false);*/

}

void plot(TString channel, bool wobtag, bool do2step) {
  
  SetPlotStyle();
  
  // full range unfolding, including events 0-2000 GeV
  TString unfoldType = "_full2";

  TString nobtag = "_nobtag";
  if (!wobtag) nobtag = "";

  // do two-step unfolding
  TString twoStep = "_2step";
  if (!do2step) twoStep = "";
  
  TString muOrEl = "";
  if (channel == "ele") muOrEl = "_el";


  // ---------------------------------------------------------------------------------------------------------------
  // get files & histograms
  
  const int nSYST = 1+10+4; //nominal+expSyst+thSyst
  TString name_syst[nSYST] = {"_CT10_nom_nom",
			      "_CT10_nom_jecup",
			      "_CT10_nom_jecdn",
			      "_CT10_nom_jerup",
			      "_CT10_nom_jerdn",			      
			      "_CT10_nom_btagup",
			      "_CT10_nom_btagdn",
			      "_CT10_nom_toptagFITup",
			      "_CT10_nom_toptagFITdn",
			      "_CT10_nom_nom_bkgup",
			      "_CT10_nom_nom_bkgdn",
			      "_CT10_pdfup_nom",
			      "_CT10_pdfdown_nom",
			      "_scaleup_nom",
			      "_scaledown_nom",
  };
  
  TFile* f_syst[nSYST];
  TH1F* h_unfolded[nSYST];
  TH1F* h_true;
  TH1F* h_measured;
  
  TH1F* h_part;
  TH1F* h_unfolded_part[nSYST];
  
  cout << endl << "Getting files and hists..." << endl;

  /*
  TFile* f_syst_MSTW  = new TFile("UnfoldingPlots/unfold"+muOrEl+twoStep+"_MSTW_nom_nom"+nobtag+unfoldType+".root");
  TFile* f_syst_NNPDF = new TFile("UnfoldingPlots/unfold"+muOrEl+twoStep+"_NNPDF_nom_nom"+nobtag+unfoldType+".root");

  TH1F* h_true_MSTW  = (TH1F*) f_syst_MSTW->Get("pt_genTop")->Clone();
  h_true_MSTW->SetName("pt_genTop_MSTW");
  TH1F* h_true_NNPDF = (TH1F*) f_syst_NNPDF->Get("pt_genTop")->Clone();
  h_true_NNPDF->SetName("pt_genTop_NNPDF");
  */


  for (int is=0; is<nSYST; is++) {
    
    f_syst[is] = new TFile("UnfoldingPlots/unfold"+muOrEl+twoStep+name_syst[is]+nobtag+unfoldType+".root");
    
    if (is==0) {
      h_true = (TH1F*) f_syst[is]->Get("pt_genTop")->Clone();
      h_measured = (TH1F*) f_syst[is]->Get("ptRecoTop"+twoStep+nobtag+unfoldType)->Clone();
      h_true->SetAxisRange(400,1150,"X");
      h_measured->SetAxisRange(400,1150,"X");
      if (twoStep == "_2step") {
	h_part = (TH1F*) f_syst[is]->Get("pt_partTop")->Clone();
	h_part->SetAxisRange(400,1150,"X");
      }
	
    }
    
    h_unfolded[is] = (TH1F*) f_syst[is]->Get("UnfoldedData")->Clone();
    h_unfolded[is]->SetName("UnfoldedData"+name_syst[is]);
    h_unfolded[is]->SetAxisRange(400,1150,"X");
    if (twoStep == "_2step") {
      h_unfolded_part[is] = (TH1F*) f_syst[is]->Get("UnfoldedData_rp")->Clone();
      h_unfolded_part[is]->SetName("UnfoldedData_part"+name_syst[is]);
      h_unfolded_part[is]->SetAxisRange(400,1150,"X");
    }
  }
  

  TH1F* h_dummy = (TH1F*) h_measured->Clone("dummy");
  h_dummy->Reset();
  
  TH1F* h_dummy_r = (TH1F*) h_measured->Clone("dummy_r");
  h_dummy_r->Reset();

  TH1F* h_dummy_part = (TH1F*) h_measured->Clone("dummy_part");
  h_dummy_part->Reset();
    
  TH1F* h_dummy_r_part = (TH1F*) h_measured->Clone("dummy_r_part");
  h_dummy_r_part->Reset();
    


  // ----------------------------------------------------------------------------------------------------------------
  // colors and stuff
  
  h_measured->SetLineColor(1);
  h_measured->SetMarkerColor(1);
  h_measured->SetMarkerStyle(24);
  
  h_true->SetLineColor(2);
  //h_true_MSTW->SetLineColor(4);
  //h_true_NNPDF->SetLineColor(8);
  
  h_unfolded[0]->SetLineColor(1);
  h_unfolded[0]->SetMarkerColor(1);
  h_unfolded[0]->SetMarkerStyle(8);
  
  if (twoStep == "_2step") {
    h_part->SetLineColor(2);
    
    h_unfolded_part[0]->SetLineColor(1);
    h_unfolded_part[0]->SetMarkerColor(1);
    h_unfolded_part[0]->SetMarkerStyle(8);

  }
  
  float tmp_max = 0;
  
  
  // ----------------------------------------------------------------------------------------------------------------
  // systematics for ratio plot
  
  TH1F* h_systEXP_up = (TH1F*) h_measured->Clone("syst_up_exp");
  TH1F* h_systEXP_dn = (TH1F*) h_measured->Clone("syst_dn_exp");
  h_systEXP_up->Reset();
  h_systEXP_dn->Reset();
  
  TH1F* h_systTH_up = (TH1F*) h_measured->Clone("syst_up_th");
  TH1F* h_systTH_dn = (TH1F*) h_measured->Clone("syst_dn_th");
  h_systTH_up->Reset();
  h_systTH_dn->Reset();

  // experimental  
  TH1F* h_syst_jec    = (TH1F*) h_measured->Clone("syst_jec");
  TH1F* h_syst_jer    = (TH1F*) h_measured->Clone("syst_jer");
  TH1F* h_syst_btag   = (TH1F*) h_measured->Clone("syst_btag");
  TH1F* h_syst_toptag = (TH1F*) h_measured->Clone("syst_toptag");
  TH1F* h_syst_bkg    = (TH1F*) h_measured->Clone("syst_bkg");
  // statistics
  TH1F* h_syst_stat   = (TH1F*) h_measured->Clone("syst_stat");
  // theory
  TH1F* h_syst_pdf    = (TH1F*) h_measured->Clone("syst_pdf");
  TH1F* h_syst_Q2     = (TH1F*) h_measured->Clone("syst_Q2");

  TH1F* h_syst_tot = (TH1F*) h_measured->Clone("syst_tot");
  
  h_syst_jec->Reset();   
  h_syst_jer->Reset(); 
  h_syst_btag->Reset();   
  h_syst_toptag->Reset(); 
  h_syst_bkg->Reset(); 
  h_syst_stat->Reset(); 
  h_syst_tot->Reset(); 
  h_syst_pdf->Reset();
  h_syst_Q2->Reset(); 
  
  
  float count[nSYST] = {0};
  float sig[nSYST] = {0};
  

  cout << endl << "*** unfolding result (parton-level) ***" << endl;

  for (int i=0; i<h_unfolded[0]->GetNbinsX()+1; i++) {
    
    for (int is=0; is<nSYST; is++) {
      count[is] = 0;
      sig[is] = 0;
      
      count[is] = h_unfolded[is]->GetBinContent(i+1);
      sig[is]   = h_unfolded[is]->GetBinError(i+1);
    }
    
    float this_systEXP_up = 0;
    this_systEXP_up += (count[1]-count[0])*(count[1]-count[0]); //jec
    this_systEXP_up += (count[3]-count[0])*(count[3]-count[0]); //jer
    this_systEXP_up += (count[5]-count[0])*(count[5]-count[0]); //btag
    this_systEXP_up += (count[7]-count[0])*(count[7]-count[0]); //toptag
    this_systEXP_up += (count[9]-count[0])*(count[9]-count[0]); //background normalizations
    this_systEXP_up += sig[0]*sig[0];                           //stastistics
    this_systEXP_up = sqrt(this_systEXP_up);
    
    float this_systEXP_dn = 0;
    this_systEXP_dn += (count[2]-count[0])*(count[2]-count[0]);
    this_systEXP_dn += (count[4]-count[0])*(count[4]-count[0]);
    this_systEXP_dn += (count[6]-count[0])*(count[6]-count[0]);
    this_systEXP_dn += (count[8]-count[0])*(count[8]-count[0]);
    this_systEXP_dn += (count[10]-count[0])*(count[10]-count[0]);
    this_systEXP_dn += sig[0]*sig[0];
    this_systEXP_dn = sqrt(this_systEXP_dn);
    
    float this_systTH_up = 0;
    this_systTH_up += (count[11]-count[0])*(count[11]-count[0]); //pdf
    //this_systTH_up += (count[13]-count[0])*(count[13]-count[0]); //q2
    this_systTH_up = sqrt(this_systTH_up);
    
    float this_systTH_dn = 0;
    this_systTH_dn += (count[12]-count[0])*(count[12]-count[0]);
    //this_systTH_dn += (count[14]-count[0])*(count[14]-count[0]);
    this_systTH_dn = sqrt(this_systTH_dn);
    
    float upEXP = count[0] + this_systEXP_up;
    float dnEXP = count[0] - this_systEXP_dn;
    
    h_systEXP_up->SetBinContent(i+1,upEXP);
    h_systEXP_dn->SetBinContent(i+1,dnEXP);  
    
    float upTH = count[0] + this_systTH_up;
    float dnTH = count[0] - this_systTH_dn;
    
    h_systTH_up->SetBinContent(i+1,upTH);
    h_systTH_dn->SetBinContent(i+1,dnTH);  
    
    int ibin1 = h_systEXP_up->GetBin(i+1);
    int ibin2 = h_systEXP_up->GetBin(i+2);
    int lowedge = h_systEXP_up->GetBinLowEdge(ibin1);
    int highedge = h_systEXP_up->GetBinLowEdge(ibin2);
    if (lowedge > 300 && highedge < 1300) {
      //cout << "measured [" << lowedge << "," << highedge << "] = " 
      //   << count[0] << " +" << this_systEXP_up << " / -" << this_systEXP_dn << " (exp) +" << this_systTH_up << " / -" << this_systTH_dn << " (th)" << endl;
      //cout << "generator (CT10) = " << h_true->GetBinContent(i+1) << endl;

      cout << (float)lowedge << "--" << (float)highedge << " & $" << count[0] << "~^{+" << this_systEXP_up << "}_{-" << this_systEXP_dn << "}{~(\\rm ex)~}^{+" 
	   << this_systTH_up << "}_{-" << this_systTH_dn << "}{~(\\rm th)}$ & " << h_true->GetBinContent(i+1) << endl;

    }
  }
  cout << endl;
  
  h_dummy->GetXaxis()->SetTitle("p_{T} [GeV]");
  h_dummy->GetYaxis()->SetTitle("d#sigma/dp_{T} [fb/GeV]");
  h_dummy->SetAxisRange(400,1150,"X");
  h_dummy->SetAxisRange(0,12,"Y");
  
  // getting the relative systematics

  //cout << "*** systematic uncertainties for each bin (parton-level) ***" << endl; 

  float count_r[nSYST] = {0};
  float err_r[nSYST] = {0};
  float err_stat = 0;
  for (int i=0; i<h_unfolded[0]->GetNbinsX()+1; i++) {

    err_stat = h_unfolded[0]->GetBinError(i+1);
    
    for (int is=0; is<nSYST; is++) {
      count_r[is] = 0;
      count_r[is] = h_unfolded[is]->GetBinContent(i+1);
      err_r[is] = h_unfolded[is]->GetBinError(i+1);
    }

    // experimental
    double syst_jecup   = fabs((count_r[1]-count_r[0])/count_r[0])*100;
    double syst_jecdn   = fabs((count_r[2]-count_r[0])/count_r[0])*100;
    double max_syst_jec = max(syst_jecup,syst_jecdn);
    double syst_jerup   = fabs((count_r[3]-count_r[0])/count_r[0])*100;
    double syst_jerdn   = fabs((count_r[4]-count_r[0])/count_r[0])*100;
    double max_syst_jer = max(syst_jerup,syst_jerdn);
    double syst_btagup   = fabs((count_r[5]-count_r[0])/count_r[0])*100;
    double syst_btagdn   = fabs((count_r[6]-count_r[0])/count_r[0])*100;
    double max_syst_btag = max(syst_btagup,syst_btagdn);
    double syst_toptagup   = fabs((count_r[7]-count_r[0])/count_r[0])*100;
    double syst_toptagdn   = fabs((count_r[8]-count_r[0])/count_r[0])*100;
    double max_syst_toptag = max(syst_toptagup,syst_toptagdn);
    double syst_bkgup   = fabs((count_r[9]-count_r[0])/count_r[0])*100;
    double syst_bkgdn   = fabs((count_r[10]-count_r[0])/count_r[0])*100;
    double max_syst_bkg = max(syst_bkgup,syst_bkgdn);
    // statistics    
    double syst_stat   = err_stat/count_r[0]*100;
    // theoretical
    double syst_pdfup   = fabs((count_r[11]-count_r[0])/count_r[0])*100;
    double syst_pdfdn   = fabs((count_r[12]-count_r[0])/count_r[0])*100;
    double max_syst_pdf = max(syst_pdfup,syst_pdfdn);
    double syst_scaleup = fabs((count_r[13]-count_r[0])/count_r[0])*100;
    double syst_scaledn = fabs((count_r[14]-count_r[0])/count_r[0])*100;
    double max_syst_Q2  = max(syst_scaleup,syst_scaledn);

    /*
    double syst_total_up = sqrt(syst_jecup*syst_jecup + syst_jerup*syst_jerup + syst_btagup*syst_btagup + syst_toptagup*syst_toptagup + syst_bkgup*syst_bkgup + 
				syst_stat*syst_stat + syst_scaleup*syst_scaleup + syst_pdfup*syst_pdfup);
    double syst_total_dn = sqrt(syst_jecdn*syst_jecdn + syst_jerdn*syst_jerdn + syst_btagdn*syst_btagdn + syst_toptagdn*syst_toptagdn + syst_bkgdn*syst_bkgdn + 
				syst_stat*syst_stat + syst_scaledn*syst_scaledn + syst_pdfdn*syst_pdfdn);
    */
    double syst_total_up = sqrt(syst_jecup*syst_jecup + syst_jerup*syst_jerup + syst_btagup*syst_btagup + syst_toptagup*syst_toptagup + syst_bkgup*syst_bkgup + 
				syst_pdfup*syst_pdfup);
    double syst_total_dn = sqrt(syst_jecdn*syst_jecdn + syst_jerdn*syst_jerdn + syst_btagdn*syst_btagdn + syst_toptagdn*syst_toptagdn + syst_bkgdn*syst_bkgdn + 
				syst_pdfdn*syst_pdfdn);
    double max_syst_total = max(syst_total_up,syst_total_dn);

    /*
    cout << "statistical error for bin "<<i<<": "<<syst_stat<<endl;
    cout << "relative syst scaleup for bin "<<i<<": "<<syst_scaleup<<endl;
    cout << "relative syst scaledown for bin "<<i<<": "<<syst_scaledn<<endl;
    cout << "max(syst_scaleup,syst_scaledown) for bin"<<i<<": "<<max_syst_Q2<<endl;
    cout << "relative syst pdfup for bin "<<i<<": "<<syst_pdfup<<endl;
    cout << "relative syst pdfdown for bin "<<i<<": "<<syst_pdfdown<<endl;
    cout << "max(syst_pdfup,syst_pdfdown) for bin"<<i<<": "<<max_syst_pdf<<endl;
    cout << "relative syst jecup for bin "<<i<<": "<<syst_jecup<<endl;
    cout << "relative syst jecdn for bin "<<i<<": "<<syst_jecdn<<endl;
    cout << "max(syst_jecup,syst_jecdn) for bin"<<i<<": "<<max_syst_jec<<endl;
    cout << "relative syst jerup for bin "<<i<<": "<<syst_jerup<<endl;
    cout << "relative syst jerdn for bin "<<i<<": "<<syst_jerdn<<endl;
    cout << "max(syst_jerup,syst_jerdn) for bin"<<i<<": "<<max_syst_jer<<endl;
    cout << "relative syst btagup for bin "<<i<<": "<<syst_btagup<<endl;
    cout << "relative syst btagdn for bin "<<i<<": "<<syst_btagdn<<endl;
    cout << "max(syst_btagup,syst_btagdn) for bin"<<i<<": "<<max_syst_btag<<endl;
    cout << "relative syst toptagup for bin "<<i<<": "<<syst_toptagup<<endl;
    cout << "relative syst toptagdn for bin "<<i<<": "<<syst_toptagdn<<endl;
    cout << "max(syst_toptagup,syst_toptagdn) for bin"<<i<<": "<<max_syst_toptag<<endl;
    cout << "relative syst bkgup for bin "<<i<<": "<<syst_bkgup<<endl;
    cout << "relative syst bkgdn for bin "<<i<<": "<<syst_bkgdn<<endl;
    cout << "max(syst_bkgup,syst_bkgdn) for bin"<<i<<": "<<max_syst_bkg<<endl;
    */
    
    h_syst_jec->SetBinContent(i+1,max_syst_jec);    
    h_syst_jer->SetBinContent(i+1,max_syst_jer);    
    h_syst_btag->SetBinContent(i+1,max_syst_btag);   
    h_syst_toptag->SetBinContent(i+1,max_syst_toptag); 
    h_syst_bkg->SetBinContent(i+1,max_syst_bkg); 
    h_syst_stat->SetBinContent(i+1,syst_stat);  
    h_syst_pdf->SetBinContent(i+1,max_syst_pdf);
    h_syst_Q2->SetBinContent(i+1,max_syst_Q2);  
    h_syst_tot->SetBinContent(i+1,max_syst_total);  
    
    h_syst_jec->SetBinError(i+1,0.001);
    h_syst_jer->SetBinError(i+1,0.001);
    h_syst_btag->SetBinError(i+1,0.001);
    h_syst_toptag->SetBinError(i+1,0.001);
    h_syst_bkg->SetBinError(i+1,0.001);
    h_syst_stat->SetBinError(i+1,0.001);
    h_syst_pdf->SetBinError(i+1,0.001);
    h_syst_Q2->SetBinError(i+1,0.001);  
    h_syst_tot->SetBinError(i+1,0.001);
    
  }
   

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

  h_dummy->Draw("hist");
  h_true->Draw("hist,same");
  //h_true_MSTW->Draw("hist,same");
  //h_true_NNPDF->Draw("hist,same");
  h_unfolded[0]->Draw("hist,ep,same");
  //gr->Draw("ep,same");
  h_dummy->Draw("hist,axis,same"); 
  
    
  
  // ----------------------------------------------------------------------------------------------------------------
  // making ratio part of plot
  
  TString baselab = h_unfolded[0]->GetName();
  TH1F* h_ratio       = (TH1F*) h_unfolded[0]->Clone(baselab+"_ratio");
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
  
  blaEXP->SetMarkerSize(0);
  blaEXP->SetLineColor(0);
  blaEXP->SetFillColor(18);
  blaEXP->SetFillStyle(1001);
  
  blaTH->SetMarkerSize(0);
  blaTH->SetLineColor(0);
  blaTH->SetFillColor(2);
  blaTH->SetFillStyle(3353);
  

  // ----------------------------------------------------------------------------------------------------------------
  TLegend* leg = new TLegend(0.45,0.45,0.9,0.75);  
  leg->AddEntry(h_true,"POWHEG t#bar{t} MC (CT10)","l");
  leg->AddEntry(h_unfolded[0],"Unfolded data","pel");
  leg->AddEntry(blaEXP,"Experimental uncertainties","f");
  leg->AddEntry(blaTH,"Theory uncertainties","f");
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetTextSize(0.05);
  leg->SetTextFont(42);
  leg->Draw();

  mySmallText(0.38,0.82,1,0.05,"CMS Preliminary, L = 19.7 fb^{-1}, #sqrt{s} = 8 TeV");


  // ----------------------------------------------------------------------------------------------------------------

  TH1F* line = new TH1F("line",";;",1,400,1300);
  line->SetBinContent(1,1.0);
  line->SetLineColor(1);
  line->SetLineStyle(2);
  line->SetLineWidth(0.5);  

  p2->cd();
  

  h_ratio->GetXaxis()->SetTitleSize(0.12);
  h_ratio->GetXaxis()->SetLabelSize(0.12);
  h_ratio->GetYaxis()->SetLabelSize(0.1);
  h_ratio->GetYaxis()->SetTitle("Data/MC");
  h_ratio->GetXaxis()->SetTitle("Top quark p_{T} [GeV]");
  h_ratio->GetYaxis()->SetTitleSize(0.12);
  h_ratio->GetYaxis()->SetTitleOffset(0.7);
  h_ratio->GetYaxis()->SetNdivisions(505);
  //h_ratio->GetYaxis()->SetNdivisions(510);
  h_ratio->GetYaxis()->SetTitleOffset(0.38);
  h_ratio->GetXaxis()->SetTitleOffset(1.2);
  
  h_ratio->SetAxisRange(0.0,2.0,"Y");
  h_ratio->Draw("ep,hist");
  //grr->Draw("p,same");
  //grr->Draw("p,same");
  blaEXP->Draw("same,e2");
  blaTH->Draw("same,e2");
  h_ratio->Draw("pe,same,hist");
  //grr->Draw("p,same");
  h_ratio->Draw("same,axis");
  line->Draw("same");
  
  p1->cd();
  
  
  c->SaveAs("UnfoldingPlots/unfoldWithError"+muOrEl+twoStep+nobtag+unfoldType+".png");
  c->SaveAs("UnfoldingPlots/unfoldWithError"+muOrEl+twoStep+nobtag+unfoldType+".eps");
  c->SaveAs("UnfoldingPlots/unfoldWithError"+muOrEl+twoStep+nobtag+unfoldType+".pdf");

  
  TCanvas *c1 = new TCanvas("c1", "", 800, 600);
  c1->SetTopMargin(0.05);
  c1->SetRightMargin(0.05);
  c1->SetBottomMargin(0.16);
  c1->SetLeftMargin(0.16);
  

  h_dummy_r->GetXaxis()->SetTitle("Top quark p_{T} [GeV]");
  h_dummy_r->GetYaxis()->SetTitle("Uncertainty [%]");
  h_dummy_r->SetAxisRange(400,1150,"X");
  h_dummy_r->SetAxisRange(0,50,"Y");
  
  h_dummy_r->GetYaxis()->SetTitleSize(0.055);    
  h_dummy_r->GetYaxis()->SetTitleOffset(1.0);
  h_dummy_r->GetYaxis()->SetLabelSize(0.045);
  
  h_dummy_r->GetXaxis()->SetTitleSize(0.05);
  h_dummy_r->GetXaxis()->SetTitleOffset(1.2);
  h_dummy_r->GetXaxis()->SetLabelSize(0.0455);
  
  c1->cd();


  h_syst_tot->SetFillColor(17);
  h_syst_tot->SetFillStyle(3344);
  h_syst_tot->SetLineColor(16);
  h_syst_tot->SetLineWidth(2);

  h_syst_stat->SetLineColor(1);
  h_syst_stat->SetLineWidth(2);
  h_syst_stat->SetMarkerColor(1);
  h_syst_stat->SetMarkerStyle(20);

  h_syst_jec->SetLineColor(4);
  h_syst_jec->SetLineWidth(2);
  h_syst_jec->SetMarkerColor(4);
  h_syst_jec->SetMarkerStyle(21);
  
  h_syst_jer->SetLineColor(8);
  h_syst_jer->SetLineWidth(2);
  h_syst_jer->SetMarkerColor(8);
  h_syst_jer->SetMarkerStyle(22);
  
  h_syst_toptag->SetLineColor(2);
  h_syst_toptag->SetLineWidth(2);
  h_syst_toptag->SetMarkerColor(2);
  h_syst_toptag->SetMarkerStyle(23);

  h_syst_btag->SetLineColor(kAzure+10);
  h_syst_btag->SetLineWidth(2);
  h_syst_btag->SetMarkerColor(kAzure+10);
  h_syst_btag->SetMarkerStyle(24);  

  h_syst_bkg->SetLineColor(kOrange+1);
  h_syst_bkg->SetLineWidth(2);
  h_syst_bkg->SetMarkerColor(kOrange+1);
  h_syst_bkg->SetMarkerStyle(26);

  h_syst_pdf->SetLineColor(6);
  h_syst_pdf->SetLineWidth(2);
  h_syst_pdf->SetMarkerColor(6);
  h_syst_pdf->SetMarkerStyle(25);

  /*
  h_syst_Q2->SetLineColor(kOrange+1);
  h_syst_Q2->SetLineWidth(2);
  h_syst_Q2->SetMarkerColor(kOrange+1);
  h_syst_Q2->SetMarkerStyle(26);
  */    
  
  TLegend* leg2 = new TLegend(0.2,0.58,0.45,0.92);  
  leg2->AddEntry(h_syst_tot,"Total syst. uncertainty","f");
  leg2->AddEntry(h_syst_stat,"Statistical uncertainty","lp");
  leg2->AddEntry(h_syst_jec,"Jet energy scale","lp");
  leg2->AddEntry(h_syst_jer,"Jet energy resolution","lp");
  leg2->AddEntry(h_syst_toptag,"Top-tagging efficiency","lp");
  if (nobtag == "") leg2->AddEntry(h_syst_btag,"b-tagging efficiency","lp");
  leg2->AddEntry(h_syst_bkg,"Background normalization","lp");
  leg2->AddEntry(h_syst_pdf,"PDF uncertainty","lp");
  //leg2->AddEntry(h_syst_Q2,"Q^{2} scale","lp");
  leg2->SetFillStyle(0);
  leg2->SetBorderSize(0);
  leg2->SetTextSize(0.032);
  leg2->SetTextFont(42);

  	
  h_dummy_r->Draw("hist");
  h_syst_tot->Draw("hist,same");
  h_syst_stat->Draw("ep,same");
  h_syst_jec->Draw("ep,same");
  h_syst_jer->Draw("ep,same");
  h_syst_toptag->Draw("ep,same");
  if (nobtag == "") h_syst_btag->Draw("ep,same");
  h_syst_bkg->Draw("ep,same");
  //h_syst_Q2->Draw("ep,same");
  h_syst_pdf->Draw("ep,same");
  h_dummy_r->Draw("hist,axis,same");
  leg2->Draw(); 

  mySmallText(0.6,0.87,1,0.04,"CMS Preliminary");
  mySmallText(0.6,0.82,1,0.04,"L = 19.7 fb^{-1}, #sqrt{s} = 8 TeV");

  c1->SaveAs("UnfoldingPlots/unfold_relative_uncertainties"+muOrEl+twoStep+nobtag+unfoldType+".png");
  c1->SaveAs("UnfoldingPlots/unfold_relative_uncertainties"+muOrEl+twoStep+nobtag+unfoldType+".pdf");
  c1->SaveAs("UnfoldingPlots/unfold_relative_uncertainties"+muOrEl+twoStep+nobtag+unfoldType+".eps");


  // -----------------------------------------------------------
  // Now do particle-level...
  // -----------------------------------------------------------

  if (twoStep == "_2step") {

    // ----------------------------------------------------------------------------------------------------------------
    // systematics for ratio plot
    
    TH1F* h_systEXP_up_part = (TH1F*) h_measured->Clone("syst_up_exp_part");
    TH1F* h_systEXP_dn_part = (TH1F*) h_measured->Clone("syst_dn_exp_part");
    h_systEXP_up_part->Reset();
    h_systEXP_dn_part->Reset();
    
    TH1F* h_systTH_up_part = (TH1F*) h_measured->Clone("syst_up_th_part");
    TH1F* h_systTH_dn_part = (TH1F*) h_measured->Clone("syst_dn_th_part");
    h_systTH_up_part->Reset();
    h_systTH_dn_part->Reset();
    
    TH1F* h_syst_jec_part    = (TH1F*) h_measured->Clone("syst_jec_part");
    TH1F* h_syst_jer_part    = (TH1F*) h_measured->Clone("syst_jer_part");
    TH1F* h_syst_btag_part   = (TH1F*) h_measured->Clone("syst_btag_part");
    TH1F* h_syst_toptag_part = (TH1F*) h_measured->Clone("syst_toptag_part");
    TH1F* h_syst_bkg_part    = (TH1F*) h_measured->Clone("syst_bkg_part");
    TH1F* h_syst_stat_part   = (TH1F*) h_measured->Clone("syst_stat_part");
    TH1F* h_syst_pdf_part    = (TH1F*) h_measured->Clone("syst_pdf_part");
    TH1F* h_syst_Q2_part     = (TH1F*) h_measured->Clone("syst_Q2_part");
    TH1F* h_syst_tot_part    = (TH1F*) h_measured->Clone("syst_stat_tot");
    
    h_syst_jec_part->Reset();   
    h_syst_jer_part->Reset(); 
    h_syst_btag_part->Reset();   
    h_syst_toptag_part->Reset(); 
    h_syst_bkg_part->Reset(); 
    h_syst_stat_part->Reset(); 
    h_syst_pdf_part->Reset();
    h_syst_Q2_part->Reset(); 
    h_syst_tot_part->Reset(); 
    
    
    float count_part[nSYST] = {0};
    float sig_part[nSYST] = {0};
    
    cout << endl << "*** unfolding result (particle-level) ***" << endl;

    for (int i=0; i<h_unfolded_part[0]->GetNbinsX()+1; i++) {
      
      for (int is=0; is<nSYST; is++) {
	count_part[is] = 0;
	sig_part[is] = 0;
	
	count_part[is] = h_unfolded_part[is]->GetBinContent(i+1);
	sig_part[is]   = h_unfolded_part[is]->GetBinError(i+1);
      }
      
      float this_systEXP_up_part = 0;
      this_systEXP_up_part += (count_part[1]-count_part[0])*(count_part[1]-count_part[0]); //jec
      this_systEXP_up_part += (count_part[3]-count_part[0])*(count_part[3]-count_part[0]); //jer
      this_systEXP_up_part += (count_part[5]-count_part[0])*(count_part[5]-count_part[0]); //btag
      this_systEXP_up_part += (count_part[7]-count_part[0])*(count_part[7]-count_part[0]); //toptag
      this_systEXP_up_part += (count_part[9]-count_part[0])*(count_part[9]-count_part[0]); //background normalization
      this_systEXP_up_part += sig_part[0]*sig_part[0];                                     //statistics
      this_systEXP_up_part = sqrt(this_systEXP_up_part);
      
      float this_systEXP_dn_part = 0;
      this_systEXP_dn_part += (count_part[2]-count_part[0])*(count_part[2]-count_part[0]);
      this_systEXP_dn_part += (count_part[4]-count_part[0])*(count_part[4]-count_part[0]);
      this_systEXP_dn_part += (count_part[6]-count_part[0])*(count_part[6]-count_part[0]);
      this_systEXP_dn_part += (count_part[8]-count_part[0])*(count_part[8]-count_part[0]);
      this_systEXP_dn_part += (count_part[10]-count_part[0])*(count_part[10]-count_part[0]);
      this_systEXP_dn_part += sig_part[0]*sig_part[0];
      this_systEXP_dn_part = sqrt(this_systEXP_dn_part);
      
      float this_systTH_up_part = 0;
      this_systTH_up_part += (count_part[11]-count_part[0])*(count_part[11]-count_part[0]);
      //this_systTH_up_part += (count_part[13]-count_part[0])*(count_part[13]-count_part[0]);
      this_systTH_up_part = sqrt(this_systTH_up_part);
      
      float this_systTH_dn_part = 0;
      this_systTH_dn_part += (count_part[12]-count_part[0])*(count_part[12]-count_part[0]);
      //this_systTH_dn_part += (count_part[14]-count_part[0])*(count_part[14]-count_part[0]);
      this_systTH_dn_part = sqrt(this_systTH_dn_part);
      
      float upEXP_part = count_part[0] + this_systEXP_up_part;
      float dnEXP_part = count_part[0] - this_systEXP_dn_part;
      
      h_systEXP_up_part->SetBinContent(i+1,upEXP_part);
      h_systEXP_dn_part->SetBinContent(i+1,dnEXP_part);  
      
      float upTH_part = count_part[0] + this_systTH_up_part;
      float dnTH_part = count_part[0] - this_systTH_dn_part;
      
      h_systTH_up_part->SetBinContent(i+1,upTH_part);
      h_systTH_dn_part->SetBinContent(i+1,dnTH_part);  
      
      int ibin1_p = h_systEXP_up_part->GetBin(i+1);
      int ibin2_p = h_systEXP_up_part->GetBin(i+2);
      int lowedge_p = h_systEXP_up_part->GetBinLowEdge(ibin1_p);
      int highedge_p = h_systEXP_up_part->GetBinLowEdge(ibin2_p);
      if (lowedge_p > 300 && highedge_p < 1300) {
	/*
	cout << "measured [" << lowedge_p << "," << highedge_p << "] = " 
	     << count_part[0] << " +" << this_systEXP_up_part << " / -" << this_systEXP_dn_part 
	     << " (exp) +" << this_systTH_up_part << " / -" << this_systTH_dn_part << " (th)" << endl;
	cout << "generator (CT10) = " << h_part->GetBinContent(i+1) << endl;
	*/
	cout << lowedge_p << "--" << highedge_p << " & $" << count_part[0] << "~^{+" << this_systEXP_up_part << "}_{-" << this_systEXP_dn_part << "}{~(\\rm ex)~}^{+" 
	     << this_systTH_up_part << "}_{-" << this_systTH_dn_part << "}{~(\\rm th)}$ & " << h_part->GetBinContent(i+1) << endl;

      }
    }
    cout << endl;
  
    h_dummy_part->GetXaxis()->SetTitle("p_{T} [GeV]");
    h_dummy_part->GetYaxis()->SetTitle("d#sigma/dp_{T} [fb/GeV]");
    h_dummy_part->SetAxisRange(400,1150,"X");
    h_dummy_part->SetAxisRange(0,10,"Y");
    
    // getting the relative systematics

    //cout << endl << "*** systematic uncertainties for each bin (particle-level) ***" << endl; 

    float count_r_part[nSYST] = {0};
    float err_stat_part = 0;
    for (int i=0; i<h_unfolded_part[0]->GetNbinsX()+1; i++) {
      
      err_stat_part = h_unfolded_part[0]->GetBinError(i+1);
      
      for (int is=0; is<nSYST; is++) {
	count_r_part[is] = 0;
	count_r_part[is] = h_unfolded_part[is]->GetBinContent(i+1);
      }

      // experimental
      double syst_jecup_part   = fabs((count_r_part[1]-count_r_part[0])/count_r_part[0])*100;
      double syst_jecdn_part   = fabs((count_r_part[2]-count_r_part[0])/count_r_part[0])*100;
      double max_syst_jec_part = max(syst_jecup_part,syst_jecdn_part);
      double syst_jerup_part   = fabs((count_r_part[3]-count_r_part[0])/count_r_part[0])*100;
      double syst_jerdn_part   = fabs((count_r_part[4]-count_r_part[0])/count_r_part[0])*100;
      double max_syst_jer_part = max(syst_jerup_part,syst_jerdn_part);
      double syst_btagup_part   = fabs((count_r_part[5]-count_r_part[0])/count_r_part[0])*100;
      double syst_btagdn_part   = fabs((count_r_part[6]-count_r_part[0])/count_r_part[0])*100;
      double max_syst_btag_part = max(syst_btagup_part,syst_btagdn_part);
      double syst_toptagup_part   = fabs((count_r_part[7]-count_r_part[0])/count_r_part[0])*100;
      double syst_toptagdn_part   = fabs((count_r_part[8]-count_r_part[0])/count_r_part[0])*100;
      double max_syst_toptag_part = max(syst_toptagup_part,syst_toptagdn_part);
      double syst_bkgup_part   = fabs((count_r_part[9]-count_r_part[0])/count_r_part[0])*100;
      double syst_bkgdn_part   = fabs((count_r_part[10]-count_r_part[0])/count_r_part[0])*100;
      double max_syst_bkg_part = max(syst_bkgup_part,syst_bkgdn_part);
      // statistics
      double syst_stat_part   = err_stat_part/count_r_part[0]*100;
      // theoretical
      double syst_pdfup_part   = fabs((count_r_part[11]-count_r_part[0])/count_r_part[0])*100;
      double syst_pdfdn_part   = fabs((count_r_part[12]-count_r_part[0])/count_r_part[0])*100;
      double max_syst_pdf_part = max(syst_pdfup_part,syst_pdfdn_part);
      double syst_scaleup_part = fabs((count_r_part[13]-count_r_part[0])/count_r_part[0])*100;
      double syst_scaledn_part = fabs((count_r_part[14]-count_r_part[0])/count_r_part[0])*100;
      double max_syst_Q2_part = max(syst_scaleup_part,syst_scaledn_part);

      /*
      double syst_total_up_part = sqrt(syst_jecup_part*syst_jecup_part + syst_jerup_part*syst_jerup_part + 
				       syst_btagup_part*syst_btagup_part + syst_toptagup_part*syst_toptagup_part + syst_bkgup_part*syst_bkgup_part +
				       syst_stat_part*syst_stat_part + syst_scaleup_part*syst_scaleup_part + syst_pdfup_part*syst_pdfup_part);
      double syst_total_dn_part = sqrt(syst_jecdn_part*syst_jecdn_part + syst_jerdn_part*syst_jerdn_part + 
				       syst_btagdn_part*syst_btagdn_part + syst_toptagdn_part*syst_toptagdn_part + syst_bkgdn_part*syst_bkgdn_part +
				       syst_stat_part*syst_stat_part + syst_scaledn_part*syst_scaledn_part + syst_pdfdn_part*syst_pdfdn_part );
      */
      double syst_total_up_part = sqrt(syst_jecup_part*syst_jecup_part + syst_jerup_part*syst_jerup_part + 
				       syst_btagup_part*syst_btagup_part + syst_toptagup_part*syst_toptagup_part + syst_bkgup_part*syst_bkgup_part +
				       syst_pdfup_part*syst_pdfup_part);
      double syst_total_dn_part = sqrt(syst_jecdn_part*syst_jecdn_part + syst_jerdn_part*syst_jerdn_part + 
				       syst_btagdn_part*syst_btagdn_part + syst_toptagdn_part*syst_toptagdn_part + syst_bkgdn_part*syst_bkgdn_part +
				       syst_pdfdn_part*syst_pdfdn_part );
      double max_syst_total_part = max(syst_total_up_part,syst_total_dn_part);

      /*
      cout << "max(syst_jecup,syst_jecdn) for bin"<<i<<": "<<max_syst_jec_part<<endl;
      cout << "relative syst jerup for bin "<<i<<": "<<syst_jerup_part<<endl;
      cout << "relative syst jerdn for bin "<<i<<": "<<syst_jerdn_part<<endl;
      cout << "max(syst_jerup,syst_jerdn) for bin"<<i<<": "<<max_syst_jer_part<<endl;
      cout << "relative syst btagup for bin "<<i<<": "<<syst_btagup_part<<endl;
      cout << "relative syst btagdn for bin "<<i<<": "<<syst_btagdn_part<<endl;
      cout << "max(syst_btagup,syst_btagdn) for bin"<<i<<": "<<max_syst_btag_part<<endl;
      cout << "relative syst toptagup for bin "<<i<<": "<<syst_toptagup_part<<endl;
      cout << "relative syst toptagdn for bin "<<i<<": "<<syst_toptagdn_part<<endl;
      cout << "max(syst_toptagup,syst_toptagdn) for bin"<<i<<": "<<max_syst_toptag_part<<endl;
      cout << "relative syst bkgup for bin "<<i<<": "<<syst_bkgup_part<<endl;
      cout << "relative syst bkgdn for bin "<<i<<": "<<syst_bkgdn_part<<endl;
      cout << "max(syst_bkgdn,syst_bkgdn) for bin"<<i<<": "<<max_syst_bkg_part<<endl;
      cout << "statistical error for bin "<<i<<": "<<syst_stat_part<<endl;
      cout << "relative syst scaleup for bin "<<i<<": "<<syst_scaleup_part<<endl;
      cout << "relative syst scaledown for bin "<<i<<": "<<syst_scaledown_part<<endl;
      cout << "max(syst_pdfup,syst_pdfdown) for bin"<<i<<": "<<max_syst_pdf_part<<endl;
      cout << "relative syst jecup for bin "<<i<<": "<<syst_jecup_part<<endl;
      cout << "relative syst jecdn for bin "<<i<<": "<<syst_jecdn_part<<endl;
      cout << "max(syst_scaleup_part,syst_scaledown_part) for bin"<<i<<": "<<max_syst_Q2_part<<endl;
      cout << "relative syst pdfup for bin "<<i<<": "<<syst_pdfup_part<<endl;
      cout << "relative syst pdfdown for bin "<<i<<": "<<syst_pdfdown_part<<endl;
      */
      
      h_syst_jec_part->SetBinContent(i+1,max_syst_jec_part);    
      h_syst_jer_part->SetBinContent(i+1,max_syst_jer_part);    
      h_syst_btag_part->SetBinContent(i+1,max_syst_btag_part);   
      h_syst_toptag_part->SetBinContent(i+1,max_syst_toptag_part); 
      h_syst_bkg_part->SetBinContent(i+1,max_syst_bkg_part);  
      h_syst_stat_part->SetBinContent(i+1,syst_stat_part);  
      h_syst_pdf_part->SetBinContent(i+1,max_syst_pdf_part);
      h_syst_Q2_part->SetBinContent(i+1,max_syst_Q2_part);  
      h_syst_tot_part->SetBinContent(i+1,max_syst_total_part);  
      
      h_syst_jec_part->SetBinError(i+1,0.001);
      h_syst_jer_part->SetBinError(i+1,0.001);
      h_syst_btag_part->SetBinError(i+1,0.001);
      h_syst_toptag_part->SetBinError(i+1,0.001);
      h_syst_bkg_part->SetBinError(i+1,0.001);
      h_syst_stat_part->SetBinError(i+1,0.001);
      h_syst_tot_part->SetBinError(i+1,0.001);
      h_syst_pdf_part->SetBinError(i+1,0.001);
      h_syst_Q2_part->SetBinError(i+1,0.001);  
      
    }
    
    
    // ----------------------------------------------------------------------------------------------------------------
    // RATIO PLOTS !!!!!!!
    // ----------------------------------------------------------------------------------------------------------------
    
    gStyle->SetPadLeftMargin(0.12);
    gStyle->SetPadRightMargin(0.1);
    gStyle->SetTextSize(f_textSize);
    gStyle->SetLabelSize(f_textSize,"x");
    gStyle->SetTitleSize(f_textSize,"x");
    gStyle->SetLabelSize(f_textSize,"y");
    gStyle->SetTitleSize(f_textSize,"y");
    gStyle->SetOptStat(0);
    
    TCanvas *c2 = new TCanvas("c2", "", 700, 625);
    
    TPad* p3 = new TPad("p3","p3",0,ratio_size+0.0,1,1);
    p3->SetBottomMargin(0.04);
    p3->SetLeftMargin(0.13);
    p3->SetRightMargin(0.075);
    
    TPad* p4 = new TPad("p4","p4",0,0,1,ratio_size-0.0);
    p4->SetTopMargin(0.00);
    p4->SetBottomMargin(0.4);
    p4->SetLeftMargin(0.13);
    p4->SetRightMargin(0.075);
    
    p3->Draw();
    p4->Draw();
    
    h_dummy_part->GetYaxis()->SetTitleSize(0.065);    
    h_dummy_part->GetYaxis()->SetTitleOffset(0.7);
    h_dummy_part->GetYaxis()->SetLabelSize(0.054);
    
    h_dummy_part->GetXaxis()->SetTitleSize(0);
    h_dummy_part->GetXaxis()->SetLabelSize(0);
    
    p3->cd();
    
    h_dummy_part->Draw("hist");
    h_part->Draw("hist,same");
    //h_true_MSTW->Draw("hist,same");
    //h_true_NNPDF->Draw("hist,same");
    h_unfolded_part[0]->Draw("hist,ep,same");
    //gr->Draw("ep,same");
    h_dummy_part->Draw("hist,axis,same"); 
    
    
    
    // ----------------------------------------------------------------------------------------------------------------
    // making ratio part of plot
    
    TString baselab2 = h_unfolded_part[0]->GetName();
    TH1F* h_ratio_part    = (TH1F*) h_unfolded_part[0]->Clone(baselab2+"_ratio");
    TH1F* h_ratioEXP_up_part = (TH1F*) h_systEXP_up_part->Clone(baselab2+"_ratioEXP_up");
    TH1F* h_ratioEXP_dn_part = (TH1F*) h_systEXP_dn_part->Clone(baselab2+"_ratioEXP_dn");
    
    TH1F* h_ratioTH_up_part = (TH1F*) h_systTH_up_part->Clone(baselab2+"_ratioTH_up");
    TH1F* h_ratioTH_dn_part = (TH1F*) h_systTH_dn_part->Clone(baselab2+"_ratioTH_dn");
    
    h_ratio_part->Divide(h_part);
    h_ratioEXP_up_part->Divide(h_part);
    h_ratioEXP_dn_part->Divide(h_part);
    h_ratioTH_up_part->Divide(h_part);
    h_ratioTH_dn_part->Divide(h_part);
    
    
    // ----------------------------------------------------------------------------------------------------------------
    TH1F* blaEXP_part = (TH1F*) h_ratioEXP_up_part->Clone("blaEXP_part");
    blaEXP_part->Reset();
    for (int i=0; i<blaEXP_part->GetNbinsX(); i++) {
      float up = h_ratioEXP_up_part->GetBinContent(i+1);
      float dn = h_ratioEXP_dn_part->GetBinContent(i+1);
      
      blaEXP_part->SetBinContent(i+1,(up-dn)/2+dn);
      blaEXP_part->SetBinError(i+1,(up-dn)/2);
    }
    
    TH1F* blaTH_part = (TH1F*) h_ratioTH_up_part->Clone("blaTH_part");
    blaTH_part->Reset();
    for (int i=0; i<blaTH_part->GetNbinsX(); i++) {
      float up = h_ratioTH_up_part->GetBinContent(i+1);
      float dn = h_ratioTH_dn_part->GetBinContent(i+1);
      
      blaTH_part->SetBinContent(i+1,(up-dn)/2+dn);
      blaTH_part->SetBinError(i+1,(up-dn)/2);
    }
    
    blaEXP_part->SetMarkerSize(0);
    blaEXP_part->SetLineColor(0);
    blaEXP_part->SetFillColor(18);
    blaEXP_part->SetFillStyle(1001);
    
    blaTH_part->SetMarkerSize(0);
    blaTH_part->SetLineColor(0);
    blaTH_part->SetFillColor(2);
    blaTH_part->SetFillStyle(3353);
    
    
    // ----------------------------------------------------------------------------------------------------------------
    TLegend* leg3 = new TLegend(0.45,0.45,0.9,0.75);  
    leg3->AddEntry(h_part,"POWHEG t#bar{t} MC (CT10)","l");
    leg3->AddEntry(h_unfolded_part[0],"Unfolded data","pel");
    leg3->AddEntry(blaEXP_part,"Experimental uncertainties","f");
    leg3->AddEntry(blaTH_part,"Theory uncertainties","f");
    leg3->SetFillStyle(0);
    leg3->SetBorderSize(0);
    leg3->SetTextSize(0.05);
    leg3->SetTextFont(42);
    leg3->Draw();
    
    mySmallText(0.38,0.82,1,0.05,"CMS Preliminary, L = 19.7 fb^{-1}, #sqrt{s} = 8 TeV");


    // ----------------------------------------------------------------------------------------------------------------
        
    p4->cd();
    
    
    h_ratio_part->GetXaxis()->SetTitleSize(0.12);
    h_ratio_part->GetXaxis()->SetLabelSize(0.12);
    h_ratio_part->GetYaxis()->SetLabelSize(0.1);
    h_ratio_part->GetYaxis()->SetTitle("Data/MC");
    h_ratio_part->GetXaxis()->SetTitle("Particle-level top p_{T} [GeV]");
    h_ratio_part->GetYaxis()->SetTitleSize(0.12);
    h_ratio_part->GetYaxis()->SetTitleOffset(0.7);
    h_ratio_part->GetYaxis()->SetNdivisions(505);
    h_ratio_part->GetYaxis()->SetTitleOffset(0.38);
    h_ratio_part->GetXaxis()->SetTitleOffset(1.2);
    
    h_ratio_part->SetAxisRange(0.0,2.0,"Y");
    h_ratio_part->Draw("ep,hist");
    blaEXP_part->Draw("same,e2");
    blaTH_part->Draw("same,e2");
    h_ratio_part->Draw("pe,same,hist");
    h_ratio_part->Draw("same,axis");
    line->Draw("same");
    
    p3->cd();
    
    
    c2->SaveAs("UnfoldingPlots/unfoldWithError_part"+muOrEl+twoStep+nobtag+unfoldType+".png");
    c2->SaveAs("UnfoldingPlots/unfoldWithError_part"+muOrEl+twoStep+nobtag+unfoldType+".eps");
    c2->SaveAs("UnfoldingPlots/unfoldWithError_part"+muOrEl+twoStep+nobtag+unfoldType+".pdf");
    
    
    TCanvas *c3 = new TCanvas("c3", "", 800, 600);
    c3->SetTopMargin(0.05);
    c3->SetRightMargin(0.05);
    c3->SetBottomMargin(0.16);
    c3->SetLeftMargin(0.16);
    
    
    h_dummy_r_part->GetXaxis()->SetTitle("Particle-level top p_{T} [GeV]");
    h_dummy_r_part->GetYaxis()->SetTitle("Uncertainty [%]");
    h_dummy_r_part->SetAxisRange(400,1150,"X");
    h_dummy_r_part->SetAxisRange(0,50,"Y");
    
    h_dummy_r_part->GetYaxis()->SetTitleSize(0.055);    
    h_dummy_r_part->GetYaxis()->SetTitleOffset(1.0);
    h_dummy_r_part->GetYaxis()->SetLabelSize(0.045);
    
    h_dummy_r_part->GetXaxis()->SetTitleSize(0.05);
    h_dummy_r_part->GetXaxis()->SetTitleOffset(1.2);
    h_dummy_r_part->GetXaxis()->SetLabelSize(0.0455);
    
    c3->cd();
    

    h_syst_tot_part->SetFillColor(17);
    h_syst_tot_part->SetFillStyle(3344);
    h_syst_tot_part->SetLineColor(16);
    h_syst_tot_part->SetLineWidth(2);
    
    h_syst_stat_part->SetLineColor(1);
    h_syst_stat_part->SetLineWidth(2);
    h_syst_stat_part->SetMarkerColor(1);
    h_syst_stat_part->SetMarkerStyle(20);
    
    h_syst_jec_part->SetLineColor(4);
    h_syst_jec_part->SetLineWidth(2);
    h_syst_jec_part->SetMarkerColor(4);
    h_syst_jec_part->SetMarkerStyle(21);
    
    h_syst_jer_part->SetLineColor(8);
    h_syst_jer_part->SetLineWidth(2);
    h_syst_jer_part->SetMarkerColor(8);
    h_syst_jer_part->SetMarkerStyle(22);
    
    h_syst_toptag_part->SetLineColor(2);
    h_syst_toptag_part->SetLineWidth(2);
    h_syst_toptag_part->SetMarkerColor(2);
    h_syst_toptag_part->SetMarkerStyle(23);
    
    h_syst_btag_part->SetLineColor(kAzure+10);
    h_syst_btag_part->SetLineWidth(2);
    h_syst_btag_part->SetMarkerColor(kAzure+10);
    h_syst_btag_part->SetMarkerStyle(24);  

    h_syst_bkg_part->SetLineColor(kOrange+1);
    h_syst_bkg_part->SetLineWidth(2);
    h_syst_bkg_part->SetMarkerColor(kOrange+1);
    h_syst_bkg_part->SetMarkerStyle(26);
    
    h_syst_pdf_part->SetLineColor(6);
    h_syst_pdf_part->SetLineWidth(2);
    h_syst_pdf_part->SetMarkerColor(6);
    h_syst_pdf_part->SetMarkerStyle(25);
    
    /*
    h_syst_Q2_part->SetLineColor(kOrange+1);
    h_syst_Q2_part->SetLineWidth(2);
    h_syst_Q2_part->SetMarkerColor(kOrange+1);
    h_syst_Q2_part->SetMarkerStyle(26);
    */
  
    TLegend* leg4 = new TLegend(0.2,0.58,0.45,0.92);  
    leg4->AddEntry(h_syst_tot_part,"Total syst. uncertainty","f");
    leg4->AddEntry(h_syst_stat_part,"Statistical uncertainty","lp");
    leg4->AddEntry(h_syst_jec_part,"Jet energy scale","lp");
    leg4->AddEntry(h_syst_jer_part,"Jet energy resolution","lp");
    leg4->AddEntry(h_syst_toptag_part,"Top-tagging efficiency","lp");
    if (nobtag == "") leg4->AddEntry(h_syst_btag_part,"b-tagging efficiency","lp");
    leg4->AddEntry(h_syst_bkg_part,"Background normalization","lp");
    leg4->AddEntry(h_syst_pdf_part,"PDF uncertainty","lp");
    //leg4->AddEntry(h_syst_Q2_part,"Q^{2} scale","lp");
    leg4->SetFillStyle(0);
    leg4->SetBorderSize(0);
    leg4->SetTextSize(0.032);
    leg4->SetTextFont(42);
    
    
    h_dummy_r_part->Draw("hist");
    h_syst_tot_part->Draw("hist,same");
    h_syst_stat_part->Draw("ep,same");
    h_syst_jec_part->Draw("ep,same");
    h_syst_jer_part->Draw("ep,same");
    h_syst_toptag_part->Draw("ep,same");
    if (nobtag == "") h_syst_btag_part->Draw("ep,same");
    h_syst_bkg_part->Draw("ep,same");
    //h_syst_Q2_part->Draw("ep,same");
    h_syst_pdf_part->Draw("ep,same");
    h_dummy_r_part->Draw("hist,axis,same");
    leg4->Draw(); 
    
    mySmallText(0.6,0.87,1,0.04,"CMS Preliminary");
    mySmallText(0.6,0.82,1,0.04,"L = 19.7 fb^{-1}, #sqrt{s} = 8 TeV");
    
    c3->SaveAs("UnfoldingPlots/unfold_relative_uncertainties_part"+muOrEl+twoStep+nobtag+unfoldType+".png");
    c3->SaveAs("UnfoldingPlots/unfold_relative_uncertainties_part"+muOrEl+twoStep+nobtag+unfoldType+".pdf");
    c3->SaveAs("UnfoldingPlots/unfold_relative_uncertainties_part"+muOrEl+twoStep+nobtag+unfoldType+".eps");
  }

  return;

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


void mySmallText(Double_t x,Double_t y,Color_t color,Double_t tsize, char *text) {
  TLatex l;
  l.SetTextSize(tsize); 
  l.SetNDC();
  l.SetTextColor(color);
  l.DrawLatex(x,y,text);
}
