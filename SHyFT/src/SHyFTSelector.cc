#include "Analysis/SHyFT/interface/SHyFTSelector.h"
#include "DataFormats/Candidate/interface/ShallowCloneCandidate.h"


#include <iostream>

using namespace std;

SHyFTSelector::SHyFTSelector( edm::ParameterSet const & params ) :
   EventSelector(),
   muonTag_         (params.getParameter<edm::InputTag>("muonSrc") ),
   electronTag_     (params.getParameter<edm::InputTag>("electronSrc") ),
   jetTag_          (params.getParameter<edm::InputTag>("jetSrc") ),
   metTag_          (params.getParameter<edm::InputTag>("metSrc") ),  
   trigTag_         (params.getParameter<edm::InputTag>("trigSrc") ),
   muTrig_          (params.getParameter<std::string>("muTrig")),
   eleTrig_         (params.getParameter<std::string>("eleTrig")),
   pvSelector_      (params.getParameter<edm::ParameterSet>("pvSelector") ),
   muonIdTight_     (params.getParameter<edm::ParameterSet>("muonIdTight") ),
   electronIdTight_ (params.getParameter<edm::ParameterSet>("electronIdTight") ),
   muonIdLoose_     (params.getParameter<edm::ParameterSet>("muonIdLoose") ),
   electronIdLoose_ (params.getParameter<edm::ParameterSet>("electronIdLoose") ),
   jetIdLoose_      (params.getParameter<edm::ParameterSet>("jetIdLoose") ),
   pfjetIdLoose_    (params.getParameter<edm::ParameterSet>("pfjetIdLoose") ),
   minJets_         (params.getParameter<int> ("minJets") ),
   muJetDR_         (params.getParameter<double>("muJetDR")),
   eleJetDR_        (params.getParameter<double>("eleJetDR")),
   muPlusJets_      (params.getParameter<bool>("muPlusJets") ),
   ePlusJets_       (params.getParameter<bool>("ePlusJets") ),
   muPtMin_         (params.getParameter<double>("muPtMin")), 
   muEtaMax_        (params.getParameter<double>("muEtaMax")), 
   eleEtMin_        (params.getParameter<double>("eleEtMin")), 
   eleEtaMax_       (params.getParameter<double>("eleEtaMax")), 
   muPtMinLoose_    (params.getParameter<double>("muPtMinLoose")), 
   muEtaMaxLoose_   (params.getParameter<double>("muEtaMaxLoose")), 
   eleEtMinLoose_   (params.getParameter<double>("eleEtMinLoose")), 
   eleEtaMaxLoose_  (params.getParameter<double>("eleEtaMaxLoose")), 
   jetPtMin_        (params.getParameter<double>("jetPtMin")), 
   jetEtaMax_       (params.getParameter<double>("jetEtaMax")), 
   jetScale_        (params.getParameter<double>("jetScale")),
   jetUncertainty_  (params.getParameter<double>("jetUncertainty")),
   jetSmear_        (params.getParameter<double>("jetSmear")),
   metMin_          (params.getParameter<double>("metMin")),
   unclMetScale_    (params.getParameter<double>("unclMetScale")),
   elDist_          (params.getParameter<double>("elDist")),
   elDcot_          (params.getParameter<double>("elDcot")),
   eRelIso_         (params.getParameter<double>("eRelIso")),
   eEt_             (params.getParameter<double>("eEtCut")),
   pvTag_           (params.getParameter<edm::InputTag>("pvSrc") ),
   use36xData_      (params.getParameter<bool>("use36xData")),
   useAntiSelection_(params.getParameter<bool>("useAntiSelection")),
   useEleMC_        (params.getParameter<bool>("useEleMC")),
   jecPayload_      (params.getParameter<std::string>("jecPayload"))
{
   // make the bitset
   push_back( "Inclusive"      );
   push_back( "Trigger"        );
   push_back( "PV"             );
   push_back( ">= 1 Lepton"    );
   push_back( "== 1 Tight Lepton"    );
   push_back( "== 1 Tight Lepton, Mu Veto");
   push_back( "== 1 Lepton"    );
   push_back( "MET Cut"        );
   push_back( "Z Veto"         );
   push_back( "Conversion Veto A");
   push_back( "Conversion Veto B");
   push_back( "Cosmic Veto"    );
   push_back( ">=1 Jets"       );
   push_back( ">=2 Jets"       );
   push_back( ">=3 Jets"       );
   push_back( ">=4 Jets"       );
   push_back( ">=5 Jets"       );


   // turn (almost) everything on by default
   set( "Inclusive"      );
   set( "Trigger"        );
   set( "PV"             );
   set( ">= 1 Lepton"    );
   set( "== 1 Tight Lepton"    );
   set( "== 1 Tight Lepton, Mu Veto");
   set( "== 1 Lepton"    );
   set( "MET Cut"        );
   set( "Z Veto"         );
   set( "Conversion Veto A");
   set( "Conversion Veto B");
   set( "Cosmic Veto"    );
   set( ">=1 Jets", minJets_ >= 1);
   set( ">=2 Jets", minJets_ >= 2);
   set( ">=3 Jets", minJets_ >= 3);
   set( ">=4 Jets", minJets_ >= 4);
   set( ">=5 Jets", minJets_ >= 5); 


   inclusiveIndex_ = index_type(&bits_, std::string("Inclusive"      ));
   triggerIndex_ = index_type(&bits_, std::string("Trigger"        ));
   pvIndex_ = index_type(&bits_, std::string("PV"             ));
   lep1Index_ = index_type(&bits_, std::string(">= 1 Lepton"    ));
   lep2Index_ = index_type(&bits_, std::string("== 1 Tight Lepton"    ));
   lep3Index_ = index_type(&bits_, std::string("== 1 Tight Lepton, Mu Veto"));
   lep4Index_ = index_type(&bits_, std::string("== 1 Lepton"    ));
   metIndex_ = index_type(&bits_, std::string("MET Cut"        ));
   zvetoIndex_ = index_type(&bits_, std::string("Z Veto"         ));
   conversionIndexA_ = index_type(&bits_, std::string("Conversion Veto A"));
   conversionIndexB_ = index_type(&bits_, std::string("Conversion Veto B"));
   cosmicIndex_ = index_type(&bits_, std::string("Cosmic Veto"    ));
   jet1Index_ = index_type(&bits_, std::string(">=1 Jets"));
   jet2Index_ = index_type(&bits_, std::string(">=2 Jets"));
   jet3Index_ = index_type(&bits_, std::string(">=3 Jets"));
   jet4Index_ = index_type(&bits_, std::string(">=4 Jets"));
   jet5Index_ = index_type(&bits_, std::string(">=5 Jets")); 

   if ( params.exists("cutsToIgnore") )
      setIgnoredCuts( params.getParameter<std::vector<std::string> >("cutsToIgnore") );
	

   retInternal_ = getBitTemplate();

   jecUnc_ = boost::shared_ptr<JetCorrectionUncertainty>( new JetCorrectionUncertainty(jecPayload_));

}

