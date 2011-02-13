#include "Analysis/BoostedTopAnalysis/interface/Type11Selection_v1.h"

Type11Selection_v1::Type11Selection_v1 ( edm::ParameterSet const & params ) :
  pfJetIdParams_         (params.getParameter<edm::ParameterSet>("pfJetIDParams") ),
  pfJetSel_              (new PFJetIDSelectionFunctor(pfJetIdParams_)),
  caTopJetPtMin_                (params.getParameter<double>("caTopJetPtMin") ),
  caTopJetEtaCut_                (params.getParameter<double>("caTopJetEtaCut") ),
  patJetCollectionInputTag_ (params.getParameter<edm::InputTag>("patJetCollectionInputTag") ),
  caTopJetCollectionInputTag_ (params.getParameter<edm::InputTag>("caTopJetCollectionInputTag") )
{
  std::cout<< "Instantiated Type11Selection_v1" <<std::endl;

}

bool Type11Selection_v1::operator() ( edm::EventBase const & t, pat::strbitset & ret )
{
	ret.set(false);
	caTopJets_.clear();

	edm::Handle<vector<pat::Jet>  >   caTopJetHandle;
	t.getByLabel( caTopJetCollectionInputTag_, caTopJetHandle );

	edm::Handle<vector<pat::Jet>  >   patJetHandle;
	t.getByLabel( patJetCollectionInputTag_, patJetHandle );
	 
	pat::strbitset retPFJet = pfJetSel_->getBitTemplate();
	for( vector<pat::Jet>::const_iterator jetBegin=patJetHandle->begin(), jetEnd=patJetHandle->end(), ijet=jetBegin ; ijet!=jetEnd; ijet++ )
	{		
		if ( ijet->pt() > caTopJetPtMin_ && fabs( ijet->eta() ) < caTopJetEtaCut_)
		{
			//Jet ID is applied to the patJet. The caTop jet is then matched to the patJet
			// You can't apply jet ID to the caTop jet because
			// PF Jet ID removes all jets with 0 or 1 constituents. 
			// the constituents of caTop jets are subjets, not particles, so this requirement does not work
			retPFJet.set(false);
			bool passJetID = (*pfJetSel_)( *ijet, retPFJet );
			if( passJetID ) 
			{
				//match a caTopJet
				for( vector<pat::Jet>::const_iterator caJetBegin=caTopJetHandle->begin(), caJetEnd=caTopJetHandle->end(), jjet=caJetBegin ; jjet!=caJetEnd; jjet++ )
				{
					if ( ijet->pt() == jjet->pt() &&  ijet->eta() == jjet->eta() )
					{
						caTopJets_.push_back( edm::Ptr<pat::Jet>(caTopJetHandle, jjet-caJetBegin )  );
					}
				}
			}
		}
	}

  return bool(ret);

}
