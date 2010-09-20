#ifndef Analysis_BoostedTopAnalysis_interface_WPlusBJetAnalysis_h
#define Analysis_BoostedTopAnalysis_interface_WPlusBJetAnalysis_h

#include "Analysis/BoostedTopAnalysis/interface/WPlusBJetEventSelector.h"
#include "PhysicsTools/FWLite/interface/TFileService.h"
#include "Math/GenVector/PxPyPzM4D.h"

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
    virtual ~WPlusBJetAnalysis() { }
    virtual void beginJob() {}
    virtual void analyze( const edm::EventBase& iEvent ) ;
    virtual void endJob() {
      twPlusBJetSelection_.print( std::cout );
      owPlusBJetSelection_.print( std::cout );
    }

  private:
    TFileDirectory& theDir;
    edm::InputTag     jetSrc_;
    WPlusBJetEventSelector    twPlusBJetSelection_; //towards direction selector
    WPlusBJetEventSelector    owPlusBJetSelection_; //opposite direction selector
    std::map<std::string, TH1F*> histograms1d;
    std::map<std::string, TH2F*> histograms2d;

};


#endif
