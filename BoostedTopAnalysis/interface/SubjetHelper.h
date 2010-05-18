#ifndef Analysis_BoostedTopAnalysis_SubjetHelper_h
#define Analysis_BoostedTopAnalysis_SubjetHelper_h

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Utilities/interface/Exception.h"

namespace pat {

  void subjetHelper( pat::Jet const &jet,
		     double & y,
		     double & mu,
		     double & dR );
}
#endif
