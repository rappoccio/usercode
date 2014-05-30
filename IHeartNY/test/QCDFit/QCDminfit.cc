/*
QCDminfit_sub.cc performs a maximum likelihood fit in the MET distribution to determine the amount of QCD background. The fit parameters
are the number of ttbar, single top, w+jets, and QCD events in the sample. These are used to normalize the respective templates in order
to fit the MET distribution in data. Templates are taken from the MET histograms produced by plotMET.py, normalized to 1. The QCD template
is further modified by subtracting the ttbar and w+jets sidebands before the normalization. The fit may be performed for any of the njets
bins, or njets inclusive.

The fit is performed using a direct interface with TMinuit, where the function TMinuit minimizes is fcn = -2*log(L). The factor of -2
allows for easy insertion of constraints, through adding quadratic terms to fcn.
For more info on TMinuit see root.cern.ch/root/html/TMinuit.html .

The inputs to be changed when running the program are found in lines 60, 78, and 79. Line 60 gives the rebinning factor (number of bins
in the original histogram to be combined before the fit) and 78, 79 give the njets bin and cutflow stage used to select the histograms
for the fit.

*/

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
#include <TAxis.h>
#include <TLine.h>
#include <TMath.h>
#include <THStack.h>
#include <sstream>
#include "TLatex.h"
#include "TText.h"
#include "TLegend.h"
#include "TFile.h"
#include "TGraphAsymmErrors.h"
#include "TH1D.h"
#include "TH1.h"

//#include "tdrstyle.C"

using namespace std;
// Declare pointer to data as global (not elegant but TMinuit needs this).
vector<int> data_Vec; //input data
vector<double> top_Vec; //ttbar+stop template from MC
vector<double> qcd_Vec; //qcd template from data driven method

double L = 19748; //UPDATED (in pb)

int Ntotal; //Total # of events -- define as global, currently rewritten for each Njets bin
int nbins = 200;
double xmin = 0.;
double xmax = 400.;

// Rebinning factor, giving number of bins to combine into one (1 means no rebinning).
int binfac = 40;
TString binsize = "80";
TString numberofbins = "5";

double numEvent[2]; //set it global use to set limit in fcn

// Helper functions
void fcn(int& npar, double* deriv, double& f, double par[], int flag);
void getData(TString& temp_num, int binfac);
double* getTemp(TString& temp_num, int binfac, bool dosub);
double* getWeightArray();

TText* doPrelim(float luminosity, float x, float y);

