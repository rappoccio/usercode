/*
QCDminfit_3.cc performs a maximum likelihood fit in the MET distribution to determine the 
amount of QCD background. The fit parameters are the number of top (ttbar + single top), 
w+jets, and QCD events in the sample. These are used to normalize the respective templates
in order to fit the MET distribution in data. Templates are taken from the MET histograms 
produced by iheartny_topxs_fwlite.py, scaled and combined as necessary, and normalized 
to 1. The QCD template may be further modified by subtracting the MC sidebands. The fit 
may be performed for any of the plots.

The fit is performed using a direct interface with TMinuit, where the function TMinuit 
minimizes is fcn = -2*log(L). The factor of -2 allows for easy insertion of constraints, 
through adding quadratic terms to fcn.
For more info on TMinuit see root.cern.ch/root/html/TMinuit.html .

The inputs to be changed when running the program are found in the following lines:  
Lines 71-74 describe the histogram being fitted
Line 77 gives the rebinning factor
Line 78 gives the new binsize (in GeV)
Line 79 gives the new number of bins
Lines 83-107 describe the channel and the paths to the relevant .root files

Line 128 gives the cut stage for the MC template
Line 129 gives the cut stage for the QCD template
Line 130 specifies whether MC sidebands are subtracted from the data sideband to give the
QCD template.
Line 131 specifies whether to fit in exclusive regions or inclusive
Line 132 indicates whether to scale up or down the amount of non-QCD subtracted from the sideband
Line 134 indicates the percent by which the parameters are constrained to their input values in the fit


*/

#include <iostream>
#include <iomanip>
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
vector<double> wjets_Vec; //wjets template from MC
vector<double> qcd_Vec; //qcd template from data driven method

double L = 19700; //UPDATED (in pb)

int Ntotal; //Total # of events -- define as global, currently rewritten for each Njets bin

TString fitDist = "ptMET";
int nbins = 200;
double xmin = 0.;
double xmax = 400.;

// Rebinning factor, giving number of bins to combine into one (1 means no rebinning).
int binfac = 10;
TString binsize  = "20";      //binfac * 2
TString numberofbins  = "20"; //200 / binfac

TString whichHist = "2Dcut_";

//muons
/*
TString channel = "mu";
//TString DIR = "/2Dhist";
//TString DIR_TT = "/2Dhists";
//TString FOLDER = "histfiles";
//TString FOLDER_TT = "histfiles_CT10_nom";
TString DIR = "/qcd";
TString DIR_TT = "/qcd";
TString FOLDER = "histfiles";
TString FOLDER_TT = "histfiles_CT10_nom";
*/

//electrons

TString channel = "el";
//TString DIR = "/2Dhist_el";
//TString DIR_TT = "/2Dhists_el";
//TString FOLDER = "histfiles";
//TString FOLDER_TT = "histfiles_CT10_nom";
TString DIR = "/qcd_el";
TString DIR_TT = "/qcd_el";
TString FOLDER = "histfiles";
TString FOLDER_TT = "histfiles_CT10_nom";


double Nraw[5];
double Nnorm[5];
double Nfit[5];
double Nside[5];

// Helper functions
void fcn(int& npar, double* deriv, double& f, double par[], int flag);
void getData(TString& temp_num, int binfac, bool exclusive, TString channel);
double* getTemp(TString& temp_num, TString& QCD_temp_num, int binfac, bool dosub, bool exclusive, TString var, TString channel);
double* getWeightArray();

TText* doPrelim(float luminosity, float x, float y);

