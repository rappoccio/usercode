#ifndef makeHists_h
#define makeHists_h

#include <TH1.h>
#include <TString.h>
#include <THStack.h>
#include <TColor.h>
#include <TFile.h>
#include <TROOT.h>
#include <Rtypes.h>
#include <vector>
#include <iostream>


// -------------------------------------------------------------------------------------
// various declarations
// -------------------------------------------------------------------------------------

const double LUM = 19.7;
bool use2D = true;

bool do_htlep150qcd = false;
bool do_met50qcd = false;
bool do_qcd = true;  //add triangular cut for electrons

bool extLumi = true;
bool extBtag = true;
bool extJet = false;
bool extToptag = false;

bool addBSM = false;

TString fittype = "";

// END USER SETTINGS

int getRebin(TString var){
  int rebin = 1;
  if (var=="etaAbsLep") rebin = 2;
  else if (var=="vtxMass") rebin = 2;
  else if (var=="htLep") rebin = 8;

  return rebin;
}

TString extName = "";

void setExtName () {
  if (extBtag) extName += "_nobtag";
  if (extLumi) extName += "_nolumi";
  if (extJet) extName += "_nojet";
  if (extToptag) extName += "_notoptag";
  if (fittype != "") extName += "_"+fittype;
  if (addBSM) extName += "_withBSM";
}



// -------------------------------------------------------------------------------------
// helper class for summed, weighted histograms (e.g. single top)
// -------------------------------------------------------------------------------------

class SummedHist {
 public : 
 SummedHist( TString const & name, int color ) : name_(name), color_(color) {
    summedHist_ = 0;
  };
  
  // return the summed histogram if created, else create it (summing up histograms in vector hists_) 
  TH1F* hist() { 
    if (summedHist_ != 0) {
      return summedHist_; 
    }
    else if (hists_.size() == 0) {
      return 0; 
    } 
    else {
      summedHist_ = (TH1F*)hists_[0]->Clone();
      summedHist_->SetName( name_ );
      summedHist_->SetFillColor( color_ );
      for (unsigned int j = 1; j<hists_.size(); ++j) {
	summedHist_->Add( hists_[j], 1.0 );
      }
      return summedHist_; 
    };
  }

  // return the vector of input histograms  
  std::vector<TH1F*> const & hists() const {
    return hists_;
  }
  
  // add histogram to the vector of inputs
  void push_back( TH1F const * ihist, double norm ) {
    TH1F* clone = (TH1F*) ihist->Clone();
    TString iname( name_ );
    iname += hists_.size();
    clone->SetName( iname );
    clone->Scale( norm );
    hists_.push_back( clone );
    norms_.push_back( norm );
  };
  

 protected : 
  
  std::vector<TH1F*> hists_;
  std::vector<double> norms_;
  
  TString name_; 
  int color_;
  TH1F* summedHist_; 
  
};


// -------------------------------------------------------------------------------------
// modify name for theta input
// -------------------------------------------------------------------------------------

void adjustThetaName( TString & thetaname, TString name, TString ptbin = "" ) {
  if      ( name == "nom" ) return;
  else if ( name == "pdfup_CT10" ) thetaname += "__pdf_CT10__up";
  else if ( name == "pdfdn_CT10" ) thetaname += "__pdf_CT10__down";
  else if ( name == "nom_MSTW" )   thetaname += "__pdf_MSTW__nom";
  else if ( name == "pdfup_MSTW" ) thetaname += "__pdf_MSTW__up";
  else if ( name == "pdfdn_MSTW" ) thetaname += "__pdf_MSTW__down";
  else if ( name == "nom_NNPDF" )   thetaname += "__pdf_NNPDF__nom";
  else if ( name == "pdfup_NNPDF" ) thetaname += "__pdf_NNPDF__up";
  else if ( name == "pdfdn_NNPDF" ) thetaname += "__pdf_NNPDF__down";
  else if ( name == "jecdn" ) thetaname += "__jec__down";
  else if ( name == "jecup" ) thetaname += "__jec__up";
  else if ( name == "jerdn" ) thetaname += "__jer__down";
  else if ( name == "jerup" ) thetaname += "__jer__up";
  else if ( name == "scaledown_nom" ) thetaname += "__scale__down";
  else if ( name == "scaleup_nom" ) thetaname += "__scale__up";
  else if ( name == "toptagdn" ) thetaname += "__toptag"+ptbin+"__down";
  else if ( name == "toptagup" ) thetaname += "__toptag"+ptbin+"__up";
  else if ( name == "btagdn" ) thetaname += "__btag__down";
  else if ( name == "btagup" ) thetaname += "__btag__up";
  else if ( name == "qcd" ) thetaname += "qcd";
  else {
    std::cerr << "name is " << name << std::endl;
    std::cerr << "Problem in adjusting theta name  " << thetaname << " ! broken!" << std::endl;
  }
  return;
}


