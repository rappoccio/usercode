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
vector<double> stop_Vec;  // Single top shape from MC
vector<double> wjets_Vec; // WJets shape from MC
vector<double> qcd_Vec;   // QCD shape from data driven method

double L = 19748; //luminosity in pb-1, using Alice's ntuples (SingleEleA,B,C,Cextra,D)
double trig_eff = 0.93;
double btag_eff = 0.97;

double Ntotal; //Total # of events -- define as global, currently rewritten for each Njets bin
double * ini_val;

int nbins = 9; 
double xmin = 300.;
double xmax = 1200.; 

// Helper functions
void fcn(int& npar, double* deriv, double& f, double par[], int flag);
void getData();
double* getBkg(double qcdnorm);
double* getWeightArray();
TText* doPrelim(float luminosity, float x, float y);

//-------------------------------------------------------------------------
int ptXsec() {

  cout << "Beginning..." << endl;

  double qcdnorm = 15.; //Set this using value from MET fit

  getData();
  ini_val = getBkg(qcdnorm);

  cout << "Total data: " << Ntotal << endl;
  cout << "Normalizations: " << endl;
  cout << "   Single top: " << ini_val[0] << endl;
  cout << "   WJets: " << ini_val[1] << endl;
  cout << "   QCD: " << ini_val[2] << endl;
  
  // Initialize minuit, set initial values etc. of parameters.
  const int npar = 9;              // N-B in each bin, should match nbins
  TMinuit minuit(npar);
  minuit.SetFCN(fcn);
  // SetPrintLevel: 1 verbose, 0 normal, -1 quiet
  minuit.SetPrintLevel(1);
  minuit.SetErrorDef(1.);
  
  int ierflg = 0;
  string parName[npar] = {"bin1", "bin2", "bin3", "bin4", "bin5", "bin6", "bin7", "bin8", "bin9"};
  double par[npar];
  
  // Initialize parameters
  for(int i=0; i<npar; i++){ par[i] = (Ntotal - ini_val[0] - ini_val[1] - ini_val[2]) / 9.; }

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
  
  // Plot the pt fit result(s)
  TH1F* result = new TH1F("result", "", nbins, xmin, xmax);
  TH1F* data = new TH1F("data", "", nbins, xmin, xmax);
  
  //ttbar, stop, wjets, and qcd contribution
  TH1F* his_Con[4];
  TString sample_names_array[4] = {"ttbar", "stop", "wjets", "qcd"};
  
  for(int i=0; i<4; i++){
    his_Con[i] = new TH1F(sample_names_array[i]+"_Con", "", nbins, xmin, xmax);
  }
  
  THStack* hs = new THStack("hs","stacked histograms");
  
  for (int i=0; i<nbins; i++){
    
    double ttbar_con = outpar[i];
    double stop_con = ini_val[0]*stop_Vec[i];
    double wjets_con = ini_val[1]*wjets_Vec[i];
    double qcd_con   = ini_val[2]*qcd_Vec[i];    
    double sum = ttbar_con + stop_con + wjets_con + qcd_con;

    data->SetBinContent(i+1, data_Vec[i]);
    result->SetBinContent(i+1, sum); //fitting results
    his_Con[0]->SetBinContent(i+1, ttbar_con);
    his_Con[1]->SetBinContent(i+1, stop_con);
    his_Con[2]->SetBinContent(i+1, wjets_con);
    his_Con[3]->SetBinContent(i+1, qcd_con);
 }
    
  //make fit plot
  TCanvas* canvasFit = new TCanvas("canvasFit", "canvasFit", 700, 500);
  
  his_Con[0]->SetFillColor(kRed+1);
  his_Con[1]->SetFillColor(kOrange);
  his_Con[2]->SetFillColor(kGreen-3);
  his_Con[3]->SetFillColor(kCyan);
  
  hs->Add(his_Con[3]);
  hs->Add(his_Con[2]);
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
  hs->GetYaxis()->SetTitle("Events / 100 GeV");
  result->Draw("same");
  data->Draw("same");
  
  TLegend* legFit = new TLegend(0.56, 0.5, 0.86, 0.82);
  legFit->SetBorderSize(0);
  legFit->SetTextFont(42);
  legFit->SetFillColor(0);
  legFit->AddEntry(data     , " Data", "LPE");
  legFit->AddEntry(result   , " Fit", "L");
  legFit->AddEntry(his_Con[0], " t#bar{t}", "F");
  legFit->AddEntry(his_Con[1], " single top", "F");
  legFit->AddEntry(his_Con[2], " wjets ", "F");
  legFit->AddEntry(his_Con[3], " QCD", "F");
  legFit->SetTextSize(0.04);
  legFit->Draw("same");
  
  TText* textPrelim = doPrelim(L/1000, 0.46,0.96);
  textPrelim->Draw();
  textPrelim->SetTextFont(42);
  gPad->RedrawAxis();

  // Calculate diff xsec
  double xsec[npar];
  double incxsec = 0.;

  TH1F* xsecHist = new TH1F("xsecHist", "", nbins, xmin, xmax);

  for (int i = 0; i < npar; i++){
    xsec[i] = outpar[i] / (btag_eff * trig_eff * L * 100.); //(N-B)/L*eff*dpT
    incxsec += xsec[i] * 100.;
    xsecHist->SetBinContent(i+1, xsec[i]);
  }
  
  //make xsec plot
  TCanvas* canvasXsec = new TCanvas("canvasXsec", "canvasXsec", 700, 500);
  
  xsecHist->SetLineStyle(1);             
  xsecHist->SetLineWidth(3);
  xsecHist->Draw();
  xsecHist->GetXaxis()->SetTitle("Top jet p_{t} (GeV)");
  xsecHist->GetYaxis()->SetTitle("d#sigma/dp_{t} / 100 GeV");
  xsecHist->SetTitle("Differential ttbar xsec");
  
  TText* textPrelim2 = doPrelim(L/1000, 0.46,0.96);
  textPrelim2->Draw();
  textPrelim2->SetTextFont(42);
  gPad->RedrawAxis();

  cout << "The differential cross section is: " << endl;
  cout << xsec[0] << " for 300 GeV - 400 GeV " << endl;
  cout << xsec[1] << " for 400 GeV - 500 GeV " << endl;
  cout << xsec[2] << " for 500 GeV - 600 GeV " << endl;
  cout << xsec[3] << " for 600 GeV - 700 GeV " << endl;
  cout << xsec[4] << " for 700 GeV - 800 GeV " << endl;
  cout << xsec[5] << " for 800 GeV - 900 GeV " << endl;
  cout << xsec[6] << " for 900 GeV - 1000 GeV " << endl;
  cout << xsec[7] << " for 1000 GeV - 1100 GeV " << endl;
  cout << xsec[8] << " for 1100 GeV - 1200 GeV " << endl;

  cout << " This yields an inclusive cross section of " << incxsec << endl;
   
  cout << "To exit, quit ROOT from the File menu of the plot" << endl;
  return 0;
  
}

