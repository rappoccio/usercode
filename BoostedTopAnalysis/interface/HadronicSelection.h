#ifndef Analysis_BoostedTopAnalysis_interface_HadronicSelection_h_h
#define Analysis_BoostedTopAnalysis_interface_HadronicSelection_h_h

#include "PhysicsTools/Utilities/interface/EventSelector.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "PhysicsTools/PatUtils/interface/JetIDSelectionFunctor.h"
#include "Analysis/BoostedTopAnalysis/interface/CATopTagFunctor.h"

class HadronicSelection : public EventSelector {
 public:
  HadronicSelection(
   edm::InputTag const & jetTag,
   edm::InputTag const & trigTag,
   boost::shared_ptr<JetIDSelectionFunctor> & jetIdTight,
   boost::shared_ptr<CATopTagFunctor>       & caTopTagFunctor,
   int minJets,
   int minTags,
   double jetPtMin      , double jetEtaMax,
   double topMassMin    , double topMassMax,
   double minMass       ,
   double wMassMin      , double wMassMax
   );

  ~HadronicSelection() {}
  
  virtual bool operator()( edm::EventBase const & t, std::strbitset & ret);

  std::vector<pat::Jet>      const & selectedJets     () const { return selectedJets_;     } 
  std::vector<pat::Jet>      const & taggedJets       () const { return taggedJets_;       } 
 
 protected: 
  edm::InputTag               jetTag_;
  edm::InputTag               trigTag_;

  std::vector<pat::Jet>       selectedJets_;
  std::vector<pat::Jet>       taggedJets_;

  boost::shared_ptr<JetIDSelectionFunctor>                jetIdTight_;
  boost::shared_ptr<CATopTagFunctor>                      caTopTagFunctor_;

  int minJets_;
  int minTags_;

  double jetPtMin_ ;
  double jetEtaMax_;
  
  double topMassMin_;
  double topMassMax_;
  double minMass_;
  double wMassMin_;
  double wMassMax_;

  
};


#endif
