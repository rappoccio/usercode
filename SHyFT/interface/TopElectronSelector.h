/*
How to use:     edm::Handle<std::vector<reco::Vertex> > primVtxHandle;
                event.getByLabel(pvTag_, primVtxHandle);
                typedef math::XYZPoint Point;
                Point PV  = primVtxHandle->at(0).position();

                TopElectronSelector patEleTight(TopElectronSelector::TIGHT, PV);
                for ( std::vector<pat::Electron>::const_iterator electronBegin = electronHandle->begin(),
                     electronEnd = electronHandle->end(), ielectron = electronBegin; ielectron != electronEnd; ++ielectron ) {
                bool passTight = patEleTight(*ielectron); }

Contact:        Sadia Khalil (skhalil@fnal.gov)
*/
#ifndef PhysicsTools_PatUtils_interface_TopElectronSelector_h
#define PhysicsTools_PatUtils_interface_TopElectronSelector_h

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "PhysicsTools/SelectorUtils/interface/Selector.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

//Math
#include "CLHEP/Units/GlobalPhysicalConstants.h"
typedef math::XYZPoint Point;

class TopElectronSelector : public Selector<pat::Electron>  {

   public: // interface  
      
      enum Version_t { VETO, LOOSE, MEDIUM, TIGHT, NONE, N_VERSIONS};
      TopElectronSelector() {}
      
      // initialize it by inserting directly the cut values in a parameter set
      TopElectronSelector( edm::ParameterSet const & parameters ){//, const Point PV){
     
         std::string versionStr = parameters.getParameter<std::string>("version");
         Version_t version = N_VERSIONS;
         
         if ( versionStr == "NONE" ){
            version  = NONE;
         }

         initialize( version,
                     parameters.getParameter<Double_t>("deta_EB"), 
                     parameters.getParameter<Double_t>("dphi_EB"),
                     parameters.getParameter<Double_t>("sihih_EB"), 
                     parameters.getParameter<Double_t>("hoe_EB"), 
                     parameters.getParameter<Double_t>("d0_EB"),
                     parameters.getParameter<Double_t>("dZ_EB"),
                     parameters.getParameter<Double_t>("ooemoop_EB"),
                     parameters.getParameter<Double_t>("deta_EE"), 
                     parameters.getParameter<Double_t>("dphi_EE"), 
                     parameters.getParameter<Double_t>("sihih_EE"), 
                     parameters.getParameter<Double_t>("hoe_EE"),
                     parameters.getParameter<Double_t>("d0_EE"),
                     parameters.getParameter<Double_t>("dZ_EE"),
                     parameters.getParameter<Double_t>("ooemoop_EE")
            );

         if ( parameters.exists("cutsToIgnore") )
            setIgnoredCuts( parameters.getParameter<std::vector<std::string> >("cutsToIgnore") ); 
                    
         retInternal_ = getBitTemplate();
         //pvSrc_ = parameters.getParameter<edm::InputTag>("pvSrc");
         //PVtx_ = PV;
      }
      