//-------------------------------------------------------------------------
int QCDminfit() {

  cout << "Beginning QCD normalization..." << endl;

  // User inputs
  TString temp_num = "7";
  bool dosub = true;

  int nbins_new = nbins / binfac;
  cout << "New # of bins is " << nbins_new << endl;
  cout << "Fitting ptMET" << temp_num << endl;

  getData(temp_num, binfac);
  double * ini_val = getTemp(temp_num, binfac, dosub);
  
  // Initialize minuit, set initial values etc. of parameters.
  const int npar = 2; // the number of parameters
  TMinuit minuit(npar);
  minuit.SetFCN(fcn);
  // SetPrintLevel: 1 verbose, 0 normal, -1 quiet
  minuit.SetPrintLevel(1);
  minuit.SetErrorDef(0.5); //because is NLL
  
  int ierflg = 0;
  string parName[npar] = {"top", "qcd"};
  double par[npar];
  
  //for(int i=0; i<npar; i++){
    // use the MC estimations for the normalization start values,
    // but correct if out of range.
    //if (ini_val[i] < 0.) {
    //  par[i] = 0.;
    //  numEvent[i] = 0.;
    //}
    
    //else if (ini_val[i] >= Ntotal) {
    //  par[i] = Ntotal - 1.;
    //  numEvent[i] = Ntotal - 1.;
    //}
    
    //else {
    //  par[i] = ini_val[i];
    //  numEvent[i] = ini_val[i];
    //}
  //}
  par[0] = 0.5 * Ntotal;
  par[1] = 0.5 * Ntotal;
  numEvent[0] = 0.5 * Ntotal;
  numEvent[1] = 0.5 * Ntotal;

  for(int i=0; i<npar; i++){
    // optimize parameters with initial value of par[i], moving in increments
    // of 1., between 0 and Ntotal
    minuit.mnparm(i, parName[i], par[i], 1., 0, Ntotal, ierflg);
  }
  
  // 1 standard
  // 2 try to improve minimum (slower)
  double arglist[10];
  arglist[0]=2;
  double arglist2[10];
  arglist[0]=10000;
  arglist[1]=2.;
  double arglist3[10];
  arglist[0]=10000;
  arglist[1]=2;
  minuit.mnexcm("SET STR",arglist,1,ierflg);
  minuit.mnexcm("MIGRAD",arglist2,2,ierflg);
  minuit.mnexcm("MINOS", arglist3,3,ierflg);
  // minuit.Migrad();
  
  double outpar[npar], err[npar];
  
  for (int i=0; i<npar; i++){
    minuit.GetParameter(i,outpar[i],err[i]);
  }
  
  // Plot the result.
  TH1F* result = new TH1F("result", "", nbins_new, xmin, xmax);
  TH1F* data = new TH1F("data", "", nbins_new, xmin, xmax);
  
  //ttbar, stop, wjets, and qcd contribution
  TH1F* his_Con[2];
  TH1F* his_Temp[2];
  TString sample_names_array[2] = {"top", "qcd"};
  
  for(int i=0; i<2; i++){
    his_Con[i] = new TH1F(sample_names_array[i]+"_Con", "", nbins_new, xmin, xmax);
    his_Temp[i] = new TH1F(sample_names_array[i]+"_Temp", "", nbins_new, xmin, xmax);
  }
  
  THStack* hs = new THStack("hs","stacked histograms");
  
  for (int i=0; i<nbins_new; i++){
    
    data->SetBinContent(i+1, data_Vec[i]);
    
    double mean, top_con, qcd_con;
    
    top_con = outpar[0]*top_Vec[i];
    qcd_con = outpar[1]*qcd_Vec[i];
    
    mean = top_con + qcd_con;
    result->SetBinContent(i+1, mean); //fitting results
    his_Con[0]->SetBinContent(i+1, top_con);
    his_Con[1]->SetBinContent(i+1, qcd_con);
    his_Temp[0]->SetBinContent(i+1, top_Vec[i]);
    his_Temp[1]->SetBinContent(i+1, qcd_Vec[i]);
    
  }
  
  double pplus, pminus, pparab, pgcc;
  minuit.mnerrs(2, pplus, pminus, pparab, pgcc);
    
  //print out the results
  cout << " When fitting ptMET" << temp_num << ", the fitting results were" << endl;
  cout << " \t top \t qcd"<<endl;

  cout <<" Before fit "<< ini_val[0]<<" \t "<<ini_val[1]<<std::endl;
  cout <<" After fit "<<outpar[0]<<" +- "<<err[0]<<" \t "<<outpar[1]<<" +- "<<err[1]<<endl;
  cout <<" MINOS errors are +"<<pplus<<", -"<<pminus<<", "<<pparab<<" parabolic and "<<pgcc<<" gcc"<<endl;
  
  //make template plots
  TCanvas* canvasTemp = new TCanvas("canvasTemp", "canvasTemp", 700, 500);
  
  his_Temp[0]->SetLineColor(kRed+1);
  his_Temp[1]->SetLineColor(kOrange);
  
  his_Temp[0]->SetLineWidth(5);
  his_Temp[1]->SetLineWidth(5);
  
  gStyle->SetOptStat(0);
  his_Temp[0]->SetTitle("");
  his_Temp[0]->Draw();
  double sigmax = his_Temp[0]->GetMaximum();
  double qcdmax = his_Temp[1]->GetMaximum();
  his_Temp[0]->SetMaximum(1.2 * max(sigmax, qcdmax));
  his_Temp[0]->GetXaxis()->SetTitleSize(0.05);
  
  his_Temp[1]->Draw("same");
  
  TLegend* legTemp = new TLegend(0.53, 0.45, 0.73, 0.8);
  legTemp->SetBorderSize(0);
  legTemp->SetTextFont(42);
  legTemp->SetFillColor(0);
  legTemp->AddEntry(his_Temp[0], " top", "L");
  legTemp->AddEntry(his_Temp[1], " QCD", "L");
  
  legTemp->SetTextSize(0.045);
  legTemp->Draw("same");
  TText* textPrelimA = doPrelim(L/1000, 0.525, 0.915);
  textPrelimA->Draw();
  textPrelimA->SetTextFont(42);

  //canvasTemp->Update();
  //canvasTemp->SaveAs("Temp_"+binsize+"b_"+temp_num+".png");

  //make fit plot
  TCanvas* canvasFit = new TCanvas("canvasFit", "canvasFit", 700, 500);
  
  his_Con[0]->SetFillColor(kRed+1);
  his_Con[1]->SetFillColor(kYellow);
  
  hs->Add(his_Con[1]);
  hs->Add(his_Con[0]);
  result->SetLineStyle(1); // 1 = solid, 2 = dashed, 3 = dotted
  result->SetLineColor(kBlue); // black (default)
  result->SetLineWidth(3);
  
  data->Sumw2();
  data->SetMarkerStyle(20);
  data->SetMarkerSize(1.2);
  data->SetLineWidth(1);
  
  hs->SetTitle("");
  double h_max = data->GetMaximum();
  double f_max = result->GetMaximum();
  double comb_max = max(h_max, f_max);
  hs->Draw();
  hs->SetMaximum(1.2*comb_max);
  hs->GetXaxis()->SetTitle("missing E_{T} (GeV)");
  hs->GetYaxis()->SetTitle("Number of Events / "+binsize+" GeV");
  hs->GetXaxis()->SetTitleSize(0.05);
  hs->GetYaxis()->SetTitleSize(0.05);
  hs->GetYaxis()->SetTitleOffset(1.0);
  result->Draw("same");
  data->Draw("same");
  
  TLegend* legFit = new TLegend(0.56, 0.5, 0.86, 0.82);
  legFit->SetBorderSize(0);
  legFit->SetTextFont(42);
  legFit->SetFillColor(0);
  legFit->AddEntry(data , " Data", "LPE");
  legFit->AddEntry(result , " Fit", "L");
  legFit->AddEntry(his_Con[0], " top", "F");
  legFit->AddEntry(his_Con[1], " QCD", "F");
  legFit->SetTextSize(0.04);
  legFit->Draw("same");
  
  TText* textPrelimB = doPrelim(L/1000, 0.525, 0.915);
  textPrelimB->Draw();
  textPrelimB->SetTextFont(42);
  gPad->RedrawAxis();
  
  //canvasFit->Update();
  //canvasFit->SaveAs("Fit_"+binsize+"b_"+temp_num+".png");
   
  cout << "To exit, quit ROOT from the File menu of the plot" << endl;
  return 0;
  
}

