// -*- C++ -*-
//
// Package:    SemiLepSel
// Class:      SemiLepSel
// 
/**\class SemiLepSel SemiLepSel.cc Analysis/SemiLepSel/src/SemiLepSel.cc

 Description: <one line class summary>

 Implementation:
     <Notes on implementation>
*/
//
// Original Author:  "Hu Guofan"
//         Created:  Mon Mar 30 15:34:47 CDT 2009
// $Id: SemiLepSel.cc,v 1.1 2009/04/09 18:55:59 guofan Exp $
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

//
// class declaration
//
using namespace std;
using namespace edm;
using namespace reco;

class SemiLepSel : public edm::EDFilter {
   public:
      explicit SemiLepSel(const edm::ParameterSet&);
      ~SemiLepSel();

   private:
      virtual void beginJob(const edm::EventSetup&) ;
      virtual bool filter(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      bool select( vector<const Candidate *> ) ;
      
      // ----------member data ---------------------------
      edm::InputTag src_;
      int numofevents_;
      int semilepevents_;
      int enu_;
      int munu_;
      int taunu_;
      bool verbose_;

};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//


SemiLepSel::SemiLepSel(const edm::ParameterSet& iConfig) :
  src_( iConfig.getParameter<InputTag>("src")  ),
  verbose_( iConfig.getParameter<bool>("verbose")  ),
  numofevents_(0), semilepevents_(0)
{
   //now do what ever initialization is needed
   enu_=0;
   munu_=0;
   taunu_=0;

}


SemiLepSel::~SemiLepSel()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called on each new Event  ------------
bool
SemiLepSel::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   if( verbose_ )   cout<<"--------------Filter an event------------------"<<endl;
   numofevents_++;

   Handle<vector<reco::GenParticle> > particles;
   iEvent.getByLabel(src_  ,particles);

   vector<const Candidate *> status3part ;
   if( verbose_ ) cout<<"searching the status 3 particles"<<endl;
   for( vector<reco::GenParticle>::const_iterator p = particles->begin(); p != particles->end(); ++p){
      if( p->status() == 3 ) {
          //if( verbose_ ) cout<<"searching the status 3 particles"<<endl;
          status3part.push_back(&*p);
      }
   }

   if( verbose_ ) cout<<"the number of status 3 particles are "<<status3part.size()<<endl;

   if( select(status3part) ){
       cout<<"This event is a semileptonic event"<<endl;
       semilepevents_++;
       return true;
   }
   else return false; 
}

// ------------ method called once each job just before starting event loop  ------------
void 
SemiLepSel::beginJob(const edm::EventSetup&)
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
SemiLepSel::endJob() {
   cout<<"the total number of events received by SemiLepSel is "<<numofevents_<<endl;
   cout<<"the number of semileptonic event is "<<semilepevents_<<endl;
   cout<<"the number of e nu events is "<<enu_<<endl;
   cout<<"the number of mu nu events is " << munu_<<endl;
   cout<<"the number of tau nu events is " << taunu_  <<endl;

}

bool SemiLepSel::select( vector<const Candidate *>   parton )   {

   int numW=0;
   const Candidate * w1, * w2;
   for( vector<const Candidate *>::const_iterator p1 = parton.begin(); p1 != parton.end(); ++p1 ){
	if( abs( (*p1)->pdgId() ) == 24 ) {
	   numW++;
	   if(numW == 1)  w1 = *p1;
	   if(numW == 2)  w2 = *p1;
	}
   }

   if ( verbose_ )    cout<<"the number of W boson is "<<numW<<endl;
   if(numW == 1){
	if( verbose_ )  cout<<"this is not ttbar event ! The number of daughters of W is "<<w1->numberOfDaughters()<<endl;
	if( abs(w1->daughter(0)->pdgId() ) > 10 && abs(w1->daughter(0)->pdgId() ) < 19  && 
	    abs(w1->daughter(1)->pdgId() ) > 10 && abs(w1->daughter(1)->pdgId() ) < 19 ) 
		return true;
        else return false;
   }
   if( numW == 2){
        if( verbose_ )  cout<<"this is ttbar event ! The number of daughters of W is "<<w1->numberOfDaughters()<<" and "<<w2->numberOfDaughters()<<endl;
	if( ( abs(w1->daughter(0)->pdgId() ) > 10 && abs(w1->daughter(0)->pdgId() ) < 19 &&
            abs(w2->daughter(0)->pdgId() ) > 0  && abs(w2->daughter(0)->pdgId() )  < 9 ) ||
            ( abs(w1->daughter(0)->pdgId() ) > 0 && abs(w1->daughter(0)->pdgId() ) < 9 &&
            abs(w2->daughter(0)->pdgId() ) > 10  && abs(w2->daughter(0)->pdgId() )  < 19 ) )
		{
		   if(( abs(w1->daughter(0)->pdgId() ) > 10 && abs(w1->daughter(0)->pdgId() ) <	13 ) ||
			(abs(w2->daughter(0)->pdgId() ) > 10 &&abs(w2->daughter(0)->pdgId() )  < 13 ) )  enu_++;
		   if(( abs(w1->daughter(0)->pdgId() ) > 12 && abs(w1->daughter(0)->pdgId() ) < 15 ) ||
                        (abs(w2->daughter(0)->pdgId() ) > 12 &&abs(w2->daughter(0)->pdgId() )  < 15 ) )  munu_++;
                   if(( abs(w1->daughter(0)->pdgId() ) > 14 && abs(w1->daughter(0)->pdgId() ) < 17 ) ||
                        (abs(w2->daughter(0)->pdgId() ) > 14 &&abs(w2->daughter(0)->pdgId() )  < 17 ) )  taunu_++;
  		   return true;
		}
	else return false;

   }

   if( numW > 2)  cout<<"some exotic events!!!!"<<endl;

}





//define this as a plug-in
DEFINE_FWK_MODULE(SemiLepSel);
