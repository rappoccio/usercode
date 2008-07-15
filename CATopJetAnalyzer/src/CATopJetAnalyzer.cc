// -*- C++ -*-
//
// Package:    CATopJetAnalyzer
// Class:      CATopJetAnalyzer
// 
/**\class CATopJetAnalyzer CATopJetAnalyzer.cc Analysis/CATopJetAnalyzer/src/CATopJetAnalyzer.cc

 Description: <one line class summary>

 Implementation:
     <Notes on implementation>
*/
//
// Original Author:  "Salvatore Rappoccio"
//         Created:  Thu Jul  3 00:19:30 CDT 2008
// $Id$
//
//


// system include files
#include <memory>
#include <vector>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "PhysicsTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ParameterSet/interface/InputTag.h"

#include "DataFormats/Math/interface/deltaR.h"

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/JetReco/interface/BasicJet.h"
#include "DataFormats/Candidate/interface/CompositeCandidate.h"
#include "PhysicsTools/CandUtils/interface/AddFourMomenta.h"
#include "DataFormats/Candidate/interface/CandMatchMap.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "PhysicsTools/CandUtils/interface/helicityAngle.h"

#include "PhysicsTools/CandUtils/interface/Booster.h"
#include <Math/VectorUtil.h>
#include <TH1.h>

using namespace edm;
using namespace reco;
using namespace std;


//
// class decleration
//

class CATopJetAnalyzer : public edm::EDAnalyzer {
   public:
      explicit CATopJetAnalyzer(const edm::ParameterSet&);
      ~CATopJetAnalyzer();


   private:
      virtual void beginJob(const edm::EventSetup&) ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      // ----------member data ---------------------------

  double myHelicityAngle( Candidate const & booster, Candidate const & c1, Candidate const & c2);
  void fillHistos( int i, int highestflavor, BasicJet const & jet ) ;


  TH1D * partonPt;
  TH1D * partonEta;
  TH1D * partonId;

  TH1D * partonPt_tagged;
  TH1D * partonEta_tagged;
  TH1D * partonId_tagged;

  static const int ncuts = 4;

  double TopMass_;
  double WMass_;

  vector<string> cuts;

  TH1D * njets_top[ncuts];
  TH1D * jetPt_top[ncuts];
  TH1D * jetEta_top[ncuts];
  TH1D * jetId_top[ncuts];

  TH1D * njets[ncuts];
  TH1D * jetPt[ncuts];
  TH1D * jetEta[ncuts];
  TH1D * jetId[ncuts];


  TH1D * jetNConstituents_;
  TH1D * jetTopMass_;
  TH1D * jetWMass_;
  TH1D * jetHelicity_;


