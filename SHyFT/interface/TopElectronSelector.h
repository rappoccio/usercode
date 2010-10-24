#ifndef PhysicsTools_PatUtils_interface_TopElectronSelector_h
#define PhysicsTools_PatUtils_interface_TopElectronSelector_h

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "PhysicsTools/SelectorUtils/interface/Selector.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

/*
Who should use : This is a simplified version of SimpleCutBaseElectronSelectionFunctor, what Nikos 
                 has implemented for egamma. It is meant to call TOP recommended electron selections.. 
                
How to use:      Make class instances to your required version, for example as

                 TopElectronSelector patEle70(TopElectronSelector::cIso70, use36xData_);
                 for ( std::vector<pat::Electron>::const_iterator electronBegin = electronHandle->begin(),
                     electronEnd = electronHandle->end(), ielectron = electronBegin;
                  ielectron != electronEnd; ++ielectron ) {
                 bool pass70 = patEle70(*ielectron);
                 }

Contact:         Sadia Khalil (skhalil@fnal.gov)
*/

//Math
#include "CLHEP/Units/GlobalPhysicalConstants.h"

class TopElectronSelector : public Selector<pat::Electron>  {

   public: // interface  
  
      enum Version_t { wp95, wp70, sigihih70, dphi70, deta70, hoe70, NONE };
      TopElectronSelector() {}
  
      // initialize it by inserting directly the cut values in a parameter set
      TopElectronSelector( edm::ParameterSet const & parameters, Bool_t is36xData)
      {
         // get the cuts from the PS
         initialize( parameters.getParameter<Double_t>("sihih_EB"), 
                     parameters.getParameter<Double_t>("dphi_EB"), 
                     parameters.getParameter<Double_t>("deta_EB"), 
                     parameters.getParameter<Double_t>("hoe_EB"),                      
                     parameters.getParameter<Double_t>("sihih_EE"), 
                     parameters.getParameter<Double_t>("dphi_EE"), 
                     parameters.getParameter<Double_t>("deta_EE"), 
                     parameters.getParameter<Double_t>("hoe_EE"), 
                     parameters.getParameter<Double_t>("relIso"),
                     parameters.getParameter<Double_t>("d0"),
                     parameters.getParameter<Double_t>("Et"));
         if ( parameters.exists("cutsToIgnore") )
            setIgnoredCuts( parameters.getParameter<std::vector<std::string> >("cutsToIgnore") );            
         retInternal_ = getBitTemplate();
         is36xData_ = is36xData;
      }
      // initialize it by using only the version name
      TopElectronSelector( Version_t  version, Bool_t is36xData)                                             
                                               
      {
         if (version == NONE) {
            std::cout << "TopElectronSelector: If you want to use version NONE "
                      << "then you have also to provide the selection cuts by yourself " << std::endl;
            std::cout << "TopElectronSelector: ID Version is changed to 70cIso " << std::endl;
            version = wp70;
         }
         initialize(version);
         retInternal_ = getBitTemplate();
         is36xData_  = is36xData;
      }

