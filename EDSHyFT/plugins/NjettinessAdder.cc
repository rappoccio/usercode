#include "Analysis/EDSHyFT/plugins/NjettinessAdder.h"
#include "Analysis/EDSHyFT/interface/Njettiness.hh"
//#include "ExoDiBosonResonances/PATtupleProduction/interface/Njettiness.hh"
//#include "/uscms_data/d3/yongjie/8TeV/PATtoEDM/Andreas/CMSSW_5_3_2_patch2/src/ExoDiBosonReosnances/PATtupleProduction/interface/Njettiness.hh"
#include "FWCore/Framework/interface/MakerMacros.h"


#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/TriggerPath.h"
#include "PhysicsTools/SelectorUtils/interface/PFJetIDSelectionFunctor.h"
#include "Analysis/BoostedTopAnalysis/interface/SubjetHelper.h"
#include "AnalysisDataFormats/TopObjects/interface/CATopJetTagInfo.h"
#include "Analysis/BoostedTopAnalysis/interface/CATopTagFunctor.h"
#include "Analysis/BoostedTopAnalysis/interface/BoostedTopWTagFunctor.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h" 
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "DataFormats/PatCandidates/interface/MET.h"


void NjettinessAdder::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {
  // read input collection
    edm::Handle<edm::View<pat::Jet> > jets;
    //edm::Handle<edm::View<reco::PFCandidate>> jets;
    iEvent.getByLabel(src_, jets);
  typedef reco::Candidate::PolarLorentzVector LorentzV;
  typedef std::vector<reco::Candidate::PolarLorentzVector> p4_vector;
  std::auto_ptr<p4_vector> CA8P4( new p4_vector() );
  std::auto_ptr<std::vector<double> > Tau1 ( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > Tau2 ( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > Tau3 ( new std::vector<double>() );



  // prepare room for output
 // std::vector<pat::Jet> outJets;   outJets.reserve(jets->size());

  for ( typename edm::View<pat::Jet>::const_iterator jetIt = jets->begin() ; jetIt != jets->end() ; ++jetIt ) {
	if(jetIt->pt()>150.0)
		{
    		pat::Jet newCand(*jetIt);
    		edm::Ptr<pat::Jet> jetPtr = jets->ptrAt(jetIt - jets->begin());
    		Tau1->push_back( getTau(1, jetPtr ) );
    		Tau2->push_back( getTau(2, jetPtr ) );
    		Tau3->push_back( getTau(3, jetPtr ) );
    		//newCand.addUserFloat("tau2", getTau(2, jetPtr ) );
    		//newCand.addUserFloat("tau3", getTau(3, jetPtr ) );
    		reco::Candidate::PolarLorentzVector TJet(jetIt->pt(), jetIt->eta(), jetIt->phi(), jetIt->mass());
    		CA8P4->push_back( TJet );



		}	
  }


 // std::auto_ptr<std::vector<pat::Jet> > out(new std::vector<pat::Jet>(outJets));
  iEvent.put(CA8P4      ,"CA8P4");  
  iEvent.put(Tau3     ,"Tau3");  
  iEvent.put(Tau2     ,"Tau2");  
  iEvent.put(Tau1     ,"Tau1");  


  //iEvent.put(out);
 
}

float NjettinessAdder::getTau(int num, edm::Ptr<pat::Jet> object) const
{
  std::vector<const reco::PFCandidate*> all_particles;
  if(object->isPFJet())
    {
      for (unsigned k =0; k < object->getPFConstituents().size(); k++)
	all_particles.push_back( object->getPFConstituent(k).get() );
    } else {
    for (unsigned j = 0; j < object->numberOfDaughters(); j++){
      reco::PFJet const *pfSubjet = dynamic_cast <const reco::PFJet *>(object->daughter(j));
      if (!pfSubjet) break;
          for (unsigned k =0; k < pfSubjet->getPFConstituents().size(); k++)
	    all_particles.push_back( pfSubjet->getPFConstituent(k).get() );	
    }
  }
  std::vector<fastjet::PseudoJet> FJparticles;
  for (unsigned particle = 0; particle < all_particles.size(); particle++){
    const reco::PFCandidate *thisParticle = all_particles.at(particle);
    FJparticles.push_back( fastjet::PseudoJet( thisParticle->px(), thisParticle->py(), thisParticle->pz(), thisParticle->energy() ) );	
  }
  NsubParameters paraNsub = NsubParameters(1.0, cone_); //assume R=0.7 jet clusering used
  Njettiness routine(Njettiness::onepass_kt_axes, paraNsub);
  return routine.getTau(num, FJparticles); 
}



DEFINE_FWK_MODULE(NjettinessAdder);
