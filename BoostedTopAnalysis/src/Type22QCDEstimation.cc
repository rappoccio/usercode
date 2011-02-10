#include "Analysis/BoostedTopAnalysis/interface/Type22QCDEstimation.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "AnalysisDataFormats/TopObjects/interface/CATopJetTagInfo.h"

Type22QCDEstimation::Type22QCDEstimation( const edm::ParameterSet & iConfig,  TFileDirectory & iDir ) :
  theDir( iDir ),
  type22Selection_v1_     ( iConfig.getParameter<edm::ParameterSet>("Type22Selection") ),
  bTagOP_                 ( iConfig.getParameter<edm::ParameterSet>("Type22Selection").getParameter<double>("bTagOP") ),
  bTagAlgo_               ( iConfig.getParameter<edm::ParameterSet>("Type22Selection").getParameter<string>("bTagAlgo") ),
  wMassMin_               ( iConfig.getParameter<double>("wMassMin") ),
  wMassMax_               ( iConfig.getParameter<double>("wMassMax") ),
  topMassMin_             ( iConfig.getParameter<double>("topMassMin") ),
  topMassMax_             ( iConfig.getParameter<double>("topMassMax") ),
  mistagFileName_         ( iConfig.getParameter<string>("mistagFile") ),
  prob                    ( iConfig.getParameter<double>("Probability") ),
  runOnData_              ( iConfig.getParameter<bool>("runOnData") ),
  type11Selection_v1_     ( iConfig.getParameter<edm::ParameterSet>("Type11Selection") ),
  caTopJetMassMin_        ( iConfig.getParameter<double>("caTopJetMassMin") ),
  caTopJetMassMax_        ( iConfig.getParameter<double>("caTopJetMassMax") ),
  caTopMinMassMin_        ( iConfig.getParameter<double>("caTopMinMassMin") ),
  caTopMistagFileName_    ( iConfig.getParameter<string>("caTopMistagFileName") )
{
  std::cout << "Instantiated Type22QCDEstimation" << std::endl;
 
  // Type22 histograms
  histograms1d["ttMassType22"]    = theDir.make<TH1F>("ttMassType22",   "t#bar{t} Inv Mass Type22",   200,  0,  2000 );
  histograms1d["topMassPred"]     = theDir.make<TH1F>("topMassPred",    "Top Mass",                   100,  0,  500 );
  histograms1d["ttMassType22Pred"]  = theDir.make<TH1F>("ttMassType22Pred",   "t#bar{t} Inv Mass Type22",   200,  0,  2000 );
  // Type11 histograms
  histograms1d["ttMassType11_measured"]    = theDir.make<TH1F>("ttMassType11_measured",   "measured t#bar{t} Inv Mass Type11",   200,  0,  2000 );
  histograms1d["ttMassType11_predicted"]   = theDir.make<TH1F>("ttMassType11_predicted",   "predictedt#bar{t} Inv Mass Type11",   200,  0,  2000 );
  histograms1d["ttMassType11_error_squared"] = theDir.make<TH1F>("ttMassType11_error_squared", "sum of squared errors t#bar{t} Inv Mass Type11",   200,  0,  2000 );
  histograms1d["caTopDijetMass"]  = theDir.make<TH1F>("caTopDijetMass",   "dijet mass",   200,  0,  2000 );
  histograms1d["caTopJetMass"]  = theDir.make<TH1F>("caTopJetMass",   "jet mass",   100,  0,  500 );
  histograms1d["caTopMinMass"]  = theDir.make<TH1F>("caTopMinMass",   "jet minmass",   100,  0,  150 );
  histograms1d["caTopNsubjets"]  = theDir.make<TH1F>("caTopNsubjets",   "jet nsubjets",   6,  0,  6 );
  // Input histograms
  mistagFile_   =  TFile::Open( mistagFileName_.c_str() );
  wMistag_      =  (TH1F*)mistagFile_       ->  Get("wMistag");
  caTopMistagFile_   =  TFile::Open( caTopMistagFileName_.c_str() );
  topMistag_      =  (TH1F*)caTopMistagFile_       ->  Get("MISTAG_RATE");
  
  //use the PredictedDistrubution class to get correct error
  ttMassPred  =  new PredictedDistribution( (TH1D*)wMistag_ , "ttMassPred", "t#bar{t} Inv Mass",  200,  0,  2000 );

  edm::Service<edm::RandomNumberGenerator> rng;
  if ( ! rng.isAvailable()) {
    throw cms::Exception("Configuration")
      << "Module requires the RandomNumberGeneratorService\n";
  }

  CLHEP::HepRandomEngine& engine = rng->getEngine();
  flatDistribution_ = new CLHEP::RandFlat(engine, 0., 1.);

}

