#ifndef Analysis_BTagFilter_interface_BTagFilter_h
#define Analysis_BTagFilter_interface_BTagFilter_h

#include "PhysicsTools/UtilAlgos/interface/ParameterAdapter.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "PhysicsTools/UtilAlgos/interface/ObjectCountFilter.h"
#include "PhysicsTools/UtilAlgos/interface/MinNumberSelector.h"
#include "Analysis/BTagFilter/interface/BTagFilter.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include <vector>
#include <string>

struct BDiscriminatorSelector {
  BDiscriminatorSelector( std::string disc, double discCut ) : disc_(disc), discCut_(discCut) {}
  template<typename T>
  bool operator()( const T & t ) const { return t.bDiscriminator(disc_) > discCut_; }

private:
  std::string   disc_;
  double        discCut_;
};



namespace reco {
  namespace modules {
    
    template<>
      struct ParameterAdapter<BDiscriminatorSelector> {
      static BDiscriminatorSelector make( const edm::ParameterSet & cfg ) {
        return BDiscriminatorSelector( cfg.getParameter<std::string>( "disc" ),
				       cfg.getParameter<double> ( "discCut" ));
      }
    };

  }
}


namespace pat {

typedef ObjectCountFilter<
          std::vector<Jet>,
          BDiscriminatorSelector,
          MinNumberSelector
        > BDiscriminatorPatJetSelector;

}

#endif