bool SHyFTSelector::operator() ( edm::EventBase const & event, pat::strbitset & ret)
{

   ret.set(false);

   allJets_.clear();
   selectedJets_.clear();
   cleanedJets_.clear();
   allMuons_.clear();
   selectedMuons_.clear();
   oldElectrons_.clear();
   looseMuons_.clear();
   looseElectrons_.clear();
   selectedMETs_.clear();
   allElectrons_.clear();
   selectedElectrons_.clear();//to select ==1 tight electron or anti-electron depends on the switch
   selectedLooseElectrons_.clear();//to apply ZVeto  
   selectedLooseMuons_.clear();
   passCut( ret, inclusiveIndex_);


   bool passTrig = false;
   if (!ignoreCut(triggerIndex_) ) {


      edm::Handle<pat::TriggerEvent> triggerEvent;
      event.getByLabel(trigTag_, triggerEvent);
    
      pat::TriggerEvent const * trig = &*triggerEvent;
      
      if ( muPlusJets_ && trig->wasRun() && trig->wasAccept() ) {   
         pat::TriggerPath const * muPath = trig->path(muTrig_);
       
         if ( muPath != 0 && muPath->wasAccept() ) {
            passTrig = true;    
         }  
       
      } 
    
      if(ePlusJets_){
         if(!useEleMC_ && trig->wasRun() && trig->wasAccept() ){
            pat::TriggerPath const * elePath = trig->path(eleTrig_);
          
            if (elePath != 0 && elePath->wasAccept() ) {
               passTrig = true;
            }
         }
         else if(useEleMC_)  {passTrig = true;}
      }
   }
  


  
   if ( ignoreCut(triggerIndex_) || 
        passTrig ) {
      passCut(ret, triggerIndex_);


      bool passPV = false;

      passPV = pvSelector_( event );
      if ( ignoreCut(pvIndex_) || passPV ) {
         passCut(ret, pvIndex_);
  
         edm::Handle<std::vector<reco::Vertex> > primVtxHandle;
         event.getByLabel(pvTag_, primVtxHandle);           

         edm::Handle< vector< pat::Electron > > electronHandle;
         event.getByLabel (electronTag_, electronHandle);
  
         edm::Handle< vector< pat::Muon > > muonHandle;
         event.getByLabel (muonTag_, muonHandle);

         edm::Handle< vector< pat::Jet > > jetHandle;

         edm::Handle< edm::OwnVector<reco::Candidate> > jetClonesHandle ;

         edm::Handle< vector< pat::MET > > metHandle;
         event.getByLabel (metTag_, metHandle);


	 reco::Candidate::LorentzVector metP4 = metHandle->at(0).p4();

         TopElectronSelector patEle70(TopElectronSelector::wp70, use36xData_);
         TopElectronSelector patEle95(TopElectronSelector::wp95, use36xData_);
         TopElectronSelector EleSihih(TopElectronSelector::sigihih70, use36xData_);
         TopElectronSelector EleDphi(TopElectronSelector::dphi70, use36xData_);
         TopElectronSelector EleDeta(TopElectronSelector::deta70, use36xData_); 
         TopElectronSelector EleHoE(TopElectronSelector::hoe70, use36xData_); 
      
         bool conversionVetoA = true;
         bool conversionVetoB = true;
         double PVz = -999;
         if ( primVtxHandle->size() > 0 ) {
            PVz = primVtxHandle->at(0).z();
         } else {
            throw cms::Exception("InvalidInput") << " There needs to be at least one primary vertex in the event." << std::endl;
         }


         int nElectrons = 0;
         for ( std::vector<pat::Electron>::const_iterator electronBegin = electronHandle->begin(),
                  electronEnd = electronHandle->end(), ielectron = electronBegin;
               ielectron != electronEnd; ++ielectron ) {
	   allElectrons_.push_back( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Electron>( electronHandle, ielectron - electronBegin ) ) );
            ++nElectrons;

            bool pass70       = patEle70(*ielectron);
            bool pass95       = patEle95(*ielectron);
            bool pass_sihih   = EleSihih(*ielectron);
            bool pass_dphi    = EleDphi(*ielectron);
            bool pass_deta    = EleDeta(*ielectron);
            bool pass_hoe     = EleHoE(*ielectron);
    
            double scEta   = fabs( ielectron->superCluster()->eta() );
            double Et      = ielectron->et();
            double dB      = ielectron->dB();
            double vCut    = fabs(PVz - ielectron->vertex().z());
            float  el_dist = ielectron->userFloat("el_dist");
            float  el_dcot = ielectron->userFloat("el_dcot");
            bool   isConv  = fabs(el_dist) < elDist_ && fabs(el_dcot) < elDcot_ ;            
            double nHits   = ielectron->gsfTrack()->trackerExpectedHitsInner().numberOfHits();
            double relIso  = ( ielectron->dr03TkSumPt() + ielectron->dr03EcalRecHitSumEt() + ielectron->dr03HcalTowerSumEt() ) / ielectron->p4().Pt();

//Electron Selection for e+jets
//-----------------------------
            if( (scEta > 2.5 || scEta <= 1.566 )  && scEta > 1.4442 ) continue;   
            if( fabs(ielectron->eta()) >= eleEtaMaxLoose_ ) continue;
            //bool passd0;
            
            if(useAntiSelection_){
               if( Et       > eEt_                                         &&                   
                   relIso   < eRelIso_                                     &&
                   vCut     < 1                                            && 
                   ( fabs(dB) < 0.02  + pass_sihih + pass_dphi + pass_deta + pass_hoe ) <= 2 ){  //fail atleast two of the IDs                 
                  selectedElectrons_.push_back( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Electron>( electronHandle, ielectron - electronBegin ) ) );
                  if(nHits > 0 ) conversionVetoA = false;
                  if(nHits > 0 || isConv) conversionVetoB = false;                  
               }
               else if(pass95 ){
                  selectedLooseElectrons_.push_back( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Electron>( electronHandle, ielectron - electronBegin ) ) );
               }   
            }//anti
            
            else{
               if( pass70 && vCut < 1 ) { //tight            
                  selectedElectrons_.push_back( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Electron>( electronHandle, ielectron - electronBegin ) ) );
                  if(nHits > 0 ) conversionVetoA = false;
                  if(nHits > 0 || isConv) conversionVetoB = false;  
               }
               else if( pass95 ){//loose
                  selectedLooseElectrons_.push_back( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Electron>( electronHandle, ielectron - electronBegin ) ) );            
               }            
            }//else regular selection
            
            