//-------------------------------------------------------------------------
int QCDminfit_3() {

  cout << "Beginning QCD normalization..." << endl;

  // User inputs
  TString temp_num = "4";
  TString QCD_temp_num = "4";
  bool dosub = true;
  bool exclusive = true; 
  TString var = "";    // Amount of non-QCD subtracted from the sideband
                         //"_raw" = none, "" = nominal, "_up" = nominal x 2, "_dn" = nominal x 1/2
  double cons[3] = {-1.0, -1.0, -1.0}; //% constraints on parameters (negative = no constraint)

  int nbins_new = nbins / binfac;
  cout << "New # of bins is " << nbins_new << endl;
  cout << "Fitting " << fitDist << temp_num << endl;

  getData(temp_num, binfac, exclusive, channel);
  cout << "Got data..." << endl;
  double* ratios = getTemp(temp_num, QCD_temp_num, binfac, dosub, exclusive, var, channel);
  cout << "Got MC..." << endl;

  // Initialize minuit, set initial values etc. of parameters.
  const int npar = 3; // the number of parameters
  TMinuit minuit(npar);

  minuit.SetFCN(fcn);
  // SetPrintLevel: 1 verbose, 0 normal, -1 quiet
  minuit.SetPrintLevel(1);
  minuit.SetErrorDef(0.5); //because is NLL
  
  int ierflg = 0;
  string parName[npar] = {"top", "wjets", "qcd"};
  double par[npar];

  double ini_val[npar] = {Nnorm[0] + Nnorm[1] + Nnorm[2],
			  Nnorm[3],
			  0.1 * Ntotal};

  // Determine upper and lower bounds for parameters
  double lowerbound[npar];
  double upperbound[npar];
  for (int ii = 0; ii < npar; ii++){
    if (cons[ii] < 0.) {
      lowerbound[ii] = 0.;
      upperbound[ii] = Ntotal;
    }
    else {
      lowerbound[ii] = ini_val[ii]*(1-cons[ii]);
      upperbound[ii] = ini_val[ii]*(1+cons[ii]);
    }
  }
  
  par[0] = ini_val[0];
  par[1] = ini_val[1];
  par[2] = ini_val[2];

  for(int i=0; i<npar; i++){
    // optimize parameters with initial value of par[i], moving in increments
    // of 1., between 0 and Ntotal
    minuit.mnparm(i, parName[i], par[i], 1., lowerbound[i], upperbound[i], ierflg);
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
  
  //top, wjets, and qcd contribution
  TH1F* his_Con[3];
  TH1F* his_Temp[3];
  TString sample_names_array[3] = {"top", "wjets", "qcd"};
  
  for(int i=0; i<3; i++){
    his_Con[i] = new TH1F(sample_names_array[i]+"_Con", "", nbins_new, xmin, xmax);
    his_Temp[i] = new TH1F(sample_names_array[i]+"_Temp", "", nbins_new, xmin, xmax);
  }
  
  THStack* hs = new THStack("hs","stacked histograms");
  
  for (int i=0; i<nbins_new; i++){
    
    data->SetBinContent(i+1, data_Vec[i]);
    
    double mean, top_con, wjets_con, qcd_con;
    
    top_con = outpar[0]*top_Vec[i];
    wjets_con = outpar[1]*wjets_Vec[i];
    qcd_con = outpar[2]*qcd_Vec[i];
    
    mean = top_con + wjets_con + qcd_con;
    result->SetBinContent(i+1, mean); //fitting results
    his_Con[0]->SetBinContent(i+1, top_con);
    his_Con[1]->SetBinContent(i+1, wjets_con);
    his_Con[2]->SetBinContent(i+1, qcd_con);
    his_Temp[0]->SetBinContent(i+1, top_Vec[i]);
    his_Temp[1]->SetBinContent(i+1, wjets_Vec[i]);
    his_Temp[2]->SetBinContent(i+1, qcd_Vec[i]);
    
  }
    
  double pplus, pminus, pparab, pgcc;
  minuit.mnerrs(2, pplus, pminus, pparab, pgcc);

  //Get post-fit numbers
  for (int i=0; i<3; i++){
    Nfit[i] = Nnorm[i] * outpar[0] / (Nnorm[0] + Nnorm[1] + Nnorm[2]) * ratios[i];
  }
  Nfit[3] = outpar[1] * ratios[3];

    
  //print out the results
  cout << fixed << setprecision(1);
  
  cout << "Cutflow: Step " << temp_num << endl;
  cout << "                    " << setw(10) << "TTbar"  << setw(18) << "TTbar_nonSemiLep" << setw(10) << "WJets"  
       << setw(10) << "S.T."   << setw(10) << "QCD"     << setw(10) << "Data"   << endl;
  cout << "Raw counts:         " << setw(10) << Nraw[0]  << setw(18) << Nraw[1]            << setw(10) << Nraw[3]  
       << setw(10) << Nraw[2]  << setw(10) << "N/A"     << setw(10) << Nraw[4]  << endl;
  cout << "Post normalization: " << setw(10) << Nnorm[0] << setw(18) << Nnorm[1]           << setw(10) << Nnorm[3] 
       << setw(10) << Nnorm[2] << setw(10) << "N/A"     << setw(10) << Nnorm[4] << endl;
  cout << "Post fit:           " << setw(10) << Nfit[0]  << setw(18) << Nfit[1]            << setw(10) << Nfit[3]  
       << setw(10) << Nfit[2]  << setw(10) << outpar[2] << setw(10) << Nfit[4]  << endl;
  cout << fixed << setprecision(2);
  cout << "Post / pre fit ratio: " << outpar[0] / (Nnorm[0] + Nnorm[1] + Nnorm[2]) << endl;
  cout << fixed << setprecision(1);
  cout << endl;
  cout << "QCD fit result:" << endl;
  cout << "\t Basic: " << outpar[2] * ratios[4] << " +- " << err[2] * ratios[4] << endl;
  cout << "\t MINOS: " << outpar[2] * ratios[4] << " + " << pplus * ratios[4] << " - " << pminus * ratios[4] << endl;
  cout << endl;
  cout << "Cutflow in sideband: Step " << temp_num << endl;
  cout << setw(10) << "TTbar"  << setw(18) << "TTbar_nonSemiLep" << setw(10) << "WJets"  
       << setw(10) << "S.T."   << setw(13) << "Data"   << endl;
  cout << setw(10) << Nside[0]  << setw(18) << Nside[1] << setw(10) << Nside[3] 
       << setw(10) << Nside[2]  << setw(13) << Nside[4]  << endl;
  
  //make template plots
  TCanvas* canvasTemp = new TCanvas("canvasTemp", "canvasTemp", 700, 500);
  
  his_Temp[0]->SetLineColor(kRed+1);
  his_Temp[1]->SetLineColor(kGreen-3);
  his_Temp[2]->SetLineColor(kOrange);
  
  his_Temp[0]->SetLineWidth(5);
  his_Temp[1]->SetLineWidth(5);
  his_Temp[2]->SetLineWidth(5);
  
  gStyle->SetOptStat(0);
  gStyle->SetPadBottomMargin(0.11);
  gStyle->SetPadTopMargin(0.08);
  gStyle->SetPadLeftMargin(0.1);
  gStyle->SetPadRightMargin(0.05);
  his_Temp[0]->SetTitle("");
  his_Temp[0]->Draw();
  double topmax = his_Temp[0]->GetMaximum();
  double wjetmax = his_Temp[1]->GetMaximum();
  double qcdmax = his_Temp[2]->GetMaximum();
  double tmpmax1 = max(topmax, wjetmax);
  double tmpmax2 = max(tmpmax1, qcdmax);
  his_Temp[0]->SetMaximum(1.2 * tmpmax2);
  if (fitDist == "ptMET") his_Temp[0]->GetXaxis()->SetTitle("missing E_{T} (GeV)");
  if (fitDist == "htLep") his_Temp[0]->GetXaxis()->SetTitle("H_{T}^{lep} (GeV)");
  his_Temp[0]->GetYaxis()->SetTitle("a.u.");
  his_Temp[0]->GetXaxis()->SetTitleSize(0.05);
  his_Temp[0]->GetYaxis()->SetTitleSize(0.05);
  his_Temp[0]->GetYaxis()->SetTitleOffset(0.9);
  
  his_Temp[1]->Draw("same");
  his_Temp[2]->Draw("same");
  
  TLegend* legTemp = new TLegend(0.72, 0.63, 0.92, 0.83);
  legTemp->SetBorderSize(0);
  legTemp->SetTextFont(42);
  legTemp->SetFillColor(0);
  legTemp->AddEntry(his_Temp[0], " Top", "L");
  legTemp->AddEntry(his_Temp[1], " WJets", "L");
  legTemp->AddEntry(his_Temp[2], " QCD", "L");
  
  legTemp->SetTextSize(0.045);
  legTemp->Draw("same");
  TText* textPrelimA = doPrelim(L/1000, 0.600, 0.875);
  textPrelimA->Draw();
  textPrelimA->SetTextFont(42);

  canvasTemp->Update();
  canvasTemp->SaveAs("plots_"+channel+"/"+fitDist+"/Temp_3temp_"+whichHist+numberofbins+"b_"+temp_num+var+".png");
  canvasTemp->SaveAs("plots_"+channel+"/"+fitDist+"/Temp_3temp_"+whichHist+numberofbins+"b_"+temp_num+var+".pdf");

  //make fit plot
  TCanvas* canvasFit = new TCanvas("canvasFit", "canvasFit", 700, 500);
  
  his_Con[0]->SetFillColor(kRed+1);
  his_Con[1]->SetFillColor(kGreen-3);
  his_Con[2]->SetFillColor(kYellow);
  
  hs->Add(his_Con[2]);
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
  if (fitDist == "ptMET") hs->GetXaxis()->SetTitle("missing E_{T} (GeV)");
  if (fitDist == "htLep") hs->GetXaxis()->SetTitle("H_{T}^{lep} (GeV)");
  hs->GetYaxis()->SetTitle("Number of Events / "+binsize+" GeV");
  hs->GetXaxis()->SetTitleSize(0.05);
  hs->GetYaxis()->SetTitleSize(0.05);
  hs->GetYaxis()->SetTitleOffset(1.0);
  result->Draw("same");
  data->Draw("same");
  
  TLegend* legFit = new TLegend(0.72, 0.53, 0.92, 0.85);
  legFit->SetBorderSize(0);
  legFit->SetTextFont(42);
  legFit->SetFillColor(0);
  legFit->AddEntry(data , " Data", "LPE");
  legFit->AddEntry(result , " Fit", "L");
  legFit->AddEntry(his_Con[0], " Top", "F");
  legFit->AddEntry(his_Con[1], " W #rightarrow #mu#nu", "F");
  legFit->AddEntry(his_Con[2], " QCD", "F");
  legFit->SetTextSize(0.04);
  legFit->Draw("same");
  
  TText* textPrelimB = doPrelim(L/1000, 0.600, 0.875);
  textPrelimB->Draw();
  textPrelimB->SetTextFont(42);
  gPad->RedrawAxis();
  
  canvasFit->Update();
  canvasFit->SaveAs("plots_"+channel+"/"+fitDist+"/Fit_3temp_"+whichHist+numberofbins+"b_"+temp_num+var+".png");
  canvasFit->SaveAs("plots_"+channel+"/"+fitDist+"/Fit_3temp_"+whichHist+numberofbins+"b_"+temp_num+var+".pdf");

  cout << "To exit, quit ROOT from the File menu of the plot" << endl;
  return 0;
  
}

//-------------------------------------------------------------------------
double* getWeightArray(){

  double xs_array[16], nE_array[16];
  double* weight_array = new double[16];

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
  xs_array[12] = 5400*1.207; //W+1jets
  nE_array[12] = 23141598;
  xs_array[13] = 1750*1.207; //W+2jets
  nE_array[13] = 34044921;
  xs_array[14] = 519*1.207; //W+3jets
  nE_array[14] = 15539503;
  xs_array[15] = 214*1.207; //W+4jets
  nE_array[15] = 13382803;

  weight_array[0] = xs_array[0]*L/nE_array[0]; //TTjets 0-700
  weight_array[1] = xs_array[1]*L*0.074/nE_array[1]; //TTjets 700-1000
  weight_array[2] = xs_array[2]*L*0.015/nE_array[2]; //TTjets 1000-Inf
  weight_array[3] = xs_array[3]*L/nE_array[3]; //TTjets 0-700 nonSemiLep
  weight_array[4] = xs_array[4]*L*0.074/nE_array[4]; //TTjets 700-1000 nonSemiLep
  weight_array[5] = xs_array[5]*L*0.015/nE_array[5]; //TTjets 1000-Inf nonSemiLep
  weight_array[6] = xs_array[6]*L/nE_array[6]; //St_tW
  weight_array[7] = xs_array[7]*L/nE_array[7]; //St_tWB
  weight_array[8] = xs_array[8]*L/nE_array[8]; //St_t
  weight_array[9] = xs_array[9]*L/nE_array[9]; //St_tB
  weight_array[10] = xs_array[10]*L/nE_array[10]; //St_s
  weight_array[11] = xs_array[11]*L/nE_array[11]; //St_sB
  weight_array[12] = xs_array[12]*L/nE_array[12]; //W+1jets
  weight_array[13] = xs_array[13]*L/nE_array[13]; //W+2jets
  weight_array[14] = xs_array[14]*L/nE_array[14]; //W+3jets
  weight_array[15] = xs_array[15]*L/nE_array[15]; //W+4jets
  
  return weight_array;

}


// function to read in the data from a histogram
void getData(TString& temp_num, int binfac, bool exclusive, TString channel){

  int nbins_new = nbins / binfac;
  TH1D* h_data = new TH1D("data", "data", nbins, xmin, xmax);
  TFile* datafile;
  if (channel == "mu") {
    datafile = TFile::Open("../"+FOLDER+DIR+"/SingleMu_iheartNY_V1_mu_Run2012_"+whichHist+"nom.root", "READ");
  }
  if (channel == "el") {
    datafile = TFile::Open("../"+FOLDER+DIR+"/SingleEl_iheartNY_V1_el_Run2012_"+whichHist+"nom.root", "READ");
  }
  h_data = (TH1D*) gDirectory->Get(fitDist+temp_num);
  h_data->Sumw2();
  if (exclusive && temp_num == "4"){
    TH1D* h_data_sub = (TH1D*) gDirectory->Get(fitDist+"6");
    h_data_sub->Sumw2();
    h_data->Add(h_data_sub, -1);
  }
  if (exclusive && temp_num == "5"){
    TH1D* h_data_sub = (TH1D*) gDirectory->Get(fitDist+"6");
    h_data_sub->Sumw2();
    h_data->Add(h_data_sub, -1);
  }
  if (exclusive && temp_num == "6"){
    TH1D* h_data_sub = (TH1D*) gDirectory->Get(fitDist+"7");
    h_data_sub->Sumw2();
    h_data->Add(h_data_sub, -1);
  }
  h_data->Rebin(binfac);

  // Write histogram to data vector, calc total # of events
  for(int ibin=0; ibin<nbins_new; ibin++){
    int nn = h_data->GetBinContent(ibin+1);
    data_Vec.push_back(nn);
    Ntotal += nn;
  }
  Nraw[4] = Nnorm[4] = Nfit[4] = h_data->Integral(0,nbins_new+1);

}

// Function to produce the top and QCD templates
double* getTemp(TString& temp_num, TString& QCD_temp_num, int binfac, bool dosub, bool exclusive, TString var, TString channel){

  double* ratios = new double[5]; //EDIT might be wrong size -- was ini_val
  TString sample_array[16] = {"TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+channel+"_CT10_nom_",
			      "TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+channel+"_CT10_nom_",
			      "TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+channel+"_CT10_nom_",
			      "TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+channel+"_CT10_nom_",
			      "TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+channel+"_CT10_nom_",
			      "TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+channel+"_CT10_nom_",
			      "T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+channel+"_",
			      "Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+channel+"_",
			      "T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+channel+"_",
			      "Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+channel+"_",
			      "T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+channel+"_",
			      "Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+channel+"_",
			      "W1JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_"+channel+"_",
			      "W2JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_"+channel+"_",
			      "W3JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_"+channel+"_",
			      "W4JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_"+channel+"_"};

  TString shortnames[16] = {"TTbar_m0to700", "TTbar_m700to1000", "TTbar_m1000toInf", "TTbar_nonSemiLep_m0to700", 
			    "TTbar_nonSemiLep_m700to1000", "TTbar_nonSemiLep_m1000toInf",
			    "St_tW", "St_tWB", "St_t", "St_tB", "St_s", "St_sB", "W1Jets", "W2Jets", "W3Jets", "W4Jets"};

  TString sample_com_array[3] = {"top", "wjets", "qcd"};
  TH1D** his_com_array = new TH1D*[3];

  TString top_cont_names[3] = {"TTjets", "TTjets_nonsemilep", "Stop"};
  TH1D** top_cont_array = new TH1D*[3];

  TH1D** top_his_array = new TH1D*[12];
  TFile* top_file_array[12];

  TH1D** wjets_his_array = new TH1D*[4];
  TFile* wjets_file_array[4];

  TH1D** qcd_his_array = new TH1D*[17];
  TFile* qcd_file_array[17];

  double* weight = getWeightArray();
  int nbins_new = nbins / binfac;

  for(int i=0; i<3; i++){
    his_com_array[i] = new TH1D(sample_com_array[i], sample_com_array[i], nbins_new, xmin, xmax);
  }

  for(int i=0; i<3; i++){
    top_cont_array[i] = new TH1D(top_cont_names[i], top_cont_names[i], nbins_new, xmin, xmax);
  }
  
  // Do first recombination
  // TTjets semilep
  for(int i=0; i<3; i++){
    top_file_array[i] = TFile::Open("../"+FOLDER_TT+DIR_TT+"/"+sample_array[i]+whichHist+"nom.root", "READ");
    top_his_array[i] = (TH1D*) gDirectory->Get(fitDist+temp_num);
    if (exclusive && temp_num == "4"){
      TH1D* hist_sub = (TH1D*) gDirectory->Get(fitDist+"6");
      top_his_array[i]->Add(hist_sub, -1);
    }
    if (exclusive && temp_num == "5"){
      TH1D* hist_sub = (TH1D*) gDirectory->Get(fitDist+"6");
      top_his_array[i]->Add(hist_sub, -1);
    }
    if (exclusive && temp_num == "6"){
      TH1D* hist_sub = (TH1D*) gDirectory->Get(fitDist+"7");
      top_his_array[i]->Add(hist_sub, -1);
    }
    top_his_array[i]->Rebin(binfac);
    Nraw[0] += top_his_array[i]->Integral(0, nbins_new+1);
    top_his_array[i]->Scale(weight[i]);
    top_cont_array[0]->Add(top_his_array[i]);
  }
  cout << "Got ttjets semilep..." << endl;

  // TTjets nonsemilep
  for(int i=3; i<6; i++){
    top_file_array[i] = TFile::Open("../"+FOLDER_TT+DIR_TT+"/"+sample_array[i]+whichHist+"nom.root", "READ");
    top_his_array[i] = (TH1D*) gDirectory->Get(fitDist+temp_num);
    if (exclusive && temp_num == "4"){
      TH1D* hist_sub = (TH1D*) gDirectory->Get(fitDist+"6");
      top_his_array[i]->Add(hist_sub, -1);
    }
    if (exclusive && temp_num == "5"){
      TH1D* hist_sub = (TH1D*) gDirectory->Get(fitDist+"6");
      top_his_array[i]->Add(hist_sub, -1);
    }
    if (exclusive && temp_num == "6"){
      TH1D* hist_sub = (TH1D*) gDirectory->Get(fitDist+"7");
      top_his_array[i]->Add(hist_sub, -1);
    }
    top_his_array[i]->Rebin(binfac);
    Nraw[1] += top_his_array[i]->Integral(0, nbins_new+1);
    top_his_array[i]->Scale(weight[i]);
    top_cont_array[1]->Add(top_his_array[i]);
  }
  cout << "Got ttjets nonsemilep..." << endl;
  
  // Stop
  for(int i=6; i<12; i++){
    top_file_array[i] = TFile::Open("../"+FOLDER+DIR+"/"+sample_array[i]+whichHist+"nom.root", "READ");
    top_his_array[i] = (TH1D*) gDirectory->Get(fitDist+temp_num);
    if (exclusive && temp_num == "4"){
      TH1D* hist_sub = (TH1D*) gDirectory->Get(fitDist+"6");
      top_his_array[i]->Add(hist_sub, -1);
    }
    if (exclusive && temp_num == "5"){
      TH1D* hist_sub = (TH1D*) gDirectory->Get(fitDist+"6");
      top_his_array[i]->Add(hist_sub, -1);
    }
    if (exclusive && temp_num == "6"){
      TH1D* hist_sub = (TH1D*) gDirectory->Get(fitDist+"7");
      top_his_array[i]->Add(hist_sub, -1);
    }
    top_his_array[i]->Rebin(binfac);
    Nraw[2] += top_his_array[i]->Integral(0, nbins_new+1);
    top_his_array[i]->Scale(weight[i]);
    top_cont_array[2]->Add(top_his_array[i]);
  }
  cout << "Got single top..." << endl;

  //Combine into one top histo
  for (int i=0; i<3; i++){
    Nnorm[i] = top_cont_array[i]->Integral(0, nbins_new+1);
    ratios[i] = top_cont_array[i]->Integral(0, nbins_new+1) / top_cont_array[i]->Integral();
    his_com_array[0]->Add(top_cont_array[i]);
  }

  // Get WJets template
  for(int i=0; i<4; i++){
    wjets_file_array[i] = TFile::Open("../"+FOLDER+DIR+"/"+sample_array[i+12]+whichHist+"nom.root", "READ");
    wjets_his_array[i] = (TH1D*) gDirectory->Get(fitDist+temp_num);
    if (exclusive && temp_num == "4"){
      TH1D* hist_sub = (TH1D*) gDirectory->Get(fitDist+"6");
      wjets_his_array[i]->Add(hist_sub, -1);
    }
    if (exclusive && temp_num == "5"){
      TH1D* hist_sub = (TH1D*) gDirectory->Get(fitDist+"6");
      wjets_his_array[i]->Add(hist_sub, -1);
    }
    if (exclusive && temp_num == "6"){
      TH1D* hist_sub = (TH1D*) gDirectory->Get(fitDist+"7");
      wjets_his_array[i]->Add(hist_sub, -1);
    }
    wjets_his_array[i]->Rebin(binfac);
    Nraw[3] += wjets_his_array[i]->Integral(0, nbins_new+1);
    wjets_his_array[i]->Scale(weight[i+12]);
    his_com_array[1]->Add(wjets_his_array[i]);
  }
  cout << "Got wjets..." << endl;
  Nnorm[3] = his_com_array[1]->Integral(0, nbins_new+1);
  ratios[3] = his_com_array[1]->Integral(0, nbins_new+1) / his_com_array[1]->Integral();

  // Get QCD template
  if (channel == "mu") {
    qcd_file_array[0] = TFile::Open("../"+FOLDER+DIR+"/SingleMu_iheartNY_V1_mu_Run2012_"+whichHist+"qcd.root", "READ");
  }
  if (channel == "el") {
    qcd_file_array[0] = TFile::Open("../"+FOLDER+DIR+"/SingleEl_iheartNY_V1_el_Run2012_"+whichHist+"qcd.root", "READ");
  }

  qcd_his_array[0] = (TH1D*) gDirectory->Get(fitDist+QCD_temp_num);
  if (exclusive && QCD_temp_num == "4"){
    TH1D* hist_sub = (TH1D*) gDirectory->Get(fitDist+"6");
    qcd_his_array[0]->Add(hist_sub, -1);
  }
  if (exclusive && QCD_temp_num == "5"){
    TH1D* hist_sub = (TH1D*) gDirectory->Get(fitDist+"6");
    qcd_his_array[0]->Add(hist_sub, -1);
  }
  if (exclusive && QCD_temp_num == "6"){
    TH1D* hist_sub = (TH1D*) gDirectory->Get(fitDist+"7");
    qcd_his_array[0]->Add(hist_sub, -1);
  }
  qcd_his_array[0]->Rebin(binfac);
  his_com_array[2]->Add(qcd_his_array[0]);
  if (dosub && var != "_raw") {
    for(int i=0; i<16; i++){
      if (i < 6){
	qcd_file_array[i+1] = TFile::Open("../"+FOLDER_TT+DIR_TT+"/"+sample_array[i]+whichHist+"qcd.root", "READ");
      }
      else {
	qcd_file_array[i+1] = TFile::Open("../"+FOLDER+DIR+"/"+sample_array[i]+whichHist+"qcd.root", "READ");
      }
      qcd_his_array[i+1] = (TH1D*) gDirectory->Get(fitDist+QCD_temp_num);
      if (exclusive && QCD_temp_num == "4"){
	TH1D* hist_sub = (TH1D*) gDirectory->Get(fitDist+"6");
	qcd_his_array[i+1]->Add(hist_sub, -1);
      }
      if (exclusive && QCD_temp_num == "5"){
	TH1D* hist_sub = (TH1D*) gDirectory->Get(fitDist+"6");
	qcd_his_array[i+1]->Add(hist_sub, -1);
      }
      if (exclusive && QCD_temp_num == "6"){
	TH1D* hist_sub = (TH1D*) gDirectory->Get(fitDist+"7");
	qcd_his_array[i+1]->Add(hist_sub, -1);
      }
      qcd_his_array[i+1]->Rebin(binfac);
      if (var == ""){
	qcd_his_array[i+1]->Scale(weight[i]);
      }
      if (var == "_up"){
	qcd_his_array[i+1]->Scale(weight[i]*2);
      }
      if (var == "_dn"){
	qcd_his_array[i+1]->Scale(weight[i]*0.5);
      }
      his_com_array[2]->Add(qcd_his_array[i+1], -1);
    }
  }
  cout << "Got QCD..." << endl;
  ratios[4] = his_com_array[2]->Integral(0, nbins_new+1) / his_com_array[2]->Integral();


  // Make breakdown plots
  int colors[6] = {400, 632+1, 632-7, 6, 416-3, 1}; //QCD, tt signal, tt other, single top, wjets, data
  gStyle->SetPadBottomMargin(0.11);
  gStyle->SetPadTopMargin(0.08);
  gStyle->SetPadLeftMargin(0.1);
  gStyle->SetPadRightMargin(0.05);
  TCanvas* canvasTop = new TCanvas("canvasTop", "canvasTop", 700, 500);
  THStack* topcont = new THStack("topcont","top contributions");

  for (int i = 0; i<3; i++) {
    top_cont_array[i]->SetFillColor(colors[i+1]);
    topcont->Add(top_cont_array[i]);
  }
  topcont->SetTitle("Contributions to top template");
  topcont->Draw();
  //topcont->SetTitle("");
  if (fitDist == "ptMET") topcont->GetXaxis()->SetTitle("missing E_{T} (GeV)");
  if (fitDist == "htLep") topcont->GetXaxis()->SetTitle("H_{T}^{lep} (GeV)");
  topcont->GetXaxis()->SetTitleSize(0.05);
  topcont->GetYaxis()->SetTitle("Number of Events / "+binsize+" GeV");
  topcont->GetYaxis()->SetTitleSize(0.05);
  topcont->GetYaxis()->SetTitleOffset(0.9);

  TLegend* leg1 = new TLegend(0.72, 0.63, 0.92, 0.85);
  leg1->SetBorderSize(0);
  leg1->SetTextFont(42);
  leg1->SetFillColor(0);
  leg1->AddEntry(top_cont_array[0], " t#bar{t} Signal", "F");
  leg1->AddEntry(top_cont_array[1], " t#bar{t} Other", "F");
  leg1->AddEntry(top_cont_array[2], " Single Top", "F");
  leg1->SetTextSize(0.04);
  leg1->Draw("same");

  TText* textPrelim1 = doPrelim(L/1000, 0.600, 0.875);
  textPrelim1->Draw();
  textPrelim1->SetTextFont(42);
  gPad->RedrawAxis();

  canvasTop->Update();
  canvasTop->SaveAs("plots_"+channel+"/"+fitDist+"/TopComp_3temp_"+whichHist+numberofbins+"b_"+temp_num+var+".png");
  canvasTop->SaveAs("plots_"+channel+"/"+fitDist+"/TopComp_3temp_"+whichHist+numberofbins+"b_"+temp_num+var+".pdf");

  TCanvas* canvasTopNorm = new TCanvas("canvasTopNorm", "canvasTopNorm", 700, 500);
  gStyle->SetOptStat(0);
  double tempmax = 0.;
  for (int i = 0; i<3; i++){
    if (top_cont_array[i]->Integral() > 0.){
      top_cont_array[i]->Scale(1./top_cont_array[i]->Integral());
    }
    top_cont_array[i]->SetFillColor(0);
    top_cont_array[i]->SetLineColor(colors[i+1]);
    top_cont_array[i]->SetLineWidth(5);
    if (top_cont_array[i]->GetMaximum() > tempmax){
      tempmax = top_cont_array[i]->GetMaximum();
    }
  }

  gStyle->SetPadBottomMargin(0.11);
  gStyle->SetPadTopMargin(0.08);
  gStyle->SetPadLeftMargin(0.1);
  gStyle->SetPadRightMargin(0.05);
  top_cont_array[0]->Draw();
  top_cont_array[0]->SetMaximum(1.2 * tempmax);
  top_cont_array[0]->SetTitle("Components of top template");
  //top_cont_array[0]->SetTitle("");
  if (fitDist == "ptMET") top_cont_array[0]->GetXaxis()->SetTitle("missing E_{T} (GeV)");
  if (fitDist == "htLep") top_cont_array[0]->GetXaxis()->SetTitle("H_{T}^{lep} (GeV)");
  top_cont_array[0]->GetXaxis()->SetTitleSize(0.05);
  top_cont_array[0]->GetYaxis()->SetTitle("a.u.");
  top_cont_array[0]->GetYaxis()->SetTitleSize(0.05);
  top_cont_array[0]->GetYaxis()->SetTitleOffset(0.9);

  top_cont_array[1]->Draw("same");
  top_cont_array[2]->Draw("same");

  TLegend* leg2 = new TLegend(0.72, 0.63, 0.92, 0.85);
  leg2->SetBorderSize(0);
  leg2->SetTextFont(42);
  leg2->SetFillColor(0);
  leg2->AddEntry(top_cont_array[0], " t#bar{t} Signal", "L");
  leg2->AddEntry(top_cont_array[1], " t#bar{t} Other", "L");
  leg2->AddEntry(top_cont_array[2], " Single Top", "L");
  leg2->SetTextSize(0.04);
  leg2->Draw("same");
  
  TText* textPrelim2 = doPrelim(L/1000, 0.600, 0.875);
  textPrelim2->Draw();
  textPrelim2->SetTextFont(42);
  gPad->RedrawAxis();

  canvasTopNorm->Update();
  canvasTopNorm->SaveAs("plots_"+channel+"/"+fitDist+"/TopTemp_3temp_"+whichHist+numberofbins+"b_"+temp_num+var+".png");
  canvasTopNorm->SaveAs("plots_"+channel+"/"+fitDist+"/TopTemp_3temp_"+whichHist+numberofbins+"b_"+temp_num+var+".pdf");

  if (dosub && var != "_raw") {
    TH1F** qcd_cont_array = new TH1F*[6];
    TString qcd_cont_names[6] = {"qcdcorr", "qcdttbarsig", "qcdttbarbkg", "qcdstop", "qcdwjets", "qcdraw"};
    for(int i=0; i<6; i++){
      qcd_cont_array[i] = new TH1F(qcd_cont_names[i], qcd_cont_names[i], nbins_new, xmin, xmax);
    }
    
    qcd_cont_array[0]->Add(his_com_array[2]);  //corrected (QCD)
    qcd_cont_array[1]->Add(qcd_his_array[1]);  //TTjets
    qcd_cont_array[1]->Add(qcd_his_array[2]);
    qcd_cont_array[1]->Add(qcd_his_array[3]);
    qcd_cont_array[2]->Add(qcd_his_array[4]);  //TTjets nonsemilep
    qcd_cont_array[2]->Add(qcd_his_array[5]);
    qcd_cont_array[2]->Add(qcd_his_array[6]);
    qcd_cont_array[3]->Add(qcd_his_array[7]);  //Single top
    qcd_cont_array[3]->Add(qcd_his_array[8]);
    qcd_cont_array[3]->Add(qcd_his_array[9]);
    qcd_cont_array[3]->Add(qcd_his_array[10]);
    qcd_cont_array[3]->Add(qcd_his_array[11]);
    qcd_cont_array[3]->Add(qcd_his_array[12]);
    qcd_cont_array[4]->Add(qcd_his_array[13]); //WJets
    qcd_cont_array[4]->Add(qcd_his_array[14]);
    qcd_cont_array[4]->Add(qcd_his_array[15]);
    qcd_cont_array[4]->Add(qcd_his_array[16]);
    qcd_cont_array[5]->Add(qcd_his_array[0]);  //raw data

    TCanvas* canvasQCD = new TCanvas("canvasQCD", "canvasQCD", 700, 500);
    THStack* QCDcont = new THStack("QCDcont","QCD contributions");

    for (int i = 0; i<5; i++) {
      qcd_cont_array[i]->SetFillColor(colors[i]);
      Nside[i] = qcd_cont_array[i+1]->Integral(0, nbins_new+1);
      QCDcont->Add(qcd_cont_array[i]);
    }

    gStyle->SetPadBottomMargin(0.11);
    gStyle->SetPadTopMargin(0.08);
    gStyle->SetPadLeftMargin(0.11);
    gStyle->SetPadRightMargin(0.05);
    QCDcont->SetTitle("Contributions to data sideband");
    //QCDcont->SetTitle("");
    QCDcont->Draw();
    if (fitDist == "ptMET") QCDcont->GetXaxis()->SetTitle("missing E_{T} (GeV)");
    if (fitDist == "htLep") QCDcont->GetXaxis()->SetTitle("H_{T}^{lep} (GeV)");
    QCDcont->GetXaxis()->SetTitleSize(0.05);
    QCDcont->GetYaxis()->SetTitle("Number of Events / "+binsize+" GeV");
    QCDcont->GetYaxis()->SetTitleSize(0.05);
    QCDcont->GetYaxis()->SetTitleOffset(1.0);

    qcd_cont_array[5]->SetLineColor(kBlack);
    qcd_cont_array[5]->SetLineWidth(3);
    qcd_cont_array[5]->Draw("same");

    TLegend* leg3 = new TLegend(0.72, 0.53, 0.92, 0.85);
    leg3->SetBorderSize(0);
    leg3->SetTextFont(42);
    leg3->SetFillColor(0);
    leg3->AddEntry(qcd_cont_array[5], " Data", "L");
    leg3->AddEntry(qcd_cont_array[1], " t#bar{t} Signal", "F");
    leg3->AddEntry(qcd_cont_array[2], " t#bar{t} Other", "F");
    leg3->AddEntry(qcd_cont_array[3], " Single Top", "F");
    leg3->AddEntry(qcd_cont_array[4], " W #rightarrow #mu#nu", "F");
    leg3->AddEntry(qcd_cont_array[0], " QCD", "F");
    leg3->SetTextSize(0.04);
    leg3->Draw("same");

    TText* textPrelim3 = doPrelim(L/1000, 0.600, 0.875);
    textPrelim3->Draw();
    textPrelim3->SetTextFont(42);
    gPad->RedrawAxis();

    canvasQCD->Update();
    canvasQCD->SaveAs("plots_"+channel+"/"+fitDist+"/QCDComp_3temp_"+whichHist+numberofbins+"b_"+temp_num+var+".png");
    canvasQCD->SaveAs("plots_"+channel+"/"+fitDist+"/QCDComp_3temp_"+whichHist+numberofbins+"b_"+temp_num+var+".pdf");
    
    TCanvas* canvasQCDNorm = new TCanvas("canvasQCDNorm", "canvasQCDNorm", 700, 500);
    gStyle->SetOptStat(0);

    double tempmax2 = 0.;
    for (int i = 1; i<6; i++){
      if (qcd_cont_array[i]->Integral() > 0.){
	qcd_cont_array[i]->Scale(1./qcd_cont_array[i]->Integral());
      }
      qcd_cont_array[i]->SetFillColor(0);
      qcd_cont_array[i]->SetLineColor(colors[i]);
      qcd_cont_array[i]->SetLineWidth(5);
	if (qcd_cont_array[i]->GetMaximum() > tempmax2){
	  tempmax2 = qcd_cont_array[i]->GetMaximum();
	}
    }

    gStyle->SetPadBottomMargin(0.11);
    gStyle->SetPadTopMargin(0.08);
    gStyle->SetPadLeftMargin(0.1);
    gStyle->SetPadRightMargin(0.05);
    qcd_cont_array[1]->Draw();
    qcd_cont_array[1]->SetMaximum(1.2 * tempmax2);
    qcd_cont_array[1]->SetTitle("Distributions in sideband");
    //qcd_cont_array[1]->SetTitle("");
    if (fitDist == "ptMET") qcd_cont_array[1]->GetXaxis()->SetTitle("missing E_{T} (GeV)");
    if (fitDist == "htLep") qcd_cont_array[1]->GetXaxis()->SetTitle("H_{T}^{lep} (GeV)");
    qcd_cont_array[1]->GetXaxis()->SetTitleSize(0.05);
    qcd_cont_array[1]->GetYaxis()->SetTitle("a.u.");
    qcd_cont_array[1]->GetYaxis()->SetTitleSize(0.05);
    qcd_cont_array[1]->GetYaxis()->SetTitleOffset(0.9);

    qcd_cont_array[2]->Draw("same");
    qcd_cont_array[3]->Draw("same");
    qcd_cont_array[4]->Draw("same");
    qcd_cont_array[5]->Draw("same");

    TLegend* leg4 = new TLegend(0.72, 0.53, 0.92, 0.85);
    leg4->SetBorderSize(0);
    leg4->SetTextFont(42);
    leg4->SetFillColor(0);
    leg4->AddEntry(qcd_cont_array[5], " Data", "L");
    leg4->AddEntry(qcd_cont_array[1], " t#bar{t} Signal", "L");
    leg4->AddEntry(qcd_cont_array[2], " t#bar{t} Other", "L");
    leg4->AddEntry(qcd_cont_array[3], " Single Top", "L");
    leg4->AddEntry(qcd_cont_array[4], " W #rightarrow #mu#nu", "L");
    leg4->SetTextSize(0.04);
    leg4->Draw("same");

    TText* textPrelim4 = doPrelim(L/1000, 0.600, 0.875);
    textPrelim4->Draw();
    textPrelim4->SetTextFont(42);
    gPad->RedrawAxis();

    canvasQCDNorm->Update();
    canvasQCDNorm->SaveAs("plots_"+channel+"/"+fitDist+"/QCDTemp_3temp_"+whichHist+numberofbins+"b_"+temp_num+var+".png");
    canvasQCDNorm->SaveAs("plots_"+channel+"/"+fitDist+"/QCDTemp_3temp_"+whichHist+numberofbins+"b_"+temp_num+var+".pdf");
  }


  // Normalize histograms to 1 (but first determine Nexp)
  his_com_array[0]->Scale(1./his_com_array[0]->Integral());
  his_com_array[1]->Scale(1./his_com_array[1]->Integral());
  his_com_array[2]->Scale(1./his_com_array[2]->Integral());

  // write histograms to corresponding vectors
  for(int ibin=0; ibin<nbins_new; ibin++){

    double top = his_com_array[0]->GetBinContent(ibin+1);
    top_Vec.push_back(top);

    double wjets = his_com_array[1]->GetBinContent(ibin+1);
    wjets_Vec.push_back(wjets);
    
    double qcd = his_com_array[2]->GetBinContent(ibin+1);
    qcd_Vec.push_back(qcd);
     
  }

  return ratios;
   
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
    double xi = par[0]*top_Vec[i] + par[1]*wjets_Vec[i] + par[2]*qcd_Vec[i];

    lnL += log(TMath::Poisson(data_i, xi));
    
  }

  f = -2.0 * lnL;

  //top constraint
  //double ntop = Nnorm[0] + Nnorm[1] + Nnorm[2];
  //double ntop_err = ntop*0.5;
  //f += (par[0]-ntop)*(par[0]-ntop)/ntop_err/ntop_err;

  //W+jets constraint
  //double nwjets = Nnorm[3];
  //double nwjets_err = nwjets*0.5;
  //f += (par[1]-nwjets)*(par[1]-nwjets)/nwjets_err/nwjets_err;

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
