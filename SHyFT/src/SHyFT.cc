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
  edm::BasicAnalyzer(iConfig,iDir),
  wPlusJets(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis")),
  theDir(iDir),
  subdirEB( theDir.mkdir("eleEB") ),
  subdirEE( theDir.mkdir("eleEE") ),
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
  weightSFCalc_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<bool>("weightSFCalc")),
  jetAlgo_(iConfig.getParameter<edm::ParameterSet>("shyftAnalysis").getParameter<string>("jetAlgo"))
{
  
   if ( simpleSFCalc_) 
      gRandom->SetSeed( 960622508 );
  

   if ( useCustomPayload_ ) {
      customBtagFile_ = boost::shared_ptr<TFile>( new TFile(customTagRootFile_.c_str(), "READ") );
   }

   //cout <<"let book the histo " << endl;
   //book all the histograms for muons
   if(muPlusJets_) {
      theDir.make<TH1F>("muPt",       "Muon p_{T} (GeV/c) ",   100,    0, 200);
      theDir.make<TH1F>("muEta",      "Muon eta",               50, -3.0, 3.0);
      theDir.make<TH1F>("muNhits",    "Muon N Hits",            35,    0,  35);
      theDir.make<TH1F>("muD0",       "Muon D0",                60, -0.2, 0.2);
      theDir.make<TH1F>("muChi2",     "Muon Chi2",              20,    0,   5);
      theDir.make<TH1F>("muHCalVeto", "Muon hCalVeto",          30,    0,  30);
      theDir.make<TH1F>("muECalVeto", "Muon eCalVeto",          30,    0,  30);
      theDir.make<TH1F>("muTrackIso", "Muon Track Iso",         30,    0,  30);
      theDir.make<TH1F>("muECalIso",  "Muon ECal Iso",          30,    0,  30);
      theDir.make<TH1F>("muHCalIso",  "Muon HCal Iso",          30,    0,  30);
      theDir.make<TH1F>("muRelIso",   "Muon Rel Iso",           30,    0,  30);
   }
  
   // book all the histograms for electrons
   if(ePlusJets_) {
      theDir.make<TH1F>("ePt",       "Electron p_{T} (GeV/c) ", 100,    0, 200);
      theDir.make<TH1F>("eEta",      "Electron eta",             60, -3.0, 3.0);
      theDir.make<TH1F>("ePhi",      "Electron Phi",             50, -3.2, 3.2);
      theDir.make<TH1F>("eD0",       "Electron D0",              60, -0.2, 0.2);
      theDir.make<TH1F>("eTrackIso", "Electron Track Iso",       30,    0,  30);
      theDir.make<TH1F>("eECalIso",  "Electron ECal Iso",        30,    0,  30);
      theDir.make<TH1F>("eHCalIso",  "Electron HCal Iso",        30,    0,  30);
      theDir.make<TH1F>("eRelIso",   "Electron Rel Iso",         30,    0,  30);
      theDir.make<TH1F>("ejetdR_EE", "dR b/w closest jet and electron in EE", 50, 0, 1.0);
      theDir.make<TH1F>("ejetdR_EB", "dR b/w closest jet and electron in EB", 50, 0, 1.0);
      theDir.make<TH1F>("eDelEta_EE",  "#Delta #eta in EE", 36, -0.04, 0.04);
      theDir.make<TH1F>("eDelEta_EB",  "#Delta #eta in EB", 36, -0.04, 0.04);
      theDir.make<TH1F>("eDelPhi_EE",  "#Delta #phi in EE", 50, -0.25, 0.25);
      theDir.make<TH1F>("eDelPhi_EB",  "#Delta #phi in EB", 50, -0.25, 0.25);
      theDir.make<TH1F>("eSigihih_EE", "#sigma_{i#eta i#eta} in EE", 50, 0, 0.05);
      theDir.make<TH1F>("eSigihih_EB", "#sigma_{i#eta i#eta} in EB", 20, 0, 0.02);
      theDir.make<TH1F>("eHoE_EE", "HoE in EE", 30, 0, 0.15);
      theDir.make<TH1F>("eHoE_EB", "HoE in EB", 30, 0, 0.15);  
   }
  
   theDir.make<TH1F>("metPt", "Missing p_{T} (GeV/c)", 100, 0, 200 );
   theDir.make<TH2F>("massVsPt", "Mass vs pt", 25, 0, 250, 25, 0, 500);

   sampleHistName_ = "";
   std::vector<std::string> sampleNameBase;
   std::vector<std::string> sampleName;
   std::vector<std::string> secvtxName(5,"_secvtxMass_");
   secvtxName[0]+="1j_"; secvtxName[1]+="2j_"; secvtxName[2]+="3j_"; secvtxName[3]+="4j_"; secvtxName[4]+="5j_";

   std::vector<std::string> pTName(6,"_elPt_");
   pTName[0]+="0j";pTName[1]+="1j"; pTName[2]+="2j"; pTName[3]+="3j"; pTName[4]+="4j"; pTName[5]+="5j";

   std::vector<std::string> hTName(6,"_hT_");
   hTName[0]+="0j";hTName[1]+="1j"; hTName[2]+="2j"; hTName[3]+="3j"; hTName[4]+="4j"; hTName[5]+="5j";

   std::vector<std::string> METName(6,"_MET_");
   METName[0]+="0j";METName[1]+="1j"; METName[2]+="2j"; METName[3]+="3j"; METName[4]+="4j"; METName[5]+="5j";


   std::vector<std::string> wMTName(6,"_wMT_");
   wMTName[0]+="0j";wMTName[1]+="1j"; wMTName[2]+="2j"; wMTName[3]+="3j"; wMTName[4]+="4j"; wMTName[5]+="5j";

   std::vector<std::string> muEtaName(6,"_muEta_");
   muEtaName[0]+="0j";muEtaName[1]+="1j"; muEtaName[2]+="2j"; muEtaName[3]+="3j"; muEtaName[4]+="4j"; muEtaName[5]+="5j";

   std::vector<std::string> elEtaName(6,"_elEta_");
   elEtaName[0]+="0j";elEtaName[1]+="1j"; elEtaName[2]+="2j"; elEtaName[3]+="3j"; elEtaName[4]+="4j"; elEtaName[5]+="5j";

  
  std::vector<std::string> secvtxEnd;
  std::vector<std::string> muEtaEnd;
  std::vector<std::string> metEnd;

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

    muEtaEnd.push_back("0t_b");  
    muEtaEnd.push_back("0t_c");  
    muEtaEnd.push_back("0t_q");
    muEtaEnd.push_back("0t_x");  
    muEtaEnd.push_back("0t");
    muEtaEnd.push_back("1t_b");  
    muEtaEnd.push_back("1t_c");  
    muEtaEnd.push_back("1t_q");
    muEtaEnd.push_back("1t_x");  
    muEtaEnd.push_back("1t");
    muEtaEnd.push_back("2t_b");  
    muEtaEnd.push_back("2t_c"); 
    muEtaEnd.push_back("2t_q");
    muEtaEnd.push_back("2t_x");
    muEtaEnd.push_back("2t");
    
    metEnd.push_back("0t_b");  
    metEnd.push_back("0t_c");  
    metEnd.push_back("0t_q");
    metEnd.push_back("0t_x");  
    metEnd.push_back("0t");
    metEnd.push_back("1t_b");  
    metEnd.push_back("1t_c");  
    metEnd.push_back("1t_q");
    metEnd.push_back("1t_x");  
    metEnd.push_back("1t");
    metEnd.push_back("2t_b");  
    metEnd.push_back("2t_c"); 
    metEnd.push_back("2t_q");
    metEnd.push_back("2t_x");
    metEnd.push_back("2t");

  }
  else {
    secvtxEnd.push_back("1t"); secvtxEnd.push_back("2t");
    muEtaEnd.push_back("0t"); muEtaEnd.push_back("1t"); muEtaEnd.push_back("2t");
    metEnd.push_back("0t"); metEnd.push_back("1t"); metEnd.push_back("2t");
  }

  

  if(useHFcat_ && ( sampleNameInput=="Vqq" || sampleNameInput=="Wjets" || sampleNameInput=="Wc" || sampleNameInput=="Zjets")) {
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


   theDir.make<TH1F>("nJets",    "N Jets, pt>30, eta<2.4",  15,    0,   15);
   for(unsigned int i=1; i<5; ++i) {
      string jtNum = Form("%d",i);
      theDir.make<TH1F>(("jet"+jtNum+"Pt").c_str(),   ("jet "+jtNum+" leading jet pt").c_str(),     150,    0,  300);
      theDir.make<TH1F>(("jet"+jtNum+"Eta").c_str(),  ("jet "+jtNum+" leading jet eta").c_str(),     50, -3.0,  3.0);
      theDir.make<TH1F>(("jet"+jtNum+"Phi").c_str(),  ("jet "+jtNum+" leading jet phi").c_str(),     60, -3.5,  3.5);
      theDir.make<TH1F>(("jet"+jtNum+"Mass").c_str(), ("jet "+jtNum+" leading jet mass").c_str(),    50,    0,  150);
      if(doMC_) {
	theDir.make<TH2F>(("jet"+jtNum+"PtTrueRes").c_str(),("jet "+jtNum+" leading jet pt / gen pt").c_str(), 25, -5.0, 5.0, 50, 0, 3);
	theDir.make<TH2F>(("jet"+jtNum+"PtTrueResBJets").c_str(),("jet "+jtNum+" leading bjet pt / gen pt").c_str(), 25, -5.0, 5.0, 50, 0, 3);
      }
   }

   if(doMC_) {
     theDir.make<TH1F>("bmass",    "B Sec Vtx Mass",          40,    0,   10);
     theDir.make<TH1F>("cmass",    "C Sec Vtx Mass",          40,    0,   10);
     theDir.make<TH1F>("lfmass",   "LF Sec Vtx Mass",         40,    0,   10);
     theDir.make<TH1F>("flavorHistory", "Flavor History",     12,    0,   12);
      if ( reweightPDF_ )
	theDir.make<TH1F>("pdfWeight", "PDF Weight", 50, 0., 2.0);
   }
   theDir.make<TH1F>("discriminator", "BTag Discriminator", 30,    2,    8);
   theDir.make<TH1F>("nVertices",     "num sec Vertices",    5,    0,    5);
   theDir.make<TH1F>("nTags",     "number of Tags",          3,    0,    3);
  
   theDir.make<TH1F>("m3", "M3 pretag", 60, 0, 600);
   
   for ( int itag = 0; itag <= 2; ++itag ) {
      std::string m3_temp = "m3_" + boost::lexical_cast<std::string>(itag) + "t";
      theDir.make<TH1F>(m3_temp.c_str(), "M3", 60, 0, 600);
   }
  
   TString histTitle;//lep;
   //if(muPlusJets_)     { lep = "mu";}
   //else if(ePlusJets_) { lep = "el";}
   
   for(unsigned int i=0; i<6; ++i) {
      string jtNum = Form("_%dj",i);
      string jt; 
      if(i==0 || i==1) jt = Form("%d Jet", i);
      else if(i>1)     jt = Form("%d Jets", i);

     
      for ( int itag = 0; itag <= 2; ++itag ) {
         
         if(i==0 && itag>0) continue;
         if(i==1 && itag==2) continue;

         //Declare the muon Tag histos
         //---------------------------
         if(muPlusJets_){
            histTitle = "HT (sum Jet Et + mu Pt + MET), "+jt;
            theDir.make<TH1F>( (sampleNameInput+"_hT"+jtNum + "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), histTitle, 120, 0, 1200);
            
            histTitle = "HTlep (sum Jet Et + mu Pt), "+jt;
            theDir.make<TH1F>( (sampleNameInput+"_hT_Lep"+jtNum+ + "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), histTitle, 120, 0, 1200);

            histTitle = "Missing E_{T},  "+jt;
            theDir.make<TH1F>( (sampleNameInput+"_MET"+jtNum+ + "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), histTitle, 120,0,300);

            histTitle = "W Trans Mass, "+jt;
            theDir.make<TH1F>( (sampleNameInput+"_wMT"+jtNum+ + "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), histTitle, 50,0,500);

            theDir.make<TH1F>( (sampleNameInput+"_muPt"+jtNum+ + "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), "muon p_{T}", 100, 0, 200);
            // theDir.make<TH1F>( (sampleNameInput+"_muEta"+jtNum+ + "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), "muon #eta", 120, 0, 2.4);   


            theDir.make<TH2F>( (sampleNameInput+"_muisoVsMuEta"+jtNum+ + "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), "Muon isolation vs Muon Eta, 0-Tag",
                               12, 0., 2.4,
                               20, 0., 1.0
               );

            theDir.make<TH2F>( (sampleNameInput+"_muisoVsHt"+jtNum+ + "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), "Muon isolation vs H_{T}",
                               20., 0., 400,
                               20, 0., 1.0
               );


            theDir.make<TH2F>( (sampleNameInput+"_muisoVsMET"+jtNum+ + "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), "Muon isolation vs MET",
                               20., 0., 200,
                               20, 0., 1.0
               );

            theDir.make<TH2F>( (sampleNameInput+"_muisoVswMT"+jtNum+ + "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), "Muon isolation vs wMT",
                               20., 0., 200,
                               20, 0., 1.0
               );

            theDir.make<TH2F>( (sampleNameInput+"_muisoVsD0"+jtNum+ + "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), "Muon isolation vs D0",
                               100., 0., 0.2,
                               20, 0., 1.0
               );
         }
         //Declare electron Tag histos for EE and EB separately
         //----------------------------------------------------
          else if (ePlusJets_) {
             histTitle = "HT (sum Jet Et + el Pt + MET), "+jt;
             subdirEE.make<TH1F>( (sampleNameInput+"_hT"+jtNum+ "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), histTitle, 120, 0, 1200);
             subdirEB.make<TH1F>( (sampleNameInput+"_hT"+jtNum+ "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), histTitle, 120, 0, 1200);

             //histTitle = "HTlep (sum Jet Et + el Pt), "+jt;
             //subdirEE.make<TH1F>( (sampleNameInput+"_hT_Lep"+jtNum+ "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), histTitle, 120, 0, 1200);
             //subdirEB.make<TH1F>( (sampleNameInput+"_hT_Lep"+jtNum+ "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), histTitle, 120, 0, 1200);

            //histTitle = "Missing E_{T}, "+jt;
            //subdirEE.make<TH1F>( (sampleNameInput+"_MET"+jtNum+ "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), histTitle, 120,0,300);
            //subdirEB.make<TH1F>( (sampleNameInput+"_MET"+jtNum+ "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), histTitle, 120,0,300);

            histTitle = "W Trans Mass, "+jt;
            subdirEE.make<TH1F>( (sampleNameInput+"_wMT"+jtNum+ "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), histTitle, 50,0,500);
            subdirEB.make<TH1F>( (sampleNameInput+"_wMT"+jtNum+ "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), histTitle, 50,0,500);

            subdirEE.make<TH1F>( (sampleNameInput+"_elPt"+jtNum+ "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), "electron p_{T}", 100, 0, 200);
            subdirEB.make<TH1F>( (sampleNameInput+"_elPt"+jtNum+ "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), "electron p_{T}", 100, 0, 200);
            //subdirEE.make<TH1F>( (sampleNameInput+"_elEta"+jtNum+ "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), "electron #eta", 250, -2.5, 2.5);
            //subdirEB.make<TH1F>( (sampleNameInput+"_elEta"+jtNum+ "_" + boost::lexical_cast<std::string>(itag) + "t").c_str(), "electron #eta", 250, -2.5, 2.5);
         }

      } // End loop over itags (0,1,2)

   }
   for (unsigned int j=0;j<sampleName.size();++j) {
     if(useHFcat_){

       for ( int itag = 0; itag <= 2; ++itag ) {
          if(muPlusJets_){
             
             // hT
             for ( unsigned int k=0; k < hTName.size(); ++k ) {
                // Next do the untagged histograms by flavor path
                std::string untemp = sampleName[j]+hTName[k]+ "_" + boost::lexical_cast<std::string>(itag) + "t";
                theDir.make<TH1F>(untemp.c_str(), "hT", 120, 0, 1200);
             }         
             // wMT
             for ( unsigned int k=0; k < wMTName.size(); ++k ) {
                // Next do the untagged histograms by flavor path
                std::string untemp = sampleName[j]+wMTName[k]+ "_" + boost::lexical_cast<std::string>(itag) + "t";
                theDir.make<TH1F>(untemp.c_str(), "wMT", 120, 0,  300);
             }
             
             // MET
             for ( unsigned int k=0; k < METName.size(); ++k ) {
                // Next do the untagged histograms by flavor path
                std::string untemp = sampleName[j]+METName[k]+ "_" + boost::lexical_cast<std::string>(itag) + "t";
                theDir.make<TH1F>(untemp.c_str(), "MET", 120, 0,  300);
             }
             
             //   // muEta
             //   for ( unsigned int k=0; k < muEtaName.size(); ++k ) {
             //     // Next do the untagged histograms by flavor path
             //     std::string untemp = sampleName[j]+muEtaName[k]+ "_" + boost::lexical_cast<std::string>(itag) + "t";
             //     theDir.make<TH1F>(untemp.c_str(), "muEta",  120, 0, 2.4);
             //   }
         }
          
          // else if(ePlusJets_){
             // hT
            //  for ( unsigned int k=0; k < hTName.size(); ++k ) {
//                 if(k==0 && itag>0) continue;
//                 if(k==1 && itag==2) continue;
//                 // Next do the untagged histograms by flavor path
//                 std::string untemp = sampleName[j]+hTName[k]+ "_" + boost::lexical_cast<std::string>(itag) + "t";
//                 subdirEE.make<TH1F>(untemp.c_str(), "hT", 120, 0, 1200);
//                 subdirEB.make<TH1F>(untemp.c_str(), "hT", 120, 0, 1200);
//              }         
//              // wMT
//              for ( unsigned int k=0; k < wMTName.size(); ++k ) {
//                 if(k==0 && itag>0) continue;
//                 if(k==1 && itag==2) continue;
//                 // Next do the untagged histograms by flavor path
//                 std::string untemp = sampleName[j]+wMTName[k]+ "_" + boost::lexical_cast<std::string>(itag) + "t";
//                 subdirEE.make<TH1F>(untemp.c_str(), "wMT", 120, 0,  300);
//                 subdirEB.make<TH1F>(untemp.c_str(), "wMT", 120, 0,  300);
//              }
             // MET
             //for ( unsigned int k=0; k < METName.size(); ++k ) {
             // if(k==0 && itag>0) continue;
             // if(k==1 && itag==2) continue;
             // // Next do the untagged histograms by flavor path
             // std::string untemp = sampleName[j]+METName[k]+ "_" + boost::lexical_cast<std::string>(itag) + "t";
             // subdirEE.make<TH1F>(untemp.c_str(), "MET", 120, 0,  300);
             // subdirEB.make<TH1F>(untemp.c_str(), "MET", 120, 0,  300);
             //}
             
             // }//ePlusJets
       }// end loop over itag (0,1,2)
     }//if HF
     
     if(muPlusJets_){
         // secvtx mass
         for(unsigned int k=0;k<secvtxName.size();++k) {
            for(unsigned int l=0;l<secvtxEnd.size();++l) {
               std::string temp = sampleName[j]+secvtxName[k]+secvtxEnd[l];
               theDir.make<TH1F>(temp.c_str(), "secvtxmass", 40,    0,   10);
               std::string temp2 = sampleName[j]+secvtxName[k]+secvtxEnd[l]+"_vs_iso";
               theDir.make<TH2F>(temp2.c_str(), "secvtxmass", 40,    0,   10,
                                 10, 0., 1.0 );
               if(k==0 && l==4) break;
               else if( (!doMC_) && k==0 && l==0) break;
            }//l
         }//k         
         // mu eta
         for(unsigned int k=0;k<muEtaName.size();++k) {
            for(unsigned int l=0;l<muEtaEnd.size();++l) {
               std::string temp3 = sampleName[j]+ muEtaName[k] +"_"+muEtaEnd[l];
               theDir.make<TH1F>(temp3.c_str(), "Muon eta", 12, 0, 2.4);
               if ( k==0 && l == 4 ) break;   // cut off 0-jet bin after 0-tags
               else if(k==1 && l == 9) break; // cut off 1-jet bin after 1-tags
               else if( (!doMC_) && k==0 && l==0) break; // Data says "You had me at "Hello" ".
               else if( (!doMC_) && k==1 && l==1) break; // 
            }//l
         }//k
      }//muPlusJets
       
       else if(ePlusJets_){
          //secvtxMass
         for(unsigned int k=0;k<secvtxName.size();++k) {
            for(unsigned int l=0;l<secvtxEnd.size();++l) {
               std::string temp = sampleName[j]+secvtxName[k]+secvtxEnd[l];
               subdirEE.make<TH1F>(temp.c_str(), "secvtxmass", 40,    0,   10);
               subdirEB.make<TH1F>(temp.c_str(), "secvtxmass", 40,    0,   10);
               if(k==0 && l==4) break;
               else if( (!doMC_) && k==0 && l==0) break;
            }//l
         }//k
         // el eta
         for(unsigned int k=0;k<elEtaName.size();++k) {
            for(unsigned int l=0;l<muEtaEnd.size();++l) {
               std::string temp3 = sampleName[j]+ elEtaName[k] +"_"+muEtaEnd[l];
               //cout << "Eta Name = " << sampleName[j]+ elEtaName[k] +"_"+muEtaEnd[l] << endl;
               subdirEE.make<TH1F>(temp3.c_str(), "Electron eta", 15, 0.0, 3.0);//---------------------->
               subdirEB.make<TH1F>(temp3.c_str(), "Electron eta", 15, 0.0, 3.0);
               if ( k==0 && l == 4 ) break;   // cut off 0-jet bin after 0-tags
               else if(k==1 && l == 9) break; // cut off 1-jet bin after 1-tags
               else if( (!doMC_) && k==0 && l==0) break; // Data says "You had me at "Hello" ".
               else if( (!doMC_) && k==1 && l==1) break; // 
            }//l
         }//k
         //MET
         for(unsigned int k=0;k<METName.size();++k) {
            for(unsigned int l=0;l<metEnd.size();++l) {
               std::string temp4 = sampleName[j]+ METName[k] +"_"+metEnd[l];
               //cout << "MET Name = " << sampleName[j]+ METName[k] +"_"+metEnd[l] << endl;
               subdirEE.make<TH1F>(temp4.c_str(), "Electron met", 120, 0, 300);//---------------------->
               subdirEB.make<TH1F>(temp4.c_str(), "Electron met", 120, 0, 300);
               if ( k==0 && l == 4 ) break;   // cut off 0-jet bin after 0-tags
               else if(k==1 && l == 9) break; // cut off 1-jet bin after 1-tags
               else if( (!doMC_) && k==0 && l==0) break; // Data says "You had me at "Hello" ".
               else if( (!doMC_) && k==1 && l==1) break; // 
            }//l
         }//k 
/*
         //pT
        for(unsigned int k=0;k<pTName.size();++k) {
            for(unsigned int l=0;l<metEnd.size();++l) {
               std::string temp5 = sampleName[j]+ pTName[k] +"_"+metEnd[l];
               //cout << "Pt Name = " << sampleName[j]+ pTName[k] +"_"+metEnd[l] << endl;
               subdirEE.make<TH1F>(temp5.c_str(), "Electron Pt", 100, 0, 200);//---------------------->
               subdirEB.make<TH1F>(temp5.c_str(), "Electron Pt", 100, 0, 200);
               if ( k==0 && l == 4 ) break;   // cut off 0-jet bin after 0-tags
               else if(k==1 && l == 9) break; // cut off 1-jet bin after 1-tags
               else if( (!doMC_) && k==0 && l==0) break; // Data says "You had me at "Hello" ".
               else if( (!doMC_) && k==1 && l==1) break; // 
            }//l
         }//k 
        //wMT
        for(unsigned int k=0;k<wMTName.size();++k) {
            for(unsigned int l=0;l<metEnd.size();++l) {
               std::string temp6 = sampleName[j]+ wMTName[k] +"_"+metEnd[l];
               //cout << "wMT Name = " << sampleName[j]+ wMTName[k] +"_"+metEnd[l] << endl;
               subdirEE.make<TH1F>(temp6.c_str(), "Electron wMT", 50, 0, 500);//---------------------->
               subdirEB.make<TH1F>(temp6.c_str(), "Electron wMT", 50, 0, 500);
               if ( k==0 && l == 4 ) break;   // cut off 0-jet bin after 0-tags
               else if(k==1 && l == 9) break; // cut off 1-jet bin after 1-tags
               else if( (!doMC_) && k==0 && l==0) break; // Data says "You had me at "Hello" ".
               else if( (!doMC_) && k==1 && l==1) break; // 
            }//l
         }//k 
        //hT
         for(unsigned int k=0;k<hTName.size();++k) {
            for(unsigned int l=0;l<metEnd.size();++l) {
               std::string temp7 = sampleName[j]+ hTName[k] +"_"+metEnd[l];
               //cout << "hT Name = " << sampleName[j]+ hTName[k] +"_"+metEnd[l] << endl;
               subdirEE.make<TH1F>(temp7.c_str(), "Electron hT", 120, 0, 1200);//---------------------->
               subdirEB.make<TH1F>(temp7.c_str(), "Electron hT", 120, 0, 1200);
               if ( k==0 && l == 4 ) break;   // cut off 0-jet bin after 0-tags
               else if(k==1 && l == 9) break; // cut off 1-jet bin after 1-tags
               else if( (!doMC_) && k==0 && l==0) break; // Data says "You had me at "Hello" ".
               else if( (!doMC_) && k==1 && l==1) break; // 
            }//l
         }//k       
*/
      }//ePlusJets

   }//end j sample Name
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
   const pat::Electron * electron_ = dynamic_cast<const pat::Electron*>(electrons[0].masterClonePtr().get());
   if ( electron_ == NULL ) return false;
   double ePt_      = electron_ ->pt();
   double eEta_     = electron_ ->eta();
   double ePhi_     = electron_ ->phi();
   double eD0_      = electron_ ->dB();
   double trackIso_ = electron_ ->dr03TkSumPt();
   double eCalIso_  = electron_ ->dr03EcalRecHitSumEt();
   double hCalIso_  = electron_ ->dr03HcalTowerSumEt();
   double relIso_   = ( trackIso_ + eCalIso_ + hCalIso_ )/ePt_ ;

   double deta_     =  electron_ ->deltaEtaSuperClusterTrackAtVtx();
   double dphi_     =  electron_ ->deltaPhiSuperClusterTrackAtVtx();
   double sihih_    =  electron_ ->sigmaIetaIeta();
   double hoe_      =  electron_ ->hadronicOverEm();
   
   theDir.getObject<TH1>( "ePt"      )->Fill( ePt_        , globalWeight_);
   theDir.getObject<TH1>( "eEta"     )->Fill( eEta_       , globalWeight_);
   theDir.getObject<TH1>( "ePhi"     )->Fill( ePhi_       , globalWeight_);
   theDir.getObject<TH1>( "eD0"      )->Fill( eD0_        , globalWeight_);
   theDir.getObject<TH1>( "eTrackIso")->Fill( trackIso_   , globalWeight_);
   theDir.getObject<TH1>( "eECalIso" )->Fill( eCalIso_    , globalWeight_);
   theDir.getObject<TH1>( "eHCalIso" )->Fill( hCalIso_    , globalWeight_);
   theDir.getObject<TH1>( "eRelIso"  )->Fill( relIso_     , globalWeight_);
  
   if(electron_->isEE()){
      theDir.getObject<TH1>( "eDelEta_EE") ->Fill( deta_     , globalWeight_); 
      theDir.getObject<TH1>( "eDelPhi_EE") ->Fill( dphi_     , globalWeight_);
      theDir.getObject<TH1>( "eSigihih_EE")->Fill( sihih_    , globalWeight_);
      theDir.getObject<TH1>( "eHoE_EE")    ->Fill( hoe_      , globalWeight_);
   }

   else if(electron_->isEB()){
      theDir.getObject<TH1>( "eDelEta_EB") ->Fill( deta_     , globalWeight_); 
      theDir.getObject<TH1>( "eDelPhi_EB") ->Fill( dphi_     , globalWeight_);
      theDir.getObject<TH1>( "eSigihih_EB")->Fill( sihih_    , globalWeight_);
      theDir.getObject<TH1>( "eHoE_EB")    ->Fill( hoe_      , globalWeight_);
   }

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

   theDir.getObject<TH1>( "muPt"      )->Fill( muPt_        , globalWeight_);
   theDir.getObject<TH1>( "muEta"     )->Fill( muEta_       , globalWeight_);
   theDir.getObject<TH1>( "muNhits"   )->Fill( nhits_       , globalWeight_);
   theDir.getObject<TH1>( "muD0"      )->Fill( muD0_        , globalWeight_);
   theDir.getObject<TH1>( "muChi2"    )->Fill( norm_chi2_   , globalWeight_);
   theDir.getObject<TH1>( "muHCalVeto")->Fill( muHCalVeto_  , globalWeight_);
   theDir.getObject<TH1>( "muECalVeto")->Fill( muECalVeto_  , globalWeight_);
   theDir.getObject<TH1>( "muTrackIso")->Fill( trackIso_    , globalWeight_);
   theDir.getObject<TH1>( "muECalIso" )->Fill( eCalIso_     , globalWeight_);
   theDir.getObject<TH1>( "muHCalIso" )->Fill( hCalIso_     , globalWeight_);
   theDir.getObject<TH1>( "muRelIso"  )->Fill( relIso_      , globalWeight_);
  
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

  TH1 * bEff = 0;
  TH1 * cEff = 0;
  TH1 * pEff = 0;
  if ( useCustomPayload_ ) {
    std::string bstr = jetAlgo_ + "BEff";
    std::string cstr = jetAlgo_ + "CEff";
    std::string pstr = jetAlgo_ + "LFEff";

    bEff = (TH1*)customBtagFile_->Get( bstr.c_str() );
    cEff = (TH1*)customBtagFile_->Get( cstr.c_str() );
    pEff = (TH1*)customBtagFile_->Get( pstr.c_str() );        
  }

  // std::cout << "Filling global weight in make_templates : " << globalWeight_ << std::endl;
  reco::Candidate::LorentzVector nu_p4 = met.p4();
  reco::Candidate::LorentzVector lep_p4 = ( muPlusJets_  ? muons[0].p4() : electrons[0].p4() );
  double wPt = lep_p4.Pt() + nu_p4.Pt();
  double wPx = lep_p4.Px() + nu_p4.Px();
  double wPy = lep_p4.Py() + nu_p4.Py();
  double wMT = TMath::Sqrt(wPt*wPt-wPx*wPx-wPy*wPy);
  double hT = lep_p4.pt() + nu_p4.Et();
  double hT_lep = lep_p4.pt();
  double hcalIso(-99.), ecalIso(-99.), trkIso(-99.), pt(-99.), relIso(-99.), d0(-99);
  if(muPlusJets_){
    pat::Muon const * patMuon = dynamic_cast<pat::Muon const *>(&* muons[0].masterClonePtr());
    if ( patMuon == 0 )
      throw cms::Exception("InvalidMuonPointer") << "Muon pointer is invalid you schmuck." << std::endl;
    hcalIso = patMuon->hcalIso();
    ecalIso = patMuon->ecalIso();
    trkIso  = patMuon->trackIso();
    pt      = patMuon->pt() ;
    d0      = fabs(patMuon->dB());  
    relIso = (ecalIso + hcalIso + trkIso) / pt;
  }
  else if(ePlusJets_){
    pat::Electron const * patElectron = dynamic_cast<pat::Electron const *>(&* electrons[0].masterClonePtr());
    if ( patElectron == 0 )
      throw cms::Exception("InvalidElectronPointer") << "Electron pointer is invalid you schmuck." << std::endl;
    hcalIso = patElectron->dr03HcalTowerSumEt();
    ecalIso = patElectron->dr03EcalRecHitSumEt();
    trkIso  = patElectron->dr03TkSumPt();
    pt      = patElectron->pt() ;
    d0      = fabs(patElectron->dB());
    relIso = (ecalIso + hcalIso + trkIso) / pt;
  }
  unsigned int maxJets = jets.size();
  unsigned int ibjet = 0;
  if ( (int)maxJets >= nJetsCut_ ) {
    if ( maxJets > 4 ) maxJets = 4;
    for ( unsigned int i=0; i<maxJets; ++i) {
      theDir.getObject<TH1>( "jet" + boost::lexical_cast<std::string>(i+1) + "Pt") ->Fill( jets[i].pt()  , globalWeight_);
      theDir.getObject<TH1>( "jet" + boost::lexical_cast<std::string>(i+1) + "Eta")->Fill( jets[i].eta() , globalWeight_);
      theDir.getObject<TH1>( "jet" + boost::lexical_cast<std::string>(i+1) + "Phi")->Fill( jets[i].phi() , globalWeight_);
      theDir.getObject<TH1>( "jet" + boost::lexical_cast<std::string>(i+1) + "Mass")->Fill( jets[i].mass() , globalWeight_);
      pat::Jet const * patJet = dynamic_cast<pat::Jet const *>( &* jets[i].masterClonePtr()  );
      if ( doMC_ && patJet != 0 && patJet->genJet() != 0 ) {
	static_cast<TH2*>(theDir.getObject<TH1>( "jet" + boost::lexical_cast<std::string>(i+1) + "PtTrueRes")) ->Fill( jets[i].eta(), jets[i].pt() / patJet->genJet()->pt() , globalWeight_ );
	if ( abs(patJet->partonFlavour()) == 5 ) {
	  ++ibjet;
	  static_cast<TH2*>(theDir.getObject<TH1>( "jet" + boost::lexical_cast<std::string>(ibjet) + "PtTrueResBJets")) ->Fill( jets[i].eta(), jets[i].pt() / patJet->genJet()->pt(), globalWeight_  );
	}
      }
    }
  } 
  
  //SecVtxMass and b-tagging related quantities
  int numBottom=0,numCharm=0,numLight=0;
  int numTags=0, numJets=0;
  // A bit of explanation:
  // The vertex mass is only defined (obviously) for jets with a vertex. So,
  // if we are counting tags from MC, there's no problem. However, if we are reweighting the jets
  // based on the tag efficiencies, there's an issue, because if we set this to "-1", then 
  // there's no way to achieve a correct event counting since "Integral" won't count the underflow
  // bins. Furthermore, the shape is meaningless because lots of jets with mass=-1 will be
  // included in the weighting of the distribution.
  // Thus, we set this to -1 for the straight counting, and 0 for the weighted version.
  // At the end we use the shape from counting but the rates from weighting. 
  double vertexMass = -1.0;
  if ( reweightBTagEff_ )
    vertexMass = 0.0;

  std::vector<double> vertexMasses;
  // --------------
  // Fill the M3 if there are more than 3 jets
  // --------------
  reco::Candidate::LorentzVector p4_m3(0,0,0,0);
  double M3 = 0.0;
  double highestPt = 0.0;
  if ( jets.size() >= 3 ) {

    // std::vector<TVector3> JetEnergy;
    std::vector<TLorentzVector> jets_p4;
    for (unsigned i=0; i< jets.size(); ++i) {
      // JetEnergy.push_back( TVector3( jets[i].px(), jets[i].py(), jets[i].pz() ) );
      jets_p4.push_back( TLorentzVector( jets[i].px(), jets[i].py(), jets[i].pz(), jets[i].energy() ) );
    }
    
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
    theDir.getObject<TH1>( "m3")->Fill( M3, globalWeight_ );
    //std::cout << "m3 here inside >=3 jets " <<M3 << std::endl;
  }
 
  //std::cout << "M3 = " << M3 << std::endl;

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
      
      static_cast<TH2*>(theDir.getObject<TH1>( "massVsPt") )->Fill( jetPt, jet->mass(), globalWeight_ );

           //dR b/w jet and lepton
      if(ePlusJets_){
         pat::Electron const * iElectron = dynamic_cast<pat::Electron const *>(&* electrons[0].masterClonePtr());
         if ( iElectron == 0 )
            throw cms::Exception("InvalidElectronPointer") << "Electron pointer is invalid you schmuck." << std::endl;
         double dR = reco::deltaR( iElectron->eta(), iElectron->phi(), jetIter->eta(), jetIter->phi() );
         if(iElectron->isEE()){
            theDir.getObject<TH1>( "ejetdR_EE")->Fill( dR, globalWeight_ );
         }
         else if(iElectron->isEB()){
            theDir.getObject<TH1>( "ejetdR_EB")->Fill( dR, globalWeight_ );
         }
      }
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
      theDir.getObject<TH1>( "nVertices")-> Fill( svTagInfos->nVertices(), globalWeight_ );
      
      // Check to make sure we have a vertex
      
      if ( svTagInfos->nVertices() <= 0 ) {
	continue;
      }
      
      // This discriminator is only filled when we have a secondary vertex
      // tag info and a vertex in it
      theDir.getObject<TH1>( "discriminator")-> Fill ( jet->bDiscriminator(btaggerString_), globalWeight_ );

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
      double discCut = allDiscrCut_;
      if ( doMC_ ) {
	if ( bDiscrCut_ > 0.0 && jetFlavor == 5 ){ 
	  discCut = bDiscrCut_;
	}
	if ( cDiscrCut_ > 0.0 && jetFlavor == 4 ) { 
	  discCut = cDiscrCut_;
	}
	if ( lDiscrCut_ > 0.0 && jetFlavor!=5 && jetFlavor != 4 ) {
	  discCut = lDiscrCut_;	
	}
      }

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
      



      // copy ( jet->userDataNames().begin(), jet->userDataNames().end(), std::ostream_iterator<std::string>(std::cout, "\n"));

      // if ( jet->hasUserData("secvtxMass") )
	vertexMasses.push_back( jet->userFloat("secvtxMass") );
      // else {
      // 	std::cout << "Yuck... you forgot to add the userData." << std::endl;
      // 	vertexMasses.push_back( svTagInfos->secondaryVertex(0).p4().mass() );
      // }
      
      
      if( jet->bDiscriminator(btaggerString_) < discCut || !keepGoing ) continue;
      ++allNumTags_;
      
      // Take the template info from the first tag (ordered by jet pt)      
      if ( firstTag ) {
	
	// if ( jet->hasUserData("secvtxMass") )
	  vertexMass = jet->userFloat("secvtxMass");
	// else {
	//   std::cout << "Yuck... you forgot to add the userData." << std::endl;
	//   vertexMass = svTagInfos->secondaryVertex(0).p4().mass();
	// }
	
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
	theDir.getObject<TH1>( "bmass")->Fill(vertexMass, globalWeight_);
	break;
      case 4:
	// charm
	theDir.getObject<TH1>( "cmass")->Fill(vertexMass, globalWeight_);
	break;
      default:
	// light flavour
	theDir.getObject<TH1>( "lfmass")->Fill(vertexMass, globalWeight_);
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

  
  theDir.getObject<TH1>( "nTags")->Fill(numTags, globalWeight_);



  if ( !reweightBTagEff_ )  {
    if( numTags > 0 ) {
      string massName  = sampleHistName_ + Form("_secvtxMass_%dj_%dt", numJets, numTags);      
      if ( muPlusJets_ ) {
            theDir.getObject<TH1>(massName             )-> Fill (vertexMass, globalWeight_);
            static_cast<TH2*>(theDir.getObject<TH1>( massName +"_vs_iso"            ))-> Fill (vertexMass, relIso, globalWeight_);
            if( doMC_ ) {
               theDir.getObject<TH1>(massName + whichtag  )-> Fill (vertexMass, globalWeight_);
               static_cast<TH2*>(theDir.getObject<TH1>( massName + whichtag + "_vs_iso"  ))-> Fill (vertexMass, relIso, globalWeight_);
            } // end if doMC
         }//muPlusJets

         else if(ePlusJets_){
            pat::Electron const * patElectron = dynamic_cast<pat::Electron const *>(&* electrons[0].masterClonePtr());
            if ( patElectron == 0 )
               throw cms::Exception("InvalidElectronPointer") << "Electron pointer is invalid you schmuck." << std::endl;
            if(patElectron->isEE()){
               subdirEE.getObject<TH1>(massName)-> Fill (vertexMass, globalWeight_);
               if( doMC_ ) subdirEE.getObject<TH1>(massName + whichtag  )-> Fill (vertexMass, globalWeight_);//end if doMC
            }
            else if(patElectron->isEB()){
               subdirEB.getObject<TH1>(massName)-> Fill (vertexMass, globalWeight_);
               if( doMC_ ) subdirEB.getObject<TH1>(massName + whichtag  )-> Fill (vertexMass, globalWeight_);//end if doMC
            }
         }//ePlusJets

    } // end if numTags > 0    

    if(numJets > 3){
       string m3Name = Form("m3_%dt", numTags);
       theDir.getObject<TH1>( m3Name )->Fill(M3, globalWeight_);
    }
    string muEtaName  = sampleHistName_ + Form("_muEta_%dj_%dt", numJets, numTags);
    if ( muPlusJets_ ) {
       theDir.getObject<TH1>( muEtaName )-> Fill (fabs(muons[0].eta()), globalWeight_);	
       if ( doMC_ ) 
          theDir.getObject<TH1>( muEtaName + whichtag  )-> Fill (fabs(muons[0].eta()), globalWeight_);	
       
       theDir.getObject<TH1>(sampleHistName_ + Form("_hT_%dj_%dt",     numJets, numTags))->Fill( hT,                   globalWeight_ );
       theDir.getObject<TH1>(sampleHistName_ + Form("_wMT_%dj_%dt",    numJets, numTags))->Fill( wMT,                  globalWeight_ );
       theDir.getObject<TH1>(sampleHistName_ + Form("_MET_%dj_%dt",    numJets, numTags))->Fill( met.pt(),             globalWeight_ );       
       static_cast<TH2*>(theDir.getObject<TH1>(sampleNameInput + Form("_muisoVsMuEta_%dj_%dt", numJets, numTags)))->Fill( fabs(muons[0].eta()), relIso, globalWeight_ );
       static_cast<TH2*>(theDir.getObject<TH1>(sampleNameInput + Form("_muisoVsHt_%dj_%dt", numJets, numTags)))->Fill( hT, relIso, globalWeight_ );
       static_cast<TH2*>(theDir.getObject<TH1>(sampleNameInput + Form("_muisoVswMT_%dj_%dt", numJets, numTags)))->Fill( wMT, relIso, globalWeight_ );
       static_cast<TH2*>(theDir.getObject<TH1>(sampleNameInput + Form("_muisoVsMET_%dj_%dt", numJets, numTags)))->Fill( met.pt(), relIso, globalWeight_ );
       static_cast<TH2*>(theDir.getObject<TH1>(sampleNameInput + Form("_muisoVsD0_%dj_%dt", numJets, numTags)))->Fill( d0, relIso, globalWeight_ );
    }
    else if(ePlusJets_){
         pat::Electron const * patElectron = dynamic_cast<pat::Electron const *>(&* electrons[0].masterClonePtr());
         if ( patElectron == 0 )
            throw cms::Exception("InvalidElectronPointer") << "Electron pointer is invalid you schmuck." << std::endl;
         //Fill the EE electrons
         //---------------------
         if(patElectron->isEE()){
            subdirEE.getObject<TH1>(sampleHistName_ + Form("_elEta_%dj_%dt",    numJets, numTags))->Fill( fabs(electrons[0].eta()), globalWeight_); //remove the fabs eta
            //subdirEE.getObject<TH1>(sampleHistName_ + Form("_elPt_%dj_%dt",     numJets, numTags))->Fill( electrons[0].pt(),    globalWeight_ );
            //subdirEE.getObject<TH1>(sampleHistName_ + Form("_hT_%dj_%dt",       numJets, numTags))->Fill( hT,                   globalWeight_ );
            //subdirEE.getObject<TH1>(sampleHistName_ + Form("_wMT_%dj_%dt",      numJets, numTags))->Fill( wMT,                  globalWeight_ );
            subdirEE.getObject<TH1>(sampleHistName_ + Form("_MET_%dj_%dt",      numJets, numTags))->Fill( met.pt(),             globalWeight_ );
            if ( doMC_ ){
               subdirEE.getObject<TH1>( sampleHistName_ + Form("_elEta_%dj_%dt", numJets, numTags) + whichtag  )->Fill( fabs(electrons[0].eta()), globalWeight_); //remove the fabs eta
               //subdirEE.getObject<TH1>( sampleHistName_ + Form("_elPt_%dj_%dt",  numJets, numTags) + whichtag  )->Fill( electrons[0].pt(),    globalWeight_ );
               //subdirEE.getObject<TH1>( sampleHistName_ + Form("_hT_%dj_%dt",    numJets, numTags) + whichtag  )->Fill( hT,                   globalWeight_ );
               //subdirEE.getObject<TH1>( sampleHistName_ + Form("_wMT_%dj_%dt",   numJets, numTags) + whichtag  )->Fill( wMT,                  globalWeight_ );
               subdirEE.getObject<TH1>( sampleHistName_ + Form("_MET_%dj_%dt",   numJets, numTags) + whichtag  )->Fill( met.pt(),             globalWeight_ ); 
            }

            // if(useHFcat_){
               // subdirEE.getObject<TH1>(sampleHistName_ + Form("_hT_%dj_%dt",       numJets, numTags))->Fill( hT,                   globalWeight_ );
               //subdirEE.getObject<TH1>(sampleHistName_ + Form("_wMT_%dj_%dt",      numJets, numTags))->Fill( wMT,                  globalWeight_ );
               //subdirEE.getObject<TH1>(sampleHistName_ + Form("_MET_%dj_%dt",      numJets, numTags))->Fill( met.pt(),             globalWeight_ );
            // }
            subdirEE.getObject<TH1>(sampleNameInput + Form("_hT_%dj_%dt",       numJets, numTags))->Fill( hT,                   globalWeight_ );
            subdirEE.getObject<TH1>(sampleNameInput + Form("_wMT_%dj_%dt",      numJets, numTags))->Fill( wMT,                  globalWeight_ );
            //subdirEE.getObject<TH1>(sampleNameInput + Form("_MET_%dj_%dt",      numJets, numTags))->Fill( met.pt(),             globalWeight_ );
            subdirEE.getObject<TH1>(sampleNameInput + Form("_elPt_%dj_%dt",     numJets, numTags))->Fill( electrons[0].pt(),    globalWeight_ );
         }//is EE
         //Fill the EB electrons
         //---------------------
         else if(patElectron->isEB()){
            subdirEB.getObject<TH1>(sampleHistName_ + Form("_elEta_%dj_%dt",    numJets, numTags))->Fill(fabs(electrons[0].eta()), globalWeight_); //remove the fabs eta
            //subdirEB.getObject<TH1>(sampleHistName_ + Form("_elPt_%dj_%dt",     numJets, numTags))->Fill( electrons[0].pt(),    globalWeight_ );
            //subdirEB.getObject<TH1>(sampleHistName_ + Form("_hT_%dj_%dt",       numJets, numTags))->Fill( hT,                   globalWeight_ );
            //subdirEB.getObject<TH1>(sampleHistName_ + Form("_wMT_%dj_%dt",      numJets, numTags))->Fill( wMT,                  globalWeight_ );
            subdirEB.getObject<TH1>(sampleHistName_ + Form("_MET_%dj_%dt",      numJets, numTags))->Fill( met.pt(),             globalWeight_ );
            if ( doMC_ ){
               subdirEB.getObject<TH1>(sampleHistName_ + Form("_elEta_%dj_%dt", numJets, numTags) + whichtag )->Fill (fabs(electrons[0].eta()), globalWeight_);//remove the fabs eta
               //subdirEB.getObject<TH1>(sampleHistName_ + Form("_elPt_%dj_%dt",  numJets, numTags) + whichtag )->Fill( electrons[0].pt(),    globalWeight_ );
               //subdirEB.getObject<TH1>(sampleHistName_ + Form("_hT_%dj_%dt",    numJets, numTags) + whichtag )->Fill( hT,                   globalWeight_ );
               //subdirEB.getObject<TH1>(sampleHistName_ + Form("_wMT_%dj_%dt",   numJets, numTags) + whichtag )->Fill( wMT,                  globalWeight_ );
               subdirEB.getObject<TH1>(sampleHistName_ + Form("_MET_%dj_%dt",   numJets, numTags) + whichtag )->Fill( met.pt(),             globalWeight_ );
            }

            // if(useHFcat_){
            // subdirEB.getObject<TH1>(sampleHistName_ + Form("_hT_%dj_%dt",       numJets, numTags))->Fill( hT,                   globalWeight_ );
            // subdirEB.getObject<TH1>(sampleHistName_ + Form("_wMT_%dj_%dt",      numJets, numTags))->Fill( wMT,                  globalWeight_ );
               //subdirEB.getObject<TH1>(sampleHistName_ + Form("_MET_%dj_%dt",      numJets, numTags))->Fill( met.pt(),             globalWeight_ );
            //}
            subdirEB.getObject<TH1>(sampleNameInput + Form("_hT_%dj_%dt",       numJets, numTags))->Fill( hT,                   globalWeight_ );
            subdirEB.getObject<TH1>(sampleNameInput + Form("_wMT_%dj_%dt",      numJets, numTags))->Fill( wMT,                  globalWeight_ );
            //subdirEB.getObject<TH1>(sampleNameInput + Form("_MET_%dj_%dt",      numJets, numTags))->Fill( met.pt(),             globalWeight_ );
            subdirEB.getObject<TH1>(sampleNameInput + Form("_elPt_%dj_%dt",     numJets, numTags))->Fill( electrons[0].pt(),    globalWeight_ );
         }//is EB

      }//ePlusJets
   
  }// end if not reweighting b-tag eff

  else {  // reweighting b-tag eff:

    // std::cout << "Reweighting b-tag eff" << std::endl;
    // Here will be the efficiencies for the jets
    std::vector<shyft::helper::EffInfo> effs;
    // "unity"
    shyft::helper::EffInfo unity( -1, 1.0, 0);

    // Loop over jets, create the efficiency vector to be used in
    // the combinatoric calculations. 
    // std::cout << "Looping over jets" << std::endl;
    for ( ShallowCloneCollection::const_iterator jetBegin = jets.begin(),
	    jetEnd = jets.end(), jetIter = jetBegin;
	  jetIter != jetEnd; ++jetIter)
      {
         //std::cout << "Processing jet " << jetIter - jetBegin << std::endl;
	const pat::Jet* jet = dynamic_cast<const pat::Jet *>(jetIter->masterClonePtr().get());
	// We first get the flavor of the jet so we can fill look at btag efficiency.
	int jetFlavor = std::abs( jet->partonFlavour() );
	double jetPt  = std::abs( jet->pt() );
	double jetEta = std::abs( jet->eta() );


	if ( weightSFCalc_ ) {
	  double isf = 1.0;

	  // Check to see if the actual jet is tagged
	  double discCut = allDiscrCut_;
	  if ( bDiscrCut_ > 0.0 && jetFlavor == 5 ){ 
	    discCut = bDiscrCut_;
	  }
	  if ( cDiscrCut_ > 0.0 && jetFlavor == 4 ) { 
	    discCut = cDiscrCut_;
	  }
	  if ( lDiscrCut_ > 0.0 && jetFlavor!=5 && jetFlavor != 4 ) {
	    discCut = lDiscrCut_;	
	  }
	  
	  
	  if ( jetFlavor == 5 || jetFlavor == 4 ) {
	    isf = bcEffScale_;
	  } else { 
	    isf = lfEffScale_;
	  }

	  bool tagged = jet->bDiscriminator(btaggerString_) >= discCut;
	  if (!tagged )
	    isf = 0.0;

	  effs.push_back( shyft::helper::EffInfo(jetIter - jetBegin, 
						 isf,
						 jetFlavor
						 ) );
	}
	else {
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
	}
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

	int kknumTags = std::min( (int) inumTags, 2 );
	if( kknumTags > 0 ) {
       string massName  = sampleHistName_ + Form("_secvtxMass_%dj_%dt", numJets, kknumTags);      
       if(muPlusJets_){
          // std::cout << "Getting " << massName << std::endl;
          theDir.getObject<TH1>( massName                       )-> Fill (vertexMass, globalWeight_ * iprob);
          static_cast<TH2*>(theDir.getObject<TH1>( massName +"_vs_iso"            ))-> Fill (vertexMass, relIso, globalWeight_ * iprob);
          if( doMC_ ) {	
             // std::cout << "Getting " << massName + whichtag << std::endl;
             theDir.getObject<TH1>(massName + whichtag              )-> Fill (vertexMass, globalWeight_ * iprob);	
             static_cast<TH2*>(theDir.getObject<TH1>( massName + whichtag + "_vs_iso"  ))-> Fill (vertexMass, relIso, globalWeight_ * iprob);
          } // end if doMC
       }
       else if(ePlusJets_){
          pat::Electron const * patElectron = dynamic_cast<pat::Electron const *>(&* electrons[0].masterClonePtr());
          if ( patElectron == 0 )
             throw cms::Exception("InvalidElectronPointer") << "Electron pointer is invalid you schmuck." << std::endl;
          
          if(patElectron->isEE()){
             subdirEE.getObject<TH1>(massName)-> Fill (vertexMass, globalWeight_* iprob);
             if( doMC_ )  subdirEE.getObject<TH1>(massName + whichtag)-> Fill (vertexMass, globalWeight_ * iprob);
          }
          else if(patElectron->isEB()){
             subdirEB.getObject<TH1>(massName)-> Fill (vertexMass, globalWeight_* iprob);
             if( doMC_ )  subdirEB.getObject<TH1>(massName + whichtag)-> Fill (vertexMass, globalWeight_ * iprob);
          }
          
       }//ePlusJets
       
	} // end if kknumTags > 0
    
    if(numJets > 3){
       string m3Name = Form("m3_%dt", kknumTags);
       theDir.getObject<TH1>( m3Name )->Fill(M3, globalWeight_);
    }
	string muEtaName  = sampleHistName_ + Form("_muEta_%dj_%dt", numJets, kknumTags);
	if ( muPlusJets_ ) {
       theDir.getObject<TH1>( muEtaName )-> Fill (fabs(muons[0].eta()), globalWeight_ * iprob);	
       if ( doMC_ ) 
          theDir.getObject<TH1>( muEtaName + whichtag  )-> Fill (fabs(muons[0].eta()), globalWeight_ * iprob);	       
       theDir.getObject<TH1>(sampleHistName_ + Form("_hT_%dj_%dt",     numJets, kknumTags))->Fill( hT,                   globalWeight_ * iprob );
       theDir.getObject<TH1>(sampleHistName_ + Form("_wMT_%dj_%dt",    numJets, kknumTags))->Fill( wMT,                  globalWeight_ * iprob );
       theDir.getObject<TH1>(sampleHistName_ + Form("_MET_%dj_%dt",    numJets, kknumTags))->Fill( met.pt(),             globalWeight_ * iprob );  
       static_cast<TH2*>(theDir.getObject<TH1>(sampleNameInput + Form("_muisoVsMuEta_%dj_%dt", numJets, kknumTags)))->Fill( fabs(muons[0].eta()), relIso, globalWeight_ * iprob );
       static_cast<TH2*>(theDir.getObject<TH1>(sampleNameInput + Form("_muisoVsHt_%dj_%dt", numJets, kknumTags)))->Fill( hT, relIso, globalWeight_ * iprob );
       static_cast<TH2*>(theDir.getObject<TH1>(sampleNameInput + Form("_muisoVswMT_%dj_%dt", numJets, kknumTags)))->Fill( wMT, relIso, globalWeight_ * iprob );
       static_cast<TH2*>(theDir.getObject<TH1>(sampleNameInput + Form("_muisoVsMET_%dj_%dt", numJets, kknumTags)))->Fill( met.pt(), relIso, globalWeight_ * iprob );
       static_cast<TH2*>(theDir.getObject<TH1>(sampleNameInput + Form("_muisoVsD0_%dj_%dt", numJets, kknumTags)))->Fill( d0, relIso, globalWeight_ * iprob );
	}
     
     else if(ePlusJets_){
               pat::Electron const * patElectron = dynamic_cast<pat::Electron const *>(&* electrons[0].masterClonePtr());
               if ( patElectron == 0 )
                  throw cms::Exception("InvalidElectronPointer") << "Electron pointer is invalid you schmuck." << std::endl;
               //Fill the EE electrons
               //---------------------
               if(patElectron->isEE()){
                  subdirEE.getObject<TH1>(sampleHistName_ + Form("_elEta_%dj_%dt",    numJets, kknumTags))-> Fill (fabs(electrons[0].eta()), globalWeight_ * iprob); //remove the fabs eta
                  //subdirEE.getObject<TH1>(sampleHistName_ + Form("_elPt_%dj_%dt",     numJets, kknumTags))->Fill( electrons[0].pt(),    globalWeight_ * iprob);
                  //subdirEE.getObject<TH1>(sampleHistName_ + Form("_hT_%dj_%dt",       numJets, kknumTags))->Fill( hT,                   globalWeight_ * iprob);
                  //subdirEE.getObject<TH1>(sampleHistName_ + Form("_wMT_%dj_%dt",      numJets, kknumTags))->Fill( wMT,                  globalWeight_ * iprob);
                  subdirEE.getObject<TH1>(sampleHistName_ + Form("_MET_%dj_%dt",      numJets, kknumTags))->Fill( met.pt(),             globalWeight_ * iprob);
                  if ( doMC_ ){
                     subdirEE.getObject<TH1>(sampleHistName_ + Form("_elEta_%dj_%dt",    numJets, kknumTags) + whichtag  )->Fill (fabs(electrons[0].eta()), globalWeight_ * iprob); //remove the fabs eta
                     //subdirEE.getObject<TH1>(sampleHistName_ + Form("_elPt_%dj_%dt",     numJets, kknumTags) + whichtag  )->Fill( electrons[0].pt(),    globalWeight_ * iprob);
                     //subdirEE.getObject<TH1>(sampleHistName_ + Form("_hT_%dj_%dt",       numJets, kknumTags) + whichtag  )->Fill( hT,                   globalWeight_ * iprob);
                     //subdirEE.getObject<TH1>(sampleHistName_ + Form("_wMT_%dj_%dt",      numJets, kknumTags) + whichtag  )->Fill( wMT,                  globalWeight_ * iprob);
                     subdirEE.getObject<TH1>(sampleHistName_ + Form("_MET_%dj_%dt",      numJets, kknumTags) + whichtag  )->Fill( met.pt(),             globalWeight_ * iprob);      
                  }

                  // if(useHFcat_){
                  //   subdirEE.getObject<TH1>(sampleHistName_ + Form("_hT_%dj_%dt",       numJets, numTags))->Fill( hT,                   globalWeight_ * iprob);
                  //   subdirEE.getObject<TH1>(sampleHistName_ + Form("_wMT_%dj_%dt",      numJets, numTags))->Fill( wMT,                  globalWeight_ * iprob);
                     //subdirEE.getObject<TH1>(sampleHistName_ + Form("_MET_%dj_%dt",      numJets, kknumTags))->Fill( met.pt(),             globalWeight_ * iprob);
                  //}
                  subdirEE.getObject<TH1>(sampleNameInput + Form("_hT_%dj_%dt",       numJets, kknumTags))->Fill( hT,                   globalWeight_ * iprob);
                  subdirEE.getObject<TH1>(sampleNameInput + Form("_wMT_%dj_%dt",      numJets, kknumTags))->Fill( wMT,                  globalWeight_ * iprob);
                  //subdirEE.getObject<TH1>(sampleNameInput + Form("_MET_%dj_%dt",      numJets, kknumTags))->Fill( met.pt(),             globalWeight_ * iprob);
                  subdirEE.getObject<TH1>(sampleNameInput + Form("_elPt_%dj_%dt",     numJets, kknumTags))->Fill( electrons[0].pt(),    globalWeight_ * iprob);
                  
               }//EE
               //Fill the EB electrons
               //---------------------
               else if(patElectron->isEB()){
                  subdirEB.getObject<TH1>(sampleHistName_ + Form("_elEta_%dj_%dt",   numJets, kknumTags))->Fill (fabs(electrons[0].eta()), globalWeight_ * iprob);//remove the fabs eta
                  //subdirEB.getObject<TH1>(sampleHistName_ + Form("_elPt_%dj_%dt",    numJets, kknumTags))->Fill ( electrons[0].pt(),    globalWeight_ * iprob);
                  //subdirEB.getObject<TH1>(sampleHistName_ + Form("_hT_%dj_%dt",      numJets, kknumTags))->Fill ( hT,                   globalWeight_ * iprob);
                  //subdirEB.getObject<TH1>(sampleHistName_ + Form("_wMT_%dj_%dt",     numJets, kknumTags))->Fill ( wMT,                  globalWeight_ * iprob);                  
                  subdirEB.getObject<TH1>(sampleHistName_ + Form("_MET_%dj_%dt",     numJets, kknumTags))->Fill ( met.pt(),             globalWeight_ * iprob);
                  if ( doMC_ ){
                     subdirEB.getObject<TH1>(sampleHistName_ + Form("_elEta_%dj_%dt",  numJets, kknumTags) + whichtag  )->Fill (fabs(electrons[0].eta()), globalWeight_ * iprob); //remove the fabs eta
                     //subdirEB.getObject<TH1>(sampleHistName_ + Form("_elPt_%dj_%dt",   numJets, kknumTags) + whichtag  )->Fill( electrons[0].pt(),    globalWeight_ * iprob);
                     //subdirEB.getObject<TH1>(sampleHistName_ + Form("_hT_%dj_%dt",     numJets, kknumTags) + whichtag  )->Fill( hT,                   globalWeight_ * iprob);
                     //subdirEB.getObject<TH1>(sampleHistName_ + Form("_wMT_%dj_%dt",    numJets, kknumTags) + whichtag  )->Fill( wMT,                  globalWeight_ * iprob);
                     subdirEB.getObject<TH1>(sampleHistName_ + Form("_MET_%dj_%dt",    numJets, kknumTags) + whichtag  )->Fill( met.pt(),             globalWeight_ * iprob);
                  }

                  //if(useHFcat_){
                  // subdirEB.getObject<TH1>(sampleHistName_ + Form("_hT_%dj_%dt",       numJets, kknumTags))->Fill( hT,                   globalWeight_ * iprob);
                  //  subdirEB.getObject<TH1>(sampleHistName_ + Form("_wMT_%dj_%dt",      numJets, kknumTags))->Fill( wMT,                  globalWeight_ * iprob);
                     //subdirEB.getObject<TH1>(sampleHistName_ + Form("_MET_%dj_%dt",      numJets, kknumTags))->Fill( met.pt(),             globalWeight_ * iprob);
                  //}
                  subdirEB.getObject<TH1>(sampleNameInput + Form("_hT_%dj_%dt",       numJets, kknumTags))->Fill( hT,                   globalWeight_ * iprob);
                  subdirEB.getObject<TH1>(sampleNameInput + Form("_wMT_%dj_%dt",      numJets, kknumTags))->Fill( wMT,                  globalWeight_ * iprob);
                  //subdirEB.getObject<TH1>(sampleNameInput + Form("_MET_%dj_%dt",      numJets, kknumTags))->Fill( met.pt(),             globalWeight_ * iprob);
                  subdirEB.getObject<TH1>(sampleNameInput + Form("_elPt_%dj_%dt",     numJets, kknumTags))->Fill( electrons[0].pt(),    globalWeight_ * iprob);
               }//is EB

            }//ePlusJets

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
  theDir.getObject<TH1>( "metPt")->Fill( met.pt(), globalWeight_ );
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
  // bit_  = "Z Veto";
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
  //cout << passPre << endl;
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
    if ( useHFcat_ ) theDir.getObject<TH1>( "flavorHistory")-> Fill ( *heavyFlavorCategory, globalWeight_ );
  }

  sampleHistName_ = sampleNameInput + calcSampleName(iEvent);

  //cout << "sampleHistName_ = "<< sampleHistName_  << endl; 
 
  if (passPre) 
    {
      theDir.getObject<TH1>( "nJets")->Fill( jets.size(), globalWeight_ );
      if(useHFcat_ && sampleHistName_ == sampleNameInput) return;
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
     stringstream tmpString;
     tmpString.str("");
     tmpString << HFcat_;
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
            sampleName += "Z_path";           
            sampleName+=tmpString.str();
            break;
         }
         else if (gpIter->status() == 3 && std::abs(gpIter->pdgId()) == 24)
         {
            sampleName += "W_path";
            sampleName+=tmpString.str();
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
     // sampleName+="_path";
     //stringstream tmpString;
     //tmpString.str("");
     //tmpString << *heavyFlavorCategory;
     //sampleName+=tmpString.str();
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
  // double pdf1 = pdfstuff->pdf()->xPDF.first;
  // double pdf2 = pdfstuff->pdf()->xPDF.second;  

  LHAPDF::usePDFMember(1,0);
  double xpdf1 = LHAPDF::xfx(1, x1, Q, id1);
  double xpdf2 = LHAPDF::xfx(1, x2, Q, id2);
  double w0 = xpdf1 * xpdf2;

  for(int i=1; i <=44; ++i){
    LHAPDF::usePDFMember(1,i);
    double xpdf1_new = LHAPDF::xfx(1, x1, Q, id1);
    double xpdf2_new = LHAPDF::xfx(1, x2, Q, id2);
    double weight = xpdf1_new * xpdf2_new / w0;
    iWeightSum += weight*weight;
  }


  iWeightSum = TMath::Sqrt(iWeightSum) ;

  // char buff[1000];
  // sprintf(buff, "Q = %6.2f, id1 = %4d, id2 = %4d, x1 = %6.2f, x2 = %6.2f, pdf1 = %6.2f, pdf2 = %6.2f",
  // 	  Q, id1, id2, x1, x2, pdf1, pdf2
  // 	  );
  // std::cout << buff << std::endl;
  // sprintf(buff, "  New :  pdf1 = %6.2f, pdf2 = %6.2f, prod=%6.2f",
  // 	  newpdf1, newpdf2, prod
  // 	  );
  // std::cout << buff << std::endl;
  



    
  globalWeight_ *= iWeightSum ;
  // std::cout << "Global weight = " << globalWeight_ << std::endl;
  theDir.getObject<TH1>( "pdfWeight")->Fill( globalWeight_ );

}