//-------------------------------------------------------------------------
double* getWeightArray(){

  double xs_array[13], nE_array[13];
  double* weight_array = new double[13];

  xs_array[0] = 245.8; //TTjets 0-700
  nE_array[0] = 21675970;
  xs_array[1] = 245.8; //TTjets 700-1000
  nE_array[1] = 3082812;
  xs_array[2] = 245.8; //TTjets 1000-Inf
  nE_array[2] = 1249111;
  xs_array[3] = 245.8; //TTjets 0-700 notSemiLep
  nE_array[3] = 21675970;
  xs_array[4] = 245.8; //TTjets 700-1000 notSemiLep
  nE_array[4] = 3082812;
  xs_array[5] = 245.8; //TTjets 1000-Inf notSemiLep
  nE_array[5] = 1249111;
  xs_array[6] = 11.1; //St_tW
  nE_array[6] = 497658;
  xs_array[7] = 11.1; //St_tWB
  nE_array[7] = 493460;
  xs_array[8] = 56.4; //St_t
  nE_array[8] = 3758227;
  xs_array[9] = 30.7; //St_tB
  nE_array[9] = 1935072;
  xs_array[10] = 3.79; //St_s
  nE_array[10] = 259961;
  xs_array[11] = 1.76; //St_sB
  nE_array[11] = 139974;
  xs_array[12] = 36703.2; //Wjets
  nE_array[12] = 57709905;

  weight_array[0] = xs_array[0]*L/nE_array[0]; //TTjets 0-700
  weight_array[1] = xs_array[1]*L*0.074/nE_array[1]; //TTjets 700-1000
  weight_array[2] = xs_array[2]*L*0.014/nE_array[2]; //TTjets 1000-Inf
  weight_array[3] = xs_array[3]*L/nE_array[3]; //TTjets 0-700 nonSemiLep
  weight_array[4] = xs_array[4]*L*0.074/nE_array[4]; //TTjets 700-1000 nonSemiLep
  weight_array[5] = xs_array[5]*L*0.014/nE_array[5]; //TTjets 1000-Inf nonSemiLep
  weight_array[6] = xs_array[6]*L/nE_array[6]; //St_tW
  weight_array[7] = xs_array[7]*L/nE_array[7]; //St_tWB
  weight_array[8] = xs_array[8]*L/nE_array[8]; //St_t
  weight_array[9] = xs_array[9]*L/nE_array[9]; //St_tB
  weight_array[10] = xs_array[10]*L/nE_array[10]; //St_s
  weight_array[11] = xs_array[11]*L/nE_array[11]; //St_sB
  weight_array[12] = xs_array[12]*L/nE_array[12]; //Wjets
  
  return weight_array;

}



