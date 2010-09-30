#include "Analysis/SHyFT/interface/SHyFT.h"


using namespace std;


SHyFT::SHyFT(const edm::ParameterSet& iConfig, TFileDirectory& iDir) :
  wPlusJets(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis")),
  theDir(iDir),
  muPlusJets_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<bool>("muPlusJets")),
  ePlusJets_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<bool>("ePlusJets")),
  useHFcat_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<bool>("heavyFlavour")),
  nJetsCut_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<int>("minJets")),  
  mode(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<int>("mode")),
  sampleNameInput(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<std::string>("sampleName")),
  doMC_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<bool>("doMC") )
{
  //book all the histograms for muons
  histograms["muPt"]     = theDir.make<TH1F>("muPt",     "Muon p_{T} (GeV/c) ", 100,    0, 200);
  histograms["muEta"]    = theDir.make<TH1F>("muEta",    "Muon eta",             50, -3.0, 3.0);
  histograms["nHits"]    = theDir.make<TH1F>("nHits",    "Muon N Hits",          35,    0,  35);
  histograms["d0"]       = theDir.make<TH1F>("d0",       "Muon D0",              60, -0.2, 0.2);
  histograms["Chi2"]     = theDir.make<TH1F>("Chi2",     "Muon Chi2",            20,    0,   5);
  histograms["hCalVeto"] = theDir.make<TH1F>("hCalVeto", "Muon hCalVeto",        30,    0,  30);
  histograms["eCalVeto"] = theDir.make<TH1F>("eCalVeto", "Muon eCalVeto",        30,    0,  30);

  // book all the histograms for electrons
  histograms["ePt"]  = theDir.make<TH1F>("ePt",  "Electron p_{T} (GeV/c) ", 100,    0, 200);
  histograms["eEta"] = theDir.make<TH1F>("eEta", "Electron eta",             50, -3.0, 3.0);
  histograms["ePhi"] = theDir.make<TH1F>("ePhi", "Electron Phi",             50, -3.2, 3.2);
  histograms["eD0"]  = theDir.make<TH1F>("eD0",  "Electron D0",              60, -0.2, 0.2);

  histograms["metPt"] = theDir.make<TH1F>("metPt", "Missing p_{T} (GeV/c)", 100, 0, 200 );

  histograms2d["massVsPt"] = theDir.make<TH2F>("massVsPt", "Mass vs pt", 25, 0, 250, 25, 0, 500);

  std::vector<std::string> sampleNameBase;
  std::vector<std::string> sampleName;
  std::vector<std::string> secvtxName(5,"_secvtxMass_");
  secvtxName[0]+="1j_"; secvtxName[1]+="2j_"; secvtxName[2]+="3j_"; secvtxName[3]+="4j_"; secvtxName[4]+="5j_";
  
  std::vector<std::string> secvtxEnd;
  secvtxEnd.push_back("1t_b");  secvtxEnd.push_back("1t_c");  secvtxEnd.push_back("1t_q");
  secvtxEnd.push_back("1t_x");  secvtxEnd.push_back("1t");    secvtxEnd.push_back("2t_bb");
  secvtxEnd.push_back("2t_bc"); secvtxEnd.push_back("2t_bq"); secvtxEnd.push_back("2t_cc");
  secvtxEnd.push_back("2t_cq"); secvtxEnd.push_back("2t_qq"); secvtxEnd.push_back("2t");
  secvtxEnd.push_back("2t_xx");

  if(sampleNameInput=="Vqq") {
    sampleNameBase.push_back(sampleNameInput+"W");
    sampleNameBase.push_back(sampleNameInput+"Z");
    sampleNameBase.push_back(sampleNameInput+"X");
    for(int i=0;i<3;++i) {
      sampleName.push_back(sampleNameBase[i]+"bb");
      sampleName.push_back(sampleNameBase[i]+"b2");
      sampleName.push_back(sampleNameBase[i]+"cc");
      sampleName.push_back(sampleNameBase[i]+"c2");
    }
  }
  else if (sampleNameInput=="Wjets") {
    sampleName.push_back("Wjetsb3");
    sampleName.push_back("Wjetsc3");
  }
  else sampleName.push_back(sampleNameInput);

  //Calibration Plots
  histograms["wMT"]           = theDir.make<TH1F>("wMT", "W Transverse Mass",           200,    0,  200);
  histograms["trackIso"]      = theDir.make<TH1F>("trackIso", "TrackIso",                50,    0,   50);
  histograms["eCalIso"]       = theDir.make<TH1F>("eCalIso",  "eCalIso",                 80,    0,   40);
  histograms["hCalIso"]       = theDir.make<TH1F>("hCalIso",  "hCalIso",                 60,    0,   30);
  histograms["relIso"]        = theDir.make<TH1F>("relIso",   "RelIso",                  50,    0,    5);
  histograms["nJets"]         = theDir.make<TH1F>("nJets",    "N Jets, pt>30, eta<2.4",  15,    0,   15);
  histograms["jet1Pt"]        = theDir.make<TH1F>("jet1Pt",   "1st leading jet pt",     150,    0,  300);
  histograms["jet2Pt"]        = theDir.make<TH1F>("jet2Pt",   "2nd leading jet pt",     150,    0,  300);
  histograms["jet3Pt"]        = theDir.make<TH1F>("jet3Pt",   "3rd leading jet pt",     150,    0,  300);
  histograms["jet4Pt"]        = theDir.make<TH1F>("jet4Pt",   "4th leading jet pt",     150,    0,  300);
  histograms["jet1Eta"]       = theDir.make<TH1F>("jet1Eta",  "1st leading jet eta",     50, -3.0,  3.0);
  histograms["jet2Eta"]       = theDir.make<TH1F>("jet2Eta",  "2nd leading jet eta",     50, -3.0,  3.0);
  histograms["jet3Eta"]       = theDir.make<TH1F>("jet3Eta",  "3rd leading jet eta",     50, -3.0,  3.0);
  histograms["jet4Eta"]       = theDir.make<TH1F>("jet4Eta",  "4th leading jet eta",     50, -3.0,  3.0);
  histograms["jet1PtTrueRes"] = theDir.make<TH1F>("jet1PtTrueRes",   "1st leading jet pt / gen pt",     150,    0,  3);
  histograms["jet2PtTrueRes"] = theDir.make<TH1F>("jet2PtTrueRes",   "2nd leading jet pt / gen pt",     150,    0,  3);
  histograms["jet3PtTrueRes"] = theDir.make<TH1F>("jet3PtTrueRes",   "3rd leading jet pt / gen pt",     150,    0,  3);
  histograms["jet4PtTrueRes"] = theDir.make<TH1F>("jet4PtTrueRes",   "4th leading jet pt / gen pt",     150,    0,  3);
  histograms["jet1Mass"]      = theDir.make<TH1F>("jet1Mass", "1st leading jet mass",    50,    0,  150);
  histograms["jet2Mass"]      = theDir.make<TH1F>("jet2Mass", "2nd leading jet mass",    50,    0,  150);
  histograms["jet3Mass"]      = theDir.make<TH1F>("jet3Mass", "3rd leading jet mass",    50,    0,  150);
  histograms["jet4Mass"]      = theDir.make<TH1F>("jet4Mass", "4th leading jet mass",    50,    0,  150);
  histograms["bmass"]         = theDir.make<TH1F>("bmass",    "B Sec Vtx Mass",          28,    0,    7);
  histograms["cmass"]         = theDir.make<TH1F>("cmass",    "C Sec Vtx Mass",          28,    0,    7);
  histograms["lfmass"]        = theDir.make<TH1F>("lfmass",   "LF Sec Vtx Mass",         28,    0,    7);
  histograms["flavorHistory"] = theDir.make<TH1F>("flavorhistory", "Flavor History",     12,    0,   12);
  histograms["discriminator"] = theDir.make<TH1F>("discriminator", "BTag Discriminator", 30,    2,    8);
  histograms["nVertices"]     = theDir.make<TH1F>("nVertices",     "num sec Vertices",    5,    0,    5);
  /*  ev.add ( new TH1F( TString("beff_pt0to50"),    "0 non-b untag, 1 b untag, 2 non-b tag, 3 b tag",      4,    0,      4) );
  ev.add ( new TH1F( TString("beff_pt50to100"),  "0 non-b untag, 1 b untag, 2 non-b tag, 3 b tag",      4,    0,      4) );
  ev.add ( new TH1F( TString("beff_pt100to150"), "0 non-b untag, 1 b untag, 2 non-b tag, 3 b tag",      4,    0,      4) );
  ev.add ( new TH1F( TString("beff_pt150to200"), "0 non-b untag, 1 b untag, 2 non-b tag, 3 b tag",      4,    0,      4) );
  ev.add ( new TH1F( TString("beff_pt200to250"), "0 non-b untag, 1 b untag, 2 non-b tag, 3 b tag",      4,    0,      4) );
  ev.add ( new TH1F( TString("beff_pt250to300"), "0 non-b untag, 1 b untag, 2 non-b tag, 3 b tag",      4,    0,      4) );
  ev.add ( new TH1F( TString("beff_pt300plus"),  "0 non-b untag, 1 b untag, 2 non-b tag, 3 b tag",      4,    0,      4) );
  */
  histograms["tag_eff"]    = theDir.make<TH1F>("tag_eff", "0 lf untag, 1 c untag, 2 b untag, 3 lf tag, 4 c tag, 5 b tag", 6, 0, 6);
  histograms["tag_jet_pt"] = theDir.make<TH1F>("tag_jet_pt", "JetPt to go with tagging efficiency", 150,    0,    300);

  histograms[sampleNameInput+"_hT"]    = theDir.make<TH1F>( (sampleNameInput+"_hT").c_str(),    "HT using Et is the sum of Jet Et plus Muon Pt", 50, 0,  1200);
  histograms[sampleNameInput+"_hT_1j"] = theDir.make<TH1F>( (sampleNameInput+"_hT_1j").c_str(), "HT using Pt is the sum of Jet Et plus Muon Pt", 10,  50, 300);
  histograms[sampleNameInput+"_hT_2j"] = theDir.make<TH1F>( (sampleNameInput+"_hT_2j").c_str(), "HT using Pt is the sum of Jet Et plus Muon Pt", 10,  80, 500);
  histograms[sampleNameInput+"_hT_3j"] = theDir.make<TH1F>( (sampleNameInput+"_hT_3j").c_str(), "HT using Pt is the sum of Jet Et plus Muon Pt", 10, 110, 600);
  histograms[sampleNameInput+"_hT_4j"] = theDir.make<TH1F>( (sampleNameInput+"_hT_4j").c_str(), "HT using Pt is the sum of Jet Et plus Muon Pt",  5, 140, 600);
  histograms[sampleNameInput+"_hT_5j"] = theDir.make<TH1F>( (sampleNameInput+"_hT_5j").c_str(), "HT using Pt is the sum of Jet Et plus Muon Pt",  5, 170, 600);
  //histograms[sampleNameInput+"_hTvsNJet"] = theDir.make<TH2F>( (sampleNameInput+"_hTvsNJet").c_str(),  "HT as a function of NJets", 5, 0.5, 5.5, 50, 0, 1200);
  //ev.add ( new TH1F( sampleNameInput+TString("_hTUsingPt"), "HT s is Sum of Jet Pt", 50, 0, 1200) );

  for (unsigned int j=0;j<sampleName.size();++j) {
    for(unsigned int k=0;k<secvtxName.size();++k) {
      for(unsigned int l=0;l<secvtxEnd.size();++l) {
	std::string temp = sampleName[j]+secvtxName[k]+secvtxEnd[l];
        histograms[temp] = theDir.make<TH1F>(temp.c_str(), "secvtxmass", 40,    0,   10);
        if(k==0 && l==4) break;
      }
    }
  }

}


