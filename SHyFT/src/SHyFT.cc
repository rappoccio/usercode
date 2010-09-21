#include "Analysis/SHyFT/interface/SHyFT.h"
#include "TVector3.h"
#include "TLorentzVector.h"
#include <sstream>
// #include "/uscmst1/prod/sw/cms/slc5_ia32_gcc434/external/lhapdf/5.6.0/full/include/LHAPDF/LHAPDF.h"
#include "/uscmst1/prod/sw/cms/slc5_ia32_gcc434/external/lhapdf/5.6.0-cms2/share/lhapdf/PDFsets/../../../include/LHAPDF/LHAPDF.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
// namespace LHAPDF {
      
//       void initPDF(int nset);
//       void initPDFSet(int nset, const std::string& filename, int member=0);
//       int numberPDF(int nset);
//       void usePDFMember(int nset, int member);
//       double xfx(int nset, double x, double Q, int fl);
//       double getXmin(int nset, int member);
//       double getXmax(int nset, int member);
//       double getQ2min(int nset, int member);
//       double getQ2max(int nset, int member);
//       void extrapolate(bool extrapolate=true);
// }


using namespace std;


SHyFT::SHyFT(const edm::ParameterSet& iConfig, TFileDirectory& iDir) :
  wPlusJets(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis")),
  theDir(iDir),
  muPlusJets_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<bool>("muPlusJets")),
  ePlusJets_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<bool>("ePlusJets")),
  useHFcat_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<bool>("heavyFlavour")),
  nJetsCut_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<int>("minJets")),  
  sampleNameInput(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<std::string>("sampleName")),
  doMC_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<bool>("doMC") ),
  doBTagPerformance_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<bool>("doBTagPerformance") ),
  plRootFile_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<string>("payload")  ),
  bPerformanceTag_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<string>("bPerformanceTag")  ),
  cPerformanceTag_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<string>("cPerformanceTag")  ),
  lPerformanceTag_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<string>("lPerformanceTag")  ),
  btaggerString_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<std::string>("btaggerString")),
  identifier_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<std::string>("identifier")),
  reweightPDF_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<bool>("reweightPDF")),
  pdfInputTag_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<edm::InputTag>("pdfSrc")),
  pdfToUse_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<std::string>("pdfToUse")),
  pdfVariation_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<int>("pdfVariation")),
  doTagWeight_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<bool>("doTagWeight")),
  bcEffScale_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<double>("bcEffScale")),
  lfEffScale_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<double>("lfEffScale")),
  useDefaultDiscr_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<bool>("useDefaultDiscriminant")),
  bDiscrCut_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<double>("bDiscriminantCut")),
  cDiscrCut_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<double>("cDiscriminantCut")),
  lDiscrCut_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<double>("lDiscriminantCut")),
  useCustomPayload_ (iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<bool>("useCustomPayload")),
  customTagRootFile_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<string>("customPayload")),
  jetAlgo_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<string>("jetAlgo"))
{

  if ( doBTagPerformance_ ) {
    btagPayloadFile_ = boost::shared_ptr<TFile>( new TFile( plRootFile_.c_str(), "READ") );
    es_  = boost::shared_ptr<fwlite::EventSetup>( new fwlite::EventSetup(&*btagPayloadFile_) );
  }

  if ( useCustomPayload_ ) {
    customBtagFile_ = boost::shared_ptr<TFile>( new TFile(customTagRootFile_.c_str(), "READ") );
  }

  //book all the histograms for muons
  if(muPlusJets_) {
    histograms["muPt"]       = theDir.make<TH1F>("muPt",       "Muon p_{T} (GeV/c) ",   100,    0, 200);
    histograms["muEta"]      = theDir.make<TH1F>("muEta",      "Muon eta",               50, -3.0, 3.0);
    histograms["muNhits"]    = theDir.make<TH1F>("muNhits",    "Muon N Hits",            35,    0,  35);
    histograms["muD0"]       = theDir.make<TH1F>("muD0",       "Muon D0",                60, -0.2, 0.2);
    histograms["muChi2"]     = theDir.make<TH1F>("muChi2",     "Muon Chi2",              20,    0,   5);
    histograms["muHCalVeto"] = theDir.make<TH1F>("muHCalVeto", "Muon hCalVeto",          30,    0,  30);
    histograms["muECalVeto"] = theDir.make<TH1F>("muECalVeto", "Muon eCalVeto",          30,    0,  30);
    histograms["muTrackIso"] = theDir.make<TH1F>("muTrackIso", "Muon Track Iso",         30,    0,  30);
    histograms["muECalIso"]  = theDir.make<TH1F>("muECalIso",  "Muon ECal Iso",          30,    0,  30);
    histograms["muHCalIso"]  = theDir.make<TH1F>("muHCalIso",  "Muon HCal Iso",          30,    0,  30);
    histograms["muRelIso"]   = theDir.make<TH1F>("muRelIso",   "Muon Rel Iso",           30,    0,  30);
  }
  
  // book all the histograms for electrons
  if(ePlusJets_) {
    histograms["ePt"]       = theDir.make<TH1F>("ePt",       "Electron p_{T} (GeV/c) ", 100,    0, 200);
    histograms["eEta"]      = theDir.make<TH1F>("eEta",      "Electron eta",             50, -3.0, 3.0);
    histograms["ePhi"]      = theDir.make<TH1F>("ePhi",      "Electron Phi",             50, -3.2, 3.2);
    //  histograms["eNhits"]    = theDir.make<TH1F>("eNhits",    "Electron N Hits",          35,    0,  35);
    histograms["eD0"]       = theDir.make<TH1F>("eD0",       "Electron D0",              60, -0.2, 0.2);
    histograms["eChi2"]     = theDir.make<TH1F>("eChi2",     "Electron Chi2",            20,    0,   5);
    histograms["eTrackIso"] = theDir.make<TH1F>("eTrackIso", "Electron Track Iso",       30,    0,  30);
    histograms["eECalIso"]  = theDir.make<TH1F>("eECalIso",  "Electron ECal Iso",        30,    0,  30);
    histograms["eHCalIso"]  = theDir.make<TH1F>("eHCalIso",  "Electron HCal Iso",        30,    0,  30);
    histograms["eRelIso"]   = theDir.make<TH1F>("eRelIso",   "Electron Rel Iso",         30,    0,  30);
  }
  
  histograms["metPt"]      = theDir.make<TH1F>("metPt", "Missing p_{T} (GeV/c)", 100, 0, 200 );
  histograms2d["massVsPt"] = theDir.make<TH2F>("massVsPt", "Mass vs pt", 25, 0, 250, 25, 0, 500);

  std::vector<std::string> sampleNameBase;
  std::vector<std::string> sampleName;
  std::vector<std::string> secvtxName(5,"_secvtxMass_");
  secvtxName[0]+="1j_"; secvtxName[1]+="2j_"; secvtxName[2]+="3j_"; secvtxName[3]+="4j_"; secvtxName[4]+="5j_";
  
  std::vector<std::string> secvtxEnd;
  if(doMC_) {
    secvtxEnd.push_back("1t_b");  secvtxEnd.push_back("1t_c");  secvtxEnd.push_back("1t_q");
    secvtxEnd.push_back("1t_x");  secvtxEnd.push_back("1t");    secvtxEnd.push_back("2t_bb");
    secvtxEnd.push_back("2t_bc"); secvtxEnd.push_back("2t_bq"); secvtxEnd.push_back("2t_cc");
    secvtxEnd.push_back("2t_cq"); secvtxEnd.push_back("2t_qq"); secvtxEnd.push_back("2t");
    secvtxEnd.push_back("2t_xx");
  }
  else {
    secvtxEnd.push_back("1t"); secvtxEnd.push_back("2t");
  }
  
  if(sampleNameInput=="Vqq" || sampleNameInput=="Wjets" || sampleNameInput=="Wc" || sampleNameInput=="Zjets") {
    stringstream tmpString;
    for(int i=1;i<12;++i) {
      tmpString.str("");
      tmpString << i;
      if(!useHFcat_)
        sampleName.push_back(sampleNameInput+"_path"+tmpString.str());
      if(sampleNameInput != "Zjets")
        sampleName.push_back(sampleNameInput+"W_path"+tmpString.str());
      if(sampleNameInput=="Vqq"  || sampleNameInput == "Zjets") {
        sampleName.push_back(sampleNameInput+"Z_path"+tmpString.str());
      }
    }
  }
  else sampleName.push_back(sampleNameInput);

  histograms["nJets"]         = theDir.make<TH1F>("nJets",    "N Jets, pt>30, eta<2.4",  15,    0,   15);
  for(unsigned int i=1; i<5; ++i) {
    string jtNum = Form("%d",i);
    histograms["jet"+jtNum+"Pt"]   = theDir.make<TH1F>(("jet"+jtNum+"Pt").c_str(),   ("jet "+jtNum+" leading jet pt").c_str(),     150,    0,  300);
    histograms["jet"+jtNum+"Eta"]  = theDir.make<TH1F>(("jet"+jtNum+"Eta").c_str(),  ("jet "+jtNum+" leading jet eta").c_str(),     50, -3.0,  3.0);
    histograms["jet"+jtNum+"Phi"]  = theDir.make<TH1F>(("jet"+jtNum+"Phi").c_str(),  ("jet "+jtNum+" leading jet phi").c_str(),     60, -3.5,  3.5);
    histograms["jet"+jtNum+"Mass"] = theDir.make<TH1F>(("jet"+jtNum+"Mass").c_str(), ("jet "+jtNum+" leading jet mass").c_str(),    50,    0,  150);
    if(doMC_) {
      histograms2d["jet"+jtNum+"PtTrueRes"]      = theDir.make<TH2F>(("jet"+jtNum+"PtTrueRes").c_str(),("jet "+jtNum+" leading jet pt / gen pt").c_str(), 25, -5.0, 5.0, 50, 0, 3);
      histograms2d["jet"+jtNum+"PtTrueResBJets"] = theDir.make<TH2F>(("jet"+jtNum+"PtTrueResBJets").c_str(),("jet "+jtNum+" leading bjet pt / gen pt").c_str(), 25, -5.0, 5.0, 50, 0, 3);
    }
  }
  if(doMC_) {
    histograms["bmass"]         = theDir.make<TH1F>("bmass",    "B Sec Vtx Mass",          40,    0,   10);
    histograms["cmass"]         = theDir.make<TH1F>("cmass",    "C Sec Vtx Mass",          40,    0,   10);
    histograms["lfmass"]        = theDir.make<TH1F>("lfmass",   "LF Sec Vtx Mass",         40,    0,   10);
    histograms["flavorHistory"] = theDir.make<TH1F>("flavorHistory", "Flavor History",     12,    0,   12);
    if ( reweightPDF_ )
      histograms["pdfWeight"] = theDir.make<TH1F>("pdfWeight", "PDF Weight", 50, 0., 2.0);
  }
  histograms["discriminator"] = theDir.make<TH1F>("discriminator", "BTag Discriminator", 30,    2,    8);
  histograms["nVertices"]     = theDir.make<TH1F>("nVertices",     "num sec Vertices",    5,    0,    5);
  histograms["nTags"]         = theDir.make<TH1F>("nTags",     "number of Tags",          3,    0,    3);
  
  //Using btagging and mistag to do normalization
  histograms3d["normalization"]	= theDir.make<TH3F>("normalization",	"Normalization",	5,	1,	6,	2,	1,	3,   11,  0,  11 );
  //Store stat errors
  histograms3d["normalization"]		->  Sumw2();
  
  histograms["m3"] = theDir.make<TH1F>("m3", "M3", 60, 0, 600);
  
  histograms[sampleNameInput+"_hT"]     = theDir.make<TH1F>( (sampleNameInput+"_hT").c_str(),     "HT (sum Jet Et plus mu Pt + MET)", 100, 0, 1200);
  histograms[sampleNameInput+"_hT_Lep"] = theDir.make<TH1F>( (sampleNameInput+"_hT_lep").c_str(), "HT (sum Jet Et plus mu Pt)",       100, 0, 1200);
  histograms[sampleNameInput+"_wMT"]    = theDir.make<TH1F>( (sampleNameInput+"_wMT").c_str(),    "W Transverse Mass, total",          50, 0,  500);
  histograms[sampleNameInput+"_MET"]    = theDir.make<TH1F>( (sampleNameInput+"_MET").c_str(),    "Missing E_{T}, total" ,             50, 0,  200);
  for(unsigned int i=0; i<6; ++i) {
    string jtNum = Form("_%dj",i);
    histograms[sampleNameInput+"_muPt"+jtNum] = theDir.make<TH1F>( (sampleNameInput+"_muPt"+jtNum).c_str(), "muon p_{T}", 100, 0, 200);
    histograms[sampleNameInput+"_muEta"+jtNum] = theDir.make<TH1F>( (sampleNameInput+"_muEta"+jtNum).c_str(), "muon #eta", 60, 0, 2.4);
    histograms[sampleNameInput+"_muPt"+jtNum+"_0t"] = theDir.make<TH1F>( (sampleNameInput+"_muPt"+jtNum+"_0t").c_str(), "muon p_{T}", 100, 0, 200);
    histograms[sampleNameInput+"_muEta"+jtNum+"_0t"] = theDir.make<TH1F>( (sampleNameInput+"_muEta"+jtNum+"_0t").c_str(), "muon #eta", 60, 0, 2.4);
    histograms[sampleNameInput+"_hT"+jtNum]   = theDir.make<TH1F>( (sampleNameInput+"_hT"+jtNum).c_str(), "HT (sum Jet Et + mu Pt + MET)", 50, 0, 1200);
    histograms[sampleNameInput+"_hT"+jtNum+"_0t"]  = theDir.make<TH1F>( (sampleNameInput+"_hT"+jtNum+"_0t").c_str(), "HT (sum Jet Et + mu Pt + MET, 0-Tag)", 50, 0, 1200);
    histograms[sampleNameInput+"_hT_Lep"+jtNum] = theDir.make<TH1F>( (sampleNameInput+"_hT_Lep"+jtNum).c_str(), "HTlep (sum Jet Et + mu Pt)", 50, 0, 1200);
    histograms[sampleNameInput+"_hT_Lep"+jtNum+"_0t"] = theDir.make<TH1F>( (sampleNameInput+"_hT_Lep"+jtNum+"_0t").c_str(), "HTlep (sum Jet Et + mu Pt, 0-Tag)", 50, 0, 1200);
    histograms[sampleNameInput+"_wMT"+jtNum]  = theDir.make<TH1F>( (sampleNameInput+"_wMT"+jtNum).c_str(), "W Trans. Mass, 0 Jets", 25, 0, 500);
    histograms[sampleNameInput+"_wMT"+jtNum+"_0t"] = theDir.make<TH1F>( (sampleNameInput+"_wMT"+jtNum+"_0t").c_str(), "W Trans. Mass, 0 Jets, 0-Tag", 25,0,500);
    histograms[sampleNameInput+"_MET"+jtNum]  = theDir.make<TH1F>( (sampleNameInput+"_MET"+jtNum).c_str(), "Missing E_{T}, 0 Jets", 20, 0, 200);
    histograms[sampleNameInput+"_MET"+jtNum+"_0t"] = theDir.make<TH1F>( (sampleNameInput+"_MET"+jtNum+"_0t").c_str(), "Missing E_{T}, 0 Jets, 0-Tag", 20,0,200);
  }
  for (unsigned int j=0;j<sampleName.size();++j) {
    for(unsigned int k=0;k<secvtxName.size();++k) {
      for(unsigned int l=0;l<secvtxEnd.size();++l) {
        std::string temp = sampleName[j]+secvtxName[k]+secvtxEnd[l];
        histograms[temp] = theDir.make<TH1F>(temp.c_str(), "secvtxmass", 40,    0,   10);
        if(k==0 && l==4) break;
        else if( (!doMC_) && k==0 && l==0) break;
        //std::cout << temp << std::endl;
      }
    }
  }
  
  allNumTags_ = 0;
  allNumJets_ = 0;

  if ( reweightPDF_ ) {
    std::cout << "Initializing pdfs, identifier = " << identifier_ << std::endl;
    // For the first one, MAKE ABSOLUTELY SURE it is the one used to generate
    // your sample. 
    std::cout << "PDF to use = " << pdfToUse_ << std::endl;
    LHAPDF::initPDFSet(pdfToUse_);
    std::cout << "Done initializing pdfs" << std::endl;
  }


  // for closure test
  nExpectedTaggedJets_ = 0.;
  nObservedTaggedJets_ = 0.;
  nExpectedTaggedEvents_ = 0.;
  nObservedTaggedEvents_ = 0.;
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
  double trackIso_ = electron_ ->trackIso();
  double eCalIso_  = electron_ ->ecalIso();
  double hCalIso_  = electron_ ->hcalIso();
  double relIso_   = ( trackIso_ + eCalIso_ + hCalIso_ )/ePt_ ;

  histograms["ePt"      ]->Fill( ePt_        , globalWeight_);
  histograms["eEta"     ]->Fill( eEta_       , globalWeight_);
  histograms["ePhi"     ]->Fill( ePhi_       , globalWeight_);
  histograms["eD0"      ]->Fill( eD0_        , globalWeight_);
  histograms["eTrackIso"]->Fill( trackIso_   , globalWeight_);
  histograms["eECalIso" ]->Fill( eCalIso_    , globalWeight_);
  histograms["eHCalIso" ]->Fill( hCalIso_    , globalWeight_);
  histograms["eRelIso"  ]->Fill( relIso_     , globalWeight_);
  
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
  double muD0_       = globalMuon->dB();
  double norm_chi2_  = globalMuon->normChi2();
  double muHCalVeto_ = globalMuon->isolationR03().hadVetoEt;
  double muECalVeto_ = globalMuon->isolationR03().emVetoEt;
  double trackIso_   = globalMuon->trackIso();
  double eCalIso_    = globalMuon->ecalIso();
  double hCalIso_    = globalMuon->hcalIso();
  double relIso_     = ( trackIso_ + eCalIso_ + hCalIso_ )/muPt_ ;

  histograms["muPt"      ]->Fill( muPt_        , globalWeight_);
  histograms["muEta"     ]->Fill( muEta_       , globalWeight_);
  histograms["muNhits"   ]->Fill( nhits_       , globalWeight_);
  histograms["muD0"      ]->Fill( muD0_        , globalWeight_);
  histograms["muChi2"    ]->Fill( norm_chi2_   , globalWeight_);
  histograms["muHCalVeto"]->Fill( muHCalVeto_  , globalWeight_);
  histograms["muECalVeto"]->Fill( muECalVeto_  , globalWeight_);
  histograms["muTrackIso"]->Fill( trackIso_    , globalWeight_);
  histograms["muECalIso" ]->Fill( eCalIso_     , globalWeight_);
  histograms["muHCalIso" ]->Fill( hCalIso_     , globalWeight_);
  histograms["muRelIso"  ]->Fill( relIso_      , globalWeight_);
  
  return true;
}