      void initialize( Version_t version) 
      {
         version_ = version;
         // push back the variables
         
         push_back("sihih_EB"   );
         push_back("dphi_EB"    );
         push_back("deta_EB"    );
         push_back("hoe_EB"     );
         push_back("sihih_EE"   );
         push_back("dphi_EE"    );
         push_back("deta_EE"    );
         push_back("hoe_EE"     );
         push_back("relIso"     );
         push_back("d0"         );
         push_back("Et"         );
                    
         if (version_ == wp95) {
            set("sihih_EB",    1.0e-02);
            set("dphi_EB",     8.0e-01);
            set("deta_EB",     7.0e-03);
            set("hoe_EB",      1.5e-01); 
            set("sihih_EE",    3.0e-02);
            set("dphi_EE",     7.0e-01);
            set("deta_EE",     1.0e-01);// 
            set("hoe_EE",      7.0e-02);
            set("relIso",      1.0e-00);
            set("d0",          false  );
            set("Et",          20.0   );
         }
         else if (version_ == wp70) {
            set("sihih_EB",    1.0e-02);
            set("dphi_EB",     3.0e-02);
            set("deta_EB",     4.0e-03);
            set("hoe_EB",      2.5e-02);
            set("sihih_EE",    3.0e-02);
            set("dphi_EE",     2.0e-02);
            set("deta_EE",     5.0e-03); //
            set("hoe_EE",      2.5e-02);
            set("relIso",      1.0e-01); 
            set("d0",          2.0e-02);
            set("Et",          30.0   );
         }
         else if (version == sigihih70){
            set("sihih_EB",    1.0e-02);
            set("sihih_EE",    3.0e-02);
            //set("relIso",      1.0e-01); 
            //set("d0",          2.0e-02);
            //set("Et",          30.0   );
         }
         else if (version == dphi70){
            set("dphi_EB",     3.0e-02);
            set("dphi_EE",     2.0e-02);
            //set("relIso",      1.0e-01); 
            //set("d0",          2.0e-02);
            //set("Et",          30.0   );
         }
         else if (version == deta70){
            set("deta_EB",     4.0e-03);
            set("deta_EE",     5.0e-03);//10000.
            //set("relIso",      1.0e-01); 
            //set("d0",          2.0e-02);
            //set("Et",          30.0   );
         }
         else if (version == hoe70){
            set("hoe_EB",      2.5e-02);
            set("hoe_EE",      2.5e-02);
            //set("relIso",      1.0e-01); 
            //set("d0",          2.0e-02);
            //set("Et",          30.0   );
         }

         indexSinhih_EB_     = index_type(&bits_, "sihih_EB"     ); 
         indexDphi_EB_       = index_type(&bits_, "dphi_EB"      );
         indexDeta_EB_       = index_type(&bits_, "deta_EB"      ); 
         indexHoE_EB_        = index_type(&bits_, "hoe_EB"       ); 
         indexSinhih_EE_     = index_type(&bits_, "sihih_EE"     ); 
         indexDphi_EE_       = index_type(&bits_, "dphi_EE"      );
         indexDeta_EE_       = index_type(&bits_, "deta_EE"      ); 
         indexHoE_EE_        = index_type(&bits_, "hoe_EE"       ); 
         indexRelIso_        = index_type(&bits_, "relIso"       );
         indexD0_            = index_type(&bits_, "d0"           );
         indexEt_            = index_type(&bits_, "Et"           );
      }

      void initialize(Double_t sihih_EB, Double_t  dphi_EB, Double_t deta_EB, Double_t hoe_EB,
                      Double_t sihih_EE, Double_t  dphi_EE, Double_t deta_EE, Double_t hoe_EE,
                      Double_t relIso, Double_t d0, Double_t et)
      {
         version_ = NONE;
         push_back("sihih_EB"   );
         push_back("dphi_EB"    );
         push_back("deta_EB"    );
         push_back("hoe_EB"     );
         push_back("sihih_EE"   );
         push_back("dphi_EE"    );
         push_back("deta_EE"    );
         push_back("hoe_EE"     );
         push_back("relIso"     );
         push_back("d0"         );
         push_back("Et"         );
     
         set("sihih_EB",    sihih_EB);
         set("dphi_EB",     dphi_EB);
         set("deta_EB",     deta_EB);
         set("hoe_EB",      hoe_EB);
         set("sihih_EE",    sihih_EE);
         set("dphi_EE",     dphi_EE);
         set("deta_EE",     deta_EE);
         set("hoe_EE",      hoe_EE);
         set("relIso",      relIso);
         set("d0",          d0);
         set("Et",          et);
      }

