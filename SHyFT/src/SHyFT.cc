#include "Analysis/SHyFT/interface/SHyFT.h"
#include "TVector3.h"
#include "TLorentzVector.h"
#include <sstream>

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
  doMC_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<bool>("doMC") ),
  plRootFile_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<string>("payload")  ),
  f_( plRootFile_.c_str(), "READ"),  es_(&f_),
  bPerformanceTag_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<string>("bPerformanceTag")  ),
  cPerformanceTag_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<string>("cPerformanceTag")  ),
  lPerformanceTag_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<string>("lPerformanceTag")  ),
  btaggerString_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<std::string>("btaggerString"))
{
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
      sampleName.push_back(sampleNameInput+"_path"+tmpString.str());
      if ( sampleNameInput != "Zjets" )
	sampleName.push_back(sampleNameInput+"W_path"+tmpString.str());
      if(sampleNameInput=="Vqq"  || sampleNameInput == "Zjets") {
        sampleName.push_back(sampleNameInput+"Z_path"+tmpString.str());
      }
    }
  }
  else sampleName.push_back(sampleNameInput);

  histograms["nJets"]         = theDir.make<TH1F>("nJets",    "N Jets, pt>30, eta<2.4",  15,    0,   15);
  histograms["jet1Pt"]        = theDir.make<TH1F>("jet1Pt",   "1st leading jet pt",     150,    0,  300);
  histograms["jet2Pt"]        = theDir.make<TH1F>("jet2Pt",   "2nd leading jet pt",     150,    0,  300);
  histograms["jet3Pt"]        = theDir.make<TH1F>("jet3Pt",   "3rd leading jet pt",     150,    0,  300);
  histograms["jet4Pt"]        = theDir.make<TH1F>("jet4Pt",   "4th leading jet pt",     150,    0,  300);
  histograms["jet1Eta"]       = theDir.make<TH1F>("jet1Eta",  "1st leading jet eta",     50, -3.0,  3.0);
  histograms["jet2Eta"]       = theDir.make<TH1F>("jet2Eta",  "2nd leading jet eta",     50, -3.0,  3.0);
  histograms["jet3Eta"]       = theDir.make<TH1F>("jet3Eta",  "3rd leading jet eta",     50, -3.0,  3.0);
  histograms["jet4Eta"]       = theDir.make<TH1F>("jet4Eta",  "4th leading jet eta",     50, -3.0,  3.0);
  histograms["jet1Phi"]       = theDir.make<TH1F>("jet1Phi",  "1st leading jet phi",     60, -3.5,  3.5);
  histograms["jet2Phi"]       = theDir.make<TH1F>("jet2Phi",  "2nd leading jet phi",     60, -3.5,  3.5);
  histograms["jet3Phi"]       = theDir.make<TH1F>("jet3Phi",  "3rd leading jet phi",     60, -3.5,  3.5);
  histograms["jet4Phi"]       = theDir.make<TH1F>("jet4Phi",  "4th leading jet phi",     60, -3.5,  3.5);
  if(doMC_) {
    histograms2d["jet1PtTrueRes"] = theDir.make<TH2F>("jet1PtTrueRes",   "1st leading jet pt / gen pt",  25, -5.0, 5.0, 50,    0,  3);
    histograms2d["jet2PtTrueRes"] = theDir.make<TH2F>("jet2PtTrueRes",   "2nd leading jet pt / gen pt",  25, -5.0, 5.0, 50,    0,  3);
    histograms2d["jet3PtTrueRes"] = theDir.make<TH2F>("jet3PtTrueRes",   "3rd leading jet pt / gen pt",  25, -5.0, 5.0, 50,    0,  3);
    histograms2d["jet4PtTrueRes"] = theDir.make<TH2F>("jet4PtTrueRes",   "4th leading jet pt / gen pt",  25, -5.0, 5.0, 50,    0,  3);

    histograms2d["jet1PtTrueResBJets"] = theDir.make<TH2F>("jet1PtTrueResBJets",   "1st leading bjet pt / gen pt",  25, -5.0, 5.0, 50,    0,  3);
    histograms2d["jet2PtTrueResBJets"] = theDir.make<TH2F>("jet2PtTrueResBJets",   "2nd leading bjet pt / gen pt",  25, -5.0, 5.0, 50,    0,  3);
    histograms2d["jet3PtTrueResBJets"] = theDir.make<TH2F>("jet3PtTrueResBJets",   "3rd leading bjet pt / gen pt",  25, -5.0, 5.0, 50,    0,  3);
    histograms2d["jet4PtTrueResBJets"] = theDir.make<TH2F>("jet4PtTrueResBJets",   "4th leading bjet pt / gen pt",  25, -5.0, 5.0, 50,    0,  3);

  }
  histograms["jet1Mass"]      = theDir.make<TH1F>("jet1Mass", "1st leading jet mass",    50,    0,  150);
  histograms["jet2Mass"]      = theDir.make<TH1F>("jet2Mass", "2nd leading jet mass",    50,    0,  150);
  histograms["jet3Mass"]      = theDir.make<TH1F>("jet3Mass", "3rd leading jet mass",    50,    0,  150);
  histograms["jet4Mass"]      = theDir.make<TH1F>("jet4Mass", "4th leading jet mass",    50,    0,  150);
  if(doMC_) {
    histograms["bmass"]         = theDir.make<TH1F>("bmass",    "B Sec Vtx Mass",          40,    0,   10);
    histograms["cmass"]         = theDir.make<TH1F>("cmass",    "C Sec Vtx Mass",          40,    0,   10);
    histograms["lfmass"]        = theDir.make<TH1F>("lfmass",   "LF Sec Vtx Mass",         40,    0,   10);
    histograms["flavorHistory"] = theDir.make<TH1F>("flavorHistory", "Flavor History",     12,    0,   12);
  }
  histograms["discriminator"] = theDir.make<TH1F>("discriminator", "BTag Discriminator", 30,    2,    8);
  histograms["nVertices"]     = theDir.make<TH1F>("nVertices",     "num sec Vertices",    5,    0,    5);
  histograms["nTags"]         = theDir.make<TH1F>("nTags",     "number of Tags",          3,    0,    3);
  

  histograms["tag_eff"]    = theDir.make<TH1F>("tag_eff", "0 lf untag, 1 c untag, 2 b untag, 3 lf tag, 4 c tag, 5 b tag", 6, 0, 6);
  histograms["tag_jet_pt"] = theDir.make<TH1F>("tag_jet_pt", "JetPt to go with tagging efficiency", 150,    0,    300);
  histograms2d["eff_vs_pt"]  = theDir.make<TH2F>("eff_vs_pt", "eff_vs_pt", 150, 0, 300, 6, 0, 6); 
  histograms2d["eff_vs_eta"] = theDir.make<TH2F>("eff_vs_eta", "eff_vs_eta", 50, -3.0, 3.0, 6, 0, 6);

  
  //Using btagging and mistag to do normalization
  histograms3d["normalization"]	= theDir.make<TH3F>("normalization",	"Normalization",	5,	1,	6,	2,	1,	3,   11,  0,  11 );
  //Store stat errors
  histograms3d["normalization"]		->  Sumw2();
  
  histograms["m3"] = theDir.make<TH1F>("m3", "M3", 60, 0, 600);
  
  histograms[sampleNameInput+"_muPt_0j"] = theDir.make<TH1F>( (sampleNameInput+"_muPt_0j").c_str(), "muon p_{T}", 100, 0, 200);
  histograms[sampleNameInput+"_muPt_1j"] = theDir.make<TH1F>( (sampleNameInput+"_muPt_1j").c_str(), "muon p_{T}", 100, 0, 200);
  histograms[sampleNameInput+"_muPt_2j"] = theDir.make<TH1F>( (sampleNameInput+"_muPt_2j").c_str(), "muon p_{T}", 100, 0, 200);
  histograms[sampleNameInput+"_muPt_3j"] = theDir.make<TH1F>( (sampleNameInput+"_muPt_3j").c_str(), "muon p_{T}", 100, 0, 200);
  histograms[sampleNameInput+"_muPt_4j"] = theDir.make<TH1F>( (sampleNameInput+"_muPt_4j").c_str(), "muon p_{T}", 100, 0, 200);
  histograms[sampleNameInput+"_muPt_5j"] = theDir.make<TH1F>( (sampleNameInput+"_muPt_5j").c_str(), "muon p_{T}", 100, 0, 200);
  histograms[sampleNameInput+"_hT"]    = theDir.make<TH1F>( (sampleNameInput+"_hT").c_str(),    "HT (sum Jet Et plus mu Pt)", 50, 0, 1200);
  histograms[sampleNameInput+"_hT_0j"] = theDir.make<TH1F>( (sampleNameInput+"_hT_0j").c_str(), "HT (sum Jet Et plus mu Pt)", 50, 0, 1200);
  histograms[sampleNameInput+"_hT_1j"] = theDir.make<TH1F>( (sampleNameInput+"_hT_1j").c_str(), "HT (sum Jet Et plus mu Pt)", 50, 0, 1200);
  histograms[sampleNameInput+"_hT_2j"] = theDir.make<TH1F>( (sampleNameInput+"_hT_2j").c_str(), "HT (sum Jet Et plus mu Pt)", 50, 0, 1200);
  histograms[sampleNameInput+"_hT_3j"] = theDir.make<TH1F>( (sampleNameInput+"_hT_3j").c_str(), "HT (sum Jet Et plus mu Pt)", 50, 0, 1200);
  histograms[sampleNameInput+"_hT_4j"] = theDir.make<TH1F>( (sampleNameInput+"_hT_4j").c_str(), "HT (sum Jet Et plus mu Pt)", 50, 0, 1200);
  histograms[sampleNameInput+"_hT_5j"] = theDir.make<TH1F>( (sampleNameInput+"_hT_5j").c_str(), "HT (sum Jet Et plus mu Pt)", 50, 0, 1200);
  histograms[sampleNameInput+"_hT_0j_0t"] = theDir.make<TH1F>( (sampleNameInput+"_hT_0j_0t").c_str(), "HT (sum Jet Et plus mu Pt for 0-Tag)", 50,  50, 1200);
  histograms[sampleNameInput+"_hT_1j_0t"] = theDir.make<TH1F>( (sampleNameInput+"_hT_1j_0t").c_str(), "HT (sum Jet Et plus mu Pt for 0-Tag)", 50,  50, 1200);
  histograms[sampleNameInput+"_hT_2j_0t"] = theDir.make<TH1F>( (sampleNameInput+"_hT_2j_0t").c_str(), "HT (sum Jet Et plus mu Pt for 0-Tag)", 50,  50, 1200);
  histograms[sampleNameInput+"_hT_3j_0t"] = theDir.make<TH1F>( (sampleNameInput+"_hT_3j_0t").c_str(), "HT (sum Jet Et plus mu Pt for 0-Tag)", 50,  50, 1200);
  histograms[sampleNameInput+"_hT_4j_0t"] = theDir.make<TH1F>( (sampleNameInput+"_hT_4j_0t").c_str(), "HT (sum Jet Et plus mu Pt for 0-Tag)", 50,  50, 1200);
  histograms[sampleNameInput+"_hT_5j_0t"] = theDir.make<TH1F>( (sampleNameInput+"_hT_5j_0t").c_str(), "HT (sum Jet Et plus mu Pt for 0-Tag)", 50,  50, 1200);
  
  histograms[sampleNameInput+"_wMT"]    = theDir.make<TH1F>( (sampleNameInput+"_wMT").c_str(),    "W Transverse Mass, total",  25,   0, 500);
  histograms[sampleNameInput+"_wMT_0j"] = theDir.make<TH1F>( (sampleNameInput+"_wMT_0j").c_str(), "W Transverse Mass, 0 jets", 25,   0, 500);
  histograms[sampleNameInput+"_wMT_1j"] = theDir.make<TH1F>( (sampleNameInput+"_wMT_1j").c_str(), "W Transverse Mass, 1 jets", 25,   0, 500);
  histograms[sampleNameInput+"_wMT_2j"] = theDir.make<TH1F>( (sampleNameInput+"_wMT_2j").c_str(), "W Transverse Mass, 2 jets", 25,   0, 500);
  histograms[sampleNameInput+"_wMT_3j"] = theDir.make<TH1F>( (sampleNameInput+"_wMT_3j").c_str(), "W Transverse Mass, 3 jets", 25,   0, 500);
  histograms[sampleNameInput+"_wMT_4j"] = theDir.make<TH1F>( (sampleNameInput+"_wMT_4j").c_str(), "W Transverse Mass, 4 jets", 25,   0, 500);
  histograms[sampleNameInput+"_wMT_5j"] = theDir.make<TH1F>( (sampleNameInput+"_wMT_5j").c_str(), "W Transverse Mass, 5 jets", 25,   0, 500);
  histograms[sampleNameInput+"_wMT_0j_0t"] = theDir.make<TH1F>( (sampleNameInput+"_wMT_0j_0t").c_str(), "W Transverse Mass, 0 jets with 0-Tag", 25,   0, 500);
  histograms[sampleNameInput+"_wMT_1j_0t"] = theDir.make<TH1F>( (sampleNameInput+"_wMT_1j_0t").c_str(), "W Transverse Mass, 1 jets with 0-Tag", 25,   0, 500);
  histograms[sampleNameInput+"_wMT_2j_0t"] = theDir.make<TH1F>( (sampleNameInput+"_wMT_2j_0t").c_str(), "W Transverse Mass, 2 jets with 0-Tag", 25,   0, 500);
  histograms[sampleNameInput+"_wMT_3j_0t"] = theDir.make<TH1F>( (sampleNameInput+"_wMT_3j_0t").c_str(), "W Transverse Mass, 3 jets with 0-Tag", 25,   0, 500);
  histograms[sampleNameInput+"_wMT_4j_0t"] = theDir.make<TH1F>( (sampleNameInput+"_wMT_4j_0t").c_str(), "W Transverse Mass, 4 jets with 0-Tag", 25,   0, 500);
  histograms[sampleNameInput+"_wMT_5j_0t"] = theDir.make<TH1F>( (sampleNameInput+"_wMT_5j_0t").c_str(), "W Transverse Mass, 5 jets with 0-Tag", 25,   0, 500);
  
  histograms[sampleNameInput+"_MET"]    = theDir.make<TH1F>( (sampleNameInput+"_MET").c_str(),    "Missing E_{T}, total" , 25,   0, 250);
  histograms[sampleNameInput+"_MET_0j"] = theDir.make<TH1F>( (sampleNameInput+"_MET_0j").c_str(), "Missing E_{T}, 0 Jets", 25,   0, 250);
  histograms[sampleNameInput+"_MET_1j"] = theDir.make<TH1F>( (sampleNameInput+"_MET_1j").c_str(), "Missing E_{T}, 1 Jets", 25,   0, 250);
  histograms[sampleNameInput+"_MET_2j"] = theDir.make<TH1F>( (sampleNameInput+"_MET_2j").c_str(), "Missing E_{T}, 2 Jets", 25,   0, 250);
  histograms[sampleNameInput+"_MET_3j"] = theDir.make<TH1F>( (sampleNameInput+"_MET_3j").c_str(), "Missing E_{T}, 3 Jets", 25,   0, 250);
  histograms[sampleNameInput+"_MET_4j"] = theDir.make<TH1F>( (sampleNameInput+"_MET_4j").c_str(), "Missing E_{T}, 4 Jets", 25,   0, 250);
  histograms[sampleNameInput+"_MET_5j"] = theDir.make<TH1F>( (sampleNameInput+"_MET_5j").c_str(), "Missing E_{T}, 5 Jets", 25,   0, 250);
  histograms[sampleNameInput+"_MET_0j_0t"] = theDir.make<TH1F>( (sampleNameInput+"_MET_0j_0t").c_str(), "Missing E_{T}, 0 Jets in 0-Tag Sample", 25,   0, 250);
  histograms[sampleNameInput+"_MET_1j_0t"] = theDir.make<TH1F>( (sampleNameInput+"_MET_1j_0t").c_str(), "Missing E_{T}, 1 Jets in 0-Tag Sample", 25,   0, 250);
  histograms[sampleNameInput+"_MET_2j_0t"] = theDir.make<TH1F>( (sampleNameInput+"_MET_2j_0t").c_str(), "Missing E_{T}, 2 Jets in 0-Tag Sample", 25,   0, 250);
  histograms[sampleNameInput+"_MET_3j_0t"] = theDir.make<TH1F>( (sampleNameInput+"_MET_3j_0t").c_str(), "Missing E_{T}, 3 Jets in 0-Tag Sample", 25,   0, 250);
  histograms[sampleNameInput+"_MET_4j_0t"] = theDir.make<TH1F>( (sampleNameInput+"_MET_4j_0t").c_str(), "Missing E_{T}, 4 Jets in 0-Tag Sample", 25,   0, 250);
  histograms[sampleNameInput+"_MET_5j_0t"] = theDir.make<TH1F>( (sampleNameInput+"_MET_5j_0t").c_str(), "Missing E_{T}, 5 Jets in 0-Tag Sample", 25,   0, 250);
  
  for (unsigned int j=0;j<sampleName.size();++j) {
    for(unsigned int k=0;k<secvtxName.size();++k) {
      for(unsigned int l=0;l<secvtxEnd.size();++l) {
        std::string temp = sampleName[j]+secvtxName[k]+secvtxEnd[l];
        histograms[temp] = theDir.make<TH1F>(temp.c_str(), "secvtxmass", 40,    0,   10);
        if(k==0 && l==4) break;
        else if(!doMC_ && k==0 && l==0) break;
        //std::cout << temp << std::endl;
      }
    }
  }
  
  //Book some data histograms
  /*  if(!doMC_) {
    for(unsigned int k=0;k<secvtxName.size();++k) {
      std::string temp = string("Data") + secvtxName[k];
      histograms[temp+"1t"]   = theDir.make<TH1F>( (temp+"1t").c_str(), "Data SecvtxMass",  40,    0,   10);
      if( k!=0 )
        histograms[temp+"2t"] = theDir.make<TH1F>( (temp+"2t").c_str(), "Data SecvtxMass",  40,    0,   10);
    }
    }*/
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

  histograms["ePt"      ]->Fill( ePt_        );
  histograms["eEta"     ]->Fill( eEta_       );
  histograms["ePhi"     ]->Fill( ePhi_       );
  histograms["eD0"      ]->Fill( eD0_        );
  histograms["eTrackIso"]->Fill( trackIso_   );
  histograms["eECalIso" ]->Fill( eCalIso_    );
  histograms["eHCalIso" ]->Fill( hCalIso_    );
  histograms["eRelIso"  ]->Fill( relIso_     );
  
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

  histograms["muPt"      ]->Fill( muPt_        );
  histograms["muEta"     ]->Fill( muEta_       );
  histograms["muNhits"   ]->Fill( nhits_       );
  histograms["muD0"      ]->Fill( muD0_        );
  histograms["muChi2"    ]->Fill( norm_chi2_   );
  histograms["muHCalVeto"]->Fill( muHCalVeto_  );
  histograms["muECalVeto"]->Fill( muECalVeto_  );
  histograms["muTrackIso"]->Fill( trackIso_    );
  histograms["muECalIso" ]->Fill( eCalIso_     );
  histograms["muHCalIso" ]->Fill( hCalIso_     );
  histograms["muRelIso"  ]->Fill( relIso_      );
  
  return true;
}


