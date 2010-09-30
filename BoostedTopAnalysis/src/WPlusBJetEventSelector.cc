#include "Analysis/BoostedTopAnalysis/interface/WPlusBJetEventSelector.h"
#include "DataFormats/Math/interface/deltaR.h"
#include <utility>


WPlusBJetEventSelector::WPlusBJetEventSelector ( edm::ParameterSet const & params ) :
  pfJetIdParams_         (params.getParameter<edm::ParameterSet>("pfJetIDParams") ),
  pfJetSel_              (new PFJetIDSelectionFunctor(pfJetIdParams_)),
  jetTag_	(params.getParameter<edm::InputTag>("jetSrc")  ),
  wJetSelector_ (params.getParameter<edm::ParameterSet>("BoostedTopWJetParameters") ),
  jetPtMin_	(params.getParameter<double>("jetPtMin") ),
  jetEtaMax_	(params.getParameter<double>("jetEtaMax") ),
  bTagAlgo_	(params.getParameter<string>("bTagAlgorithm") ),
  bTagOP_	(params.getParameter<double>("bTagOP")  )
{
  //make the bitset
  push_back("Inclusive");
  push_back("Jet Preselection"  );
  push_back(">= 1 WJet");
  push_back(">= 1 bJet");

  //turn on
  set("Inclusive");
  set("Jet Preselection" );
  set(">= 1 WJet");
  set(">= 1 bJet");

}

bool WPlusBJetEventSelector::operator() (edm::EventBase const & t, reco::Candidate::LorentzVector const & v, pat::strbitset & ret, bool towards)
{
  ret.set(false);
  wJets_.clear();
  bJets_.clear();
  pfJets_.clear();
  minDrPair_.clear();
  aJetFound_ = false;

  edm::Handle<vector<pat::Jet>  >   jetHandle;
  t.getByLabel( jetTag_, jetHandle );

  //Get the towards Lorentz vector
  reco::Candidate::LorentzVector vtowards = (towards) ? v : (-1)*v ;
  //Contain non-tagged jets inside the cone
  std::vector<edm::Ptr<pat::Jet> >  nonTags;

  pat::strbitset retPFJet = pfJetSel_->getBitTemplate();
  //Apply pfJets ID
  for( vector<pat::Jet>::const_iterator jetBegin=jetHandle->begin(), jetEnd=jetHandle->end(), ijet=jetBegin ;
    ijet!=jetEnd; ijet++ )
  {
    retPFJet.set(false);
    bool passJetID = (*pfJetSel_)( *ijet, retPFJet );
    if( passJetID )
      pfJets_.push_back( edm::Ptr<pat::Jet>(jetHandle, ijet-jetBegin )  );
  }

  //Search for W, b jets
  for( vector<edm::Ptr<pat::Jet> >::const_iterator jetBegin=pfJets_.begin(), jetEnd=pfJets_.end(), ijet=jetBegin ;
    ijet!=jetEnd; ijet++ )
  {
    pat::Jet const & jet = **ijet;
    //Only consider jets in the towards hemisphere
    double dPhi_ = fabs( reco::deltaPhi<double>( vtowards.phi(), jet.phi()  ) );
    if( dPhi_ < TMath::Pi()/2 ) {
      if( jet.pt() > jetPtMin_ && fabs( jet.eta() ) < jetEtaMax_ ) {
        pat::strbitset iret = wJetSelector_.getBitTemplate();
	if( wJetSelector_( jet, iret )  ) {
	  wJets_.push_back( *ijet  );
	} // end if wjet selector
	// not W jet, check b tag
	else {
	  if( jet.bDiscriminator( bTagAlgo_ ) > bTagOP_ )
	    bJets_.push_back( *ijet );
	  else  // put inside the nonTags container
	    nonTags.push_back( *ijet  );
	}  // end else
      }  // end if pt, eta
    } // end if deltaR

  }  // end for pat jets

  //If W is found, search for the nearest jet
  if( hasWJets() ) {
    double minDeltaR = 99999. ;
    for( size_t i=0; i<nonTags.size(); i++ ) {
      double deltaR_ = reco::deltaR<double>( wJets_.at(0)->eta(), wJets_.at(0)->phi(), 
      						nonTags.at(i)->eta(), nonTags.at(i)->phi() );
      if( deltaR_ < minDeltaR ) {
        minDeltaR = deltaR_;
	aJetFound_ = true;
	aJet_ = nonTags.at(i);
      }  //end if < minDeltaR 
    }  // end i
  }  // end if hasWJets

  //Found the min DeltaR pair of jets
  double minDeltaR = 9999. ;
  for( size_t i=0; i<nonTags.size(); i++ ) {
    for( size_t j=i+1; j<nonTags.size(); j++ ) {
      double deltaR_ = reco::deltaR<double>( nonTags.at(i)->eta(), nonTags.at(i)->phi(),
      						nonTags.at(j)->eta(), nonTags.at(j)->phi() );
      if( deltaR_ < minDeltaR ) {
        minDrPair_.clear();
        minDeltaR = deltaR_ ;
	minDrPair_.push_back( nonTags.at(i)  );
	minDrPair_.push_back( nonTags.at(j)  );
      }
    }  // end for j
  }  // end for i

  passCut( ret, "Inclusive" );

  if( ignoreCut( "Jet Preselection" ) || pfJets_.size() >= 2 )  {
    passCut( ret, "Jet Preselection" );
    if( ignoreCut(">= 1 WJet") || hasWJets() )  {
      passCut( ret, ">= 1 WJet" );

      if( ignoreCut(">= 1 bJet") || hasBJets() ) {
        passCut( ret, ">= 1 bJet" );
      }  // end >= 1 bjet
    }  // end >= 1 wjet
  } // pass jet preselection

  return (bool)ret;
}