// -------------------------------------------------------------------------------------
// W+jets
// -------------------------------------------------------------------------------------

SummedHist * getWJets( TString name, TString histname, bool doElectron, TString ptbin = "") {

  const int nwjets = 4;

  TString DIR = "histfiles/";
  if (do_qcd && doElectron) DIR += "qcd_el/";
  else if (use2D && doElectron) DIR += "2Dhist_el/";
  else if (use2D) DIR += "2Dhist/";

  if (do_htlep150qcd) {
    DIR = "histfiles_htlep150/";
    if (doElectron) DIR = "histfiles_htlep150qcd/";
  }
  else if (do_met50qcd) {
    DIR = "histfiles_met50qcd/";
  }

  TString muOrEl = "mu";
  if (doElectron) muOrEl = "el";

  TString wjets_names[nwjets] = {
    "W1JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_"+muOrEl+"_",
    "W2JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_"+muOrEl+"_",
    "W3JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_"+muOrEl+"_",
    "W4JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_"+muOrEl+"_",
  };
  double wjets_norms[nwjets] = {
    5400. * 1.207 * 1000. * LUM / 23141598.,  // W+1 jets
    1750. * 1.207 * 1000. * LUM / 34044921.,  // W+2 jets
    519. * 1.207 * 1000. * LUM  / 15539503.,  // W+3 jets
    214. * 1.207 * 1000. * LUM  / 13382803.   // W+4 jets
  };

  TString thetaChannel = "mu_";
  if (doElectron) thetaChannel = "el_";

  TString thetaname = thetaChannel + histname + "__WJets";
  adjustThetaName( thetaname, name, ptbin );
  
  SummedHist* wjets = new SummedHist( thetaname, kGreen-3 );
  
  TString name2d = "";
  if (use2D) name2d = "2Dcut_";

  for (int i=0 ; i<nwjets; i++) {
    TString iname = DIR + wjets_names[i] + name2d + name + ".root";
    TFile* infile = TFile::Open( iname );
    TH1F* hist = (TH1F*) infile->Get(histname)->Clone();
    hist->Sumw2();
    wjets->push_back( hist, wjets_norms[i] );
    delete infile;
  }

  return wjets;

}

//--------------------------------------------------------------------------------------
// BSM
// -------------------------------------------------------------------------------------

SummedHist * getBSM(TString histname, bool doElectron) {

  TString muOrEl = "mu";
  if (doElectron) muOrEl = "el";

  TString BSMfile = "histfiles_BSM/TT_M-1000_Tune4C_8TeV-pythia8_mu_iheartNY_"+muOrEl+"_2Dcut.root";

  double BSMnorm = 0.1 * 1000. * LUM / 100000.;

  TString thetaChannel = "mu_";
  if (doElectron) thetaChannel = "el_";

  TString thetaname = thetaChannel + histname + "__BSM";
  adjustThetaName( thetaname, "nom", "" );
  
  SummedHist* bsm = new SummedHist( thetaname, kRed+1 );
  
  TFile* infile = TFile::Open( BSMfile );
  TH1F* hist = (TH1F*) infile->Get(histname)->Clone();
  hist->Sumw2();
  bsm->push_back( hist, BSMnorm );
  delete infile;
  
  return bsm;

}

// -------------------------------------------------------------------------------------
// single top
// -------------------------------------------------------------------------------------

