#ifndef Analysis_SHyFT_interface_JetStudies2011_h
#define Analysis_SHyFT_interface_JetStudies2011_h

#include "PhysicsTools/UtilAlgos/interface/BasicAnalyzer.h"
#include "FWCore/ParameterSet/interface/ProcessDesc.h"
#include "PhysicsTools/FWLite/interface/TFileService.h"
#include "DataFormats/FWLite/interface/Event.h"
#include "Math/GenVector/PxPyPzM4D.h"
#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/FWLite/interface/Record.h"
/* #include "PhysicsTools/Utilities/interface/LumiWeighting.h" */
/* #include "DataFormats/FWLite/interface/EventSetup.h" */
/* #include "DataFormats/FWLite/interface/ESHandle.h" */
/* #include "CondFormats/PhysicsToolsObjects/interface/BinningPointByMap.h" */
/* #include "RecoBTag/PerformanceDB/interface/BtagPerformance.h" */


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
#include "TH3.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TSystem.h"

class JetStudies2011 : public edm::BasicAnalyzer {

  public:
    JetStudies2011(const edm::ParameterSet& iConfig, TFileDirectory& iDir);
    virtual ~JetStudies2011() {     
    }
    virtual void analyze(const edm::EventBase& iEvent);
    virtual void beginJob() {}
    virtual void endJob() {}

  private:


    TFileDirectory theDir;
    std::vector<TFileDirectory> dirs_;

    // the following parameters need to come from the config
    edm::InputTag   jetSrc_;
    edm::InputTag   rhoSrc_;
    edm::InputTag   pvSrc_;
    edm::InputTag   trigSrc_;
    edm::InputTag   genJetsSrc_;
    bool            useCA8GenJets_;
    bool            weightPV_;
    std::vector<std::string> trigs_;
    bool            useBTags_;
    bool            orderByMass_;

    /* boost::shared_ptr<edm::LumiWeighting> lumiWeighting_; */
};


#endif
