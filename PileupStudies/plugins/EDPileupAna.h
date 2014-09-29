#ifndef EDPileupAna_h
#define EDPileupAna_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/VertexReco/interface/Vertex.h"


class EDPileupAna : public edm::EDFilter {
  public:
  EDPileupAna( const edm::ParameterSet & params ) :
    src_( params.getParameter<edm::InputTag> ("src") )
      {	
	produces< double >  ("npv");
      };
    
    virtual ~EDPileupAna() {}
   
    /// Pass the event to the filter. NOTE! We can't use the eventSetup in FWLite so ignore it.
    virtual bool filter( edm::Event & event, const edm::EventSetup& eventSetup)
    {
      std::auto_ptr<double> npv (new double() );

      edm::Handle<std::vector<reco::Vertex> > h_vtx;
      event.getByLabel( src_, h_vtx );
      *npv = h_vtx->size();

      bool pass = *npv > 0;
      event.put( npv, "npv"); 
      return pass;
    }

  protected:
    edm::InputTag src_;
  };




#endif