// fill the plots for the electrons
bool SHyFT::analyze_electrons(const std::vector<reco::ShallowClonePtrCandidate>& electrons)
{
  if ( electrons.size() == 0 )  return false;
  const pat::Electron * electron_ = dynamic_cast<const pat::Electron*>(&electrons[0]);
  double ePt_      = electron_ ->pt();
  double eEta_     = electron_ ->eta();
  double ePhi_     = electron_ ->phi();
  double eD0_      = electron_ ->dB();
  //double trackIso_ = electron_ ->trackIso();
  //double eCalIso_  = electron_ ->ecalIso();
  //double hCalIso_  = electron_ ->hcalIso();
  //double relIso_   = ( trackIso_ + eCalIso_ + hCalIso_ )/ePt_ ;

  histograms["ePt"]->Fill( ePt_ );
  histograms["eEta"]->Fill( eEta_ );
  histograms["ePhi"]->Fill( ePhi_ );
  histograms["eD0"]->Fill( eD0_ );

  return true;
}

// fill the plots for the muons
bool SHyFT::analyze_muons(const std::vector<reco::ShallowClonePtrCandidate>& muons)
{
  const pat::Muon * globalMuon = NULL;
  for ( ShallowCloneCollection::const_iterator muonBegin = muons.begin(),
          muonEnd = muons.end(), imuon = muonBegin;
        imuon != muonEnd; ++imuon ) {
    if ( imuon->isGlobalMuon() ) {
      globalMuon = dynamic_cast<const pat::Muon *>(imuon->masterClonePtr().get());
      break;
    }
  }

  if ( globalMuon == NULL ) {  cout<<"No Global Muon is found"<<endl; return false; }
  double muPt_       = globalMuon->pt();
  double muEta_      = globalMuon->eta();
  double nhits_      = static_cast<int>( globalMuon->numberOfValidHits() );
  double d0_         = globalMuon->dB();
  double norm_chi2_  = globalMuon->normChi2();
  double hCalVeto_   = globalMuon->isolationR03().hadVetoEt;
  double eCalVeto_   = globalMuon->isolationR03().emVetoEt;
  //double trackIso_   = globalMuon->trackIso();
  //double eCalIso_    = globalMuon->ecalIso();
  //double hCalIso_    = globalMuon->hcalIso();
  //double relIso_     = ( trackIso_ + eCalIso_ + hCalIso_ )/muPt_ ;

  histograms["muPt"]->Fill( muPt_      );
  histograms["muEta"]->Fill( muEta_     );
  histograms["nHits"]->Fill( nhits_     );
  histograms["d0"]->Fill( d0_        );
  histograms["Chi2"]->Fill( norm_chi2_ );
  histograms["hCalVeto"]->Fill( hCalVeto_  );
  histograms["eCalVeto"]->Fill( eCalVeto_  );

  return true;
}


