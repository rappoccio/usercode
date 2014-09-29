/* 
QCDminfit_sub.cc performs a maximum likelihood fit in the MET distribution to determine the amount of QCD background.  The fit parameters 
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
vector<double> qcd_Vec;   //qcd template from data driven method

double L = 19748; //UPDATED (in pb)
double trig_eff = 0.93;
double btag_eff = 0.97;

int Ntotal; //Total # of events -- define as global, currently rewritten for each Njets bin
int nbins = 40; 
double xmin = 0.;
double xmax = 400.; 

// Rebinning factor, giving number of bins to combine into one (1 means no rebinning).
int binfac = 10;

double numEvent[2]; //set it global use to set limit in fcn

// Helper functions
void fcn(int& npar, double* deriv, double& f, double par[], int flag);
void getData(TString& jet_num, TString& temp_num, int binfac);
double* getTemp(TString& jet_num, TString& temp_num, int binfac, TString& ttjetsType);
double* getWeightArray(TString& ttjetsType);

TText* doPrelim(float luminosity, TString& jet_num, float x, float y);

//-------------------------------------------------------------------------
int QCDminfit_comb() {

  cout << "Beginning QCD normalization..." << endl;

  // User inputs
  TString jet_num = "all";
  TString temp_num = "";
  TString ttjetsType = "POWHEG";

  int nbins_new = nbins / binfac;
  cout << "New # of bins is " << nbins_new << endl;
  cout << "Running in Njets = " << jet_num << " bin, using MET template " << temp_num << endl;

  getData(jet_num, temp_num, binfac);
  double * ini_val = getTemp(jet_num, temp_num, binfac, ttjetsType);
  
  // Initialize minuit, set initial values etc. of parameters.
  const int npar = 2;              // the number of parameters
  TMinuit minuit(npar);
  minuit.SetFCN(fcn);
  // SetPrintLevel: 1 verbose, 0 normal, -1 quiet
  minuit.SetPrintLevel(1);
  minuit.SetErrorDef(1.);
  
  int ierflg = 0;
  string parName[npar] = {"top", "qcd"};
  double par[npar];
  
  for(int i=0; i<npar; i++){
    // use the MC estimations for the normalization start values,
    // but correct if out of range.
    if (ini_val[i] < 0.) { 
      par[i] = 0.;      
      numEvent[i] = 0.;
    }
    
    else if (ini_val[i] >= Ntotal) {
      par[i] = Ntotal - 1.;      
      numEvent[i] = Ntotal - 1.;
    }
    
    else {
      par[i] = ini_val[i];      
      numEvent[i] = ini_val[i];
    }
  }

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
  minuit.mnexcm("SET STR",arglist,1,ierflg);
  minuit.mnexcm("MIGRAD",arglist2,2,ierflg);
  //  minuit.Migrad();
  
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
    qcd_con   = outpar[1]*qcd_Vec[i];
    
    mean = top_con + qcd_con;
    result->SetBinContent(i+1, mean); //fitting results
    his_Con[0]->SetBinContent(i+1, top_con);
    his_Con[1]->SetBinContent(i+1, qcd_con);
    his_Temp[0]->SetBinContent(i+1, top_Vec[i]);
    his_Temp[1]->SetBinContent(i+1, qcd_Vec[i]);
    
  }
    
  //print out the results
  cout << " In the Njets = " << jet_num << " bin, for MET template " << temp_num << ", using " << ttjetsType << " for TTJets MC, the fitting results were" << endl;
  cout << " \t top \t qcd"<<endl;

  cout <<" Before fit "<< ini_val[0]<<" \t "<<ini_val[1]<<std::endl;
  cout <<" After fit "<<outpar[0]<<" +- "<<err[0]<<" \t "
       <<outpar[1]<<" +- "<<err[1]<<endl;
  
  //make template plots
  TCanvas* canvasTemp = new TCanvas("canvasTemp", "canvasTemp", 700, 500);
  
  his_Temp[0]->SetLineColor(kRed+1);
  his_Temp[1]->SetLineColor(kGreen-3);
  
  his_Temp[0]->SetLineWidth(5);
  his_Temp[1]->SetLineWidth(5);
  
  gStyle->SetOptStat(0);
  his_Temp[0]->SetTitle("");
  his_Temp[0]->Draw();
  his_Temp[0]->SetMaximum(1.0);
  his_Temp[0]->GetXaxis()->SetTitle("missing E_{T} (GeV)");
  
  his_Temp[1]->Draw("same");
  
  TLegend* legTemp = new TLegend(0.53, 0.45, 0.73, 0.8);
  legTemp->SetBorderSize(0);
  legTemp->SetTextFont(42);
  legTemp->SetFillColor(0);
  legTemp->AddEntry(his_Temp[0], " top", "L");
  legTemp->AddEntry(his_Temp[1], " QCD", "L");
  
  legTemp->SetTextSize(0.045);
  legTemp->Draw("same");
  TText* textPrelim1 = doPrelim(L/1000, jet_num, 0.46,0.96);
  textPrelim1->Draw();
  textPrelim1->SetTextFont(42);
  //make fit plot
  TCanvas* canvasFit = new TCanvas("canvasFit", "canvasFit", 700, 500);
  
  his_Con[0]->SetFillColor(kRed+1);
  his_Con[1]->SetFillColor(kGreen-3);
  
  hs->Add(his_Con[1]);
  hs->Add(his_Con[0]);
  result->SetLineStyle(1);             //  1 = solid, 2 = dashed, 3 = dotted
  result->SetLineColor(kViolet-3);    //  black (default)
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
  //  hs->GetYaxis()->SetTitle("Number of Events");
  result->Draw("same");
  data->Draw("same");
  
  TLegend* legFit = new TLegend(0.56, 0.5, 0.86, 0.82);
  legFit->SetBorderSize(0);
  legFit->SetTextFont(42);
  legFit->SetFillColor(0);
  legFit->AddEntry(data     , " Data", "LPE");
  legFit->AddEntry(result   , " Fit", "L");
  legFit->AddEntry(his_Con[0], " top", "F");
  legFit->AddEntry(his_Con[1], " QCD", "F");
  legFit->SetTextSize(0.04);
  legFit->Draw("same");
  
  TText* textPrelim = doPrelim(L/1000, jet_num, 0.46,0.96);
  textPrelim->Draw();
  textPrelim->SetTextFont(42);
  gPad->RedrawAxis();
  
   
  cout << "To exit, quit ROOT from the File menu of the plot" << endl;
  return 0;
  
}

//-------------------------------------------------------------------------
double* getWeightArray(TString& ttjetsType){

  double xs_array[8], nE_array[8];
  double* weight_array = new double[8];
  // Xsec, Ngen taken from elog. All Xsec in pb.
  if (ttjetsType == "NLO"){
    weight_array[0] = L * trig_eff * btag_eff * 234 / 32575025;
  }
  if (ttjetsType == "POWHEG"){
    weight_array[0] = L * trig_eff * btag_eff * 234 / 21560109;
  }
  if (ttjetsType == "SEMI"){
    weight_array[0] = L * trig_eff * btag_eff * 103 / 25273288;
  }
  if (ttjetsType == "LEP"){
    weight_array[0] = L * trig_eff * btag_eff * 24.8 / 12043695;
  }

  // All numbers have been modified re: Kevin's email, 08/20/13
  xs_array[1] = 11.1;  //St_tW
  nE_array[1] = 495559;
  xs_array[2] = 11.1;  //St_tWB
  nE_array[2] = 491463;
  xs_array[3] = 56.4;  //St_t
  nE_array[3] = 3748155;
  xs_array[4] = 30.7;  //St_tB
  nE_array[4] = 1930185;
  xs_array[5] = 3.79;  //St_s
  nE_array[5] = 259176;
  xs_array[6] = 1.76;  //St_sB
  nE_array[6] = 139604;
  xs_array[7] = 37509.0; //wjets     
  nE_array[7] = 57653686;

  weight_array[1] = xs_array[1]*L*trig_eff*btag_eff/nE_array[1]; //St_tW
  weight_array[2] = xs_array[2]*L*trig_eff*btag_eff/nE_array[2]; //St_tWB
  weight_array[3] = xs_array[3]*L*trig_eff*btag_eff/nE_array[3]; //St_t
  weight_array[4] = xs_array[4]*L*trig_eff*btag_eff/nE_array[4]; //St_tB
  weight_array[5] = xs_array[5]*L*trig_eff*btag_eff/nE_array[5]; //St_s
  weight_array[6] = xs_array[6]*L*trig_eff*btag_eff/nE_array[6]; //St_sB
  weight_array[7] = xs_array[7]*L*trig_eff*btag_eff/nE_array[7]; //wjets
  
  return weight_array;

}



//  function to read in the data from a histogram
void getData(TString& jet_num, TString& temp_num, int binfac){

  int nbins_new = nbins / binfac;
  TH1D* h_data = new TH1D("data", "data", nbins, xmin, xmax);
  TFile* datafile = TFile::Open("Data_Var.root", "READ");
  if (jet_num == "all") {
    h_data = (TH1D*) gDirectory->Get("histMET"+temp_num);
  }
  else {
    h_data = (TH1D*) gDirectory->Get("histMET"+jet_num+"j"+temp_num);
  }
  h_data->Rebin(binfac);

  // Write histogram to data vector, calc total # of events
  for(int ibin=0; ibin<nbins_new; ibin++){
    int nn = h_data->GetBinContent(ibin+1);
    data_Vec.push_back(nn);
    Ntotal += nn;
  }

}

// Function to produce the top and QCD templates
double* getTemp(TString& jet_num, TString& temp_num, int binfac, TString& ttjetsType){

  double* ini_val = new double[2];
  TString sample_array[10] = {"TTjets_POWHEG_Var", "TTjets_POWHEG_old_Var", "St_tW_Var", "St_tWB_Var", "St_t_Var", "St_tB_Var", "St_s_Var", "St_sB_Var", "WJets_old_Var", "QCD_old_Var"};
  TString sample_com_array[2] = {"top", "qcd"};
  TH1D** his_array = new TH1D*[10];
  TH1D** his_com_array = new TH1D*[2];
  TFile* file_array[10];

  double* weight = getWeightArray(ttjetsType);  
  int nbins_new = nbins / binfac;

  for(int i=0; i<2; i++){
    his_com_array[i] = new TH1D(sample_com_array[i], sample_com_array[i], nbins_new, xmin, xmax);
  }
  
  for(int i=0; i<10; i++){
    file_array[i] = TFile::Open(sample_array[i]+".root", "READ");
    if (jet_num == "all") {
      his_array[i] = (TH1D*) gDirectory->Get("histMET"+temp_num);
    }
    else {
      his_array[i] = (TH1D*) gDirectory->Get("histMET"+jet_num+"j"+temp_num);
    }

    his_array[i]->Rebin(binfac);
  }
  
  // Rescale and combine histograms
  // ttbar
  his_array[0]->Scale(weight[0]);
  his_com_array[0]->Add(his_array[0]);

  // stop
  his_array[2]->Scale(weight[1]);
  his_com_array[0]->Add(his_array[2]);
  his_array[3]->Scale(weight[2]);
  his_com_array[0]->Add(his_array[3]);
  his_array[4]->Scale(weight[3]);
  his_com_array[0]->Add(his_array[4]);
  his_array[5]->Scale(weight[4]);
  his_com_array[0]->Add(his_array[5]);
  his_array[6]->Scale(weight[5]);
  his_com_array[0]->Add(his_array[6]);
  his_array[7]->Scale(weight[6]);
  his_com_array[0]->Add(his_array[7]);
  
  // qcd
  his_com_array[1]->Add(his_array[9]);
  // Subtract out ttbar and wjets sidebands
  his_array[1]->Scale(weight[0]);
  his_array[8]->Scale(weight[7]);
  his_com_array[1]->Add(his_array[1], -1);
  his_com_array[1]->Add(his_array[8], -1);

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
TText* doPrelim(float luminosity, TString& jet_num, float x, float y)
{
 std::ostringstream stream;
 
 if(jet_num=="ge6"){
   stream  <<"CMS Preliminary, L = " <<  luminosity << " fb^{-1} N_{jets} #geq 6";
 }
 else if(jet_num=="all"){
   stream  <<"CMS Preliminary, L = " <<  luminosity << " fb^{-1}";
 }
 else{
   stream  <<"CMS Preliminary, L = " <<  luminosity << " fb^{-1} N_{jets} = "+jet_num;
 }

 TLatex* text = new TLatex(x, y, stream.str().c_str());

 text->SetNDC(true);
 text->SetTextFont(62);
 text->SetTextSize(0.04);
 return text;
}


