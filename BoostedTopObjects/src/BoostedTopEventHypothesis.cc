#include "Analysis/BoostedTopObjects/interface/BoostedTopEventHypothesis.h"
#include "CommonTools/CandUtils/interface/AddFourMomenta.h"

void BoostedTopEventHypothesis::setSemiLepType1( reco::CandidatePtr const & bJet,
						 reco::CandidatePtr const & muon,
						 reco::CandidatePtr const & met,			
						 reco::CandidatePtr const & topJet )
{
  // 4-vector utility
  AddFourMomenta addP4;

  // Need to construct the semileptonic top decay candidate hierarchy
  wVector_.resize(1);
  tVector_.resize(1);

  // create W candidate
  wVector_[0].addDaughter( muon );
  wVector_[0].addDaughter( met );
  addP4.set( wVector_[0] );


  // Create leptonic top candidate
  tVector_[0].addDaughter( bJet );
  tVector_[0].addDaughter( reco::CandidatePtr( &wVector_, 0) );
  addP4.set( tVector_[0] );

  // Create resonance candidate
  this->addDaughter( reco::CandidatePtr( &tVector_, 0 ) );
  this->addDaughter( topJet );

  decay_ = SEMI_TYPE1;
}

void BoostedTopEventHypothesis::setSemiLepType2( reco::CandidatePtr const & bJet1,
						 reco::CandidatePtr const & muon,
						 reco::CandidatePtr const & met,
						 reco::CandidatePtr const & bJet2,
						 reco::CandidatePtr const & wJet )
{
  // 4-vector utility
  AddFourMomenta addP4;

  // Need to construct the semileptonic 
  // and "type 2" top decay candidate hierarchy
  wVector_.resize(1);
  tVector_.resize(2);

  // create W candidate
  wVector_[0].addDaughter( muon );
  wVector_[0].addDaughter( met );
  addP4.set( wVector_[0] );

  // Create leptonic top candidate
  tVector_[0].addDaughter( bJet1 );
  tVector_[0].addDaughter( reco::CandidatePtr( &wVector_, 0) );
  addP4.set( tVector_[0] );

  // Create hadronic top candidate
  tVector_[1].addDaughter( bJet2 );
  tVector_[1].addDaughter( wJet ) ;
  addP4.set( tVector_[1] );
  
  // Create resonance candidate
  this->addDaughter( reco::CandidatePtr( &tVector_, 0 ) );
  this->addDaughter( reco::CandidatePtr( &tVector_, 1 ) );
  addP4.set( *this );
  
  decay_ = SEMI_TYPE2;
}

void BoostedTopEventHypothesis::setSemiLepType3( reco::CandidatePtr const & bJet1,
						 reco::CandidatePtr const & muon,
						 reco::CandidatePtr const & met,
						 reco::CandidatePtr const & bJet2,
						 reco::CandidatePtr const & qJet,
						 reco::CandidatePtr const & pJet )
{
  // 4-vector utility
  AddFourMomenta addP4;

  // Need to construct the semileptonic 
  // and "type 2" top decay candidate hierarchy
  wVector_.resize(2);
  tVector_.resize(2);

  // create leptonic W candidate
  wVector_[0].addDaughter( muon );
  wVector_[0].addDaughter( met );
  addP4.set( wVector_[0] );

  // Create leptonic top candidate
  tVector_[0].addDaughter( bJet1 );
  tVector_[0].addDaughter( reco::CandidatePtr( &wVector_, 0) );
  addP4.set( tVector_[0] );

  // Create hadronic W candidate
  wVector_[1].addDaughter( qJet );
  wVector_[1].addDaughter( pJet );
  addP4.set( wVector_[1] );

  // Create hadronic top candidate
  tVector_[1].addDaughter( bJet2 );
  tVector_[1].addDaughter( reco::CandidatePtr( &wVector_, 1) );
  addP4.set( tVector_[1] );
  
  // Create resonance candidate
  this->addDaughter( reco::CandidatePtr( &tVector_, 0 ) );
  this->addDaughter( reco::CandidatePtr( &tVector_, 1 ) );
  addP4.set( *this );

  decay_ = SEMI_TYPE3;
}

void BoostedTopEventHypothesis::setHadType1Type1( reco::CandidatePtr const & topJet1,
						  reco::CandidatePtr const & topJet2 )
{
  // 4-vector utility
  AddFourMomenta addP4;

  // Create resonance candidate
  this->addDaughter( topJet1 );
  this->addDaughter( topJet2 );
  addP4.set( *this );

  decay_ = HAD_TYPE1_TYPE1;
}
 

