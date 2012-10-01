#ifndef BoostedParticles_h
#define BoostedParticles_h

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include <vector>

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Particle.h"

typedef reco::Candidate::PolarLorentzVector LorentzV;

class BoostedParticles : public edm::EDProducer {
   public:
      explicit BoostedParticles(const edm::ParameterSet& cfg);
      ~BoostedParticles();
   private:
      virtual void beginJob(const edm::EventSetup&) ;
      virtual void produce(edm::Event& event, const edm::EventSetup& setup);
      virtual void endJob() ;
      void BBtotWtW(const reco::Candidate* bprimes, bool hasLepWt, bool hasHadWt,
                    LorentzV& Lep, LorentzV& Nu, LorentzV& LepT, 
                    LorentzV& HadT, LorentzV& WPart1, LorentzV& WPart2,
                    LorentzV& HadTtoW, LorentzV& HadTtob, LorentzV& LepTtoW, LorentzV& LepTtob);

      // ----------member data ---------------------------
   protected:

};

#endif

BoostedParticles::BoostedParticles(const edm::ParameterSet& cfg)
{  
   produces<reco::Candidate::PolarLorentzVector> ("Lep");
   produces<reco::Candidate::PolarLorentzVector> ("Nu");
   produces<reco::Candidate::PolarLorentzVector> ("LepT");
   produces<reco::Candidate::PolarLorentzVector> ("HadT");
   produces<reco::Candidate::PolarLorentzVector> ("WPart1");
   produces<reco::Candidate::PolarLorentzVector> ("WPart2"); 

   produces<reco::Candidate::PolarLorentzVector> ("HadTtoW");
   produces<reco::Candidate::PolarLorentzVector> ("HadTtob");
   produces<reco::Candidate::PolarLorentzVector> ("LepTtoW");
   produces<reco::Candidate::PolarLorentzVector> ("LepTtob");    
}

BoostedParticles::~BoostedParticles()
{
}

// ------------ method called once each job just before starting event loop  ------------
void BoostedParticles::beginJob(const edm::EventSetup&)
{
}

// ------------ method called once each job just after ending the event loop  ------------
void BoostedParticles::endJob() {
 std::cout << "----------------------------------------------------------------------------------------" << std::endl;
 std::cout << "So long, and thanks for all the fish..." << std::endl;
 std::cout << "----------------------------------------------------------------------------------------" << std::endl;
}