// fill the plots for the jets
bool SHyFT::make_templates(const std::vector<reco::ShallowClonePtrCandidate>& jets,
                           const reco::ShallowClonePtrCandidate             & met,
                           const std::vector<reco::ShallowClonePtrCandidate>& muons,
                           const std::vector<reco::ShallowClonePtrCandidate>& electrons)
{
  // std::cout << "Filling global weight in make_templates : " << globalWeight_ << std::endl;
  reco::Candidate::LorentzVector nu_p4 = met.p4();
  reco::Candidate::LorentzVector lep_p4 = ( muPlusJets_  ? muons[0].p4() : electrons[0].p4() );
  double wMT = (lep_p4 + nu_p4).mt();
  double hT = lep_p4.pt() + nu_p4.Et();
  double hT_lep = lep_p4.pt();

  unsigned int maxJets = jets.size();
  unsigned int ibjet = 0;
  if ( (int)maxJets >= nJetsCut_ ) {
    if ( maxJets > 4 ) maxJets = 4;
    for ( unsigned int i=0; i<maxJets; ++i) {
      histograms["jet" + boost::lexical_cast<std::string>(i+1) + "Pt"] ->Fill( jets[i].pt()  , globalWeight_);
      histograms["jet" + boost::lexical_cast<std::string>(i+1) + "Eta"]->Fill( jets[i].eta() , globalWeight_);
      histograms["jet" + boost::lexical_cast<std::string>(i+1) + "Phi"]->Fill( jets[i].phi() , globalWeight_);
      histograms["jet" + boost::lexical_cast<std::string>(i+1) + "Mass"]->Fill( jets[i].mass() , globalWeight_);
      pat::Jet const * patJet = dynamic_cast<pat::Jet const *>( &* jets[i].masterClonePtr()  );
      if ( doMC_ && patJet != 0 && patJet->genJet() != 0 ) {
        histograms2d["jet" + boost::lexical_cast<std::string>(i+1) + "PtTrueRes"] ->Fill( jets[i].eta(), jets[i].pt() / patJet->genJet()->pt() , globalWeight_ );
        if ( abs(patJet->partonFlavour()) == 5 ) {
          ++ibjet;
          histograms2d["jet" + boost::lexical_cast<std::string>(ibjet) + "PtTrueResBJets"] ->Fill( jets[i].eta(), jets[i].pt() / patJet->genJet()->pt(), globalWeight_  );
        }
      }
    }
  } 
  if ( maxJets >= 4 ) {
    //std::cout << iEvent.id().run() << ":" << iEvent.id().event() <<":" << iEvent.id().luminosityBlock() << ":" << std::setprecision(8) << muons[0].pt() << std::endl;
  }
  // std::cout << "jets.size() = " << jets.size() << ", wMT = " << wMT << ", hT = " << hT 
  // 	    << ", maxJets = " << maxJets << std::endl;

  //SecVtxMass and b-tagging related quantities
  int numBottom=0,numCharm=0,numLight=0;
  int numTags=0, numJets=0;
  double vertexMass = -1.0;
  // --------------
  // Fill the M3 if there are more than 3 jets
  // --------------
  reco::Candidate::LorentzVector p4_m3(0,0,0,0);
  if ( jets.size() >= 3 ) {

    // std::vector<TVector3> JetEnergy;
    std::vector<TLorentzVector> jets_p4;
    for (unsigned i=0; i< jets.size(); ++i) {
      // JetEnergy.push_back( TVector3( jets[i].px(), jets[i].py(), jets[i].pz() ) );
      jets_p4.push_back( TLorentzVector( jets[i].px(), jets[i].py(), jets[i].pz(), jets[i].energy() ) );
    }
    
    double M3 = 0.0;
    double highestPt = 0.0;

    for (unsigned int j=0;j<jets.size() - 2;++j) {
      for (unsigned int k=j+1;k<jets.size() - 1;++k) {
        for (unsigned int l = k+1; l<jets.size(); ++l) {
          TLorentzVector threeJets = jets_p4[j] + jets_p4[k] + jets_p4[l];
          if (highestPt < threeJets.Perp()) {
            M3 = threeJets.M();
            highestPt=threeJets.Perp();
          }
        }
      }
    }
    histograms["m3"]->Fill( M3, globalWeight_ );
  }

  // --------------
  // Loop over the jets. Find the flavor of the *highest pt jet* that passes
  // the discriminator cuts. 
  //    Check the parton flavor if MC
  //    Plot pt versus mass 
  //    If there is a SecondaryVertexTagInfo:
  //        plot number of vertices
  //        if there are >= 1 vertex:
  //               fill discriminator
  //               if MC, fill the tag eff.
  //               if discriminator passes cuts (i.e. is tagged):
  //                     fill secondary vertex mass
  //                     if MC, fill template
  bool firstTag = true;
  for ( ShallowCloneCollection::const_iterator jetBegin = jets.begin(),
          jetEnd = jets.end(), jetIter = jetBegin;
        jetIter != jetEnd; ++jetIter)
    {
      const pat::Jet* jet = dynamic_cast<const pat::Jet *>(jetIter->masterClonePtr().get());
      // We first get the flavor of the jet so we can fill look at btag efficiency.
      int jetFlavor = std::abs( jet->partonFlavour() );
      double jetPt  = std::abs( jet->pt() );
      hT += jet->et();
      
      histograms2d["massVsPt"]->Fill( jetPt, jet->mass(), globalWeight_ );

      //Here we determine what kind of flavor we have in this jet	
      if( doMC_ ) {
        switch (jetFlavor)
          {
          case 5:
            // bottom
            ++numBottom;
            break;
          case 4:
            // charm
            ++numCharm;
            break;
          default:
            // light flavour
            ++numLight;
          }
      }

      // Get the secondary vertex tag info
      reco::SecondaryVertexTagInfo const * svTagInfos
        = jet->tagInfoSecondaryVertex("secondaryVertex");
      if ( svTagInfos == 0 ) continue;
      histograms["nVertices"]-> Fill( svTagInfos->nVertices(), globalWeight_ );
      
      // Check to make sure we have a vertex
      if ( svTagInfos->nVertices() <= 0 )  continue;
      
      // This discriminator is only filled when we have a secondary vertex
      // tag info and a vertex in it
      histograms["discriminator"]-> Fill ( jet->bDiscriminator(btaggerString_), globalWeight_ );

      // std::cout << "Jet " << jetIter - jetBegin << ", pt = " << jet->pt() << std::endl;
      // typedef std::pair<std::string,float> sfpair;
      // typedef std::vector<sfpair> sfpair_coll;
      // sfpair_coll const & discs = jet->getPairDiscri();
      // for ( sfpair_coll::const_iterator ipairBegin = discs.begin(),
      // 	      ipairEnd = discs.end(), ipair = ipairBegin;
      // 	    ipair != ipairEnd; ++ipair ) {
      // 	std::cout << " disc : " << ipair->first << " = " << ipair->second << std::endl;
      // }

      // Check to see if the actual jet is tagged
      if( jet->bDiscriminator(btaggerString_) < btagOP_ ) continue;
      //      ++numTags;

      // Take the template info from the first tag (ordered by jet pt)
      if ( firstTag ) {
        vertexMass = svTagInfos->secondaryVertex(0).p4().mass();
        
        //Here we determine what kind of flavor we have in this jet	
        if( doMC_ ) {
          switch (jetFlavor)
            {
            case 5:
              // bottom
              histograms["bmass"]->Fill(vertexMass, globalWeight_);
              break;
            case 4:
              // charm
              histograms["cmass"]->Fill(vertexMass, globalWeight_);
              break;
            default:
              // light flavour
              histograms["lfmass"]->Fill(vertexMass, globalWeight_);
            }
        }
        firstTag = false;
      }// end if first tag
    }// end loop over jets

  if(numBottom>2) numBottom=2;
  if(numCharm>2 ) numCharm =2;
  if(numLight>2 ) numLight =2;
  
  // For now, we only care if we have 2 tags...any more are treated the same - maybe we should look at 3 tags?
  numTags = std::min( allNumTags_, 2 );
  numJets = std::min( allNumJets_, 5 );

  if(!doTagWeight_)
    histograms["nTags"]->Fill(numTags, globalWeight_);
  else {
    histograms["nTags"]->Fill((double)0,globalWeight_0t);
    histograms["nTags"]->Fill((double)1,globalWeight_1t);
    histograms["nTags"]->Fill((double)2,globalWeight_2t);
  }

  histograms[sampleNameInput + Form("_hT")    ]->Fill( hT,       globalWeight_ );
  histograms[sampleNameInput + Form("_hT_Lep")]->Fill( hT_lep,   globalWeight_ );
  histograms[sampleNameInput + Form("_wMT")   ]->Fill( wMT,      globalWeight_ );
  histograms[sampleNameInput + Form("_MET")   ]->Fill( met.pt(), globalWeight_ );

  // Now, if we have jets, fill 0, 1, and >=2 tag histograms.
  // The 0-tag histograms are hT, met, and mT_w.
  // The 1-tag and >=2-tag histogram is the secondary vertex mass
  // of the highest pt tagged jet.

  histograms[sampleNameInput + Form("_muPt_%dj",   numJets)]->Fill( muons[0].pt(),        globalWeight_ );
  histograms[sampleNameInput + Form("_muEta_%dj",  numJets)]->Fill( fabs(muons[0].eta()), globalWeight_ );
  histograms[sampleNameInput + Form("_hT_%dj",     numJets)]->Fill( hT,                   globalWeight_ );
  histograms[sampleNameInput + Form("_hT_Lep_%dj", numJets)]->Fill( hT_lep,               globalWeight_ );
  histograms[sampleNameInput + Form("_wMT_%dj",    numJets)]->Fill( wMT,                  globalWeight_ );
  histograms[sampleNameInput + Form("_MET_%dj",    numJets)]->Fill( met.pt(),             globalWeight_ );

  if ( numJets > 0 ) {    
    if ( numTags == 0 || doTagWeight_ ) {
      histograms[sampleNameInput + Form("_muPt_%dj_0t",   numJets)]->Fill( muons[0].pt(),        globalWeight_0t );
      histograms[sampleNameInput + Form("_muEta_%dj_0t",  numJets)]->Fill( fabs(muons[0].eta()), globalWeight_0t );
      histograms[sampleNameInput + Form("_hT_%dj_0t",     numJets)]->Fill( hT,                   globalWeight_0t );
      histograms[sampleNameInput + Form("_hT_Lep_%dj_0t", numJets)]->Fill( hT_lep,               globalWeight_0t );
      histograms[sampleNameInput + Form("_wMT_%dj_0t",    numJets)]->Fill( wMT,                  globalWeight_0t );
      histograms[sampleNameInput + Form("_MET_%dj_0t",    numJets)]->Fill( met.pt(),             globalWeight_0t );
    }
    if( numTags > 0 || doTagWeight_) {
      string massName  = secvtxname + Form("_secvtxMass_%dj_%dt", numJets, numTags);
      string massName1 = secvtxname + Form("_secvtxMass_%dj_1t",  numJets);
      string massName2 = secvtxname + Form("_secvtxMass_%dj_2t",  numJets);
      
      string whichtag = "";
      if( doMC_ ) {
        if( !doTagWeight_ ) {
          if (1 == numTags) {
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
          histograms[massName             ]-> Fill (vertexMass, globalWeight_);
          histograms[massName + whichtag  ]-> Fill (vertexMass, globalWeight_);
        } // if not doTagWeight
        else {
          if (numBottom>0) {
            histograms[massName1 + "_b"   ]-> Fill (vertexMass, globalWeight_1t);
            if (2==numBottom)
              histograms[massName2 + "_bb"]-> Fill (vertexMass, globalWeight_2t);
            else if (numBottom && numCharm ) 
              histograms[massName2 + "_bc"]-> Fill (vertexMass, globalWeight_2t);
            else if (numBottom && numLight )
              histograms[massName2 + "_bq"]-> Fill (vertexMass, globalWeight_2t);
          }
          else if (numCharm>0) {
            histograms[massName1 + "_c"   ]-> Fill (vertexMass, globalWeight_1t);
            if (2==numCharm)
              histograms[massName2 + "_cc"]-> Fill (vertexMass, globalWeight_2t);
            else if (numCharm && numLight)
              histograms[massName2 + "_cq"]-> Fill (vertexMass, globalWeight_2t);
          }
          else if (numLight>0) {
            histograms[massName1 + "_q"   ]-> Fill (vertexMass, globalWeight_1t);
            if (2==numLight)
              histograms[massName2 + "_qq"]-> Fill (vertexMass, globalWeight_2t);
          }
          else {
            histograms[massName1 + "_x"   ]-> Fill (vertexMass, globalWeight_1t);
            histograms[massName2 + "_xx"  ]-> Fill (vertexMass, globalWeight_2t);
          }
          histograms[massName1            ]-> Fill (vertexMass, globalWeight_1t);
          if (numJets>1)
            histograms[massName2          ]-> Fill (vertexMass, globalWeight_2t);
        } // end else (== if dotagweight)
      } // end if doMC
      else
        histograms[massName               ]-> Fill (vertexMass, globalWeight_);
    } // end if numTags > 0
  } // end if numJets > 0 
  // This is the 0-jet bin
  if(numJets==0) {
    histograms[sampleNameInput + Form("_muPt_0j_0t")  ]->Fill( muons[0].pt(),        globalWeight_ );
    histograms[sampleNameInput + Form("_muEta_0j_0t") ]->Fill( fabs(muons[0].eta()), globalWeight_ );
    histograms[sampleNameInput + Form("_hT_0j_0t")    ]->Fill( hT ,                  globalWeight_ );
    histograms[sampleNameInput + Form("_hT_Lep_0j_0t")]->Fill( hT_lep ,              globalWeight_ );
    histograms[sampleNameInput + Form("_wMT_0j_0t")   ]->Fill( wMT ,                 globalWeight_ );
    histograms[sampleNameInput + Form("_MET_0j_0t")   ]->Fill( met.pt() ,            globalWeight_ );
  }
  return true;
}

bool SHyFT::analyze_met(const reco::ShallowClonePtrCandidate & met)
{
  histograms["metPt"]->Fill( met.pt(), globalWeight_ );
  return true;
}

///////////////////
/// The event loop
//////////////////
void SHyFT::analyze(const edm::EventBase& iEvent)
{
  globalWeight_ = 1.0;

  pat::strbitset ret = wPlusJets.getBitTemplate();
  
  bool passed = wPlusJets(iEvent, ret);
  std::vector<reco::ShallowClonePtrCandidate> const & electrons = wPlusJets.selectedElectrons();
  std::vector<reco::ShallowClonePtrCandidate> const & muons     = wPlusJets.selectedMuons();
  std::vector<reco::ShallowClonePtrCandidate> const & jets      = wPlusJets.cleanedJets();
  reco::ShallowClonePtrCandidate const & met = wPlusJets.selectedMET();

  //Check if the BTagPerformanceRecord exists
  if ( doBTagPerformance_ ) {
    recId_ = es_->recordID("BTagPerformanceRecord");
    es_->syncTo( iEvent.id(), edm::Timestamp());
  }
  
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
  bit_ = "Cosmic Veto";
  bool passPre = ret[bit_];
  bool anyJets = jet1 || jet2 || jet3 || jet4 || jet5;
  
  // if not passed trigger, next event
  if ( !passTrigger )  return;
  
  if (doMC_ && reweightPDF_) {
    weightPDF(iEvent);
  }

  if ( doBTagPerformance_ ) {
    calcTagWeight(jets);
  }
  
  if(useHFcat_) {
    edm::Handle< unsigned int > heavyFlavorCategory;
    iEvent.getByLabel ( edm::InputTag("flavorHistoryFilter"),heavyFlavorCategory);
    assert ( heavyFlavorCategory.isValid() );
    if ( useHFcat_ ) histograms["flavorHistory"]-> Fill ( *heavyFlavorCategory, globalWeight_ );
  }

  secvtxname = sampleNameInput;
  //find the sample name
  if(!calcSampleName(iEvent, secvtxname) ) {
    throw cms::Exception("InvalidLogic") << " Calculating sample name broke on me... I'm outta here" << std::endl;
  }
  
  if (passPre) 
    {
      histograms["nJets"]->Fill( jets.size(), globalWeight_ );
  
      make_templates(jets, met, muons, electrons);
      analyze_met( met );
      if ( muPlusJets_ ) analyze_muons(muons);
      if ( ePlusJets_ ) analyze_electrons(electrons);          

      if ( !doMC_) {
        summary_.push_back( SHyFTSummary(iEvent.id().run(),
                                         iEvent.id().luminosityBlock(),
                                         iEvent.id().event(),
                                         allNumJets_,
                                         allNumTags_
                                         ) );
      }    
    }
}
  
void SHyFT::calcTagWeight(const std::vector<reco::ShallowClonePtrCandidate>& jets)
{
  allNumTags_ = 0;
  allNumJets_ = (int) jets.size();

  double weight0t = 0;
  double weight1t = 0;
  double weight2t = 0;

  //Get Payload and Working Point
  fwlite::ESHandle< PerformancePayload >   plBHandle;
  fwlite::ESHandle< PerformancePayload >   plLHandle;
  fwlite::ESHandle< PerformancePayload >   plCHandle;
  fwlite::ESHandle< PerformanceWorkingPoint >   wpBHandle;
  fwlite::ESHandle< PerformanceWorkingPoint >   wpLHandle;
  fwlite::ESHandle< PerformanceWorkingPoint >   wpCHandle;
  if ( es_ != 0 ) {
    es_->get(recId_).get(plBHandle, bPerformanceTag_.c_str() );
    es_->get(recId_).get(wpBHandle, bPerformanceTag_.c_str() );
    es_->get(recId_).get(plCHandle, cPerformanceTag_.c_str() );
    es_->get(recId_).get(wpCHandle, cPerformanceTag_.c_str() );
    es_->get(recId_).get(plLHandle, lPerformanceTag_.c_str() );
    es_->get(recId_).get(wpLHandle, lPerformanceTag_.c_str() );
  }
  if( !(plBHandle.isValid() && wpBHandle.isValid() ) )
    std::cout<<"BEff BtagPerformance is not valid !!"<<std::endl;
  if( !(plLHandle.isValid() && wpLHandle.isValid() ) )
    std::cout<<"LEff BtagPerformance is not valid !!"<<std::endl;
  if( !(plCHandle.isValid() && wpCHandle.isValid() ) )
    std::cout<<"CEff BtagPerformance is not valid !!"<<std::endl;
  
  BtagPerformance  perfB( *plBHandle, *wpBHandle );
  BtagPerformance  perfL( *plLHandle, *wpLHandle );
  BtagPerformance  perfC( *plCHandle, *wpCHandle );

  TH2F * eff_b=0;
  TH2F * eff_c=0;
  TH2F * eff_lf=0;
  
  if(useCustomPayload_) {
    eff_b  = (TH2F*)customBtagFile_->Get((jetAlgo_+"BEff").c_str());
    eff_c  = (TH2F*)customBtagFile_->Get((jetAlgo_+"CEff").c_str());
    eff_lf = (TH2F*)customBtagFile_->Get((jetAlgo_+"LFEff").c_str());
  }

  btagOP_ = perfB.workingPoint().cut();
  // Now get the normalization of the tag bins from the BVTX POG efficiency
  //Normalization for "1 tag" events
  for ( ShallowCloneCollection::const_iterator jetBegin = jets.begin(),
          jetEnd = jets.end(), jetIter = jetBegin;
      jetIter != jetEnd; ++jetIter)
    {
      const pat::Jet* jet = dynamic_cast<const pat::Jet *>(jetIter->masterClonePtr().get());

      // We first get the flavor of the jet so we can fill look at btag efficiency.
      int jetFlavor = std::abs( jet->partonFlavour() );
      if(!useDefaultDiscr_) {
        if(jetFlavor==5 && bDiscrCut_!=-1)
          btagOP_ = bDiscrCut_;
        else if(jetFlavor==4 && cDiscrCut_!=-1)
          btagOP_ = cDiscrCut_;
        else if(jetFlavor!=4 && jetFlavor!=5 && lDiscrCut_!=-1)
          btagOP_ = lDiscrCut_;
      }

      // We need to check out how many tags we have, so we know how to classify this event
      // Get the secondary vertex tag info
      reco::SecondaryVertexTagInfo const * svTagInfos
        = jet->tagInfoSecondaryVertex("secondaryVertex");
      if ( svTagInfos != 0 ) {
        // Check to make sure we have a vertex
        if ( svTagInfos->nVertices() > 0 ) {
          // Check to see if the actual jet is tagged
          if( jet->bDiscriminator(btaggerString_) > btagOP_ ) {
	    nObservedTaggedJets_ += 1.0;
            ++allNumTags_;
          }
        }
      }
    
      if( doMC_ ) {
        
        double jetPt = jet->pt();
        //jetPt range from BTag POG, [30, 400]
        if( jetPt < 30 )    jetPt = 30.5;
        if( jetPt > 400 )	  jetPt = 399.5;
        double jetEta = jet->eta();
        //jetEta range from BTag POG, [-3.0, 3.0]
        if( jetEta < -3.0 )	jetEta = -2.99;
        if( jetEta > 3.0 )	jetEta = 2.99;

        double bEff = 0;
        double cEff = 0;
        double lEff = 0;
        
        if(useCustomPayload_) {
	  if ( eff_b == 0 || eff_c == 0 || eff_lf == 0 ) {
	    throw cms::Exception("InvalidEfficiencyFile") <<
	      "The efficiencies from the custom payload are not valid" << std::endl;
	  }
          if ( jetPt > 300 ) jetPt = 299.0;
          jetEta = std::abs(jetEta);
          
          int ibin_b  = eff_b ->GetXaxis()->FindBin( jetPt );
          int jbin_b  = eff_b ->GetYaxis()->FindBin( jetEta );
          int ibin_c  = eff_c ->GetXaxis()->FindBin( jetPt );
          int jbin_c  = eff_c ->GetYaxis()->FindBin( jetEta );
          int ibin_lf = eff_lf->GetXaxis()->FindBin( jetPt );
          int jbin_lf = eff_lf->GetYaxis()->FindBin( jetEta );

          bEff = eff_b ->GetBinContent(ibin_b,  jbin_b)  * bcEffScale_;
          cEff = eff_c ->GetBinContent(ibin_c,  jbin_c)  * bcEffScale_;
          lEff = eff_lf->GetBinContent(ibin_lf, jbin_lf) * lfEffScale_;
        }
        else {
          BinningPointByMap p;
          p.insert( BinningVariables::JetEt,  jetPt );
          p.insert( BinningVariables::JetEta, jetEta );
          p.insert( BinningVariables::JetAbsEta,  abs(jetEta) );
          
          //btag scale factor and mistag rate
          if( !perfB.isResultOk( PerformanceResult::BTAGBEFF, p )  )
            std::cout<<"No reasonable result for b effi !"<<std::endl;
          if( !perfC.isResultOk( PerformanceResult::BTAGCEFF, p )  )
            std::cout<<"No reasonable result for c effi !"<<std::endl;
          if( !perfL.isResultOk( PerformanceResult::BTAGLEFF, p )  )
            std::cout<<"No reasonable result for lf effi !"<<std::endl;
          
          bEff = perfB.getResult( PerformanceResult::BTAGBEFF, p ) * bcEffScale_;
          cEff = perfC.getResult( PerformanceResult::BTAGCEFF, p ) * bcEffScale_;
          lEff = perfL.getResult( PerformanceResult::BTAGLEFF, p ) * lfEffScale_;
        }
        
        //Probability to tag this jet
        double weight = 1.0;
        int whichtag = 0;
        switch( jetFlavor )
          {
          case 5:
            whichtag = 5;
            weight *= bEff;
            break;
          case 4:
            whichtag = 4;
            weight *= cEff;
            break;
          default:
            whichtag = 0;
            weight *= lEff;
          }
        //Probability to untag the rest jets
        double untagRate = 1.0;
        for( ShallowCloneCollection::const_iterator jet2Iter = jetBegin;  jet2Iter != jetEnd; ++jet2Iter )
          {
            const pat::Jet* jet2 = dynamic_cast<const pat::Jet *>(jet2Iter->masterClonePtr().get());
            if( jet2Iter != jetIter )
              {
                int jetFlavor2 = std::abs( jet2->partonFlavour() );
                double jetPt2	= jet2->pt();
                //jetPt range from BTag POG, [30, 400]
                if( jetPt2 < 30 )	jetPt2 = 30.5;
                if( jetPt2 > 400 )   jetPt2 = 399.5;
                double jetEta2	= jet2->eta();
                //jetEta range from BTag POG, [-3.0, 3.0]
                if( jetEta2 < -3.0 )	jetEta2 = -2.99;
                if( jetEta2 > 3.0 )		jetEta2 = 2.99;

                if(useCustomPayload_) {
		  if ( eff_b == 0 || eff_c == 0 || eff_lf == 0 ) {
		    throw cms::Exception("InvalidEfficiencyFile") <<
		      "The efficiencies from the custom payload are not valid" << std::endl;
		  }
                  if ( jetPt2 > 300 ) jetPt2 = 299.0;
                  jetEta2 = std::abs(jetEta2);
                  int i2bin_b  = eff_b ->GetXaxis()->FindBin( jetPt2 );
                  int j2bin_b  = eff_b ->GetYaxis()->FindBin( jetEta2 );
                  int i2bin_c  = eff_c ->GetXaxis()->FindBin( jetPt2 );
                  int j2bin_c  = eff_c ->GetYaxis()->FindBin( jetEta2 );
                  int i2bin_lf = eff_lf->GetXaxis()->FindBin( jetPt2 );
                  int j2bin_lf = eff_lf->GetYaxis()->FindBin( jetEta2 );
                  
                  if      ( jetFlavor2==5 ) 
                    untagRate *= 1 - ( eff_b ->GetBinContent(i2bin_b,  j2bin_b)  * bcEffScale_ );
                  else if ( jetFlavor2==4 )
                    untagRate *= 1 - ( eff_c ->GetBinContent(i2bin_c,  j2bin_c)  * bcEffScale_ );
                  else 
                    untagRate *= 1 - ( eff_lf->GetBinContent(i2bin_lf, j2bin_lf) * lfEffScale_ );

                }
                else {
                  BinningPointByMap p2;
                  p2.insert( BinningVariables::JetEt,  jetPt2 );
                  p2.insert( BinningVariables::JetEta, jetEta2 );
                  p2.insert( BinningVariables::JetAbsEta,  abs(jetEta2) );
                  
                  switch( jetFlavor2 )
                    {
                    case 5:
                      if( !perfB.isResultOk( PerformanceResult::BTAGBEFF, p2 )  )
                        std::cout<<"No reasonable result for b effi !"<<std::endl;
                      untagRate *= (1.-perfB.getResult( PerformanceResult::BTAGBEFF, p2 ) * bcEffScale_ );
                      break;
                    case 4:
                      if( !perfC.isResultOk( PerformanceResult::BTAGCEFF, p2 )  )
                        std::cout<<"No reasonable result for c effi !"<<std::endl;
                      untagRate *= (1.-perfC.getResult( PerformanceResult::BTAGCEFF, p2 ) * bcEffScale_  );
                      break;
                    default:
                      if( !perfL.isResultOk( PerformanceResult::BTAGLEFF, p2 )  )
                        std::cout<<"No reasonable result for lf effi !"<<std::endl;
                      untagRate *= (1.-perfL.getResult( PerformanceResult::BTAGLEFF, p2 ) * lfEffScale_ );
                    }
                }
              } // end if jet1Iter != jet2Iter
          } // end for jet2Iter
        weight1t += weight*untagRate;
        if(jetIter==jetBegin)
          weight0t = (1-weight)*untagRate;
        else if (std::abs(weight0t - (1.0-weight)*untagRate) > 0.0001)
          cout << "Error with weight: weight0t = " << weight0t << " , 1-weight = " << 1.0-weight << " , untagRate = " << untagRate
               << " , new weight0t = " << (1.0-weight)*untagRate << " , njets = " << allNumJets_ << " , nTags = " << allNumTags_ << endl;
          histograms3d["normalization"]->Fill(  allNumJets_,	1,	whichtag,	weight*untagRate );
      } // end if doMC
    } // end for jetIter

  if (doTagWeight_) {
    if(weight0t>=1) {
      cout << "Weight 0t >=1 : " << weight0t << ", weight1t = " << weight1t << ", weight2t = " << weight2t << endl;
      weight0t=1;
      weight1t=0;
      weight2t=0;
    }
    else if(weight1t>=1) {
      cout << "Weight 1t >=1 : " << weight1t << ", weight0t = " << weight0t << ", weight2t = " << weight2t << endl;
      weight1t=1;
      weight0t=0;
      weight2t=0;
    }
    else
      weight2t = 1-weight0t-weight1t;
    
    if(allNumJets_==0) {
      weight0t=1;
      weight1t=0;
      weight2t=0;
    }

    globalWeight_0t = globalWeight_*weight0t;
    globalWeight_1t = globalWeight_*weight1t;
    globalWeight_2t = globalWeight_*weight2t;
    /*    cout << "njets,ntags = " << allNumJets_ << "," << allNumTags_ << " "
          << "weights:0,1,2 = " << globalWeight_0t << "," << globalWeight_1t << "," << globalWeight_2t << std::endl;*/
  }
  else {
    globalWeight_2t = globalWeight_;
    globalWeight_1t = globalWeight_;
    globalWeight_0t = globalWeight_;
  }

  // perform closure test...
  // If there are at least 1 tagged jets, increment the number of observed >=1 tag events.
  // Always fill the number of expected tagged events with the weights estimated. 
  if ( allNumTags_ > 0 )
    nObservedTaggedEvents_ += 1.0;
  nExpectedTaggedEvents_ += (1.0 - globalWeight_0t);
}


bool SHyFT::calcSampleName (const edm::EventBase& iEvent, std::string &sampleName)
{
  // Get the heavy flavor category - we first want to make sure we have flavorHistory
  if(useHFcat_) {
    edm::Handle< unsigned int > heavyFlavorCategory;
    iEvent.getByLabel ( edm::InputTag("flavorHistoryFilter"),heavyFlavorCategory);
    assert ( heavyFlavorCategory.isValid() );
    HFcat_ = (*heavyFlavorCategory);
	// For Vqq, we don't know if it is a W, a Z, or neither
    edm::Handle< vector< reco::GenParticle > > genParticleCollection;
	iEvent.getByLabel (edm::InputTag("prunedGenParticles"),genParticleCollection);
	assert ( genParticleCollection.isValid() );
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
	  }
    // from:
    // https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideFlavorHistory
    //  1. W+bb with >= 2 jets from the ME (dr > 0.5)
    //  2. W+b or W+bb with 1 jet from the ME
    //  3. W+cc from the ME (dr > 0.5)
    //  4. W+c or W+cc with 1 jet from the ME
    //  5. W+bb with 1 jet from the part[on shower (dr == 0.0)
    //  6. W+cc with 1 jet from the parton shower (dr == 0.0)
    //  7. W+bb with >= 2 partons but 1 jet from the ME (dr == 0.0)
    //  8. W+cc with >= 2 partons but 1 jet from the ME (dr == 0.0)
    //  9. W+bb with >= 2 partons but 2 jets from the PS (dr > 0.5)
    // 10. W+cc with >= 2 partons but 2 jets from the PS (dr > 0.5)
    // 11. Veto of all the previous (W+ light jets)
    sampleName+="_path";
    stringstream tmpString;
    tmpString.str("");
    tmpString << *heavyFlavorCategory;
    sampleName+=tmpString.str();
    return true;
  }
  return true;
}

