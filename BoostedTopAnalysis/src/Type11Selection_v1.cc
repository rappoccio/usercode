#include "Analysis/BoostedTopAnalysis/interface/Type11Selection_v1.h"

Type11Selection_v1::Type11Selection_v1 ( edm::ParameterSet const & params ) :
  pfJetIdParams_         (params.getParameter<edm::ParameterSet>("pfJetIDParams") ),
  pfJetSel_              (new PFJetIDSelectionFunctor(pfJetIdParams_)),
  caTopJetPtMin_                (params.getParameter<double>("caTopJetPtMin") ),
  caTopJetEtaCut_                (params.getParameter<double>("caTopJetEtaCut") ),
  caTopJetCollectionInputTag_ (params.getParameter<edm::InputTag>("caTopJetCollectionInputTag") )
{
  std::cout<< "Instantiated Type11Selection_v1" <<std::endl;

}

bool Type11Selection_v1::operator() ( edm::EventBase const & t, pat::strbitset & ret )
{
	ret.set(false);
	caTopJets_.clear();

	edm::Handle<vector<pat::Jet>  >   jetHandle;
	t.getByLabel( caTopJetCollectionInputTag_, jetHandle );
  
	pat::strbitset retPFJet = pfJetSel_->getBitTemplate();
	
	for( vector<pat::Jet>::const_iterator jetBegin=jetHandle->begin(), jetEnd=jetHandle->end(), ijet=jetBegin ; ijet!=jetEnd; ijet++ )
	{
		if ( ijet->pt() > caTopJetPtMin_ && fabs( ijet->eta() ) < caTopJetEtaCut_)
		{
			retPFJet.set(false);
			bool passJetID = (*pfJetSel_)( *ijet, retPFJet );
			if( passJetID ) 
			{
				caTopJets_.push_back( edm::Ptr<pat::Jet>(jetHandle, ijet-jetBegin )  );
			}
		}
	}

  return bool(ret);

}
