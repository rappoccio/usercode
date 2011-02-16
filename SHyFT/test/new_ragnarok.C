#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooDataHist.h"
#include "RooHistPdf.h"
#include "RooExtendPdf.h"
#include "RooAddPdf.h"
#include "RooAbsPdf.h"
#include "RooNLLVar.h"
#include "RooArgList.h"
#include "RooFitResult.h"
#include "RooPlot.h"
#include "RooFormulaVar.h"
#include "TCanvas.h"
#include "TH1.h"
#include "TFile.h"
#include "TRandom.h"
#include <iostream>
#include <sstream>
#include "RooAbsData.h"
#include "RooAddition.h"
#include "RooMinuit.h"

#include <algorithm>

using namespace RooFit ;
using namespace std;

//bool verbose;

typedef map<string, vector< RooRealVar * > > scaleFact_vect;

class Template {
public:
  Template(TH1F histo, string name, RooRealVar& dataVar, vector<RooRealVar*> scaleFactors);
  //  virtual ~Template() {}
  ~Template();

  RooRealVar   *   norm() { return norm_; }
  RooDataHist  *  hdata() { return rdh_;  }
  RooHistPdf   *    pdf() { return rhp_;  }
  RooExtendPdf *   epdf() { return rep_;  }
  double hnorm() { return hnorm_; }
  TH1F *  hist() { return &hist_;  }
  TH1F * expHist() { return expHist_; }

  void   setupPE( double F );
private:
  TH1F   hist_;          //< Input histogram for fit PDFs
  TH1F  * expHist_;      //< "Experiment" histogram (either PseudoExperiment, or Real Experiment)
  string name_;          //< Name of this template
  double hnorm_;         //< Actual normalization
  RooRealVar   * norm_;  //< Normalization RelVar
  RooDataHist  * rdh_;   //< DataHist for fit
  RooHistPdf   * rhp_;   //< HistPdf for fit
  RooExtendPdf * rep_;   //< What's this for?????           <-----------
  //  RooFormulaVar * form_;
  RooRealVar  binningVar_;
  //  RooRealVar * lum_;
};

Template::Template(TH1F hist, string name, RooRealVar& binningVar, vector<RooRealVar*> scaleFactors)://, RooRealVar& lum, RooRealVar & kFactor):
  hist_(hist),name_(name),binningVar_(binningVar) {//,lum_(scaleFactors[1]) {
  hnorm_   = hist_.Integral();
  cout << "Normaliztion of " << name_.c_str() << " is " << hnorm_ << endl;
  norm_    = new RooRealVar ((name_+"_norm").c_str(), (name_+"_norm").c_str(),hnorm_);//,-1,100000);
  rdh_     = new RooDataHist(name_.c_str(),name_.c_str(),binningVar_, &hist_);
  rhp_     = new RooHistPdf ((name_+"_pdf").c_str(),(name_+"_pdf").c_str(), binningVar_, *rdh_);
  //  lum_ = new RooRealVar (("luminosity","luminosity",lu
  //In the ScaleFactors, 0 is the xsection/fit variable, 1 is the luminosity, 2 is the generated xsection, and 3 is the number of events
  RooFormulaVar * form_ = new RooFormulaVar((name_+"_form").c_str(), (name_+"_form").c_str(),"@0*@1*@2*@3/@4",RooArgSet(*scaleFactors[0], *norm_,*scaleFactors[1],*scaleFactors[2],*scaleFactors[3]));//, lum, kFactor));
  rep_   = new RooExtendPdf((name_+"_epdf").c_str(), (name_+"_epdf").c_str(), *rhp_, *form_);
}

Template::~Template() {
  delete norm_;
  delete rdh_;
  delete rhp_;
  delete rep_;
  // delete form_;
  //  delete binningVar_;
  
}


void Template::setupPE( double F ) {
  expHist_ = new TH1F(hist_);
  expHist_->Scale( F );
}
     

class JetTagBin {
public:
  JetTagBin(TFile & file, vector<string> const & samples, string jtBinName, scaleFact_vect scaleFactor);//map<string, RooRealVar *> scaleFactors);
  ~JetTagBin();
  vector<Template*> & jtTemplates() { return jtTemplates_; }
  
  RooNLLVar * nll()  { return jtNll_; } 

  void setupPE( double nent );
  void inputData( TFile * file );
  void makeNLLVar();
  void plotOn( RooPlot * frame );

  void setKFactors( vector<double> const & inputKFactors ) {
    copy( inputKFactors.begin(), inputKFactors.end(), kFactors_.begin() );
  }

  vector<double>  kFactors() { return kFactors_; };
  
