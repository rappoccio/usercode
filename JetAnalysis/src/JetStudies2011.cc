#include "Analysis/JetAnalysis/interface/JetStudies2011.h"
#include "TVector3.h"
#include "TLorentzVector.h"
#include <sstream>
#include "TRandom.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/Math/interface/deltaR.h"

using namespace std;



JetStudies2011::JetStudies2011(const edm::ParameterSet& iConfig, TFileDirectory& iDir) :
  edm::BasicAnalyzer(iConfig,iDir),
  theDir(iDir),
  jetSrc_        ( iConfig.getParameter<edm::InputTag>("jetSrc")),
  rhoSrc_        ( iConfig.getParameter<edm::InputTag>("rhoSrc")),
  pvSrc_         ( iConfig.getParameter<edm::InputTag>("pvSrc")),
  trigSrc_       ( iConfig.getParameter<edm::InputTag>("trigSrc")),
  genJetsSrc_    ( iConfig.getParameter<edm::InputTag>("genJetsSrc")),
  useCA8GenJets_ ( iConfig.getParameter<bool>         ("useCA8GenJets")),
  weightPV_      ( iConfig.getParameter<bool>         ("weightPV")),
  lumiWeighting_ ( iConfig.getParameter<edm::ParameterSet>("lumiWeighting").getParameter<std::string>("generatedFile"),
		   iConfig.getParameter<edm::ParameterSet>("lumiWeighting").getParameter<std::string>("dataFile") ),
  trigs_         (iConfig.getParameter<std::vector<std::string> >("trigs") )
{

  theDir.make<TH1F>( "nPV",   ";N_{Primary Vertex}", 25, 0, 25 );
  theDir.make<TH1F>( "nPVRewightedNPV", ";N_{Primary Vertex}", 25, 0, 25 );  
  theDir.make<TH1F>( "nPVRewightedPtHat", ";N_{Primary Vertex}", 25, 0, 25 );

  for ( std::vector<std::string>::const_iterator itrig = trigs_.begin(),
	  itrigEnd = trigs_.end();
	itrig != itrigEnd; ++itrig ) {
    dirs_.push_back( theDir.mkdir( *itrig ) );
    dirs_.back().make<TH1F>( "jetPt_L2L3",  "L2+L3 Correction;Jet p_{T} (GeV/c)",    100, 0, 1000);
    dirs_.back().make<TH1F>( "jetPt_L1L2L3","L1+L2+L3 Correction;Jet p_{T} (GeV/c)", 100, 0, 1000);
    dirs_.back().make<TH1F>( "jetArea",     "Jet Area;Area (radians)",               100, 0, TMath::Pi() );
    dirs_.back().make<TH1F>( "jetEta",      "Jet #eta;#eta (radians)",               100, -5.0, 5.0 );    
    dirs_.back().make<TH1F>( "jetPhi",      "Jet #phi;#phi (radians)",               100, -TMath::Pi(), TMath::Pi() );
    dirs_.back().make<TH1F>( "jetMass",     "Jet Mass;Mass (GeV/c^{2})",             100, 0, 200. );
    
  }
  dirs_.push_back( theDir.mkdir( "MC") );
  dirs_.back().make<TH1F>( "jetPt_L2L3",  "L2+L3 Correction;Jet p_{T} (GeV/c)",    100, 0, 1000);
  dirs_.back().make<TH1F>( "jetPt_L1L2L3","L1+L2+L3 Correction;Jet p_{T} (GeV/c)", 100, 0, 1000);
  dirs_.back().make<TH1F>( "jetArea",     "Jet Area;Area (radians)",               100, 0, TMath::Pi() );
  dirs_.back().make<TH1F>( "jetEta",      "Jet #eta;#eta (radians)",               100, -5.0, 5.0 );    
  dirs_.back().make<TH1F>( "jetPhi",      "Jet #phi;#phi (radians)",               100, -TMath::Pi(), TMath::Pi() );
  dirs_.back().make<TH1F>( "jetMass",     "Jet Mass;Mass (GeV/c^{2})",             100, 0, 200. );
  dirs_.back().make<TH2F>( "jetRes_L2L3", "Jet Response, L2+L3;Response",          25,  0, 1000., 25., 0., 2.5 );
  dirs_.back().make<TH2F>( "jetRes_L1L2L3","Jet Response, L1+L2+L3;Response",      25,  0, 1000., 25., 0., 2.5 );
            
}