// fill the plots for the jets
bool SHyFT::analyze_jets(const std::vector<reco::ShallowClonePtrCandidate>& jets)
{

  //SecVtxMass and b-tagging related quantities
  int numBottom=0,numCharm=0,numLight=0;
  int numTags=0, numJets=0;
  double sumVertexMass=0, vertexMass=0;
  for ( ShallowCloneCollection::const_iterator jetBegin = jets.begin(),
	  jetEnd = jets.end(), jetIter = jetBegin;
	jetIter != jetEnd; ++jetIter)
  {
      const pat::Jet* jet = dynamic_cast<const pat::Jet *>(jetIter->masterClonePtr().get());

      // We first get the flavor of the jet so we can fill look at btag efficiency.
      int jetFlavor = std::abs( jet->partonFlavour() );
      double jetPt  = std::abs( jet->pt() );
     
      histograms["tag_jet_pt"]->Fill( jetPt );
      histograms2d["massVsPt"]->Fill( jetPt, jet->mass() );

      // Is this jet tagged and does it have a good secondary vertex
      if( jet->bDiscriminator("simpleSecondaryVertexBJetTags") < 2.05 ) {
        // This jet is not tagged, so we skip it but first we check the btag efficiency.
        if     ( jetFlavor == 4 ) histograms["tag_eff"]-> Fill( 1 );
        else if( jetFlavor == 5 ) histograms["tag_eff"]-> Fill( 2 );
        else                      histograms["tag_eff"]-> Fill( 0 );
        continue;
      } 
      else {
        if     ( jetFlavor == 4 ) histograms["tag_eff"]-> Fill( 4 );
        else if( jetFlavor == 5 ) histograms["tag_eff"]-> Fill( 5 );
        else                      histograms["tag_eff"]-> Fill( 3 );
      }
      reco::SecondaryVertexTagInfo const * svTagInfos
        = jet->tagInfoSecondaryVertex("secondaryVertex");
      if ( svTagInfos->nVertices() <= 0 )  continue;
      else histograms["nVertices"]-> Fill( svTagInfos->nVertices() );

      // Calculate SecVtx Mass //
      ROOT::Math::LorentzVector< ROOT::Math::PxPyPzM4D<double> > sumVec;
      
      reco::Vertex::trackRef_iterator
        kEndTracks = svTagInfos->secondaryVertex(0).tracks_end();
      for (reco::Vertex::trackRef_iterator trackIter =
             svTagInfos->secondaryVertex(0).tracks_begin();
           trackIter != kEndTracks;
           ++trackIter )
        {
          const double kPionMass = 0.13957018;
	  ROOT::Math::LorentzVector< ROOT::Math::PxPyPzM4D<double> >  p4_1;
          p4_1.SetPx( (*trackIter)->px() );
          p4_1.SetPy( (*trackIter)->py() );
          p4_1.SetPz( (*trackIter)->pz() );
          p4_1.SetM (kPionMass);
          sumVec += p4_1;
          
        }  // for trackIter
      
      vertexMass = sumVec.M();
      sumVertexMass += vertexMass;

      //Here we determine what kind of flavor we have in this jet
      if ( useHFcat_ )
        histograms["flavorhistory"]-> Fill ( HFcat_ );

      switch (jetFlavor)
      {
        case 5:
          // bottom
          histograms["bmass"]->Fill(vertexMass);
          ++numBottom; 
	  break;
        case 4:
          // charm
          histograms["cmass"]->Fill(vertexMass);
          ++numCharm;
	  break;
        default:
          // light flavour
          histograms["lfmass"]->Fill(vertexMass);
          ++numLight;
      }
      ++numTags;
      histograms["discriminator"]-> Fill ( jet->bDiscriminator("simpleSecondaryVertexBJetTags") );
      
      // For now, we only care if we have 2 tags...any more are treated the same - maybe we should look at 3 tags?
      if(numTags==2) break;
  }

   // Calculate average SecVtx mass and //  
   // fill appropriate histograms.      //                                                                                                                                                            
   // TODO !!!
  numJets = std::min( (int) jets.size(), 5 );
  //histograms[secvtxname + "_jettag"]->Fill (numJets, numTags);

  //skip 0 tag events
  if( numTags < 1 )    return  false;
  sumVertexMass /= numTags;

  string whichtag = "";
  if (1 == numTags)
    {
      // single tag                                                                                                                                                                                                
      if      (numBottom)              whichtag = "_b";
      else if (numCharm)               whichtag = "_c";
      else if (numLight)               whichtag = "_q";
      else                             whichtag = "_x";
    }
  else {
    // double tags                                                                                                                                                                                                 
    if      (2 == numBottom)         whichtag = "_bb";
    else if (2 == numCharm)          whichtag = "_cc";
    else if (2 == numLight)          whichtag = "_qq";
    else if (numBottom && numCharm)  whichtag = "_bc";
    else if (numBottom && numLight)  whichtag = "_bq";
    else if (numCharm  && numLight)  whichtag = "_cq";
    else                             whichtag = "_xx";
  } // if two tags                                                                                                                                                                                                  
  string massName = secvtxname
    + Form("_secvtxMass_%dj_%dt", numJets, numTags);

  histograms[massName           ]-> Fill (sumVertexMass);
  histograms[massName + whichtag]-> Fill (sumVertexMass);


  return true;
}

