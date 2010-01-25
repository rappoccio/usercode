#ifndef Analysis_AnalysisFilters_interface_PVSelector_h
#define Analysis_AnalysisFilters_interface_PVSelector_h

#include "FWCore/Common/interface/EventBase.h"
#include "DataFormats/Common/interface/Handle.h"

#include "PhysicsTools/Utilities/interface/Selector.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include <vector>
#include <string>

// make a selector for this selection
class PVSelector : public Selector<edm::EventBase> {
public:
  PVSelector( edm::InputTag const & pvSrc,
	      int minPVTracks = 2,
	      double maxPVZ = 20)  : 
  pvSrc_ (pvSrc)
  {
    push_back("PV NTrk", minPVTracks);
    push_back("PV Z", maxPVZ);
    set("PV NTrk");
    set("PV Z");
  }

  bool operator() ( edm::EventBase const & event,  std::strbitset & ret ) {
    event.getByLabel(pvSrc_, h_primVtx);

    // check if there is a good primary vertex
    if ( (h_primVtx->size() > 0 && h_primVtx->at(0).tracksSize() >= cut("PV NTrk", int()) ) 
	 || ignoreCut("PV NTrk")    ) {
      passCut(ret, "PV NTrk" );
      if ( (h_primVtx->size() > 0 && fabs(h_primVtx->at(0).z()) <= cut("PV Z", double()) ) 
	   || ignoreCut("PV Z")    ) 
	passCut(ret, "PV Z" );
      
    }
    return (bool)ret;
  }

  edm::Handle<std::vector<reco::Vertex> > const & vertices() const { return h_primVtx; }

private:
  edm::InputTag                      pvSrc_;
  edm::Handle<std::vector<reco::Vertex> > h_primVtx;
};

#endif