      void initialize(Version_t version,
                      Double_t sihih_EB, Double_t  dphi_EB, Double_t deta_EB, Double_t hoe_EB, Double_t d0_EB, Double_t dZ_EB, Double_t ooemoop_EB, 
                      Double_t sihih_EE, Double_t  dphi_EE, Double_t deta_EE, Double_t hoe_EE, Double_t d0_EE, Double_t dZ_EE, Double_t ooemoop_EE)
      {
         version_ = version;

         push_back("deta_EB"    );
         push_back("dphi_EB"    );
         push_back("sihih_EB"   ); 
         push_back("hoe_EB"     );
         push_back("d0_EB"      );
         push_back("dZ_EB"      );         
         push_back("ooemoop_EB" );
         push_back("deta_EE"    );
         push_back("dphi_EE"    );
         push_back("sihih_EE"   );        
         push_back("hoe_EE"     );
         push_back("d0_EE"      );
         push_back("dZ_EE"      ); 
         push_back("ooemoop_EE" );
              
         set("deta_EB",     deta_EB);
         set("dphi_EB",     dphi_EB);
         set("sihih_EB",    sihih_EB);        
         set("hoe_EB",      hoe_EB);
         set("d0_EB",       d0_EB);
         set("dZ_EB",       dZ_EB);
         set("ooemoop_EB",  ooemoop_EB);
         set("deta_EE",     deta_EE);
         set("dphi_EE",     dphi_EE);
         set("sihih_EE",    sihih_EE);        
         set("hoe_EE",      hoe_EE);
         set("d0_EB",       d0_EE);
         set("dZ_EB",       dZ_EE);
         set("ooemoop_EE",  ooemoop_EE); 

         indexSinhih_EB_     = index_type(&bits_, "sihih_EB"     ); 
         indexDphi_EB_       = index_type(&bits_, "dphi_EB"      );
         indexDeta_EB_       = index_type(&bits_, "deta_EB"      ); 
         indexHoE_EB_        = index_type(&bits_, "hoe_EB"       ); 
         indexD0_EB_         = index_type(&bits_, "d0_EB"        );
         indexDZ_EB_         = index_type(&bits_, "dZ_EB"        );
         indexOoemoop_EB_    = index_type(&bits_, "ooemoop_EB"   );
         indexSinhih_EE_     = index_type(&bits_, "sihih_EE"     ); 
         indexDphi_EE_       = index_type(&bits_, "dphi_EE"      );
         indexDeta_EE_       = index_type(&bits_, "deta_EE"      ); 
         indexHoE_EE_        = index_type(&bits_, "hoe_EE"       ); 
         indexD0_EE_         = index_type(&bits_, "d0_EE"        );
         indexDZ_EE_         = index_type(&bits_, "dZ_EE"        );
         indexOoemoop_EE_    = index_type(&bits_, "ooemoop_EE"   );    
      }

      // initialize it by using only the version name
      TopElectronSelector( Version_t  version)//, Point PV)                                          
      {
         if (version == NONE) {
            std::cout << "TopElectronSelector: If you want to use version NONE "
                      << "then you also have to provide the selection cuts by yourself " << std::endl;
            std::cout << "TopElectronSelector: ID Version is changed to TIGHT " << std::endl;
            version = TIGHT;
         }
         initialize(version);
         //pvSrc_ = parameters.getParameter<edm::InputTag>("pvSrc");
         //PVtx_ = PV;
         retInternal_ = getBitTemplate();
      }