  RooRealVar const * jtFitVar() const { return jtFitVar_;}
  string const & jtBinName() const { return jtBinName_; }
private:
  string jtBinName_;                 //< Bin Name
  TH1F * jtDataHist_;                //< Jet-tag bin template for PDF
  RooRealVar * jtFitVar_;            //< Jet-tag bin fit variable
  RooAbsData * jtData_;              //< Jet-tag bin for data to fit to
  RooAbsPdf  * jtPdf_;               //< The fitting pdf for this jet-tag bin
  RooNLLVar  * jtNll_;               //< Likelihood variable
  vector<Template*> jtTemplates_;    //< Vector of templates representing the various species (ttbar,W+Jets, etc)
  vector<double>  kFactors_;         //< K-factors for each bin for testing
};

JetTagBin::JetTagBin(TFile & file, vector<string> const & samples, string jtBinName, scaleFact_vect scaleFactors)://map<string, RooRealVar *> scaleFactors):
  jtBinName_(jtBinName)
{
  // I don't know if I should provide the guess here --also for different sized bins, I think we may have to dynamically provide range
  // GetBinLowEdge and GetBinWidth should work if we move this below the th1f access
  jtFitVar_= new RooRealVar(jtBinName.c_str(), jtBinName.c_str(), 50, 600);
  for(unsigned int i=0;i<samples.size();++i) {
    string name = samples[i]+jtBinName;
    cout << "opening histogram " << name << endl;
    TH1F * tempHisto = (TH1F*)file.Get(name.c_str());
    TH1F * tempHisto2;
    if(tempHisto==0) {
      cout << "Template " << name << " does not exist" << endl;
      break;
    }
    else
      tempHisto2 = (TH1F*) tempHisto->Clone();

    Template * temp = new Template(*tempHisto2, name, *jtFitVar_, scaleFactors[samples[i]]);//, kFactors_[i]]);
    jtTemplates_.push_back( temp );
    kFactors_.push_back(1.0);
  }
  RooArgList TemplateList;
  //RooArgList NormList;
  cout << "making lists" << endl;
  for(unsigned int i=0;i<jtTemplates_.size();++i) {
    TemplateList.add(*(jtTemplates_[i]->epdf()));
    //TemplateList.add(*(jtTemplates_[i]->rhp()));
    //NormList.add(*(jtTemplates_[i]->norm()));
  }
  cout << "making combined pdf" << endl;
  jtPdf_ = new RooAddPdf((jtBinName_+"_pdf").c_str(),(jtBinName_+"_pdf").c_str(),TemplateList);

}


void JetTagBin::setupPE( double Lum )
{
  cout << "generating pseudoexperiment" << endl;

  bool first = true;
  TH1F * temp = 0;  // Will hold the sum of all the experiments
  for ( vector<Template *>::iterator tBegin = jtTemplates_.begin(),
	  tEnd = jtTemplates_.end(), it = tBegin;
	it != tEnd; ++it ) {
    Template & t = **it;
    t.setupPE( Lum * kFactors_[it - tBegin] );
    if ( first ) {
      temp = (TH1F*)( t.expHist()->Clone() ); 
      first = false;
    } else {
      temp->Add( t.expHist() );
    }

  }

  cout << "Generated pseudoexperiment with sum of xs * LUM * eff = " << temp->Integral() << " events" << endl;

  // Vary the bin contents
  for ( int ibin = 1; ibin <= temp->GetNbinsX(); ++ibin ) {
    temp->SetBinContent( ibin, gRandom->Poisson( temp->GetBinContent(ibin) ) );
  }

  jtData_ = new RooDataHist(("PEData_"+jtBinName_).c_str(),("PEData_"+jtBinName_).c_str(),*jtFitVar_,Import(*temp));
}


void JetTagBin::inputData( TFile * file ) 
{
  TH1F * tempDataHist = (TH1F*)file->Get(("Data_"+jtBinName_).c_str());
  cout << "Loaded Data_" << jtBinName_ << " from the file." << endl;
  jtDataHist_ = (TH1F*) tempDataHist->Clone();
  jtData_ = new RooDataHist(("Data_"+jtBinName_).c_str(),("Data_"+jtBinName_).c_str(),*jtFitVar_,Import(*jtDataHist_));
  
}


void JetTagBin::makeNLLVar()
{
  cout << "creating nllVar" << endl;
  jtNll_ = new RooNLLVar((jtBinName_+"_nll").c_str(), (jtBinName_+"_nll").c_str(), *jtPdf_, *jtData_);
}

void JetTagBin::plotOn( RooPlot * frame )
{
  cout << "Plotting On" << endl;
  jtData_->plotOn(frame);
  jtPdf_->plotOn(frame);
}

