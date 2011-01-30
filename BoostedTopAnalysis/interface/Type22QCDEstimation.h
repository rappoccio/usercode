#ifndef Analysis_BoostedTopAnalysis_interface_Type22QCDEstimation_h
#define Analysis_BoostedTopAnalysis_interface_Type22QCDEstimation_h

#include "Analysis/BoostedTopAnalysis/interface/Type22Selection_v1.h"
#include "PhysicsTools/FWLite/interface/TFileService.h"

#include "TH1F.h"

class Type22QCDEstimation {
  public :
    Type22QCDEstimation( const edm::ParameterSet & iConfig, TFileDirectory & iDir );
    virtual ~Type22QCDEstimation() { } //delete flatDistribution_; 
    virtual void beginJob() {}
    virtual void analyze( const edm::EventBase& iEvent ) ;
    virtual void endJob() {  type22Selection_v1_.print(cout);  }

  private :
    TFileDirectory& theDir;
    Type22Selection_v1   type22Selection_v1_;
    double              bTagOP_;
    string              bTagAlgo_;
    BoostedTopWTagFunctor   *        wJetSelector_;
    std::map<std::string, TH1F*>     histograms1d;

};


#endif
