#include "Analysis/BoostedTopAnalysis/interface/WPlusBJetAnalysis.h"
using namespace std;

WPlusBJetAnalysis::WPlusBJetAnalysis( const edm::ParameterSet & iConfig,  TFileDirectory & iDir ) :
  theDir( iDir ),
  wPlusBJetType22Selection_( iConfig.getParameter<edm::ParameterSet>("WPlusBJetEventSelection")  ),
  wPlusBJetType23Selection_( iConfig.getParameter<edm::ParameterSet>("WPlusBJetEventSelection")  ),
  wPlusBJetType33Selection_( iConfig.getParameter<edm::ParameterSet>("WPlusBJetEventSelection")  )
{
  cout<< "Instantiate WPlusBJetAnalysis" << endl;
  histograms1d["nJet"]  = theDir.make<TH1F>("nJet",   "Number of Jets",     20,   0,    20);
  histograms1d["jetPt"] = theDir.make<TH1F>("jetPt",  "Jet Pt; Jet Pt (GeV/c^{2})",   200,    0,    1000 );
  histograms1d["jetEta"]  = theDir.make<TH1F>("jetEta", "Jet #eta; Jet #eta",     50,   -4.0,     4.0 );
  histograms1d["jetMass"] = theDir.make<TH1F>("jetMass",  "Jet Mass; Jet Mass (GeV/c^{2})",   200,    0,    1000 );
  histograms1d["nW"]      = theDir.make<TH1F>("nW",     "Number of W",    10,   0,    10 );
  histograms1d["nB"]      = theDir.make<TH1F>("nB",     "Number of B",    10,   0,    10 );
  histograms1d["wMass0"]   = theDir.make<TH1F>("wMass0",  "W Jet Mass",     40,   0,    200 );
  histograms1d["wMass1"]   = theDir.make<TH1F>("wMass1",  "W Jet Mass",     40,   0,    200 );
  histograms1d["nTightTopType22"]   = theDir.make<TH1F>("nTightTopType22",    "Number of Tight Top",    10,   0,  10 );
  histograms1d["nLooseTopType22"]   = theDir.make<TH1F>("nLooseTopType22",    "Number of Loose Top",    10,   0,  10 );
  histograms1d["tightTopMass0Type22"]    = theDir.make<TH1F>("tightTopMass0Type22",   "Tight Top Mass; Mass (GeV/c^{2})",   100,  0,  500 );
  histograms1d["looseTopMass0Type22"]    = theDir.make<TH1F>("looseTopMass0Type22",   "Loose Top Mass; Mass (GeV/c^{2})",   100,  0,  500 );
  histograms1d["tightTopMass1Type22"]    = theDir.make<TH1F>("tightTopMass1Type22",   "Tight Top Mass; Mass (GeV/c^{2})",   100,  0,  500 );
  histograms1d["looseTopMass1Type22"]    = theDir.make<TH1F>("looseTopMass1Type22",   "Loose Top Mass; Mass (GeV/c^{2})",   100,  0,  500 );

  histograms1d["tightTopMass0Type23"]    = theDir.make<TH1F>("tightTopMass0Type23",   "Tight Top Mass; Mass (GeV/c^{2})",   100,  0,  500 );
  histograms1d["tightTopMass1Type23"]    = theDir.make<TH1F>("tightTopMass1Type23",   "Tight Top Mass; Mass (GeV/c^{2})",   100,  0,  500 );

  histograms1d["type3TopMass0Type23"]    = theDir.make<TH1F>("type3TopMass0Type23",   "Type 3 Top Mass; Mass (GeV/c^{2})",   100,  0,  500 );
  histograms1d["type3TopMass1Type23"]    = theDir.make<TH1F>("type3TopMass1Type23",   "Type 3 Top Mass; Mass (GeV/c^{2})",   100,  0,  500 );
  histograms1d["minPairMass0Type23"]     = theDir.make<TH1F>("minPairMass0Type23",    "Min Pair Inv Mass; Mass (GeV/c^{2})",  100,  0,  500 );
  histograms1d["minPairMass1Type23"]     = theDir.make<TH1F>("minPairMass1Type23",    "Min Pair Inv Mass; Mass (GeV/c^{2})",  100,  0,  500 );

  histograms1d["type3TopMass0Type33"]    = theDir.make<TH1F>("type3TopMass0Type33",   "Type 3 Top Mass; Mass (GeV/c^{2})",   100,  0,  500 );
  histograms1d["type3TopMass1Type33"]    = theDir.make<TH1F>("type3TopMass1Type33",   "Type 3 Top Mass; Mass (GeV/c^{2})",   100,  0,  500 );
  histograms1d["minPairMass0Type33"]     = theDir.make<TH1F>("minPairMass0Type33",    "Min Pair Inv Mass; Mass (GeV/c^{2})",  100,  0,  500 );
  histograms1d["minPairMass1Type33"]     = theDir.make<TH1F>("minPairMass1Type33",    "Min Pair Inv Mass; Mass (GeV/c^{2})",  100,  0,  500 );

  histograms1d["leadJetPt"]       = theDir.make<TH1F>("leadJetPt",      "Leading Jet Pt",           200,  0,    1000 );
  histograms1d["leadJetEta"]      = theDir.make<TH1F>("leadJetEta",     "Leading Jet #eta",         50,   -4.0, 4.0 );
  histograms1d["minPairDr0Type33"]       = theDir.make<TH1F>("minPairDr0Type33",      "Min Pair #Delta R",        50,   0.0, 6.0 );
  histograms1d["minPairDPhi0Type33"]     = theDir.make<TH1F>("minPairDPhi0Type33",    "Min Pair #Delta Phi",      50,   0,    3. );
  histograms1d["minPairDr1Type33"]       = theDir.make<TH1F>("minPairDr1Type33",      "Min Pair #Delta R",        50,   0.0, 6.0 );
  histograms1d["minPairDPhi1Type33"]     = theDir.make<TH1F>("minPairDPhi1Type33",    "Min Pair #Delta Phi",      50,   0,    3. );

  histograms1d["wbJetDr0Type22"]         = theDir.make<TH1F>("wbJetDr0Type22",        "W and B Jet #Delta R",     50,   0.0, 6.0 );
  histograms1d["wbJetDPhi0Type22"]       = theDir.make<TH1F>("wbJetDPhi0Type22",      "W and B Jet #Delta Phi",   50,   0.,   3. );
  histograms1d["wbJetDr1Type22"]         = theDir.make<TH1F>("wbJetDr1Type22",        "W and B Jet #Delta R",     50,   0.0, 6.0 );
  histograms1d["wbJetDPhi1Type22"]       = theDir.make<TH1F>("wbJetDPhi1Type22",      "W and B Jet #Delta Phi",   50,   0.,   3. );

  histograms1d["waJetDr0Type22"]         = theDir.make<TH1F>("waJetDr0Type22",        "W and A Jet #Delta R",     50,   0.0, 6.0 );
  histograms1d["waJetDPhi0Type22"]       = theDir.make<TH1F>("waJetDPhi0Type22",      "W and A Jet #Delta Phi",   50,   0.,   3. );
  histograms1d["waJetDr1Type22"]         = theDir.make<TH1F>("waJetDr1Type22",        "W and A Jet #Delta R",     50,   0.0, 6.0 );
  histograms1d["waJetDPhi1Type22"]       = theDir.make<TH1F>("waJetDPhi1Type22",      "W and A Jet #Delta Phi",   50,   0.,   3. );


  histograms1d["topPairDPhi"]     = theDir.make<TH1F>("topPairDPhi",    "Top Pair #Delta Phi",      50,   0.,   4. );
  histograms1d["topPairDr"]       = theDir.make<TH1F>("topPairDr",      "Top Pair #Delta R",        50,   0.0,  6.0 );
  histograms1d["pairBJetDPhi0"]    = theDir.make<TH1F>("pairBJetDPhi0",   "Min Pair and B Jet #Delta Phi",  50, 0.0, 3. );
  histograms1d["pairBJetDr0"]      = theDir.make<TH1F>("pairBJetDr0",     "Min Pair and B Jet #Delta R",  50,   0.0,  6 );
  histograms1d["pairBJetDPhi1"]    = theDir.make<TH1F>("pairBJetDPhi1",   "Min Pair and B Jet #Delta Phi",  50, 0.0, 3. );
  histograms1d["pairBJetDr1"]      = theDir.make<TH1F>("pairBJetDr1",     "Min Pair and B Jet #Delta R",  50,   0.0,  6 );

  histograms1d["wJetPt"]          = theDir.make<TH1F>("wJetPt",         "W Jet Pt",                 200,  0,    1000 );
  histograms1d["bJetPt"]          = theDir.make<TH1F>("bJetPt",         "b Jet Pt",                 200,  0,    1000 );
  histograms1d["ttMassType22"]    = theDir.make<TH1F>("ttMassType22",   "t#bar{t} Inv Mass Type22",   200,  0,  2000 );
  histograms1d["ttMassType23"]    = theDir.make<TH1F>("ttMassType23",   "t#bar{t} Inv Mass Type23",   200,  0,  2000 );
  histograms1d["ttMassType33"]    = theDir.make<TH1F>("ttMassType33",   "t#bar{t} Inv Mass Type33",   200,  0,  2000 );

  histograms1d["ttMassType22_pred"]    = theDir.make<TH1F>("ttMassType22_pred",   "t#bar{t} Inv Mass Type22",   200,  0,  2000 );
  histograms1d["ttMassType23_pred"]    = theDir.make<TH1F>("ttMassType23_pred",   "t#bar{t} Inv Mass Type23",   200,  0,  2000 );
  histograms1d["ttMassType33_pred"]    = theDir.make<TH1F>("ttMassType33_pred",   "t#bar{t} Inv Mass Type33",   200,  0,  2000 );


  histograms2d["jetMassVsPt"]     = theDir.make<TH2F>("jetMassVsPt",    "Jet Mass Vs Pt; Jet Pt (GeV/c^{2}); Jet Mass (GeV/c^{2})",    200,  0,    1000,   100,    0,    500 );

}