JetTagBin::~JetTagBin() {
}



class SHyFT {
public:

  SHyFT( string const & fileName, double lum );
  ~SHyFT() { file_->Close(); }
  
  void generatePEs( double Lum ); 
  void makeNLLVars();
  void fit(bool verbose);
  void print();
  void plot( double lum );
  RooFitResult * fitResult() { return fitResult_; }

  void setKFactors( vector<double> const & inputKFactors ) {
    for ( vector<JetTagBin*>::iterator bBegin = bins_.begin(),
	    bEnd = bins_.end(), ib = bBegin;
	  ib != bEnd; ++ib ) {
      (*ib)->setKFactors( inputKFactors );
    }
  }
  
protected:
  vector< JetTagBin * > bins_;
  vector< RooNLLVar * > nlls_;
  //map<string, vector< RooRealVar * > > scaleFactors_;
  scaleFact_vect scaleFactors_;
  vector<string> samples_;
  TFile * file_;
  RooRealVar ttbar_xsec_;
  RooRealVar WJets_xsec_;
  RooFitResult* fitResult_;
  RooRealVar lum_;
  RooRealVar kFactor1;
  RooRealVar kFactor2;
  RooRealVar genXsec_ttbar;
  RooRealVar genXsec_wjets;
  RooRealVar genNevt_ttbar;
  RooRealVar genNevt_wjets;
};


SHyFT::SHyFT( string const & fileName, double lum ) :
  file_( new TFile(fileName.c_str()) ),
  ttbar_xsec_("ttbar_hT_xsec","ttbar_hT_xsec", 1., .0001, 100. ),
  WJets_xsec_("WJets_hT_xsec","WJets_hT_xsec", 1., .0001, 100. ),
  lum_("luminosity","luminosity",lum),
  genXsec_ttbar("genXsec_ttbar","genXsec_ttbar",1.0),
  genXsec_wjets("genXsec_wjets","genXsec_wjets",1.0),
  genNevt_ttbar("genNevt_ttbar","genNevt_ttbar",221131.),
  genNevt_wjets("genNevt_wjets","genNevt_wjets",1204434.)
  
{

  //  RooRealVar Lum("luminosity","luminosity", lum );
  //  RooRealVar kFactor1("kFactor1","kFactor1",1.0);
  //RooRealVar kFactor2("kFactor2","kFactor2",1.0);

  vector<RooRealVar *> ttbarSF;
  vector<RooRealVar *> wjetsSF;

  ttbarSF.push_back(&ttbar_xsec_);
  ttbarSF.push_back(&lum_);
  ttbarSF.push_back(&genXsec_ttbar);
  ttbarSF.push_back(&genNevt_ttbar);
  wjetsSF.push_back(&WJets_xsec_);
  wjetsSF.push_back(&lum_);
  wjetsSF.push_back(&genXsec_wjets);
  wjetsSF.push_back(&genNevt_wjets);

  scaleFactors_["ttbar"]=ttbarSF;
  scaleFactors_["WJets"]=wjetsSF;
  
  //  scaleFactors_["ttbar"]=&ttbar_xsec_;
  //scaleFactors_["WJets"]=&WJets_xsec_;

  samples_.push_back("ttbar");//_hT_");
  samples_.push_back("WJets");//_hT_");

  stringstream tmpString;
  
  for(int n_jets = 1; n_jets <=5; ++n_jets) { //will run only once
    //    for(int n_tags = 1; n_tags < 2; ++ n_tags) { // will run only once for now, but must run later until 3
    //      if(n_tags > n_jets) continue;
      tmpString.str("");
      // eventually we will have a loop over all jets with 0T as a fixed string for ht and mt
      // then we loop over jets and tags  like this for secvtxmass
      tmpString << "_hT_" << n_jets << "j"; //_" << n_tags << "t";
      bins_.push_back(new JetTagBin(*file_, samples_, tmpString.str(), scaleFactors_ ) );
      //}
  }

}

void SHyFT::print()
{
  cout << "Printing" << endl;
  for(unsigned int i=0;i<bins_.size();++i) {
    bins_[i]->nll()->Print();
  }
}

void SHyFT::generatePEs(double Lum)
{
  cout << "Generating Pseudoexperiments" << endl;
  for(unsigned int i=0;i<bins_.size();++i) {
    bins_[i]->setupPE( Lum );
  }
}

void SHyFT::makeNLLVars()
{
  cout << "Making NLL variables" << endl;
  for(unsigned int i=0;i<bins_.size();++i) {
    bins_[i]->makeNLLVar();
  }
}