// function to read in the data from a histogram
void getData(TString& temp_num, int binfac){

  int nbins_new = nbins / binfac;
  TH1D* h_data = new TH1D("data", "data", nbins, xmin, xmax);
  TFile* datafile = TFile::Open("../histfiles/SingleMu_iheartNY_V1_mu_Run2012_nom.root", "READ");
  h_data = (TH1D*) gDirectory->Get("ptMET"+temp_num);
  h_data->Rebin(binfac);

  // Write histogram to data vector, calc total # of events
  for(int ibin=0; ibin<nbins_new; ibin++){
    int nn = h_data->GetBinContent(ibin+1);
    data_Vec.push_back(nn);
    Ntotal += nn;
  }
  cout << "Number of data events: " << h_data->Integral() << endl;

}

// Function to produce the top and QCD templates
double* getTemp(TString& temp_num, int binfac, bool dosub){

  double* ini_val = new double[2];
  TString top_array[13] = {"TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom",
			   "TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom",
			   "TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom",
			   "TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom",
			   "TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom",
			   "TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom",
			   "T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom",
			   "Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom",
			   "T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom",
			   "Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom",
			   "T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom",
			   "Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom",
			   "WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu_nom"};

  TString qcd_array[14] = {"SingleMu_iheartNY_V1_mu_Run2012_qcd",
			   "TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd",
			   "TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd",
			   "TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd",
			   "TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd",
			   "TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd",
			   "TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd",
			   "T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd",
			   "Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd",
			   "T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd",
			   "Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd",
			   "T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd",
			   "Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd",
			   "WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu_qcd"};

  TString shortnames[13] = {"TTbar_m0to700", "TTbar_m700to1000", "TTbar_m1000toInf", "TTbar_nonSemiLep_m0to700", 
			    "TTbar_nonSemiLep_m700to1000", "TTbar_nonSemiLep_m1000toInf",
			    "St_tW", "St_tWB", "St_t", "St_tB", "St_s", "St_sB", "WJets"};

  TString sample_com_array[2] = {"top", "qcd"};
  TH1D** top_his_array = new TH1D*[13];
  TH1D** qcd_his_array = new TH1D*[14];
  TH1D** his_com_array = new TH1D*[2];
  TFile* top_file_array[13];
  TFile* qcd_file_array[14];

  double* weight = getWeightArray();
  int nbins_new = nbins / binfac;

  for(int i=0; i<2; i++){
    his_com_array[i] = new TH1D(sample_com_array[i], sample_com_array[i], nbins_new, xmin, xmax);
  }
  
  // Get top template
  for(int i=0; i<13; i++){
    top_file_array[i] = TFile::Open("../histfiles/"+top_array[i]+".root", "READ");
    top_his_array[i] = (TH1D*) gDirectory->Get("ptMET"+temp_num);
    top_his_array[i]->Rebin(binfac);
    double nraw = top_his_array[i]->Integral();
    top_his_array[i]->Scale(weight[i]);
    double nscale = top_his_array[i]->Integral();
    his_com_array[0]->Add(top_his_array[i]);
    cout << "Contribution from " << shortnames[i] << " is " << nraw << " before normalization and " 
	 << nscale << " after." << endl;
  }
  
  // Get qcd template
  qcd_file_array[0] = TFile::Open("../histfiles/"+qcd_array[0]+".root", "READ");
  qcd_his_array[0] = (TH1D*) gDirectory->Get("ptMET"+temp_num);
  qcd_his_array[0]->Rebin(binfac);
  his_com_array[1]->Add(qcd_his_array[0]);
  cout << "There are " << qcd_his_array[0]->Integral() << " events in the data sideband " << endl;
  if (dosub) {
    for(int i=0; i<13; i++){
      qcd_file_array[i+1] = TFile::Open("../histfiles/"+qcd_array[i+1]+".root", "READ");
      qcd_his_array[i+1] = (TH1D*) gDirectory->Get("ptMET"+temp_num);
      qcd_his_array[i+1]->Rebin(binfac);
      double nraw = qcd_his_array[i+1]->Integral();
      qcd_his_array[i+1]->Scale(weight[i]);
      double nscale = qcd_his_array[i+1]->Integral();
      his_com_array[1]->Add(qcd_his_array[i+1], -1);
      cout << "Contribution from " << shortnames[i] << " in sideband is " << nraw << " before normalization and " 
	   << nscale << " after." << endl;    
    }
  }


  // Normalize histograms to 1 (but first determine Nexp)
  ini_val[0] = his_com_array[0]->Integral();
  ini_val[1] = Ntotal - ini_val[0];
  if (ini_val[1] < 0.) ini_val[1] = 0.;

  his_com_array[0]->Scale(1./his_com_array[0]->Integral());
  his_com_array[1]->Scale(1./his_com_array[1]->Integral());

  // write histograms to corresponding vectors
  for(int ibin=0; ibin<nbins_new; ibin++){

    double top = his_com_array[0]->GetBinContent(ibin+1);
    top_Vec.push_back(top);
    
    double qcd = his_com_array[1]->GetBinContent(ibin+1);
    qcd_Vec.push_back(qcd);
     
  }

  return ini_val;
   
}

//-------------------------------------------------------------------------

// fcn passes back f = - 2*ln(L), the function to be minimized.
void fcn(int& npar, double* deriv, double& f, double par[], int flag){

  double lnL = 0.0;

  int nbins_new = nbins / binfac;

  for (int i=0; i<nbins_new; i++){

    //data_i is the observed number of events in each bin
    int data_i = data_Vec[i];

    //xi is the expected number of events in each bin
    double xi = par[0]*top_Vec[i] + par[1]*qcd_Vec[i];

    lnL += log(TMath::Poisson(data_i, xi));
    
  }

  f = -2.0 * lnL;

  //Single top constraint
  //double nstop_err = numEvent[1]*0.1;

  //f += (par[1]-numEvent[1])*(par[1]-numEvent[1])/nstop_err/nstop_err;

}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
TText* doPrelim(float luminosity, float x, float y)
{
 std::ostringstream stream;
 
 stream <<"CMS Preliminary, L = " << luminosity << " fb^{-1}";
 
 TLatex* text = new TLatex(x, y, stream.str().c_str());

 text->SetNDC(true);
 text->SetTextFont(62);
 text->SetTextSize(0.04);
 return text;
}
