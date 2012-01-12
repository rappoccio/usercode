// system include files
#include <memory>
#include <iostream>
#include <string>
#include <vector>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/ValueMap.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "Analysis/EDSHyFT/plugins/BTagSFUtil_tprime.h"
#include "RecoBTag/Records/interface/BTagPerformanceRecord.h"
#include "CondFormats/PhysicsToolsObjects/interface/BinningPointByMap.h"
#include "RecoBTag/PerformanceDB/interface/BtagPerformance.h"
#include "FWCore/Framework/interface/ESHandle.h"

class BTaggingSFProducer : public edm::EDProducer {
public:
  explicit BTaggingSFProducer(const edm::ParameterSet&);
  ~BTaggingSFProducer();
  
private:
  virtual void beginJob() ;
  virtual void produce(edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;
  
  // ----------member data --------------------------
  edm::InputTag jetSource_;
  std::string tagger_;
  double discriminantValue_;
  std::string result_;

  // just counting bs and others
  int countbs;
  int countbs_tagged;
  int countbs_modtag;

  int countNObs;
  int count_NObsTagged;
  int count_NObsModTag;
};

BTaggingSFProducer::BTaggingSFProducer(const edm::ParameterSet& iConfig)
{
        jetSource_= iConfig.getParameter<edm::InputTag>("jetSource");
	tagger_ = iConfig.getParameter<std::string>("Tagger");
	discriminantValue_ = iConfig.getParameter<double>("DiscriminantValue");

	produces< std::vector< pat::Jet > >();
		
	//        produces<edm::ValueMap<int> >().setBranchAlias("bTaggingSetting");

	countbs = 0;
	countbs_tagged = 0;
	countbs_modtag = 0;
	countNObs = 0;
	count_NObsTagged = 0;
	count_NObsModTag = 0;

	
}

BTaggingSFProducer::~BTaggingSFProducer()
{

}

// ------------ method called to produce the data  ------------
void
BTaggingSFProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
        using namespace edm;
        using namespace reco;

        // GETTING DB INFORMATION

	std::map<std::string,PerformanceResult::ResultType> measureMap;
        measureMap["BTAGBEFF"]=PerformanceResult::BTAGBEFF;
        measureMap["BTAGBERR"]=PerformanceResult::BTAGBERR;
        measureMap["BTAGCEFF"]=PerformanceResult::BTAGCEFF;
	measureMap["BTAGCERR"]=PerformanceResult::BTAGCERR;
        measureMap["BTAGLEFF"]=PerformanceResult::BTAGLEFF;
        measureMap["BTAGLERR"]=PerformanceResult::BTAGLERR;
        measureMap["BTAGNBEFF"]=PerformanceResult::BTAGNBEFF;
        measureMap["BTAGNBERR"]=PerformanceResult::BTAGNBERR;
	measureMap["BTAGBEFFCORR"]=PerformanceResult::BTAGBEFFCORR;
        measureMap["BTAGBERRCORR"]=PerformanceResult::BTAGBERRCORR;
        measureMap["BTAGCEFFCORR"]=PerformanceResult::BTAGCEFFCORR;
	measureMap["BTAGCERRCORR"]=PerformanceResult::BTAGCERRCORR;
        measureMap["BTAGLEFFCORR"]=PerformanceResult::BTAGLEFFCORR;
        measureMap["BTAGLERRCORR"]=PerformanceResult::BTAGLERRCORR;
	measureMap["BTAGNBEFFCORR"]=PerformanceResult::BTAGNBEFFCORR;
        measureMap["BTAGNBERRCORR"]=PerformanceResult::BTAGNBERRCORR;
        measureMap["BTAGNBERRCORR"]=PerformanceResult::BTAGNBERRCORR;
        measureMap["MUEFF"]=PerformanceResult::MUEFF;
        measureMap["MUERR"]=PerformanceResult::MUERR;
        measureMap["MUFAKE"]=PerformanceResult::MUFAKE;
        measureMap["MUEFAKE"]=PerformanceResult::MUEFAKE;

	edm::ESHandle<BtagPerformance> perfH_Mistag;
	edm::ESHandle<BtagPerformance> perfH_Btag;
	edm::ESHandle<BtagPerformance> perfH_Mistag_Eff;

	iSetup.get<BTagPerformanceRecord>().get("MISTAGCSVM",perfH_Mistag);
	iSetup.get<BTagPerformanceRecord>().get("BTAGCSVM", perfH_Btag);

	const BtagPerformance & perf_Mistag = *(perfH_Mistag.product());
	const BtagPerformance & perf_Btag = *(perfH_Btag.product());