//Electron Selection for mu+jets
//------------------------------
            

            // Tight cuts
            if ( ielectron->et() > eleEtMin_ && fabs(ielectron->eta()) < eleEtaMax_ && 
                 electronIdTight_(*ielectron) &&
                 ielectron->electronID( "eidRobustTight" ) > 0  ) {
               oldElectrons_.push_back( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Electron>( electronHandle, ielectron - electronBegin ) ) );
            } else {
               // Loose cuts
               if ( ielectron->et() > eleEtMinLoose_ && fabs(ielectron->eta()) < eleEtaMaxLoose_ && 
                    electronIdLoose_(*ielectron) ) {
                  looseElectrons_.push_back( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Electron>( electronHandle, ielectron - electronBegin ) ) );
               }
            }
         }


//Loose Muon Selection to be vetoed for electron selection 
//--------------------------------------------------------
           
         for ( std::vector<pat::Muon>::const_iterator muonBegin = muonHandle->begin(),
                  muonEnd = muonHandle->end(), imuon = muonBegin;
               imuon != muonEnd; ++imuon ) {   
            if ( !imuon->isGlobalMuon() ) continue;
            if ( imuon->pt() > muPtMinLoose_ && fabs(imuon->eta()) < muEtaMaxLoose_ &&  muonIdLoose_(*imuon,event) ) {
               selectedLooseMuons_.push_back( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Muon>( muonHandle, imuon - muonBegin ) ) );
            }
         }