  bool genericQCD_;
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
CATopJetAnalyzer::CATopJetAnalyzer(const edm::ParameterSet& iConfig):
  genericQCD_( iConfig.getParameter<bool>("genericQCD") ),
  TopMass_(iConfig.getParameter<double>("TopMass") ),
  WMass_(iConfig.getParameter<double>("WMass") ),
  verbose_(iConfig.getParameter<bool>("verbose") )
{
  cuts.push_back("3 or 4 subjets");
  cuts.push_back("Top mass cut");
  cuts.push_back("W mass cut");
  cuts.push_back("W helicity cut");
}


CATopJetAnalyzer::~CATopJetAnalyzer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to for each event  ------------
void
CATopJetAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{


   Handle<vector<BasicJet> > pBasicJets;
   iEvent.getByLabel("caTopJetsProducer", "caTopJets", pBasicJets);

   vector<BasicJet> const & caloJets = *pBasicJets;

   Handle<GenParticleCollection > pGenParticles;
   iEvent.getByLabel("genParticles", pGenParticles);
   
   GenParticleCollection const & genParticles = *pGenParticles;

   // Get list of hard partons
   vector<GenParticle const *> hardPartons;

   // Loop over partons to get hard partons
   GenParticleCollection::const_iterator igen = genParticles.begin(),
     igenBegin = igen,
     igenEnd = genParticles.end();
   for ( ; igen != igenEnd; ++igen ) {
     
     if ( genericQCD_ ) {
       // Look at hard scatter for QCD events
       int index = igen - igenBegin;
       if ( index == 6 || index == 7 ) {
	 partonPt->Fill( igen->pt() );
	 partonEta->Fill( igen->eta() );
	 partonId->Fill( igen->pdgId() );
	 hardPartons.push_back( &*igen );
       

	 // See if this parton is matched to a tagged jet
	 bool matched = false;
	 vector<BasicJet>::const_iterator icaloJet = caloJets.begin(),
	   icaloJetEnd = caloJets.end();
	 for ( ; icaloJet != icaloJetEnd; ++icaloJet) {
	   double dR = deltaR<BasicJet,GenParticle>( *icaloJet, *igen );
	 
	   if ( dR < 1.0 ) {
	     matched = true;
	   }
	 }

	 // If it is matched to a tagged jet, count it
	 if ( matched ) {
	   partonPt_tagged->Fill( igen->pt() );
	   partonEta_tagged->Fill( igen->eta() );
	   partonId_tagged->Fill( igen->pdgId() );  

	   
	 }
       }  
       
     }
   }
     
   njets[0]->Fill( caloJets.size() );

   vector<BasicJet>::const_iterator icaloJet = caloJets.begin(),
     icaloJetEnd = caloJets.end();
   for ( ; icaloJet != icaloJetEnd; ++icaloJet) {

     if ( verbose_ ) cout << "Processing icaloJet with pt = " << icaloJet->pt() << endl;
     
     GenParticleCollection::const_iterator igen = genParticles.begin(),
       igenBegin = igen,
       igenEnd = genParticles.end();
     int highestFlavor = 0;
     for ( ; igen != igenEnd; ++igen ) {

       if ( igen->status() == 3 && abs(igen->pdgId()) <= 7 ) {
	 if ( abs(igen->pdgId()) > highestFlavor ) {
	   highestFlavor = abs(igen->pdgId());
	 }
       }
     }

     if ( verbose_ ) cout << "Highest flavor = " << highestFlavor << endl;

     fillHistos(0, highestFlavor, *icaloJet);


     // Now get cut variables

     Jet::Constituents constituents = icaloJet->getJetConstituents();
     int nsubjets = constituents.size();
     double mtop = icaloJet->mass();
     double mw = 99999.;
     double h = 99999.;

     if ( verbose_ ) cout << "nsubjets = " << nsubjets << endl;

     jetNConstituents_->Fill( nsubjets );

     if ( nsubjets < 3 ) continue;

     for ( int isub = 0; isub < nsubjets - 1; ++isub ) {
       for ( int jsub = isub + 1; jsub < nsubjets; ++jsub ) {

	 Jet::Constituent icand = constituents[isub];
	 Jet::Constituent jcand = constituents[jsub];

	 

	 CompositeCandidate wCand("wCand");
	 wCand.addDaughter( *icand, "jet1" );
	 wCand.addDaughter( *jcand, "jet2" );

	 AddFourMomenta addFourMomenta;
	 addFourMomenta.set(wCand);

	 double imw = wCand.mass();
	 double ih = myHelicityAngle( wCand, *icand, *icaloJet );



	 if ( verbose_ ) {
	   cout << "Creating W candidates, examining: " << endl;
	   cout << "icand = " << isub << ", pt = " << icand->pt() << ", eta = " << icand->eta() << ", phi = " << icand->phi() << endl;
	   cout << "jcand = " << jsub << ", pt = " << jcand->pt() << ", eta = " << jcand->eta() << ", phi = " << jcand->phi() << endl;
	 }

	 if ( fabs( imw - WMass_ ) < mw ) {
	   mw = imw;
	   h = ih; 
	 }
       }
     }

     jetTopMass_->Fill( mtop );
     jetWMass_->Fill( mw );
     jetHelicity_->Fill( h );

     
   }
   
   
}

void CATopJetAnalyzer::fillHistos( int i, int highestFlavor, BasicJet const & jet ) 
{
  
  if ( verbose_ ) cout << "Plotting histogram " << i << " with pt = " << jet.pt() << endl;
  // Now look at kinematic distributions
  if ( highestFlavor == 6 ) {
    jetPt_top[i]->Fill( jet.pt() );
    jetEta_top[i]->Fill( jet.eta() );
  } else {
    jetPt[i]->Fill( jet.pt() );
    jetEta[i]->Fill( jet.eta() );       
  }
  jetId[i]->Fill( highestFlavor);
}

double CATopJetAnalyzer::myHelicityAngle( Candidate const & booster, Candidate const & c1, Candidate const & c2) {
  Particle::Vector boost = booster.p4().BoostToCM();
  Particle::LorentzVector c1a = ROOT::Math::VectorUtil::boost( c1.p4(), boost );
  Particle::LorentzVector c2a = ROOT::Math::VectorUtil::boost( c2.p4(), boost );

  double h = ROOT::Math::VectorUtil::Angle( c1a, c2a );
  if ( h > M_PI / 2 ) h = M_PI - h;
  return h;  
}   

// ------------ method called once each job just before starting event loop  ------------
void 
CATopJetAnalyzer::beginJob(const edm::EventSetup&)
{
   //now do what ever initialization is needed

  edm::Service<TFileService> fs;

  partonPt = fs->make<TH1D>("partonPt", "parton pt", 100, 0, 5000);
  partonEta = fs->make<TH1D>("partonEta", "parton eta", 100, -5.0, 5.0 );
  partonId = fs->make<TH1D>("partonId", "parton id", 30, 0, 30);

  partonPt_tagged = fs->make<TH1D>("partonPt_tagged", "parton pt tagged", 100, 0, 5000);
  partonEta_tagged = fs->make<TH1D>("partonEta_tagged", "parton eta tagged", 100, -5.0, 5.0 );
  partonId_tagged = fs->make<TH1D>("partonId_tagged", "parton id tagged", 30, 0, 30);

  jetNConstituents_ = fs->make<TH1D>("jetNConstituents", "jet number of constituents", 10, 0, 10);
  jetTopMass_ =  fs->make<TH1D>("jetTopMass", "jet top mass", 60, 0, 300);
  jetWMass_ =  fs->make<TH1D>("jetWMass", "jet W mass", 60, 0, 300);
  jetHelicity_ =  fs->make<TH1D>("jetHelicity", "jet W helicity", 60, 0, 6.28);

  for ( int i = 0; i < ncuts; ++i ) {
    njets[i] = fs->make<TH1D>("njets" + i, "jet multiplicity",10,0,10);
    jetPt[i] = fs->make<TH1D>("jetPt" + i, "jet pt", 100, 0, 5000);
    jetEta[i]= fs->make<TH1D>("jetEta" + i, "jet eta", 100, -5.0, 5.0 );
    jetId[i] = fs->make<TH1D>("jetId" + i, "jet pdgid", 30, 0, 30);


    njets_top[i] = fs->make<TH1D>("njets_top" + i, "jet multiplicity",10,0,10);
    jetPt_top[i] = fs->make<TH1D>("jetPt_top" + i, "jet pt", 100, 0, 5000);
    jetEta_top[i]= fs->make<TH1D>("jetEta_top" + i, "jet eta", 100, -5.0, 5.0 );
    jetId_top[i] = fs->make<TH1D>("jetId_top" + i, "jet pdgid", 30, 0, 30);
  }
}

// ------------ method called once each job just after ending the event loop  ------------
void 
CATopJetAnalyzer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(CATopJetAnalyzer);
