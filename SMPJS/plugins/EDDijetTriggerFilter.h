#ifndef EDDijetTriggerFilter_h
#define EDDijetTriggerFilter_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"


class EDDijetTriggerFilter : public edm::EDFilter {
  public:
  EDDijetTriggerFilter( const edm::ParameterSet & params ) :
      src_( params.getParameter<edm::InputTag> ("src") ),
      trigsToRead_ (params.getParameter<std::vector<std::string> > ("trigs") )
    {	
      produces< std::vector<std::string> >  ("jetPaths");	
      produces< std::vector<int> > ("prescales");
    };
    
    virtual ~EDDijetTriggerFilter() {}
   
    /// Pass the event to the filter. NOTE! We can't use the eventSetup in FWLite so ignore it.
    virtual bool filter( edm::Event & event, const edm::EventSetup& eventSetup)
    {
      std::auto_ptr< std::vector<std::string> > jetPaths (new std::vector<std::string>() );
      std::auto_ptr< std::vector<int> > prescales (new std::vector<int>() );

      edm::Handle<pat::TriggerEvent > trigHandle;
      event.getByLabel( src_, trigHandle );


      if ( trigHandle.isValid() && trigHandle->wasRun() && trigHandle->wasAccept() ) {
	pat::TriggerPathCollection const * paths = trigHandle->paths();
	for ( pat::TriggerPathCollection::const_iterator ipath = paths->begin(), pathsEnd = paths->end();
	      ipath != pathsEnd; ++ipath ) {
	  if ( ipath->wasRun() && ipath->wasAccept() && 
	       ipath->name().find("HLT_Jet") != std::string::npos && 
	       ipath->name().find("NoJetID") == std::string::npos ) {
	    for ( std::vector<std::string>::const_iterator iaccepted = trigsToRead_.begin(), iacceptedEnd = trigsToRead_.end();
		  iaccepted != iacceptedEnd; ++iaccepted ) {
	      if ( ipath->name().find( *iaccepted ) != std::string::npos ) {
		jetPaths->push_back( *iaccepted );
		prescales->push_back( ipath->prescale() );
	      }
	    }
	  }
	}
      }

      bool pass = jetPaths->size() > 0;
      event.put( jetPaths, "jetPaths"); 
      event.put( prescales, "prescales" );
      return pass;
    }

  protected:
    edm::InputTag src_;
    std::vector<std::string> trigsToRead_;
  };




#endif
