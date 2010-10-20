#include "Analysis/SHyFT/interface/SHyFT.h"
#include "TVector3.h"
#include "TLorentzVector.h"
#include <sstream>
#include "TRandom.h"
#include "Analysis/SHyFT/interface/combinatorics.h"
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
  identifier_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<std::string>("identifier")),
  reweightPDF_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<bool>("reweightPDF")),
  reweightBTagEff_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<bool>("reweightBTagEff")),
  pdfInputTag_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<edm::InputTag>("pdfSrc")),
  pdfToUse_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<std::string>("pdfToUse")),
  pdfEigenToUse_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<int>("pdfEigenToUse")),
  pdfVariation_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<int>("pdfVariation")),
  btaggerString_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<std::string>("btaggerString")),
  bcEffScale_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<double>("bcEffScale")),
  lfEffScale_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<double>("lfEffScale")),
  allDiscrCut_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<double>("allDiscriminantCut")),
  bDiscrCut_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<double>("bDiscriminantCut")),
  cDiscrCut_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<double>("cDiscriminantCut")),
  lDiscrCut_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<double>("lDiscriminantCut")),
  useCustomPayload_ (iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<bool>("useCustomPayload")),
  customTagRootFile_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<string>("customPayload")),
  simpleSFCalc_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<bool>("simpleSFCalc")),
  jetAlgo_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<string>("jetAlgo"))
{

  if ( simpleSFCalc_) 
    gRandom->SetSeed( 960622508 );
  

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

  sampleHistName_ = "";
  std::vector<std::string> sampleNameBase;
  std::vector<std::string> sampleName;
  std::vector<std::string> secvtxName(5,"_secvtxMass_");
  secvtxName[0]+="1j_"; secvtxName[1]+="2j_"; secvtxName[2]+="3j_"; secvtxName[3]+="4j_"; secvtxName[4]+="5j_";

  std::vector<std::string> hTName(6,"_hT_");
  hTName[0]+="0j";hTName[1]+="1j"; hTName[2]+="2j"; hTName[3]+="3j"; hTName[4]+="4j"; hTName[5]+="5j";

  std::vector<std::string> METName(6,"_MET_");
  METName[0]+="0j";METName[1]+="1j"; METName[2]+="2j"; METName[3]+="3j"; METName[4]+="4j"; METName[5]+="5j";

  std::vector<std::string> muEtaName(6,"_muEta_");
  muEtaName[0]+="0j";muEtaName[1]+="1j"; muEtaName[2]+="2j"; muEtaName[3]+="3j"; muEtaName[4]+="4j"; muEtaName[5]+="5j";

  
  std::vector<std::string> secvtxEnd;
  if(doMC_) {
    secvtxEnd.push_back("1t_b");  
    secvtxEnd.push_back("1t_c");  
    secvtxEnd.push_back("1t_q");
    secvtxEnd.push_back("1t_x");  
    secvtxEnd.push_back("1t");
    secvtxEnd.push_back("2t_b");  
    secvtxEnd.push_back("2t_c"); 
    secvtxEnd.push_back("2t_q");
    secvtxEnd.push_back("2t_x");
    secvtxEnd.push_back("2t");
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
  
  histograms[sampleNameInput+"_hT"]     = theDir.make<TH1F>( (sampleNameInput+"_hT").c_str(),     "HT (sum Jet Et plus mu Pt + MET)", 120, 0, 1200);
  histograms[sampleNameInput+"_hT_Lep"] = theDir.make<TH1F>( (sampleNameInput+"_hT_lep").c_str(), "HT (sum Jet Et plus mu Pt)",       120, 0, 1200);
  histograms[sampleNameInput+"_wMT"]    = theDir.make<TH1F>( (sampleNameInput+"_wMT").c_str(),    "W Transverse Mass, total",          50, 0,  500);
  histograms[sampleNameInput+"_MET"]    = theDir.make<TH1F>( (sampleNameInput+"_MET").c_str(),    "Missing E_{T}, total" ,            120, 0,  300);

  
  for(unsigned int i=0; i<6; ++i) {
    string jtNum = Form("_%dj",i);
    histograms[sampleNameInput+"_muPt"+jtNum] = theDir.make<TH1F>( (sampleNameInput+"_muPt"+jtNum).c_str(), "muon p_{T}", 100, 0, 200);
    histograms[sampleNameInput+"_muEta"+jtNum] = theDir.make<TH1F>( (sampleNameInput+"_muEta"+jtNum).c_str(), "muon #eta", 120, 0, 2.4);
    histograms[sampleNameInput+"_muPt"+jtNum+"_0t"] = theDir.make<TH1F>( (sampleNameInput+"_muPt"+jtNum+"_0t").c_str(), "muon p_{T}", 100, 0, 200);
    histograms[sampleNameInput+"_muEta"+jtNum+"_0t"] = theDir.make<TH1F>( (sampleNameInput+"_muEta"+jtNum+"_0t").c_str(), "muon #eta", 120, 0, 2.4);
    histograms[sampleNameInput+"_hT"+jtNum]   = theDir.make<TH1F>( (sampleNameInput+"_hT"+jtNum).c_str(), "HT (sum Jet Et + mu Pt + MET)", 120, 0, 1200);
    histograms[sampleNameInput+"_hT"+jtNum+"_0t"]  = theDir.make<TH1F>( (sampleNameInput+"_hT"+jtNum+"_0t").c_str(), "HT (sum Jet Et + mu Pt + MET, 0-Tag)", 120, 0, 1200);
    histograms[sampleNameInput+"_hT_Lep"+jtNum] = theDir.make<TH1F>( (sampleNameInput+"_hT_Lep"+jtNum).c_str(), "HTlep (sum Jet Et + mu Pt)", 120, 0, 1200);
    histograms[sampleNameInput+"_hT_Lep"+jtNum+"_0t"] = theDir.make<TH1F>( (sampleNameInput+"_hT_Lep"+jtNum+"_0t").c_str(), "HTlep (sum Jet Et + mu Pt, 0-Tag)", 120, 0, 1200);
    histograms[sampleNameInput+"_wMT"+jtNum]  = theDir.make<TH1F>( (sampleNameInput+"_wMT"+jtNum).c_str(), "W Trans. Mass, 0 Jets", 50, 0, 500);
    histograms[sampleNameInput+"_wMT"+jtNum+"_0t"] = theDir.make<TH1F>( (sampleNameInput+"_wMT"+jtNum+"_0t").c_str(), "W Trans. Mass, 0 Jets, 0-Tag", 50,0,500);
    histograms[sampleNameInput+"_MET"+jtNum]  = theDir.make<TH1F>( (sampleNameInput+"_MET"+jtNum).c_str(), "Missing E_{T}, 0 Jets", 120,0.,300.);
    histograms[sampleNameInput+"_MET"+jtNum+"_0t"] = theDir.make<TH1F>( (sampleNameInput+"_MET"+jtNum+"_0t").c_str(), "Missing E_{T}, 0 Jets, 0-Tag", 120,0,300);
    histograms2d[sampleNameInput+"_muisoVsMuEta"+jtNum] = 
      theDir.make<TH2F>( (sampleNameInput+"_muisoVsMuEta"+jtNum).c_str(), "Muon isolation vs Muon Eta", 
			 12, 0., 2.4,
			 20, 0., 1.0
			 );
    histograms2d[sampleNameInput+"_muisoVsHt"+jtNum] = 
      theDir.make<TH2F>( (sampleNameInput+"_muisoVsHt"+jtNum).c_str(), "Muon isolation vs H_{T}", 
			 20., 0., 400,
			 20, 0., 1.0
			 );

    histograms2d[sampleNameInput+"_muisoVsMET"+jtNum] = 
      theDir.make<TH2F>( (sampleNameInput+"_muisoVsMET"+jtNum).c_str(), "Muon isolation vs MET", 
			 20., 0., 200,
			 20, 0., 1.0
			 );
    histograms2d[sampleNameInput+"_muisoVswMT"+jtNum] = 
      theDir.make<TH2F>( (sampleNameInput+"_muisoVswMT"+jtNum).c_str(), "Muon isolation vs wMT", 
			 20., 0., 200,
			 20, 0., 1.0
			 );

    histograms2d[sampleNameInput+"_muisoVsD0"+jtNum] = 
      theDir.make<TH2F>( (sampleNameInput+"_muisoVsD0"+jtNum).c_str(), "Muon isolation vs D0", 
			 100., 0., 0.2,
			 20, 0., 1.0
			 );

    histograms2d[sampleNameInput+"_muisoVsMuEta"+jtNum+"_0t"] = 
      theDir.make<TH2F>( (sampleNameInput+"_muisoVsMuEta"+jtNum+"_0t").c_str(), "Muon isolation vs Muon Eta, 0-Tag", 
			 12, 0., 2.4,
			 20, 0., 1.0
			 );
    histograms2d[sampleNameInput+"_muisoVsHt"+jtNum+"_0t"] = 
      theDir.make<TH2F>( (sampleNameInput+"_muisoVsHt"+jtNum+"_0t").c_str(), "Muon isolation vs H_{T}", 
			 20., 0., 400,
			 20, 0., 1.0
			 );

    histograms2d[sampleNameInput+"_muisoVsMET"+jtNum+"_0t"] = 
      theDir.make<TH2F>( (sampleNameInput+"_muisoVsMET"+jtNum+"_0t").c_str(), "Muon isolation vs MET", 
			 20., 0., 200,
			 20, 0., 1.0
			 );
    histograms2d[sampleNameInput+"_muisoVswMT"+jtNum+"_0t"] = 
      theDir.make<TH2F>( (sampleNameInput+"_muisoVswMT"+jtNum+"_0t").c_str(), "Muon isolation vs wMT", 
			 20., 0., 200,
			 20, 0., 1.0
			 );
    histograms2d[sampleNameInput+"_muisoVsD0"+jtNum+"_0t"] = 
      theDir.make<TH2F>( (sampleNameInput+"_muisoVsD0"+jtNum+"_0t").c_str(), "Muon isolation vs D0", 
			 100., 0., 0.2,
			 20, 0., 1.0
			 );



  }
  for (unsigned int j=0;j<sampleName.size();++j) {

    // hT
    for ( unsigned int k=0; k < hTName.size(); ++k ) {
      // First do the pretagged histograms by flavor path
      std::string pretemp = sampleName[j]+hTName[k];
      histograms[pretemp] = theDir.make<TH1F>(pretemp.c_str(), "hT", 120, 0, 1200);
      // Next do the untagged histograms by flavor path
      std::string untemp = sampleName[j]+hTName[k]+"_0t";
      histograms[untemp] = theDir.make<TH1F>(untemp.c_str(), "hT", 120, 0, 1200);
    }

    // MET
    for ( unsigned int k=0; k < METName.size(); ++k ) {
      // First do the pretagged histograms by flavor path
      std::string pretemp = sampleName[j]+METName[k];
      histograms[pretemp] = theDir.make<TH1F>(pretemp.c_str(), "MET", 120, 0,  300);
      // Next do the untagged histograms by flavor path
      std::string untemp = sampleName[j]+METName[k]+"_0t";
      histograms[untemp] = theDir.make<TH1F>(untemp.c_str(), "MET", 120, 0,  300);
    }

    // muEta
    for ( unsigned int k=0; k < muEtaName.size(); ++k ) {
      // First do the pretagged histograms by flavor path
      std::string pretemp = sampleName[j]+muEtaName[k];
      histograms[pretemp] = theDir.make<TH1F>(pretemp.c_str(), "muEta",  120, 0, 2.4);
      // Next do the untagged histograms by flavor path
      std::string untemp = sampleName[j]+muEtaName[k]+"_0t";
      histograms[untemp] = theDir.make<TH1F>(untemp.c_str(), "muEta",  120, 0, 2.4);
    }
    

    // secvtx mass
    for(unsigned int k=0;k<secvtxName.size();++k) {
      for(unsigned int l=0;l<secvtxEnd.size();++l) {
        std::string temp = sampleName[j]+secvtxName[k]+secvtxEnd[l];
        histograms[temp] = theDir.make<TH1F>(temp.c_str(), "secvtxmass", 40,    0,   10);
        std::string temp2 = sampleName[j]+secvtxName[k]+secvtxEnd[l]+"_vs_iso";
        histograms2d[temp2] = theDir.make<TH2F>(temp2.c_str(), "secvtxmass", 40,    0,   10,
						10, 0., 1.0 );
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
    LHAPDF::usePDFMember(pdfEigenToUse_);
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

  allNumTags_ = 0;
  allNumJets_ = (int) jets.size();
 
  // std::cout << "Filling global weight in make_templates : " << globalWeight_ << std::endl;
  reco::Candidate::LorentzVector nu_p4 = met.p4();
  reco::Candidate::LorentzVector lep_p4 = ( muPlusJets_  ? muons[0].p4() : electrons[0].p4() );
  // double wMT = (lep_p4 + nu_p4).mt();
  double hT = lep_p4.pt() + nu_p4.Et();
  // double hT_lep = lep_p4.pt();
  pat::Muon const * patMuon = dynamic_cast<pat::Muon const *>(&* muons[0].masterClonePtr());
  if ( patMuon == 0 )
    throw cms::Exception("InvalidMuonPointer") << "Muon pointer is invalid you schmuck." << std::endl;
  double hcalIso = patMuon->hcalIso();
  double ecalIso = patMuon->ecalIso();
  double trkIso  = patMuon->trackIso();
  double pt      = patMuon->pt() ;
  double d0      = fabs(patMuon->dB());
  
  double relIso = (ecalIso + hcalIso + trkIso) / pt;

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

  //SecVtxMass and b-tagging related quantities
  int numBottom=0,numCharm=0,numLight=0;
  int numTags=0, numJets=0;
  double vertexMass = 0.0;
  std::vector<double> vertexMasses;
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


  // bool foundWeird = false;
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
      if ( svTagInfos == 0 ) { 
	continue;
      }
      histograms["nVertices"]-> Fill( svTagInfos->nVertices(), globalWeight_ );
      
      // Check to make sure we have a vertex
      
      if ( svTagInfos->nVertices() <= 0 ) {
	continue;
      }
      
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

      // If desired to use the simple SF inclusion, throw a random variable between 1 and 0,
      // if it is less than the SF, keep going, else, throw the jet away
      bool keepGoing = true;
      if ( simpleSFCalc_ ) {
	double irand = gRandom->Uniform();
	double max = 0;
	if ( jetFlavor == 5 || jetFlavor == 4 )
	  max = bcEffScale_;
	else
	  max = lfEffScale_;
	if ( irand < max ) keepGoing=true;
	else keepGoing=false;
      }

      // Check to see if the actual jet is tagged
      double discCut = allDiscrCut_;
      if ( doMC_ ) {
	if ( bDiscrCut_ > 0.0 && jetFlavor == 5 ) discCut = bDiscrCut_;
	if ( cDiscrCut_ > 0.0 && jetFlavor == 4 ) discCut = cDiscrCut_;
	if ( lDiscrCut_ > 0.0 && jetFlavor!=5 && jetFlavor != 4 ) discCut = lDiscrCut_;	
      }
      vertexMasses.push_back( svTagInfos->secondaryVertex(0).p4().mass() );


      if( jet->bDiscriminator(btaggerString_) < discCut || !keepGoing ) continue;
      ++allNumTags_;

      // Take the template info from the first tag (ordered by jet pt)      
      if ( firstTag ) {

	if ( jet->hasUserData("secvtxMass") )
	  vertexMass = jet->userFloat("secvtxMass");
	else 
	  vertexMass = svTagInfos->secondaryVertex(0).p4().mass();
        
        firstTag = false;
      }// end if first tag
    }// end loop over jets



  //Here we determine what kind of flavor we have in this jet	
  string whichtag = "";
  int massFlavor = 0;
  if( doMC_ ) {

    // Restrict to >= 2 tags
    if(numBottom>2) numBottom=2;
    if(numCharm>2 ) numCharm =2;
    if(numLight>2 ) numLight =2;

    if      ( numBottom ) massFlavor = 5; 
    else if ( numCharm  ) massFlavor = 4;
    else                  massFlavor = 0;

    switch (massFlavor)
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

    if      (numBottom)              whichtag = "_b";
    else if (numCharm)               whichtag = "_c";
    else if (numLight)               whichtag = "_q";
    else                             whichtag = "_x";


    // if (1 == numTags) {
    //   // single tag
    //   if      (numBottom)              whichtag = "_b";
    //   else if (numCharm)               whichtag = "_c";
    //   else if (numLight)               whichtag = "_q";
    //   else                             whichtag = "_x";
    // }
    // else {
    //   // double tags
    //   if      (2 == numBottom)         whichtag = "_bb";
    //   else if (2 == numCharm)          whichtag = "_cc";
    //   else if (2 == numLight)          whichtag = "_qq";
    //   else if (numBottom && numCharm)  whichtag = "_bc";
    //   else if (numBottom && numLight)  whichtag = "_bq";
    //   else if (numCharm  && numLight)  whichtag = "_cq";
    //   else                             whichtag = "_xx";
    // } // if two tags
  }
  
  // For now, we only care if we have 2 tags...any more are treated the same - maybe we should look at 3 tags?
  numTags = std::min( allNumTags_, 2 );
  numJets = std::min( allNumJets_, 5 );


  histograms["nTags"]->Fill(numTags, globalWeight_);

  // Now, if we have jets, fill 0, 1, and >=2 tag histograms.
  // The 0-tag histograms are hT, met, and mT_w.
  // The 1-tag and >=2-tag histogram is the secondary vertex mass
  // of the highest pt tagged jet.

  // Fill a "summed" histogram without path name also, if we are using flavor history categories
  if ( useHFcat_ ) {
    histograms[sampleHistName_ + Form("_muEta_%dj",  numJets)]->Fill( fabs(muons[0].eta()), globalWeight_ );
    histograms[sampleHistName_ + Form("_hT_%dj",     numJets)]->Fill( hT,                   globalWeight_ );
    histograms[sampleHistName_ + Form("_MET_%dj",    numJets)]->Fill( met.pt(),             globalWeight_ );
  }

  histograms[sampleNameInput + Form("_muEta_%dj",  numJets)]->Fill( fabs(muons[0].eta()), globalWeight_ );
  histograms[sampleNameInput + Form("_hT_%dj",     numJets)]->Fill( hT,                   globalWeight_ );
  histograms[sampleNameInput + Form("_MET_%dj",    numJets)]->Fill( met.pt(),             globalWeight_ );
  histograms2d[sampleNameInput + Form("_muisoVsMuEta_%dj", numJets)]->Fill( fabs(muons[0].eta()), relIso, globalWeight_ );
  histograms2d[sampleNameInput + Form("_muisoVsHt_%dj", numJets)]->Fill( hT, relIso, globalWeight_ );
  histograms2d[sampleNameInput + Form("_muisoVsMET_%dj", numJets)]->Fill( met.pt(), relIso, globalWeight_ );
  histograms2d[sampleNameInput + Form("_muisoVsD0_%dj", numJets)]->Fill( d0, relIso, globalWeight_ );



  
  if ( !reweightBTagEff_ )  {
    if( numTags > 0 ) {
      string massName  = sampleHistName_ + Form("_secvtxMass_%dj_%dt", numJets, numTags);
      
      histograms[massName             ]-> Fill (vertexMass, globalWeight_);
      histograms2d[massName +"_vs_iso"            ]-> Fill (vertexMass, relIso, globalWeight_);
      if( doMC_ ) {	
	histograms[massName + whichtag  ]-> Fill (vertexMass, globalWeight_);	
	histograms2d[massName + whichtag + "_vs_iso"  ]-> Fill (vertexMass, relIso, globalWeight_);
      } // end if doMC
    } // end if numTags > 0    
    else {  // if ( numTags == 0 ) {
      // Fill a "summed" histogram without path name also, if we are using flavor history categories
      if ( useHFcat_ ) {
	histograms[sampleHistName_ + Form("_muEta_%dj_0t",  numJets)]->Fill( fabs(muons[0].eta()), globalWeight_ );
	histograms[sampleHistName_ + Form("_hT_%dj_0t",     numJets)]->Fill( hT,                   globalWeight_ );
	histograms[sampleHistName_ + Form("_MET_%dj_0t",    numJets)]->Fill( met.pt(),             globalWeight_ );
      }
      histograms[sampleNameInput + Form("_muEta_%dj_0t",  numJets)]->Fill( fabs(muons[0].eta()), globalWeight_ );
      histograms[sampleNameInput + Form("_hT_%dj_0t",     numJets)]->Fill( hT,                   globalWeight_ );
      histograms[sampleNameInput + Form("_MET_%dj_0t",    numJets)]->Fill( met.pt(),             globalWeight_ );
      histograms2d[sampleNameInput + Form("_muisoVsMuEta_%dj_0t", numJets)]->Fill( fabs(muons[0].eta()), relIso, globalWeight_ );
      histograms2d[sampleNameInput + Form("_muisoVsHt_%dj_0t", numJets)]->Fill( hT, relIso, globalWeight_ );
      histograms2d[sampleNameInput + Form("_muisoVsMET_%dj_0t", numJets)]->Fill( met.pt(), relIso, globalWeight_ );
      histograms2d[sampleNameInput + Form("_muisoVsD0_%dj_0t", numJets)]->Fill( d0, relIso, globalWeight_ );
    } // end ntags = 0
  }// end if not reweighting b-tag eff

  else {  // reweighting b-tag eff:

    // std::cout << "Reweighting b-tag eff" << std::endl;
    // Here will be the efficiencies for the jets
    std::vector<shyft::helper::EffInfo> effs;
    std::string bstr = jetAlgo_ + "BEff";
    std::string cstr = jetAlgo_ + "CEff";
    std::string pstr = jetAlgo_ + "LFEff";
    // "unity"
    shyft::helper::EffInfo unity( -1, 1.0, 0);


    // get the efficiency parameterizations
    // std::cout << "Getting custom eff parameterizations" << std::endl;
    TH2 * bEff = (TH2*)customBtagFile_->Get( bstr.c_str() );
    TH2 * cEff = (TH2*)customBtagFile_->Get( cstr.c_str() );
    TH2 * pEff = (TH2*)customBtagFile_->Get( pstr.c_str() );    

    // Loop over jets, create the efficiency vector to be used in
    // the combinatoric calculations. 
    // std::cout << "Looping over jets" << std::endl;
    for ( ShallowCloneCollection::const_iterator jetBegin = jets.begin(),
	    jetEnd = jets.end(), jetIter = jetBegin;
	  jetIter != jetEnd; ++jetIter)
      {
	// std::cout << "Processing jet " << jetIter - jetBegin << std::endl;
	const pat::Jet* jet = dynamic_cast<const pat::Jet *>(jetIter->masterClonePtr().get());
	// We first get the flavor of the jet so we can fill look at btag efficiency.
	int jetFlavor = std::abs( jet->partonFlavour() );
	double jetPt  = std::abs( jet->pt() );
	double jetEta = std::abs( jet->eta() );
	int ibin = bEff->GetXaxis()->FindBin( jetPt );
	// int jbin = bEff->GetYaxis()->FindBin( jetEta );
	if ( ibin >= bEff->GetNbinsX() ) ibin = bEff->GetNbinsX() - 1;
	if ( jetFlavor == 5 ) {
	  effs.push_back( shyft::helper::EffInfo(jetIter - jetBegin, 
						 bEff->GetBinContent( ibin ) * bcEffScale_,
						 jetFlavor
						 ) );
	} else if (jetFlavor == 4 ) {
	  effs.push_back( shyft::helper::EffInfo(jetIter - jetBegin, 
						 cEff->GetBinContent( ibin ) * bcEffScale_,
						 jetFlavor
						 ) );
	} else {
	  effs.push_back( shyft::helper::EffInfo(jetIter - jetBegin, 
						 pEff->GetBinContent( ibin ) * lfEffScale_,
						 jetFlavor
						 ) );
	}

	// if ( jbin >= bEff->GetNbinsY() ) jbin = bEff->GetNbinsY() - 1;
	// if ( jetFlavor == 5 ) {
	//   effs.push_back( shyft::helper::EffInfo(jetIter - jetBegin, 
	// 					 bEff->GetBinContent( ibin, jbin ) * bcEffScale_,
	// 					 jetFlavor
	// 					 ) );
	// } else if (jetFlavor == 4 ) {
	//   effs.push_back( shyft::helper::EffInfo(jetIter - jetBegin, 
	// 					 cEff->GetBinContent( ibin, jbin ) * bcEffScale_,
	// 					 jetFlavor
	// 					 ) );
	// } else {
	//   effs.push_back( shyft::helper::EffInfo(jetIter - jetBegin, 
	// 					 pEff->GetBinContent( ibin, jbin ) * lfEffScale_,
	// 					 jetFlavor
	// 					 ) );
	// }
      }
    
    double totalSum = 0.0;
    for ( unsigned int inumTags = 0; inumTags <= jets.size(); ++inumTags ) {
      // std::cout << "inumTags = " << inumTags << std::endl;
      double sum = 0.0;
      do {

	// std::cout << "Combination : " << std::endl;
	// copy(effs.begin(), effs.end(), std::ostream_iterator<shyft::helper::EffInfo>(std::cout, " "));
	// std::cout << std::endl;

	// Get the "tag" bit, from "begin" to "inumTags"
	shyft::helper::EffInfo ni = accumulate(effs.begin(), effs.begin() + inumTags, unity, std::multiplies<shyft::helper::EffInfo>());
	// Get the "untag" bit, from "inumTags" to "end"
	shyft::helper::EffInfo nj = accumulate(effs.begin()+inumTags, effs.end(), unity, shyft::helper::oneminusmultiplies<shyft::helper::EffInfo>());
	// The product is the total probability to tag exactly inumTags jets.
	double iprob = ni.eff * nj.eff;
	sum += iprob;	

	if( inumTags > 0 ) {
	  int kknumTags = std::min( (int) inumTags, 2 );
	  string massName  = sampleHistName_ + Form("_secvtxMass_%dj_%dt", numJets, kknumTags);      
	  // std::cout << "Getting " << massName << std::endl;
	  histograms  [massName                       ]-> Fill (vertexMass, globalWeight_ * iprob);
	  histograms2d[massName +"_vs_iso"            ]-> Fill (vertexMass, relIso, globalWeight_ * iprob);
	  if( doMC_ ) {	
	    // std::cout << "Getting " << massName + whichtag << std::endl;
	    histograms  [massName + whichtag              ]-> Fill (vertexMass, globalWeight_ * iprob);	
	    histograms2d[massName + whichtag + "_vs_iso"  ]-> Fill (vertexMass, relIso, globalWeight_ * iprob);
	  } // end if doMC

	} // end if inumTags > 0
	else {  // if ( inumTags == 0 ) {
	  // Fill a "summed" histogram without path name also, if we are using flavor history categories
	  if ( useHFcat_ ) {
	    histograms[sampleHistName_ + Form("_muEta_%dj_0t",  numJets)]->Fill( fabs(muons[0].eta()), globalWeight_ * iprob );
	    histograms[sampleHistName_ + Form("_hT_%dj_0t",     numJets)]->Fill( hT,                   globalWeight_ * iprob );
	    histograms[sampleHistName_ + Form("_MET_%dj_0t",    numJets)]->Fill( met.pt(),             globalWeight_ * iprob );
	  }
	  histograms  [sampleNameInput + Form("_muEta_%dj_0t",        numJets)]->Fill( fabs(muons[0].eta()), globalWeight_ * iprob );
	  histograms  [sampleNameInput + Form("_hT_%dj_0t",           numJets)]->Fill( hT,                   globalWeight_ * iprob );
	  histograms  [sampleNameInput + Form("_MET_%dj_0t",          numJets)]->Fill( met.pt(),             globalWeight_ * iprob );
	  histograms2d[sampleNameInput + Form("_muisoVsMuEta_%dj_0t", numJets)]->Fill( fabs(muons[0].eta()), relIso, globalWeight_ * iprob );
	  histograms2d[sampleNameInput + Form("_muisoVsHt_%dj_0t",    numJets)]->Fill( hT, relIso, globalWeight_ * iprob );
	  histograms2d[sampleNameInput + Form("_muisoVsMET_%dj_0t",   numJets)]->Fill( met.pt(), relIso, globalWeight_ * iprob );
	  histograms2d[sampleNameInput + Form("_muisoVsD0_%dj_0t",    numJets)]->Fill( d0, relIso, globalWeight_ * iprob );
	} // end ntags = 0    
      } while (shyft::helper::next_combination(effs.begin(),effs.begin() + inumTags, effs.end())); 
      // std::cout << "Combination probability = " << sum << std::endl;
      totalSum += sum;
    } // end loop over number of tags
    // std::cout << "Total probabilty = " << totalSum << std::endl;
  } // end if reweighting b-tag eff



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
  
  wPlusJets(iEvent, ret);
  std::vector<reco::ShallowClonePtrCandidate> const & electrons = wPlusJets.selectedElectrons();
  std::vector<reco::ShallowClonePtrCandidate> const & muons     = wPlusJets.selectedMuons();
  std::vector<reco::ShallowClonePtrCandidate> const & jets      = wPlusJets.cleanedJets();
  reco::ShallowClonePtrCandidate const & met = wPlusJets.selectedMET();
  
  string bit_;

  bit_ = "Trigger" ;
  bool passTrigger = ret[ bit_ ];
  // bit_ = "== 1 Lepton";
  // bool passOneLepton = ret[ bit_ ];
  // bit_ = ">=1 Jets";
  // bool jet1 = ret[bit_];
  // bit_ = ">=2 Jets";
  // bool jet2 = ret[bit_];
  // bit_ = ">=3 Jets";
  // bool jet3 = ret[bit_];
  // bit_ = ">=4 Jets";
  // bool jet4 = ret[bit_];
  // bit_ = ">=5 Jets";
  // bool jet5 = ret[bit_];
  bit_ = "Cosmic Veto";
  bool passPre = ret[bit_];
  // bool anyJets = jet1 || jet2 || jet3 || jet4 || jet5;
  
  // if not passed trigger, next event
  if ( !passTrigger )  return;
  
  if (doMC_ && reweightPDF_) {
    weightPDF(iEvent);
  }
  
  if(useHFcat_) {
    edm::Handle< unsigned int > heavyFlavorCategory;
    iEvent.getByLabel ( edm::InputTag("flavorHistoryFilter"),heavyFlavorCategory);
    assert ( heavyFlavorCategory.isValid() );
    if ( useHFcat_ ) histograms["flavorHistory"]-> Fill ( *heavyFlavorCategory, globalWeight_ );
  }

  sampleHistName_ = sampleNameInput + calcSampleName(iEvent);
  
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
  


std::string SHyFT::calcSampleName (const edm::EventBase& iEvent)
{
  std::string sampleName("");
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
  }
  return sampleName;
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


  // Eigenvector already set up for this job.
  // It is, contrary to the LHAPDF documentation, ABYSMALLY SLOW
  // to switch between PDF sets and so we will run
  // one single PDF with one single eigenvector *per job*
  
  double newpdf1 = LHAPDF::xfx(x1, Q, id1)/x1;
  double newpdf2 = LHAPDF::xfx(x2, Q, id2)/x2;
  double prod =  (newpdf1/pdf1*newpdf2/pdf2);
  iWeightSum += prod*prod;    
  iWeightSum = TMath::Sqrt(iWeightSum) ;
    
  globalWeight_ *= iWeightSum ;
  std::cout << "Global weight = " << globalWeight_ << std::endl;
  histograms["pdfWeight"]->Fill( globalWeight_ );

}