SummedHist * getSingleTop( TString name, TString histname, bool doElectron, TString ptbin = "") {

  const int nsingletop = 6;

  TString DIR = "histfiles/";
  if (do_qcd && doElectron) DIR += "qcd_el/";
  else if (use2D && doElectron) DIR += "2Dhist_el/";
  else if (use2D) DIR += "2Dhist/";

  if (do_htlep150qcd) {
    DIR = "histfiles_htlep150/";
    if (doElectron) DIR = "histfiles_htlep150qcd/";
  }
  else if (do_met50qcd) {
    DIR = "histfiles_met50qcd/";
  }

  TString muOrEl = "mu";
  if (doElectron) muOrEl = "el";

  TString singletop_names[nsingletop] = {
    "T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_",
    "Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_",
    "T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_",
    "Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_",
    "T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_",
    "Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_",
  };
  double singletop_norms[nsingletop] = {
    3.79 * 1000. * LUM / 259961. , // All single-top approx NNLO cross sections from
    1.76 * 1000. * LUM / 139974. , // https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma8TeV
    56.4 * 1000. * LUM / 3758227.,
    30.7 * 1000. * LUM / 1935072., 
    11.1 * 1000. * LUM / 497658. , 
    11.1 * 1000. * LUM / 493460.
  };

  TString thetaChannel = "mu_";
  if (doElectron) thetaChannel = "el_";

  TString thetaname = thetaChannel + histname + "__SingleTop";
  adjustThetaName( thetaname, name, ptbin );

  SummedHist* singletop = new SummedHist( thetaname, 6 );

  TString name2d = "";
  if (use2D) name2d = "2Dcut_";

  for (int i=0; i<nsingletop; i++) {
    TString iname = DIR + singletop_names[i] + name2d + name + ".root";
    TFile* infile = TFile::Open( iname );
    TH1F* hist = (TH1F*) infile->Get(histname);
    hist->Sumw2();
    singletop->push_back( hist, singletop_norms[i] );
    delete infile;
  }
  
  return singletop;

}


// -------------------------------------------------------------------------------------
// non-semileptonic ttbar
// -------------------------------------------------------------------------------------

SummedHist * getTTbarNonSemiLep( TString name, TString histname, bool doElectron, TString ptbin = "", TString pdfdir = "CT10_nom" ) {

  if (pdfdir=="MG") {

    TString DIR = "histfiles_MG/";
    
    TString muOrEl = "mu";
    if (doElectron) muOrEl = "el";
    
    TString ttbar_name1 = "TTJets_HadronicMGDecays_8TeV-madgraph_iheartNY_V1_"+muOrEl+"_";
    TString ttbar_name2 = "TTJets_FullLeptMGDecays_8TeV-madgraph_iheartNY_V1_"+muOrEl+"_";
    
    double ttbar_norm1 = 252.89*1000.0*19.7/10537444.*0.457;
    double ttbar_norm2 = 252.89*1000.0*19.7/12119013.*0.105;
    
    TString thetaChannel = "mu_";
    if (doElectron) thetaChannel = "el_";
    
    TString thetaname = thetaChannel + histname + "__TTbar_nonSemiLep";
    adjustThetaName( thetaname, name, ptbin );
    
    SummedHist* ttbar = new SummedHist( thetaname, kRed-7);
    
    TString name2d = "";
    if (use2D) name2d = "2Dcut_";
    
    TString iname1 = DIR + ttbar_name1 + name2d + name + TString(".root");
    TString iname2 = DIR + ttbar_name2 + name2d + name + TString(".root");
    TFile* infile1 = TFile::Open( iname1 );
    TFile* infile2 = TFile::Open( iname2 );
    TH1F* hist1 = (TH1F*) infile1->Get(histname);
    TH1F* hist2 = (TH1F*) infile2->Get(histname);
    hist1->Sumw2();
    hist2->Sumw2();
    ttbar->push_back( hist1, ttbar_norm1 );
    ttbar->push_back( hist2, ttbar_norm2 );
    delete infile1;
    delete infile2;
    
    return ttbar;
    
  }
  else { 
    
    const int nttbar = 3;
    const int nq2 = 3;
    
    TString DIR = "histfiles_" + pdfdir + "/";
    if (do_qcd && doElectron) DIR += "qcd_el/";
    else if (use2D && doElectron) DIR += "2Dhists_el/";
    else if (use2D) DIR += "2Dhists/";
    
    if (do_htlep150qcd) {
      DIR = "histfiles_htlep150/";
      if (doElectron) DIR = "histfiles_htlep150qcd/";
    }
    else if (do_met50qcd) {
      DIR = "histfiles_met50qcd/";
    }
    
    TString muOrEl = "mu";
    if (doElectron) muOrEl = "el";
    
    TString ttbar_names[nttbar] = {
      "TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_",
      "TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_",
      "TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"
    };
    double ttbar_xs[nq2] = {
      252.89 * 1000. * LUM,  // nominal
      (252.89+6.39) * 1000. * LUM,  // q2 up
      (252.89-8.64) * 1000. * LUM   // q2 down
    };
    double ttbar_nevents[nq2][nttbar] = {
      {21675970., 3082812., 1249111.},  // nominal
      {14983686., 2243672., 1241650.},  // q2 up
      {14545715*89./102., 2170074., 1308090.}   // q2 down
    };
    double ttbar_eff[nq2][nttbar] = {
      {1.0, 0.074, 0.015},  // nominal
      {1.0, 0.074, 0.014},  // q2 up
      {1.0, 0.081, 0.016}   // q2 down
    };
    
    unsigned int iq2 = 0;
    if ( pdfdir.Contains("scaleup") ) iq2 = 1;
    if ( pdfdir.Contains("scaledown") ) iq2 = 2;
    
    double ttbar_norms[nttbar] = {
      ttbar_xs[iq2] * ttbar_eff[iq2][0] / ttbar_nevents[iq2][0],
      ttbar_xs[iq2] * ttbar_eff[iq2][1] / ttbar_nevents[iq2][1],
      ttbar_xs[iq2] * ttbar_eff[iq2][2] / ttbar_nevents[iq2][2]
    };
    
    TString thetaChannel = "mu_";
    if (doElectron) thetaChannel = "el_";
    
    TString thetaname = thetaChannel + histname + "__TTbar_nonSemiLep";
    adjustThetaName( thetaname, name, ptbin );
    
    SummedHist* ttbar = new SummedHist( thetaname, kRed-7);
    
    TString name2d = "";
    if (use2D) name2d = "2Dcut_";
    
    for (int i=0; i<nttbar; i++) {
      TString iname = DIR + ttbar_names[i] + pdfdir + "_" + name2d + name + ".root";
      TFile* infile = TFile::Open( iname );
      TH1F* hist = (TH1F*) infile->Get(histname);
      hist->Sumw2();
      ttbar->push_back( hist, ttbar_norms[i] );
      delete infile;
    }
    
    return ttbar;
    
  }
}