bool SHyFT::analyze_met(const reco::ShallowClonePtrCandidate & met)
{
  histograms["metPt"]->Fill( met.pt() );

  return true;
}



///////////////////
/// The event loop
//////////////////
void SHyFT::analyze(const edm::EventBase& iEvent)
{

  pat::strbitset ret = wPlusJets.getBitTemplate();

  bool passed = wPlusJets(iEvent, ret);
  std::vector<reco::ShallowClonePtrCandidate> const & electrons = wPlusJets.selectedElectrons();
  std::vector<reco::ShallowClonePtrCandidate> const & muons     = wPlusJets.selectedMuons();
  std::vector<reco::ShallowClonePtrCandidate> const & jets      = wPlusJets.cleanedJets();
  //std::vector<reco::ShallowClonePtrCandidate> const & jetsBeforeClean = wPlusJets.selectedJets();
  reco::ShallowClonePtrCandidate const & met = wPlusJets.selectedMET();

  string bit_;

  bit_ = "Trigger" ;
  bool passTrigger = ret[ bit_ ];
  bit_ = "== 1 Lepton";
  bool passOneLepton = ret[ bit_ ];
  bit_ = ">=1 Jets";
  bool jet1 = ret[bit_];
  bit_ = ">=2 Jets";
  bool jet2 = ret[bit_];
  bit_ = ">=3 Jets";
  bool jet3 = ret[bit_];
  bit_ = ">=4 Jets";
  bool jet4 = ret[bit_];
  bit_ = ">=5 Jets";
  bool jet5 = ret[bit_];

  bool anyJets = jet1 || jet2 || jet3 || jet4 || jet5;

  // if not passed trigger, next event                                                                                                                                                                       
  if ( !passTrigger )  return;

  secvtxname = sampleNameInput;
  //find the sample name
  if(!calcSampleName(iEvent, secvtxname) ) return;

  // TODO: check the logic !
  // TODO: integrate the secvtxname initialization 

  if( !passOneLepton ) return;

  if (anyJets) 
  {
    analyze_jets(jets);
    analyze_met( met );
    if ( muPlusJets_ ) analyze_muons(muons);
    if ( ePlusJets_ ) analyze_electrons(electrons);


    histograms["nJets"]->Fill( jets.size() );
    unsigned int maxJets = jets.size();
    if ( (int)maxJets >= nJetsCut_ ) {
      if ( maxJets > 4 ) maxJets = 4;
      for ( unsigned int i=0; i<maxJets; ++i) {
	histograms["jet" + boost::lexical_cast<std::string>(i+1) + "Pt"] ->Fill( jets[i].pt()  );
	histograms["jet" + boost::lexical_cast<std::string>(i+1) + "Eta"]->Fill( jets[i].eta() );
	histograms["jet" + boost::lexical_cast<std::string>(i+1) + "Mass"]->Fill( jets[i].mass() );
	pat::Jet const * patJet = dynamic_cast<pat::Jet const *>( &* jets[i].masterClonePtr()  );
	if ( doMC_ && patJet != 0 && patJet->genJet() != 0 ) {
	  histograms["jet" + boost::lexical_cast<std::string>(i+1) + "PtTrueRes"] ->Fill( jets[i].pt() / patJet->genJet()->pt()  );
	}
      }

      reco::Candidate::LorentzVector nu_p4 = met.p4();
      reco::Candidate::LorentzVector mu_p4 = muons[0].p4();
      double wMT = (mu_p4 + nu_p4).mt();
      histograms["wMT"]->Fill( wMT );
    } 
    if ( maxJets >= 4 ) {
        
      std::cout << iEvent.id().run() << ":" << iEvent.id().event() <<":" << iEvent.id().luminosityBlock() << ":" << std::setprecision(8) << muons[0].pt() << std::endl;

    }
    return;

  }
  
}

