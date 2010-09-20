#ifndef Analysis_SHyFT_interface_SHyFT_h
#define Analysis_SHyFT_interface_SHyFT_h

#include "PhysicsTools/SelectorUtils/interface/WPlusJetsEventSelector.h"
#include "FWCore/ParameterSet/interface/ProcessDesc.h"
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

enum
{
   kNormalMode,
   kVqqMode,
   kLFMode,
   kWcMode
};


// TODO: bring the isolation plots back to life 

typedef std::vector<reco::ShallowClonePtrCandidate> ShallowCloneCollection;


class SHyFT {

  public:
    SHyFT(const edm::ParameterSet& iConfig, TFileDirectory& iDir);
    virtual ~SHyFT() {}
    virtual void analyze(const edm::EventBase& iEvent);
    virtual void beginJob() {}
    virtual void endJob();

  private:
    bool analyze_electrons(const std::vector<reco::ShallowClonePtrCandidate>& electrons);
    bool analyze_muons(const std::vector<reco::ShallowClonePtrCandidate>& muons);    
    bool analyze_jets(const std::vector<reco::ShallowClonePtrCandidate>& jets);
    bool analyze_met( const reco::ShallowClonePtrCandidate & met );
    bool calcSampleName (const edm::EventBase& iEvent, std::string &sampleName);

    WPlusJetsEventSelector wPlusJets;
    TFileDirectory& theDir;
    // 'registry' for the histograms                                                                                                                                                                    
    std::map<std::string, TH1F*> histograms;
    // the following parameters need to come from the config
    bool muPlusJets_;
    bool ePlusJets_;
    bool useHFcat_;
    int nJetsCut_ ;
    int mode;
    std::string sampleNameInput;
    // used to be a global, what a shit!
    int HFcat_;
    std::string secvtxname;
    bool doMC_;
};


#endif