void Type22QCDEstimation::analyze( const edm::EventBase & iEvent )
{
  double evtWeight = 1.0;

  edm::Handle<GenEventInfoProduct>    genEvt;
  iEvent.getByLabel( edm::InputTag("generator"),  genEvt );
  if( genEvt.isValid() )  {
    //evtWeight = genEvt->weight() ;
  }

  ///////////////////////////////////////////////////////////////////////////////////////////////
  // Type 1+1
  bool type11doubleTagged = false;
  
  pat::strbitset   retType11 = type11Selection_v1_.getBitTemplate();
  bool passType11 = type11Selection_v1_( iEvent, retType11 );
  std::vector<edm::Ptr<pat::Jet> >  const &  caTopJets_ = type11Selection_v1_.caTopJets();

  if( passType11 && caTopJets_.size()>=2)  {
    //cout<<"\n\nAnalyze event "<<iEvent.id().event()<<endl;
    //cout<<" caTopJets_.size() = "<<caTopJets_.size()<<endl;
	  
	double j0_pt=-99;
	double j1_pt=-99;
	double j0_mass=-99;
	double j1_mass=-99;
	double j0_minmass=-99;
	double j1_minmass=-99;
	double j0_nsubjets=-99;
	double j1_nsubjets=-99;		
	double j0_topmass=-99;
	double j1_topmass=-99;
	double j0_phi=-99;
	double j1_phi=-99;
    int jetCount =0;
    math::XYZTLorentzVector j0,j1;
	
	for( vector<edm::Ptr<pat::Jet> >::const_iterator jetBegin=caTopJets_.begin(), jetEnd=caTopJets_.end(), ijet=jetBegin ;
      ijet!=jetEnd; ijet++ ) 
    {
      pat::Jet const & jet = **ijet;
  	  //cout<<"  jet "<< jetCount <<" pt "<<jet.pt()<<" mass "<<jet.mass()<<endl;
	  if (jetCount==0) j0 = jet.p4();
	  if (jetCount==1) j1 = jet.p4();
	  if (jetCount==0) j0_pt = jet.pt();
	  if (jetCount==1) j1_pt = jet.pt();
	  if (jetCount==0) j0_mass = jet.mass();
	  if (jetCount==1) j1_mass = jet.mass();
	  if (jetCount==0) j0_phi = jet.phi();
	  if (jetCount==1) j1_phi = jet.phi();
	  //cout<<" CATop  jet 0 corr/uncorr pt = "<<jet.pt()<<" / "<<jet.correctedJet("Uncorrected").pt()<<endl;
	  //const reco::CATopJetTagInfo * catopTag = dynamic_cast<reco::CATopJetTagInfo const *>(jet.tagInfo("CATopPFJet"));
      //if ( catopTag != 0 )
	  //{
	  //  cout<<"catopTag->properties().minMass  "<<catopTag->properties().minMass  <<endl;
	  //  cout<<"catopTag->properties().nSubJets "<<catopTag->properties().nSubJets <<endl;
	  //}
	  int subjetLoopCount=0;
	  math::XYZTLorentzVector Subjet0, Subjet1, Subjet2;
	  math::XYZTLorentzVector SumSubjetVector;
	  std::vector<const reco::Candidate *>  subjets = jet.getJetConstituentsQuick();
	  for (std::vector<const reco::Candidate *>::iterator subjetIt = subjets.begin(); subjetIt != subjets.end(); subjetIt++)
	  {					
	 	reco::Candidate const * subjetCand =  (*subjetIt);
		reco::PFJet const * pfSubjet = dynamic_cast<reco::PFJet const *>(subjetCand);  
		//cout<<"    subjet pt "<<pfSubjet->pt()<<endl;					
		//cout<<"    subjet mass "<<pfSubjet->mass()<<endl;					
		
		SumSubjetVector += pfSubjet->p4();
					
		if (subjetLoopCount==0) Subjet0 = pfSubjet->p4();
		if (subjetLoopCount==1) Subjet1 = pfSubjet->p4();
		if (subjetLoopCount==2) Subjet2 = pfSubjet->p4();
	 	subjetLoopCount++;
	  }
	  
	  histograms1d["caTopJetMass"] ->Fill( jet.mass(),evtWeight );
	  histograms1d["caTopNsubjets"] ->Fill (subjetLoopCount,evtWeight );


	  if (jetCount==0) j0_nsubjets = subjetLoopCount;
	  if (jetCount==1) j1_nsubjets = subjetLoopCount;
				
	  if (jetCount==0) j0_topmass = SumSubjetVector.mass();
	  if (jetCount==1) j1_topmass = SumSubjetVector.mass();
		
	  if (subjetLoopCount>=3)
	  {
		math::XYZTLorentzVector firstCombination	= Subjet0 + Subjet1;
		math::XYZTLorentzVector secondCombination	= Subjet0 + Subjet2;
		math::XYZTLorentzVector thirdCombination	= Subjet1 + Subjet2;

		//cout<<"      Subjet0.mass() "<<Subjet0.mass()<<endl;
		//cout<<"      Subjet1.mass() "<<Subjet1.mass()<<endl;
		//cout<<"      Subjet2.mass() "<<Subjet2.mass()<<endl;

		double min2 = std::min(firstCombination.mass(), secondCombination.mass() );
		double minMassPairing = std::min(min2, thirdCombination.mass() );
		//cout<<"      firstCombination.mass() "<<firstCombination.mass()<<endl;
		//cout<<"      secondCombination.mass() "<<secondCombination.mass()<<endl;
		//cout<<"      thirdCombination.mass() "<<thirdCombination.mass()<<endl;
		//cout<<"      minMassPairing "<<minMassPairing<<endl;
	    if (jetCount==0) j0_minmass = minMassPairing;
		if (jetCount==1) j1_minmass = minMassPairing;
	  	histograms1d["caTopMinMass"] ->Fill (minMassPairing,evtWeight);
	  }	
      jetCount++;
	}
	double deltaphi = fabs(deltaPhi( j0_phi, j1_phi )) ;
	//cout<<"deltaphi "<<deltaphi<<endl;
	math::XYZTLorentzVector dijet	= j0 + j1;
	double dijet_mass = dijet.mass();
	histograms1d["caTopDijetMass"] ->Fill (dijet_mass );
	/*
	cout<<" summary:"<<endl;
    cout<<"  dijet_mass "<<dijet_mass<<endl;
    cout<<"  j0_mass "<<j0_mass<<endl;
    cout<<"  j1_mass "<<j1_mass<<endl;
    cout<<"  j0_nsubjets "<<j0_nsubjets<<endl;
    cout<<"  j1_nsubjets "<<j1_nsubjets<<endl;
    cout<<"  j0_minmass "<<j0_minmass<<endl;
    cout<<"  j1_minmass "<<j1_minmass<<endl;
    cout<<"  j0_topmass "<<j0_topmass<<endl;
    cout<<"  j1_topmass "<<j1_topmass<<endl;
	*/
	if (deltaphi>2.1)
	{
		if ( j0_mass > caTopJetMassMin_ && j0_mass < caTopJetMassMax_ && j0_minmass > caTopMinMassMin_ && j0_nsubjets>2)
		{
			if ( j1_mass > caTopJetMassMin_ && j1_mass < caTopJetMassMax_ && j1_minmass > caTopMinMassMin_ && j1_nsubjets>2)
			{
				cout<<"Yipee!, Type1+Type1, Event id, "<<iEvent.id()<<endl;
				cout<<" summary:"<<endl;
				cout<<"  dijet_mass "<<dijet_mass<<endl;
				cout<<"  j0_mass "<<j0_mass<<endl;
				cout<<"  j1_mass "<<j1_mass<<endl;
				cout<<"  j0_nsubjets "<<j0_nsubjets<<endl;
				cout<<"  j1_nsubjets "<<j1_nsubjets<<endl;
				cout<<"  j0_minmass "<<j0_minmass<<endl;
				cout<<"  j1_minmass "<<j1_minmass<<endl;
				cout<<"  j0_topmass "<<j0_topmass<<endl;
				cout<<"  j1_topmass "<<j1_topmass<<endl;

				type11doubleTagged = true;
				histograms1d["ttMassType11_measured"] ->Fill (dijet_mass, evtWeight);
			}
		}

	  
		//Data driven background estimation
		int bin0 = topMistag_->FindBin( j0_pt );
		int bin1 = topMistag_->FindBin( j1_pt );

		double mistagProb_jet0 = topMistag_->GetBinContent(bin0);
		double mistagProb_jet1 = topMistag_->GetBinContent(bin1);
			
		double mistagError_jet0 = topMistag_->GetBinError(bin0);
		double mistagError_jet1 = topMistag_->GetBinError(bin1);
			
		//cout<<"j0pt "<<j0_pt<<"  bin0 "<<bin0<<"  mistagrate0 "<< mistagProb_jet0<<"  j1pt "<<j1_pt<<"  bin1 "<<bin1<<"  mistagrate1 "<< mistagProb_jet1<<endl;	
		double weight = mistagProb_jet0 * mistagProb_jet1;
		double error_squared =  
		( mistagProb_jet1*mistagError_jet0 ) * ( mistagProb_jet1*mistagError_jet0 ) + ( mistagProb_jet0*mistagError_jet1 )  *( mistagProb_jet0*mistagError_jet1 ) ;

		histograms1d["ttMassType11_predicted"] ->Fill (dijet_mass, weight);
		histograms1d["ttMassType11_error_squared"] ->Fill (dijet_mass, error_squared);
	}	

  }

  ///////////////////////////////////////////////////////////////////////////////////////////////
  // Type 2+2

  pat::strbitset   retType22 = type22Selection_v1_.getBitTemplate();
  bool passType22 = type22Selection_v1_( iEvent, retType22 );

  std::vector<edm::Ptr<pat::Jet> >  const &  pfJets_ = type22Selection_v1_.pfJets();
  wJetSelector_  = &(type22Selection_v1_.wJetSelector() );
  if( passType22 && !type11doubleTagged)  {
  //if( retType22[string("nJets >= 4")] )  {
    pat::Jet const & leadJet = *pfJets_.at(0);
    std::vector<edm::Ptr<pat::Jet> >  hemisphere0, hemisphere1;
    std::vector<edm::Ptr<pat::Jet> >  wTags0,   wTags1;
    std::vector<edm::Ptr<pat::Jet> >  bTags0,   bTags1;
    std::vector<edm::Ptr<pat::Jet> >  noTags0,  noTags1;
    pat::Jet const * aJet0=NULL;
    pat::Jet const * aJet1=NULL;
    for( vector<edm::Ptr<pat::Jet> >::const_iterator jetBegin=pfJets_.begin(), jetEnd=pfJets_.end(), ijet=jetBegin ;
      ijet!=jetEnd; ijet++ ) 
    {
      pat::Jet const & jet = **ijet;
      bool  wtagged = false;
      bool  btagged = false;
      pat::strbitset iret = wJetSelector_->getBitTemplate();
      wtagged = wJetSelector_->operator()( jet, iret );
      bool passWMass = (jet.mass() > wMassMin_ ) && (jet.mass() < wMassMax_ );
      btagged = (jet.bDiscriminator( bTagAlgo_ ) > bTagOP_ );

      double dPhi_ = fabs( reco::deltaPhi<double>( leadJet.phi(), jet.phi() ) );
      if( dPhi_ < TMath::Pi()/2 ) {
        hemisphere0.push_back( *ijet );
        if( wtagged && passWMass ) 
        //double x = flatDistribution_->fire();
        //if( x < prob )
          wTags0.push_back( *ijet );
        else if ( btagged )
          bTags0.push_back( *ijet );
        else
          noTags0.push_back( *ijet );
      }  else {
        hemisphere1.push_back( *ijet );
        if( wtagged && passWMass )
        //double x = flatDistribution_->fire();
        //if( x < prob )
          wTags1.push_back( *ijet );
        else if ( btagged )
          bTags1.push_back( *ijet );
        else
          noTags1.push_back( *ijet );
      }
    } // end ijet

    if( wTags0.size() >= 1 )  {
      double minDr = 999999. ;
      for(size_t i=0; i<noTags0.size(); i++ ) {
        double dR = reco::deltaR<double>( wTags0.at(0)->eta(), wTags0.at(0)->phi(),
                                          noTags0.at(i)->eta(), noTags0.at(i)->phi() );
        if( dR < minDr )  {
          aJet0 = &(*noTags0.at(i));
          minDr = dR;
        }
      }
    }

    if( wTags1.size() >= 1 )  {
      double minDr = 999999. ;
      for( size_t i=0; i<noTags1.size(); i++ )  {
        double dR = reco::deltaR<double>( wTags1.at(0)->eta(), wTags1.at(0)->phi(),
                                          noTags1.at(i)->eta(), noTags1.at(i)->phi() );
        if( dR < minDr )  {
          aJet1 = &(*noTags1.at(i));
          minDr = dR;
        }
      }
    }

    bool hasTwoWTags = (wTags0.size() >=1 ) && (wTags1.size() >=1 );
    bool hasBTag0 = (bTags0.size() >=1 );
    bool hasBTag1 = (bTags1.size() >= 1 );
    bool hasWTag0 = (wTags0.size() >= 1 );
    bool hasWTag1 = (wTags1.size() >= 1 );
    bool hasOneWTag = (hasWTag0 && !hasWTag1 ) || (hasWTag1 && !hasWTag0) ;
    bool hasWTag = hasWTag0 || hasWTag1;
    //if( hasOneWTag )  
    //  cout<<"wTags0.size() "<<wTags0.size()<<", wTags1.size() "<<wTags1.size() <<endl;
    bool hasBTag = hasBTag0 || hasBTag1;
    bool hasLooseTop0 = false, hasTightTop0 = false;
    bool hasLooseTop1 = false, hasTightTop1 = false;

    reco::Candidate::LorentzVector p4_top0;
    reco::Candidate::LorentzVector p4_top1;
    if( hasBTag0 && hasWTag0 )  {
      p4_top0 = wTags0.at(0)->p4() + bTags0.at(0)->p4() ;
      if( p4_top0.mass() > topMassMin_ && p4_top0.mass() < topMassMax_ )
        hasTightTop0 = true;
    } else if( aJet0 && hasWTag0 ) {
      p4_top0 = wTags0.at(0)->p4() + aJet0->p4() ;
      if( p4_top0.mass() > topMassMin_ && p4_top0.mass() < topMassMax_ )
        hasLooseTop0 = true;
    }
    if( hasBTag1 && hasWTag1 )  {
      p4_top1 = wTags1.at(0)->p4() + bTags1.at(0)->p4();
      if( p4_top1.mass() > topMassMin_ && p4_top1.mass() < topMassMax_ )
        hasTightTop1 = true;
    } else if ( aJet1 && hasWTag1 ) {
      p4_top1 = wTags1.at(0)->p4() + aJet1->p4();
      if( p4_top1.mass() > topMassMin_ && p4_top1.mass() < topMassMax_ )
        hasLooseTop1 = true;
    }

    if( (hasTightTop0 && hasTightTop1) || (hasTightTop0 && hasLooseTop1) || (hasLooseTop0 && hasTightTop1) )  {
      if(runOnData_)    cout<<"Woohoo, Type2+Type2, Event id, "<<iEvent.id()<<endl;
      double ttMass = (p4_top0+p4_top1).mass() ;
      histograms1d["ttMassType22"]      ->  Fill( ttMass, evtWeight );
      //This is our signal, return
      return;
    }

    //Background estimation starts here
    if( hasOneWTag && hasBTag ) {
      if( hasWTag0 )  { 
        //cout<<"case 1"<<endl;
        bool passTopMass1 = false;
        p4_top1.SetPxPyPzE(0,0,0,0);
        if( hasTightTop0 )  { 
          //cout<<"case 10"<<endl;
          for( size_t i=0; i<noTags1.size(); i++ )  {

            double pt = noTags1.at(i)->pt();
            int bin = wMistag_       ->  FindBin( pt );
            double weight = wMistag_ ->  GetBinContent( bin );  //dummy value, depend on pt
            if( hasBTag1 )  {
              p4_top1 = noTags1.at(i)->p4() + bTags1.at(0)->p4();
              histograms1d["topMassPred"]     ->  Fill( p4_top1.mass(), weight*evtWeight );
              if( p4_top1.mass() > topMassMin_ && p4_top1.mass() < topMassMax_ )  {
                passTopMass1 = true;
                double ttMass = (p4_top0+p4_top1).mass() ;
                histograms1d["ttMassType22Pred"]      ->  Fill( ttMass, weight*evtWeight );
                ttMassPred      ->    Accumulate( ttMass, pt, 1,  evtWeight );
              }
            }
            else {  
              double minDr = 9999.0;
              pat::Jet const * nearestJet=NULL;
              for( size_t j=0; j<noTags1.size(); j++ )  {
                if( i==j )   continue;
                double dR = reco::deltaR<double>( noTags1.at(i)->eta(), noTags1.at(i)->phi(),
                                                  noTags1.at(j)->eta(), noTags1.at(j)->phi() );
                if( dR < minDr )  {
                  minDr = dR ;
                  nearestJet = &(*noTags1.at(j));
                }                
              } //end j
              if( nearestJet )  {
                //cout<<"case 11"<<endl;
                p4_top1 = noTags1.at(i)->p4() + nearestJet->p4();
                int  bin1  = wMistag_      ->  FindBin( nearestJet->pt() );
                double weight1 =  wMistag_ -> GetBinContent( bin1 );

                weight *= (1-weight1);
                histograms1d["topMassPred"]   ->  Fill( p4_top1.mass(), weight*evtWeight );
                if( p4_top1.mass() > topMassMin_ && p4_top1.mass() < topMassMax_ )  {
                  passTopMass1 = true;
                  double ttMass = (p4_top0+p4_top1).mass() ;
                  histograms1d["ttMassType22Pred"]    ->  Fill( ttMass, weight*evtWeight );
                  ttMassPred          ->      Accumulate( ttMass, pt, 1,  (1-weight1)*evtWeight );
                }
              }
            }  // end else
          }  // end i
        } //hasTightTop
        else if( hasLooseTop0 )  {
          //cout<<"case 12"<<endl;
          //cout<<bTags1.size()<<endl;
          for( size_t i=0; i<noTags1.size(); i++ )  {
            double pt = noTags1.at(i)->pt();
            int bin     = wMistag_      ->  FindBin( pt );
            double weight = wMistag_    ->  GetBinContent( bin ) ; //dummy value
            p4_top1 = noTags1.at(i)->p4() + bTags1.at(0)->p4();
            histograms1d["topMassPred"]     ->   Fill( p4_top1.mass(), weight*evtWeight );
            if( p4_top1.mass() > topMassMin_ && p4_top1.mass() < topMassMax_ )  {
              passTopMass1 = true;
              double ttMass = (p4_top0+p4_top1).mass() ;
              histograms1d["ttMassType22Pred"]      ->  Fill( ttMass, weight*evtWeight );
              ttMassPred          ->      Accumulate( ttMass, pt, 1,  evtWeight );
            }
          }
        }        
      } // hasWTag0 
      else  {
        //cout<<"case 2"<<endl;
        bool passTopMass0 = false;
        p4_top0.SetPxPyPzE(0,0,0,0);
        if( hasTightTop1 )  {
          //cout<<"case 20"<<endl;
          for( size_t i=0; i<noTags0.size(); i++ )  {
            double pt = noTags0.at(i)->pt();
            int   bin   =   wMistag_      ->  FindBin( pt );
            double weight = wMistag_      ->  GetBinContent( bin );  //dummy value, depend on pt
            if( hasBTag0 )  {
              p4_top0 = noTags0.at(i)->p4() + bTags0.at(0)->p4();
              histograms1d["topMassPred"]     ->  Fill( p4_top0.mass(), weight*evtWeight );
              if( p4_top0.mass() > topMassMin_ && p4_top0.mass() < topMassMax_ )  {
                passTopMass0 = true;
                double ttMass = (p4_top0+p4_top1).mass() ;
                histograms1d["ttMassType22Pred"]      ->  Fill( ttMass, weight*evtWeight );
                ttMassPred       ->      Accumulate( ttMass, pt, 1,  evtWeight );
              }
            }
            else {
              double minDr = 9999.0;
              pat::Jet const * nearestJet=NULL;
              for( size_t j=0; j<noTags0.size(); j++ )  {
                if( i==j )   continue;
                double dR = reco::deltaR<double>( noTags0.at(i)->eta(), noTags0.at(i)->phi(),
                                                  noTags0.at(j)->eta(), noTags0.at(j)->phi() );
                if( dR < minDr )  {
                  minDr = dR ;
                  nearestJet = &(*noTags0.at(j));
                }
              } //end j
              if( nearestJet )  {
                //cout<<"case 22"<<endl;
                p4_top0 = noTags0.at(i)->p4() + nearestJet->p4();
                int   bin1  =  wMistag_       ->  FindBin( nearestJet->pt() );
                double weight1  = wMistag_    ->  GetBinContent( bin1 );
                weight *= (1-weight1);
                histograms1d["topMassPred"]   ->  Fill( p4_top0.mass(), weight*evtWeight );
                if( p4_top0.mass() > topMassMin_ && p4_top0.mass() < topMassMax_ )  {
                  passTopMass0 = true;
                  double ttMass = (p4_top0+p4_top1).mass() ;
                  histograms1d["ttMassType22Pred"]    ->  Fill( ttMass, weight*evtWeight );
                  ttMassPred      ->      Accumulate( ttMass, pt, 1,  (1-weight1)*evtWeight );
                }
              }
            }  // end else
          }  // end i
        } //hasTightTop
        else if( hasLooseTop1 )  {
          //cout<<"case 23"<<endl;
          for( size_t i=0; i<noTags0.size(); i++ )  {
            double pt = noTags0.at(i)->pt();
            int   bin =   wMistag_    ->  FindBin( pt );
            double weight = wMistag_  ->  GetBinContent( bin ); ; //dummy value
            p4_top0 = noTags0.at(i)->p4() + bTags0.at(0)->p4();
            histograms1d["topMassPred"]     ->   Fill( p4_top0.mass(), weight*evtWeight );
            if( p4_top0.mass() > topMassMin_ && p4_top0.mass() < topMassMax_ )  {
              passTopMass0 = true;
              double ttMass = (p4_top0+p4_top1).mass() ;
              histograms1d["ttMassType22Pred"]      ->  Fill( ttMass, weight*evtWeight );
              ttMassPred      ->      Accumulate( ttMass, pt, 1, evtWeight );
            }
          }
        }
      } // else 
    } // end Background estimation

  } // passType22

}