void SHyFT::endJob()
{

  std::cout << "----------------------------------------------------------------------------------------" << std::endl;
  std::cout << "      So long, and thanks for all the fish..." << std::endl;
  std::cout << "                 -- " << identifier_ << std::endl;
  std::cout << "----------------------------------------------------------------------------------------" << std::endl;
  wPlusJets.print(std::cout);
  wPlusJets.printSelectors(std::cout);
  if ( !doMC_ ) {
    sort(summary_.begin(), summary_.end());
    std::cout << "** Start " << identifier_ << " **" << std::endl;
    copy(summary_.begin(), summary_.end(), std::ostream_iterator<SHyFTSummary>(std::cout, "\n"));  
    std::cout << "** End **" << std::endl;
  }
  std::cout << "  Btagging closure test: " << std::endl;
  std::cout << "  N_exp_>=1     : " << nExpectedTaggedEvents_ << std::endl;
  std::cout << "  N_obs_>=1     : " << nObservedTaggedEvents_ << std::endl;
  std::cout << "  N_obs jettags : " << nObservedTaggedJets_ << std::endl;
}


void SHyFT::weightPDF(  edm::EventBase const & iEvent) 
{
  // 
  // NOTA BENE!!!!
  //
  //     The values "pdf1" and "pdf2" below are *wrong* for madgraph or alpgen samples.
  //     They must be taken from the "zeroth" PDF in the PDF set, assuming that is set
    
  double iWeightSum = 0.0;
  unsigned int nWeightSum = 0;
  edm::Handle<GenEventInfoProduct> pdfstuff;
  iEvent.getByLabel(pdfInputTag_, pdfstuff);
       
  float Q = pdfstuff->pdf()->scalePDF;
  int id1 = pdfstuff->pdf()->id.first;
  double x1 = pdfstuff->pdf()->x.first;
  int id2 = pdfstuff->pdf()->id.second;
  double x2 = pdfstuff->pdf()->x.second;

  // BROKEN for Madgraph productions:
  double pdf1 = pdfstuff->pdf()->xPDF.first;
  double pdf2 = pdfstuff->pdf()->xPDF.second;  

  // char buff[1000];
  // sprintf(buff, "Q = %6.2f, id1 = %4d, id2 = %4d, x1 = %6.2f, x2 = %6.2f, pdf1 = %6.2f, pdf2 = %6.2f",
  // 	    Q, id1, id2, x1, x2, pdf1, pdf2
  // 	    );
  // std::cout << buff << std::endl;


  if ( pdfVariation_ != 0 ) {
    // Here is where we check the varied systematic PDF's
    unsigned int nweights = 1;
    unsigned int neigen = 0;
    if (LHAPDF::numberPDF()>1) {
      nweights += LHAPDF::numberPDF();
      neigen = nweights / 2;
    }

    for (unsigned int i=0; i<neigen; ++i) {
      int toGrab = 2*i;
      if ( pdfVariation_ < 0 )
	toGrab = 2*i+1;
      LHAPDF::usePDFMember(toGrab);
      double newpdf1 = LHAPDF::xfx(x1, Q, id1)/x1;
      double newpdf2 = LHAPDF::xfx(x2, Q, id2)/x2;
      double prod =  (newpdf1/pdf1*newpdf2/pdf2);
      iWeightSum += prod*prod;
      ++nWeightSum;
      // sprintf(buff, "         pdf1 = %6.2f, pdf2 = %6.2f, prod=%6.2f",
      // 	newpdf1, newpdf2, prod
      // 	);
      // std::cout << buff << std::endl;
    }
  } else {
    // Here is where we normalize to the central value (0th PDF)
    LHAPDF::usePDFMember(0);
    double newpdf1 = LHAPDF::xfx(x1, Q, id1)/x1;
    double newpdf2 = LHAPDF::xfx(x2, Q, id2)/x2;
    double prod =  (newpdf1/pdf1*newpdf2/pdf2);
    iWeightSum += prod*prod;
    ++nWeightSum;
    // sprintf(buff, "         pdf1 = %6.2f, pdf2 = %6.2f, prod=%6.2f",
    // 	      newpdf1, newpdf2, prod
    // 	      );
    // std::cout << buff << std::endl;    
  }
    
  if (nWeightSum > 0 )
    iWeightSum = TMath::Sqrt(iWeightSum) / TMath::Sqrt((double)nWeightSum) ;
  else 
    iWeightSum = 1.0;

    
  globalWeight_ *= iWeightSum ;
  // std::cout << "Global weight = " << globalWeight_ << std::endl;
  histograms["pdfWeight"]->Fill( globalWeight_ );

}
