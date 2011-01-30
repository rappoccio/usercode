#include "Analysis/BoostedTopAnalysis/interface/Type22QCDEstimation.h"

Type22QCDEstimation::Type22QCDEstimation( const edm::ParameterSet & iConfig,  TFileDirectory & iDir ) :
  theDir( iDir ),
  type22Selection_v1_     ( iConfig.getParameter<edm::ParameterSet>("Type22Selection") ),
  bTagOP_                 ( iConfig.getParameter<edm::ParameterSet>("Type22Selection").getParameter<double>("bTagOP") ),
  bTagAlgo_               ( iConfig.getParameter<edm::ParameterSet>("Type22Selection").getParameter<string>("bTagAlgo") )
{
  histograms1d["ttMassType22"]    = theDir.make<TH1F>("ttMassType22",   "t#bar{t} Inv Mass Type22",   200,  0,  2000 );
}

void Type22QCDEstimation::analyze( const edm::EventBase & iEvent )
{
  pat::strbitset   retType22 = type22Selection_v1_.getBitTemplate();
  bool passType22 = type22Selection_v1_( iEvent, retType22 );

  std::vector<edm::Ptr<pat::Jet> >  const &  pfJets_ = type22Selection_v1_.pfJets();
  wJetSelector_  = &(type22Selection_v1_.wJetSelector() );
  if( passType22 )  {
    pat::Jet const & leadJet = *pfJets_.at(0);
    std::vector<edm::Ptr<pat::Jet> >  hemisphere0, hemisphere1;
    std::vector<edm::Ptr<pat::Jet> >  wTags0,   wTags1;
    std::vector<edm::Ptr<pat::Jet> >  bTags0,   bTags1;
    std::vector<edm::Ptr<pat::Jet> >  noTags0,  noTags1;
    for( vector<edm::Ptr<pat::Jet> >::const_iterator jetBegin=pfJets_.begin(), jetEnd=pfJets_.end(), ijet=jetBegin ;
      ijet!=jetEnd; ijet++ ) 
    {
      pat::Jet const & jet = **ijet;
      bool  wtagged = false;
      bool  btagged = false;
      pat::strbitset iret = wJetSelector_->getBitTemplate();
      wtagged = wJetSelector_->operator()( jet, iret );
      btagged = (jet.bDiscriminator( bTagAlgo_ ) > bTagOP_ );

      double dPhi_ = fabs( reco::deltaPhi<double>( leadJet.phi(), jet.phi() ) );
      if( dPhi_ < TMath::Pi()/2 ) {
        hemisphere0.push_back( *ijet );
        if( wtagged ) 
          wTags0.push_back( *ijet );
        else if ( btagged )
          bTags0.push_back( *ijet );
        else
          noTags0.push_back( *ijet );
      }  else {
        hemisphere1.push_back( *ijet );
        if( wtagged )
          wTags1.push_back( *ijet );
        else if ( btagged )
          bTags1.push_back( *ijet );
        else
          noTags1.push_back( *ijet );
      }
    } // end ijet


  } // passType22

}



