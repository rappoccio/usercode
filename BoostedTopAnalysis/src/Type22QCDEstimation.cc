#include "Analysis/BoostedTopAnalysis/interface/Type22QCDEstimation.h"

Type22QCDEstimation::Type22QCDEstimation( const edm::ParameterSet & iConfig,  TFileDirectory & iDir ) :
  theDir( iDir ),
  type22Selection_v1_     ( iConfig.getParameter<edm::ParameterSet>("Type22Selection") )
{
}

void Type22QCDEstimation::analyze( const edm::EventBase & iEvent )
{
  pat::strbitset   retType22 = type22Selection_v1_.getBitTemplate();
  bool passType22 = type22Selection_v1_( iEvent, retType22 );
}



