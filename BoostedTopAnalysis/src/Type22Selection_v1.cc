#include "Analysis/BoostedTopAnalysis/interface/Type22Selection_v1.h"

Type22Selection_v1::Type22Selection_v1 ( edm::ParameterSet const & params ) :
  pfJetIdParams_         (params.getParameter<edm::ParameterSet>("pfJetIDParams") ),
  pfJetSel_              (new PFJetIDSelectionFunctor(pfJetIdParams_)),
  wJetSelector_          (params.getParameter<edm::ParameterSet>("BoostedTopWJetParameters") ),
  jetPt0_                (params.getParameter<double>("jetPt0") ),
  jetPt1_                (params.getParameter<double>("jetPt1") ),
  jetEta_                (params.getParameter<double>("jetEta") ),
  bTagOP_                (params.getParameter<double>("bTagOP") ),
  bTagAlgo_              (params.getParameter<string>("bTagAlgo") ),
  jetTag_               (params.getParameter<edm::InputTag>("jetSrc") )
{
/*
  push_back("Inclusive");
  push_back("nJets >= 2");
  push_back("nJets >= 4");
  push_back("hasOneWTag");
  push_back("hasOneBTag");

  set("Inclusive");
  set("nJets >= 2");
  set("nJets >= 4");
  set("hasOneWTag");
  set("hasOneBTag");
*/
}

bool Type22Selection_v1::operator() ( edm::EventBase const & t, pat::strbitset & ret )
{
  ret.set(false);
  pfJets_.clear();
  highPtJets_.clear();
  wTags_.clear();
  bTags_.clear();

  //passCut( ret, "Inclusive" );

  edm::Handle<vector<pat::Jet>  >   jetHandle;
  t.getByLabel( jetTag_, jetHandle );

  //std::cout<<"Type22Selection Event "<<t.id()<<endl;

  pat::strbitset retPFJet = pfJetSel_->getBitTemplate();
  for( vector<pat::Jet>::const_iterator jetBegin=jetHandle->begin(), jetEnd=jetHandle->end(), ijet=jetBegin ;
    ijet!=jetEnd; ijet++ )
  {
	//std::cout<<"     Type22Selection ijet->pt() "<<ijet->pt()<<" ijet->eta() "<<ijet->eta()<<" ijet->phi() "<<ijet->phi()<<endl;

    if( ijet->pt() > jetPt1_ && fabs( ijet->eta() ) < jetEta_ )  {
	  retPFJet.set(false);
      bool passJetID = (*pfJetSel_)( *ijet, retPFJet );
      if( passJetID ) {
        pfJets_.push_back( edm::Ptr<pat::Jet>(jetHandle, ijet-jetBegin )  );
        if( ijet->pt() > jetPt0_ )
          highPtJets_.push_back( edm::Ptr<pat::Jet>(jetHandle, ijet-jetBegin )  );
      }
    } // end if jetPt, jetEta
  }

  //Search for W, b jets
  for( vector<edm::Ptr<pat::Jet> >::const_iterator jetBegin=pfJets_.begin(), jetEnd=pfJets_.end(), ijet=jetBegin ;
    ijet!=jetEnd; ijet++ )
  {
    pat::Jet const & jet = **ijet;
    pat::strbitset iret = wJetSelector_.getBitTemplate();
    if( wJetSelector_( jet, iret )  ) {
      wTags_.push_back( *ijet );
    }  else {
      if( jet.bDiscriminator( bTagAlgo_ ) > bTagOP_ )
        bTags_.push_back( *ijet );
    }
  }

  //std::cout<<"   pfJets_.size() "<<pfJets_.size()<<endl;
  //std::cout<<"   highPtJets_.size() "<<highPtJets_.size()<<endl;
  //std::cout<<"   wTags_.size() "<<wTags_.size()<<endl;
  //std::cout<<"   bTags_.size() "<<bTags_.size()<<endl;
/*
  if( highPtJets_.size() >= 2 )  {
    passCut( ret, "nJets >= 2" );
    if( pfJets_.size() >= 4 ) {
      passCut( ret, "nJets >= 4" );
      if( wTags_.size() >= 1 )  {
        passCut( ret, "hasOneWTag" );
        if( bTags_.size() >= 1 )  {
          passCut( ret, "hasOneBTag" );
        }
      }
    }
  }
*/
  return bool(ret);

}
