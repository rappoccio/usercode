#include "Analysis/BoostedTopAnalysis/interface/WPlusBJetAnalysis.h"
using namespace std;

WPlusBJetAnalysis::WPlusBJetAnalysis( const edm::ParameterSet & iConfig,  TFileDirectory & iDir ) :
  theDir( iDir ),
  jetSrc_( iConfig.getParameter<edm::InputTag>("jetSrc") ),
  twPlusBJetSelection_ ( iConfig.getParameter<edm::ParameterSet>("WPlusBJetSelection") ),
  owPlusBJetSelection_ (twPlusBJetSelection_ )
{
  cout<< "Instantiate WPlusBJetAnalysis" << endl;
  histograms1d["nJet"]  = theDir.make<TH1F>("nJet",   "Number of Jets",     20,   0,    20);
  histograms1d["jetPt"] = theDir.make<TH1F>("jetPt",  "Jet Pt; Jet Pt (GeV/c^{2})",   200,    0,    1000 );
  histograms1d["jetEta"]  = theDir.make<TH1F>("jetEta", "Jet #eta; Jet #eta",     50,   -3.0,     3.0 );
  histograms1d["jetMass"] = theDir.make<TH1F>("jetMass",  "Jet Mass; Jet Mass (GeV/c^{2})",   200,    0,    1000 );
  histograms1d["nW"]      = theDir.make<TH1F>("nW",     "Number of W",    10,   0,    10 );
  histograms1d["nB"]      = theDir.make<TH1F>("nB",     "Number of B",    10,   0,    10 );
  histograms1d["wMass"]   = theDir.make<TH1F>("wMass",  "W Jet Mass",     40,   0,    200 );
  histograms1d["nTightTop"]   = theDir.make<TH1F>("nTightTop",    "Number of Tight Top",    10,   0,  10 );
  histograms1d["nLooseTop"]   = theDir.make<TH1F>("nLooseTop",    "Number of Loose Top",    10,   0,  10 );
  histograms1d["tightTopMass"]    = theDir.make<TH1F>("tightTopMass",   "Tight Top Mass; Mass (GeV/c^{2})",   100,  0,  500 );
  histograms1d["looseTopMass"]    = theDir.make<TH1F>("looseTopMass",   "Loose Top Mass; Mass (GeV/c^{2})",   100,  0,  500 );
  histograms1d["type3TopMass"]    = theDir.make<TH1F>("type3TopMass",   "Type 3 Top Mass; Mass (GeV/c^{2})",   100,  0,  500 );
  histograms1d["ttMass"]          = theDir.make<TH1F>("ttMass",         "t#bar{t} Inv Mass; Mass (GeV/c^{2})",  200,  0,  2000 );
  histograms1d["minPairMass"]     = theDir.make<TH1F>("minPairMass",    "Min Pair Inv Mass; Mass (GeV/c^{2})",  100,  0,  500 );
  histograms1d["nType3Top"]       = theDir.make<TH1F>("nType3Top",      "Number of Type 3 Top",     10,   0,    10 );
  histograms1d["leadJetPt"]       = theDir.make<TH1F>("leadJetPt",      "Leading Jet Pt",           200,  0,    1000 );
  histograms1d["minPairDr"]       = theDir.make<TH1F>("minPairDr",      "Min Pair #Delta R",        50,   0.0, 6.0 );
  histograms1d["wbJetDr"]         = theDir.make<TH1F>("wbJetDr",        "W and B Jet #Delta R",     50,   0.0, 6.0 );
  histograms1d["waJetDr"]         = theDir.make<TH1F>("waJetDr",        "W and A Jet #Delta R",     50,   0.0, 6.0 );
  

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
  if( theJet->pt() < 160 )   return ;

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

  if( tret[std::string(">= 1 WJet")] )
    histograms1d["wMass"]     ->  Fill( tWJets.at(0)->mass() );
  if( oret[std::string(">= 1 WJet")] )
    histograms1d["wMass"]     ->  Fill( oWJets.at(0)->mass() );
  
  //cout<<"Point 3"<<endl;

  int numTightTop = 0, numLooseTop = 0, numType3Top = 0;

  reco::Candidate::LorentzVector p4_top1(0,0,0,0), p4_top2(0,0,0,0);

  if( tret[std::string(">= 1 bJet")] ) {   // find a tight top
    //cout<<"I"<<endl;
    reco::Candidate::LorentzVector p4_W( tWJets.at(0)->p4() );
    reco::Candidate::LorentzVector p4_b( tbJets.at(0)->p4() );
    p4_top1 = p4_W + p4_b;
    double wbJetDr = reco::deltaR<double>( p4_W.eta(), p4_W.phi() , p4_b.eta(), p4_b.phi() );
    histograms1d["wbJetDr"]           ->  Fill( wbJetDr );

    histograms1d["tightTopMass"]      ->  Fill( p4_top1.mass() );
    numTightTop ++;
    //cout<<"Point I"<<endl;

  }
  else if( tret[std::string(">= 1 WJet")] && twPlusBJetSelection_.aJetFound() )  {  // find a loose top 
    //cout<<"II"<<endl;
    reco::Candidate::LorentzVector p4_W( tWJets.at(0)->p4() );
    reco::Candidate::LorentzVector p4_a( taJet->p4() );
    p4_top1 = p4_W + p4_a;
    double waJetDr  = reco::deltaR<double>( p4_W.eta(), p4_W.phi(), p4_a.eta(), p4_a.phi() );
    histograms1d["waJetDr"]         ->  Fill( waJetDr );

    histograms1d["looseTopMass"]      ->  Fill( p4_top1.mass() );
    numLooseTop ++;
    //cout<<"Point II"<<endl;
  }
  else if( tMinDrPair.size() == 2 && tbJets.size() >= 1 && numWJets >= 1 && numBJets >= 1 ) { // Check the minDrPair
    //cout<<"III"<<endl;
    reco::Candidate::LorentzVector p4_0( tMinDrPair.at(0)->p4() );
    reco::Candidate::LorentzVector p4_1( tMinDrPair.at(1)->p4() );
    reco::Candidate::LorentzVector p4_pair = p4_0 + p4_1;
    double minPairMass = p4_pair.mass();
    histograms1d["minPairMass"]       ->  Fill( minPairMass );
    double minPairDr = reco::deltaR<double>( p4_0.eta(), p4_0.phi(), p4_1.eta(), p4_1.phi() );
    histograms1d["minPairDr"]     ->  Fill( minPairDr );

    if( minPairMass > 50 && minPairMass < 100 )  {
      numType3Top ++;
      reco::Candidate::LorentzVector p4_b( tbJets.at(0)->p4() );
      p4_top1 = p4_0 + p4_1 + p4_b ;
      histograms1d["type3TopMass"]      ->  Fill( p4_top1.mass() );
    //cout<<"Point III"<<endl;
    }

  }

  //cout<<"Point a"<<endl;


  if( oret[std::string(">= 1 bJet")] ) {   // find a tight top
    reco::Candidate::LorentzVector p4_W( oWJets.at(0)->p4() );
    reco::Candidate::LorentzVector p4_b( obJets.at(0)->p4() );
    p4_top2 = p4_W + p4_b;
    double wbJetDr = reco::deltaR<double>( p4_W.eta(), p4_W.phi() , p4_b.eta(), p4_b.phi() );
    histograms1d["wbJetDr"]           ->  Fill( wbJetDr );

    histograms1d["tightTopMass"]      ->  Fill( p4_top2.mass() );
    numTightTop ++;
    //cout<<"Point aa"<<endl;

  }
  else if( oret[std::string(">= 1 WJet")] && owPlusBJetSelection_.aJetFound() )  {  // find a loose top 
    reco::Candidate::LorentzVector p4_W( oWJets.at(0)->p4() );
    reco::Candidate::LorentzVector p4_a( oaJet->p4() );
    p4_top2 = p4_W + p4_a;
    double waJetDr  = reco::deltaR<double>( p4_W.eta(), p4_W.phi(), p4_a.eta(), p4_a.phi() );
    histograms1d["waJetDr"]         ->  Fill( waJetDr );

    histograms1d["looseTopMass"]      ->  Fill( p4_top2.mass() );
    numLooseTop ++;
    //cout<<"Point bb"<<endl;
  }
  else if( oMinDrPair.size() == 2 && obJets.size() >= 1 && numWJets >= 1 && numBJets >= 1) { // Check the minDrPair
    reco::Candidate::LorentzVector p4_0( oMinDrPair.at(0)->p4() );
    reco::Candidate::LorentzVector p4_1( oMinDrPair.at(1)->p4() );
    reco::Candidate::LorentzVector p4_pair = p4_0 + p4_1;
    double minPairMass = p4_pair.mass();
    histograms1d["minPairMass"]       ->  Fill( minPairMass );
    double minPairDr = reco::deltaR<double>( p4_0.eta(), p4_0.phi(), p4_1.eta(), p4_1.phi() );
    histograms1d["minPairDr"]     ->  Fill( minPairDr );

    if( minPairMass > 50 && minPairMass < 100 )  {
      numType3Top ++;
      reco::Candidate::LorentzVector p4_b( obJets.at(0)->p4() );
      p4_top2 = p4_0 + p4_1 + p4_b ;
      histograms1d["type3TopMass"]      ->  Fill( p4_top2.mass() );
    }
    //cout<<"Point cc"<<endl;

  }
  
  if( p4_top1.mass() > 100 && p4_top2.mass() > 100 )  {
    histograms1d["ttMass"]      ->  Fill( (p4_top1+p4_top2).mass() );
  }

  histograms1d["nTightTop"]     ->  Fill( numTightTop );
  histograms1d["nLooseTop"]     ->  Fill( numLooseTop );
  histograms1d["nType3Top"]     ->  Fill( numType3Top );

  //cout<<"Point 4"<<endl;
  //cout<<"Number of W Jets\t"<<twPlusBJetSelection_.wJets().size()<<"\t"<<owPlusBJetSelection_.wJets().size()<<endl;
  //cout<<"Number of B Jets\t"<<twPlusBJetSelection_.bJets().size()<<"\t"<<owPlusBJetSelection_.bJets().size()<<endl;
  //cout<<"Number of min pair\t"<<twPlusBJetSelection_.minDrPair().size()<<"\t"<<owPlusBJetSelection_.minDrPair().size()<<endl;


}
