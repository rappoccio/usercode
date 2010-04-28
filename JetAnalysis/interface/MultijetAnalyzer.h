#ifndef Analysis_JetAnalysis_interface_MultijetStudies_h
#define Analysis_JetAnalysis_interface_MultijetStudies_h

#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TSystem.h"
#include "TLorentzVector.h"


#include "Analysis/JetAnalysis/interface/DijetSelector.h"

#include "PhysicsTools/FWLite/interface/TFileService.h"
#include "DataFormats/FWLite/interface/ChainEvent.h"
#include "FWCore/PythonParameterSet/interface/PythonProcessDesc.h"
#include "FWCore/ParameterSet/interface/ProcessDesc.h"


class MultijetAnalyzer {

  public:
    MultijetAnalyzer(const edm::ParameterSet& iConfig, TFileDirectory& iDir);
    virtual ~MultijetAnalyzer() {}
    virtual void analyze(const edm::EventBase& iEvent);
    virtual void finalize();

  private:


    // Selectors : The DijetSelector can be used as a
    // multijet selector by removing the dphi requirement
    DijetSelector caloSelector;
    DijetSelector pfSelector;

    // Directory for histograms
    TFileDirectory& theDir;

    bool doTracks;
    bool useMC;

    // Histograms
    std::map<std::string, TH1*> hists;
};


#endif
