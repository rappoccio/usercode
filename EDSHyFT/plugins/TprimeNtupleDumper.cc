#ifndef TprimeNtupleDumper_h
#define TprimeNtupleDumper_h

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include <vector>

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Particle.h"

class TprimeNtupleDumper : public edm::EDProducer {
public:
  explicit TprimeNtupleDumper(const edm::ParameterSet& cfg);
  ~TprimeNtupleDumper();
  
private:
  virtual void beginJob(const edm::EventSetup&) ;
  virtual void produce(edm::Event& event, const edm::EventSetup& setup);
  virtual void endJob() ;
  
};

#endif

TprimeNtupleDumper::~TprimeNtupleDumper(){
}

void TprimeNtupleDumper::beginJob(const edm::EventSetup&){
}

void TprimeNtupleDumper::endJob(){
}

TprimeNtupleDumper::TprimeNtupleDumper(const edm::ParameterSet& cfg){
  produces<double>("fitMass");
  produces<double>("TTMass");
  produces<double>("fitChi2");
  produces<int>("nJets");
  
}

void TprimeNtupleDumper::produce(edm::Event& event, const edm::EventSetup& setup){
  std::auto_ptr<double> pfitMass ( new double(0.0) );
  std::auto_ptr<double> pTTMass  ( new double(0.0) );
  std::auto_ptr<double> pfitChi2 ( new double(-1.0) );
  std::auto_ptr<int>    pnJets   ( new int(-1) );
  
  std::string label="pfShyftSkim";
  label+=":jets";
  // get the jet collection
  edm::Handle<std::vector<pat::Jet> > jets;
  event.getByLabel(edm::InputTag(label), jets);
  // save number of jets is a naive way
  *pnJets = jets->size();

  // extract and save fit mass and chi^2
  label="kinFitTtSemiLepEvent";
  edm::Handle<std::vector<pat::Particle> > fitLeptons;
  event.getByLabel(edm::InputTag(label+":Leptons"), fitLeptons);

  edm::Handle<std::vector<pat::Particle> > fitNeutrinos;
  event.getByLabel(edm::InputTag(label+":Neutrinos"), fitNeutrinos);

  edm::Handle<std::vector<pat::Particle> > fitPartonsHadB;
  event.getByLabel(edm::InputTag(label+":PartonsHadB"), fitPartonsHadB);

  edm::Handle<std::vector<pat::Particle> > fitPartonsHadP;
  event.getByLabel(edm::InputTag(label+":PartonsHadP"), fitPartonsHadP);
  
  edm::Handle<std::vector<pat::Particle> > fitPartonsHadQ;
  event.getByLabel(edm::InputTag(label+":PartonsHadQ"), fitPartonsHadQ);

  edm::Handle<std::vector<pat::Particle> > fitPartonsLepB;
  event.getByLabel(edm::InputTag(label+":PartonsLepB"), fitPartonsLepB);
  
  edm::Handle<std::vector<double> > fitChi2;
  event.getByLabel(edm::InputTag(label+":Chi2"), fitChi2);

  // make a very simple solution - take the best Chi2 combination only
  for(size_t i=0; i<(fitChi2->size()); i++){
    std::cout << "i = " << i << "   Chi2 = " << (fitChi2->at(i)) << "   Neutrino pz = " << fitNeutrinos->at(i).pz() << std::endl;
    if(fitChi2->at(i)>=0){
      *pfitChi2 = fitChi2->at(i);

      reco::Candidate::LorentzVector vect4 = fitPartonsHadP->at(i).p4();
      vect4 += fitPartonsHadQ->at(i).p4();
      vect4 += fitPartonsLepB->at(i).p4();
      
      *pfitMass = vect4.M();

      vect4 += fitLeptons->at(i).p4();
      vect4 += fitNeutrinos->at(i).p4();
      vect4 += fitPartonsLepB->at(i).p4();

      *pTTMass = vect4.M();
      
      std::cout << "   fitMass = " << *pfitMass << "   TTmass = " << *pTTMass << std::endl;
      break;    
    }
  }
  
  
  event.put(pfitMass, "fitMass");
  event.put(pTTMass,  "TTMass");
  event.put(pfitChi2, "fitChi2");
  event.put(pnJets,   "nJets");
  return;
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(TprimeNtupleDumper);
