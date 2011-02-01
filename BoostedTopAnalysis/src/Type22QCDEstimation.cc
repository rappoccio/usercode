#include "Analysis/BoostedTopAnalysis/interface/Type22QCDEstimation.h"

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
  prob                    ( iConfig.getParameter<double>("Probability") )
{
  histograms1d["ttMassType22"]    = theDir.make<TH1F>("ttMassType22",   "t#bar{t} Inv Mass Type22",   200,  0,  2000 );
  histograms1d["topMassPred"]     = theDir.make<TH1F>("topMassPred",    "Top Mass",                   100,  0,  500 );
  histograms1d["ttMassType22Pred"]  = theDir.make<TH1F>("ttMassType22Pred",   "t#bar{t} Inv Mass Type22",   200,  0,  2000 );

  mistagFile_   =  TFile::Open( mistagFileName_.c_str() );
  wMistag_      =  (TH1F*)mistagFile_       ->  Get("wMistag");

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
  pat::strbitset   retType22 = type22Selection_v1_.getBitTemplate();
  bool passType22 = type22Selection_v1_( iEvent, retType22 );

  std::vector<edm::Ptr<pat::Jet> >  const &  pfJets_ = type22Selection_v1_.pfJets();
  wJetSelector_  = &(type22Selection_v1_.wJetSelector() );
  if( passType22 )  {
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
      cout<<"Woohoo, Type2+Type2, Event id, "<<iEvent.id()<<endl;
      double ttMass = (p4_top0+p4_top1).mass() ;
      histograms1d["ttMassType22"]      ->  Fill( ttMass );
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
              histograms1d["topMassPred"]     ->  Fill( p4_top1.mass(), weight );
              if( p4_top1.mass() > topMassMin_ && p4_top1.mass() < topMassMax_ )  {
                passTopMass1 = true;
                double ttMass = (p4_top0+p4_top1).mass() ;
                histograms1d["ttMassType22Pred"]      ->  Fill( ttMass, weight );
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
                histograms1d["topMassPred"]   ->  Fill( p4_top1.mass(), weight );
                if( p4_top1.mass() > topMassMin_ && p4_top1.mass() < topMassMax_ )  {
                  passTopMass1 = true;
                  double ttMass = (p4_top0+p4_top1).mass() ;
                  histograms1d["ttMassType22Pred"]    ->  Fill( ttMass, weight );
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
            histograms1d["topMassPred"]     ->   Fill( p4_top1.mass(), weight );
            if( p4_top1.mass() > topMassMin_ && p4_top1.mass() < topMassMax_ )  {
              passTopMass1 = true;
              double ttMass = (p4_top0+p4_top1).mass() ;
              histograms1d["ttMassType22Pred"]      ->  Fill( ttMass, weight );
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
              histograms1d["topMassPred"]     ->  Fill( p4_top0.mass(), weight );
              if( p4_top0.mass() > topMassMin_ && p4_top0.mass() < topMassMax_ )  {
                passTopMass0 = true;
                double ttMass = (p4_top0+p4_top1).mass() ;
                histograms1d["ttMassType22Pred"]      ->  Fill( ttMass, weight );
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
                histograms1d["topMassPred"]   ->  Fill( p4_top0.mass(), weight );
                if( p4_top0.mass() > topMassMin_ && p4_top0.mass() < topMassMax_ )  {
                  passTopMass0 = true;
                  double ttMass = (p4_top0+p4_top1).mass() ;
                  histograms1d["ttMassType22Pred"]    ->  Fill( ttMass, weight );
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
            histograms1d["topMassPred"]     ->   Fill( p4_top0.mass(), weight );
            if( p4_top0.mass() > topMassMin_ && p4_top0.mass() < topMassMax_ )  {
              passTopMass0 = true;
              double ttMass = (p4_top0+p4_top1).mass() ;
              histograms1d["ttMassType22Pred"]      ->  Fill( ttMass, weight );
            }
          }
        }
      } // else 
    } // end Background estimation

  } // passType22

}