      bool operator()( const pat::Electron & electron, pat::strbitset & ret ) 
      {
         // for the time being only Spring10 variable definition
         return spring10Cuts(electron, ret);
      }
      using Selector<pat::Electron>::operator();
      // function with the Spring10 variable definitions
      bool spring10Cuts( const pat::Electron & electron, pat::strbitset & ret) 
      {
         ret.set(false);
         
         //Quick soloution to fix the Ecal endcap allignment if running on 36x
         //===================================================================
         math::XYZVector SCCorrPos(0, 0, 0);
         std::vector<double> cEEP(3);
         std::vector<double> cEEM(3);
         cEEP[0] =  0.52;
         cEEP[1] = -0.81;
         cEEP[2] =  0.81;
         cEEM[0] = -0.02;
         cEEM[1] = -0.81;
         cEEM[2] = -0.94;
 
         reco::SuperClusterRef SC = electron.superCluster();
         Double_t e_sc_x          = SC->x();
         Double_t e_sc_y          = SC->y();
         Double_t e_sc_z          = SC->z();
   
         Double_t eEta  = SC->eta();
         Double_t ePhi  = SC->phi();
         
         if(electron.isEE() && electron.eta() > 0){
            SCCorrPos =  math::XYZVector(e_sc_x + cEEP[0], e_sc_y + cEEP[1], e_sc_z + cEEP[2]);   
         }
         else if(electron.isEE() && electron.eta() < 0){
            SCCorrPos =  math::XYZVector(e_sc_x + cEEM[0], e_sc_y + cEEM[1], e_sc_z + cEEM[2]);  
         }
         else if(electron.isEB()){
            SCCorrPos =  math::XYZVector(e_sc_x, e_sc_y, e_sc_z);
         }
            
         Double_t deta_sc = SCCorrPos.eta() - eEta; 
         Double_t dphi_sc = correct_phi(SCCorrPos.phi() - ePhi); 
        
         //--------End Ecal Allignment--------------
         Double_t Deta = -1000.;
         Double_t Dphi = -1000.;
        
         if(is36xData_){           
            Deta = electron.deltaEtaSuperClusterTrackAtVtx() + deta_sc ;
            Dphi = correct_phi(electron.deltaPhiSuperClusterTrackAtVtx() + dphi_sc);
         }
         else{       
            Deta = electron.deltaEtaSuperClusterTrackAtVtx();
            Dphi = electron.deltaPhiSuperClusterTrackAtVtx();          
         }
      
         Double_t eleEt    = electron.p4().Pt();
         Double_t sihih    = electron.sigmaIetaIeta();
         Double_t HoE      = electron.hadronicOverEm();       
         Double_t relIso   = (electron.dr03TkSumPt()+electron.dr03EcalRecHitSumEt()+electron.dr03HcalTowerSumEt()) / eleEt;
         Double_t d0       = electron.dB();
         Double_t et       = electron.et();

         // now apply the cuts
         if (electron.isEB()) { // BARREL case
            // check the EB cuts
            if ( sihih      <  cut(indexSinhih_EB_,double()) || ignoreCut(indexSinhih_EB_)) passCut(ret, indexSinhih_EB_);
            if ( fabs(Dphi) <  cut(indexDphi_EB_,  double()) || ignoreCut(indexDphi_EB_)  ) passCut(ret, indexDphi_EB_);
            if ( fabs(Deta) <  cut(indexDeta_EB_,  double()) || ignoreCut(indexDeta_EB_)  ) passCut(ret, indexDeta_EB_);
            if ( HoE        <  cut(indexHoE_EB_,   double()) || ignoreCut(indexHoE_EB_)   ) passCut(ret, indexHoE_EB_);
            // pass all the EE cuts
            passCut(ret, indexSinhih_EE_);	
            passCut(ret, indexDphi_EE_);	
            passCut(ret, indexDeta_EE_);	
            passCut(ret, indexHoE_EE_);	
             
         } else {  // ENDCAPS case
            // check the EE cuts
            if ( sihih      <  cut(indexSinhih_EE_,double()) || ignoreCut(indexSinhih_EE_)) passCut(ret, indexSinhih_EE_);
            if ( fabs(Dphi) <  cut(indexDphi_EE_,  double()) || ignoreCut(indexDphi_EE_)  ) passCut(ret, indexDphi_EE_);
            if ( fabs(Deta) <  cut(indexDeta_EE_,  double()) || ignoreCut(indexDeta_EE_)  ) passCut(ret, indexDeta_EE_);
            if ( HoE        <  cut(indexHoE_EE_,   double()) || ignoreCut(indexHoE_EE_)   ) passCut(ret, indexHoE_EE_);
            // pass all the EB cuts
            passCut(ret, indexSinhih_EB_);	
            passCut(ret, indexDphi_EB_);	
            passCut(ret, indexDeta_EB_);	
            passCut(ret, indexHoE_EB_);
         }
         
         if ( relIso  < cut(indexRelIso_, double()) || ignoreCut(indexRelIso_)  ) passCut(ret, indexRelIso_ );
         if ( fabs(d0)< cut(indexD0_,     double()) || ignoreCut(indexD0_)      ) passCut(ret, indexD0_); 
         if ( et      > cut(indexEt_,     double()) || ignoreCut(indexEt_)      ) passCut(ret, indexEt_);

         setIgnored(ret);   
         return (bool)ret;
      }
      
      float correct_phi(float dphi){   
         if (fabs(dphi) > CLHEP::pi) {
            if (dphi < 0)
               dphi = CLHEP::twopi+dphi;
            else
               dphi = dphi-CLHEP::twopi; 
         }
         return dphi;
      }
      
   private: // member variables
      // version of the cuts  
      Version_t version_;
      Bool_t is36xData_;      
      index_type indexSinhih_EB_;
      index_type indexDphi_EB_;
      index_type indexDeta_EB_;
      index_type indexHoE_EB_;
      index_type indexSinhih_EE_;
      index_type indexDphi_EE_;
      index_type indexDeta_EE_;
      index_type indexHoE_EE_;
      index_type indexRelIso_;
      index_type indexD0_; 
      index_type indexEt_;
};


#endif