      void initialize( Version_t version) 
      {
         version_ = version;
         push_back("deta_EB"    );
         push_back("dphi_EB"    );
         push_back("sihih_EB"   );
         push_back("hoe_EB"     );
         push_back("d0_EB"      );
         push_back("dZ_EB"      ); 
         push_back("ooemoop_EB" );
         push_back("deta_EE"    );
         push_back("dphi_EE"    );
         push_back("sihih_EE"   );
         push_back("hoe_EE"     ); 
         push_back("d0_EE"      );
         push_back("dZ_EE"      );  
         push_back("ooemoop_EE" );               
    
         if (version_ == VETO) {
            set("deta_EB",     7.0e-03);
            set("dphi_EB",     8.0e-01);
            set("sihih_EB",    1.0e-02);
            set("hoe_EB",      1.5e-01); 
            set("d0_EB",       4.0e-02);
            set("dZ_EB",       2.0e-01); 
            set("ooemoop_EB",  false);
            set("deta_EE",     1.0e-02);
            set("dphi_EE",     7.0e-01);
            set("sihih_EE",    3.0e-02);
            set("hoe_EE",      false);
            set("d0_EE",       4.0e-02);
            set("dZ_EE",       2.0e-01);
            set("ooemoop_EE",  false);
         }
         
         if (version_ == LOOSE) {
            set("deta_EB",     7.0e-03);
            set("dphi_EB",     1.5e-02);
            set("sihih_EB",    1.0e-02);
            set("hoe_EB",      1.2e-01);
            set("d0_EB",       2.0e-02);
            set("dZ_EB",       2.0e-01); 
            set("ooemoop_EB",  5.0e-02);
            set("deta_EE",     9.0e-03);
            set("dphi_EE",     1.0e-01);
            set("sihih_EE",    3.0e-02);
            set("hoe_EE",      1.0e-02);
            set("d0_EE",       2.0e-02);
            set("dZ_EE",       2.0e-01);
            set("ooemoop_EE",  5.0e-02);
         }

          if (version_ == MEDIUM) {
            set("deta_EB",     4.0e-03);
            set("dphi_EB",     6.0e-02);
            set("sihih_EB",    1.0e-02);
            set("hoe_EB",      1.2e-01); 
            set("d0_EB",       2.0e-02);
            set("dZ_EB",       1.0e-01); 
            set("ooemoop_EB",  5.0e-02);
            set("deta_EE",     7.0e-03);
            set("dphi_EE",     3.0e-02);
            set("sihih_EE",    3.0e-02);
            set("hoe_EE",      1.0e-02);
            set("d0_EE",       2.0e-02);
            set("dZ_EE",       1.0e-01);
            set("ooemoop_EE",  5.0e-02);
         }

          if (version_ == TIGHT) {
            set("deta_EB",     4.0e-03);
            set("dphi_EB",     3.0e-02);
            set("sihih_EB",    1.0e-02);
            set("hoe_EB",      1.2e-01); 
            set("d0_EB",       2.0e-02);
            set("dZ_EB",       1.0e-01); 
            set("ooemoop_EB",  5.0e-02);
            set("deta_EE",     5.0e-03);
            set("dphi_EE",     2.0e-02);
            set("sihih_EE",    3.0e-02);
            set("hoe_EE",      1.0e-02);
            set("d0_EE",       2.0e-02);
            set("dZ_EE",       1.0e-01);
            set("ooemoop_EE",  5.0e-02);
         }

         indexSinhih_EB_     = index_type(&bits_, "sihih_EB"     ); 
         indexDphi_EB_       = index_type(&bits_, "dphi_EB"      );
         indexDeta_EB_       = index_type(&bits_, "deta_EB"      ); 
         indexHoE_EB_        = index_type(&bits_, "hoe_EB"       ); 
         indexD0_EB_         = index_type(&bits_, "d0_EB"        );
         indexDZ_EB_         = index_type(&bits_, "dZ_EB"        );
         indexOoemoop_EB_    = index_type(&bits_, "ooemoop_EB"   );
         indexSinhih_EE_     = index_type(&bits_, "sihih_EE"     ); 
         indexDphi_EE_       = index_type(&bits_, "dphi_EE"      );
         indexDeta_EE_       = index_type(&bits_, "deta_EE"      ); 
         indexHoE_EE_        = index_type(&bits_, "hoe_EE"       ); 
         indexD0_EE_         = index_type(&bits_, "d0_EE"        );
         indexDZ_EE_         = index_type(&bits_, "dZ_EE"        );
         indexOoemoop_EE_    = index_type(&bits_, "ooemoop_EE"   );
      }

     

      // Allow for multiple definitions of the cuts. 
      bool operator()( const pat::Electron & electron, pat::strbitset & ret)//, edm::EventBase const & event) 
      {
         return spring12Cuts(electron, ret);//, event);
      }

      using Selector<pat::Electron>::operator();
      
