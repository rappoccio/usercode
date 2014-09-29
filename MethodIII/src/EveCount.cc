// -*- C++ -*-
//
// Package:    EveCount
// Class:      EveCount
// 
/**\class EveCount EveCount.cc Analysis/EveCount/src/EveCount.cc

 Description: <one line class summary>

 Implementation:
     <Notes on implementation>
*/
//
// Original Author:  "Hu Guofan"
//         Created:  Tue Mar 31 12:36:57 CDT 2009
// $Id: EveCount.cc,v 1.1 2009/04/09 18:49:12 guofan Exp $
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "PhysicsTools/UtilAlgos/interface/TFileService.h"
#include "PhysicsTools/UtilAlgos/interface/TFileDirectory.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/Common/interface/Association.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"

//
// class decleration
//

#include <TH1.h>


using namespace edm;
using namespace pat;
using namespace std;

class EveCount : public edm::EDAnalyzer {
   public:
      explicit EveCount(const edm::ParameterSet&);
      ~EveCount();


   private:
      virtual void beginJob(const edm::EventSetup&) ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      // ----------member data ---------------------------
      InputTag muonsrc_;
      InputTag matchsrc_;
      InputTag jetsrc_;
      double bTagThreshold_; 
      bool verbose_;
      double Lxy_;
      int nOfJets[5];
      int nOfMuonMatch[5];
      int nOfOneVertex[5];
      int nOfOneTag[5];
      int nOfTwoTag[5];
      int nOfEvt;

      TH1F * muonNum_;
      TH1F * bTagDiscriminator_;

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
EveCount::EveCount(const edm::ParameterSet& iConfig)  : 
   muonsrc_( iConfig.getParameter<InputTag>("muonsrc") ),
   matchsrc_( iConfig.getParameter<InputTag>("matchsrc") ),
   jetsrc_ ( iConfig.getParameter<InputTag>("jetsrc") ),
   bTagThreshold_ ( iConfig.getParameter<double>("bTagThreshold")  ),
   Lxy_( iConfig.getParameter<double>("Lxy")  ),
   verbose_( iConfig.getParameter<bool>("verbose") )
{
   //now do what ever initialization is needed
  Service<TFileService> fs;
  TFileDirectory plots = TFileDirectory( fs->mkdir("counts") );

  muonNum_  = plots.make<TH1F>("muonNum",  "Number of muons in event", 20, 0, 20);
  bTagDiscriminator_  = plots.make<TH1F>("bTag", "b Tagging discriminator ", 100, -50, 50);

  nOfEvt =0;
  for(int i=0; i<5; i++){
    nOfJets[i]=0;
    nOfMuonMatch[i]=0;
    nOfOneVertex[i]=0;
    nOfOneTag[i]=0;
    nOfTwoTag[i]=0;
  }

}


EveCount::~EveCount()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to for each event  ------------
void
EveCount::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   if(verbose_ ) cout<<"---------begin the analyzer----------"<<endl;
   nOfEvt++;


   Handle<vector<pat::Jet> > jets;
   iEvent.getByLabel(jetsrc_ , jets );

   if(jets->size() == 0 ) {
	cout<<"No jets in the event"<<endl;
	return;
   }
   int njet = ( jets->size() > 5 ) ? 5 : jets->size();
   if ( verbose_ )  cout<<"The number of jets is "<<njet<<endl;
   nOfJets[njet-1]++;

   Handle<edm::Association<vector<reco::GenParticle> > > match;
   iEvent.getByLabel(matchsrc_, match);

   Handle<reco::CandidateView > muons;
   iEvent.getByLabel(muonsrc_  , muons);

   if( verbose_ )   cout<<"The number of muons in this event is "<<muons->size()<<endl;
   if( verbose_ )   cout<<"Filling the muons number histogram"<<endl;
   muonNum_ ->Fill( muons->size() );

   reco::CandidateView::const_iterator im_begin = muons->begin(),
	im_end = muons->end(), im = muons->begin();

