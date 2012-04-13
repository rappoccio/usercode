
#include "Analysis/BoostedTopAnalysis/interface/HadronicSelection.h"

#include <iostream>

using namespace std;

HadronicSelection::HadronicSelection( 
    edm::InputTag const & jetTag,
    edm::InputTag const & trigTag,
    boost::shared_ptr<JetIDSelectionFunctor> & jetIdTight,
    boost::shared_ptr<CATopTagFunctor>       & caTopTagFunctor,
    int minJets, int minTags,
    double jetPtMin      , double jetEtaMax,
    double topMassMin    , double topMassMax,
    double minMass       ,
    double wMassMin      , double wMassMax
    ) :
  jetTag_(jetTag),
  trigTag_(trigTag),
  jetIdTight_(jetIdTight),
  caTopTagFunctor_(caTopTagFunctor),
  minJets_(minJets),
  minTags_(minTags),
  jetPtMin_(jetPtMin), jetEtaMax_(jetEtaMax),
  topMassMin_(topMassMin), topMassMax_(topMassMax),
  minMass_(minMass),
  wMassMin_(wMassMin), wMassMax_(wMassMax)
{
  // make the bitset
  push_back( "Inclusive"      );
  push_back( "Trigger"        );
  push_back( ">= 1 Jet"       );
  push_back( ">= 1 Tight Jet" );
  push_back( ">= N Tight Jets", minJets_);
  push_back( ">= 1 Tag"       );
  push_back( ">= N Tags"      , minTags_);

  // all on by default
  set( "Inclusive"      );
  set( "Trigger"        );
  set( ">= 1 Jet"       );
  set( ">= 1 Tight Jet" );
  set( ">= N Tight Jets");
  set( ">= 1 Tag"       );
  set( ">= N Tags"      );


}

bool HadronicSelection::operator() ( edm::EventBase const & event, std::strbitset & ret)
{
  selectedJets_.clear();
  taggedJets_.clear();

  passCut( ret, "Inclusive");

  // Get all the jets
  edm::Handle< vector< pat::Jet > > jetHandle;
  event.getByLabel (jetTag_, jetHandle);
  if ( !jetHandle.isValid() ) return (bool)ret;

  // Get the trigger
  edm::Handle<pat::TriggerEvent> triggerEvent;
  event.getByLabel(edm::InputTag("patTriggerEvent"), triggerEvent);
  if (!triggerEvent.isValid() ) return (bool)ret;  


  // Get a list of the jets that pass our tight event selection
  for ( std::vector<pat::Jet>::const_iterator jetBegin = jetHandle->begin(),
	  jetEnd = jetHandle->end(), ijet = jetBegin;
	ijet != jetEnd; ++ijet ) {
    std::strbitset iret = jetIdTight_->getBitTemplate();
    if ( ijet->pt() > jetPtMin_ && 
	 fabs(ijet->eta()) < jetEtaMax_  ) {
      selectedJets_.push_back( *ijet );
      std::strbitset ret = (*caTopTagFunctor_).getBitTemplate();
      if ( (*caTopTagFunctor_)(*ijet, ret ) ) {
	taggedJets_.push_back( *ijet );
      }
    }
  }

  // Check the trigger requirement
  pat::TriggerEvent const * trig = &*triggerEvent;

  bool passTrig = false;
  if ( trig->wasRun() && trig->wasAccept() ) {
    pat::TriggerPath const * jetPath = trig->path("HLT_Jet110");
    if ( jetPath != 0 && jetPath->wasAccept() ) {
      passTrig = true;    
    }
  }

  // Now check trigger requirement
  if ( ignoreCut("Trigger") || 
       passTrig ) {
    passCut(ret, "Trigger");

    // Now check if there is at least one jet with pt,Y cuts
    if ( ignoreCut(">= 1 Jet") ||
	 static_cast<int>(jetHandle->size()) > 0 ){
      passCut(ret,">= 1 Jet");

      // Now check if there is at least one jet that passes the jet ID cuts
      if ( ignoreCut(">= 1 Tight Jet") ||
	   static_cast<int>(selectedJets_.size()) > 0 ){
	passCut(ret,">= 1 Tight Jet");
      
	// Next require at least N (configurable) jets that pass the jet ID cuts. 
	if ( ignoreCut(">= N Tight Jets") ||
	     static_cast<int>(selectedJets_.size()) >=  this->cut(">= N Tight Jets", int()) ){
	  passCut(ret,">= N Tight Jets");

	  // Now look for >= 1 tags
	  if ( ignoreCut(">= 1 Tag") ||
	       static_cast<int>(taggedJets_.size()) > 0 ){
	    passCut(ret,">= 1 Tag");

	    // Next require at least N (configurable) tags
	    if ( ignoreCut(">= N Tags") ||
		 static_cast<int>(taggedJets_.size()) >=  this->cut(">= N Tags", int()) ){
	      passCut(ret,">= N Tags");
	    }// end if >= N Tags

	  }// end if >= 1 Tag

	}// end if >= N Tight Jets

      }// End if >= 1 Tight Jet

    }// End if >= 1 Jet	  
    
  } // end if trigger
  
  
  return (bool)ret;
}
