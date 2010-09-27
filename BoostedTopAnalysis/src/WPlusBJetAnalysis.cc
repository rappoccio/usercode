#include "Analysis/BoostedTopAnalysis/interface/WPlusBJetAnalysis.h"
using namespace std;

WPlusBJetAnalysis::WPlusBJetAnalysis( const edm::ParameterSet & iConfig,  TFileDirectory & iDir ) :
  theDir( iDir ),
  jetSrc_( iConfig.getParameter<edm::InputTag>("jetSrc") ),
  twPlusBJetSelection_ ( iConfig.getParameter<edm::ParameterSet>("WPlusBJetSelection") ),
  owPlusBJetSelection_ (twPlusBJetSelection_ ),
  leadJetPtCut_ ( iConfig.getParameter<double>("leadJetPtCut")  )
{
  cout<< "Instantiate WPlusBJetAnalysis" << endl;
  histograms1d["nJet"]  = theDir.make<TH1F>("nJet",   "Number of Jets",     20,   0,    20);
  histograms1d["jetPt"] = theDir.make<TH1F>("jetPt",  "Jet Pt; Jet Pt (GeV/c^{2})",   200,    0,    1000 );
  histograms1d["jetEta"]  = theDir.make<TH1F>("jetEta", "Jet #eta; Jet #eta",     50,   -3.0,     3.0 );
  histograms1d["jetMass"] = theDir.make<TH1F>("jetMass",  "Jet Mass; Jet Mass (GeV/c^{2})",   200,    0,    1000 );
  histograms1d["nW"]      = theDir.make<TH1F>("nW",     "Number of W",    10,   0,    10 );
  histograms1d["nB"]      = theDir.make<TH1F>("nB",     "Number of B",    10,   0,    10 );
  histograms1d["wMass0"]   = theDir.make<TH1F>("wMass0",  "W Jet Mass",     40,   0,    200 );
  histograms1d["wMass1"]   = theDir.make<TH1F>("wMass1",  "W Jet Mass",     40,   0,    200 );
  histograms1d["nTightTop"]   = theDir.make<TH1F>("nTightTop",    "Number of Tight Top",    10,   0,  10 );
  histograms1d["nLooseTop"]   = theDir.make<TH1F>("nLooseTop",    "Number of Loose Top",    10,   0,  10 );
  histograms1d["tightTopMass0"]    = theDir.make<TH1F>("tightTopMass0",   "Tight Top Mass; Mass (GeV/c^{2})",   100,  0,  500 );
  histograms1d["looseTopMass0"]    = theDir.make<TH1F>("looseTopMass0",   "Loose Top Mass; Mass (GeV/c^{2})",   100,  0,  500 );
  histograms1d["type3TopMass0"]    = theDir.make<TH1F>("type3TopMass0",   "Type 3 Top Mass; Mass (GeV/c^{2})",   100,  0,  500 );
  histograms1d["tightTopMass1"]    = theDir.make<TH1F>("tightTopMass1",   "Tight Top Mass; Mass (GeV/c^{2})",   100,  0,  500 );
  histograms1d["looseTopMass1"]    = theDir.make<TH1F>("looseTopMass1",   "Loose Top Mass; Mass (GeV/c^{2})",   100,  0,  500 );
  histograms1d["type3TopMass1"]    = theDir.make<TH1F>("type3TopMass1",   "Type 3 Top Mass; Mass (GeV/c^{2})",   100,  0,  500 );
  histograms1d["minPairMass0"]     = theDir.make<TH1F>("minPairMass0",    "Min Pair Inv Mass; Mass (GeV/c^{2})",  100,  0,  500 );
  histograms1d["minPairMass1"]     = theDir.make<TH1F>("minPairMass1",    "Min Pair Inv Mass; Mass (GeV/c^{2})",  100,  0,  500 );

  histograms1d["nType3Top"]       = theDir.make<TH1F>("nType3Top",      "Number of Type 3 Top",     10,   0,    10 );
  histograms1d["leadJetPt"]       = theDir.make<TH1F>("leadJetPt",      "Leading Jet Pt",           200,  0,    1000 );
  histograms1d["minPairDr0"]       = theDir.make<TH1F>("minPairDr0",      "Min Pair #Delta R",        50,   0.0, 6.0 );
  histograms1d["minPairDPhi0"]     = theDir.make<TH1F>("minPairDPhi0",    "Min Pair #Delta Phi",      50,   0,    3. );
  histograms1d["wbJetDr0"]         = theDir.make<TH1F>("wbJetDr0",        "W and B Jet #Delta R",     50,   0.0, 6.0 );
  histograms1d["wbJetDPhi0"]       = theDir.make<TH1F>("wbJetDPhi0",      "W and B Jet #Delta Phi",   50,   0.,   3. );
  histograms1d["waJetDr0"]         = theDir.make<TH1F>("waJetDr0",        "W and A Jet #Delta R",     50,   0.0, 6.0 );
  histograms1d["waJetDPhi0"]       = theDir.make<TH1F>("waJetDPhi0",      "W and A Jet #Delta Phi",   50,   0.,   3. );
  histograms1d["minPairDr1"]       = theDir.make<TH1F>("minPairDr1",      "Min Pair #Delta R",        50,   0.0, 6.0 );
  histograms1d["minPairDPhi1"]     = theDir.make<TH1F>("minPairDPhi1",    "Min Pair #Delta Phi",      50,   0,    3. );
  histograms1d["wbJetDr1"]         = theDir.make<TH1F>("wbJetDr1",        "W and B Jet #Delta R",     50,   0.0, 6.0 );
  histograms1d["wbJetDPhi1"]       = theDir.make<TH1F>("wbJetDPhi1",      "W and B Jet #Delta Phi",   50,   0.,   3. );
  histograms1d["waJetDr1"]         = theDir.make<TH1F>("waJetDr1",        "W and A Jet #Delta R",     50,   0.0, 6.0 );
  histograms1d["waJetDPhi1"]       = theDir.make<TH1F>("waJetDPhi1",      "W and A Jet #Delta Phi",   50,   0.,   3. );


  histograms1d["topPairDPhi"]     = theDir.make<TH1F>("topPairDPhi",    "Top Pair #Delta Phi",      50,   0.,   4. );
  histograms1d["topPairDr"]       = theDir.make<TH1F>("topPairDr",      "Top Pair #Delta R",        50,   0.0,  6.0 );
  histograms1d["pairBJetDPhi0"]    = theDir.make<TH1F>("pairBJetDPhi0",   "Min Pair and B Jet #Delta Phi",  50, 0.0, 3. );
  histograms1d["pairBJetDr0"]      = theDir.make<TH1F>("pairBJetDr0",     "Min Pair and B Jet #Delta R",  50,   0.0,  6 );
  histograms1d["pairBJetDPhi1"]    = theDir.make<TH1F>("pairBJetDPhi1",   "Min Pair and B Jet #Delta Phi",  50, 0.0, 3. );
  histograms1d["pairBJetDr1"]      = theDir.make<TH1F>("pairBJetDr1",     "Min Pair and B Jet #Delta R",  50,   0.0,  6 );

  histograms1d["minPairMassType33"]   = theDir.make<TH1F>("minPairMassType33",  "Min Pair Mass from Type33",  100,  0,  500 );
  histograms1d["topMassType33"]       = theDir.make<TH1F>("topMassType33",      "Top Mass from Type33",       100,  0,  500 );
  histograms1d["wJetPt"]          = theDir.make<TH1F>("wJetPt",         "W Jet Pt",                 200,  0,    1000 );
  histograms1d["bJetPt"]          = theDir.make<TH1F>("bJetPt",         "b Jet Pt",                 200,  0,    1000 );
  histograms1d["ttMassType22"]    = theDir.make<TH1F>("ttMassType22",   "t#bar{t} Inv Mass Type22",   200,  0,  2000 );
  histograms1d["ttMassType23"]    = theDir.make<TH1F>("ttMassType23",   "t#bar{t} Inv Mass Type23",   200,  0,  2000 );
  histograms1d["ttMassType33"]    = theDir.make<TH1F>("ttMassType33",   "t#bar{t} Inv Mass Type33",   200,  0,  2000 );

  histograms2d["jetMassVsPt"]     = theDir.make<TH2F>("jetMassVsPt",    "Jet Mass Vs Pt; Jet Pt (GeV/c^{2}); Jet Mass (GeV/c^{2})",    200,  0,    1000,   100,    0,    500 );

}

