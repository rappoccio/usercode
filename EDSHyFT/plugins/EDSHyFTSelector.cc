#include "Analysis/EDSHyFT/plugins/EDSHyFTSelector.h"
#include "FWCore/Framework/interface/MakerMacros.h"

bool EDSHyFTSelector::filter( edm::Event & event, const edm::EventSetup& eventSetup)
{
  bool passed = edm::FilterWrapper<SHyFTSelector>::filter( event, eventSetup );

  std::vector<reco::ShallowClonePtrCandidate> const & ijets = filter_->cleanedJets();
  reco::ShallowClonePtrCandidate const & imet = filter_->selectedMET();
  std::vector<reco::ShallowClonePtrCandidate> const & imuons = filter_->selectedMuons();
  std::vector<reco::ShallowClonePtrCandidate> const & ielectrons = filter_->selectedElectrons();

  std::auto_ptr< std::vector<pat::Jet> > jets ( new std::vector<pat::Jet> );
  std::auto_ptr< std::vector<pat::MET> > mets ( new std::vector<pat::MET> );
  std::auto_ptr< std::vector<pat::Muon> > muons ( new std::vector<pat::Muon> );
  std::auto_ptr< std::vector<pat::Electron> > electrons ( new std::vector<pat::Electron> );

  mets->push_back( *(dynamic_cast<pat::MET const *>( imet.masterClonePtr().get() )) );
  
  typedef std::vector<reco::ShallowClonePtrCandidate>::const_iterator clone_iter;
  for ( clone_iter ibegin = ijets.begin(), iend = ijets.end(), i = ibegin;
	i != iend; ++i ) {
    pat::Jet const * ijet = dynamic_cast<pat::Jet const *>( i->masterClonePtr().get() );
    if ( ijet != 0 ){
      int matched = 0;
      if(ijet->genJet()) matched=1;
      jets->push_back( *ijet );
      jets->back().addUserInt("matched",matched);
    }
  }


  for ( clone_iter jbegin = imuons.begin(), jend = imuons.end(), j = jbegin;
	j != jend; ++j ) {
    pat::Muon const * jmuon = dynamic_cast<pat::Muon const *>( j->masterClonePtr().get() );
    if ( jmuon != 0 )
      muons->push_back( *jmuon );
  }


  for ( clone_iter jbegin = ielectrons.begin(), jend = ielectrons.end(), j = jbegin;
	j != jend; ++j ) {
    pat::Electron const * jelectron = dynamic_cast<pat::Electron const *>( j->masterClonePtr().get() );
    if ( jelectron != 0 )
      electrons->push_back( *jelectron );
  }


  event.put( jets, "jets");
  event.put( mets, "MET");
  event.put( muons, "muons");
  event.put( electrons, "electrons");

  return passed; 
}


typedef edm::FilterWrapper<SHyFTSelector> EDSHyFTSelectorBase;
DEFINE_FWK_MODULE(EDSHyFTSelectorBase);
DEFINE_FWK_MODULE(EDSHyFTSelector);