	edm::Handle<std::vector<pat::Jet > > jetsH;
	iEvent.getByLabel(jetSource_, jetsH);

       	const std::vector<pat::Jet> theJets = *jetsH;

	std::auto_ptr< std::vector<pat::Jet> > jetsBtags( new std::vector<pat::Jet> (*jetsH) );
	
	int runNumber = iEvent.id().run();
	int eventNumber = iEvent.id().event();
	
	//	std::cout<< " runNumber: " << runNumber << " eventNumber: " << eventNumber << std::endl;

	//	std::cout<<" Events " << std::endl;

	BTagSFUtil btaggingUtility( runNumber+eventNumber);
	//	iSetup.get<BTagPerformanceRecord>().get( 
	
	for ( unsigned int i = 0; 
	      i < jetsBtags->size();
	      ++i)
	  {
	    pat::Jet & jet = (*jetsBtags)[i];

            // GET The mistag efficiency and the light and heavy flavour tagging scale factors                                                                
	    double ScaleFactor_heavy;
	    double ScaleFactor_heavy_unc;
	    double tagEfficiency;
	    double ScaleFactor_light;
	    double ScaleFactor_light_unc;
	    double mistagEfficiency;

            BinningPointByMap measurePoint;
            measurePoint.reset();

	    double tempJetPt = jet.et();
	    
	    if ( jet.et() >= 240.0)
		tempJetPt = 239.0;

            measurePoint.insert( BinningVariables::JetEt, tempJetPt);
            measurePoint.insert( BinningVariables::JetAbsEta, fabs( jet.eta() ));

	    ScaleFactor_heavy = (double) perf_Btag.getResult(measureMap["BTAGBEFFCORR"], measurePoint);
	    ScaleFactor_heavy_unc = (double) perf_Btag.getResult(measureMap["BTAGBERRCORR"], measurePoint);
	    tagEfficiency = 0.7;
	    ScaleFactor_light = (double) perf_Mistag.getResult(measureMap["BTAGLEFFCORR"], measurePoint);
	    ScaleFactor_light_unc = (double) perf_Mistag.getResult(measureMap["BTAGLERRCORR"], measurePoint) ;
	    mistagEfficiency  = (double) perf_Mistag.getResult(measureMap["BTAGLEFF"], measurePoint );

	    //	    if ( fabs( jet.eta() ) > 2.4)
	    // {
	    //	std::cout << " jet et: " << jet.et() << " eta: " << jet.eta() << " flavor: " << jet.partonFlavour() << std::endl;
		
	    //	if ( ( abs(jet.partonFlavour()) == 4 ) || ( abs(jet.partonFlavour()) == 5) )
	    //	  {
	    //	    std::cout<< " ScaleFactor_heavy: " << ScaleFactor_heavy << " ScaleFactor_heavy_unc: " << ScaleFactor_heavy_unc
	    //		     << " tagEfficiency: " << tagEfficiency << std::endl;
	    //	  }
	    //	else
	    //	  {
	    //	    std::cout<< " ScaleFactor_light: " << ScaleFactor_light << " ScaleFactor_light_unc: " << ScaleFactor_light_unc
	    //		     << " mistagEfficiency: " << mistagEfficiency << std::endl;
	    //	  }
	    // }

	    bool btag = false;
	    bool btagNominal = false;
	    bool btagUp = false;
	    bool btagDown = false;

	    int parton = 0;

	    if ( jet.bDiscriminator(tagger_.c_str()) >= discriminantValue_ )
	      {
		btag = true;
		btagNominal = true;
		btagUp = true;
		btagDown = true;
	      }

	    parton = jet.partonFlavour();

	    double ScaleFactor_heavy_up = ScaleFactor_heavy;
            double ScaleFactor_heavy_down = ScaleFactor_heavy;

            double ScaleFactor_light_up = ScaleFactor_light;
	    double ScaleFactor_light_down = ScaleFactor_light;

	    if ( abs(parton) == 5 )
	      {
		if ( jet.pt() > 240.0)
		  {
		    ScaleFactor_heavy_up = ScaleFactor_heavy + 0.15*ScaleFactor_heavy;
		    ScaleFactor_heavy_down = ScaleFactor_heavy - 0.15*ScaleFactor_heavy;
		  }
		else 
		  {
		    ScaleFactor_heavy_up = ScaleFactor_heavy + ScaleFactor_heavy_unc;
		    ScaleFactor_heavy_down = ScaleFactor_heavy - ScaleFactor_heavy_unc;
		  }
	      }
	    else if ( abs(parton) == 4 )
	      {
		if ( jet.pt() > 240.0)
                  {
                    ScaleFactor_heavy_up = ScaleFactor_heavy + 0.2*ScaleFactor_heavy;
                    ScaleFactor_heavy_down = ScaleFactor_heavy - 0.2*ScaleFactor_heavy;
                  }
                else
                  {
                    ScaleFactor_heavy_up = ScaleFactor_heavy + 2.0*ScaleFactor_heavy_unc;
                    ScaleFactor_heavy_down = ScaleFactor_heavy - 2.0*ScaleFactor_heavy_unc;
                  }		
	      }
	    else
	      {
		ScaleFactor_light_down = ScaleFactor_light - ScaleFactor_light_unc;		
		ScaleFactor_light_up = ScaleFactor_light + ScaleFactor_light_unc;
	      }

	    //	    if ( fabs( jet.eta() ) > 2.4)
	    // {
	    //	if ( ( abs(parton) == 4 ) || ( abs(parton) == 5) )
	    //	  std::cout << " ScaleFactor_heavy_up: " << ScaleFactor_heavy_up << " ScaleFactor_heavy_down: " << ScaleFactor_heavy_down << std::endl;
	    //	else
	    //	  std::cout << " ScaleFactor_light_up: " << ScaleFactor_light_up << " ScaleFactor_light_down: " << ScaleFactor_light_down << std::endl;
	    // }
	    
	    if ( fabs( ScaleFactor_heavy ) < 2.0)
	      {
		btaggingUtility.modifyBTagsWithSF( btagNominal, parton, ScaleFactor_heavy, tagEfficiency, ScaleFactor_light, mistagEfficiency);
		btaggingUtility.modifyBTagsWithSF( btagUp, parton, ScaleFactor_heavy_up, tagEfficiency, ScaleFactor_light_up, mistagEfficiency);
		btaggingUtility.modifyBTagsWithSF( btagDown, parton, ScaleFactor_heavy_down, tagEfficiency, ScaleFactor_light_down, mistagEfficiency);
	      }

	    int btaggingSummary = 1*btag + 2*btagNominal + 4*btagUp + 8*btagDown;
	    
	    //if ( (btaggingSummary != 0) && ( btaggingSummary != 15 ) )
	    //	    if( ( fabs( jet.eta() ) > 2.4) && (btaggingSummary != 0) && ( btaggingSummary != 15) )
	    // {
	    //	std::cout<< " btag: " << btag << " Nominal: " << btagNominal << " btagUp: " << btagUp << " btagDown: " << btagDown << std::endl;
	    //	std::cout<< "#####################################" << std::endl;
	    //  }

	    jet.addUserInt("btagRegular", btaggingSummary);
	    
	    if ( abs(parton)  == 4  or abs(parton) == 5 )
	      {

		countbs++;
		if ( btag == true )
		  countbs_tagged++;
		if ( btagNominal == true)
		  countbs_modtag++;
	      }
	    else if ( abs(parton) > 0 )
	      {
		//  std::cout << " or here? " << std::endl;
		countNObs++;
		if ( btag == true )
		  count_NObsTagged++;
		if ( btagNominal == true)
		  count_NObsModTag++;	 
	      }

	    //if  ( (btaggingSummary != 0) && ( btaggingSummary != 15) )
            // {
	    //  std::cout << std::endl << " jet : " << i << " et: " << jet.et() << " fabs(eta): "<< fabs( jet.eta() )
            //              << " jet.partonFlavour(): " <<  jet.partonFlavour() << std::endl;
	    //	std::cout << " jet : " << i << " SF_H: " << ScaleFactor_heavy << " SF_L: " << ScaleFactor_light << " +/- " << ScaleFactor_light_unc
	    //             << " mistag Efficiency: " << mistagEfficiency <<  std::endl;
	    //	std::cout << " ScaleFactor_heavy_up: " << ScaleFactor_heavy_up << " ScaleFactor_light_up: " << ScaleFactor_light_up 
	    //		  << " ScaleFactor_heavy_down: " << ScaleFactor_heavy_down << " ScaleFactor_light_down: " << ScaleFactor_light_down << std::endl;
	    //	std::cout<< " jet : " << i << " partonFlavour: " << parton <<  " discriminant: " << btag << " Modified: " << btagNominal 
	    //		 << " modified up: " << btagUp << " modified down: " << btagDown << " total: " << btaggingSummary << std::endl;   
	    // }
	    //	    std::cout<<" modified btagging: " << btaggingSummary << std::endl;
	  }

	// put value map into event
        iEvent.put(jetsBtags);
}

// ------------ method called once each job just before starting event loop  ------------
void
BTaggingSFProducer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void
BTaggingSFProducer::endJob() {
  

}

//define this as a plug-in
DEFINE_FWK_MODULE(BTaggingSFProducer);
