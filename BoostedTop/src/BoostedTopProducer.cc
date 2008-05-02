#include "Analysis/BoostedTop/interface/BoostedTopProducer.h"
#include "PhysicsTools/CandUtils/interface/AddFourMomenta.h"

#include <string>
#include <sstream>

using std::string;

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
BoostedTopProducer::BoostedTopProducer(const edm::ParameterSet& iConfig) :
  eleLabel_   (iConfig.getParameter<edm::InputTag>  ("electronLabel")),
  muoLabel_   (iConfig.getParameter<edm::InputTag>  ("muonLabel")),
  jetLabel_   (iConfig.getParameter<edm::InputTag>  ("jetLabel")),
  metLabel_   (iConfig.getParameter<edm::InputTag>  ("metLabel")),
  solLabel_   (iConfig.getParameter<edm::InputTag>  ("solLabel")),
  caloIsoCut_ (iConfig.getParameter<double>         ("caloIsoCut") ),
  mTop_       (iConfig.getParameter<double>         ("mTop") )
{
  //register products
  produces<std::vector<reco::NamedCompositeCandidate> > ();
}


BoostedTopProducer::~BoostedTopProducer()
{
}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
BoostedTopProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{

  // -----------------------------------------------------
  // get the bare PAT objects
  // -----------------------------------------------------
   edm::Handle<std::vector<pat::Muon> > muonHandle;
   iEvent.getByLabel(muoLabel_,muonHandle);
   std::vector<pat::Muon> const & muons = *muonHandle;
   
   edm::Handle<std::vector<pat::Jet> > jetHandle;
   iEvent.getByLabel(jetLabel_,jetHandle);
   std::vector<pat::Jet> const & jets = *jetHandle;

   edm::Handle<std::vector<pat::Electron> > electronHandle;
   iEvent.getByLabel(eleLabel_,electronHandle);
   std::vector<pat::Electron> const & electrons = *electronHandle;

   edm::Handle<std::vector<pat::MET> > metHandle;
   iEvent.getByLabel(metLabel_,metHandle);
   std::vector<pat::MET> const & mets = *metHandle;

   // -----------------------------------------------------
   // Event Preselection:
   //    <= 1 isolated electron or muon
   //    >= 1 electron or muon
   //    >= 2 jets
   //    >= 1 missing et
   //
   // To explain:
   //    We want to look at leptons within "top jets" in some
   //    cases. This means the isolation will kill those events.
   //    However, if there IS an isolated lepton, we want only
   //    one of them. 
   // 
   //    So to select the prompt W lepton, the logic is:
   //    1. If there is an isolated lepton, accept it as the W lepton.
   //    2. Else, take the highest Pt lepton (possibly non-isolated)
   // 
   // -----------------------------------------------------
   bool preselection = true;
  
   // This will hold the prompt W lepton candidate, and a
   // maximum pt decision variable
   double maxWLeptonPt = -1;
   reco::Candidate const * Wlepton = 0;

   // ----------------------
   // Find isolated muons, and highest pt lepton
   // ----------------------
   pat::Muon     const * isolatedMuon     = 0;
   bool nIsolatedMuons = 0;
   std::vector<pat::Muon>::const_iterator muit = muons.begin(),
     muend = muons.end();
   for (; muit != muend; ++muit ) {

     // Find highest pt lepton
     double pt = muit->pt();
     if ( pt > maxWLeptonPt ) {
       maxWLeptonPt = pt;
       Wlepton = &*muit;
     }

     // Find any isolated muons
     double caloIso = muit->caloIso();
     if ( caloIso >= 0 && caloIso < caloIsoCut_ ) {
       nIsolatedMuons++;
       isolatedMuon = &*muit;
     }
   }

   // ----------------------
   // Find isolated electrons, and highest pt lepton
   // ----------------------
   pat::Electron     const * isolatedElectron     = 0;
   bool nIsolatedElectrons = 0;
   std::vector<pat::Electron>::const_iterator eit = electrons.begin(),
     eend = electrons.end();
   for (; eit != eend; ++eit ) {

     // Find highest pt lepton
     double pt = eit->pt();
     if ( pt > maxWLeptonPt ) {
       maxWLeptonPt = pt;
       Wlepton = &*eit;
     }

     // Find any isolated electrons
     double caloIso = eit->caloIso();
     if ( caloIso >= 0 && caloIso < caloIsoCut_ ) {
       nIsolatedElectrons++;
       isolatedElectron = &*eit;
     }
   }

   // ----------------------
   // Now decide on the "prompt" lepton from the W:
   // Choose isolated leptons over all, and if no isolated,
   // then take highest pt lepton. 
   // ----------------------
   bool isMuon = true;
   if      ( isolatedMuon     != 0 ) { Wlepton = isolatedMuon; isMuon = true; }
   else if ( isolatedElectron != 0 ) { Wlepton = isolatedElectron; isMuon = false; } 
   // else do nothing, it's already set to highest pt lepton

   // Get some pointers for convenience.
   pat::Muon     const * muon     = dynamic_cast<pat::Muon const *>    (Wlepton);
   pat::Electron const * electron = dynamic_cast<pat::Electron const *>(Wlepton);

   // ----------------------
   // Veto events that have more than one isolated lepton
   // ----------------------
   int nIsolatedLeptons = nIsolatedMuons + nIsolatedElectrons;
   if ( nIsolatedLeptons > 1 ) {
     preselection = false;
   }

   // ----------------------
   // Veto events that have no prompt lepton candidates
   // ----------------------
   if ( Wlepton == 0 ) {
     preselection = false;
   }

   // ----------------------
   // Veto events with < 2 jets or no missing et
   // ----------------------
   if ( jets.size() < 2 ||
	mets.size() == 0 ) {
     preselection = false;
   }

   bool write = false;


   
   // -----------------------------------------------------
   //
   // NamedCompositeCandidates to store the event solution.
   // This will take one of two forms:
   //    a) lv jj jj   Full reconstruction.
   //       
   //   ttbar->
   //       (hadt -> (hadW -> hadp + hadq) + hadb) + 
   //       (lept -> (lepW -> lepton + neutrino) + lepb)
   // 
   //    b) lv jj (j)  Partial reconstruction, associate 
   //                  at least 1 jet to the lepton 
   //                  hemisphere, and at least one jet in 
   //                  the opposite hemisphere.
   //
   //    ttbar->
   //        (hadt -> (hadJet1 [+ hadJet2] ) ) +
   //        (lept -> (lepW -> lepton + neutrino) + lepJet1 )
   //
   // There will also be two subcategories of (b) that 
   // will correspond to physics cases:
   // 
   //    b1)           Lepton is isolated: Moderate ttbar mass.
   //    b2)           Lepton is nonisolated: High ttbar mass. 
   //
   // -----------------------------------------------------
   reco::NamedCompositeCandidate ttbar("ttbar");
   AddFourMomenta addFourMomenta;


   // Main decisions after preselection
   if ( preselection ) {

     // This will be modified for the z solution, so make a copy
     pat::MET              neutrino( mets[0] );


     // 1. First examine the low mass case with 4 jets and widely separated
     //    products. We take out the TtSemiEvtSolution from the TQAF and
     //    form the ttbar invariant mass.
     if ( jets.size() >= 4 ) {

       // get the ttbar semileptonic event solution if there are more than 3 jets
       edm::Handle< std::vector<TtSemiEvtSolution> > eSols;
       iEvent.getByLabel(solLabel_, eSols);

       // Have solution, continue
       if ( eSols->size() >= 0 ) {
	 // Just set the ttbar solution to the best ttbar solution from
	 // TtSemiEvtSolutionMaker
	 int bestSol = (*eSols)[0].getLRBestJetComb();   
	 ttbar = (*eSols)[bestSol].getRecoHyp();
	 write = true;
       }
       // No ttbar solution with 4 jets, something is weird, print a warning
       else {
	 edm::LogWarning("DataNotFound") << "BoostedTopProducer: Cannot find TtSemiEvtSolution\n";
       }
     }
     // 2. With 2 or 3 jets, we decide based on the separation between
     // the lepton and the closest jet in that hemisphere whether to
     // consider it "moderate" or "high" mass. 
     else if ( jets.size() == 2 || jets.size() == 3 ) {

       // ------------------------------------------------------------------
       // First create a leptonic W candidate
       // ------------------------------------------------------------------
       NamedCompositeCandidate lepW("lepW");
       
       if ( isMuon ) {
	 lepW.addDaughter(  *muon,     "muon" );
       } else {
	 lepW.addDaughter( *electron, "electron" );
       }
       lepW.addDaughter  ( neutrino, "neutrino");
       addFourMomenta.set( lepW );

       bool nuzHasComplex = false;
       MEzCalculator zcalculator;
       zcalculator.SetMET( neutrino );
       if ( isMuon ) 
	 zcalculator.SetMuon( *muon );
       else
	 zcalculator.SetMuon( *electron ); // This name is misleading, should be setLepton
       double neutrinoPz = zcalculator.Calculate(1);// closest to the lepton Pz
       if (zcalculator.IsComplex()) nuzHasComplex = true;
       // Set the neutrino pz
       neutrino.setPz( neutrinoPz );

       // ------------------------------------------------------------------
       // Next ensure that there is a jet within the hemisphere of the 
       // leptonic W, and one in the opposite hemisphere
       // ------------------------------------------------------------------
       reco::NamedCompositeCandidate hadt("hadt");
       reco::NamedCompositeCandidate lept("lept");
       lept.addDaughter( lepW, "lepW" );

       std::string hadName("hadJet");
       std::string lepName("lepJet");

       // Get the W momentum
       TLorentzVector p4_W (lepW.px(), lepW.py(), lepW.pz(), lepW.energy() );

       // Loop over the jets
       std::vector<pat::Jet>::const_iterator jetit = jets.begin(),
	 jetend = jets.end();
       unsigned long ii = 1; // Count by 1 for naming histograms
       for ( ; jetit != jetend; ++jetit, ++ii ) {
	 // Get this jet's momentum
	 TLorentzVector p4_jet (jetit->px(), jetit->py(), jetit->pz(), jetit->energy() );

	 // Calculate psi (like DeltaR, only more invariant under Rapidity)
	 double psi = Psi( p4_W, p4_jet, mTop_ );

	 // Get jets that are in the leptonic hemisphere
	 if ( psi < TMath::Pi() ) {
	   // Add this jet to the leptonic top
	   std::stringstream s;
	   s << lepName << ii;
	   lept.addDaughter( *jetit, s.str() );
	 }
	 // Get jets that are in the hadronic hemisphere
	 if ( psi > TMath::Pi() ) {
	   // Add this jet to the hadronic top. We don't
	   // make any W hypotheses in this case, since
	   // we cannot determine which of the three
	   // jets are merged.
	   std::stringstream s;
	   s << hadName << ii;
	   hadt.addDaughter( *jetit, s.str() );
	   
	 }
       } // end loop over jets

       addFourMomenta.set( lept );
       addFourMomenta.set( hadt );

       bool lepWHasJet = lept.numberOfDaughters() >= 2; // W and >= 1 jet
       bool hadWHasJet = hadt.numberOfDaughters() >= 1; // >= 1 jet
       if ( lepWHasJet && hadWHasJet ) {
	 ttbar.addDaughter( lept, "lept");
	 ttbar.addDaughter( hadt, "hadt");
	 addFourMomenta.set( ttbar );
	 write = true; 
       } // end of hadronic jet and leptonic jet


     } // end if there are 2 or 3 jets 
   
   } // end if preselection is satisfied

   // Write the solution to the event record   
   std::vector<reco::NamedCompositeCandidate> ttbarList;
   if ( write ) {
     ttbarList.push_back( ttbar );
   }
   std::auto_ptr<std::vector<reco::NamedCompositeCandidate> > pTtbar ( new std::vector<reco::NamedCompositeCandidate>(ttbarList) );
   iEvent.put( pTtbar );

   
}

// ------------ method called once each job just before starting event loop  ------------
void 
BoostedTopProducer::beginJob(const edm::EventSetup&)
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
BoostedTopProducer::endJob() {
}

double
BoostedTopProducer::Psi(TLorentzVector p1, TLorentzVector p2, double mass) {

	TLorentzVector ptot = p1 + p2;
	Double_t theta1 = TMath::ACos( (p1.Vect().Dot(ptot.Vect()))/(p1.P()*ptot.P()) );
	Double_t theta2 = TMath::ACos( (p2.Vect().Dot(ptot.Vect()))/(p2.P()*ptot.P()) );
	//Double_t sign = 1.;
	//if ( (theta1+theta2) > (TMath::Pi()/2) ) sign = -1.;
	double th1th2 = theta1 + theta2;
	double psi = (p1.P()+p2.P())*TMath::Abs(TMath::Sin(th1th2))/(2.* mass );
	if ( th1th2 > (TMath::Pi()/2) )
		psi = (p1.P()+p2.P())*( 1. + TMath::Abs(TMath::Cos(th1th2)))/(2.* mass );
	
	return psi;
}

//define this as a plug-in
DEFINE_FWK_MODULE(BoostedTopProducer);
