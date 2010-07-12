#ifndef Analysis_BoostedTopAnalysis_interface_WPlusBJetEventSelector_h
#define Analysis_BoostedTopAnalysis_interface_WPlusBJetEventSelector_h

#include "PhysicsTools/SelectorUtils/interface/EventSelector.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/Candidate/interface/ShallowClonePtrCandidate.h"
#include "Analysis/BoostedTopAnalysis/interface/BoostedTopWTagFunctor.h"
#include "DataFormats/Candidate/interface/Candidate.h"

using namespace std;

class WPlusBJetEventSelector : public EventSelector {
  public:
    WPlusBJetEventSelector( edm::ParameterSet const & params );
    virtual bool operator()( edm::EventBase const & t, reco::Candidate::LorentzVector const & v, pat::strbitset & ret, bool towards);

    vector<reco::ShallowClonePtrCandidate> const & wJets ()  const { return wJets_; }
    vector<reco::ShallowClonePtrCandidate> const & bJets ()  const { return bJets_; }
    bool hasWJets ()  const { return wJets_.size() > 0 ; }
    bool hasBJets ()  const { return bJets_.size() > 0 ; }

  private:

    edm::InputTag               jetTag_;
    std::vector<reco::ShallowClonePtrCandidate>  wJets_;
    std::vector<reco::ShallowClonePtrCandidate>  bJets_;
    BoostedTopWTagFunctor  wJetSelector_;
    double  jetPtMin_;
    double  jetEtaMax_;
    double  dR_;  //hemisphere cone size
    string  bTagAlgo_;
    double  bTagOP_;

};

#endif