bool SHyFT::calcSampleName (const edm::EventBase& iEvent, std::string &sampleName)
{
    // Get the heavy flavor category - we first want to make sure we have flavorHistory
    if(useHFcat_) {
      edm::Handle< unsigned int > heavyFlavorCategory;
      iEvent.getByLabel ( edm::InputTag("flavorHistoryFilter"),heavyFlavorCategory);
      assert ( heavyFlavorCategory.isValid() );
      HFcat_ = (*heavyFlavorCategory);

	// Light Flavor Mode //
	if (kLFMode == mode)
	  {
	    // Wqq
	    if (5 == HFcat_)
	      {
		sampleName += "b3";
	      }
	    else if (6 == HFcat_)
	      {
		sampleName += "c3";
	      }
	    else if (11 != HFcat_)
	      {
		// skip this event
		return false;
	      } // else if ! 11
	    return true;
	  }
    
	// Wc Mode //
	if (kWcMode == mode)
	  {
	    // Wc
	    if (4 != HFcat_)
	      {
		// skip this event
		return false;
	      } // if not Wc
	    return true;
	  } // else if Wc
    
	// Vqq Mode //
    
	// MadGraph (at least as CMS has implemented it) has this _lovely_
	// feature that if the W or Z is far enough off-shell, it erases
	// the W or Z from the event record.  This means that in some
	// number of cases, we won't be able to tell whether this is a W or
	// Z event by looking for a W or Z in the GenParticle collection.
	// (We'll eventually have to be more clever).
	//   sampleName = "X";
	edm::Handle< vector< reco::GenParticle > > genParticleCollection;
	iEvent.getByLabel (edm::InputTag("prunedGenParticles"),genParticleCollection);
	assert ( genParticleCollection.isValid() );
	// We don't know if it is a W, a Z, or neither
	// Iterate over genParticles
	const vector< reco::GenParticle>::const_iterator 
	  kGenPartEnd = genParticleCollection->end();
	for (vector< reco::GenParticle>::const_iterator gpIter =
	       genParticleCollection->begin(); 
	     gpIter != kGenPartEnd; ++gpIter ) 
	  {
	    if (gpIter->status() == 3 && std::abs(gpIter->pdgId()) == 23)
	      {
		sampleName += "Z";
		break;
	      }
	    else if (gpIter->status() == 3 && std::abs(gpIter->pdgId()) == 24)
	      {
		sampleName += "W";
		break;
	      }
	    else if (gpIter==kGenPartEnd-1) 
	      {
		sampleName += "X";
		break;
	      }
	  } // for  gpIter
	switch (HFcat_)
	  {
	    // from:
	    // https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideFlavorHistory
	    //  1. W+bb with >= 2 jets from the ME (dr > 0.5)
	    //  2. W+b or W+bb with 1 jet from the ME
	    //  3. W+cc from the ME (dr > 0.5)
	    //  4. W+c or W+cc with 1 jet from the ME
	    //  5. W+bb with 1 jet from the parton shower (dr == 0.0)
	    //  6. W+cc with 1 jet from the parton shower (dr == 0.0)
	    //  7. W+bb with >= 2 partons but 1 jet from the ME (dr == 0.0)
	    //  8. W+cc with >= 2 partons but 1 jet from the ME (dr == 0.0)
	    //  9. W+bb with >= 2 partons but 2 jets from the PS (dr > 0.5)
	    // 10. W+cc with >= 2 partons but 2 jets from the PS (dr > 0.5)
	    // 11. Veto of all the previous (W+ light jets)
	  case 1:
	    sampleName += "bb";
	    break;
	  case 2:
	    // Sometimes this is referred to as 'b' (e.g., 'Wb'), but I
	    // am using the suffix '2' to keep this case clear for when
	    // we have charm (see below).
	    sampleName += "b2";
	    break; 
	  case 3:
	    sampleName += "cc";
	    break;
	  case 4:
	    // We want to keep this case clear from real W + single charm
	    // produced (as opposed to two charm quarks produced and one
	    // goes down the beampipe), so we use 'c2' instead of 'c'.
	    sampleName += "c2";
	    break;
	  default:
	    // we don't want the rest of the cases.  Return an empty
	    // string so we know.
	    return false;
	  } // switch HFcat_
	return true;
      }
  
      // Normal Mode //
      else if (kNormalMode == mode)
	{
	  // all we want is the sample name, so in this case we're done.
	  return true;
	}
      else
	{
	  std::cout << "Error with naming sample" << std::endl;
	  return false;
	}
}

void SHyFT::endJob()
{
  wPlusJets.print(std::cout);
  wPlusJets.printSelectors(std::cout);
}