void BoostedTopEventHypothesis::setHadType1Type2( reco::CandidatePtr const & topJet1,
						  reco::CandidatePtr const & bJet2,
						  reco::CandidatePtr const & wJet2 )
{
  // 4-vector utility
  AddFourMomenta addP4;
  
  // Need to construct the "type 2" top decay candidate hierarchy
  tVector_.resize(1);

  // Create hadronic top candidate
  tVector_[0].addDaughter( bJet2 );
  tVector_[0].addDaughter( wJet2 ) ;
  addP4.set( tVector_[0] );
  
  // Create resonance candidate
  this->addDaughter( topJet1 );
  this->addDaughter( reco::CandidatePtr( &tVector_, 0 ) );
  addP4.set( *this );

  decay_ = HAD_TYPE1_TYPE2;
} 
  
void BoostedTopEventHypothesis::setHadType1Type3( reco::CandidatePtr const & topJet1,
						  reco::CandidatePtr const & bJet2,
						  reco::CandidatePtr const & qJet2,
						  reco::CandidatePtr const & pJet2 )
{
  // 4-vector utility
  AddFourMomenta addP4;

  // Need to construct the semileptonic 
  // and "type 2" top decay candidate hierarchy
  wVector_.resize(1);
  tVector_.resize(1);

  // Create hadronic W candidate
  wVector_[0].addDaughter( qJet2 );
  wVector_[0].addDaughter( pJet2 );
  addP4.set( wVector_[0] );

  // Create hadronic top candidate
  tVector_[0].addDaughter( bJet2 );
  tVector_[0].addDaughter( reco::CandidatePtr( &wVector_, 0) );
  addP4.set( tVector_[0] );
  
  // Create resonance candidate
  this->addDaughter( topJet1 );
  this->addDaughter( reco::CandidatePtr( &tVector_, 0 ) );
  addP4.set( *this );
  

  decay_ = HAD_TYPE1_TYPE3;
} 


void BoostedTopEventHypothesis::setHadType2Type2( reco::CandidatePtr const & bJet1,
						  reco::CandidatePtr const & wJet1,
						  reco::CandidatePtr const & bJet2,
						  reco::CandidatePtr const & wJet2 )
{  
  // 4-vector utility
  AddFourMomenta addP4;
  
  // Need to construct both "type 2" top decay candidate hierarchy
  tVector_.resize(2);

  // Create hadronic top candidate
  tVector_[0].addDaughter( bJet1 );
  tVector_[0].addDaughter( wJet1 ) ;
  addP4.set( tVector_[0] );

  // Create hadronic top candidate
  tVector_[1].addDaughter( bJet2 );
  tVector_[1].addDaughter( wJet2 ) ;
  addP4.set( tVector_[1] );

  
  // Create resonance candidate
  this->addDaughter( reco::CandidatePtr( &tVector_, 0 ) );
  this->addDaughter( reco::CandidatePtr( &tVector_, 1 ) );
  addP4.set( *this );

  decay_ = HAD_TYPE2_TYPE2;
} 
  
void BoostedTopEventHypothesis::setHadType2Type3( reco::CandidatePtr const & bJet1,
						  reco::CandidatePtr const & wJet1,
						  reco::CandidatePtr const & bJet2,
						  reco::CandidatePtr const & qJet2,
						  reco::CandidatePtr const & pJet2 )
{  
  // 4-vector utility
  AddFourMomenta addP4;
  
  // Need to construct "type 2" and "type 3" top decay candidate hierarchy
  wVector_.resize(1);
  tVector_.resize(2);

  // Create hadronic top candidate
  tVector_[0].addDaughter( bJet1 );
  tVector_[0].addDaughter( wJet1 ) ;
  addP4.set( tVector_[0] );

  // Create hadronic W candidate
  wVector_[0].addDaughter( qJet2 );
  wVector_[0].addDaughter( pJet2 );
  addP4.set( wVector_[0] );

  // Create hadronic top candidate
  tVector_[1].addDaughter( bJet2 );
  tVector_[1].addDaughter( reco::CandidatePtr( &wVector_, 0) );
  addP4.set( tVector_[1] );
  
  // Create resonance candidate
  this->addDaughter( reco::CandidatePtr( &tVector_, 0 ) );
  this->addDaughter( reco::CandidatePtr( &tVector_, 1 ) );
  addP4.set( *this );

  decay_ = HAD_TYPE2_TYPE3;
} 