void WPlusBJetAnalysis::analyze( const edm::EventBase & iEvent )
{
  //cout<<"Point 1"<<endl;

  const boost::shared_ptr<PFJetIDSelectionFunctor> & pfJetSel = twPlusBJetSelection_.pfJetSel();
  pat::strbitset retPFJet = pfJetSel->getBitTemplate();

  edm::Handle<vector<pat::Jet>  >  jetHandle;
  iEvent.getByLabel( jetSrc_, jetHandle );

 // cout<<"Point 2"<<endl;
  //Apply pfJet ID and get the leading jet
  const pat::Jet * theJet;
  int   numJets = 0;
  for( vector<pat::Jet>::const_iterator jetBegin=jetHandle->begin(), jetEnd=jetHandle->end(), ijet=jetBegin ;
    ijet!=jetEnd; ijet++ )
  {
    retPFJet.set(false);
    bool passJetID = (*pfJetSel)( *ijet, retPFJet );
    if( passJetID ) {
      numJets ++ ;
      histograms1d["jetPt"]     ->  Fill( ijet->pt() );
      histograms1d["jetEta"]    ->  Fill( ijet->eta() );
      histograms1d["jetMass"]   ->  Fill( ijet->mass() );

      histograms2d["jetMassVsPt"]   ->  Fill( ijet->pt(), ijet->mass() );
      if( numJets == 1 )
        theJet = &(*ijet);
    }
  }  // end ijet

  histograms1d["nJet"]    ->  Fill( numJets );

  //cout<<"Point 2"<<endl;
  if( numJets < 1 )   return;
  histograms1d["leadJetPt"]     ->  Fill( theJet->pt() );
  if( theJet->pt() < leadJetPtCut_ )   return ;

  pat::strbitset tret = twPlusBJetSelection_.getBitTemplate();
  //Analyze the towards direction
  bool tpassWPlusBJet  = twPlusBJetSelection_( iEvent, theJet->p4(), tret, true );

  pat::strbitset oret = owPlusBJetSelection_.getBitTemplate();
  //Analyze the opposite direction
  bool opassWPlusBJet  = owPlusBJetSelection_( iEvent, theJet->p4(), oret, false );

  if( tpassWPlusBJet && opassWPlusBJet )
      cout<<"Run, "<<iEvent.id().run() << "Event, " << iEvent.id().event() <<endl;
  
  std::vector<edm::Ptr<pat::Jet> >  const & tWJets = twPlusBJetSelection_.wJets();
  std::vector<edm::Ptr<pat::Jet> >  const & oWJets = owPlusBJetSelection_.wJets();
  std::vector<edm::Ptr<pat::Jet> >  const & tbJets = twPlusBJetSelection_.bJets();
  std::vector<edm::Ptr<pat::Jet> >  const & obJets = owPlusBJetSelection_.bJets();
  std::vector<edm::Ptr<pat::Jet> >  const & tMinDrPair = twPlusBJetSelection_.minDrPair();
  std::vector<edm::Ptr<pat::Jet> >  const & oMinDrPair = owPlusBJetSelection_.minDrPair();
  edm::Ptr<pat::Jet> const & taJet = twPlusBJetSelection_.aJet();
  edm::Ptr<pat::Jet> const & oaJet = owPlusBJetSelection_.aJet();

  int numWJets = tWJets.size() + oWJets.size();
  int numBJets = twPlusBJetSelection_.bJets().size() + owPlusBJetSelection_.bJets().size();

  histograms1d["nW"]      ->  Fill( numWJets );
  histograms1d["nB"]      ->  Fill( numBJets );

  int numTightTop = 0, numLooseTop = 0, numType3Top = 0;
  bool tType2 = true, oType2 = true;
  bool tTight = true, oTight = true;

  reco::Candidate::LorentzVector p4_top0(0,0,0,0), p4_top1(0,0,0,0);
  reco::Candidate::LorentzVector p4_W0(0,0,0,0),  p4_W1(0,0,0,0);
  reco::Candidate::LorentzVector p4_b0(0,0,0,0),  p4_b1(0,0,0,0);
  reco::Candidate::LorentzVector p4_a0(0,0,0,0),  p4_a1(0,0,0,0);
  reco::Candidate::LorentzVector p4_first0(0,0,0,0),  p4_first1(0,0,0,0);
  reco::Candidate::LorentzVector p4_second0(0,0,0,0),  p4_second1(0,0,0,0);
  reco::Candidate::LorentzVector p4_minPair0(0,0,0,0),  p4_minPair1(0,0,0,0);

  if( tret[std::string(">= 1 bJet")] ) {   // find a tight top
    //cout<<"I"<<endl;
    p4_W0 =  tWJets.at(0)->p4() ;
    p4_b0 =  tbJets.at(0)->p4() ;
    p4_top0 = p4_W0 + p4_b0;
    tType2 = true;
    tTight = true;
  }
  else if( tret[std::string(">= 1 WJet")] && twPlusBJetSelection_.aJetFound() )  {  // find a loose top 
    //cout<<"II"<<endl;
    p4_W0 =  tWJets.at(0)->p4() ;
    p4_a0 =  taJet->p4() ;
    p4_top0 = p4_W0 + p4_a0;
    tType2 = true;
    tTight = false;
  }
  else if( tMinDrPair.size() == 2 && tbJets.size() >= 1 ) { // Check the minDrPair
    //cout<<"III"<<endl;
    p4_first0 = tMinDrPair.at(0)->p4() ;
    p4_second0 =  tMinDrPair.at(1)->p4() ;
    p4_minPair0 = p4_first0 + p4_second0 ;
    p4_b0   = tbJets.at(0)->p4() ;
    p4_top0 = p4_minPair0 + p4_b0 ;
    tType2 = false;
  }
  else  //not interesting events
    return;


  if( oret[std::string(">= 1 bJet")] ) {   // find a tight top
    //cout<<"Point aa"<<endl;
    p4_W1 =  oWJets.at(0)->p4() ;
    p4_b1 =  obJets.at(0)->p4() ;
    p4_top1 = p4_W1 + p4_b1;
    oType2 = true;
    oTight = true;
  }
  else if( oret[std::string(">= 1 WJet")] && owPlusBJetSelection_.aJetFound() )  {  // find a loose top 
    //cout<<"Point bb"<<endl;
    p4_W1 =  oWJets.at(0)->p4() ;
    p4_a1 =  oaJet->p4() ;
    p4_top1 = p4_W1 + p4_a1;
    oType2 = true;
    oTight = false;
  }
  else if( oMinDrPair.size() == 2 && obJets.size() >= 1 ) { // Check the minDrPair
    p4_first1 = oMinDrPair.at(0)->p4() ;
    p4_second1 =  oMinDrPair.at(1)->p4() ;
    p4_minPair1 = p4_first1 + p4_second1 ;
    p4_b1   = obJets.at(0)->p4() ;
    p4_top1 = p4_minPair1 + p4_b1;
    oType2 = false;
  }
  else // not interesting events
    return;

  if( tType2 )  { 
    histograms1d["wMass0"]    ->  Fill( p4_W0.mass() );
    histograms1d["wJetPt"]    ->  Fill( p4_W0.pt() );
    if( p4_W0.mass() > 50 && p4_W0.mass() < 100 ) {
      if( tTight ) {
        histograms1d["tightTopMass0"]     ->  Fill( p4_top0.mass() );
        double deltaR = reco::deltaR<double>( p4_W0.eta(), p4_W0.phi(), p4_b0.eta(), p4_b0.phi() );
        double dPhi   = reco::deltaPhi<double>( p4_W0.phi(), p4_b0.phi() );
        histograms1d["wbJetDr0"]          ->  Fill( deltaR );
        histograms1d["wbJetDPhi0"]        ->  Fill( dPhi );
        histograms1d["bJetPt"]            ->  Fill( p4_b0.pt() );
        numTightTop ++;
      } // end tTight
      else {
        histograms1d["looseTopMass0"]     ->  Fill( p4_top0.mass() );
        double deltaR = reco::deltaR<double>( p4_W0.eta(), p4_W0.phi(), p4_a0.eta(), p4_a0.phi() );
        double dPhi   = reco::deltaPhi<double>( p4_W0.phi(), p4_a0.phi() );
        histograms1d["waJetDr0"]          ->  Fill( deltaR );
        histograms1d["waJetDPhi0"]        ->  Fill( dPhi );
        numLooseTop ++;
      }  //end else
    }  // end mass > 50, mass < 100 
  } // end tType2
  else  {
    histograms1d["minPairMass0"]          ->  Fill( p4_minPair0.mass() );
    histograms1d["bJetPt"]                ->  Fill( p4_b0.pt() );
    if( p4_minPair0.mass() > 50 && p4_minPair0.mass() < 100 ) {
      histograms1d["type3TopMass0"]       ->  Fill( p4_top0.mass() );
      double deltaR = reco::deltaR<double>( p4_first0.eta(), p4_first0.phi(), p4_second0.eta(), p4_second0.phi() );
      double dPhi   = reco::deltaPhi<double>( p4_first0.phi(), p4_second0.phi() );
      double deltaR1 = reco::deltaR<double>( p4_minPair0.eta(), p4_minPair0.phi(), p4_b0.eta(), p4_b0.phi() );
      double dPhi1   = reco::deltaPhi<double>( p4_minPair0.phi(), p4_b0.phi() );
      histograms1d["minPairDr0"]          ->  Fill( deltaR );
      histograms1d["minPairDPhi0"]        ->  Fill( dPhi  );
      histograms1d["pairBJetDPhi0"]       ->  Fill( dPhi1 );
      histograms1d["pairBJetDr0"]         ->  Fill( deltaR1 );
      numType3Top ++;
    }
  }

  if( oType2 )  {
    histograms1d["wMass1"]    ->  Fill( p4_W1.mass() );
    histograms1d["wJetPt"]    ->  Fill( p4_W1.pt() );
    if( p4_W1.mass() > 50 && p4_W1.mass() < 100 ) {
      if( oTight )  {
        histograms1d["tightTopMass1"]     ->  Fill( p4_top1.mass() );
        double deltaR = reco::deltaR<double>( p4_W1.eta(), p4_W1.phi(), p4_b1.eta(), p4_b1.phi() );
        double dPhi   = reco::deltaPhi<double>( p4_W1.phi(), p4_b1.phi() );
        histograms1d["wbJetDr1"]          ->  Fill( deltaR );
        histograms1d["wbJetDPhi1"]        ->  Fill( dPhi );
        histograms1d["bJetPt"]            ->  Fill( p4_b1.pt() );
        numTightTop ++;
      } // end oTight
      else  {
        histograms1d["looseTopMass1"]     ->  Fill( p4_top1.mass() );
        double deltaR = reco::deltaR<double>( p4_W1.eta(), p4_W1.phi(), p4_a1.eta(), p4_a1.phi() );
        double dPhi   = reco::deltaPhi<double>( p4_W1.phi(), p4_a1.phi() );
        histograms1d["waJetDr1"]          ->  Fill( deltaR );
        histograms1d["waJetDPhi1"]        ->  Fill( dPhi );
        numLooseTop ++;
      } // end else
    } // end mass cut
  } // end oType2
  else  {
    histograms1d["minPairMass1"]          ->  Fill( p4_minPair1.mass() );
    histograms1d["bJetPt"]                ->  Fill( p4_b1.pt() );
    if( p4_minPair1.mass() > 50 && p4_minPair1.mass() < 100 )  {
      histograms1d["type3TopMass1"]       ->  Fill( p4_top1.mass() );
      double deltaR = reco::deltaR<double>( p4_first1.eta(), p4_first1.phi(), p4_second1.eta(), p4_second1.phi() );
      double dPhi   = reco::deltaPhi<double>( p4_first1.phi(), p4_second1.phi() );
      double deltaR1 = reco::deltaR<double>( p4_minPair1.eta(), p4_minPair1.phi(), p4_b1.eta(), p4_b1.phi() );
      double dPhi1   = reco::deltaPhi<double>( p4_minPair1.phi(), p4_b1.phi() );
      histograms1d["minPairDr1"]          ->  Fill( deltaR );
      histograms1d["minPairDPhi1"]        ->  Fill( dPhi  );
      histograms1d["pairBJetDPhi1"]       ->  Fill( dPhi1 );
      histograms1d["pairBJetDr1"]         ->  Fill( deltaR1 );
      numType3Top ++;
    }
  }

  double top0Mass = p4_top0.mass();
  double top1Mass = p4_top1.mass();
  double minPairMass0 = p4_minPair0.mass();
  double minPairMass1 = p4_minPair1.mass();
  double wMass0   = p4_W0.mass();
  double wMass1   = p4_W1.mass();

  if( !tType2 && !oType2 )  {
    histograms1d["minPairMassType33"]     ->  Fill( p4_minPair0.mass() );
    histograms1d["minPairMassType33"]     ->  Fill( p4_minPair1.mass() );

    if( minPairMass0 > 50 && minPairMass0 < 100 && minPairMass1 > 50 && minPairMass1 < 100 ) {
      histograms1d["topMassType33"]         ->  Fill( top0Mass );
      histograms1d["topMassType33"]         ->  Fill( top1Mass );
      if( top0Mass > 140 && top0Mass < 230 && top1Mass > 140 && top1Mass < 230 ) {
        histograms1d["ttMassType33"]    ->  Fill( (p4_top0+p4_top1).mass() );
      }
    } // minPairMass cut
  }
  else if( numTightTop >= 1 )  {
    if( tType2 && oType2 ) {
      if( top0Mass > 140 && top0Mass < 230 && top1Mass > 140 && top1Mass < 230 && 
          wMass0 > 50 && wMass0 < 100 && wMass1 > 50 && wMass1 < 100 )
        histograms1d["ttMassType22"]          ->  Fill( (p4_top0+p4_top1).mass() );
    }
    else  { 
      if( top0Mass > 140 && top0Mass < 230 && top1Mass > 140 && top1Mass < 230 &&
         (  ( wMass0 > 50 && wMass0 < 100 && minPairMass1 > 50 && minPairMass1 < 100   )  ||
            ( minPairMass0 > 50 && minPairMass0 < 100  && wMass1 > 50 && wMass1 < 100 )     )   )
        histograms1d["ttMassType23"]          ->  Fill( (p4_top0+p4_top1).mass() );
    }
  }


  double topPairDr = reco::deltaR<double>( p4_top0.eta(), p4_top0.phi(), p4_top1.eta(), p4_top1.phi() );
  double topPairDPhi  = reco::deltaPhi<double>( p4_top0.phi(), p4_top1.phi() );
  histograms1d["topPairDPhi"]       ->  Fill( topPairDPhi );
  histograms1d["topPairDr"]         ->  Fill( topPairDr );


  histograms1d["nTightTop"]     ->  Fill( numTightTop );
  histograms1d["nLooseTop"]     ->  Fill( numLooseTop );
  histograms1d["nType3Top"]     ->  Fill( numType3Top );

}
