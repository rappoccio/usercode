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

using namespace RooFit ;
using namespace std;

double lum=0.10;

class Template {
public:
  Template(TH1F histo, string name, RooRealVar& dataVar, RooRealVar& scaleFactor);
  //  virtual ~Template() {}
  ~Template();

  RooDataHist * rdh() { return rdh_;  }
  RooHistPdf  * rhp() { return rhp_;  }
  // RooExtendPdf  * rep() { return rep_;  }
  RooRealVar * norm() { return norm_; }
  RooExtendPdf * epdf() { return rep_; }
  double hnorm() { return hnorm_; }
  TH1F hist() { return hist_; }
                           
private:
  TH1F   hist_;
  string name_;
  double hnorm_;
  RooRealVar    * norm_;
  RooDataHist * rdh_;
  RooHistPdf  * rhp_;
    //  RooFormulaVar * form_;
  RooRealVar  binningVar_;
  RooExtendPdf * rep_;
};

Template::Template(TH1F hist, string name, RooRealVar& binningVar, RooRealVar& scaleFactor):
  hist_(hist),name_(name),binningVar_(binningVar) {//form_(formula),name_(name) {
  hnorm_   = hist_.Integral();
  norm_    = new RooRealVar ((name_+"_norm").c_str(), (name_+"_norm").c_str(),hnorm_);//,-1,100000);
  //  binningVar_ = new RooRealVar ((name_+"_binningVar").c_str(), (name_+"_binningVar").c_str(),&binningVar,-1,100000);
  //  binningVar_ = new RooRealVar(binningVar);
  rdh_     = new RooDataHist(name_.c_str(),name_.c_str(),binningVar_, &hist_);
  rhp_   = new RooHistPdf ((name_+"_pdf").c_str(),(name_+"_pdf").c_str(), binningVar_, *rdh_);
  //  rep_   = new RooExtendPdf((name_+"_epdf").c_str(), (name_+"_epdf").c_str(), *rhp_, *norm_);//binningVar_);
  RooFormulaVar * form_ = new RooFormulaVar((name_+"_form").c_str(), (name_+"_form").c_str(),"@0*@1",RooArgSet(scaleFactor, norm_));
  rep_   = new RooExtendPdf((name_+"_epdf").c_str(), (name_+"_epdf").c_str(), *rhp_, *form_);//binningVar_);
  //norm needs to now not have a range and we have norm_scale
}

Template::~Template() {
  delete norm_;
  delete rdh_;
  delete rhp_;
  // delete form_;
  delete rep_;
    //  delete binningVar_;
  
}

class JetTagBin {
public:
  JetTagBin(TFile & file, vector<string> const & samples, string jtBinName, std::map<std::string, RooRealVar *> scaleFactors);//, ScaleFactors SF);
  //  virtual ~JetTagBin() {}
  ~JetTagBin();
  vector<Template*> & jtTemplates() { return jtTemplates_; }

  //this needs to be instantiated
  //  RooNLLVar getNllVar(RooDataHist) {return nll_; } 


private:
  vector<Template*> jtTemplates_;
  RooRealVar * jtFitVar_;
  //  RooNLLVar nll_;
  RooDataHist * jtData_; 
  string jtBinName_;
  RooAbsPdf *jtPdf_;

};

JetTagBin::JetTagBin(TFile & file, vector<string> const & samples, string jtBinName, std::map<std::string, RooRealVar *> scaleFactors):
  jtBinName_(jtBinName)
{
  
  RooRealVar ttbar("ttbar_frac", "ttbar_frac",  0, 100000);
  RooRealVar wjets("wjets_frac", "wjets_frac",  0, 100000);
  
  jtFitVar_= new RooRealVar(jtBinName.c_str(),jtBinName.c_str(),80,50,300);
  //TODO: create a map from scale factor to sample name!!!!!!
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
  RooArgList NormList;
  cout << "making lists" << endl;
  for(unsigned int i=0;i<jtTemplates_.size();++i) {
    TemplateList.add(*(jtTemplates_[i]->epdf()));
    //TemplateList.add(*(jtTemplates_[i]->rhp()));
    //NormList.add(*(jtTemplates_[i]->norm()));
  }
  cout << "making combined pdf" << endl;
  //  RooAddPdf model("model","model",RooArgList(*ttbar.rhp(),*wjets.rhp()),RooArgList(*ttbar.norm(),*wjets.norm()));
  //jtPdf_ = new RooAddPdf((jtBinName+"_pdf").c_str(),(jtBinName+"_pdf").c_str(),TemplateList,NormList);
  jtPdf_ = new RooAddPdf((jtBinName+"_pdf").c_str(),(jtBinName+"_pdf").c_str(),TemplateList);

  RooDataSet * data = jtPdf_->generate(*jtFitVar_,1000);
  /*attempt by petar....keeping for use of nll
    #define MULTI_DIM 0
    #if MULTI_DIM
    RooNLLVar nll("nll","nll", data, *jtPdf_ );
    RooMinimizer m("m","m", 
    #else
    jtPdf_->fitTo(*data);
    #endif */
  
  cout << "about to fit" << endl;
  //this has memory issues here, but I guess that's okay because we don't want to fit here
  RooFitResult * r = jtPdf_->fitTo(*data,Extended(kTRUE),Save(kTRUE),Verbose(kTRUE));
  //jtPdf_->fitTo(*data);
  cout << "finished fit" << endl;
  
  //plotting stuff and examination below here
  TCanvas * c1 = new TCanvas("c1", "Combined Fit");
  RooPlot *frame = jtFitVar_->frame();
  data->plotOn(frame);
  jtPdf_->plotOn(frame);
  //jtPdf_->plotOn(frame,Components("ttbar_hT_1j_pdf"),LineColor(3));
  //jtPdf_->plotOn(frame,Components("WJets_hT_1j_pdf"),LineColor(2));
  frame->Draw();
  //jtFitVar_->Print("t");
  //jtPdf_->Print("v");
  r->Print("v");
  c1->SaveAs("new_test.png");
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
  RooRealVar ttbar_xsec("ttbar_hT_xsec","ttbar_hT_xsec", 1., -100., 100. );
  RooRealVar WJets_xsec("WJets_hT_xsec","WJets_hT_xsec", 1., -100., 100. );
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
  vector<string> samples;
  samples.push_back("ttbar");//_hT_");
  samples.push_back("WJets");//_hT_");

  stringstream tmpString;
  
  for(int n_jets = 1; n_jets <2; ++n_jets) { //will run only once
    for(int n_tags = 1; n_tags < 2; ++ n_tags) { // will run only once for now, but must run later until 3
      if(n_tags > n_jets) continue;
      tmpString.str("");
      // eventually we will have a loop over all jets with 0T as a fixed string for ht and mt
      // then we loop over jets and tags  like this for secvtxmass
      tmpString << "_hT_" << n_jets << "j"; //_" << n_tags << "t";
      JetTagBin * jetTagBin = new JetTagBin(file, samples, tmpString.str(), scaleFactors );
      bins_.push_back( jetTagBin );
    }
  }
  file.Close();


  for(unsigned int i=0; i<bins_.size(); ++i) {
    delete bins_[i]; // is this the proper way to delete this?
  }
}

