#ifndef BoostedSusy_h
#define BoostedSusy_h

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
typedef std::vector< LorentzV > p4_vector;

class BoostedSusy : public edm::EDProducer {
   public:
      explicit BoostedSusy(const edm::ParameterSet& cfg);
      ~BoostedSusy();
   private:
      virtual void beginJob(const edm::EventSetup&) ;
      virtual void produce(edm::Event& event, const edm::EventSetup& setup);
      virtual void endJob() ;    
      void topDecay (const reco::Candidate* top, int TopDau, const reco::Candidate* &WtoLep, const reco::Candidate* &WtoHad,
                     const reco::Candidate* &TtoWtoLep1, const reco::Candidate* &TtoWtoLep2,
                     const reco::Candidate* &TtoWtoHad1, const reco::Candidate* &TtoWtoHad2,
                     const reco::Candidate* &Ttob); 
      void setPointers(std::vector<const reco::Candidate *> decayList);

      // ----------member data ---------------------------
   protected:
      
};

#endif

BoostedSusy::BoostedSusy(const edm::ParameterSet& cfg)
{  
   //register the products

   
   //~g -> ~t_1 t, ~t_1 -> chi0 t
   //=============================
   // Stop products
   // ---------------
   produces< LorentzV > ("chi0G1");
   produces< LorentzV > ("chi0G2");
   produces< LorentzV > ("topStop1");
   produces< LorentzV > ("topStop2");
   produces< LorentzV > ("bStop1");
   produces< LorentzV > ("bStop2");
   produces< LorentzV > ("WtoLepStop1");
   produces< LorentzV > ("WtoLepStop2");
   produces< LorentzV > ("Lep1Stop1");
   produces< LorentzV > ("Lep2Stop1");
   produces< LorentzV > ("Lep1Stop2");
   produces< LorentzV > ("Lep2Stop2");
   produces< LorentzV > ("WtoHadStop1");
   produces< LorentzV > ("WtoHadStop2");
   produces< LorentzV > ("Had1Stop1");
   produces< LorentzV > ("Had2Stop1");
   produces< LorentzV > ("Had1Stop2");
   produces< LorentzV > ("Had2Stop2");

   // top products
   // -------------
   produces< LorentzV > ("topG1");
   produces< LorentzV > ("topG2");
   produces< LorentzV > ("bG1");
   produces< LorentzV > ("bG2");
   produces< LorentzV > ("WtoLepG1");
   produces< LorentzV > ("WtoLepG2");
   produces< LorentzV > ("Lep1G1");
   produces< LorentzV > ("Lep1G2");
   produces< LorentzV > ("Lep2G1");
   produces< LorentzV > ("Lep2G2");
   produces< LorentzV > ("WtoHadG1");
   produces< LorentzV > ("WtoHadG2");
   produces< LorentzV > ("Had1G1");
   produces< LorentzV > ("Had1G2");
   produces< LorentzV > ("Had2G1");
   produces< LorentzV > ("Had2G2");
}


BoostedSusy::~BoostedSusy()
{
}

// ------------ method called once each job just before starting event loop  ------------
void BoostedSusy::beginJob(const edm::EventSetup&)
{
}

// ------------ method called once each job just after ending the event loop  ------------
void BoostedSusy::endJob() {
 std::cout << "----------------------------------------------------------------------------------------" << std::endl;
 std::cout << "So long, and thanks for all the fish..." << std::endl;
 std::cout << "----------------------------------------------------------------------------------------" << std::endl;
}
