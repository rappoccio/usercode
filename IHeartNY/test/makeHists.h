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


// -------------------------------------------------------------------------------------
// QCD normalization
// -------------------------------------------------------------------------------------

std::pair<double, double> getQCDnorm(int cut, bool doElectron) {

  if ( !(cut==4||cut==6||cut==7) ) {
    std::cout << "Not a valid cut option! Options are cut == 4,6,7. Exiting..." << std::endl;
    return std::make_pair(0,0);
  }

  float qcd_mu_reliso_norm[8] = {0.0, 0.0, 0.0, 0.0,  401.4, 0.0, 28.5,  1.0};
  float qcd_mu_reliso_err[8]  = {0.0, 0.0, 0.0, 0.0,   71.6, 0.0, 21.5, 10.0};
  //float qcd_mu_2Dcut_norm[8]  = {0.0, 0.0, 0.0, 0.0, 1207.7, 0.0, 29.5,  9.3};
  //float qcd_mu_2Dcut_err[8]   = {0.0, 0.0, 0.0, 0.0,   80.4, 0.0, 21.5, 14.6};

  // preliminary version of muon values with new ntuples -- needs to be checked!
  float qcd_mu_2Dcut_norm[8]  = {0.0, 0.0, 0.0, 0.0, 1449.6, 0.0, 57.5,  11.0};
  float qcd_mu_2Dcut_err[8]   = {0.0, 0.0, 0.0, 0.0,   81.8, 0.0, 23.7, 12.8};

  // for now, electrons using same values as for muons -- needs to be updated!
  //float qcd_el_2Dcut_norm[8]  = {0.0, 0.0, 0.0, 0.0, 3653.2, 0.0, 210.4, 0.0};
  //float qcd_el_2Dcut_err[8]   = {0.0, 0.0, 0.0, 0.0,  322.8, 0.0,  16.1, 0.0};
  float qcd_el_2Dcut_norm[8]  = {0.0, 0.0, 0.0, 0.0, 0, 0.0, 0, 0.0};
  float qcd_el_2Dcut_err[8]   = {0.0, 0.0, 0.0, 0.0,  0, 0.0,  0, 0.0};

  float qcd_norm = 0;
  float qcd_err  = 0;
  if (use2D && doElectron) {
    qcd_norm = qcd_el_2Dcut_norm[cut];
    qcd_err  = qcd_el_2Dcut_err[cut];
  }
  else if (use2D) {
    qcd_norm = qcd_mu_2Dcut_norm[cut];
    qcd_err  = qcd_mu_2Dcut_err[cut];
  }
  else {
    qcd_norm = qcd_mu_reliso_norm[cut];
    qcd_err  = qcd_mu_reliso_err[cut];
  }

  return std::make_pair(qcd_norm, qcd_err);

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

void adjustThetaName( TString & thetaname, TString name ) {
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
  else if ( name == "toptagdn" ) thetaname += "__toptag__down";
  else if ( name == "toptagup" ) thetaname += "__toptag__up";
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

SummedHist * getWJets( TString name, TString histname, bool doElectron ) {

  const int nwjets = 4;

  TString DIR = "histfiles/";
  if (use2D && doElectron) DIR += "2Dhist_el/";
  else if (use2D) DIR += "2Dhist/";

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

  TString thetaname = histname + "__WJets";
  adjustThetaName( thetaname, name );
  
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


// -------------------------------------------------------------------------------------
// single top
// -------------------------------------------------------------------------------------

SummedHist * getSingleTop( TString name, TString histname, bool doElectron ) {

  const int nsingletop = 6;

  TString DIR = "histfiles/";
  if (use2D && doElectron) DIR += "2Dhist_el/";
  else if (use2D) DIR += "2Dhist/";

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

  TString thetaname = histname + "__SingleTop";
  adjustThetaName( thetaname, name );

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

SummedHist * getTTbarNonSemiLep( TString name, TString histname, bool doElectron, TString pdfdir = "CT10_nom" ) {

  const int nttbar = 3;
  const int nq2 = 3;

  TString DIR = "histfiles_" + pdfdir + "/";
  if (use2D && doElectron) DIR += "2Dhists_el/";
  else if (use2D) DIR += "2Dhists/";

  TString muOrEl = "mu";
  if (doElectron) muOrEl = "el";

  TString ttbar_names[nttbar] = {
    "TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_",
    "TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_",
    "TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"
  };
  double ttbar_xs[nq2] = {
    245.8 * 1000. * LUM,  // nominal
    252.0 * 1000. * LUM,  // q2 up
    237.4 * 1000. * LUM   // q2 down
  };
  double ttbar_nevents[nq2][nttbar] = {
    {21675970., 3082812., 1249111.},  // nominal
    {14983686., 2243672., 1241650.},  // q2 up
    {1789004., 2170074., 1308090.}   // q2 down
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
  
  TString thetaname = histname + "__TTbar_nonSemiLep";
  adjustThetaName( thetaname, name );

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


// -------------------------------------------------------------------------------------
// signal ttbar
// -------------------------------------------------------------------------------------

SummedHist * getTTbar( TString name, TString histname, bool doElectron, TString pdfdir = "CT10_nom" ) {

  const int nttbar = 3;
  const int nq2 = 3;

  TString DIR = "histfiles_" + pdfdir + "/";
  if (use2D && doElectron) DIR += "2Dhists_el/";
  else if (use2D) DIR += "2Dhists/";

  TString muOrEl = "mu";
  if (doElectron) muOrEl = "el";


  TString ttbar_names[nttbar] = {
    "TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_",
    "TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_",
    "TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"
  };
  double ttbar_xs[nttbar] = {
    245.8 * 1000. * LUM,  // nominal
    252.0 * 1000. * LUM,  // q2 up
    237.4 * 1000. * LUM   // q2 down
  };
  double ttbar_nevents[nq2][nttbar] = {
    {21675970.,3082812.,1249111.},  // nominal
    {14983686.,2243672.,1241650.},  // q2 up
    {1789004.,2170074.,1308090.}   // q2 down
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

  TString thetaname = histname + "__TTbar_semiLep";
  adjustThetaName( thetaname, name );
  
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


// -------------------------------------------------------------------------------------
// QCD
// -------------------------------------------------------------------------------------

SummedHist * getQCD( TString var, bool doElectron ) {

  SummedHist* wjets_qcd = getWJets( "qcd", var, doElectron );
  SummedHist* singletop_qcd = getSingleTop( "qcd", var, doElectron );
  SummedHist* ttbar_qcd = getTTbar( "qcd", var, doElectron );
  SummedHist* ttbar_nonsemilep_qcd = getTTbarNonSemiLep( "qcd", var, doElectron );

  SummedHist* qcd = new SummedHist( var + "__QCD", kYellow);

  TString filepath;
  if (doElectron && use2D) filepath = "histfiles/2Dhist_el/SingleEl_iheartNY_V1_el_Run2012_2Dcut_qcd.root";
  else if (use2D) filepath = "histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_qcd.root";
  else filepath = "histfiles/SingleMu_iheartNY_V1_mu_Run2012_qcd.root";

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



#endif
