#ifndef EDSHyFTPFSelector_h
#define EDSHyFTPFSelector_h


#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "PhysicsTools/UtilAlgos/interface/EDFilterWrapper.h"
#include "Analysis/SHyFT/interface/SHyFTPFSelector.h"

class EDSHyFTPFSelector : public edm::FilterWrapper<SHyFTPFSelector> {
 public:
 EDSHyFTPFSelector( const edm::ParameterSet & params ) :
  edm::FilterWrapper<SHyFTPFSelector>( params.getParameter<edm::ParameterSet>("shyftPFSelection") )
    {
      produces< std::vector<pat::Jet> >      ("jets");
      produces< std::vector<pat::MET> >      ("MET");
      produces< std::vector<pat::Muon> >     ("muons");
      produces< std::vector<pat::Electron> > ("electrons");
    };
    
  virtual ~EDSHyFTPFSelector() {}

  virtual bool filter( edm::Event & event, const edm::EventSetup& eventSetup);
   
  /// Pass the event to the filter. NOTE! We can't use the eventSetup in FWLite so ignore it.

  virtual void endJob() {
    filter_->print(std::cout);
  }
};

#endif
