#ifndef Analysis_BoostedTopAnalysis_interface_CATopTagFunctor_h
#define Analysis_BoostedTopAnalysis_interface_CATopTagFunctor_h


/**
  \class    CATopTagFunctor CATopTagFunctor.h "PhysicsTools/Utilities/interface/CATopTagFunctor.h"
  \brief    Jet selector for pat::Jets

  Selector functor for pat::Jets that implements top-jet tagging from
  the CATopTag algorithm

  \author Salvatore Rappoccio
  \version  $Id: CATopTagFunctor.h,v 1.6 2009/10/12 01:07:00 srappocc Exp $
*/




#include "DataFormats/PatCandidates/interface/Jet.h"
#include "AnalysisDataFormats/TopObjects/interface/CATopJetTagInfo.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "PhysicsTools/Utilities/interface/Selector.h"

#include <TMath.h>
class CATopTagFunctor : public Selector<pat::Jet>  {

 public: // interface

  enum Version_t { CALO, PF, N_VERSIONS };
  enum Quality_t { LOOSE, TIGHT, N_QUALITY};
  

  CATopTagFunctor( Version_t version, Quality_t quality, std::string tagName ) :
   version_(version), quality_(quality), tagName_(tagName)
  {

    push_back("Top Mass"             );
    push_back("Top Mass Min", 100.0  );
    push_back("Top Mass Max", 250.0  );
    push_back("Min Mass",     50.0   );
    push_back("W Mass"               );
    push_back("W Mass Min",   0.0    );
    push_back("W Mass Max",   99999.0);


    set("Top Mass"    );
    set("Top Mass Min");
    set("Top Mass Max");
    set("Min Mass"    );
    set("W Mass",       false  );
    set("W Mass Min",   false  );
    set("W Mass Max",   false  );

  }

  // Allow for multiple definitions of the cuts. 
  bool operator()( const pat::Jet & jet, std::strbitset & ret )  
  {
    if ( version_ == CALO || version_ == PF ) 
      return caloTag( jet, ret );
    else {
      return false;
    }
  }

  // cuts based on craft 08 analysis. 
  bool caloTag( const pat::Jet & jet, std::strbitset & ret) 
  {
    
    const reco::CATopJetTagInfo * catopTag = 
      dynamic_cast<reco::CATopJetTagInfo const *>(jet.tagInfo(tagName_));

/*     std::cout << "---------" << std::endl; */
/*     std::cout << "top Mass = " << catopTag->properties().topMass << std::endl; */
/*     std::cout << "min Mass = " << catopTag->properties().minMass << std::endl; */
/*     std::cout << "w Mass   = " << catopTag->properties().wMass << std::endl; */

    // First check top mass cut
    if ( considerCut("Top Mass") ) {
      if ( ignoreCut("Top Mass Min")    || 
	   (catopTag->properties().topMass >= cut("Top Mass Min", double()) ) ) 
	passCut( ret, "Top Mass Min");
      if ( ignoreCut("Top Mass Max")    || 
	   (catopTag->properties().topMass <= cut("Top Mass Max", double()) ) ) 
	passCut( ret, "Top Mass Max");

      // If it passes the full range, set top mass to "pass"
      if ( ret[std::string("Top Mass Max")] && ret[std::string("Top Mass Min")] )
	passCut( ret, "Top Mass");      
    }else {
      passCut( ret, "Top Mass");
      passCut( ret, "Top Mass Max");
      passCut( ret, "Top Mass Min");
    }
    


    // Next check min mass cut
    if ( ignoreCut("Min Mass")    || 
	 (catopTag->properties().minMass >= cut("Min Mass", double()) ) ) 
      passCut( ret, "Min Mass");


    
    // Next check w mass cut
    if ( considerCut("W Mass") ) {
      if ( ignoreCut("W Mass Min")    || 
	   (catopTag->properties().wMass >= cut("W Mass Min", double()) ) ) 
	passCut( ret, "W Mass Min");
      if ( ignoreCut("W Mass Max")    || 
	   (catopTag->properties().wMass <= cut("W Mass Max", double()) ) ) 
	passCut( ret, "W Mass Max");

      // If it passes the full range, set w mass to "pass"
      if ( ret[std::string("W Mass Max")] && ret[std::string("W Mass Min")] )
	passCut( ret, "W Mass");
    } else {
      passCut( ret, "W Mass");
      passCut( ret, "W Mass Max");
      passCut( ret, "W Mass Min");
    }
    
    
/*     ret.print(std::cout); */
    // We're done, return
    return (bool)ret;
  }
  
 private: // member variables
  
  Version_t version_;
  Quality_t quality_;

  std::string tagName_;
  
};

#endif