void WPlusBJetAnalysis::analyze( const edm::EventBase & iEvent )
{
  //cout<<"Point 1"<<endl;

  pat::strbitset retType22 = wPlusBJetType22Selection_.getBitTemplate();
  bool passType22 = wPlusBJetType22Selection_( iEvent, retType22 );

  std::vector<edm::Ptr<pat::Jet> >  const &  pfJets = wPlusBJetType22Selection_.pfJets();
  std::vector<edm::Ptr<pat::Jet> >  const &  tWJets = wPlusBJetType22Selection_.wJet0();
  std::vector<edm::Ptr<pat::Jet> >  const &  oWJets = wPlusBJetType22Selection_.wJet1();
  std::vector<edm::Ptr<pat::Jet> >  const &  tbJets = wPlusBJetType22Selection_.bJet0();
  std::vector<edm::Ptr<pat::Jet> >  const &  obJets = wPlusBJetType22Selection_.bJet1();
  std::vector<edm::Ptr<pat::Jet> >  const &  tMinDrPair = wPlusBJetType22Selection_.minDrPair0();
  std::vector<edm::Ptr<pat::Jet> >  const &  oMinDrPair = wPlusBJetType22Selection_.minDrPair1();
  edm::Ptr<pat::Jet>   const  & taJet = wPlusBJetType22Selection_.aJet0();
  edm::Ptr<pat::Jet>   const  & oaJet = wPlusBJetType22Selection_.aJet1();

  histograms1d["nJet"]      ->  Fill( pfJets.size() );
  for( size_t i=0; i<pfJets.size(); i++ ) {
    histograms1d["jetPt"]     ->  Fill( pfJets.at(i)->pt() );
    histograms1d["jetEta"]    ->  Fill( pfJets.at(i)->eta() );
    histograms1d["jetMass"]   ->  Fill( pfJets.at(i)->mass() );
    if( i==0 ) {
      histograms1d["leadJetPt"]       ->  Fill( pfJets.at(0)->pt() );
      histograms1d["leadJetEta"]      ->  Fill( pfJets.at(0)->eta() );
    }
    if( pfJets.at(i)->pt() > 200 )
      histograms2d["jetMassVsPt"]     ->  Fill( pfJets.at(i)->pt() , pfJets.at(i)->mass() );
  }

  if( retType22[string("Leading Jet Pt")] ) {
    int numWJets = tWJets.size() + oWJets.size();
    int numBJets = tbJets.size() + obJets.size();

    histograms1d["nW"]      ->  Fill( numWJets );
    histograms1d["nB"]      ->  Fill( numBJets );
    if( tWJets.size() >= 1 ) {
      histograms1d["wMass0"]      ->  Fill( tWJets.at(0)->mass() );
      histograms1d["wJetPt"]      ->  Fill( tWJets.at(0)->pt() );
    }
    if( oWJets.size() >= 1 ) {
      histograms1d["wMass1"]      ->  Fill( oWJets.at(0)->mass() );
      histograms1d["wJetPt"]      ->  Fill( oWJets.at(0)->pt() );
    }
    if( tbJets.size() >=1 ) 
      histograms1d["bJetPt"]      ->  Fill( tbJets.at(0)->pt() );
    if( obJets.size() >=1 )
      histograms1d["bJetPt"]      ->  Fill( obJets.at(0)->pt() );

    if( retType22[string("hasTwoTops")] ) {
      int numTightTop=0, numLooseTop=0;
      reco::Candidate::LorentzVector const p4_top0 = wPlusBJetType22Selection_.p4_top0();
      reco::Candidate::LorentzVector const p4_top1 = wPlusBJetType22Selection_.p4_top1();

      if ( wPlusBJetType22Selection_.hasTightTop0() ) {
        numTightTop++;
        double deltaR = reco::deltaR<double>( tWJets.at(0)->eta(), tWJets.at(0)->phi(), tbJets.at(0)->eta(), tbJets.at(0)->phi() );
        double deltaPhi = fabs( reco::deltaPhi<double>( tWJets.at(0)->phi(), tbJets.at(0)->phi() ) );
        histograms1d["wbJetDr0Type22"]            ->  Fill( deltaR );
        histograms1d["wbJetDPhi0Type22"]          ->  Fill( deltaPhi );
        histograms1d["tightTopMass0Type22"]       ->  Fill( p4_top0.mass() );
      }
      else {
        numLooseTop++;
        double deltaR = reco::deltaR<double>( tWJets.at(0)->eta(), tWJets.at(0)->phi(), taJet->eta(), taJet->phi() );
        double deltaPhi = fabs( reco::deltaPhi<double>( tWJets.at(0)->phi(), taJet->phi() ) );
        histograms1d["waJetDr0Type22"]            ->  Fill( deltaR );
        histograms1d["waJetDPhi0Type22"]          ->  Fill( deltaPhi );
        histograms1d["looseTopMass0Type22"]       ->  Fill( p4_top0.mass() );
      }
      if( wPlusBJetType22Selection_.hasTightTop1()  ) {
        numTightTop++;
        double deltaR = reco::deltaR<double>( oWJets.at(0)->eta(), oWJets.at(0)->phi(), obJets.at(0)->eta(), obJets.at(0)->phi() );
        double deltaPhi = fabs( reco::deltaPhi<double>( oWJets.at(0)->phi(), obJets.at(0)->phi() ) );
        histograms1d["wbJetDr1Type22"]            ->  Fill( deltaR );
        histograms1d["wbJetDPhi1Type22"]          ->  Fill( deltaPhi );
        histograms1d["tightTopMass1Type22"]       ->  Fill( p4_top1.mass() );
      }
      else  {
        numLooseTop++;
        double deltaR = reco::deltaR<double>( oWJets.at(0)->eta(), oWJets.at(0)->phi(), oaJet->eta(), oaJet->phi() );
        double deltaPhi = fabs( reco::deltaPhi<double>( oWJets.at(0)->phi(), oaJet->phi() ) );
        histograms1d["waJetDr1Type22"]            ->  Fill( deltaR );
        histograms1d["waJetDPhi1Type22"]          ->  Fill( deltaPhi );
        histograms1d["looseTopMass1Type22"]       ->  Fill( p4_top1.mass() );
      }
      histograms1d["nTightTopType22"]   ->  Fill( numTightTop );
      histograms1d["nLooseTopType22"]   ->  Fill( numLooseTop );

      if( passType22 ) {
        histograms1d["ttMassType22"]    ->  Fill( (p4_top0+p4_top1).mass() );
        double deltaR = reco::deltaR<double>( p4_top0.eta(), p4_top0.phi(), p4_top1.eta(), p4_top1.phi() );
        double deltaPhi = fabs( reco::deltaPhi<double>( p4_top0.phi(), p4_top1.phi() ) );
        histograms1d["topPairDPhi"]     ->  Fill( deltaPhi );
        histograms1d["topPairDr"]       ->  Fill( deltaR );
      }
    } // end if ret hasTwoTops
  } // end if ret leading jet pt


  if( retType22[string(">= 1 WJet")] && !retType22[string(">= 2 WJet")] ) {
    pat::strbitset retType23 = wPlusBJetType23Selection_.getBitTemplate();
    bool passType23 = wPlusBJetType23Selection_( iEvent, retType23 );
    if( retType23[string("hasMinPair")] ) {
      reco::Candidate::LorentzVector const p4_top0 = wPlusBJetType23Selection_.p4_top0();
      reco::Candidate::LorentzVector const p4_top1 = wPlusBJetType23Selection_.p4_top1();
      if( tMinDrPair.size() == 2 ) {
        double minPairMass = (tMinDrPair.at(0)->p4()+tMinDrPair.at(1)->p4()).mass();
        histograms1d["minPairMass0Type23"]      ->  Fill( minPairMass );
        if( retType23[string("minPairMassCut")] ) {
          histograms1d["type3TopMass0Type23"]   ->  Fill( p4_top0.mass() );
          histograms1d["tightTopMass1Type23"]   ->  Fill( p4_top1.mass() );
        }
      } // end tMinDrPair
      else {
        double minPairMass = (oMinDrPair.at(0)->p4()+oMinDrPair.at(1)->p4()).mass();
        histograms1d["minPairMass1Type23"]      ->  Fill( minPairMass );
        if( retType23[string("minPairMassCut")] ) {
          histograms1d["type3TopMass1Type23"]   ->  Fill( p4_top1.mass() );
          histograms1d["tightTopMass0Type23"]   ->  Fill( p4_top0.mass() );
        }
      } // end else
      if( passType23 ) {
        histograms1d["ttMassType23"]    ->  Fill( (p4_top0+p4_top1).mass() );
        double deltaR = reco::deltaR<double>( p4_top0.eta(), p4_top0.phi(), p4_top1.eta(), p4_top1.phi() );
        double deltaPhi = fabs( reco::deltaPhi<double>( p4_top0.phi(), p4_top1.phi() ) );
        histograms1d["topPairDPhi"]     ->  Fill( deltaPhi );
        histograms1d["topPairDr"]       ->  Fill( deltaR );        
      } // end passType23
    }  // hasMinPair    
  }  // end if >= 1 WJet and !>= 2 WJet

  if( !retType22[string(">= 1 WJet")] ) {
    pat::strbitset  retType33 = wPlusBJetType33Selection_.getBitTemplate();
    bool passType33 = wPlusBJetType33Selection_( iEvent, retType33 );

    if( retType33[string("hasMinPair1")] )  {
      reco::Candidate::LorentzVector const p4_top0 = wPlusBJetType33Selection_.p4_top0();
      reco::Candidate::LorentzVector const p4_top1 = wPlusBJetType33Selection_.p4_top1();
      reco::Candidate::LorentzVector  p4_first0 = tMinDrPair.at(0)->p4();
      reco::Candidate::LorentzVector  p4_second0  = tMinDrPair.at(1)->p4();
      reco::Candidate::LorentzVector  p4_first1 = oMinDrPair.at(0)->p4();
      reco::Candidate::LorentzVector  p4_second1  = oMinDrPair.at(1)->p4();
      double dR0 = reco::deltaR<double>( p4_first0.eta(), p4_first0.phi(), p4_second0.eta(), p4_second0.phi() );
      double dR1 = reco::deltaR<double>( p4_first1.eta(), p4_first1.phi(), p4_second1.eta(), p4_second1.phi() );
      double dPhi0 = fabs( reco::deltaPhi<double> ( p4_first0.phi(), p4_second0.phi() ) );
      double dPhi1 = fabs( reco::deltaPhi<double> ( p4_first1.phi(), p4_second1.phi() ) );
      histograms1d["minPairDr0Type33"]    ->  Fill( dR0 );
      histograms1d["minPairDPhi0Type33"]  ->  Fill( dPhi0 );
      histograms1d["minPairDr1Type33"]    ->  Fill( dR1 );
      histograms1d["minPairDPhi1Type33"]  ->  Fill( dPhi1 );
      histograms1d["minPairMass0Type33"]  ->  Fill( (p4_first0+p4_second0).mass() );
      histograms1d["minPairMass1Type33"]  ->  Fill( (p4_first1+p4_second1).mass() );
      if( retType33[string("minPairMassCut")] ) {
        histograms1d["type3TopMass0Type33"]   ->  Fill( p4_top0.mass() );
        histograms1d["type3TopMass1Type33"]   ->  Fill( p4_top1.mass() );
      }
      if( passType33 )  {
        histograms1d["ttMassType33"]    ->  Fill( (p4_top0+p4_top1).mass() );
        double deltaR = reco::deltaR<double>( p4_top0.eta(), p4_top0.phi(), p4_top1.eta(), p4_top1.phi() );
        double deltaPhi = fabs( reco::deltaPhi<double>( p4_top0.phi(), p4_top1.phi() ) ) ;
        histograms1d["topPairDPhi"]     ->  Fill( deltaPhi );
        histograms1d["topPairDr"]       ->  Fill( deltaR );
      }
    }  // hasMinPair1
  }  // end if !>= 1 WJet

  std::vector<Type2L>     const & looseTops0  = wPlusBJetType22Selection_.looseTops0();
  std::vector<Type2T>     const & tightTops0  = wPlusBJetType22Selection_.tightTops0();
  std::vector<Type3>      const & type3Tops0  = wPlusBJetType22Selection_.type3Tops0();  
  std::vector<Type2L>     const & looseTops1  = wPlusBJetType22Selection_.looseTops1();
  std::vector<Type2T>     const & tightTops1  = wPlusBJetType22Selection_.tightTops1();
  std::vector<Type3>      const & type3Tops1  = wPlusBJetType22Selection_.type3Tops1();

  //cout<<"bein here"<<endl;
  //for type2+type2
  for( size_t i=0; i<tightTops0.size(); i++ ) {
    for( size_t j=0; j<tightTops1.size(); j++ ) {
      FourVector top0 = tightTops0.at(i).top();
      FourVector top1 = tightTops1.at(j).top();
      if( top0.mass() > 140 && top0.mass() < 230 && top1.mass() > 140 && top1.mass() < 230 ) {
        double weight = tightTops0.at(i).weight * tightTops1.at(j).weight;
        histograms1d["ttMassType22_pred"]   ->  Fill( (top0+top1).mass(), weight );
      }
    } // end j
    for( size_t j=0; j<looseTops1.size(); j++ ) {
      const FourVector top0 = tightTops0.at(i).top();
      const FourVector top1 = looseTops1.at(j).top();
      if( top0.mass() > 140 && top0.mass() < 230 && top1.mass() > 140 && top1.mass() < 230 ) {
        double weight = tightTops0.at(i).weight * looseTops1.at(j).weight;
        histograms1d["ttMassType22_pred"]   ->  Fill( (top0+top1).mass(), weight );
      }
    }  // end j
  } // end i

  //cout<<"Point1"<<endl;

  for( size_t i=0; i<looseTops0.size(); i++ ) {
    for( size_t j=0; j<tightTops1.size(); j++ ) {
      const FourVector top0 = looseTops0.at(i).top();
      const FourVector top1 = tightTops1.at(j).top();
      if( top0.mass() > 140 && top0.mass() < 230 && top1.mass() > 140 && top1.mass() < 230 ) {
        double weight = looseTops0.at(i).weight * tightTops1.at(j).weight;
        histograms1d["ttMassType22_pred"]   ->  Fill( (top0+top1).mass(), weight );
      }
    } // end j
  } // end i

  //cout<<"Point2"<<endl;
  // for type2+type3
  for( size_t i=0; i<tightTops0.size(); i++ ) {
    for( size_t j=0; j<type3Tops1.size(); j++ ) {
      const FourVector top0 = tightTops0.at(i).top();
      const FourVector top1 = type3Tops1.at(j).top();
      if( top0.mass() > 140 && top0.mass() < 230 && top1.mass() > 140 && top1.mass() < 230 && 
          type3Tops1.at(j).minMass() > 50 && type3Tops1.at(j).minMass() < 100) {
        double weight = tightTops0.at(i).weight * type3Tops1.at(j).weight;
        histograms1d["ttMassType23_pred"]   ->  Fill( (top0+top1).mass(), weight );
      }
    } // end j
  } // end i

  //cout<<"Point3"<<endl;
  for( size_t i=0; i<type3Tops0.size(); i++ ) {
    for( size_t j=0; j<tightTops1.size(); j++ ) {
      const FourVector top0 = type3Tops0.at(i).top();
      const FourVector top1 = tightTops1.at(j).top();
      if( top0.mass() > 140 && top0.mass() < 230 && top1.mass() > 140 && top1.mass() < 230 &&
          type3Tops0.at(i).minMass() > 50 && type3Tops0.at(i).minMass() < 100 ) {
        double weight = type3Tops0.at(i).weight * tightTops1.at(j).weight;
        histograms1d["ttMassType23_pred"]   ->  Fill( (top0+top1).mass(), weight );
      }
    } // end j
  } // end i
  //cout<<"Point4"<<endl;

  // for type3+type3
  for( size_t i=0; i<type3Tops0.size(); i++ ) {
    for( size_t j=0; j<type3Tops1.size(); j++ ) {
      const FourVector top0 = type3Tops0.at(i).top();
      const FourVector top1 = type3Tops1.at(j).top();
      if( top0.mass() > 140 && top0.mass() < 230 && top1.mass() > 140 && top1.mass() < 230 &&
          type3Tops0.at(i).minMass() > 50 && type3Tops0.at(i).minMass() < 100 && 
          type3Tops1.at(j).minMass() > 50 && type3Tops1.at(j).minMass() < 100 ) {
        double weight = type3Tops0.at(i).weight * type3Tops1.at(j).weight;
        histograms1d["ttMassType23_pred"]   ->  Fill( (top0+top1).mass(), weight );
      }
    } // end j
  } // end i
  //cout<<"end"<<endl;
}
