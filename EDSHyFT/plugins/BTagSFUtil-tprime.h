#ifndef BTagSFUtil_h
#define BTagSFUtil_h

#include <Riostream.h>
#include "TRandom3.h"
#include "TMath.h"

class BTagSFUtil{

 public:
    
  BTagSFUtil( int seed=0 );

  void modifyBTagsWithSF( bool& isBTagged_medium, int pdgIdPart,float Btageff_SF_m = 0.96, float Btagmistag_SF_m = 1.08, float  Btagmistag_eff_m = 0.01);

 private:
  
  TRandom3* rand_;

};



BTagSFUtil::BTagSFUtil( int seed ) {

  rand_ = new TRandom3(seed);

}

void BTagSFUtil::modifyBTagsWithSF(bool& isBTagged_medium, int pdgIdPart, float Btageff_SF_m,float Btagmistag_SF_m, float Btagmistag_eff_m){

  // b quarks and c quarks:
  if( abs( pdgIdPart ) == 5 ||  abs( pdgIdPart ) == 4) { 

    float coin = rand_->Uniform(1.);
    
    //    cout << "Sf / coin = "<< Btageff_SF_m << " " << coin  << endl;

    if( isBTagged_medium ){ 
      if( coin > Btageff_SF_m ) {isBTagged_medium=false;} //turn medium off 
    }
    

    // light quarks:
  } else if( abs( pdgIdPart)>0 ) { //in data it is 0 (save computing time)

    // no need to upgrade if is medium tagged
    if( isBTagged_medium ) return;

    float Btagmistag_SF = Btagmistag_SF_m;
    float Btagmistag_eff = Btagmistag_eff_m;
    
    float mistagPercent = ( Btagmistag_SF*Btagmistag_eff - Btagmistag_eff ) / ( 1. - Btagmistag_eff );    
    float coin = rand_->Uniform(1.);

    // for light quarks, the jet has to be upgraded:

    if( coin < mistagPercent ) {isBTagged_medium = true;}

    
  } //if light quark

}


#endif
