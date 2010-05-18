#ifndef Analysis_BoostedTopAnalysis_interface_HadronicAnalysis_h
#define Analysis_BoostedTopAnalysis_interface_HadronicAnalysis_h

#include "Analysis/BoostedTopAnalysis/interface/HadronicSelection.h"
#include "PhysicsTools/FWLite/interface/TFileService.h"
#include "DataFormats/FWLite/interface/Event.h"
#include "Math/GenVector/PxPyPzM4D.h"
#include "DataFormats/FWLite/interface/Handle.h"


#include <iostream>
#include <iomanip>
#include <cmath>      //necessary for absolute function fabs()
#include <boost/shared_ptr.hpp>
#include <boost/lexical_cast.hpp>


//Root includes
#include "TROOT.h"
#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TSystem.h"

typedef std::vector<reco::ShallowClonePtrCandidate> ShallowCloneCollection;


class HadronicAnalysis {

  public:
    HadronicAnalysis(const edm::ParameterSet& iConfig, TFileDirectory& iDir);
    virtual ~HadronicAnalysis() {}
    virtual void analyze(const edm::EventBase& iEvent);
    virtual void beginJob() {}
    virtual void endJob() {
      hadronicSelection_.print(std::cout);
    }

  private:
    HadronicSelection   hadronicSelection_;
    TFileDirectory& theDir;
    // 'registry' for the histograms                                                                                                                                                                    
    std::map<std::string, TH1F*> histograms1d;
    std::map<std::string, TH2F*> histograms2d;

};

#endif