//-------------------------------------------------------------------------
double* getWeightArray(){

  double xs_array[8], nE_array[8];
  double* weight_array = new double[8];

  // Xsec, Ngen taken from elog. All Xsec in pb.
  xs_array[0] = 234.;     //TTjets (POWHEG)
  nE_array[0] = 21560109;
  xs_array[1] = 11.1;     //St_tW
  nE_array[1] = 495559;
  xs_array[2] = 11.1;     //St_tWB
  nE_array[2] = 491463;
  xs_array[3] = 56.4;     //St_t
  nE_array[3] = 3748155;
  xs_array[4] = 30.7;     //St_tB
  nE_array[4] = 1930185;
  xs_array[5] = 3.79;     //St_s
  nE_array[5] = 259176;
  xs_array[6] = 1.76;     //St_sB
  nE_array[6] = 139604;
  xs_array[7] = 37509.0;  //wjets     
  nE_array[7] = 57653686;

  weight_array[0] = xs_array[0]*L*trig_eff*btag_eff/nE_array[0]; //TTjets
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
void getData(){
  TH1D* h_data = new TH1D("data", "data", nbins, xmin, xmax);
  //TFile* datafile = TFile::Open("Data_pt.root", "READ");
  TFile* datafile = TFile::Open("TTjets_POWHEG_pt.root", "READ"); //using ttjets for closure test
  h_data = (TH1D*) gDirectory->Get("ptTopTagHist");
  h_data->Rebin(2);
  double * weight = getWeightArray();
  h_data->Scale(weight[0]);

  // Write histogram to data vector, calc total # of events
  for(int ibin=0; ibin<nbins; ibin++){
    double nn = h_data->GetBinContent(ibin+1);
    data_Vec.push_back(nn);
    Ntotal += nn;
  }
}

// Function to produce the ttbar, stop, w+jets, and QCD templates
double* getBkg(double qcdnorm){

  double* ini_val = new double[3];
  TString sample_array[10] = {"St_tW", "St_tWB", "St_t", "St_tB", "St_s", "St_sB", "WJets", "QCD_old", "WJets_old", "TTjets_POWHEG_old"};
  TString sample_com_array[3] = {"stop", "wjets", "qcd"};
  TH1D** his_array = new TH1D*[10];
  TH1D** his_com_array = new TH1D*[3];
  TFile* file_array[10];

  double* weight = getWeightArray();  

  for(int i=0; i<3; i++){
    his_com_array[i] = new TH1D(sample_com_array[i], sample_com_array[i], nbins, xmin, xmax);
  }
  
  for(int i=0; i<10; i++){
    file_array[i] = TFile::Open(sample_array[i]+"_pt.root", "READ");
    his_array[i] = (TH1D*) gDirectory->Get("ptTopTagHist");
    his_array[i]->Rebin(2);
  }
  
  // Rescale and combine histograms
  // stop
  his_array[0]->Scale(weight[1]);
  his_com_array[0]->Add(his_array[0]);
  his_array[1]->Scale(weight[2]);
  his_com_array[0]->Add(his_array[1]);
  his_array[2]->Scale(weight[3]);
  his_com_array[0]->Add(his_array[2]);
  his_array[3]->Scale(weight[4]);
  his_com_array[0]->Add(his_array[3]);
  his_array[4]->Scale(weight[5]);
  his_com_array[0]->Add(his_array[4]);
  his_array[5]->Scale(weight[6]);
  his_com_array[0]->Add(his_array[5]);

  // wjets
  his_array[6]->Scale(weight[7]);
  his_com_array[1]->Add(his_array[6]);

  // qcd
  his_com_array[2]->Add(his_array[7]);
  his_array[8]->Scale(-1 * weight[7]); //wjets subtraction
  his_com_array[2]->Add(his_array[8]);
  his_array[9]->Scale(-1 * weight[0]); //ttjets subtraction
  his_com_array[2]->Add(his_array[9]);

  double ntemp = his_com_array[2]->Integral();
  his_com_array[2]->Scale(qcdnorm / ntemp);

  // Separate shape and normalization
  for(int i=0; i<3; i++){
    ini_val[i] = his_com_array[i]->Integral();
    if (his_com_array[i]->Integral() != 0.){
      his_com_array[i]->Scale(1./his_com_array[i]->Integral());
    }
  }

  // write templates to corresponding vectors
   for(int ibin=0; ibin<nbins; ibin++){

     double stop = his_com_array[0]->GetBinContent(ibin+1);
     stop_Vec.push_back(stop);
     
     double wjets = his_com_array[1]->GetBinContent(ibin+1);
     wjets_Vec.push_back(wjets);
     
     double qcd = his_com_array[2]->GetBinContent(ibin+1);
     qcd_Vec.push_back(qcd);       
     
   }

   return ini_val;
   
}

//-------------------------------------------------------------------------

// fcn passes back f = - 2*ln(L), the function to be minimized.
void fcn(int& npar, double* deriv, double& f, double par[], int flag){

  double lnL = 0.0;

  for (int i=0; i<nbins; i++){

    //data_i is the observed number of events in each bin
    int data_i = data_Vec[i];

    //xi is the expected number of events in each bin
    double xi = par[i] + ini_val[0]*stop_Vec[i] + ini_val[1]*wjets_Vec[i] + ini_val[2]*qcd_Vec[i];

    lnL += log(TMath::Poisson(data_i, xi));
    
  }

  f = -2.0 * lnL;

  // When we start using constraints instead of fixing the stop, wjets, qcd numbers they should be added here

}                         

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
TText* doPrelim(float luminosity, float x, float y)
{
 std::ostringstream stream;
 
 stream  <<"CMS Preliminary, L = " <<  luminosity << " fb^{-1}";
 
 TLatex* text = new TLatex(x, y, stream.str().c_str());

 text->SetNDC(true);
 text->SetTextFont(62);
 text->SetTextSize(0.04);
 return text;
}