void BoostedTopEventHypothesis::setHadType3Type3( reco::CandidatePtr const & bJet1,
						  reco::CandidatePtr const & qJet1,
						  reco::CandidatePtr const & pJet1,
						  reco::CandidatePtr const & bJet2,
						  reco::CandidatePtr const & qJet2,
						  reco::CandidatePtr const & pJet2 )
{
  // 4-vector utility
  AddFourMomenta addP4;
  
  // Need to construct both "type 3" top decay candidate hierarchy
  wVector_.resize(2);
  tVector_.resize(2);

  // Create hadronic W candidate
  wVector_[0].addDaughter( qJet1 );
  wVector_[0].addDaughter( pJet1 );
  addP4.set( wVector_[0] );

  // Create hadronic top candidate
  tVector_[0].addDaughter( bJet1 );
  tVector_[0].addDaughter( reco::CandidatePtr( &wVector_, 0) );
  addP4.set( tVector_[0] );

  // Create hadronic W candidate
  wVector_[1].addDaughter( qJet2 );
  wVector_[1].addDaughter( pJet2 );
  addP4.set( wVector_[1] );

  // Create hadronic top candidate
  tVector_[1].addDaughter( bJet2 );
  tVector_[1].addDaughter( reco::CandidatePtr( &wVector_, 1) );
  addP4.set( tVector_[1] );
  
  // Create resonance candidate
  this->addDaughter( reco::CandidatePtr( &tVector_, 0 ) );
  this->addDaughter( reco::CandidatePtr( &tVector_, 1 ) );
  addP4.set( *this );

  decay_ = HAD_TYPE3_TYPE3;
} 





reco::Candidate const * BoostedTopEventHypothesis::getT1()   const
{
  return  this->daughterPtr(0).get();

} 

reco::Candidate const * BoostedTopEventHypothesis::getT2()   const
{  
  return  this->daughterPtr(1).get();
} 



reco::Candidate const * BoostedTopEventHypothesis::getB1()   const
{
  reco::Candidate const * t1 = getT1();
  if ( t1 != 0 )  return t1->daughter(0);
  else return 0;
} 

reco::Candidate const * BoostedTopEventHypothesis::getB2()   const
{
  reco::Candidate const * t2 = getT2();
  if ( t2 != 0 )  return t2->daughter(0);
  else return 0;
} 

reco::Candidate const * BoostedTopEventHypothesis::getW1()   const
{
  reco::Candidate const * t1 = getT1();
  if ( t1 != 0 )  return t1->daughter(1);
  else return 0;
} 

reco::Candidate const * BoostedTopEventHypothesis::getW2()   const
{
  reco::Candidate const * t2 = getT2();
  if ( t2 != 0 )  return t2->daughter(1);
  else return 0;
} 




reco::Candidate const * BoostedTopEventHypothesis::getMu() const
{
  if ( decay_ > SEMI_TYPE3 ) return 0;

  reco::Candidate const * w1 = getW1();
  if ( w1 != 0 )  return w1->daughter(0);
  else return 0;
} 

reco::Candidate const * BoostedTopEventHypothesis::getNu()  const
{
  if ( decay_ > SEMI_TYPE3 ) return 0;

  reco::Candidate const * w1 = getW1();
  if ( w1 != 0 )  return w1->daughter(1);
  else return 0;
} 


reco::Candidate const * BoostedTopEventHypothesis::getQ1()   const
{
  if ( decay_ <= SEMI_TYPE3 ) return 0;

  reco::Candidate const * w1 = getW1();
  if ( w1 != 0 )  return w1->daughter(0);
  else return 0;  
} 
reco::Candidate const * BoostedTopEventHypothesis::getP1()   const
{
  if ( decay_ <= SEMI_TYPE3 ) return 0;

  reco::Candidate const * w1 = getW1();
  if ( w1 != 0 )  return w1->daughter(1);
  else return 0;
} 


reco::Candidate const * BoostedTopEventHypothesis::getQ2()   const
{
  reco::Candidate const * w2 = getW2();
  if ( w2 != 0 )  return w2->daughter(0);
  else return 0;  
} 
reco::Candidate const * BoostedTopEventHypothesis::getP2()   const
{
  reco::Candidate const * w2 = getW2();
  if ( w2 != 0 )  return w2->daughter(1);
  else return 0;
} 

