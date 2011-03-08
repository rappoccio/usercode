#include "Analysis/BoostedTopAnalysis/interface/CombinedQCDEstimation.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "AnalysisDataFormats/TopObjects/interface/CATopJetTagInfo.h"

CombinedQCDEstimation::CombinedQCDEstimation( const edm::ParameterSet & iConfig,  TFileDirectory & iDir ) :
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
	caTopJetPtMin_          ( iConfig.getParameter<edm::ParameterSet>("Type11Selection").getParameter<double>("caTopJetPtMin") ),
	caTopJetEtaCut_         ( iConfig.getParameter<edm::ParameterSet>("Type11Selection").getParameter<double>("caTopJetEtaCut") ),
	caTopJetMassMin_        ( iConfig.getParameter<double>("caTopJetMassMin") ),
	caTopJetMassMax_        ( iConfig.getParameter<double>("caTopJetMassMax") ),
	caTopMinMassMin_        ( iConfig.getParameter<double>("caTopMinMassMin") ),
	caTopMistagFileName_    ( iConfig.getParameter<string>("caTopMistagFileName") )
{
	std::cout << "Instantiated CombinedQCDEstimation" << std::endl;
	
	// Type22 histograms
	histograms1d["ttMassType22"]    = theDir.make<TH1F>("ttMassType22",   "t#bar{t} Inv Mass Type22",   200,  0,  2000 );
	histograms1d["topMassPred"]     = theDir.make<TH1F>("topMassPred",    "Top Mass",                   100,  0,  500 );
	histograms1d["ttMassType22Pred"]  = theDir.make<TH1F>("ttMassType22Pred",   "t#bar{t} Inv Mass Type22",   200,  0,  2000 );
	histograms1d["tightloose"]  = theDir.make<TH1F>("tightloose",   "tightloose",   2,  0,  2 );
	histograms1d["tight"]  = theDir.make<TH1F>("tight",   "tight",   1,  0,  1 );
	histograms1d["loose"]  = theDir.make<TH1F>("loose",   "loose",   1,  0,  1 );
	
	// Type12 histograms
	
	histograms1d["ttMassType12_measured"]    = theDir.make<TH1F>("ttMassType12_measured",   "measured t#bar{t} Inv Mass Type12",   200,  0,  2000 );
	histograms1d["ttMassType12Pred_method1"]    = theDir.make<TH1F>("ttMassType12Pred_method1",   "ttMassType12Pred_method1",   200,  0,  2000 );
	histograms1d["ttMassType12Pred_method2"]    = theDir.make<TH1F>("ttMassType12Pred_method2",   "ttMassType12Pred_method2",   200,  0,  2000 );
	
	// Type11 histograms
	histograms1d["ttMassType11_measured"]    = theDir.make<TH1F>("ttMassType11_measured",   "measured t#bar{t} Inv Mass Type11",   200,  0,  2000 );
	
	histograms1d["ttMassType11_predicted_0tagSample"]   = theDir.make<TH1F>("ttMassType11_predicted_0tagSample",   "predictedt#bar{t} Inv Mass Type11",   200,  0,  2000 );
	histograms1d["ttMassType11_predicted_0tagSample_errorSquared"] = theDir.make<TH1F>("ttMassType11_predicted_0tagSample_errorSquared", "sum of squared errors t#bar{t} Inv Mass Type11",   200,  0,  2000 );
	
	histograms1d["ttMassType11_predicted_1tagSample"]   = theDir.make<TH1F>("ttMassType11_predicted_1tagSample",   "predictedt#bar{t} Inv Mass Type11 - single tagged sample",   200,  0,  2000 );
	histograms1d["ttMassType11_predicted_1tagSample_errorSquared"] = theDir.make<TH1F>("ttMassType11_predicted_1tagSample_errorSquared", "sum of squared errors t#bar{t} Inv Mass Type11",   200,  0,  2000 );
    
	histograms1d["ttMassType11_test_predict"]   = theDir.make<TH1F>("ttMassType11_test_predict",   "ttMassType11_test_predict",   200,  0,  2000 );
	
	histograms1d["caTopDijetMass"]  = theDir.make<TH1F>("caTopDijetMass",   "dijet mass",   200,  0,  2000 );
	histograms1d["caTopJetMass"]  = theDir.make<TH1F>("caTopJetMass",   "jet mass",   100,  0,  500 );
	histograms1d["caTopMinMass"]  = theDir.make<TH1F>("caTopMinMass",   "jet minmass",   100,  0,  150 );
	histograms1d["caTopNsubjets"]  = theDir.make<TH1F>("caTopNsubjets",   "jet nsubjets",   6,  0,  6 );
	histograms1d["Nevents"]  = theDir.make<TH1F>("Nevents",   "Nevents",   3,  0,  3 );
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

void CombinedQCDEstimation::analyze( const edm::EventBase & iEvent )
{
	double evtWeight = 1.0;
	
	edm::Handle<GenEventInfoProduct>    genEvt;
	iEvent.getByLabel( edm::InputTag("generator"),  genEvt );
	if( genEvt.isValid() )  {
		//evtWeight = genEvt->weight() ;
	}
	
	
	bool verbose_ = false;
	int run = iEvent.id().run();
	int event = iEvent.id().event();
	int lumi = iEvent.id().luminosityBlock(); 
	if (verbose_)cout<<"\nAnalyze event "<<event<<endl;
	
	pat::strbitset   retType11 = type11Selection_v1_.getBitTemplate();
	bool passType11 = type11Selection_v1_( iEvent, retType11 );
	std::vector<edm::Ptr<pat::Jet> >  const &  caTopJets_ = type11Selection_v1_.caTopJets();
	
	pat::strbitset   retType22 = type22Selection_v1_.getBitTemplate();
	bool passType22 = type22Selection_v1_( iEvent, retType22 );
	std::vector<edm::Ptr<pat::Jet> >  const &  pfJets_ = type22Selection_v1_.pfJets();
	
	wJetSelector_  = &(type22Selection_v1_.wJetSelector() );

	if( passType11 && passType22)  
	{			
		//Put jets in the proper hemisphere
		pat::Jet const & leadJet = *caTopJets_.at(0);			
		std::vector<edm::Ptr<pat::Jet> >  hemisphere0, hemisphere1;
		std::vector<edm::Ptr<pat::Jet> >  hemisphere0_catop, hemisphere1_catop;
		std::vector<edm::Ptr<pat::Jet> >  wTags0,   wTags1;
		std::vector<edm::Ptr<pat::Jet> >  bTags0,   bTags1;
		std::vector<edm::Ptr<pat::Jet> >  noTags0,  noTags1;
		pat::Jet const * aJet0=NULL;
		pat::Jet const * aJet1=NULL;

		if (verbose_) cout<<"caTopJets_.size() = "<<caTopJets_.size()<<"  pfJets_.size() "<<pfJets_.size()<<endl;

		for( vector<edm::Ptr<pat::Jet> >::const_iterator jetBegin=caTopJets_.begin(), jetEnd=caTopJets_.end(), icatop=jetBegin ;
			icatop!=jetEnd; icatop++ ) 
		{
			pat::Jet const & caTopJet = **icatop;

			for( vector<edm::Ptr<pat::Jet> >::const_iterator jetBegin=pfJets_.begin(), jetEnd=pfJets_.end(), ijet=jetBegin ;
			ijet!=jetEnd; ijet++ ) 
			{
				pat::Jet const & jet = **ijet;
				pat::Jet const & cajet = **icatop;
				double deltaR_catop_prune = deltaR( caTopJet.eta(), caTopJet.phi(), jet.eta(), jet.phi() );
				
				bool  wtagged = false;
				bool  btagged = false;
				bool  cajet_btagged = false;
				pat::strbitset iret = wJetSelector_->getBitTemplate();
				wtagged = wJetSelector_->operator()( jet, iret );
				bool passWMass = (jet.mass() > wMassMin_ ) && (jet.mass() < wMassMax_ );
				btagged = (jet.bDiscriminator( bTagAlgo_ ) > bTagOP_ );
				cajet_btagged = (cajet.bDiscriminator( bTagAlgo_ ) > bTagOP_ );
								
				//match pruned jet to catop jet
				if( deltaR_catop_prune < 0.1 ) 
				{	
					//group the jets into hemispheres
					double dPhi_ = fabs( reco::deltaPhi<double>( leadJet.phi(), jet.phi() ) );
					if( dPhi_ < TMath::Pi()/2 ) 
					{
						hemisphere0.push_back( *ijet );
						hemisphere0_catop.push_back( *icatop );
						
						if( wtagged && passWMass ) 
							wTags0.push_back( *ijet );
						else if ( btagged )
							bTags0.push_back( *ijet );
						else
							noTags0.push_back( *ijet );												
					}
					else 
					{
						hemisphere1.push_back( *ijet );
						hemisphere1_catop.push_back( *icatop );
						
						if( wtagged && passWMass )
							wTags1.push_back( *ijet );
						else if ( btagged )
							bTags1.push_back( *ijet );
						else
							noTags1.push_back( *ijet );
					}
				}	
			}
		}	
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
		
		// Setup Type 1
		bool hasTaggedTopJet0=false;
		bool hasTaggedTopJet1=false;
		bool preselected_event=false;
		reco::Candidate::LorentzVector p4_catop_jet0;
		reco::Candidate::LorentzVector p4_catop_jet1;
		double j0_minmass=-99;
		double j1_minmass=-99;
		double j0_nsubjets=-99;
		double j1_nsubjets=-99;
		
		if ( hemisphere0_catop.size()>0 && hemisphere1_catop.size()>0 )
		{			
			pat::Jet const & catop0 = *hemisphere0_catop.at(0);
			pat::Jet const & catop1 = *hemisphere1_catop.at(0);
						
			p4_catop_jet0 = catop0.p4();
			p4_catop_jet1 = catop1.p4();

			double delta_phi_catop = fabs( reco::deltaPhi<double>( catop0.phi(), catop1.phi() ) );
			if (verbose_) cout<<"catop0  pt "<<catop0.pt()<<" eta "<<catop0.eta()<<" phi "<<catop0.phi()<<endl;
			if (verbose_) cout<<"catop1  pt "<<catop1.pt()<<" eta "<<catop1.eta()<<" phi "<<catop1.phi()<<endl;
			if (verbose_) cout<<"delta_phi_catop "<<delta_phi_catop<<endl;

			if (delta_phi_catop >2.1)
			{
				if ( catop0.pt() > caTopJetPtMin_ && catop1.pt() > caTopJetPtMin_ && fabs(catop0.eta()) < caTopJetEtaCut_ && fabs(catop1.eta()) < caTopJetEtaCut_ )
				{
					preselected_event=true;
					std::vector<const reco::Candidate *>  catop0_subjets = catop0.getJetConstituentsQuick();

					if ( catop0_subjets.size() >=3)
					{	
						int subjetLoopCount=0;
						math::XYZTLorentzVector pairwiseMass01;
						math::XYZTLorentzVector pairwiseMass02;
						math::XYZTLorentzVector pairwiseMass12;
						
						for (std::vector<const reco::Candidate *>::iterator subjetIt = catop0_subjets.begin(); subjetIt != catop0_subjets.end(); subjetIt++)
						{					
							reco::Candidate const * subjetCand =  (*subjetIt);
							reco::PFJet const * pfSubjet = dynamic_cast<reco::PFJet const *>(subjetCand);  
														
							if (subjetLoopCount==0 || subjetLoopCount==1) pairwiseMass01 += pfSubjet->p4();
							if (subjetLoopCount==0 || subjetLoopCount==2) pairwiseMass02 += pfSubjet->p4();
							if (subjetLoopCount==1 || subjetLoopCount==2) pairwiseMass12 += pfSubjet->p4();
							subjetLoopCount++;
						}
						
						double min2 = std::min(pairwiseMass01.mass(), pairwiseMass02.mass() );
						j0_minmass = std::min(min2, pairwiseMass12.mass() );
						j0_nsubjets = subjetLoopCount;
					}//end if jet0 nsubjets>=3

					std::vector<const reco::Candidate *>  catop1_subjets = catop1.getJetConstituentsQuick();

					if ( catop1_subjets.size() >=3)
					{	
						int subjetLoopCount=0;
						math::XYZTLorentzVector pairwiseMass01;
						math::XYZTLorentzVector pairwiseMass02;
						math::XYZTLorentzVector pairwiseMass12;
						
						for (std::vector<const reco::Candidate *>::iterator subjetIt = catop1_subjets.begin(); subjetIt != catop1_subjets.end(); subjetIt++)
						{					
							reco::Candidate const * subjetCand =  (*subjetIt);
							reco::PFJet const * pfSubjet = dynamic_cast<reco::PFJet const *>(subjetCand);  
														
							if (subjetLoopCount==0 || subjetLoopCount==1) pairwiseMass01 += pfSubjet->p4();
							if (subjetLoopCount==0 || subjetLoopCount==2) pairwiseMass02 += pfSubjet->p4();
							if (subjetLoopCount==1 || subjetLoopCount==2) pairwiseMass12 += pfSubjet->p4();
							subjetLoopCount++;
						}
						
						double min2 = std::min(pairwiseMass01.mass(), pairwiseMass02.mass() );
						j1_minmass = std::min(min2, pairwiseMass12.mass() );
						j1_nsubjets = subjetLoopCount;

					}//end if jet1 nsubjets>=3
					
					if ( catop0.mass() > caTopJetMassMin_ && catop0.mass() < caTopJetMassMax_ && j0_minmass > caTopMinMassMin_ && j0_nsubjets>2){hasTaggedTopJet0=true;}
					if ( catop1.mass() > caTopJetMassMin_ && catop1.mass() < caTopJetMassMax_ && j1_minmass > caTopMinMassMin_ && j1_nsubjets>2){hasTaggedTopJet1=true;}					
					
				}//end if passes pt and eta cuts
			}//end if passes deltaphi
		}//end if both hemispheres have catop jets
		
		bool hasNonLeadingBjet0 = false;
		bool hasNonLeadingBjet1 = false;
		
		for(size_t i=0; i<hemisphere0_catop.size(); i++ ) {
			pat::Jet const & catop = *hemisphere0_catop.at(i);
			if (verbose_) cout<<" hemi0  jet "<<i<<"  eta "<<catop.eta()<<" phi "<<catop.phi()<<" pt "<<catop.pt()<<" bDiscrim "<<catop.bDiscriminator( bTagAlgo_ )<<" op "<< bTagOP_ <<endl;

			if ( catop.bDiscriminator( bTagAlgo_ ) > bTagOP_ )
			{
				if (i>0) hasNonLeadingBjet0 = true;
			}
		}
		for(size_t i=0; i<hemisphere1_catop.size(); i++ ) {
			pat::Jet const & catop = *hemisphere1_catop.at(i);
			if (verbose_) cout<<" hemi1  jet "<<i<<"  eta "<<catop.eta()<<" phi "<<catop.phi()<<" pt "<<catop.pt()<<" bDiscrim "<<catop.bDiscriminator( bTagAlgo_ )<<" op "<< bTagOP_ <<endl;

			if ( catop.bDiscriminator( bTagAlgo_ ) > bTagOP_ )
			{
				if (i>0) hasNonLeadingBjet1 = true;
			}
		}
		
		// Setup Type 2		
		bool hasLooseTop0 = false, hasTightTop0 = false;
		bool hasLooseTop1 = false, hasTightTop1 = false;
		bool hasTwoWTags = (wTags0.size() >=1 ) && (wTags1.size() >=1 );
		bool hasBTag0 = (bTags0.size() >=1 );
		bool hasBTag1 = (bTags1.size() >= 1 );
		bool hasWTag0 = (wTags0.size() >= 1 );
		bool hasWTag1 = (wTags1.size() >= 1 );
		bool hasOneWTag = (hasWTag0 && !hasWTag1 ) || (hasWTag1 && !hasWTag0) ;
		bool hasWTag = hasWTag0 || hasWTag1;
		bool hasBTag = hasBTag0 || hasBTag1;
		
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
		
		if (verbose_) cout<<"hasTightTop0 "<< hasTightTop0 <<" hasTightTop1 "<<hasTightTop1<<" hasLooseTop0 "<<hasLooseTop0<<" hasLooseTop1 "<<hasLooseTop1<<endl;
		
		
		///////////////////////////////////////////////////////////////////////////////////////////////
		// Measure pass events
		
		bool type11_passevent=false;
		bool type12_passevent=false;
		bool type22_passevent=false;
		
		//Type 11
		if ( hasTaggedTopJet0 && hasTaggedTopJet1)
		{
			cout<<"Yipee!, Type1+Type1, Event id, "<<iEvent.id()<<endl;
			cout<<" summary:"<<endl;
			cout<<"  j0_pt "<<p4_catop_jet0.pt()<<endl;
			cout<<"  j1_pt "<<p4_catop_jet1.pt()<<endl;
			cout<<"  j0_mass "<<p4_catop_jet0.mass()<<endl;
			cout<<"  j1_mass "<<p4_catop_jet1.mass()<<endl;
			cout<<"  j0_nsubjets "<<j0_nsubjets<<endl;
			cout<<"  j1_nsubjets "<<j1_nsubjets<<endl;
			cout<<"  j0_minmass "<<j0_minmass<<endl;
			cout<<"  j1_minmass "<<j1_minmass<<endl;

			
			double ttMass = (p4_catop_jet0+p4_catop_jet0).mass();

			type11_passevent = true;
			histograms1d["ttMassType11_measured"] ->Fill (ttMass, evtWeight);
		}

		//Type 12
		if (!type11_passevent )
		{
			if ( (hasTaggedTopJet0 && ( hasTightTop1 || hasLooseTop1)) || (hasTaggedTopJet1 && ( hasTightTop0 || hasLooseTop0)) )
			{
					cout<<"WoopWoop!, Type1+Type2, Event id, "<<iEvent.id()<<endl;
					cout<<" summary:"<<endl;
					cout<<"  catop j0_mass "<<p4_catop_jet0.mass()<<endl;
					cout<<"  catop j1_mass "<<p4_catop_jet1.mass()<<endl;
					cout<<"  catop j0_nsubjets "<<j0_nsubjets<<endl;
					cout<<"  catop j1_nsubjets "<<j1_nsubjets<<endl;
					cout<<"  catop j0_minmass "<<j0_minmass<<endl;
					cout<<"  catop j1_minmass "<<j1_minmass<<endl;
					
					cout<<"  p4_catop_jet0.mass() "<<p4_catop_jet0.mass()<<endl;
					cout<<"  p4_catop_jet1.mass() "<<p4_catop_jet1.mass()<<endl;
					cout<<"  p4_top0.mass() "<<p4_top0.mass()<<endl;
					cout<<"  p4_top1.mass() "<<p4_top1.mass()<<endl;
					
					double ttMass =0;
					if (hasTaggedTopJet0) {ttMass = (p4_catop_jet0+p4_top1).mass() ; cout<<" catop_jet0 + hemisphere1"<<endl;}
					if (hasTaggedTopJet1) {ttMass = (p4_catop_jet1+p4_top0).mass() ; cout<<" catop_jet1 + hemisphere0"<<endl;}
					cout<<"  ttMass "<<ttMass<<endl;
					
					type12_passevent = true;
					histograms1d["ttMassType12_measured"] ->Fill (ttMass, evtWeight);
			}
		}
		
		if(hasTightTop0) histograms1d["tight"] ->Fill (0.5, 1);
		if(hasTightTop1) histograms1d["tight"] ->Fill (0.5, 1);
		if(hasLooseTop0) histograms1d["loose"] ->Fill (0.5, 1);
		if(hasLooseTop1) histograms1d["loose"] ->Fill (0.5, 1);
		
		
		
		// Type 22	
		if (!type11_passevent && !type12_passevent)
		{
			if(hasTightTop0 && hasTightTop1) histograms1d["tightloose"] ->Fill (0.5, 1);

			if((hasTightTop0 && hasLooseTop1) || (hasLooseTop0 && hasTightTop1))  histograms1d["tightloose"] ->Fill (1.5, 1);
			
			
			if( (hasTightTop0 && hasTightTop1) || (hasTightTop0 && hasLooseTop1) || (hasLooseTop0 && hasTightTop1) )  {
				if(runOnData_)    cout<<"Woohoo, Type2+Type2, Event id, "<<iEvent.id()<<endl;
				double ttMass = (p4_top0+p4_top1).mass() ;
				histograms1d["ttMassType22"]      ->  Fill( ttMass, evtWeight );
				type22_passevent=true;
				//This is our signal, return
				return;
			}
		}
		
		
		///////////////////////////////////////////////////////////////////////////////////////////////
		// Background estimation
		
		bool type11_bkgd_prediction_event=false;
		bool type12_bkgd_prediction_event=false;

		// Type 1+1 Background estimation starts here
		if (preselected_event && !type11_passevent && !type12_passevent && !type22_passevent )
		{
			int bin0 = topMistag_->FindBin( p4_catop_jet0.pt() );
			int bin1 = topMistag_->FindBin( p4_catop_jet1.pt() );
			double mistagProb_jet0 = topMistag_->GetBinContent(bin0);
			double mistagProb_jet1 = topMistag_->GetBinContent(bin1);
			double mistagError_jet0 = topMistag_->GetBinError(bin0);
			double mistagError_jet1 = topMistag_->GetBinError(bin1);
			
			if (hasTaggedTopJet0 && !hasTaggedTopJet1 && !hasNonLeadingBjet1 ) 
			{		
				if (verbose_) cout<<"  Type 11 background estimation event"<<endl;
				if (verbose_) cout<<"   hasTaggedTopJet0 "<<hasTaggedTopJet0<<endl;
				if (verbose_) cout<<"   hasTaggedTopJet1 "<<hasTaggedTopJet1<<endl;
				if (verbose_) cout<<"   hasNonLeadingBjet0 "<<hasNonLeadingBjet0<<endl;
				if (verbose_) cout<<"   hasNonLeadingBjet1 "<<hasNonLeadingBjet1<<endl;
				
				type11_bkgd_prediction_event=true;
				
				double ttMass = (p4_catop_jet0+p4_catop_jet0).mass();
				double weight = mistagProb_jet1;
				double error_squared = mistagError_jet1;
				histograms1d["ttMassType11_predicted_1tagSample"] ->Fill (ttMass, weight);
				histograms1d["ttMassType11_predicted_1tagSample_errorSquared"] ->Fill (ttMass, error_squared);
				histograms1d["ttMassType11_test_predict"] ->Fill (ttMass, weight);
				
			}
			if (hasTaggedTopJet1 && !hasTaggedTopJet0 && !hasNonLeadingBjet0 )
			{
				if (verbose_) cout<<"  Type 11 background estimation event"<<endl;
				if (verbose_) cout<<"   hasTaggedTopJet0 "<<hasTaggedTopJet0<<endl;
				if (verbose_) cout<<"   hasTaggedTopJet1 "<<hasTaggedTopJet1<<endl;
				if (verbose_) cout<<"   hasNonLeadingBjet0 "<<hasNonLeadingBjet0<<endl;
				if (verbose_) cout<<"   hasNonLeadingBjet1 "<<hasNonLeadingBjet1<<endl;
				
				type11_bkgd_prediction_event=true;

				
				double ttMass = (p4_catop_jet0+p4_catop_jet0).mass();
				double weight = mistagProb_jet0;
				double error_squared = mistagError_jet0;
				histograms1d["ttMassType11_predicted_1tagSample"] ->Fill (ttMass, weight);
				histograms1d["ttMassType11_predicted_1tagSample_errorSquared"] ->Fill (ttMass, error_squared);
				histograms1d["ttMassType11_test_predict"] ->Fill (ttMass, weight);
			}
		}
		
		// Type 1+2 Background estimation starts here
		//  Events with 1 top-tagged jet, 0 W-tagged jets, 1 b-tagged jet. 
		//  Jets in the hemisphere opposite the top jet which, when combined with the b-jet, have a pairwise mass in the top mass window, are used as probes to estimate the background
		if( preselected_event && !type11_passevent && !type12_passevent && !type22_passevent && !type11_bkgd_prediction_event )  
		{
			if( hasBTag ) {
				if( hasTaggedTopJet0  && !hasWTag1)  { 
					if (verbose_) cout<<"  Type 12 background estimation event"<<endl;
					if (verbose_) cout<<"   hasTaggedTopJet0 "<<hasTaggedTopJet0<<endl;
					if (verbose_) cout<<"   hasTaggedTopJet1 "<<hasTaggedTopJet1<<endl;
					if (verbose_) cout<<"   hasWTag0 "<<hasWTag0<<endl;
					if (verbose_) cout<<"   hasWTag1 "<<hasWTag1<<endl;
					if (verbose_) cout<<"   hasBTag0 "<<hasBTag0<<endl;
					if (verbose_) cout<<"   hasBTag1 "<<hasBTag1<<endl;
					type12_bkgd_prediction_event=true;
					
					bool passTopMass1 = false;
					p4_top1.SetPxPyPzE(0,0,0,0);
					
					for( size_t i=0; i<noTags1.size(); i++ )  {
						
						double pt = noTags1.at(i)->pt();
						int bin = wMistag_       ->  FindBin( pt );
						double weight = wMistag_ ->  GetBinContent( bin );  //dummy value, depend on pt
						if( hasBTag1 )  {
							p4_top1 = noTags1.at(i)->p4() + bTags1.at(0)->p4();
							if( p4_top1.mass() > topMassMin_ && p4_top1.mass() < topMassMax_ )  {
								passTopMass1 = true;
								double ttMass = (p4_catop_jet0+p4_top1).mass() ;
								histograms1d["ttMassType12Pred_method2"]      ->  Fill( ttMass, weight*evtWeight );
								//ttMassPred      ->    Accumulate( ttMass, pt, 1,  evtWeight );
							}
						}
					}  // end i  
				} // jet0_toptagged 
				else if ( hasTaggedTopJet1 && !hasWTag0) {
					if (verbose_) cout<<"  Type 12 background estimation event"<<endl;
					if (verbose_) cout<<"   hasTaggedTopJet0 "<<hasTaggedTopJet0<<endl;
					if (verbose_) cout<<"   hasTaggedTopJet1 "<<hasTaggedTopJet1<<endl;
					if (verbose_) cout<<"   hasWTag0 "<<hasWTag0<<endl;
					if (verbose_) cout<<"   hasWTag1 "<<hasWTag1<<endl;
					if (verbose_) cout<<"   hasBTag0 "<<hasBTag0<<endl;
					if (verbose_) cout<<"   hasBTag1 "<<hasBTag1<<endl;
					type12_bkgd_prediction_event=true;
					
					bool passTopMass0 = false;
					p4_top0.SetPxPyPzE(0,0,0,0);
					
					for( size_t i=0; i<noTags0.size(); i++ )  {
						double pt = noTags0.at(i)->pt();
						int   bin   =   wMistag_      ->  FindBin( pt );
						double weight = wMistag_      ->  GetBinContent( bin );  //dummy value, depend on pt
						if( hasBTag0 )  {
							p4_top0 = noTags0.at(i)->p4() + bTags0.at(0)->p4();
							if( p4_top0.mass() > topMassMin_ && p4_top0.mass() < topMassMax_ )  {
								passTopMass0 = true;
								double ttMass = (p4_top0+p4_catop_jet1).mass() ;
								histograms1d["ttMassType12Pred_method2"]      ->  Fill( ttMass, weight*evtWeight );
								//ttMassPred       ->      Accumulate( ttMass, pt, 1,  evtWeight );
							}
						}
					}  // end i
				} //has top jet
			} // end if has btag
		}//end if preselected
		
		
		// Type 2+2 Background estimation starts here
		if( preselected_event && !type11_passevent && !type12_passevent && !type22_passevent && !type11_bkgd_prediction_event && !type12_bkgd_prediction_event )  
		{
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
		}	
	}//end if passType11 && passType22
}//end analyze