void SHyFT::fit(bool verbose)
{
  cout << "Fitting" << endl;
  RooAddition nllsum("nllsum","nllsum",RooArgSet(*bins_[0]->nll(),
						 *bins_[1]->nll(),
						 *bins_[2]->nll(),
						 *bins_[3]->nll(),
						 *bins_[4]->nll()
						 ) );
  RooMinuit m(nllsum);
  if(verbose){
    std::cout << "VERBOSE" << std::endl;
    m.setVerbose(kTRUE);
  }
  else {
    m.setVerbose(kFALSE);
    m.setPrintLevel(-1);
  }
  m.migrad();
  fitResult_ = m.save() ;
  // Print the fit result snapshot
  if(verbose) fitResult_->Print("v") ;
}

void SHyFT::plot(double lum)
{
  //plotting stuff and examination below here
  cout << "Plotting" << endl;
  for (  vector< JetTagBin * >::iterator ibin = 
	   bins_.begin(),
	   binsBegin = bins_.begin(), binsEnd = bins_.end();
	 ibin != binsEnd; ++ibin ) {

    cout << "Plotting bin " << ibin - binsBegin+1 << endl;
    JetTagBin & bin = **ibin;
    TCanvas * c1 = new TCanvas(("c"+bin.jtBinName()).c_str(), "Combined Fit");
    RooPlot *frame = bin.jtFitVar()->frame();

    double scale0 = bin.jtTemplates().at(0)->hnorm()*(bin.kFactors().at(0))*lum;
    double scale1 = bin.jtTemplates().at(1)->hnorm()*(bin.kFactors().at(1))*lum;
    bin.jtTemplates().at(0)->epdf()->plotOn(frame, LineColor(3),Normalization(scale0));
    bin.jtTemplates().at(1)->epdf()->plotOn(frame, LineColor(2),Normalization(scale1));
    bin.plotOn( frame );
    //jtPdf_->plotOn(frame,Components("ttbar_hT_1j_pdf"),LineColor(3));
    //jtPdf_->plotOn(frame,Components("WJets_hT_1j_pdf"),LineColor(2));
    frame->Draw();
    c1->SaveAs(("fitter"+bin.jtBinName()+".png").c_str());
    delete c1;
  }
  //jtFitVar_->Print("t");
  //jtPdf_->Print("v");
  //   r->Print("v");

  //   delete r;
  
  //r->Print();
}

void Fitter(string fileName, int maxPEs)
{
  vector<double> kFactors;
  //  kFactors.push_back( 3.0 );
  kFactors.push_back( 3.0 );
  kFactors.push_back( 1.0 );
  double lum=10.0; // for now this is the same parameter input to generatePEs
  vector<RooFitResult *> results;
  //  TH1F * pull_ttbar = new TH1F("pull_ttbar", "pull_ttbar", 100, -0.3, 0.3);
  TH1F * pull_ratio = new TH1F("pull_ratio", "pull_ratio", 50, -1.1, 1.1);
  bool verbose = false;
  if(maxPEs<=10) verbose = true;

  for(int numPEs = 0; numPEs < maxPEs; ++numPEs) {
    SHyFT shyft(fileName, lum);
    shyft.setKFactors( kFactors );
    shyft.generatePEs(lum);
    shyft.makeNLLVars();
    if(verbose) shyft.print();
    shyft.fit(verbose);
    results.push_back(shyft.fitResult());
    cout << "NEVENT IS " << numPEs << endl;
  }
  for(unsigned int i=0; i<results.size(); ++i) {
    double ttbar_xsec = ((RooRealVar * )(*results.at(i)).floatParsFinal().find("ttbar_hT_xsec"))->getVal();
    double wjets_xsec = ((RooRealVar * )(*results.at(i)).floatParsFinal().find("WJets_hT_xsec"))->getVal();
    if(verbose) cout << "ttbar_xsec " << ttbar_xsec << " wjets_xsec " << wjets_xsec << endl;
    pull_ratio->Fill((ttbar_xsec/wjets_xsec)-3.0);
      
    //    (*results.at(i)).floatParsFinal().Print("s");
    //(*results.at(i)).Print("v");
    //    (*results.at(i)).printMultiline(cout,false,"");
    //(*results.at(i)).printArgs(cout);
  }
  //shyft.plot( lum );
  //  TCanvas * c1 = new TCanvas("ttbar_pulls", "ttbar_pulls");
  TCanvas * c1 = new TCanvas("ratio_pulls", "ratio_pulls");
  pull_ratio->Draw();
  c1->SaveAs("ratio_test.png");
  delete c1;
}


//petar wants plots of nll vs parameters