      //Spring 12 cuts
      bool spring12Cuts( const pat::Electron & electron, pat::strbitset & ret)//, edm::EventBase const & event) 
      {
         ret.set(false);
        
        //  edm::Handle<std::vector<reco::Vertex> > pvtxHandle_;
//          event.getByLabel( pvSrc_, pvtxHandle_ );
//          Point PV(0,0,0);
//          if ( pvtxHandle_->size() > 0 ) {
//             PV = pvtxHandle_->at(0).position();
//          } else {
//             throw cms::Exception("InvalidInput") << " There needs to be at least one primary vertex in the event." << std::endl;
//          }
        
         Double_t Deta  = electron.deltaEtaSuperClusterTrackAtVtx();
         Double_t Dphi  = electron.deltaPhiSuperClusterTrackAtVtx(); 
         Double_t sihih = electron.sigmaIetaIeta();
         Double_t HoE   = electron.hadronicOverEm();  
         Double_t D0    = electron.dB();
         Double_t DZ    = electron.gsfTrack()->dz();//
         //Double_t DZ    = electron.gsfTrack()->dz(PVtx_);//
         Double_t Ooemoop = (1.0/electron.ecalEnergy() - electron.eSuperClusterOverP()/electron.ecalEnergy());

         // now apply the cuts
         if (electron.isEB()) { // BARREL case
            // check the EB cuts
            if ( sihih      <  cut(indexSinhih_EB_,double()) || ignoreCut(indexSinhih_EB_)) passCut(ret, indexSinhih_EB_);
            if ( fabs(Dphi) <  cut(indexDphi_EB_,  double()) || ignoreCut(indexDphi_EB_)  ) passCut(ret, indexDphi_EB_);
            if ( fabs(Deta) <  cut(indexDeta_EB_,  double()) || ignoreCut(indexDeta_EB_)  ) passCut(ret, indexDeta_EB_);
            if ( HoE        <  cut(indexHoE_EB_,   double()) || ignoreCut(indexHoE_EB_)   ) passCut(ret, indexHoE_EB_);
            if ( fabs(D0)   <  cut(indexD0_EB_,    double()) || ignoreCut(indexD0_EB_)    ) passCut(ret, indexD0_EB_);
            if ( fabs(DZ)   <  cut(indexDZ_EB_,    double()) || ignoreCut(indexDZ_EB_)    ) passCut(ret, indexDZ_EB_);
            if ( Ooemoop    <  cut(indexOoemoop_EB_, double()) || ignoreCut(indexOoemoop_EB_) ) passCut(ret, indexOoemoop_EB_);   
            // pass all the EE cuts
            passCut(ret, indexSinhih_EE_);	
            passCut(ret, indexDphi_EE_);	
            passCut(ret, indexDeta_EE_);	
            passCut(ret, indexHoE_EE_);	
            passCut(ret, indexD0_EE_);
            passCut(ret, indexDZ_EE_);
            passCut(ret, indexOoemoop_EE_);
 
         } else {  // ENDCAPS case
            // check the EE cuts
            if ( sihih      <  cut(indexSinhih_EE_,double()) || ignoreCut(indexSinhih_EE_)) passCut(ret, indexSinhih_EE_);
            if ( fabs(Dphi) <  cut(indexDphi_EE_,  double()) || ignoreCut(indexDphi_EE_)  ) passCut(ret, indexDphi_EE_);
            if ( fabs(Deta) <  cut(indexDeta_EE_,  double()) || ignoreCut(indexDeta_EE_)  ) passCut(ret, indexDeta_EE_);
            if ( HoE        <  cut(indexHoE_EE_,   double()) || ignoreCut(indexHoE_EE_)   ) passCut(ret, indexHoE_EE_);
            if ( D0         <  cut(indexD0_EE_,    double()) || ignoreCut(indexD0_EE_)    ) passCut(ret, indexD0_EE_);
            if ( DZ         <  cut(indexDZ_EE_,    double()) || ignoreCut(indexDZ_EE_)    ) passCut(ret, indexDZ_EE_);
            if ( Ooemoop    <  cut(indexOoemoop_EE_, double()) || ignoreCut(indexOoemoop_EE_) ) passCut(ret, indexOoemoop_EE_);  
            // pass all the EB cuts
            passCut(ret, indexSinhih_EB_);	
            passCut(ret, indexDphi_EB_);	
            passCut(ret, indexDeta_EB_);	
            passCut(ret, indexHoE_EB_);
            passCut(ret, indexD0_EB_);
            passCut(ret, indexDZ_EB_);
            passCut(ret, indexOoemoop_EB_);
         }
        
         setIgnored(ret);   
         return (bool)ret;
      }
    
   private: // member variables
      // version of the cuts  
      Version_t version_;
      //edm::InputTag pvSrc_;
      //Point PVtx_;
      index_type indexSinhih_EB_;
      index_type indexDphi_EB_;
      index_type indexDeta_EB_;
      index_type indexHoE_EB_;
      index_type indexD0_EB_;
      index_type indexDZ_EB_; 
      index_type indexOoemoop_EB_;
      index_type indexSinhih_EE_;
      index_type indexDphi_EE_;
      index_type indexDeta_EE_;
      index_type indexHoE_EE_;
      index_type indexD0_EE_;
      index_type indexDZ_EE_;
      index_type indexOoemoop_EE_;
};

#endif
