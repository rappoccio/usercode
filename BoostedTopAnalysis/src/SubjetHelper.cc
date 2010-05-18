#include "Analysis/BoostedTopAnalysis/interface/SubjetHelper.h"

void pat::subjetHelper( pat::Jet const &jet,
			double & y,
			double & mu,
			double & dR ) {

  int numOfDaughters 	= jet.numberOfDaughters();

  if ( numOfDaughters < 2 ) {
    y = mu = dR = -1.0;
    return;
  }
  double mfat		= jet.mass();
  double m0		= jet.daughter(0) -> mass();
  double m1		= jet.daughter(1) -> mass();
  double pt0		= jet.daughter(0) -> pt();
  double pt1		= jet.daughter(1) -> pt();
  if ( m1 > m0 ) {
    double temp = m1;
    m1 = m0;
    m0 = temp;
    temp = pt1;
    pt1 = pt0;
    pt0 = temp;
  }

  dR = reco::deltaR<double>( jet.daughter(0) ->eta(),
			     jet.daughter(0) ->phi(),
			     jet.daughter(1) ->eta(),
			     jet.daughter(1) ->phi()  );
  y = std::min( pt0*pt0, pt1*pt1) * dR*dR / (mfat*mfat);
  mu = m0 / mfat ;

}