// -------------------------------------------------------------------------------------
// signal ttbar
// -------------------------------------------------------------------------------------

SummedHist * getTTbar( TString name, TString histname, bool doElectron, TString ptbin = "", TString pdfdir = "CT10_nom" ) {

  if (pdfdir=="MG") {

    TString DIR = "histfiles_MG/";

    TString muOrEl = "mu";
    if (doElectron) muOrEl = "el";
    
    TString ttbar_name = "TTJets_SemiLeptMGDecays_8TeV-madgraph_iheartNY_V1_"+muOrEl+"_";
    
    double ttbar_norm = 252.89*1000.0*19.7/25424818.*0.438;
    
    TString thetaChannel = "mu_";
    if (doElectron) thetaChannel = "el_";
    
    TString thetaname = thetaChannel + histname + "__TTbar_semiLep";
    adjustThetaName( thetaname, name, ptbin );
    
    SummedHist* ttbar = new SummedHist( thetaname, kRed +1);
    
    TString name2d = "";
    if (use2D) name2d = "2Dcut_";
    
    TString iname = DIR + ttbar_name + name2d + name + TString(".root");
    TFile* infile = TFile::Open( iname );
    TH1F* hist = (TH1F*) infile->Get(histname);
    hist->Sumw2();
    ttbar->push_back( hist, ttbar_norm );
    delete infile;

    return ttbar;
  }
  else {

    const int nttbar = 3;
    const int nq2 = 3;
    
    TString DIR = "histfiles_" + pdfdir + "/";
    if (do_qcd && doElectron) DIR += "qcd_el/";
    else if (use2D && doElectron) DIR += "2Dhists_el/";
    else if (use2D) DIR += "2Dhists/";
    
    if (do_htlep150qcd) {
      DIR = "histfiles_htlep150/";
      if (doElectron) DIR = "histfiles_htlep150qcd/";
    }
    else if (do_met50qcd) {
      DIR = "histfiles_met50qcd/";
    }
    
    TString muOrEl = "mu";
    if (doElectron) muOrEl = "el";
    
    
    TString ttbar_names[nttbar] = {
      "TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_",
      "TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_",
      "TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"
    };
    double ttbar_xs[nttbar] = {
      //245.8 * 1000. * LUM,  // nominal
      //252.0 * 1000. * LUM,  // q2 up
      //237.4 * 1000. * LUM   // q2 down
      252.89 * 1000. * LUM,  // nominal
      (252.89+6.39) * 1000. * LUM,  // q2 up
      (252.89-8.64) * 1000. * LUM   // q2 down
    };
    double ttbar_nevents[nq2][nttbar] = {
      {21675970.,3082812.,1249111.},  // nominal
      {14983686.,2243672.,1241650.},  // q2 up
      {14545715*89./102.,2170074.,1308090.}   // q2 down
    };
    double ttbar_eff[nq2][nttbar] = {
      {1.0, 0.074, 0.015},  // nominal
      {1.0, 0.074, 0.014},  // q2 up
      {1.0, 0.081, 0.016}   // q2 down
    };
    
    unsigned int iq2 = 0;
    if ( pdfdir.Contains("scaleup") ) iq2 = 1;
    if ( pdfdir.Contains("scaledown") )iq2 = 2;
    
    double ttbar_norms[nttbar] = {    
      ttbar_xs[iq2] * ttbar_eff[iq2][0] / ttbar_nevents[iq2][0],
      ttbar_xs[iq2] * ttbar_eff[iq2][1] / ttbar_nevents[iq2][1],
      ttbar_xs[iq2] * ttbar_eff[iq2][2] / ttbar_nevents[iq2][2],
    };
    
    TString thetaChannel = "mu_";
    if (doElectron) thetaChannel = "el_";
    
    TString thetaname = thetaChannel + histname + "__TTbar_semiLep";
    adjustThetaName( thetaname, name, ptbin );
    
    SummedHist* ttbar = new SummedHist( thetaname, kRed +1);
    
    TString name2d = "";
    if (use2D) name2d = "2Dcut_";
    
    for (int i=0; i<nttbar; i++) {
      TString iname = DIR + ttbar_names[i] + pdfdir + "_" + name2d + name + TString(".root");
      TFile* infile = TFile::Open( iname );
      TH1F* hist = (TH1F*) infile->Get(histname);
      hist->Sumw2();
      ttbar->push_back( hist, ttbar_norms[i] );
      delete infile;
    }
    
    return ttbar;
  }

}


