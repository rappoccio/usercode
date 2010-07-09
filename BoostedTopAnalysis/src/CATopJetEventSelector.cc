#include "Analysis/BoostedTopAnalysis/interface/CATopJetEventSelector.h"

CATopJetEventSelector::CATopJetEventSelector ( edm::ParameterSet const & params ) :
  jetTag_		(params.getParameter<edm::InputTag>("CATopJetSrc")  ),
  caTopJetSelector_	(params.getParameter<edm::ParameterSet>("CATopJetParameters") ),
  jetPtMin_		(params.getParameter<double>("jetPtMin") ),
  jetEtaMax_		(params.getParameter<double>("jetEtaMax") )
{
  //make the bitset
  push_back( "Inclusive"	);
  push_back(">= 1 TopJet"	);
  push_back(">= 2 TopJet"	);

  //turn on 
  set( "Inclusive"	);
  set(">= 1 TopJet"	);
  //set(">= 2 TopJet"	);


}

bool CATopJetEventSelector::operator() ( edm::EventBase const & t, reco::Candidate::LorentzVector const & v, pat::strbitset & ret)
{
  ret.set(false);
  topJets_.clear();

  passCut( ret, "Inclusive" );

  edm::Handle<vector<pat::Jet>  >	   jetHandle;
  t.getByLabel( jetTag_,  jetHandle );
  
  //Search for top jets
  for( vector<pat::Jet>::const_iterator jetBegin=jetHandle->begin(), jetEnd=jetHandle->end(), ijet=jetBegin ;
    ijet!=jetEnd; ijet++ )
  {
    if( ijet->pt() > jetPtMin_ && fabs( ijet->eta() ) < jetEtaMax_ ) {
      pat::strbitset iret = caTopJetSelector_.getBitTemplate();
      if( caTopJetSelector_( *ijet, iret )  ) {
        topJets_.push_back( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Jet>( jetHandle, ijet-jetBegin )  )  );
      }  
    } // end if jet pt, eta
  }  // end for jets

  if( ignoreCut(">= 1 TopJet")  ||
    hasTopJets() ) {
    passCut( ret, ">= 1 TopJet");

    if( ignoreCut(">= 2 TopJet") ||
      topJets_.size() >= 2 )  {
        passCut( ret, ">= 2 TopJet");
      }  // >= 2 TopJet
  }  // >= 1 TopJet

  return (bool)ret;
}
