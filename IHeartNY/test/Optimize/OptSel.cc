// Code to do selection optimization

#include <iostream>
#include <cstdlib>
#include <cmath>
#include <string>
#include <vector>

#include <TMinuit.h>
#include <TCanvas.h>
#include <TStyle.h>
#include <TROOT.h>
#include <TF1.h>
#include <TF2.h>
#include <TAxis.h>
#include <TLine.h>
#include <TMath.h>
#include <THStack.h>
#include <sstream>
#include "TLatex.h"
#include "TPad.h"
#include "TText.h"
#include "TLegend.h"
#include "TFile.h"
#include "TGraphAsymmErrors.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TH1.h"
#include "TH2.h"

using namespace std;

int OptSel() {

  // User options
  bool dosub = true;
  double qcdnorm_0tag = 74.5;
  double qcderr_0tag = 17.2;
  double qcdnorm_btag = 1.9;
  double qcderr_btag = 16.1;
  TString dowhich = "TH1F"; // TH1F, TH2F, or all

  // Initialize histograms
  // Not sure if this is necessary, or how to make it tidy

  TString MC_array[10] = {"TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola", 
			   "TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola", 
			   "TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola", 
			   "T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola", 
			   "Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola", 
			   "T_t-channel_TuneZ2star_8TeV-powheg-tauola", 
			   "Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola", 
			   "T_s-channel_TuneZ2star_8TeV-powheg-tauola", 
			   "Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola",
			   "WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball"};
  
  double weight[10] = { 245.8 * 19748. / 21675970.,          //TTjets 0-700
			 245.8 * 19748. * 0.074 / 3082812., //TTjets 700-1000
			 245.8 * 19748. * 0.014 / 1249111., //TTjets 1000-Inf
			 11.1 * 19748. / 497658.,           //St_tW
			 11.1 * 19748. / 493460.,           //St_tWB
			 56.4 * 19748. / 3758227.,          //St_t
			 30.7 * 19748. / 1935072.,          //St_tB
			 3.79 * 19748. / 259961.,           //St_s
			 1.76 * 19748. / 139974.,           //St_sB
			 36703.2 * 19748. / 57709905.};     //Wjets

  // Do TH2F plots
  if (dowhich == "TH2F" or dowhich == "all"){
    TString TH2Fnames[10] = {"LEPMETvsMET", "LEPMETvsBtagJetPt", "LEPMETvsHT", "LEPMETvsHTLEP", "HTvsMET", 
			     "HTvsBtagJetPt", "HTvsHTLEP", "HTLEPvsMET", "HTLEPvsBtagJetPt", "BtagJetPtvsMET"};
  
    for (int i=0; i<10; i++){
      TFile* TTjets_files[3];
      TH2F** TTjets_his_array = new TH2F*[3];
      TFile* stop_files[6];
      TH2F** stop_his_array = new TH2F*[6];
      TFile* qcd_files[10];
      TH2F** qcd_his_array = new TH2F*[9];
      
      // Get TTjets histogram
      for (int j=0; j<3; j++){
	TTjets_files[j] = TFile::Open(MC_array[j]+"_optimize_mu_nom.root", "READ");
	TTjets_his_array[j] = (TH2F*) gDirectory->Get(TH2Fnames[i]);
	TTjets_his_array[j]->Scale(weight[j]);
      }
      TH2F *TTjets_TH2F_temp = (TH2F*)TTjets_his_array[0]->Clone("TTjets_TH2F_temp");
      TTjets_TH2F_temp->Add(TTjets_his_array[1]);
      TTjets_TH2F_temp->Add(TTjets_his_array[2]);
      
      // Get stop histogram
      for (int j=0; j<6; j++){
	stop_files[j] = TFile::Open(MC_array[j+3]+"_optimize_mu_nom.root", "READ");
	stop_his_array[j] = (TH2F*) gDirectory->Get(TH2Fnames[i]);
	stop_his_array[j]->Scale(weight[j+3]);
      }
      TH2F *stop_TH2F_temp = (TH2F*)stop_his_array[0]->Clone("stop_TH2F_temp");
      for (int j=1; j<6; j++){
	stop_TH2F_temp->Add(stop_his_array[j]);
      }
      
      // Get wjets histogram
      TFile* wjets_file = TFile::Open("WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_optimize_mu_nom.root", "READ");
      TH2F *wjets_TH2F_temp = (TH2F*) gDirectory->Get(TH2Fnames[i]);
      wjets_TH2F_temp->Scale(weight[9]);
      
      // Get QCD histogram
      qcd_files[0] = TFile::Open("SingleMu_optimize_mu_Run2012_qcd.root", "READ");
      TH2F *qcd_TH2F_temp = (TH2F*) gDirectory->Get(TH2Fnames[i]);
      if (dosub) {
	for (int j=0; j<9; j++){
	  qcd_files[j+1] = TFile::Open(MC_array[j]+"_optimize_mu_qcd.root", "READ");
	  qcd_his_array[j] = (TH2F*) gDirectory->Get(TH2Fnames[i]);
	  qcd_his_array[j]->Scale(weight[j]);
	  qcd_TH2F_temp->Add(qcd_his_array[j], -1);
	}
      }
      
      // Create plots
      TCanvas *CanvasTemp = new TCanvas("CanvasTemp","CanvasTemp",900,700);
      gStyle->SetOptStat(0);
      
      CanvasTemp->Divide(2,2);
      
      CanvasTemp->cd(1);
      gStyle->SetOptStat(0);
      TTjets_TH2F_temp->GetXaxis()->SetTitleSize(0.05);
      TTjets_TH2F_temp->GetYaxis()->SetTitleOffset(1.1);
      TTjets_TH2F_temp->GetYaxis()->SetTitleSize(0.05);
      TTjets_TH2F_temp->Draw("COLZ");
      TTjets_TH2F_temp->SetTitle(TH2Fnames[i]+", TTjets");
      CanvasTemp->Update();
      
      CanvasTemp->cd(2);
      gStyle->SetOptStat(0);
      stop_TH2F_temp->GetXaxis()->SetTitleSize(0.05);
      stop_TH2F_temp->GetYaxis()->SetTitleOffset(1.1);
      stop_TH2F_temp->GetYaxis()->SetTitleSize(0.05);
      stop_TH2F_temp->Draw("COLZ");
      stop_TH2F_temp->SetTitle(TH2Fnames[i]+" , single top");
      CanvasTemp->Update();
      
      CanvasTemp->cd(3);
      gStyle->SetOptStat(0);
      wjets_TH2F_temp->GetXaxis()->SetTitleSize(0.05);
      wjets_TH2F_temp->GetYaxis()->SetTitleOffset(1.1);
      wjets_TH2F_temp->GetYaxis()->SetTitleSize(0.05);
      wjets_TH2F_temp->Draw("COLZ");
      wjets_TH2F_temp->SetTitle(TH2Fnames[i]+", wjets");
      CanvasTemp->Update();
      
      CanvasTemp->cd(4);
      gStyle->SetOptStat(0);
      qcd_TH2F_temp->GetXaxis()->SetTitleSize(0.05);
      qcd_TH2F_temp->GetYaxis()->SetTitleOffset(1.1);
      qcd_TH2F_temp->GetYaxis()->SetTitleSize(0.05);
      qcd_TH2F_temp->Draw("COLZ");
      qcd_TH2F_temp->SetTitle(TH2Fnames[i]+", QCD");
      qcd_TH2F_temp->SetMinimum(0.);
      CanvasTemp->Update();
      
      CanvasTemp->SaveAs(TH2Fnames[i]+"_plot.root");
      
      CanvasTemp->Close();
    }
  }

  // Do 1D plots here
  if (dowhich == "TH1F" or dowhich == "all"){
    TString TH1Fnames[9] = {"LEPMET_0tag", "HT_0tag", "HTLEP_0tag", "MET_0tag", 
			    "LEPMET_btag", "HT_btag", "HTLEP_btag", "MET_btag", "BtagJetPt_btag"};

    for (int i=0; i<9; i++){
      TFile* sig_files[3];
      TH1F** sig_his_array = new TH1F*[3];
      TFile* bkg_nom_files[7];
      TH1F** bkg_nom_his_array = new TH1F*[7];
      TFile* bkg_jerup_files[7];
      TH1F** bkg_jerup_his_array = new TH1F*[7];
      TFile* bkg_jerdn_files[7];
      TH1F** bkg_jerdn_his_array = new TH1F*[7];
      TFile* bkg_jecup_files[7];
      TH1F** bkg_jecup_his_array = new TH1F*[7];
      TFile* bkg_jecdn_files[7];
      TH1F** bkg_jecdn_his_array = new TH1F*[7];
      TFile* sub_files[9];
      TH1F** sub_his_array = new TH1F*[9];
      
      double qcdnorm, qcderr;
      if (i < 4) {
	qcdnorm = qcdnorm_0tag;
	qcderr = qcderr_0tag;
      }
      else {
	qcdnorm = qcdnorm_btag;
	qcderr = qcderr_btag;
      }
      
      // Get signal distribution
      for (int j=0; j<3; j++){
	sig_files[j] = TFile::Open(MC_array[j]+"_optimize_mu_nom.root", "READ");
	sig_his_array[j] = (TH1F*) gDirectory->Get(TH1Fnames[i]);
	sig_his_array[j]->Scale(weight[j]);
      }
      TH1F *sig_temp = (TH1F*)sig_his_array[0]->Clone("sig_temp");
      sig_temp->Add(sig_his_array[1]);
      sig_temp->Add(sig_his_array[2]);
      
      // Get background histograms
      // Get QCD histogram
      TFile* qcd_file = TFile::Open("SingleMu_optimize_mu_Run2012_qcd.root", "READ");
      TH1F *qcd_temp = (TH1F*) gDirectory->Get(TH1Fnames[i]);
      if (dosub) {
	for (int j=0; j<9; j++){
	  sub_files[j] = TFile::Open(MC_array[j]+"_optimize_mu_qcd.root", "READ");
	  sub_his_array[j] = (TH1F*) gDirectory->Get(TH1Fnames[i]);
	  sub_his_array[j]->Scale(weight[j]);
	  qcd_temp->Add(sub_his_array[j], -1);
	}
      }
      qcd_temp->Scale(qcdnorm / qcd_temp->Integral());
      
      TH1F *bkg_temp = (TH1F*)qcd_temp->Clone("bkg_temp");
      TH1F *bkg_jerup_temp = (TH1F*)qcd_temp->Clone("bkg_jerup_temp");
      TH1F *bkg_jerdn_temp = (TH1F*)qcd_temp->Clone("bkg_jerdn_temp");
      TH1F *bkg_jecup_temp = (TH1F*)qcd_temp->Clone("bkg_jecup_temp");
      TH1F *bkg_jecdn_temp = (TH1F*)qcd_temp->Clone("bkg_jecdn_temp");
      
      // Add other backgrounds
      for (int j=0; j<7; j++){
	bkg_nom_files[j] = TFile::Open(MC_array[j+3]+"_optimize_mu_nom.root", "READ");
	bkg_nom_his_array[j] = (TH1F*) gDirectory->Get(TH1Fnames[i]);
	bkg_nom_his_array[j]->Scale(weight[j+3]);
	bkg_temp->Add(bkg_nom_his_array[j]);
	
	bkg_jerup_files[j] = TFile::Open(MC_array[j+3]+"_optimize_mu_jerup.root", "READ");
	bkg_jerup_his_array[j] = (TH1F*) gDirectory->Get(TH1Fnames[i]);
	bkg_jerup_his_array[j]->Scale(weight[j+3]);
	bkg_jerup_temp->Add(bkg_jerup_his_array[j]);
	
	bkg_jerdn_files[j] = TFile::Open(MC_array[j+3]+"_optimize_mu_jerdn.root", "READ");
	bkg_jerdn_his_array[j] = (TH1F*) gDirectory->Get(TH1Fnames[i]);
	bkg_jerdn_his_array[j]->Scale(weight[j+3]);
	bkg_jerdn_temp->Add(bkg_jerdn_his_array[j]);
	
	bkg_jecup_files[j] = TFile::Open(MC_array[j+3]+"_optimize_mu_jecup.root", "READ");
	bkg_jecup_his_array[j] = (TH1F*) gDirectory->Get(TH1Fnames[i]);
	bkg_jecup_his_array[j]->Scale(weight[j+3]);
	bkg_jecup_temp->Add(bkg_jecup_his_array[j]);
	
	bkg_jecdn_files[j] = TFile::Open(MC_array[j+3]+"_optimize_mu_jecdn.root", "READ");
	bkg_jecdn_his_array[j] = (TH1F*) gDirectory->Get(TH1Fnames[i]);
	bkg_jecdn_his_array[j]->Scale(weight[j+3]);
	bkg_jecdn_temp->Add(bkg_jecdn_his_array[j]);
      }
      
      cout << "Number of background events: " << bkg_temp->Integral() << endl;
      
      // Calculate significance plot
      double nbins = sig_temp->GetNbinsX();
      double xmin = sig_temp->GetXaxis()->GetXmin();
      double xmax = sig_temp->GetXaxis()->GetXmax();
      TH1F* sig_plot = new TH1F("sig_plot", "sig_plot", nbins, xmin, xmax);
      for (int ii = 0; ii<nbins; ii++){
	double nsig = sig_temp->Integral(ii+1, nbins);
	double nbkg = bkg_temp->Integral(ii+1, nbins);
	double dBjerup = abs(nbkg - bkg_jerup_temp->Integral(ii+1, nbins));
	double dBjerdn = abs(nbkg - bkg_jerdn_temp->Integral(ii+1, nbins));
	double dBjer = max(dBjerup, dBjerdn);
	double dBjecup = abs(nbkg - bkg_jecup_temp->Integral(ii+1, nbins));
	double dBjecdn = abs(nbkg - bkg_jecdn_temp->Integral(ii+1, nbins));
	double dBjec = max(dBjecup, dBjecdn);
	double dBqcd = qcderr / qcdnorm * qcd_temp->Integral(ii+1, nbins);
	double dB = dBjer + dBjec + dBqcd;
	double sigma = 0.;
	if ((nbkg + nsig + dB) > 0.){
	  sigma = nsig / sqrt( nsig + nbkg + dB);
	}
	sig_plot->SetBinContent(ii, sigma);
      }
      int maxbin = sig_plot->GetMaximumBin();
      double cutval = sig_plot->GetBinLowEdge(maxbin);
      cout << " The optimal cut for " << TH1Fnames[i] << " is at " << cutval << endl;
      
      TCanvas *CanvasTemp = new TCanvas("CanvasTemp","CanvasTemp",1200,600);
      gStyle->SetOptStat(0);
      CanvasTemp->Divide(2,1);
      
      CanvasTemp->cd(1);
      gStyle->SetOptStat(0);
      sig_temp->SetLineColor(kRed);
      sig_temp->SetLineWidth(3);
      bkg_temp->SetLineColor(kBlue);
      bkg_temp->SetLineWidth(3);
      bkg_jerup_temp->SetLineColor(kBlue+3);
      bkg_jerup_temp->SetLineWidth(3);
      bkg_jerup_temp->SetLineStyle(2);
      bkg_jerdn_temp->SetLineColor(kBlue+3);
      bkg_jerdn_temp->SetLineWidth(3);
      bkg_jerdn_temp->SetLineStyle(3);
      bkg_jecup_temp->SetLineColor(kBlue-3);
      bkg_jecup_temp->SetLineWidth(3);
      bkg_jecup_temp->SetLineStyle(2);
      bkg_jecdn_temp->SetLineColor(kBlue-3);
      bkg_jecdn_temp->SetLineWidth(3);
      bkg_jecdn_temp->SetLineStyle(3);
      double s_max = sig_temp->GetMaximum();
      double b_max = bkg_temp->GetMaximum();
      double comb_max = max(s_max, b_max);
      sig_temp->SetMaximum(1.2*comb_max);
      sig_temp->GetYaxis()->SetTitleOffset(1.0);
      sig_temp->Draw();
      bkg_temp->Draw("same");
      bkg_jerup_temp->Draw("same");
      bkg_jerdn_temp->Draw("same");
      bkg_jecup_temp->Draw("same");
      bkg_jecdn_temp->Draw("same");

      TLegend* leg = new TLegend(0.56, 0.5, 0.86, 0.82);
      leg->SetBorderSize(0);
      leg->SetTextFont(42);
      leg->SetFillColor(0);
      leg->AddEntry(sig_temp, " Signal", "L");
      leg->AddEntry(bkg_temp, " Background", "L");
      leg->AddEntry(bkg_jerup_temp, " Background + jerup", "L");
      leg->AddEntry(bkg_jerdn_temp, " Background + jerdn", "L");
      leg->AddEntry(bkg_jecup_temp, " Background + jecup", "L");
      leg->AddEntry(bkg_jecdn_temp, " Background + jecdn", "L");
      leg->SetTextSize(0.04);
      leg->Draw("same");
      CanvasTemp->Update();
      
      CanvasTemp->cd(2);
      gStyle->SetOptStat(0);
      sig_plot->SetMarkerStyle(20);
      sig_plot->SetMarkerSize(1.2);
      sig_plot->GetYaxis()->SetTitle("Significance");
      sig_plot->GetYaxis()->SetTitleOffset(1.0);
      sig_plot->GetXaxis()->SetTitle(sig_temp->GetXaxis()->GetTitle());
      sig_plot->Draw();
      CanvasTemp->Update();
      
      CanvasTemp->SaveAs(TH1Fnames[i]+"_plot.root");
      CanvasTemp->Close();
    }
  }

  return 0;
}