// -------------------------------------------------------------------------------------
// QCD
// -------------------------------------------------------------------------------------

SummedHist * getQCD( TString var, bool doElectron, TString ptbin = "" ) {

  SummedHist* wjets_qcd = getWJets( "qcd", var, doElectron, ptbin );
  SummedHist* singletop_qcd = getSingleTop( "qcd", var, doElectron, ptbin );
  SummedHist* ttbar_qcd = getTTbar( "qcd", var, doElectron, ptbin );
  SummedHist* ttbar_nonsemilep_qcd = getTTbarNonSemiLep( "qcd", var, doElectron, ptbin );

  SummedHist* qcd;
  if (doElectron) qcd = new SummedHist( "el_" + var + "__QCD", kYellow);
  else qcd = new SummedHist( "mu_" + var + "__QCD", kYellow);

  TString filepath;
  if (doElectron && use2D) filepath = "histfiles/2Dhist_el/SingleEl_iheartNY_V1_el_Run2012_2Dcut_qcd.root";
  else if (use2D) filepath = "histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_qcd.root";
  else filepath = "histfiles/SingleMu_iheartNY_V1_mu_Run2012_qcd.root";

  if (do_htlep150qcd) {
    if (doElectron) filepath = "histfiles_htlep150qcd/SingleEl_iheartNY_V1_el_Run2012_2Dcut_qcd.root";
    else filepath = "histfiles_htlep150/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_qcd.root";
  }
  else if (do_met50qcd) {
    if (doElectron) filepath = "histfiles_met50qcd/SingleEl_iheartNY_V1_el_Run2012_2Dcut_qcd.root";
    else filepath = "histfiles_met50qcd/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_qcd.root";
  }
  else if (do_qcd) {
    if (doElectron) filepath = "histfiles/qcd_el/SingleEl_iheartNY_V1_el_Run2012_2Dcut_qcd.root";
    else filepath = "histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_qcd.root";
  }

  TFile* qcdFile = TFile::Open(filepath);
  TH1F* qcdHistRaw = (TH1F*) qcdFile->Get(var);
  qcdHistRaw->Sumw2();

  qcdHistRaw->Add( wjets_qcd->hist(), -1.0 );
  qcdHistRaw->Add( singletop_qcd->hist(), -1.0 );
  qcdHistRaw->Add( ttbar_qcd->hist(), -1.0 );
  qcdHistRaw->Add( ttbar_nonsemilep_qcd->hist(), -1.0 );

  for (int ibin=0; ibin<qcdHistRaw->GetNbinsX(); ibin++) {
    if (qcdHistRaw->GetBinContent(ibin+1) < 0.0) {
      //std::cout << "WARNING, negative bin content for QCD histogram" << std::endl;
      qcdHistRaw->SetBinContent(ibin+1, 0.0);
    }
  }
  
  qcd->push_back( qcdHistRaw, 1.);

  return qcd;

}