//Muon Selection for mu+jets
//--------------------------     
  
         for ( std::vector<pat::Muon>::const_iterator muonBegin = muonHandle->begin(),
                  muonEnd = muonHandle->end(), imuon = muonBegin;
               imuon != muonEnd; ++imuon ) {
	   allMuons_.push_back( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Muon>( muonHandle, imuon - muonBegin ) ) );
	   if ( !imuon->isGlobalMuon() ) continue;
	
	   // Tight cuts
	   bool passTight = muonIdTight_(*imuon,event) && imuon->isTrackerMuon() ;
	   if (  imuon->pt() > muPtMin_ && fabs(imuon->eta()) < muEtaMax_ && 
		 passTight ) {

	     selectedMuons_.push_back( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Muon>( muonHandle, imuon - muonBegin ) ) );
	   } else {
	     // Loose cuts
	     if ( imuon->pt() > muPtMinLoose_ && fabs(imuon->eta()) < muEtaMaxLoose_ && 
		  muonIdLoose_(*imuon,event) ) {
	       looseMuons_.push_back( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Muon>( muonHandle, imuon - muonBegin ) ) );
	     }
	   }
         }
	 

         event.getByLabel (jetTag_, jetHandle);
         pat::strbitset ret1 = jetIdLoose_.getBitTemplate();
         pat::strbitset ret2 = pfjetIdLoose_.getBitTemplate();
         for ( std::vector<pat::Jet>::const_iterator jetBegin = jetHandle->begin(),
                  jetEnd = jetHandle->end(), ijet = jetBegin;
               ijet != jetEnd; ++ijet ) {

	   // Here will be the working variable for all the jet energy effects
	   reco::Candidate::LorentzVector scaledJetP4 = ijet->p4();

	   // get a copy of the uncorrected p4
	   reco::Candidate::LorentzVector uncorrJet = ijet->correctedP4(0);

	   // -------
	   // Jet energy scale variation
	   //    - Also computes a piece of MET uncertainty due to this effect
	   // -------
	   if ( fabs(jetScale_) > 0.0 ) {	     
	     // First subtract the uncorrected px and py from MET
	     metP4.SetPx( metP4.Px() + uncorrJet.px() );
	     metP4.SetPy( metP4.Py() + uncorrJet.py() );

	     // Now get the uncertainties
	     jecUnc_->setJetEta( ijet->eta() );
	     jecUnc_->setJetPt( ijet->pt() );
	     double unc = fabs(jecUnc_->getUncertainty( bool(jetScale_ > 0) ));

	     // Add the "flat" flavor dependent corrections in quadrature
	     unc = sqrt( unc*unc + jetUncertainty_*jetUncertainty_);
	     
	     // Scale up or down by jetScale_
	     double ijetscale = (1 + jetScale_ * unc);
	     scaledJetP4 *= ijetscale;

	     // Correct the MET back again for this effect
	     metP4.SetPx( metP4.Px() - uncorrJet.px() * ijetscale);
	     metP4.SetPy( metP4.Py() - uncorrJet.py() * ijetscale);	     
	   }

	   // -------
	   // Jet energy resolution variation
	   //    - Also computes a piece of MET uncertainty due to this effect
	   // -------
	   if ( fabs(jetSmear_) > 0.0 && ijet->genJet() != 0 && ijet->genJet()->pt() > 15.0 ) {
	     // First subtract the uncorrected px and py from MET
	     metP4.SetPx( metP4.Px() + uncorrJet.px() );
	     metP4.SetPy( metP4.Py() + uncorrJet.py() );
	     // Next smear the jets
	     double scale = jetSmear_;
	     double recopt = ijet->pt();
	     double genpt = ijet->genJet()->pt();
	     double deltapt = (recopt-genpt)*scale;
	     double ptscale = std::max((double)0.0,(recopt+deltapt)/recopt);
	     scaledJetP4 *= ptscale;
	     // Correct the MET back again for this effect
	     metP4.SetPx( metP4.Px() - uncorrJet.px() * ptscale);
	     metP4.SetPy( metP4.Py() - uncorrJet.py() * ptscale);
	   }



	   reco::ShallowClonePtrCandidate scaledJet ( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Jet>( jetHandle, ijet - jetBegin ),
										      ijet->charge(),
										      scaledJetP4 ) );
	   allJets_.push_back( scaledJet );
            bool passJetID = false;
            if ( ijet->isCaloJet() || ijet->isJPTJet() ) {
               passJetID = jetIdLoose_(*ijet, ret1);
            }
            else {
               passJetID = pfjetIdLoose_(*ijet, ret2);
            }
            if ( scaledJet.pt() > jetPtMin_ && fabs(scaledJet.eta()) < jetEtaMax_ && passJetID ) {
              
               selectedJets_.push_back( scaledJet );

               if ( muPlusJets_ ) {

                  //Remove some jets
                  bool indeltaR = false;
                  for( std::vector<reco::ShallowClonePtrCandidate>::const_iterator muonBegin = selectedMuons_.begin(),
                          muonEnd = selectedMuons_.end(), imuon = muonBegin;
                       imuon != muonEnd; ++imuon ) {
                     if( reco::deltaR( imuon->eta(), imuon->phi(), scaledJet.eta(), scaledJet.phi() ) < muJetDR_ )
                     {  indeltaR = true; }
                  }
                  if( !indeltaR ) {
                     cleanedJets_.push_back( scaledJet );
                  }// end if jet is not within dR of a muon
               }// end if mu+jets
               else {
                  //Remove some jets
                  bool indeltaR = false;
                  for( std::vector<reco::ShallowClonePtrCandidate>::const_iterator electronBegin = selectedElectrons_.begin(),
                          electronEnd = selectedElectrons_.end(), ielectron = electronBegin;
                       ielectron != electronEnd; ++ielectron ) {
                     if( reco::deltaR( ielectron->eta(), ielectron->phi(), scaledJet.eta(), scaledJet.phi() ) < eleJetDR_ )
                     {  indeltaR = true; }
                  }
                  if( !indeltaR ) {
                     cleanedJets_.push_back( scaledJet );
                  }// end if jet is not within dR of an electron
               }// end if e+jets
            }// end if pass id and kin cuts
         }// end loop over jets



	   
	 // -------
	 // Unclustered MET resolution
	 // -------
	 if ( unclMetScale_ > 0.0 ) {

	   // Subtract off the (uncorrected) jets
	   for ( std::vector<reco::ShallowClonePtrCandidate>::const_iterator jetBegin = allJets_.begin(),
		   jetEnd = allJets_.end(), ijet = jetBegin;
		 ijet != jetEnd; ++ijet ) {
	     pat::Jet const & jet = dynamic_cast<pat::Jet const &>( *(ijet->masterClonePtr().get() ));
	     metP4.SetPx( metP4.px() + jet.correctedP4(0).px() );
	     metP4.SetPy( metP4.py() + jet.correctedP4(0).py() );
	   }

	   // Subtract off muons
	   for ( std::vector<reco::ShallowClonePtrCandidate>::const_iterator muBegin = allMuons_.begin(),
		   muEnd = allMuons_.end(), imu = muBegin;
		 imu != muEnd; ++imu ) {
	     metP4.SetPx( metP4.px() + imu->px() );
	     metP4.SetPy( metP4.py() + imu->py() );	       
	   }

	   // Subtract off electrons
	   for ( std::vector<reco::ShallowClonePtrCandidate>::const_iterator eleBegin = allElectrons_.begin(),
		   eleEnd = allElectrons_.end(), iele = eleBegin;
		 iele != eleEnd; ++iele ) {
	     metP4.SetPx( metP4.px() + iele->px() );
	     metP4.SetPy( metP4.py() + iele->py() );	       
	   }

	   // met_x and met_y are now unclustered energy
	   // apply the 10% on the unclustered energy. "factor" is either 0.9 or 1.1, for MET_minus or MET_plus, resp.
	   metP4.SetPx( metP4.px() * unclMetScale_ );
	   metP4.SetPy( metP4.py() * unclMetScale_ );


	   // Add back the jets
	   for ( std::vector<reco::ShallowClonePtrCandidate>::const_iterator jetBegin = allJets_.begin(),
		   jetEnd = allJets_.end(), ijet = jetBegin;
		 ijet != jetEnd; ++ijet ) {
	     pat::Jet const & jet = dynamic_cast<pat::Jet const &>( *(ijet->masterClonePtr().get() ));
	     metP4.SetPx( metP4.px() - jet.correctedP4(0).px() );
	     metP4.SetPy( metP4.py() - jet.correctedP4(0).py() );
	   }

	   // Add back the muons
	   for ( std::vector<reco::ShallowClonePtrCandidate>::const_iterator muBegin = allMuons_.begin(),
		   muEnd = allMuons_.end(), imu = muBegin;
		 imu != muEnd; ++imu ) {
	     metP4.SetPx( metP4.px() - imu->px() );
	     metP4.SetPy( metP4.py() - imu->py() );	       
	   }


	   // Add back the electrons
	   for ( std::vector<reco::ShallowClonePtrCandidate>::const_iterator eleBegin = allElectrons_.begin(),
		   eleEnd = allElectrons_.end(), iele = eleBegin;
		 iele != eleEnd; ++iele ) {
	     metP4.SetPx( metP4.px() - iele->px() );
	     metP4.SetPy( metP4.py() - iele->py() );	       
	   }


	 }


	 // Set the MET
         met_ = reco::ShallowClonePtrCandidate( edm::Ptr<pat::MET>( metHandle, 0),
                                                metHandle->at(0).charge(),
                                                metP4 );



         int nleptons = 0;
         if ( muPlusJets_ )
            nleptons += selectedMuons_.size();
      
         if ( ePlusJets_ ) 
            nleptons += selectedElectrons_.size();

         if ( ignoreCut(lep1Index_) || 
              ( nleptons > 0 ) ){
            passCut( ret, lep1Index_);


            if ( ignoreCut(lep2Index_) || 
                 ( nleptons == 1 ) ){
               passCut( ret, lep2Index_);
              

               //const pat::Electron * electron_ = 0;
               //electron_ = dynamic_cast<const pat::Electron *>(selectedElectrons_[0].masterClonePtr().get());
               
              
               

               bool oneMuon = 
                  ( selectedMuons_.size() == 1 && 
                    looseMuons_.size() + oldElectrons_.size() + looseElectrons_.size() == 0 
                     );
               bool oneElectron =                      //Lets ignore the dilepton cut 
                  ( selectedElectrons_.size() == 1 &&
                     selectedLooseMuons_.size() + selectedMuons_.size() == 0 
                     );

               bool oneMuonMuVeto = 
                  ( selectedMuons_.size() == 1 && 
                    looseMuons_.size() == 0 
                     );
               bool oneElectronMuVeto = 
                  ( selectedElectrons_.size() == 1 && 
                    selectedLooseMuons_.size() == 0
                    //looseMuons_.size() == 0 
                     );
      
               if ( ignoreCut(lep3Index_) || 
                    (ePlusJets_ &&  oneElectronMuVeto)||
                    (muPlusJets_ && oneMuonMuVeto)
                  ) {
                  passCut(ret, lep3Index_);

                  
                  if ( ignoreCut(lep4Index_) || 
                       ( (muPlusJets_ && oneMuon) ^ (ePlusJets_ && oneElectronMuVeto )  )
                     ) {
                     passCut(ret, lep4Index_);	  
  
                                       
                     bool metCut = met_.pt() > metMin_;
                     if ( ignoreCut(metIndex_) ||
                          metCut ) {
                        passCut( ret, metIndex_ );
	  
                     

                        bool zVeto = true;
  
                        if(ePlusJets_){
                             
                           for(std::vector<reco::ShallowClonePtrCandidate>::const_iterator iele1 = selectedElectrons_.begin();
                               iele1 != selectedElectrons_.end(); ++iele1){
                              for(std::vector<reco::ShallowClonePtrCandidate>::const_iterator iele2  = selectedLooseElectrons_.begin();
                                  iele2 != selectedLooseElectrons_.end(); ++iele2){
                                 // if (iele1->charge() * iele2->charge() >= 0) continue;
                                 double Zmass = ((iele1->p4() + iele2->p4()).M());
                                 if (Zmass <= 106 && Zmass >= 76) zVeto = false;
                              }
                           }
                        }
                        if ( selectedMuons_.size() == 2 ) {
                        }
		
                        if ( ignoreCut(zvetoIndex_) ||
                             zVeto ){
                           passCut(ret, zvetoIndex_);
                           
                          
  
                           //bool cached before
                           if ( ignoreCut(conversionIndexA_) || 
                                conversionVetoA ) {
                              passCut(ret,conversionIndexA_);
		
                              if ( ignoreCut(conversionIndexB_) || 
                                   conversionVetoB ) {
                                 passCut(ret,conversionIndexB_);

                                 bool cosmicVeto = true;
                                 if ( ignoreCut(cosmicIndex_) ||
                                      cosmicVeto ) {
                                    passCut(ret,cosmicIndex_);

                                    if ( ignoreCut(jet1Index_) ||
                                         static_cast<int>(cleanedJets_.size()) >=  1 ){
                                       passCut(ret,jet1Index_);  
                                    } // end if >=1 tight jets

                                    if ( ignoreCut(jet2Index_) ||
                                         static_cast<int>(cleanedJets_.size()) >=  2 ){
                                       passCut(ret,jet2Index_);  
                                    } // end if >=2 tight jets

                                    if ( ignoreCut(jet3Index_) ||
                                         static_cast<int>(cleanedJets_.size()) >=  3 ){
                                       passCut(ret,jet3Index_);  
                                    } // end if >=3 tight jets

                                    if ( ignoreCut(jet4Index_) ||
                                         static_cast<int>(cleanedJets_.size()) >=  4 ){
                                       passCut(ret,jet4Index_);  
                                    } // end if >=4 tight jets

                                    if ( ignoreCut(jet5Index_) ||
                                         static_cast<int>(cleanedJets_.size()) >=  5 ){
                                       passCut(ret,jet5Index_);  
                                    } // end if >=5 tight jets
		  
                                 } // end if cosmic veto
		
                              } //end if conversion veto A
                           } // end if conversion veto B

                        } // end if z veto

                     } // end if met cut
	
                  } // end if == 1 lepton

               } // end if == 1 tight lepton with a muon veto separately

            } // end if == 1 tight lepton

         } // end if >= 1 lepton

      } // end if PV
    
   } // end if trigger


   setIgnored(ret);
   return (bool)ret;
}