///////////////////
/// The event loop
//////////////////
void JetStudies2011::analyze(const edm::EventBase& iEvent)
{
  edm::Handle<std::vector<reco::Vertex> > h_pv;

  iEvent.getByLabel( pvSrc_, h_pv );
  theDir.getObject<TH1>( "nPV" )->Fill( h_pv->size() );
  if ( h_pv->size() == 0 ) 
    return;

  edm::Handle<std::vector<pat::Jet> > h_jets;
  edm::Handle<double> h_rho;
  edm::Handle<pat::TriggerEvent> h_trig;

  double weightMC = 1.0;
  bool passed = false;
  std::vector<std::pair<unsigned int, unsigned int> > fired;
  if ( iEvent.isRealData() ) {
    iEvent.getByLabel( trigSrc_,h_trig );
    // This expects the HLT trigger list to be "sorted" by priority
    for ( std::vector<std::string>::const_iterator itrigBegin = trigs_.begin(),
	    itrigEnd = trigs_.end(), itrig = itrigBegin;
	  itrig != itrigEnd; ++itrig ) {
      if ( h_trig->wasRun() && h_trig->wasAccept() && h_trig->paths() > 0 ) {
	int indexPath = h_trig->indexPath( *itrig );
	if ( indexPath > 0 ) {
	  pat::TriggerPath const * path = h_trig->path( *itrig );
	  if ( path != 0 && path->wasRun() && path->wasAccept() ) {
	    passed = true;
	    fired.push_back( std::make_pair<unsigned int, unsigned int>( itrig - itrigBegin, path->prescale() ) );
	  }
	}
      }
    }
  }
  else {
    passed = true;
    if ( weightPV_ ) {
      weightMC *= lumiWeighting_.weight( h_pv->size() );
      theDir.getObject<TH1>( "nPVRewightedNPV" )->Fill( h_pv->size(), weightMC );
    }
    edm::Handle<GenEventInfoProduct>    genEvt;
    iEvent.getByLabel( edm::InputTag("generator"),  genEvt );
    if( genEvt.isValid() )  {
      weightMC *= genEvt->weight() ;
    }
    theDir.getObject<TH1>( "nPVRewightedPtHat" )->Fill( h_pv->size(), weightMC );
  }

  if ( !passed ) 
    return;

  iEvent.getByLabel( jetSrc_, h_jets );
  iEvent.getByLabel( rhoSrc_, h_rho );

  if ( h_jets->size() != 2 ) 
    return;

  double rho = *h_rho;

  pat::Jet const & jet0 = h_jets->at(0);
  pat::Jet const & jet1 = h_jets->at(1);

  if ( reco::deltaR<pat::Jet, pat::Jet> (jet0, jet1 ) < TMath::Pi() / 2.0 ) {
    return;
  }

  double pt = jet0.pt();
  double area = jet0.jetArea();
  double mass = jet0.mass();
  double eta  = jet0.eta();
  double phi  = jet0.phi();

  if ( iEvent.isRealData() ) {    
    for ( std::vector<std::pair<unsigned int, unsigned int> >::const_iterator ifired = fired.begin(),
	    ifiredBegin = fired.begin(),
	    ifiredEnd = fired.end();
	  ifired != ifiredEnd; ++ifired ) {    
      dirs_.at( ifired->first ).getObject<TH1>( "jetArea"      )->Fill( area, weightMC * ifired->second );
      dirs_.at( ifired->first ).getObject<TH1>( "jetPt_L2L3"   )->Fill( pt, weightMC * ifired->second );
      dirs_.at( ifired->first ).getObject<TH1>( "jetPt_L1L2L3" )->Fill( pt - rho * area, weightMC * ifired->second );
      dirs_.at( ifired->first ).getObject<TH1>( "jetEta"       )->Fill( eta, weightMC * ifired->second );
      dirs_.at( ifired->first ).getObject<TH1>( "jetPhi"       )->Fill( phi, weightMC * ifired->second );
      dirs_.at( ifired->first ).getObject<TH1>( "jetMass"      )->Fill( mass, weightMC * ifired->second );
    }
  } else {
    double ptGen = 0.0;
    if ( useCA8GenJets_ ) {
      edm::Handle<std::vector<reco::GenJet> > h_genJets;
      iEvent.getByLabel( genJetsSrc_, h_genJets );
      
      for ( std::vector<reco::GenJet>::const_iterator igenBegin = h_genJets->begin(),
	      igenEnd = h_genJets->end(), igen = igenBegin;
	    igen != igenEnd; ++igen ) {
	if ( reco::deltaR<pat::Jet,reco::GenJet>( jet0, *igen ) < 0.8 ) {
	  ptGen = igen->pt();
	  break;
	}
      }
    } else {
      reco::GenJet const * igen = jet0.genJet();
      if ( igen > 0 )
	ptGen = jet0.genJet()->pt();
    }
    if ( ptGen > 0.0 ) {
      dirs_.back().getObject<TH1>( "jetArea"      )->Fill( area, weightMC );
      dirs_.back().getObject<TH1>( "jetPt_L2L3"   )->Fill( pt, weightMC );
      dirs_.back().getObject<TH1>( "jetPt_L1L2L3" )->Fill( pt - rho * area, weightMC );
      dirs_.back().getObject<TH1>( "jetEta"       )->Fill( eta, weightMC );
      dirs_.back().getObject<TH1>( "jetPhi"       )->Fill( phi, weightMC );
      dirs_.back().getObject<TH1>( "jetMass"      )->Fill( mass, weightMC );
      static_cast<TH2*>(dirs_.back().getObject<TH1>( "jetRes_L2L3"  ))->Fill( ptGen, pt/ptGen, weightMC );
      static_cast<TH2*>(dirs_.back().getObject<TH1>( "jetRes_L1L2L3"))->Fill( ptGen, (pt - rho*area)/ptGen, weightMC );
    }
  }

}