float getPostPreRatio(bool doElectron, TString ptbin, TString pdfdir, bool combined, TString sample, int cut, int cut2){

  // post-fit file
  TFile* fPOST;
  if (combined) {
    if (ptbin == "") fPOST = new TFile("run_theta/histos-mle-2d-"+pdfdir+"_comb"+extName+".root");
    else fPOST = new TFile("run_theta/histos-mle-2d-"+pdfdir+"_comb"+extName+"_2bin.root");
  }
  else if (doElectron) {
    if (ptbin == "") fPOST = new TFile("run_theta/histos-mle-2d-"+pdfdir+"_el"+extName+".root");
    else fPOST = new TFile("run_theta/histos-mle-2d-"+pdfdir+"_el"+extName+"_2bin.root");
  }
  else {
    if (ptbin == "") fPOST = new TFile("run_theta/histos-mle-2d-"+pdfdir+"_mu"+extName+".root");
    else fPOST = new TFile("run_theta/histos-mle-2d-"+pdfdir+"_mu"+extName+"_2bin.root");
  }

  // pre-fit file
  TFile* fPRE;
  if (doElectron) {
    if (cut == 4) fPRE = new TFile("NormalizedHists_"+pdfdir+"/normalized2d_eljets_etaAbsLep6"+ptbin+"_subtracted_from_etaAbsLep4"+ptbin+".root");
    if (cut == 6) fPRE = new TFile("NormalizedHists_"+pdfdir+"/normalized2d_eljets_etaAbsLep7"+ptbin+"_subtracted_from_etaAbsLep6"+ptbin+".root");
    if (cut == 7) fPRE = new TFile("NormalizedHists_"+pdfdir+"/normalized2d_eljets_vtxMass7"+ptbin+".root");
  }
  else {
    if (cut == 4) fPRE = new TFile("NormalizedHists_"+pdfdir+"/normalized2d_mujets_etaAbsLep6"+ptbin+"_subtracted_from_etaAbsLep4"+ptbin+".root");
    if (cut == 6) fPRE = new TFile("NormalizedHists_"+pdfdir+"/normalized2d_mujets_etaAbsLep7"+ptbin+"_subtracted_from_etaAbsLep6"+ptbin+".root");
    if (cut == 7) fPRE = new TFile("NormalizedHists_"+pdfdir+"/normalized2d_mujets_vtxMass7"+ptbin+".root");
  }

  TString channel = "mu_";
  if (doElectron) channel = "el_";

  TString what = "";
  if (cut == 4) what = "etaAbsLep4"+ptbin;
  if (cut == 6) what = "etaAbsLep6"+ptbin;
  if (cut == 7) what = "vtxMass7"+ptbin;

  TString hist = "";
  if (sample == "ttbar") hist = "__TTbar";
  if (sample == "singletop") hist = "__SingleTop";
  if (sample == "wjets") hist = "__WJets";
  if (sample == "qcd") hist = "__QCD";

  // Get histograms
  TH1F* h_post = (TH1F*) fPOST->Get(channel+what+hist);
  TH1F* h_pre = (TH1F*) fPRE->Get(channel+what+hist);

  // Get additional histograms if (cut,cut2) = (6,0)
  TH1F* h_post2;
  TH1F* h_pre2;
  if (cut == 6 && cut2 == 0){
    TFile* fPRE2;
    if (doElectron) fPRE2 = new TFile("NormalizedHists_"+pdfdir+"/normalized2d_eljets_vtxMass7"+ptbin+".root");
    else fPRE2 = new TFile("NormalizedHists_"+pdfdir+"/normalized2d_mujets_vtxMass7"+ptbin+".root");
    h_post2 = (TH1F*) fPOST->Get(channel+"vtxMass7"+ptbin+hist);
    h_pre2 = (TH1F*) fPRE2->Get(channel+"vtxMass7"+ptbin+hist);
  }

  // Calculate ratio
  float postPreRatio;
  if (cut == 6 && cut2 == 0) postPreRatio = ( h_post->Integral() + h_post2->Integral() ) / ( h_pre->Integral() + h_pre2->Integral() );
  else postPreRatio = h_post->Integral() / h_pre->Integral();

  return postPreRatio;
}

// -------------------------------------------------------------------------------------
// QCD normalization
// -------------------------------------------------------------------------------------

