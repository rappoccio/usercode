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
#include <iostream>
#include <sstream>
#include "RooAbsData.h"
#include "RooAddition.h"
#include "RooMinuit.h"

using namespace RooFit ;
using namespace std;

double lum=0.10;

class Template {
public:
  Template(TH1F histo, string name, RooRealVar& dataVar, RooRealVar& scaleFactor);
  //  virtual ~Template() {}
  ~Template();

  RooRealVar   *   norm() { return norm_; }
  RooDataHist  *  hdata() { return rdh_;  }
  RooHistPdf   *    pdf() { return rhp_;  }
  RooExtendPdf *   epdf() { return rep_;  }
  double hnorm() { return hnorm_; }
  TH1F    hist() { return hist_;  }
                           
private:
  TH1F   hist_;
  string name_;
  double hnorm_;
  RooRealVar   * norm_;
  RooDataHist  * rdh_;
  RooHistPdf   * rhp_;
  RooExtendPdf * rep_;
  //  RooFormulaVar * form_;
  RooRealVar  binningVar_;
};

Template::Template(TH1F hist, string name, RooRealVar& binningVar, RooRealVar& scaleFactor):
  hist_(hist),name_(name),binningVar_(binningVar) {
  hnorm_   = hist_.Integral();
  cout << "Normaliztion of " << name_.c_str() << " is " << hnorm_ << endl;
  norm_    = new RooRealVar ((name_+"_norm").c_str(), (name_+"_norm").c_str(),hnorm_);//,-1,100000);
  rdh_     = new RooDataHist(name_.c_str(),name_.c_str(),binningVar_, &hist_);
  rhp_   = new RooHistPdf ((name_+"_pdf").c_str(),(name_+"_pdf").c_str(), binningVar_, *rdh_);
  RooFormulaVar * form_ = new RooFormulaVar((name_+"_form").c_str(), (name_+"_form").c_str(),"@0*@1",RooArgSet(scaleFactor, norm_));
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

class JetTagBin {
public:
  JetTagBin(TFile & file, vector<string> const & samples, string jtBinName, std::map<std::string, RooRealVar *> scaleFactors);
  ~JetTagBin();
  vector<Template*> & jtTemplates() { return jtTemplates_; }
  
  //this needs to be instantiated
  RooNLLVar * nll()  { return jtNll_; } 


private:
  string jtBinName_;
  TH1F * jtDataHist_;
  RooRealVar * jtFitVar_;
  RooAbsData * jtData_; 
  RooAbsPdf  * jtPdf_;
  RooNLLVar  * jtNll_;
  vector<Template*> jtTemplates_;
};

JetTagBin::JetTagBin(TFile & file, vector<string> const & samples, string jtBinName, std::map<std::string, RooRealVar *> scaleFactors):
  jtBinName_(jtBinName)
{
  // I don't know if I should provide the guess here --also for different sized bins, I think we may have to dynamically provide range
  // GetBinLowEdge and GetBinWidth should work if we move this below the th1f access
  jtFitVar_= new RooRealVar(jtBinName.c_str(), jtBinName.c_str(), 50, 500);
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

    Template * temp = new Template(*tempHisto2, name, *jtFitVar_, *scaleFactors[samples[i]]);
    jtTemplates_.push_back( temp );
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
  //jtPdf_ = new RooAddPdf((jtBinName+"_pdf").c_str(),(jtBinName+"_pdf").c_str(),TemplateList,NormList);
  jtPdf_ = new RooAddPdf((jtBinName+"_pdf").c_str(),(jtBinName+"_pdf").c_str(),TemplateList);

  TH1F * tempDataHist = (TH1F*)file.Get(("Data_"+jtBinName).c_str());
  
  //  jtDataHist_ = (TH1F*)file.Get(("Data_"+jtBinName).c_str());
  
  if(tempDataHist==0) {
    int nPD = 1000;
    cout << "Data_" << jtBinName << " not located in the file, generating pseudo data with " << nPD << " entries." << endl;
    jtData_ = jtPdf_->generateBinned(*jtFitVar_,nPD);
  }
  else {
    // this compiles and "runs", but hasn't actually been tested yet. I need to make a histogram in the file called Data_hT_1j, etc and try
    cout << "Loaded Data_" << jtBinName << " from the file." << endl;
    jtDataHist_ = (TH1F*) tempDataHist->Clone();
    jtData_ = new RooDataHist(("Data_"+jtBinName).c_str(),("Data_"+jtBinName).c_str(),*jtFitVar_,Import(*jtDataHist_));
  }

  cout << "about to fit" << endl;
  //this has had memory issues here, but it's okay at the moment...could be a symptom of a problem elsewhere when it messes up
  RooFitResult * r = jtPdf_->fitTo(*jtData_,Extended(kTRUE),Save(kTRUE),Verbose(kFALSE));
  //jtPdf_->fitTo(*data);

  cout << "creating nllVar" << endl;
  jtNll_ = new RooNLLVar((jtBinName+"_nll").c_str(), (jtBinName+"_nll").c_str(), *jtPdf_, *jtData_);

  //plotting stuff and examination below here
  TCanvas * c1 = new TCanvas("c1", "Combined Fit");
  RooPlot *frame = jtFitVar_->frame();
  jtData_->plotOn(frame);
  jtPdf_->plotOn(frame);
  //jtPdf_->plotOn(frame,Components("ttbar_hT_1j_pdf"),LineColor(3));
  //jtPdf_->plotOn(frame,Components("WJets_hT_1j_pdf"),LineColor(2));
  frame->Draw();
  //jtFitVar_->Print("t");
  //jtPdf_->Print("v");
  r->Print("v");
  c1->SaveAs(("fitter"+jtBinName+".png").c_str());
  delete r;
  delete c1;
  delete frame;
  //r->Print();
}

JetTagBin::~JetTagBin() {
}


  

void Fitter(string fileName)
{

  // Create fit parameters - for now we use these as the scale factors
  RooRealVar ttbar_xsec("ttbar_hT_xsec","ttbar_hT_xsec", 1., .0001, 100. );
  RooRealVar WJets_xsec("WJets_hT_xsec","WJets_hT_xsec", 1., .0001, 100. );
  // ... etc. add more here

  //For now just work with a map to a RooRealVar without worrying about a vector
  std::map<std::string, RooRealVar *> scaleFactors;
  /*std::map<std::string, std::vector<RooRealVar *> > scaleFactors; //-- can I typedef this?
    std::vector<RooRealVar *> ttbarSF;
    std::vector<RooRealVar *> wjetsSF;
    
    ttbarSF.push_back(&ttbar_xsec);
    wjetsSF.push_back(&WJets_xsec);
  */
  scaleFactors["ttbar"]=&ttbar_xsec;
  scaleFactors["WJets"]=&WJets_xsec;
  
  //createTemplates(fileName);
  TFile file(fileName.c_str());

  vector<JetTagBin*> bins_;
  vector<RooNLLVar*> nlls_;
  vector<string> samples;
  samples.push_back("ttbar");//_hT_");
  samples.push_back("WJets");//_hT_");

  stringstream tmpString;
  
  for(int n_jets = 1; n_jets <3; ++n_jets) { //will run only once
    //    for(int n_tags = 1; n_tags < 2; ++ n_tags) { // will run only once for now, but must run later until 3
    //      if(n_tags > n_jets) continue;
      tmpString.str("");
      // eventually we will have a loop over all jets with 0T as a fixed string for ht and mt
      // then we loop over jets and tags  like this for secvtxmass
      tmpString << "_hT_" << n_jets << "j"; //_" << n_tags << "t";
      JetTagBin * jetTagBin = new JetTagBin(file, samples, tmpString.str(), scaleFactors );
      bins_.push_back( jetTagBin );
      //}
  }

  for(unsigned int i=0;i<bins_.size();++i) {
    bins_[i]->nll()->Print();
  }
  RooAddition nllsum("nllsum","nllsum",RooArgSet(*bins_[0]->nll(),*bins_[1]->nll()));
  RooMinuit m(nllsum);
  m.setVerbose(kTRUE);
  m.migrad();
  RooFitResult* r = m.save() ;
  // Print the fit result snapshot
  r->Print("v") ;
   
  file.Close();


  for(unsigned int i=0; i<bins_.size(); ++i) {
    delete bins_[i]; // is this the proper way to delete this?
  }
}
  
