#ifndef EDSHyFTSelector_h
#define EDSHyFTSelector_h


#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "PhysicsTools/UtilAlgos/interface/EDFilterWrapper.h"
#include "Analysis/SHyFT/interface/SHyFTSelector.h"

typedef reco::Candidate::PolarLorentzVector LorentzV;
typedef std::vector< LorentzV > p4_vector;

class EDSHyFTSelector : public edm::FilterWrapper<SHyFTSelector> {
 public:
 EDSHyFTSelector( const edm::ParameterSet & params ) :
  edm::FilterWrapper<SHyFTSelector>( params.getParameter<edm::ParameterSet>("shyftSelection") ),
  useData_(params.getParameter<bool>("useData")), 
  matchByHand_(params.getParameter<bool>("matchByHand")), 
  name_( params.getParameter<std::string>("@module_label") )
    {
      produces<  LorentzV > ("top1");
      produces<  LorentzV > ("top2");
      produces< std::vector<pat::Jet> >      ("jets");
      produces< std::vector<pat::MET> >      ("MET");
      produces< std::vector<pat::Muon> >     ("muons");
      produces< std::vector<pat::Electron> > ("electrons");
    };
     
  virtual ~EDSHyFTSelector() {}
 
  virtual bool filter( edm::Event & event, const edm::EventSetup& eventSetup);
   
  /// Pass the event to the filter. NOTE! We can't use the eventSetup in FWLite so ignore it.

  virtual void endJob() {
    std::cout << "----------------------------------------------------------------------------------------" << std::endl;
    std::cout << "So long, and thanks for all the fish..." << std::endl;
    std::cout << "                    -- " << name_ << std::endl;
    std::cout << "----------------------------------------------------------------------------------------" << std::endl;
    filter_->print(std::cout);
  }

 protected:
  bool useData_;
  bool matchByHand_;
  std::string name_;
};

#endif
