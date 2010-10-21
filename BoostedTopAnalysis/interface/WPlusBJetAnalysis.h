#ifndef Analysis_BoostedTopAnalysis_interface_WPlusBJetAnalysis_h
#define Analysis_BoostedTopAnalysis_interface_WPlusBJetAnalysis_h

#include "Analysis/BoostedTopAnalysis/interface/WPlusBJetType22Selection.h"
#include "Analysis/BoostedTopAnalysis/interface/WPlusBJetType23Selection.h"
#include "Analysis/BoostedTopAnalysis/interface/WPlusBJetType33Selection.h"
#include "PhysicsTools/FWLite/interface/TFileService.h"
#include "Math/GenVector/PxPyPzM4D.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/RandomNumberGenerator.h"
#include "CLHEP/Random/RandFlat.h"
#include "CLHEP/Random/RandPoissonQ.h"
#include "FWCore/Utilities/interface/Exception.h"


#include <iostream>
#include <iomanip>
#include <cmath>      //necessary for absolute function fabs()
#include <boost/shared_ptr.hpp>

//Root includes
#include "TROOT.h"
#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TSystem.h"


class WPlusBJetAnalysis{

  public:
    WPlusBJetAnalysis( const edm::ParameterSet & iConfig, TFileDirectory & iDir );
    virtual ~WPlusBJetAnalysis() { } //delete flatDistribution_; 
    virtual void beginJob() {}
    virtual void analyze( const edm::EventBase& iEvent ) ;
    virtual void endJob() {
      cout<<"Type 2 + Type 2 selection: "<<endl;
      wPlusBJetType22Selection_.print(cout);
      cout<<"Type 2 + Type 3 selection: "<<endl;
      wPlusBJetType23Selection_.print(cout);
      cout<<"Type 3 + Type 3 selection: "<<endl;
      wPlusBJetType33Selection_.print(cout);
    }

  private:
    TFileDirectory& theDir;
    std::map<std::string, TH1F*> histograms1d;
    std::map<std::string, TH2F*> histograms2d;
    WPlusBJetType22Selection  wPlusBJetType22Selection_;
    WPlusBJetType23Selection  wPlusBJetType23Selection_;
    WPlusBJetType33Selection  wPlusBJetType33Selection_;
    double wMassMin_, wMassMax_;
    double topMassMin_, topMassMax_;
    bool   runOnData_;
    std::string   bTagAlgo_;
    double        bTagOP_;
    CLHEP::RandFlat *flatDistribution_;

};


#endif
