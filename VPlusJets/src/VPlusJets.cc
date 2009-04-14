#include "Analysis/VPlusJets/interface/VPlusJets.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"


#include "FWCore/Utilities/interface/Exception.h"

#include <vector>

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
VPlusJets::VPlusJets(const edm::ParameterSet& iConfig) : 
  makeMuons_     ( iConfig.getParameter<bool>("makeMuons") ),
  makeElectrons_ ( iConfig.getParameter<bool>("makeElectrons") )
{
  // If desired, get muons
  if ( makeMuons_ ) {

    // Check for muon source... if it doesn't exist, throw exception
    muonSrc_ = iConfig.getParameter<edm::InputTag> ("muonSrc");

    // Now get the cuts... if they don't exist, throw exception
    chi2CutMuon_   = iConfig.getParameter<double>("chi2CutMuon");
    d0CutMuon_     = iConfig.getParameter<double>("d0CutMuon");
    nHitsCutMuon_  = iConfig.getParameter<unsigned int>("nHitsCutMuon");
    hcalEtCutMuon_ = iConfig.getParameter<double>("hcalEtCutMuon");
    ecalEtCutMuon_ = iConfig.getParameter<double>("ecalEtCutMuon");
    relIsoCutMuon_ = iConfig.getParameter<double>("relIsoCutMuon");

    // Check for min muon cut... if it doesn't exist, set to default (off)
    if ( iConfig.exists("minMuons") )
      minMuons_ = iConfig.getParameter<unsigned int>("minMuons");
    else 
      minMuons_ = 0;

    // Check for max muon cut... if it doesn't exist, set to default (off)
    if ( iConfig.exists("maxMuons") )
      maxMuons_ = iConfig.getParameter<unsigned int>("maxMuons");
    else 
      maxMuons_ = 9999;

  }


  // If desired, get electrons
  if ( makeElectrons_ ) {

    // Check for electron source... if it doesn't exist, throw exception
    electronSrc_ = iConfig.getParameter<edm::InputTag> ("electronSrc");

    // Now get the cuts... if they don't exist, throw exception
    d0CutElectron_     = iConfig.getParameter<double>("d0CutElectron");
    relIsoCutElectron_ = iConfig.getParameter<double>("relIsoCutElectron");

    // Check for min electron cut... if it doesn't exist, set to default (off)
    if ( iConfig.exists("minElectrons") )
      minElectrons_ = iConfig.getParameter<unsigned int>("minElectrons");
    else 
      minElectrons_ = 0;

    // Check for max electron cut... if it doesn't exist, set to default (off)
    if ( iConfig.exists("maxElectrons") )
      maxElectrons_ = iConfig.getParameter<unsigned int>("maxElectrons");
    else 
      maxElectrons_ = 9999;
    
  }


  produces<std::vector<pat::Muon> > ();
  produces<std::vector<pat::Electron> > ();
}


VPlusJets::~VPlusJets()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called on each new Event  ------------
bool
VPlusJets::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{

  // Get handle for output collections
  std::auto_ptr< std::vector<pat::Muon> >     p_muons    ( new std::vector<pat::Muon>     () ) ;
  std::auto_ptr< std::vector<pat::Electron> > p_electrons( new std::vector<pat::Electron> () ) ;

  // Get the beamspot
  reco::BeamSpot beamSpot;
  edm::Handle<reco::BeamSpot> beamSpotHandle;
  iEvent.getByLabel("offlineBeamSpot", beamSpotHandle);

  if ( beamSpotHandle.isValid() ){
    beamSpot = *beamSpotHandle;
  } else{
    edm::LogError("VPlusJets")
      << "No beam spot available from EventSetup \n";
    return false;
  }
  
  double x0 = beamSpot.x0();
  double y0 = beamSpot.y0();
  double z0 = beamSpot.z0();

  reco::TrackBase::Point beamPoint( x0, y0, z0 );

  
  if ( makeMuons_ ) {
    // get handle for input muon collection
    edm::Handle< std::vector<pat::Muon> > h_muons;
    iEvent.getByLabel( muonSrc_, h_muons );

    // Make sure it exists
    if ( !h_muons.isValid() ) {
      throw cms::Exception("ProductNotFound") << "Muon collection " << muonSrc_ << " not found, skip event\n";
    }

    // Loop over the muons
    std::vector<pat::Muon>::const_iterator imuBegin = h_muons->begin(),
      imuEnd = h_muons->end(), imu = imuBegin;
    for( ; imu != imuEnd; ++imu ) {
      pat::Muon muon( *imu );

      // get the global track
      reco::TrackRef globalTrack = muon.globalTrack();
      
      // Make sure the collection it points to is there
      if ( globalTrack.isNonnull() && globalTrack.isAvailable() ) {
	double norm_chi2 = globalTrack->chi2() / globalTrack->ndof();
	double corr_d0 = globalTrack->dxy( beamPoint );
	unsigned int nhits = globalTrack->numberOfValidHits();
	
	double hcalIso = muon.hcalIso();
	double ecalIso = muon.ecalIso();
	double trkIso  = muon.trackIso();
	double pt      = muon.pt() ;

	double relIso = (ecalIso + hcalIso + trkIso) / pt;

	// if the muon passes the event selection, add it to the output list
	if ( norm_chi2      < chi2CutMuon_ &&
	     fabs(corr_d0)  < d0CutMuon_ &&
	     nhits          >= nHitsCutMuon_ &&
	     hcalIso        < hcalEtCutMuon_ &&
	     ecalIso        < ecalEtCutMuon_ &&
	     relIso         < relIsoCutMuon_ ) {
	  p_muons->push_back( muon );
	}
      }
    }
  }
  
  if ( makeElectrons_ ) {
    // get handle for input electron collection
    edm::Handle< std::vector<pat::Electron> > h_electrons;
    iEvent.getByLabel( electronSrc_, h_electrons );

    // Make sure it exists
    if ( !h_electrons.isValid() ) {
      throw cms::Exception("ProductNotFound") << "Electron collection " << electronSrc_ << " not found, skip event\n";
    }

    // Loop over the electrons
    std::vector<pat::Electron>::const_iterator imuBegin = h_electrons->begin(),
      imuEnd = h_electrons->end(), imu = imuBegin;
    for( ; imu != imuEnd; ++imu ) {
      pat::Electron electron( *imu );

      reco::TrackRef track = electron.track();
      
      // Make sure the collection it points to is there
      if ( track.isNonnull() && track.isAvailable() ) {
	double corr_d0 = track->dxy( beamPoint );
	
	double hcalIso = electron.hcalIso();
	double ecalIso = electron.ecalIso();
	double trkIso  = electron.trackIso();
	double pt      = electron.pt() ;

	double relIso = (ecalIso + hcalIso + trkIso) / pt;

	// if the electron passes the event selection, add it to the output list
	if ( fabs(corr_d0)  < d0CutElectron_ &&
	     relIso         < relIsoCutElectron_ ) {
	  p_electrons->push_back( electron );
	}
      }
    }
  }
  

  bool pass = 
    (p_muons->size() >= minMuons_) && 
    (p_muons->size() <= maxMuons_) &&
    (p_electrons->size() >= minElectrons_) && 
    (p_electrons->size() <= maxElectrons_) ;
  
  iEvent.put( p_muons );
  iEvent.put( p_electrons );

  return pass;
}

// ------------ method called once each job just before starting event loop  ------------
void 
VPlusJets::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
VPlusJets::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(VPlusJets);