std::pair<double, double> getQCDnorm(int cut, bool doElectron, TString ptbin, bool half = false) {

  if ( !(cut==4||cut==5||cut==6||cut==7) ) {
    std::cout << "Not a valid cut option! Options are cut == 4,5,6,7. Exiting..." << std::endl;
    return std::make_pair(0,0);
  }

  float qcd_mu_reliso_norm[8] = {0.0, 0.0, 0.0, 0.0,  401.4, 0.0, 28.5,  1.0};
  float qcd_mu_reliso_err[8]  = {0.0, 0.0, 0.0, 0.0,   71.6, 0.0, 21.5, 10.0};
  //float qcd_mu_2Dcut_norm[8]  = {0.0, 0.0, 0.0, 0.0, 1450., 0.0, 58., 11.0};
  //float qcd_mu_2Dcut_err[8]   = {0.0, 0.0, 0.0, 0.0,   82., 0.0, 24., 13.0};
  float qcd_mu_2Dcut_norm[8]  = {0.0, 0.0, 0.0, 0.0, 1471., 0.0, 55., 12.0};
  float qcd_mu_2Dcut_err[8]   = {0.0, 0.0, 0.0, 0.0,   82., 0.0, 24., 13.0};

  // HTlep > 150 GeV
  if (do_htlep150qcd) {
    qcd_mu_2Dcut_norm[4] = 0.0;
    qcd_mu_2Dcut_norm[5] = 722.0;
    qcd_mu_2Dcut_norm[6] = 10.0;
    qcd_mu_2Dcut_norm[7] = 0.0;
    qcd_mu_2Dcut_err[4] = 0.0;
    qcd_mu_2Dcut_err[5] = 95.0;
    qcd_mu_2Dcut_err[6] = 10.0;
    qcd_mu_2Dcut_err[7] = 0.0;
  }
  // MET > 50 GeV
  else if (do_met50qcd) {
    qcd_mu_2Dcut_norm[4] = 180.0;
    qcd_mu_2Dcut_norm[5] = 0.0;
    qcd_mu_2Dcut_norm[6] = 31.0;
    qcd_mu_2Dcut_norm[7] = 0.0;
    qcd_mu_2Dcut_err[4] = 44.0;
    qcd_mu_2Dcut_err[5] = 0.0;
    qcd_mu_2Dcut_err[6] = 13.0;;
    qcd_mu_2Dcut_err[7] = 3.2;
  }
  else if (do_qcd) {
    // this means the default scenario for muons
  }

  //Old version, using numbers from Feb. 6
  //float qcd_el_2Dcut_norm[8]  = {0.0, 0.0, 0.0, 0.0, 4107., 0.0, 257., 20.5};
  //float qcd_el_2Dcut_err[8]   = {0.0, 0.0, 0.0, 0.0,   71., 0.0,  18.,  6.7};
  float qcd_el_2Dcut_norm[8]  = {0.0, 0.0, 0.0, 0.0, 4202., 0.0, 256., 27.8};
  float qcd_el_2Dcut_err[8]   = {0.0, 0.0, 0.0, 0.0,   73., 0.0,  18.,  7.1};
  
  // HTlep > 150 GeV
  //float qcd_el_2Dcut_norm[8]  = {0.0, 0.0, 0.0, 0.0, 0.0, 2981., 194., 16.2};
  //float qcd_el_2Dcut_err[8]   = {0.0, 0.0, 0.0, 0.0, 0.0, 55., 14.3, 7.2};
  
  // HTlep > 150 GeV + triangular cut
  if (do_htlep150qcd) {
    qcd_el_2Dcut_norm[4] = 0.0;
    qcd_el_2Dcut_norm[5] = 362.2;
    qcd_el_2Dcut_norm[6] = 31.0;
    qcd_el_2Dcut_norm[7] = 6.5;
    qcd_el_2Dcut_err[4] = 0.0;
    qcd_el_2Dcut_err[5] = 18.8;
    qcd_el_2Dcut_err[6] = 5.7;
    qcd_el_2Dcut_err[7] = 2.9;
  }
  // MET > 50 GeV + triangular cut
  else if (do_met50qcd) {
    qcd_el_2Dcut_norm[4] = 101.0;
    qcd_el_2Dcut_norm[5] = 0.0;
    qcd_el_2Dcut_norm[6] = 23.0;
    qcd_el_2Dcut_norm[7] = 2.2;
    qcd_el_2Dcut_err[4] = 35.0;
    qcd_el_2Dcut_err[5] = 0.0;
    qcd_el_2Dcut_err[6] = 15.0;
    qcd_el_2Dcut_err[7] = 1.9;
  }
  else if (do_qcd) {
    //qcd_el_2Dcut_norm[4] = 448.;
    //qcd_el_2Dcut_norm[5] = 448.;
    //qcd_el_2Dcut_norm[6] = 40.3;
    //qcd_el_2Dcut_norm[7] = 6.2;
    //qcd_el_2Dcut_err[4] = 23.;
    //qcd_el_2Dcut_err[5] = 23.;
    //qcd_el_2Dcut_err[6] = 6.5;
    //qcd_el_2Dcut_err[7] = 3.0;

    qcd_el_2Dcut_norm[4] = 448.;
    qcd_el_2Dcut_norm[5] = 448.;
    qcd_el_2Dcut_norm[6] = 40.0;
    qcd_el_2Dcut_norm[7] = 6.2;
    qcd_el_2Dcut_err[4] = 23.;
    qcd_el_2Dcut_err[5] = 23.;
    qcd_el_2Dcut_err[6] = 6.5;
    qcd_el_2Dcut_err[7] = 3.0;
  }

  float qcd_norm = 0;
  float qcd_err  = 0;
  if (use2D && doElectron) {
    if (half) {qcd_norm = qcd_el_2Dcut_norm[cut] / 2.;}
    else {qcd_norm = qcd_el_2Dcut_norm[cut];}
    qcd_err  = qcd_el_2Dcut_err[cut];
  }
  else if (use2D) {
    if (half) {qcd_norm = qcd_mu_2Dcut_norm[cut] / 2.;}
    else {qcd_norm = qcd_mu_2Dcut_norm[cut];}
    qcd_err  = qcd_mu_2Dcut_err[cut];
  }
  else {
    if (half) {qcd_norm = qcd_mu_reliso_norm[cut] / 2.;}
    else {qcd_norm = qcd_mu_reliso_norm[cut];}
    qcd_err  = qcd_mu_reliso_err[cut];
  }

  if (ptbin != ""){
    TH1F* h_qcd_bin;
    TH1F* h_qcd_sum;

    if (cut == 4){
      SummedHist* qcd_bin_4 = getQCD("etaAbsLep4"+ptbin, doElectron, ptbin );
      SummedHist* qcd_bin_6 = getQCD("etaAbsLep6"+ptbin, doElectron, ptbin );
      SummedHist* qcd_sum_4 = getQCD("etaAbsLep4", doElectron, "");
      SummedHist* qcd_sum_6 = getQCD("etaAbsLep6", doElectron, "");
      
      h_qcd_bin = (TH1F*) qcd_bin_4->hist();
      h_qcd_sum = (TH1F*) qcd_sum_4->hist();
      h_qcd_bin->Add(qcd_bin_6->hist(), -1);
      h_qcd_sum->Add(qcd_sum_6->hist(), -1);      
    }

    if (cut == 5){
      SummedHist* qcd_bin_5 = getQCD("etaAbsLep5"+ptbin, doElectron, ptbin );
      SummedHist* qcd_bin_6 = getQCD("etaAbsLep6"+ptbin, doElectron, ptbin );
      SummedHist* qcd_sum_5 = getQCD("etaAbsLep5", doElectron, "");
      SummedHist* qcd_sum_6 = getQCD("etaAbsLep6", doElectron, "");
      
      h_qcd_bin = (TH1F*) qcd_bin_5->hist();
      h_qcd_sum = (TH1F*) qcd_sum_5->hist();
      h_qcd_bin->Add(qcd_bin_6->hist(), -1);
      h_qcd_sum->Add(qcd_sum_6->hist(), -1);      
    }

    if (cut == 6){
      SummedHist* qcd_bin_6 = getQCD("etaAbsLep6"+ptbin, doElectron, ptbin );
      SummedHist* qcd_bin_7 = getQCD("etaAbsLep7"+ptbin, doElectron, ptbin );
      SummedHist* qcd_sum_6 = getQCD("etaAbsLep6", doElectron, "");
      SummedHist* qcd_sum_7 = getQCD("etaAbsLep7", doElectron, "");
      
      h_qcd_bin = (TH1F*) qcd_bin_6->hist();
      h_qcd_sum = (TH1F*) qcd_sum_6->hist();
      h_qcd_bin->Add(qcd_bin_7->hist(), -1);
      h_qcd_sum->Add(qcd_sum_7->hist(), -1);
      
    }
    
    if (cut == 7){
      SummedHist* qcd_bin_0 = getQCD("vtxMass7"+ptbin, doElectron, ptbin );
      SummedHist* qcd_sum_0 = getQCD("vtxMass7", doElectron, "");
      
      h_qcd_bin = (TH1F*) qcd_bin_0->hist();
      h_qcd_sum = (TH1F*) qcd_sum_0->hist();
    }

    float ratio = h_qcd_bin->Integral() / h_qcd_sum->Integral();
    qcd_norm = qcd_norm * ratio;
  }

  return std::make_pair(qcd_norm, qcd_err);

}




#endif
