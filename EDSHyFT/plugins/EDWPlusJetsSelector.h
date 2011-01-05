#ifndef EDWPlusJetsSelector_h
#define EDWPlusJetsSelector_h

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"

#include "PhysicsTools/UtilAlgos/interface/FWLiteFilterWrapper.h"
#include "Analysis/SHyFT/interface/SHyFTSelector.h"

class EDWPlusJetsSelector : public edm::FWLiteFilterWrapper<SHyFTSelector> {
 public:
 EDWPlusJetsSelector( const edm::ParameterSet & params ) :
  edm::FWLiteFilterWrapper<SHyFTSelector>( params )
    {
      produces< std::vector<pat::Jet> >      ("jets");
      produces< std::vector<pat::Muon> >     ("muons");
      produces< std::vector<pat::Electron> > ("electrons");
      produces< std::vector<pat::MET> >      ("mets");
    };
    
  virtual ~EDWPlusJetsSelector() {}
   
  /// Pass the event to the filter. NOTE! We can't use the eventSetup in FWLite so ignore it.
  virtual bool filter( edm::Event & event, const edm::EventSetup& eventSetup)
  {
    bool passed = edm::FWLiteFilterWrapper<SHyFTSelector>::filter( event, eventSetup );

    std::vector<reco::ShallowClonePtrCandidate> const & ijets = filter_->selectedJets();
    reco::ShallowClonePtrCandidate const &              iMET = filter_->selectedMET();
    std::vector<reco::ShallowClonePtrCandidate> const & imuons = filter_->selectedMuons();
    std::vector<reco::ShallowClonePtrCandidate> const & ielectrons = filter_->selectedElectrons();

    std::auto_ptr< std::vector<pat::Jet> > jets ( new std::vector<pat::Jet> );
    std::auto_ptr< std::vector<pat::MET> > METs ( new std::vector<pat::MET> );
    std::auto_ptr< std::vector<pat::Muon> > muons ( new std::vector<pat::Muon> );
    std::auto_ptr< std::vector<pat::Electron> > electrons ( new std::vector<pat::Electron> );

    typedef std::vector<reco::ShallowClonePtrCandidate>::const_iterator clone_iter;
    for ( clone_iter ibegin = ijets.begin(), iend = ijets.end(), i = ibegin;
	  i != iend; ++i ) {
      pat::Jet const * ijet = dynamic_cast<pat::Jet const *>( i->masterClonePtr().get() );
      jets->push_back( *ijet );
    }


    pat::MET const * met = dynamic_cast<pat::MET const *>( iMET.masterClonePtr().get() );
    METs->push_back( *met );



    for ( clone_iter jbegin = imuons.begin(), jend = imuons.end(), j = jbegin;
	  j != jend; ++j ) {
      pat::Muon const * jmuon = dynamic_cast<pat::Muon const *>( j->masterClonePtr().get() );
      muons->push_back( *jmuon );
    }


    for ( clone_iter jbegin = ielectrons.begin(), jend = ielectrons.end(), j = jbegin;
	  j != jend; ++j ) {
      pat::Electron const * jelectron = dynamic_cast<pat::Electron const *>( j->masterClonePtr().get() );
      electrons->push_back( *jelectron );
    }


    event.put( jets, "jets");
    event.put( METs, "mets");
    event.put( muons, "muons");
    event.put( electrons, "electrons");

    return passed; 
  }

  virtual void endJob() {
    filter_->print(std::cout);
  }
};



typedef edm::FWLiteFilterWrapper<SHyFTSelector> EDWPlusJetsSelectorBase;
DEFINE_FWK_MODULE(EDWPlusJetsSelectorBase);
DEFINE_FWK_MODULE(EDWPlusJetsSelector);

#endif