   for(; im != im_end; ++im){

      if(verbose_ ) cout<<"Processing muon "<<im - im_begin<<endl;
      //if( verbose_ ) cout<<"the number of mother is "<<im->numberOfMothers()<<" the first mom is "<<im->mother()<<endl;
      size_t index = (size_t) ( im - im_begin);
      const reco::CandidateBaseRef cand( muons , index );
      const reco::GenParticleRef mcMatch = (*match)[cand];
      if( mcMatch.isNonnull() ) {
          //nOfMuonMatch[njet-1]++;
	  //nOfMuonMatch[5]++;       //compile and run well with this, really a pitfall!!
	  if( verbose_ )   cout<<"There is muon match!!"<<endl;
	  const reco::Candidate * mom;
	  for( mom = mcMatch->mother(); mom->status() != 3; mom = mom->mother() );
	  if( verbose_ ) cout<<" the status 3 mom of this muon is "<<mom->mother()->pdgId()<<endl;
	  if( verbose_ ) cout<<"the first generation daughter of this mom is: "<<endl;
	  if( verbose_ ) cout<<"the total number of daugthers of this momther is "<<mom->numberOfDaughters() <<endl;
	  for( int i=0; i < mom->numberOfDaughters() ; i++)  {
		if( verbose_ )  cout<<"daughter "<<i<<" pdgID is "<<mom->daughter(i)->pdgId()<<endl;
		if( abs(mom->daughter(i)->pdgId() ) == 13 || abs(mom->daughter(i)->pdgId() ) == 15 ) {
		   if( verbose_ ) cout<<"we finally find a valid muon"<<endl;
		   nOfMuonMatch[njet-1]++;
		   break;
		}
	  }
      }
   } 
 
   vector<Jet>::const_iterator jetBegin = jets->begin(),
      jetEnd = jets->end(),  ijet = jetBegin;

   int nOfTags = 0;
   int nOfVertex = 0;
   for( ; ijet != jetEnd; ++ijet ) {
      if( verbose_ ) cout<<"Processing jet "<< ijet - jetBegin <<endl;
      // Get the associated tag infos
      float bTagDiscriminator = ijet->bDiscriminator("");
      if (verbose_ )    cout<<"the b Discriminator is "<<bTagDiscriminator<<endl;
      bTagDiscriminator_ ->Fill(bTagDiscriminator);
      if( bTagDiscriminator > bTagThreshold_ ) nOfTags++;

      reco::SecondaryVertexTagInfo const * svTagInfos = ijet->tagInfoSecondaryVertex("secondaryVertex");
      if( svTagInfos == 0 )  continue;
      if ( verbose_ )   cout<<"the number of secondary vertices is "<<svTagInfos->nVertices()<<endl;
      if ( svTagInfos->nVertices() > 0 ) {
	  double lxy = svTagInfos->flightDistance(0).significance();
	  if ( verbose_ )  cout<<"the svLxySig is "<<svTagInfos->flightDistance(0).significance()<<endl;
          if ( lxy > Lxy_ )  nOfVertex++;
      }
   }
   if ( nOfTags == 1 ) nOfOneTag[njet-1]++;
   if ( nOfTags == 2 ) nOfTwoTag[njet-1]++;
   if ( nOfVertex > 0 ) nOfOneVertex[njet-1]++;
}


// ------------ method called once each job just before starting event loop  ------------
void 
EveCount::beginJob(const edm::EventSetup&)
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
EveCount::endJob() {
   cout<<"the total number of events received by EveCount is "<<nOfEvt<<endl;
   for(int i=0; i < 5; i++){
     cout<<"Events with "<<i+1<<" jets: "<<nOfJets[i]<<endl;
     cout<<"With a valid muon matched to genMuon: "<<nOfMuonMatch[i]<<endl;
     cout<<"With one vertex: "<<nOfOneVertex[i]<<endl;
     cout<<"With one Tag: "<<nOfOneTag[i]<<endl;
     cout<<"With two Tags: "<<nOfTwoTag[i]<<endl;    
   }
}

//define this as a plug-in
DEFINE_FWK_MODULE(EveCount);