// fill the plots for the jets
bool SHyFT::make_templates(const std::vector<reco::ShallowClonePtrCandidate>& jets,
			   const reco::ShallowClonePtrCandidate & met,
			   const std::vector<reco::ShallowClonePtrCandidate>& muons,
			   const std::vector<reco::ShallowClonePtrCandidate>& electrons)
{

  reco::Candidate::LorentzVector nu_p4 = met.p4();
  reco::Candidate::LorentzVector lep_p4 = ( muPlusJets_  ? muons[0].p4() : electrons[0].p4() );
  double wMT = (lep_p4 + nu_p4).mt();
  double hT = lep_p4.pt() + nu_p4.Et();

  //SecVtxMass and b-tagging related quantities
  int numBottom=0,numCharm=0,numLight=0;
  int numTags=0, numJets=0;
  double sumVertexMass=0, vertexMass=0;

  //Get Payload and Working Point
  fwlite::ESHandle< PerformancePayload >   plBHandle;
  fwlite::ESHandle< PerformancePayload >   plLHandle;
  fwlite::ESHandle< PerformancePayload >   plCHandle;
  fwlite::ESHandle< PerformanceWorkingPoint >   wpBHandle;
  fwlite::ESHandle< PerformanceWorkingPoint >   wpLHandle;
  fwlite::ESHandle< PerformanceWorkingPoint >   wpCHandle;
  es_.get(recId_).get(plBHandle, bPerformanceTag_.c_str() );
  es_.get(recId_).get(wpBHandle, bPerformanceTag_.c_str() );
  es_.get(recId_).get(plCHandle, cPerformanceTag_.c_str() );
  es_.get(recId_).get(wpCHandle, cPerformanceTag_.c_str() );
  es_.get(recId_).get(plLHandle, lPerformanceTag_.c_str() );
  es_.get(recId_).get(wpLHandle, lPerformanceTag_.c_str() );
  if( !(plBHandle.isValid() && wpBHandle.isValid() ) )
    std::cout<<"BEff BtagPerformance is not valid !!"<<std::endl;
  if( !(plLHandle.isValid() && wpLHandle.isValid() ) )
    std::cout<<"LEff BtagPerformance is not valid !!"<<std::endl;
  if( !(plCHandle.isValid() && wpCHandle.isValid() ) )
    std::cout<<"CEff BtagPerformance is not valid !!"<<std::endl;
  
  BtagPerformance  perfB( *plBHandle, *wpBHandle );
  BtagPerformance  perfL( *plLHandle, *wpLHandle );
  BtagPerformance  perfC( *plCHandle, *wpCHandle );
  btagOP_ = perfB.workingPoint().cut();
 
 
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

    for (unsigned int j=0;j<jets.size() - 2;++j)
      {
        for (unsigned int k=j+1;k<jets.size() - 1;++k)
          {
            for (unsigned int l = k+1; l<jets.size(); ++l)
              {
                TLorentzVector threeJets = jets_p4[j] + jets_p4[k] + jets_p4[l];
                if (highestPt < threeJets.Perp())
                  {
                    M3 = threeJets.M();
                    highestPt=threeJets.Perp();
                  }
              }
          }
      }
    histograms["m3"]->Fill( M3 );
  }

  
  for ( ShallowCloneCollection::const_iterator jetBegin = jets.begin(),
          jetEnd = jets.end(), jetIter = jetBegin;
        jetIter != jetEnd; ++jetIter)
    {

      const pat::Jet* jet = dynamic_cast<const pat::Jet *>(jetIter->masterClonePtr().get());
      
      // We first get the flavor of the jet so we can fill look at btag efficiency.
      int jetFlavor = std::abs( jet->partonFlavour() );
      double jetPt  = std::abs( jet->pt() );
      hT += jet->et();
      
      //histograms["tag_jet_pt"]->Fill( jetPt );
      histograms2d["massVsPt"]->Fill( jetPt, jet->mass() );
      
      if( doMC_ ) {
	typedef std::pair<std::string, float> pair_type ;
	std::vector<pair_type> const & pairs = jet->getPairDiscri();
	for ( std::vector<pair_type>::const_iterator ipair = pairs.begin();
	      ipair != pairs.end(); ++ipair ) {
	}

        // Is this jet tagged and does it have a good secondary vertex
        if( jet->bDiscriminator(btaggerString_) < btagOP_ ) {
          //cout << "first, bop = " << btagOP_ << endl;
          // This jet is not tagged, so we skip it but first we check the btag efficiency.
          if     ( jetFlavor == 4 ) histograms["tag_eff"]-> Fill( 1 );
          else if( jetFlavor == 5 ) histograms["tag_eff"]-> Fill( 2 );
          else                      histograms["tag_eff"]-> Fill( 0 );
          continue;
        } 
        else {
          //cout << "second, bop = " << btagOP_ << endl;
          if     ( jetFlavor == 4 ) histograms["tag_eff"]-> Fill( 4 );
          else if( jetFlavor == 5 ) histograms["tag_eff"]-> Fill( 5 );
          else                      histograms["tag_eff"]-> Fill( 3 );
        }
      }
      //cout << "TESTING HERE " << endl;
      //      cout << "
      //if ( useHFcat_ ) histograms["flavorHistory"]-> Fill ( HFcat_ );
      //std::cout << jet->bDiscriminator(btaggerString_) << " " << btagOP_ << std::endl;
      //std::cout << btaggerString_ << std::endl;
      //histograms["discriminator"]-> Fill ( jet->bDiscriminator(btaggerString_) );
      
      
      //If this jet is not tagged, skip it
      //      if( jet->bDiscriminator(btaggerString_) < btagOP_ )
      //continue;
      
      reco::SecondaryVertexTagInfo const * svTagInfos
        = jet->tagInfoSecondaryVertex("secondaryVertex");
      if ( svTagInfos == 0 ) continue;
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

      
      if( doMC_ ) {
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
      }
      ++numTags;
      histograms["discriminator"]-> Fill ( jet->bDiscriminator(btaggerString_) );
      
      // For now, we only care if we have 2 tags...any more are treated the same - maybe we should look at 3 tags?
      if(numTags==2) break;
    }
  histograms["nTags"]->Fill(numTags);
  // Calculate average SecVtx mass and //  
  // fill appropriate histograms.      //
  
  numJets = std::min( (int) jets.size(), 5 );

  string muName = sampleNameInput + Form("_muPt_%dj", numJets);
  
  string htName = sampleNameInput + Form("_hT_%dj", numJets);
  string wmtName = sampleNameInput + Form("_wMT_%dj", numJets);
  string metName = sampleNameInput + Form("_MET_%dj", numJets);
  
  string htName0 = sampleNameInput + Form("_hT_%dj_0t", numJets);
  string wmtName0 = sampleNameInput + Form("_wMT_%dj_0t", numJets);
  string metName0 = sampleNameInput + Form("_MET_%dj_0t", numJets);

  histograms[muName]->Fill( muons[0].pt() );
  histograms[sampleNameInput + Form("_hT")]->Fill( hT );
  histograms[sampleNameInput + Form("_wMT")]->Fill( wMT );
  histograms[sampleNameInput + Form("_MET")]->Fill( met.pt() );
  if ( numJets > 0 ) {
    histograms[htName]->Fill( hT );
    histograms[wmtName]->Fill( wMT );
    histograms[metName]->Fill( met.pt() );
    
    if ( numTags == 0 ) {
      histograms[htName0]->Fill( hT );
      histograms[wmtName0]->Fill( wMT );
      histograms[metName0]->Fill( met.pt() );
    }
    else if( numTags > 0 )
      {
        sumVertexMass /= numTags;
        
        string whichtag = "";
        if( doMC_ ) {
          if (1 == numTags)
            {
              // single tag
              if      (numBottom)              whichtag = "_b";
              else if (numCharm)               whichtag = "_c";
              else if (numLight)               whichtag = "_q";
              else                             whichtag = "_x";
            }
          else
            {
              // double tags
              if      (2 == numBottom)         whichtag = "_bb";
              else if (2 == numCharm)          whichtag = "_cc";
              else if (2 == numLight)          whichtag = "_qq";
              else if (numBottom && numCharm)  whichtag = "_bc";
              else if (numBottom && numLight)  whichtag = "_bq";
              else if (numCharm  && numLight)  whichtag = "_cq";
              else                             whichtag = "_xx";
            } // if two tags
        }
        
        string massName = secvtxname
          + Form("_secvtxMass_%dj_%dt", numJets, numTags);
        string massName_comb = sampleNameInput
          + Form("_secvtxMass_%dj_%dt", numJets, numTags);
        string htName = sampleNameInput + Form("_hT_%dj", numJets);
        //std::cout << massName << std::endl;
        //std::cout << massName_comb << std::endl;
        if(numTags>0 && numJets>0) {
          histograms[massName           ]-> Fill (sumVertexMass);
          if( doMC_ )
            histograms[massName + whichtag]-> Fill (sumVertexMass);
          //So that we can look at all of a sample without worrying about path
          /*        if(massName_comb!=massName) {
                    histograms[massName_comb           ]-> Fill (sumVertexMass);
                    histograms[massName_comb + whichtag]-> Fill (sumVertexMass);
                    }*/
        }
        //  else if (numJets>0)
        //histograms[htName]-> Fill (hTUsingPt);     
      } // end if numTags > 0
  }// end if numJets > 0 
  else
    {
      histograms[sampleNameInput + Form("_hT_0j")]->Fill( hT );
      histograms[sampleNameInput + Form("_wMT_0j")]->Fill( wMT );
      histograms[sampleNameInput + Form("_MET_0j")]->Fill( met.pt() );
      histograms[sampleNameInput + Form("_hT_0j_0t")]->Fill( hT );
      histograms[sampleNameInput + Form("_wMT_0j_0t")]->Fill( wMT );
      histograms[sampleNameInput + Form("_MET_0j_0t")]->Fill( met.pt() );
    }
  if( doMC_ ) {
    //Normalization for "1 tag" events
    for ( ShallowCloneCollection::const_iterator jetBegin = jets.begin(),
        jetEnd = jets.end(), jetIter = jetBegin;
        jetIter != jetEnd; ++jetIter)
    {
      const pat::Jet* jet = dynamic_cast<const pat::Jet *>(jetIter->masterClonePtr().get());

      double jetPt = jet->pt();
      //jetPt range from BTag POG, [30, 400]
      if( jetPt < 30 )    jetPt = 30.5;
      if( jetPt > 400 )	  jetPt = 399.5;
      double jetEta = jet->eta();
      //jetEta range from BTag POG, [-3.0, 3.0]
      if( jetEta < -3.0 )	jetEta = -2.99;
      if( jetEta > 3.0 )	jetEta = 2.99;
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
      double bEff = perfB.getResult( PerformanceResult::BTAGBEFF, p );
      double cEff = perfC.getResult( PerformanceResult::BTAGCEFF, p );
      double lEff = perfL.getResult( PerformanceResult::BTAGLEFF, p );

      // We first get the flavor of the jet so we can fill look at btag efficiency.
      int jetFlavor = std::abs( jet->partonFlavour() );
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
          BinningPointByMap p2;
          p2.insert( BinningVariables::JetEt,  jetPt2 );
          p2.insert( BinningVariables::JetEta, jetEta2 );
          p2.insert( BinningVariables::JetAbsEta,  abs(jetEta2) );

          switch( jetFlavor2 )
          {
            case 5:
              if( !perfB.isResultOk( PerformanceResult::BTAGBEFF, p2 )  )
                std::cout<<"No reasonable result for b effi !"<<std::endl;
              untagRate *= (1.-perfB.getResult( PerformanceResult::BTAGBEFF, p2 ) );
              break;
            case 4:
              if( !perfC.isResultOk( PerformanceResult::BTAGCEFF, p2 )  )
                std::cout<<"No reasonable result for c effi !"<<std::endl;
              untagRate *= (1.-perfC.getResult( PerformanceResult::BTAGCEFF, p2 )  );
              break;
            default:
              if( !perfL.isResultOk( PerformanceResult::BTAGLEFF, p2 )  )
                std::cout<<"No reasonable result for lf effi !"<<std::endl;
              untagRate *= (1.-perfL.getResult( PerformanceResult::BTAGLEFF, p2 ) );
          }
        }
      } // end for jet2Iter
      histograms3d["normalization"]	->  Fill(  numJets,	1,	whichtag,	weight*untagRate );
    } // end for jetIter

    if( numJets < 2 )   return true;
    //Normalization for double tagged events
    for( ShallowCloneCollection::const_iterator jetBegin = jets.begin(), jetEnd = jets.end(),
        jetIter1 = jetBegin;  jetIter1 != jetEnd;  jetIter1 ++ )
      for( ShallowCloneCollection::const_iterator jetIter2 = jetIter1 + 1;  jetIter2 != jetEnd; jetIter2 ++ )
      {
        const pat::Jet* jet1 = dynamic_cast<const pat::Jet *>(jetIter1->masterClonePtr().get());
        const pat::Jet* jet2 = dynamic_cast<const pat::Jet *>(jetIter2->masterClonePtr().get());
        double jetPt1 = jet1->pt();
        double jetPt2 = jet2->pt();
        double jetEta1 = jet1->eta();
        double jetEta2 = jet2->eta();
        if( jetPt1 < 30 )   jetPt1 = 30.5;
        if( jetPt1 > 400 )  jetPt1 = 399.5;
        if( jetPt2 < 30 )   jetPt2 = 30.5;
        if( jetPt2 > 400 )  jetPt2 = 399.5;
        if( jetEta1 < -3.0 )  jetEta1 = -2.99;
        if( jetEta1 > 3.0  )  jetEta1 = 2.99;
        if( jetEta2 < -3.0 )  jetEta2 = -2.99;
        if( jetEta2 > 3.0  )  jetEta2 = 2.99;
        BinningPointByMap p1;
        p1.insert( BinningVariables::JetEt,  jetPt1 );
        p1.insert( BinningVariables::JetEta, jetEta1 );
        p1.insert( BinningVariables::JetAbsEta,  abs(jetEta1) );
        BinningPointByMap p2;
        p2.insert( BinningVariables::JetEt,  jetPt2 );
        p2.insert( BinningVariables::JetEta, jetEta2 );
        p2.insert( BinningVariables::JetAbsEta,  abs(jetEta2) );

        int flavour1 = std::abs( jet1->partonFlavour() );
        int flavour2 = std::abs( jet2->partonFlavour() );
        double weight1 = 1.0;
        double weight2 = 1.0;
        double whichtag = 0;
        //norm the flavour value as follow, b -> 5, c -> 4, l -> 0
        switch( flavour1 )
        {
          case 5:
            if( !perfB.isResultOk( PerformanceResult::BTAGBEFF, p1 )  )
              std::cout<<"No reasonable result for b effi !"<<std::endl;
            weight1 = perfB.getResult( PerformanceResult::BTAGBEFF, p1 );
            break;
          case 4:
            if( !perfC.isResultOk( PerformanceResult::BTAGCEFF, p1 )  )
              std::cout<<"No reasonable result for c effi !"<<std::endl;
            weight1 = perfC.getResult( PerformanceResult::BTAGCEFF, p1 );
            break;
          default:
            if( !perfL.isResultOk( PerformanceResult::BTAGLEFF, p1 ) )
              std::cout<<"No reasonable result for lf effi !"<<std::endl;
            weight1 = perfL.getResult( PerformanceResult::BTAGLEFF, p1 );
            flavour1 = 0;
        }
        switch ( flavour2 )
        {
          case 5:
            if( !perfB.isResultOk( PerformanceResult::BTAGBEFF, p2 )  )
              std::cout<<"No reasonable result for b effi !"<<std::endl;
            weight2 = perfB.getResult( PerformanceResult::BTAGBEFF, p2 );
            break;
          case 4:
            if( !perfC.isResultOk( PerformanceResult::BTAGCEFF, p2 ) )
              std::cout<<"No reasonable result for c effi !"<<std::endl;
            weight2 = perfC.getResult( PerformanceResult::BTAGCEFF, p2 );
            break;
          default:
            if( !perfL.isResultOk( PerformanceResult::BTAGLEFF, p2 )  )
              std::cout<<"No reasonable result for lf effi !"<<std::endl;
            weight2  = perfL.getResult( PerformanceResult::BTAGLEFF, p2 ) ;
            flavour2 = 0;
        }
        int flavourSum = flavour1 + flavour2 ;
        switch( flavourSum )
        {
          case 10:
            //_bb
            whichtag = 10;
            break;
          case 9:
            //_bc
            whichtag = 9;
            break;
          case 8:
            //_cc
            whichtag = 8;
            break;
          case 5:
            //_bq
            whichtag = 5;
            break;
          case 4:
            //_cq
            whichtag = 4;
            break;
          case 0:
            //_qq
            whichtag = 0;
            break;
          default:
            cout<<"Jet Flavour Error: "<<endl;
            return false;
        }
        histograms3d["normalization"]		->  Fill( numJets,  2,  whichtag,  weight1*weight2 );
      }  // end jetIter1, jetIter2
  }
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
  
  if ( useHFcat_ ) histograms["flavorHistory"]-> Fill ( HFcat_ );


  if( !passOneLepton ) return;


  histograms["nJets"]->Fill( jets.size() );
  
  if (anyJets) 
    {
      //Check if the BTagPerformanceRecord exists
      if( es_.exists("BTagPerformanceRecord")  )
        {
          ;//std::cout << "Got the right tree" << std::endl;
        }   else {
        std::cout << "Can't find tree" << std::endl;
      }
      
      recId_ = es_.recordID("BTagPerformanceRecord");
      es_.syncTo( iEvent.id(), edm::Timestamp());
      
      make_templates(jets, met, muons, electrons);
      analyze_met( met );
      if ( muPlusJets_ ) analyze_muons(muons);
      if ( ePlusJets_ ) analyze_electrons(electrons);
      

      unsigned int maxJets = jets.size();
      unsigned int ibjet = 0;
      if ( (int)maxJets >= nJetsCut_ ) {
        if ( maxJets > 4 ) maxJets = 4;
        for ( unsigned int i=0; i<maxJets; ++i) {

          histograms["jet" + boost::lexical_cast<std::string>(i+1) + "Pt"] ->Fill( jets[i].pt()  );
          histograms["jet" + boost::lexical_cast<std::string>(i+1) + "Eta"]->Fill( jets[i].eta() );
          histograms["jet" + boost::lexical_cast<std::string>(i+1) + "Phi"]->Fill( jets[i].phi() );
          histograms["jet" + boost::lexical_cast<std::string>(i+1) + "Mass"]->Fill( jets[i].mass() );
          pat::Jet const * patJet = dynamic_cast<pat::Jet const *>( &* jets[i].masterClonePtr()  );
          if ( doMC_ && patJet != 0 && patJet->genJet() != 0 ) {
            histograms2d["jet" + boost::lexical_cast<std::string>(i+1) + "PtTrueRes"] ->Fill( jets[i].eta(), jets[i].pt() / patJet->genJet()->pt()  );
	    if ( abs(patJet->partonFlavour()) == 5 ) {
	      ++ibjet;
	      histograms2d["jet" + boost::lexical_cast<std::string>(ibjet) + "PtTrueResBJets"] ->Fill( jets[i].eta(), jets[i].pt() / patJet->genJet()->pt()  );
	    }
          }
        }
      } 
      if ( maxJets >= 4 ) {
        //std::cout << iEvent.id().run() << ":" << iEvent.id().event() <<":" << iEvent.id().luminosityBlock() << ":" << std::setprecision(8) << muons[0].pt() << std::endl;
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
    //  5. W+bb with 1 jet from the parton shower (dr == 0.0)
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
  wPlusJets.print(std::cout);
  wPlusJets.printSelectors(std::cout);
}


