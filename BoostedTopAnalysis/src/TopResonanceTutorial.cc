// -*- C++ -*-
//
// Package:    TopResonanceTutorial
// Class:      TopResonanceTutorial
// 
/**\class TopResonanceTutorial TopResonanceTutorial.cc Test/TopResonanceTutorial/src/TopResonanceTutorial.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  James Dolen
//         Created:  Tue Jan  1 19:41:41 CST 2013
// $Id$
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

#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/Vector.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CompositeCandidate.h"
     
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "Analysis/BoostedTopAnalysis/interface/SubjetHelper.h"
#include "AnalysisDataFormats/TopObjects/interface/CATopJetTagInfo.h"

#include <cmath>
#include <vector>
#include <list>
#include <Math/VectorUtil.h>


//
// class declaration
//

class TopResonanceTutorial : public edm::EDAnalyzer {
   public:
      explicit TopResonanceTutorial(const edm::ParameterSet&);
      ~TopResonanceTutorial();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      virtual void beginRun(edm::Run const&, edm::EventSetup const&);
      virtual void endRun(edm::Run const&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

      // ----------member data ---------------------------

      TH1F * CATop_mass;      
      TH1F * CATop_minmass;       
      TH1F * CATop_nsubjets;      
      TH1F * CATop_pt;        
      TH1F * CATop_eta;         
      TH1F * CATop_rapidity;      
      TH1F * CATop_dijet_mass;    
      TH1F * Type11_mass;       
      TH1F * PrunedJet_mass;      
      TH1F * PrunedJet_pt;      
      TH1F * PrunedJet_eta;       
      TH1F * PrunedJet_rapidity;    
      TH1F * PrunedJet_dijet_mass;    
      TH1F * PrunedJet_mu;      
      TH1F * PrunedJet_y ;      
      TH1F * PrunedJet_dR;        
      TH1F * Type12_mass;       
};



//
// constructors and destructor
//
TopResonanceTutorial::TopResonanceTutorial(const edm::ParameterSet& iConfig)
{
  edm::Service<TFileService> fs;

  // pretagged CATop histograms
  CATop_mass          = fs->make<TH1F>("CATop_mass",        "CATop_mass",       100,  0,  400 );
  CATop_minmass       = fs->make<TH1F>("CATop_minmass",     "CATop_minmass",      100,  0,  200 );
  CATop_nsubjets      = fs->make<TH1F>("CATop_nsubjets",      "CATop_nsubjets",     5,    0,  5 );
  CATop_pt            = fs->make<TH1F>("CATop_pt",        "CATop_pt",         100,  0,  4000 );
  CATop_eta           = fs->make<TH1F>("CATop_eta",       "CATop_eta",        100,  -3, 3 );  
  CATop_rapidity      = fs->make<TH1F>("CATop_rapidity",      "CATop_rapidity",     100,  -3, 3 );  
  CATop_dijet_mass    = fs->make<TH1F>("CATop_dijet_mass",    "CATop_dijet_mass",     100,  0,  4000 ); 

  // Type11 histograms
  Type11_mass       = fs->make<TH1F>("Type11_mass",   "measured t#bar{t} Inv Mass Type11",   500,  0,  5000 );

  // pretagged pruned jet histograms
  PrunedJet_mass        = fs->make<TH1F>("PrunedJet_mass",        "PrunedJet_mass",       100,  0,  400 );
  PrunedJet_pt          = fs->make<TH1F>("PrunedJet_pt",        "PrunedJet_pt",         100,  0,  4000 );
  PrunedJet_eta         = fs->make<TH1F>("PrunedJet_eta",       "PrunedJet_eta",        100,  -3, 3 );  
  PrunedJet_rapidity    = fs->make<TH1F>("PrunedJet_rapidity",      "PrunedJet_rapidity",     100,  -3, 3 );  
  PrunedJet_dijet_mass  = fs->make<TH1F>("PrunedJet_dijet_mass",    "PrunedJet_dijet_mass",     100,  0,  4000 ); 
  PrunedJet_mu          = fs->make<TH1F>("PrunedJet_mu",        "PrunedJet_mu",         100,  0,  1 );  
  PrunedJet_y           = fs->make<TH1F>("PrunedJet_y",         "PrunedJet_y",          100,  0,  1 );  
  PrunedJet_dR          = fs->make<TH1F>("PrunedJet_dR",        "PrunedJet_dR",         100,  0,  1 );  

  // Type12 histograms  
  Type12_mass       = fs->make<TH1F>("Type12_mass",   "measured t#bar{t} Inv Mass Type12",   500,  0,  5000 );
}


TopResonanceTutorial::~TopResonanceTutorial()
{
}


//
// member functions
//

// ------------ method called for each event  ------------
void
TopResonanceTutorial::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;
  using namespace std;
  
  bool verbose = false;

  //-----------------------------------------------------
  //-- CATop jet loop
  //-----------------------------------------------------

  edm::Handle<std::vector<pat::Jet> > h_topTag;
  iEvent.getByLabel( "goodPatJetsCATopTagPF", h_topTag );


  math::XYZTLorentzVector leading_jet;
  math::XYZTLorentzVector pair_sum_p4;
  math::XYZTLorentzVector tagged_pair_sum_p4;
  int count_tagged = 0;

  // Example - loop over all jets in collection
  int jet_number = 0;
  for ( std::vector<pat::Jet>::const_iterator jetBegin = h_topTag->begin(),
      jetEnd = h_topTag->end(), ijet = jetBegin; ijet != jetEnd; ++ijet ) {

    const reco::CATopJetTagInfo * catopTag = dynamic_cast<reco::CATopJetTagInfo const *>(ijet->tagInfo("CATop"));

    double pt       = ijet->pt();
    double eta      = ijet->eta();
    double rapidity = ijet->rapidity();
    double mass     = ijet->mass();
    double minmass  = catopTag->properties().minMass;
    double topmass  = catopTag->properties().topMass;
    int nsubjets    = ijet->numberOfDaughters();

    if (verbose) cout<<"pt "<<pt<<" mass "<<mass<<" topmass "<<topmass<<" minmass "<<minmass<<" nsubjets "<<nsubjets<<endl;
    
    if (pt>350){

      if (jet_number<1){
        leading_jet = ijet->p4();
      }

      if (jet_number<2){

        pair_sum_p4 += ijet->p4();
        CATop_mass    ->Fill( mass );
        CATop_minmass ->Fill( minmass );
        CATop_nsubjets  ->Fill( nsubjets );
        CATop_pt    ->Fill( pt );
        CATop_eta   ->Fill( eta );
        CATop_rapidity  ->Fill( rapidity );


        if (  mass>140 && mass<250 && minmass>50 && nsubjets>2)
        {   

          tagged_pair_sum_p4 += ijet->p4();
          count_tagged++;

        }
      }
      jet_number++;
    }
  }
  if (jet_number>=2)
  {
    if (verbose) cout<<"pair mass"<<pair_sum_p4.M()<<endl;
    CATop_dijet_mass    ->Fill( pair_sum_p4.M() );
    if (count_tagged==2){
      if (verbose) cout<<"tagged pair mass"<<tagged_pair_sum_p4.M()<<endl;
      Type11_mass   ->Fill( tagged_pair_sum_p4.M() );
    }
  }

  //-----------------------------------------------------
  //-- Pruned jet loop
  //-----------------------------------------------------
  edm::Handle<std::vector<pat::Jet> > h_wTag;
  iEvent.getByLabel( "goodPatJetsCATopTagPF", h_wTag );

  math::XYZTLorentzVector pruned_pair_sum_p4;
  int pruned_jet_number=0;

  std::vector<edm::Ptr<pat::Jet> >  wTags1;
  std::vector<edm::Ptr<pat::Jet> >  noTags1;

  for ( std::vector<pat::Jet>::const_iterator jetBegin = h_wTag->begin(), jetEnd = h_wTag->end(), ijet = jetBegin; ijet != jetEnd; ++ijet ) {
      
    double pt     = ijet->pt();
    double eta    = ijet->eta();
    double rapidity = ijet->rapidity();
    double mass   = ijet->mass();
    double btagDiscriminator = ijet->bDiscriminator("combinedSecondaryVertexMVABJetTags");
    double nsubjets = ijet->numberOfDaughters();
      
    if ( pt>250){   
      pruned_pair_sum_p4 += ijet->p4();
      pruned_jet_number++;

      if (nsubjets>=2){

        reco::Candidate::PolarLorentzVector subjet0 = ijet->daughter(0)->polarP4();
        reco::Candidate::PolarLorentzVector subjet1 = ijet->daughter(1)->polarP4();
        
        /////////////////
        // use subjet helper to caculate W tagging variables

        double y = -1.0;   
        double mu = -1.0; //mass drop = leading subjet mass / jet mass
        double dR = -1.0;
        pat::subjetHelper( subjet0, subjet1, y, mu, dR, mass );


        /////////////////
        // do it another way...calculate W tagging variabels by hand

        double mu2 = subjet0.mass()/ijet->mass();

        /////////////////
        // fill some histograms

        PrunedJet_mass      ->Fill( mass );
        PrunedJet_pt        ->Fill( pt );
        PrunedJet_eta       ->Fill( eta );
        PrunedJet_rapidity  ->Fill( rapidity );
        PrunedJet_mu        ->Fill( mu );
        PrunedJet_dR        ->Fill( dR );
        PrunedJet_y         ->Fill( y );

        if (verbose) cout<<"pruned jet  pt "<<pt<<" mass "<<mass<<" btagDiscriminator "<< btagDiscriminator<<" y "<<y<<" dR "<< dR<<" mu "<<mu<<" mu2 "<<mu2<<endl;

        /////////////////
        // find tagged and untagged jets in hemisphere opposite leading jet 

        double deltaR_LJ_PrunedJet = deltaR( leading_jet.eta(), leading_jet.phi(), ijet->eta(), ijet->phi() );
/*
        if (mass>60 && mass<100 && mu>0.4){
          wTags1.push_back( *ijet );
        }
        else{
          noTags1.push_back( *ijet );
        }
*/

        }
      }
    }

  if (pruned_jet_number>=2)
  {
    if (verbose) cout<<"pruned pair mass"<<pruned_pair_sum_p4.M()<<endl;
    PrunedJet_dijet_mass->Fill( pruned_pair_sum_p4.M() );
  }
}


// ------------ method called once each job just before starting event loop  ------------
void 
TopResonanceTutorial::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
TopResonanceTutorial::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
void 
TopResonanceTutorial::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
TopResonanceTutorial::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
TopResonanceTutorial::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
TopResonanceTutorial::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
TopResonanceTutorial::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(TopResonanceTutorial);
