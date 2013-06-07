#include "Analysis/EDSHyFT/plugins/EDSHyFTSelector.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "EGamma/EGammaAnalysisTools/interface/ElectronEffectiveArea.h"

using namespace std;

bool EDSHyFTSelector::filter( edm::Event & event, const edm::EventSetup& eventSetup )
{
    bool passed = edm::FilterWrapper<SHyFTSelector>::filter( event, eventSetup );

    std::auto_ptr< LorentzV > top1   ( new LorentzV() );
    std::auto_ptr< LorentzV > top2   ( new LorentzV() );

    std::vector<reco::ShallowClonePtrCandidate> const & ijets = filter_->cleanedJets();
    reco::ShallowClonePtrCandidate const & imet = filter_->selectedMET();
    std::vector<reco::ShallowClonePtrCandidate> const & imuons = filter_->selectedMuons();
    std::vector<reco::ShallowClonePtrCandidate> const & ielectrons = filter_->selectedElectrons();
    std::auto_ptr< std::vector<pat::Jet> > jets ( new std::vector<pat::Jet> );
    std::auto_ptr< std::vector<pat::MET> > mets ( new std::vector<pat::MET> );
    std::auto_ptr< std::vector<pat::Muon> > muons ( new std::vector<pat::Muon> );
    std::auto_ptr< std::vector<pat::Electron> > electrons ( new std::vector<pat::Electron> );
    
    pat::MET const * patmet = dynamic_cast<pat::MET const *>( imet.masterClonePtr().get() ); 
    if ( patmet != 0 ){  
        mets->push_back( *patmet );
        mets->back().setP4( imet.p4() );//set back the P4 to the clonned met
    }

    typedef std::vector<reco::ShallowClonePtrCandidate>::const_iterator clone_iter;

   
    std::vector<const reco::GenParticle *> top(2);

    if(!event.isRealData()){
       edm::Handle<std::vector<reco::GenParticle> > h_gen;
       event.getByLabel(edm::InputTag("prunedGenParticles"), h_gen); 
       assert ( h_gen.isValid() );

       int numDa; int id(0);

       for (vector< reco::GenParticle>::const_iterator gpIter = h_gen->begin(); 
            gpIter != h_gen->end(); ++gpIter, ++id){
          
          if( gpIter->status() !=3) continue;
          numDa = gpIter->numberOfDaughters();
          
          if(numDa >= 2){
             if(gpIter->pdgId() == 6) {top[0] = (&(*gpIter));}
             else if (gpIter->pdgId() == -6) {top[1] = (&(*gpIter));}
          }

       }
    }
    if (top[0] != 0) {*top1 = top[0]->p4();}
    if (top[1] != 0) {*top2 = top[1]->p4();}

    if ( matchByHand_ && !event.isRealData() ) {
        edm::Handle<std::vector<reco::GenJet> > h_genJets;
        event.getByLabel("ca8GenJetsNoNu", h_genJets);
        for ( clone_iter ibegin = ijets.begin(), iend = ijets.end(), i = ibegin;i != iend; ++i ) {
            pat::Jet const * ijet = dynamic_cast<pat::Jet const *>( i->masterClonePtr().get() );
            if ( ijet != 0 ) {
                int matched = 0;
                jets->push_back( *ijet );
                jets->back().setP4( i->p4() );//set back the P4 to the clonned jet
                jets->back().addUserInt("matched",matched);

                //Find matching genJet for systematic smearing
                float minDR = 9.9;
                float dR = 10.;
                reco::GenJet theMatchingGenJet; 
                for ( std::vector<reco::GenJet>::const_iterator genJBegin = h_genJets->begin(), genJEnd = h_genJets->end(), igenjet = genJBegin; igenjet != genJEnd; ++igenjet ) {
                    dR = reco::deltaR<double>( ijet->eta(), ijet->phi(), igenjet->eta(), igenjet->phi() );
                    if ( dR < minDR ) {
                        theMatchingGenJet = (*igenjet);
                        minDR = dR;
                        matched = 1;
                    }       
                }
                if ( matched == 1 ) {
                    jets->back().addUserFloat("genJetPt",theMatchingGenJet.pt());
                    jets->back().addUserFloat("genJetPhi", theMatchingGenJet.phi());
                    jets->back().addUserFloat("genJetEta", theMatchingGenJet.eta());
                    jets->back().addUserFloat("genJetMass", theMatchingGenJet.mass());
                } else {
                    jets->back().addUserFloat("genJetPt", -10);
                    jets->back().addUserFloat("genJetPhi", -10);
                    jets->back().addUserFloat("genJetEta", -10);
                    jets->back().addUserFloat("genJetMass", -10);
                }
            }
        }   
    } else {
        for ( clone_iter ibegin = ijets.begin(), iend = ijets.end(), i = ibegin; i != iend; ++i ) {
            pat::Jet const * ijet = dynamic_cast<pat::Jet const *>( i->masterClonePtr().get() );
            if ( ijet != 0 ){
                int matched = 0; 
                if ( ijet->genJet() ) matched=1;
                jets->push_back( *ijet );
                jets->back().setP4( i->p4() );//set back the P4 to the clonned jet
                jets->back().addUserInt("matched",matched);
                if ( matched == 1 ) { 
                    jets->back().addUserFloat("genJetPt",ijet->genJet()->pt());
                    jets->back().addUserFloat("genJetPhi", ijet->genJet()->phi());
                    jets->back().addUserFloat("genJetEta", ijet->genJet()->eta());
                    jets->back().addUserFloat("genJetMass", ijet->genJet()->mass());
                }else{
                    jets->back().addUserFloat("genJetPt", -10);
                    jets->back().addUserFloat("genJetPhi", -10);
                    jets->back().addUserFloat("genJetEta", -10);
                    jets->back().addUserFloat("genJetMass", -10);
                }
            }
        }
    }
    for ( clone_iter jbegin = imuons.begin(), jend = imuons.end(), j = jbegin; j != jend; ++j ) {
        pat::Muon const * jmuon = dynamic_cast<pat::Muon const *>( j->masterClonePtr().get() );
        if ( jmuon != 0 )
            muons->push_back( *jmuon );
    }

    for ( clone_iter jbegin = ielectrons.begin(), jend = ielectrons.end(), j = jbegin; j != jend; ++j ) {
        pat::Electron const * jelectron = dynamic_cast<pat::Electron const *>( j->masterClonePtr().get() );
        if ( jelectron != 0 ){

           double scEta  = jelectron->superCluster()->eta();
           double  AEff  = 0;
           //if(useData_){
           AEff    = ElectronEffectiveArea::GetElectronEffectiveArea(ElectronEffectiveArea::kEleGammaAndNeutralHadronIso03, scEta, ElectronEffectiveArea::kEleEAData2012);
           //}else{
           //   AEff    = ElectronEffectiveArea::GetElectronEffectiveArea(ElectronEffectiveArea::kEleGammaAndNeutralHadronIso03, scEta, ElectronEffectiveArea::kEleEAFall11MC);
           // }
           electrons->push_back( *jelectron );
           electrons->back().addUserFloat("AEff", AEff);        
        }
    }

   event.put( top1, "top1"); 
   event.put( top2, "top2"); 
   event.put( jets, "jets");
   event.put( mets, "MET");
   event.put( muons, "muons");
   event.put( electrons, "electrons");
   return passed; 
}


typedef edm::FilterWrapper<SHyFTSelector> EDSHyFTSelectorBase;
DEFINE_FWK_MODULE(EDSHyFTSelectorBase);
DEFINE_FWK_MODULE(EDSHyFTSelector);
