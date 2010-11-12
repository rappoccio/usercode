#include "Analysis/BoostedTopAnalysis/interface/HadronicAnalysis.h"

using namespace std;


HadronicAnalysis::HadronicAnalysis(const edm::ParameterSet& iConfig, TFileDirectory& iDir) :
  plotTracks_(false),
  histoWeight_(1.0),
  weightHist_(0),
  hadronicSelection_(iConfig.getParameter<edm::ParameterSet>("hadronicAnalysis")),
  theDir(iDir),
  boostedTopWTagFunctor_ (iConfig.getParameter<edm::ParameterSet>("hadronicAnalysis").getParameter<edm::ParameterSet>("boostedTopWTagParams") ),
  jetPtMin_ ( iConfig.getParameter<edm::ParameterSet>("hadronicAnalysis").getParameter<edm::ParameterSet>("dijetSelectorParams").getParameter<double>("ptMin") ),
  wMinMass_ ( iConfig.getParameter<edm::ParameterSet>("hadronicAnalysis").getParameter<double>("wMinMass") ),
  wMaxMass_ ( iConfig.getParameter<edm::ParameterSet>("hadronicAnalysis").getParameter<double>("wMaxMass") ),
  mu_(iConfig.getParameter<edm::ParameterSet>("hadronicAnalysis").getParameter<edm::ParameterSet>("boostedTopWTagParams").getParameter<double>("muMax") ),
  y_(iConfig.getParameter<edm::ParameterSet>("hadronicAnalysis").getParameter<edm::ParameterSet>("boostedTopWTagParams").getParameter<double>("ycut") ),
  bTagMedium_ ( iConfig.getParameter<edm::ParameterSet>("hadronicAnalysis").getParameter<double>("bTagOPMedium") ),
  bTagLoose_  ( iConfig.getParameter<edm::ParameterSet>("hadronicAnalysis").getParameter<double>("bTagOPLoose") ),
  eventCount_ (0),
  mistagFileName_ ( iConfig.getParameter<edm::ParameterSet>("hadronicAnalysis").getParameter<std::string>("mistagFileName")  )
{
  std::cout << "Instantiated HadronicAnalysis" << std::endl;

  if ( iConfig.exists("plotOptions") ) {
    edm::ParameterSet const & plotOptions = iConfig.getParameter<edm::ParameterSet>("plotOptions");
    if ( plotOptions.exists("plotTracks") ) {
      std::cout << "HadronicAnalysis: Plotting Tracks" << std::endl;
      plotTracks_ = plotOptions.getParameter<bool>("plotTracks");
    }
    
    if ( plotOptions.exists("reweightHistoFile") && plotOptions.exists("reweightHistoName") ) {
      std::cout << "HadronicAnalysis: Getting reweighting histogram" << std::endl;
      std::string const & reweightHistoFile = plotOptions.getParameter<std::string>("reweightHistoFile");
      std::string const & reweightHistoName = plotOptions.getParameter<std::string>("reweightHistoName");

      TFile * f1 = TFile::Open(reweightHistoFile.c_str());
      weightHist_ = (TH1F*)f1->Get(reweightHistoName.c_str());
      weightHist_->SetName("weightHist");
    } else {
      weightHist_ = 0;
    }
  }

  if ( plotTracks_ ) {
    histograms1d["nTracks"] = theDir.make<TH1F>("nTracks", "Number of Tracks", 400, 0, 400 );
  }

  histograms1d["dijetMass"] = theDir.make<TH1F>("dijetMass", "Dijet Mass", 500, 0, 5000);
  histograms1d["dijetMassSingleTagged"] = theDir.make<TH1F>("dijetMassSingleTagged", "Dijet Mass, Single Tagged", 500, 0, 5000);
  histograms1d["dijetMassDoubleTagged"] = theDir.make<TH1F>("dijetMassDoubleTagged", "Dijet Mass, Double Tagged", 500, 0, 5000);

  histograms1d["jetPt0"] = theDir.make<TH1F>("jetPt0", "Jet p_{T} of First Jet", 50, 0, 500 );
  histograms1d["jetPt1"] = theDir.make<TH1F>("jetPt1", "Jet p_{T} of Second Jet", 50, 0, 500 );

  histograms1d["jetEta0"] = theDir.make<TH1F>("jetEta0", "Jet #eta of First Jet", 50, -5.0, 5.0 );
  histograms1d["jetEta1"] = theDir.make<TH1F>("jetEta1", "Jet #eta of Second Jet", 50, -5.0, 5.0 );

  histograms1d["jetPt0_G"] = theDir.make<TH1F>("jetPt0_G", "Jet p_{T} of First Jet", 50, 0, 500 );
  histograms1d["jetPt1_G"] = theDir.make<TH1F>("jetPt1_G", "Jet p_{T} of Second Jet", 50, 0, 500 );

  histograms1d["jetEta0_G"] = theDir.make<TH1F>("jetEta0_G", "Jet #eta of First Jet", 50, -5.0, 5.0 );
  histograms1d["jetEta1_G"] = theDir.make<TH1F>("jetEta1_G", "Jet #eta of Second Jet", 50, -5.0, 5.0 );


  histograms1d["jetPt0_UDS"] = theDir.make<TH1F>("jetPt0_UDS", "Jet p_{T} of First Jet", 50, 0, 500 );
  histograms1d["jetPt1_UDS"] = theDir.make<TH1F>("jetPt1_UDS", "Jet p_{T} of Second Jet", 50, 0, 500 );

  histograms1d["jetEta0_UDS"] = theDir.make<TH1F>("jetEta0_UDS", "Jet #eta of First Jet", 50, -5.0, 5.0 );
  histograms1d["jetEta1_UDS"] = theDir.make<TH1F>("jetEta1_UDS", "Jet #eta of Second Jet", 50, -5.0, 5.0 );


  histograms1d["jetPt0_BC"] = theDir.make<TH1F>("jetPt0_BC", "Jet p_{T} of First Jet", 50, 0, 500 );
  histograms1d["jetPt1_BC"] = theDir.make<TH1F>("jetPt1_BC", "Jet p_{T} of Second Jet", 50, 0, 500 );

  histograms1d["jetEta0_BC"] = theDir.make<TH1F>("jetEta0_BC", "Jet #eta of First Jet", 50, -5.0, 5.0 );
  histograms1d["jetEta1_BC"] = theDir.make<TH1F>("jetEta1_BC", "Jet #eta of Second Jet", 50, -5.0, 5.0 );


  histograms1d["jetMass0"] = theDir.make<TH1F>("jetMass0", "Jet Mass of First Jet", 100, 0, 500 );
  histograms1d["jetMass1"] = theDir.make<TH1F>("jetMass1", "Jet Mass of Second Jet", 100, 0, 500 );
  histograms1d["jetMass0_0"]  = theDir.make<TH1F>("jetMass0_0",   "Jet Mass of First Jet", 100, 0, 500 );
  histograms1d["jetMass1_0"]  = theDir.make<TH1F>("jetMass1_0",   "Jet Mass of Second Jet", 100, 0, 500 );
  histograms2d["jetMassVsMu0"]  = theDir.make<TH2F>("jetMassVsMu0", "Jet Mass Vs #mu First Jet; #mu; Jet Mass (GeV/c^{2})",
      500, 0.0,  1.0,  100,   0,    500 );
  histograms2d["jetMassVsMu1"]  = theDir.make<TH2F>("jetMassVsMu1", "Jet Mass Vs #mu Second Jet; #mu; Jet Mass (GeV/c^{2})",
      500, 0.0,  1.0,  100,   0,    500 );
  histograms1d["mu0"]     = theDir.make<TH1F>("mu0", "Mass Drop of First Jet", 500, -1.0, 1.0 );
  histograms1d["mu1"]     = theDir.make<TH1F>("mu1", "Mass Drop of Second Jet", 500, -1.0, 1.0 );
  histograms1d["y0"]     = theDir.make<TH1F>("y0", "Asymmetry of First Jet", 500, -1.0, 1.0 );
  histograms1d["y1"]     = theDir.make<TH1F>("y1", "Asymmetry of Second Jet", 500, -1.0, 1.0 );
  histograms1d["y0_0"]   = theDir.make<TH1F>("y0_0",  "Asymmetry of First Jet", 500, -1.0, 1.0 );
  histograms1d["y1_0"]   = theDir.make<TH1F>("y1_0",  "Asymmetry of Second Jet", 500, -1.0, 1.0 );
  histograms1d["dR0"]     = theDir.make<TH1F>("dR0", "#Delta R of First Jet", 500, -1.0, 6.0 );
  histograms1d["dR1"]     = theDir.make<TH1F>("dR1", "#Delta R of Second Jet", 500, -1.0, 6.0 );
  histograms1d["dR0_0"]     = theDir.make<TH1F>("dR0_0", "#Delta R of First Jet", 500, -1.0, 6.0 );
  histograms1d["dR1_0"]     = theDir.make<TH1F>("dR1_0", "#Delta R of Second Jet", 500, -1.0, 6.0 );
  histograms1d["nDaughters0"]  = theDir.make<TH1F>("nDaughters0", "Number of Daughters of First Jet",  5, 0,  5 );
  histograms1d["nDaughters1"]  = theDir.make<TH1F>("nDaughters1", "Number of Daughters of Second Jet",  5, 0,  5 );
  histograms1d["jetsDPhi"]      = theDir.make<TH1F>("jetDPhi",     "DiJet #Delta #phi",    500,    0,    4 );

  histograms1d["jetMass0_G"] = theDir.make<TH1F>("jetMass0_G", "Jet Mass of First Jet", 500, 0, 250 );
  histograms1d["jetMass1_G"] = theDir.make<TH1F>("jetMass1_G", "Jet Mass of Second Jet", 500, 0, 250 );
  histograms1d["mu0_G"]     = theDir.make<TH1F>("mu0_G", "Mass Drop of First Jet", 500, 0.0, 1.0 );
  histograms1d["mu1_G"]     = theDir.make<TH1F>("mu1_G", "Mass Drop of Second Jet", 500, 0.0, 1.0 );
  histograms1d["y0_G"]     = theDir.make<TH1F>("y0_G", "Asymmetry of First Jet", 500, 0.0, 1.0 );
  histograms1d["y1_G"]     = theDir.make<TH1F>("y1_G", "Asymmetry of Second Jet", 500, 0.0, 1.0 );
  histograms1d["dR0_G"]     = theDir.make<TH1F>("dR0_G", "#Delta R of First Jet", 500, 0.0, 1.0 );
  histograms1d["dR1_G"]     = theDir.make<TH1F>("dR1_G", "#Delta R of Second Jet", 500, 0.0, 1.0 );

  histograms1d["jetMass0_UDS"] = theDir.make<TH1F>("jetMass0_UDS", "Jet Mass of First Jet", 500, 0, 250 );
  histograms1d["jetMass1_UDS"] = theDir.make<TH1F>("jetMass1_UDS", "Jet Mass of Second Jet", 500, 0, 250 );
  histograms1d["mu0_UDS"]     = theDir.make<TH1F>("mu0_UDS", "Mass Drop of First Jet", 500, 0.0, 1.0 );
  histograms1d["mu1_UDS"]     = theDir.make<TH1F>("mu1_UDS", "Mass Drop of Second Jet", 500, 0.0, 1.0 );
  histograms1d["y0_UDS"]     = theDir.make<TH1F>("y0_UDS", "Asymmetry of First Jet", 500, 0.0, 1.0 );
  histograms1d["y1_UDS"]     = theDir.make<TH1F>("y1_UDS", "Asymmetry of Second Jet", 500, 0.0, 1.0 );
  histograms1d["dR0_UDS"]     = theDir.make<TH1F>("dR0_UDS", "#Delta R of First Jet", 500, 0.0, 1.0 );
  histograms1d["dR1_UDS"]     = theDir.make<TH1F>("dR1_UDS", "#Delta R of Second Jet", 500, 0.0, 1.0 );

  histograms1d["jetMass0_BC"] = theDir.make<TH1F>("jetMass0_BC", "Jet Mass of First Jet", 500, 0, 250 );
  histograms1d["jetMass1_BC"] = theDir.make<TH1F>("jetMass1_BC", "Jet Mass of Second Jet", 500, 0, 250 );
  histograms1d["mu0_BC"]     = theDir.make<TH1F>("mu0_BC", "Mass Drop of First Jet", 500, 0.0, 1.0 );
  histograms1d["mu1_BC"]     = theDir.make<TH1F>("mu1_BC", "Mass Drop of Second Jet", 500, 0.0, 1.0 );
  histograms1d["y0_BC"]     = theDir.make<TH1F>("y0_BC", "Asymmetry of First Jet", 500, 0.0, 1.0 );
  histograms1d["y1_BC"]     = theDir.make<TH1F>("y1_BC", "Asymmetry of Second Jet", 500, 0.0, 1.0 );
  histograms1d["dR0_BC"]     = theDir.make<TH1F>("dR0_BC", "#Delta R of First Jet", 500, 0.0, 1.0 );
  histograms1d["dR1_BC"]     = theDir.make<TH1F>("dR1_BC", "#Delta R of Second Jet", 500, 0.0, 1.0 );

  histograms1d["run"] = theDir.make<TH1F>("run", "Run Number", 135698 - 132440, 132440, 135698 );
  histograms1d["runSelected"] = theDir.make<TH1F>("runSelected", "Run Number, After selection", 135698 - 132440, 132440, 135698 );

  histograms2d["jetMassVsPt0"] = theDir.make<TH2F>("jetMassVsPt0", "First Jet Mass Versus Jet Pt", 100, 0, 500, 50, 0, 250 );
  histograms2d["jetMassVsPt1"] = theDir.make<TH2F>("jetMassVsPt1", "Second Jet Mass Versus Jet Pt", 100, 0, 500, 50, 0, 250 );
  histograms2d["jetMassVsPt"] = theDir.make<TH2F>("jetMassVsPt",  "Jet Mass Vs Jet Pt; Jet Pt (GeV/c); Jet Mass (GeV/c^{2})", 100,  0,  500,  50, 0, 250 );
  histograms2d["muVsPt0"]     = theDir.make<TH2F>("muVsPt0", "Mass Drop of First Jet", 50, 0, 500, 50, 0.0, 1.0 );
  histograms2d["muVsPt1"]     = theDir.make<TH2F>("muVsPt1", "Mass Drop of Second Jet", 50, 0, 500, 50, 0.0, 1.0 );
  histograms2d["yVsPt0"]     = theDir.make<TH2F>("yVsPt0", "Asymmetry of First Jet", 50, 0, 500, 50, 0.0, 1.0 );
  histograms2d["yVsPt1"]     = theDir.make<TH2F>("yVsPt1", "Asymmetry of Second Jet", 50, 0, 500, 50, 0.0, 1.0 );
  histograms2d["dRVsPt0"]     = theDir.make<TH2F>("dRVsPt0", "#Delta R of First Jet", 50, 0, 500, 50, 0.0, 1.0 );
  histograms2d["dRVsPt1"]     = theDir.make<TH2F>("dRVsPt1", "#Delta R of Second Jet", 50, 0, 500, 50, 0.0, 1.0 );

  histograms2d["dRVsPt0_UDS"]	= theDir.make<TH2F>("dRVsPt0_UDS",	"#Delta R of First Jet", 50, 0, 500, 50, 0.0, 1.0 );
  histograms2d["dRVsPt1_UDS"]	= theDir.make<TH2F>("dRVsPt1_UDS",      "#Delta R of Second Jet", 50, 0, 500, 50, 0.0, 1.0 );
  histograms2d["dRVsPt0_BC"]	= theDir.make<TH2F>("dRVsPt0_BC",	"#Delta R of First Jet", 50, 0, 500, 50, 0.0, 1.0 );
  histograms2d["dRVsPt1_BC"]    = theDir.make<TH2F>("dRVsPt1_BC",       "#Delta R of Second Jet", 50, 0, 500, 50, 0.0, 1.0 );
  histograms2d["dRVsPt0_G"]   = theDir.make<TH2F>("dRVsPt0_G",      "#Delta R of First Jet", 50, 0, 500, 50, 0.0, 1.0 );
  histograms2d["dRVsPt1_G"]   = theDir.make<TH2F>("dRVsPt1_G",      "#Delta R of Second Jet", 50, 0, 500, 50, 0.0, 1.0 );

  histograms2d["jetMassVsPt0_UDS"]	=  theDir.make<TH2F>("jetMassVsPt0_UDS",	"First Jet Mass Versus Jet Pt", 50, 0, 500, 50, 0, 250 );
  histograms2d["jetMassVsPt1_UDS"]      =  theDir.make<TH2F>("jetMassVsPt1_UDS",        "Second Jet Mass Versus Jet Pt", 50, 0, 500, 50, 0, 250 );
  histograms2d["jetMassVsPt0_BC"]	=  theDir.make<TH2F>("jetMassVsPt0_BC",		"First Jet Mass Versus Jet Pt", 50, 0, 500, 50, 0, 250 );
  histograms2d["jetMassVsPt1_BC"]	=  theDir.make<TH2F>("jetMassVsPt1_BC",         "Second Jet Mass Versus Jet Pt", 50, 0, 500, 50, 0, 250 );
  histograms2d["jetMassVsPt0_G"]	=  theDir.make<TH2F>("jetMassVsPt0_G",		"First Jet Mass Versus Jet Pt", 50, 0, 500, 50, 0, 250 );
  histograms2d["jetMassVsPt1_G"]	=  theDir.make<TH2F>("jetMassVsPt1_G",		"Second Jet Mass Versus Jet Pt", 50, 0, 500, 50, 0, 250 );

  histograms2d["taggedJetdRVsPt"]	 = theDir.make<TH2F>("taggedJetdRVsPt",	"#Delta R of Tagged Jets",	50, 0, 500, 50, 0.0, 1.0 );
  histograms2d["taggedJetdRVsPt_UDS"]	= theDir.make<TH2F>("taggedJetdRVsPt_UDS", "#Delta R of Tagged UDS Jets", 50, 0, 500, 50, 0.0, 1.0 );
  histograms2d["taggedJetdRVsPt_BC"]   = theDir.make<TH2F>("taggedJetdRVsPt_BC", "#Delta R of Tagged BC Jets", 50, 0, 500, 50, 0.0, 1.0 );
  histograms2d["taggedJetdRVsPt_G"]   = theDir.make<TH2F>("taggedJetdRVsPt_G", "#Delta R of Tagged G Jets", 50, 0, 500, 50, 0.0, 1.0 );

  histograms2d["taggedJetMassVsPt"]	= theDir.make<TH2F>("taggedJetMassVsPt",	"Tagged Jet Mass",	50, 0, 500, 50, 0, 250 );
  histograms2d["taggedJetMassVsPt_UDS"]     = theDir.make<TH2F>("taggedJetMassVsPt_UDS",        "Tagged UDS Jet Mass",      50, 0, 500, 50, 0, 250 );
  histograms2d["taggedJetMassVsPt_BC"]     = theDir.make<TH2F>("taggedJetMassVsPt_BC",        "Tagged BC Jet Mass",      50, 0, 500, 50, 0, 250 );
  histograms2d["taggedJetMassVsPt_G"]     = theDir.make<TH2F>("taggedJetMassVsPt_G",        "Tagged G Jet Mass",      50, 0, 500, 50, 0, 250 );

  histograms2d["antiTagJetdRVsPt"]        = theDir.make<TH2F>("antiTagJetdRVsPt", "#Delta R of Anti-Tagged Jets",      50, 0, 500, 50, 0.0, 1.0 );
  histograms2d["antiTagJetdRVsPt_UDS"]   = theDir.make<TH2F>("antiTagJetdRVsPt_UDS", "#Delta R of Anti-Tagged UDS Jets", 50, 0, 500, 50, 0.0, 1.0 );
  histograms2d["antiTagJetdRVsPt_BC"]   = theDir.make<TH2F>("antiTagJetdRVsPt_BC", "#Delta R of Anti-Tagged BC Jets", 50, 0, 500, 50, 0.0, 1.0 );
  histograms2d["antiTagJetdRVsPt_G"]   = theDir.make<TH2F>("antiTagJetdRVsPt_G", "#Delta R of Anti-Tagged G Jets", 50, 0, 500, 50, 0.0, 1.0 );

  histograms2d["antiTagJetMassVsPt"]     = theDir.make<TH2F>("antiTagJetMassVsPt",        "Anti-Tagged Jet Mass",      50, 0, 500, 50, 0, 250 );
  histograms2d["antiTagJetMassVsPt_UDS"]     = theDir.make<TH2F>("antiTagJetMassVsPt_UDS",        "Anti-Tagged UDS Jet Mass",      50, 0, 500, 50, 0, 250 );
  histograms2d["antiTagJetMassVsPt_BC"]     = theDir.make<TH2F>("antiTagJetMassVsPt_BC",        "Anti-Tagged BC Jet Mass",      50, 0, 500, 50, 0, 250 );
  histograms2d["antiTagJetMassVsPt_G"]     = theDir.make<TH2F>("antiTagJetMassVsPt_G",        "Anti-Tagged G Jet Mass",      50, 0, 500, 50, 0, 250 );

  histograms1d["partonFlavor"]		= theDir.make<TH1F>("partonFlavor",	"Parton Flavor",	100,	-50,	50 );
  histograms1d["genPartonFlavor"]	= theDir.make<TH1F>("genPartonFlavor",	"Gen Parton Flavor",	100,	-50,	50 );

  //Classify events as dijet, three jet, and double tagged events
  histograms1d["eventType"]     =   theDir.make<TH1F>("eventType",    "Type I(Dijet), Type II(2Tags), Type III(3Jets)",   5,  0,  5 );
  histograms1d["thirdJetFlavor"]  =   theDir.make<TH1F> ("thirdJetFlavor",    "Third Jet Flavour",    50,   -25,  25 );
  histograms1d["doubleTagFlavor"] =   theDir.make<TH1F> ("doubleTagFlavor",   "Double Tags Flavour",  50,   -25,  25 );
  histograms2d["thirdJetdRVsPt"]  =   theDir.make<TH2F> ("thirdJetdRVsPt",    "#Delta R of Third Jet",    50,   0,  500,  50, 0.0,  1.0 );
  histograms2d["doubleTagdRVsPt0"] =   theDir.make<TH2F> ("doubleTagdRVsPt0",   "#Delta R of Double Tags",  50,   0,  500,  50, 0.0,  1.0 );
  histograms2d["doubleTagdRVsPt1"] =   theDir.make<TH2F> ("doubleTagdRVsPt1",   "#Delta R of Double Tags",  50,   0,  500,  50, 0.0,  1.0 );
  histograms2d["thirdJetMassVsPt"]  = theDir.make<TH2F> ("thirdJetMassVsPt",  "Third Jet Mass",           50,   0,  500,  50, 0,    250 );
  histograms2d["doubleTagMassVsPt0"] = theDir.make<TH2F> ("doubleTagMassVsPt0", "Double Tags Mass",         50,   0,  500,  50, 0,    250 );
  histograms2d["doubleTagMassVsPt1"] = theDir.make<TH2F> ("doubleTagMassVsPt1", "Double Tags Mass",         50,   0,  500,  50, 0,    250 );

  histograms1d["wTag"]         = theDir.make<TH1F>("wTag", "W Jet Mistag",    200,    0,    1000 );
  histograms1d["wTagOdd"]      = theDir.make<TH1F>("wTagOdd", "W Jet Mistag",    200,    0,    1000 );
  histograms1d["wTagEven"]      = theDir.make<TH1F>("wTagEven", "W Jet Mistag",    200,    0,    1000 );
  histograms1d["bTagMedium"]   = theDir.make<TH1F>("bTagMedium", "B Jet Mistag",    200,    0,    1000 );
  histograms1d["bTagMediumOdd"]= theDir.make<TH1F>("bTagMediumOdd", "B Jet Mistag",    200,    0,    1000 );
  histograms1d["bTagMediumEven"]   = theDir.make<TH1F>("bTagMediumEven", "B Jet Mistag",    200,    0,    1000 );
  histograms1d["bTagLoose"]    = theDir.make<TH1F>("bTagLoose", "B Jet Mistag",    200,    0,    1000 );
  histograms1d["bTagLooseOdd"] = theDir.make<TH1F>("bTagLooseOdd", "B Jet Mistag",    200,    0,    1000 );
  histograms1d["bTagLooseEven"]= theDir.make<TH1F>("bTagLooseEven", "B Jet Mistag",    200,    0,    1000 );
  histograms1d["jetTotal"]     = theDir.make<TH1F>("jetTotal", "jetTotal",    200,    0,    1000 );
  histograms1d["jetTotalOdd"]  = theDir.make<TH1F>("jetTotalOdd", "jetTotal",    200,    0,    1000 );
  histograms1d["jetTotalEven"] = theDir.make<TH1F>("jetTotalEven", "jetTotal",    200,    0,    1000 );
  histograms1d["WjetID_mu"]    = theDir.make<TH1F>("WjetID_mu", "WjetID_mu",  100,    0,    1 );
  histograms1d["WjetID_y"]     = theDir.make<TH1F>("WjetID_y", "WjetID_y",    100,    0,    1 );
  histograms1d["WjetID_mass"]  = theDir.make<TH1F>("WjetID_mass", "WjetID_mass", 200,    40,    110 );
  histograms1d["WjetID_dR"]    = theDir.make<TH1F>("WjetID_dR", "WjetID_dR",  100,    0,  1 );
  histograms2d["WjetID_yVsMu"] = theDir.make<TH2F> ("WjetID_yVsMu", "WjetID_yVsMu", 50,   0,  1,  50, 0,    1 );

  //Some truth info
  histograms1d["WPt"]         = theDir.make<TH1F>("WPt",    "W Jet Pt",     200,  0,    1000 );
  histograms1d["WMass"]       = theDir.make<TH1F>("WMass",  "W Jet Mass",   100,  0,    500 );
  histograms1d["WMass_0"]     = theDir.make<TH1F>("WMass_0",  "W Jet Mass", 100,  0,    500 );
  histograms1d["W_mu"]        = theDir.make<TH1F>("W_mu",   "W Jet Mu",     500,  -1.0, 1.0 );
  histograms1d["W_y"]         = theDir.make<TH1F>("W_y",    "W Jet y",      500,  -1.0, 1.0 );
  histograms1d["W_dR"]        = theDir.make<TH1F>("W_dR",   "W Jet dR",     500,  -1.0, 6.0 );
  histograms1d["W_nD"]        = theDir.make<TH1F>("W_nD",   "W Jet Daughters",  5,  0,  5 );
  histograms1d["jetPartonDr"] = theDir.make<TH1F>("jetPartonDr",  "Jet Parton Dr",  50, 0,  6.0 );
  histograms1d["W_y_0"]         = theDir.make<TH1F>("W_y_0",    "W Jet y",      500,  -1.0, 1.0 );
  histograms1d["W_dR_0"]        = theDir.make<TH1F>("W_dR_0",   "W Jet dR",     500,  -1.0, 6.0 );
  histograms2d["W_jetMassVsPt"] = theDir.make<TH2F>("W_jetMassVsPt",    "Jet Mass Vs Pt; Jet Pt (GeV/c); Jet Mass (GeV/c^{2})",
  100,  0,  500,  50, 0,  250 );
  histograms2d["W_jetMassVsMu"] = theDir.make<TH2F>("W_jetMassVsMu",    "Jet Mass Vs #mu; #mu; Jet Mass (GeV/c^{2})", 
  500,  0,  1.0,  50, 0,  250 );

  //Histograms for closure test
  histograms1d["wTagPtO"]     = theDir.make<TH1F>("wTagPtO",  "W Jet PT",   200,  0,    1000 );
  histograms1d["wTagPtPredO"] = theDir.make<TH1F>("wTagPtPredO",  "W Jet PT",   200,  0,    1000 );
  histograms1d["wTagPtE"]     = theDir.make<TH1F>("wTagPtE",  "W Jet PT",   200,  0,    1000 );
  histograms1d["wTagPtPredE"] = theDir.make<TH1F>("wTagPtPredE",  "W Jet PT",   200,  0,    1000 );
  histograms1d["bTagPtO"]     = theDir.make<TH1F>("bTagPtO",  "b Jet PT",   200,  0,    1000 );
  histograms1d["bTagPtPredO"] = theDir.make<TH1F>("bTagPtPredO",  "b Jet PT",   200,  0,    1000 );
  histograms1d["bTagPtE"]     = theDir.make<TH1F>("bTagPtE",  "b Jet PT",   200,  0,    1000 );
  histograms1d["bTagPtPredE"] = theDir.make<TH1F>("bTagPtPredE",  "b Jet PT",   200,  0,    1000 );

  histograms1d["diWTagPtO"]       = theDir.make<TH1F>("diWTagPtO", "Double W Tag PT",   200,  0,  1000 );
  histograms1d["diWTagPtPredO"]   = theDir.make<TH1F>("diWTagPtPredO", "Double W Tag PT",   200,  0,  1000 );
  histograms1d["diWTagPtE"]       = theDir.make<TH1F>("diWTagPtE", "Double W Tag PT",   200,  0,  1000 );
  histograms1d["diWTagPtPredE"]   = theDir.make<TH1F>("diWTagPtPredE", "Double W Tag PT",   200,  0,  1000 );
  histograms1d["dibTagPtO"]       = theDir.make<TH1F>("dibTagPtO", "Double b Tag PT",   200,  0,  1000 );
  histograms1d["dibTagPtPredO"]   = theDir.make<TH1F>("dibTagPtPredO", "Double b Tag PT",   200,  0,  1000 );
  histograms1d["dibTagPtE"]       = theDir.make<TH1F>("dibTagPtE", "Double b Tag PT",   200,  0,  1000 );
  histograms1d["dibTagPtPredE"]   = theDir.make<TH1F>("dibTagPtPredE", "Double b Tag PT",   200,  0,  1000 );

  edm::Service<edm::RandomNumberGenerator> rng;
  if ( ! rng.isAvailable()) {
    throw cms::Exception("Configuration")
      << "Module requires the RandomNumberGeneratorService\n";
  }

  CLHEP::HepRandomEngine& engine = rng->getEngine();
  flatDistribution_ = new CLHEP::RandFlat(engine, 0., 1.);

  mistagFile_ = TFile::Open( mistagFileName_.c_str() );
  bMistagMO_  = (TH1*)mistagFile_->Get( "bMistagMOdd" );
  bMistagME_  = (TH1*)mistagFile_->Get( "bMistagMEven" );
  wMistagO_   = (TH1*)mistagFile_->Get( "wMistagOdd" );
  wMistagE_   = (TH1*)mistagFile_->Get( "wMistagEven" );

}

void HadronicAnalysis::analyze(const edm::EventBase& iEvent)
{
  histograms1d["run"]->Fill( iEvent.id().run() );

  analyzeWJet( iEvent );
  histoWeight_ = 1.0;
  if ( plotTracks_ ) {
    edm::Handle<std::vector<reco::Track> > h_tracks;
    iEvent.getByLabel( edm::InputTag("generalTracks"), h_tracks ) ;

    int nTracks = h_tracks->size();
    
    histograms1d["nTracks"]->Fill( nTracks, histoWeight_ );
  }

  pat::strbitset ret = hadronicSelection_.getBitTemplate();
  bool pass = hadronicSelection_(iEvent, ret);

  if ( ret[std::string("Jet Preselection")] ) {
    histograms1d["runSelected"]->Fill( iEvent.id().run() );
    std::vector<edm::Ptr<pat::Jet> > const & pretaggedJets = hadronicSelection_.pretaggedJets();

    //Classify three jets event
    if( pretaggedJets.size() >= 3 && pretaggedJets[2]->pt() > 50 ) {
      const pat::Jet & thirdJet = (*pretaggedJets[2]);
      double mu3 = 0.0, y3 = 0.0, dR3 = 0.0;
      pat::subjetHelper( thirdJet, y3, mu3, dR3 );
      histograms1d["eventType"]     ->  Fill(3);
      histograms1d["thirdJetFlavor"]    ->  Fill( thirdJet.partonFlavour() );
      histograms2d["thirdJetdRVsPt"]    ->  Fill( thirdJet.pt(), dR3 );
      histograms2d["thirdJetMassVsPt"]  ->  Fill( thirdJet.pt(),  thirdJet.mass() );
    }
    else if ( pretaggedJets.size() >= 2 ) {
      double dPhi = fabs( reco::deltaPhi<double>( pretaggedJets[0]->phi(), pretaggedJets[1]->phi() ) );
      histograms1d["jetsDPhi"]      ->  Fill( dPhi );
      //cout<<pretaggedJets.size()<<endl;
      double bDiscriminator1  = pretaggedJets[0]->bDiscriminator("trackCountingHighEffBJetTags");
      double bDiscriminator2  = pretaggedJets[1]->bDiscriminator("trackCountingHighEffBJetTags");
      //Classify double tagged events
      bool diBTag = false;
      if( bDiscriminator1 > bTagMedium_ && bDiscriminator2 > bTagMedium_ )  {
        diBTag = true;
        const pat::Jet & tag0 = (*pretaggedJets[0]);
        const pat::Jet & tag1 = (*pretaggedJets[1]);
        double mu0 = 0.0, y0 = 0.0, dR0 = 0.0;
        pat::subjetHelper( tag0, y0, mu0, dR0 );
        double mu1 = 0.0, y1 = 0.0, dR1 = 0.0;
        pat::subjetHelper( tag1, y1, mu1, dR1);
        histograms1d["eventType"]     ->  Fill(2);
        histograms1d["doubleTagFlavor"]   ->  Fill( tag0.partonFlavour() );
        histograms1d["doubleTagFlavor"]   ->  Fill( tag1.partonFlavour() );
        histograms2d["doubleTagdRVsPt0"]  ->  Fill( tag0.pt(),  dR0 );
        histograms2d["doubleTagdRVsPt1"]  ->  Fill( tag1.pt(),  dR1 );
        histograms2d["doubleTagMassVsPt0"]  ->  Fill( tag0.pt(), tag0.mass() );
        histograms2d["doubleTagMassVsPt1"]  ->  Fill( tag1.pt(), tag1.mass() );
      }

      eventCount_ ++;
      reco::Candidate::LorentzVector p4_0( pretaggedJets[0]->p4() );
      reco::Candidate::LorentzVector p4_1( pretaggedJets[1]->p4() );

      reco::Candidate::LorentzVector p4 = p4_0 + p4_1;

      // Derive mis tag rate 
      // todo: simplify the next few lines  
      double x = flatDistribution_->fire();
      //cout<<"Random number is "<<x<<endl;
      int probe_index(0), tag_index(0);
      if( x < 0.5 )  { probe_index = 0; tag_index = 1; }
      else      { probe_index = 1; tag_index = 0; }

      const pat::Jet & probe( *pretaggedJets[probe_index] );
      const pat::Jet & tag( *pretaggedJets[tag_index] );
      //Assuming same binning of all mistag TH1
      int probeBin = wMistagO_-> FindBin( probe.pt() );
      int tagBin   = wMistagO_-> FindBin( tag.pt() );

      histograms1d["jetTotal"]    ->  Fill( probe.pt() );
      pat::strbitset wRet = boostedTopWTagFunctor_.getBitTemplate();
      double theWMass = probe.mass() ;
      double tagMass = tag.mass();
      bool passMass = theWMass > wMinMass_ && theWMass < wMaxMass_ ;
      bool passTagMass = tagMass > wMinMass_ && tagMass < wMaxMass_;
      bool passWCut = boostedTopWTagFunctor_( probe, wRet );
      bool passTagCut = boostedTopWTagFunctor_ ( tag, wRet );
      bool passProbeW = passWCut && passMass;
      bool passTagW = passTagCut && passTagMass ;
      bool diWTag = passTagW && passProbeW ;
      if (passWCut) {
	histograms1d["WjetID_mass"] -> Fill( theWMass );
      }
      if (passWCut && passMass) {
        histograms1d["wTag"]    ->  Fill( probe.pt() );
        double mu(0), y(0),dR(0);
	pat::subjetHelper( probe, y, mu, dR );
        histograms1d["WjetID_mu"] -> Fill( mu );
	histograms1d["WjetID_y"] -> Fill( y );         
	histograms1d["WjetID_dR"] -> Fill( dR );
        histograms2d["WjetID_yVsMu"] -> Fill( y,mu );
      }
      if( probe.bDiscriminator("trackCountingHighEffBJetTags") > bTagLoose_ ) {
        histograms1d["bTagLoose"]     ->  Fill( probe.pt() );
        if( probe.bDiscriminator("trackCountingHighEffBJetTags") > bTagMedium_ ) {
          histograms1d["bTagMedium"]    ->  Fill( probe.pt() );
        }
      }
      //Even events
      if( eventCount_%2 == 0 )  {
        histograms1d["jetTotalEven"]      ->  Fill( probe.pt() );
        double probewWeight = wMistagO_ -> GetBinContent( probeBin );
        double probebWeight = bMistagMO_ -> GetBinContent( probeBin );
        double tagwWeight   = wMistagO_ -> GetBinContent( tagBin );
        double tagbWeight   = bMistagMO_ -> GetBinContent( tagBin );
        histograms1d["wTagPtPredE"]     ->  Fill( probe.pt(), probewWeight );
        histograms1d["bTagPtPredE"]     ->  Fill( probe.pt(), probebWeight );
        histograms1d["diWTagPtPredE"]   ->  Fill( p4.pt(), probewWeight*tagwWeight );
        histograms1d["dibTagPtPredE"]   ->  Fill( p4.pt(), probebWeight*tagbWeight );
        if( passWCut && passMass )  {
          histograms1d["wTagEven"]        ->  Fill( probe.pt() );
          histograms1d["wTagPtE"]       ->  Fill( probe.pt() );
        }
        if( probe.bDiscriminator("trackCountingHighEffBJetTags") > bTagLoose_ ) {
          histograms1d["bTagLooseEven"]   ->  Fill( probe.pt() );
          if( probe.bDiscriminator("trackCountingHighEffBJetTags") > bTagMedium_ ) {
            histograms1d["bTagMediumEven"]    ->  Fill( probe.pt() );
            histograms1d["bTagPtE"]         ->  Fill( probe.pt() );
          }
        }
        if( diBTag )
          histograms1d["dibTagPtE"]     ->  Fill( p4.pt() );
        if( diWTag )
          histograms1d["diWTagPtE"]     ->  Fill( p4.pt() );

      }
      else {  //Odd events
        histograms1d["jetTotalOdd"]      ->  Fill( probe.pt() );
        double probewWeight = wMistagE_ -> GetBinContent( probeBin );
        double probebWeight = bMistagME_ -> GetBinContent( probeBin );
        double tagwWeight   = wMistagE_ -> GetBinContent( tagBin );
        double tagbWeight   = bMistagME_ -> GetBinContent( tagBin );
        histograms1d["wTagPtPredO"]     ->  Fill( probe.pt(), probewWeight );
        histograms1d["bTagPtPredO"]     ->  Fill( probe.pt(), probebWeight );
        histograms1d["diWTagPtPredO"]   ->  Fill( p4.pt(), probewWeight*tagwWeight );
        histograms1d["dibTagPtPredO"]   ->  Fill( p4.pt(), probebWeight*tagbWeight );
        if( passWCut && passMass )  {
          histograms1d["wTagOdd"]        ->  Fill( probe.pt() );
          histograms1d["wTagPtO"]       ->  Fill( probe.pt() );
        }
        if( probe.bDiscriminator("trackCountingHighEffBJetTags") > bTagLoose_ ) {
          histograms1d["bTagLooseOdd"]   ->  Fill( probe.pt() );
          if( probe.bDiscriminator("trackCountingHighEffBJetTags") > bTagMedium_ ) {
            histograms1d["bTagMediumOdd"]    ->  Fill( probe.pt() );
            histograms1d["bTagPtO"]         ->  Fill( probe.pt() );
          }
        }
        if( diBTag )
          histograms1d["dibTagPtO"]     ->  Fill( p4.pt() );
        if( diWTag )
          histograms1d["diWTagPtO"]     ->  Fill( p4.pt() );
      }

      // end derive mis tag rate

      histograms1d["eventType"]     ->  Fill(1);

      double mu0 = 0.0, y0 = 0.0, dR0 = 0.0;
      pat::subjetHelper( *pretaggedJets[0], y0, mu0, dR0);
      double mu1 = 0.0, y1 = 0.0, dR1 = 0.0;
      pat::subjetHelper( *pretaggedJets[1], y1, mu1, dR1);	  

      if ( weightHist_ != 0 ) {
        int ibin = weightHist_->GetXaxis()->FindBin( p4_0.pt() );
        double iweight = weightHist_->GetBinContent(ibin);

        histoWeight_ = iweight;

      }

      //Check leading jet
      pat::strbitset wtagRet = boostedTopWTagFunctor_.getBitTemplate();
      const pat::Jet & theJet = (*pretaggedJets[0]);

      histograms1d["partonFlavor"]	->  Fill( theJet.partonFlavour() );
      if( theJet.genParton() != 0 )
        histograms1d["genPartonFlavor"]	->  Fill( theJet.genParton()->pdgId() );
      else
        histograms1d["genPartonFlavor"]	->  Fill( 0 );

      double mu=0.0, y=0.0, dR=0.0;
      pat::subjetHelper( theJet, y, mu, dR );
      double theMass = theJet.mass();
      bool passMassCut = ( theMass > 50 ) && ( theMass < 100 );
      bool passWJet = passMassCut && boostedTopWTagFunctor_( theJet, wtagRet);
      if( passWJet )  {
        histograms2d["taggedJetMassVsPt"]	->  Fill( theJet.pt(), theJet.mass() ) ;
        histograms2d["taggedJetdRVsPt"]	->  Fill( theJet.pt(), dR );
        if( fabs( theJet.partonFlavour() ) == 21 )  {
          histograms2d["taggedJetdRVsPt_G"]	->  Fill( theJet.pt(), dR );
          histograms2d["taggedJetMassVsPt_G"]	->  Fill( theJet.pt(), theJet.mass() ) ;
        }
        else if( ( fabs( theJet.partonFlavour() ) == 4 || fabs( theJet.partonFlavour() ) == 5 )  )
        {
          histograms2d["taggedJetdRVsPt_BC"]	 ->  Fill( theJet.pt(), dR );
          histograms2d["taggedJetMassVsPt_BC"]	->  Fill( theJet.pt(), theJet.mass() ) ;
        }
        else if( fabs( theJet.partonFlavour() ) < 4 )
        {
          histograms2d["taggedJetdRVsPt_UDS"]     ->  Fill( theJet.pt(), dR );
          histograms2d["taggedJetMassVsPt_UDS"]  ->  Fill( theJet.pt(), theJet.mass() ) ;
        }

      } // end if wtagRet
      else
      {
        histograms2d["antiTagJetMassVsPt"]   ->  Fill( theJet.pt(), theJet.mass() ) ;
        histograms2d["antiTagJetdRVsPt"]     ->  Fill( theJet.pt(), dR );
        if( fabs( theJet.partonFlavour() ) == 21 )  {
          histograms2d["antiTagJetdRVsPt_G"] ->  Fill( theJet.pt(), dR );
          histograms2d["antiTagJetMassVsPt_G"]       ->  Fill( theJet.pt(), theJet.mass() ) ;
        }
        else if( ( fabs( theJet.partonFlavour() ) == 4 || fabs( theJet.partonFlavour() ) == 5 )  )
        {
          histograms2d["antiTagJetdRVsPt_BC"]     ->  Fill( theJet.pt(), dR );
          histograms2d["antiTagJetMassVsPt_BC"]  ->  Fill( theJet.pt(), theJet.mass() ) ;
        }
        else if( fabs( theJet.partonFlavour() ) < 4 )
        {
          histograms2d["antiTagJetdRVsPt_UDS"]     ->  Fill( theJet.pt(), dR );
          histograms2d["antiTagJetMassVsPt_UDS"]  ->  Fill( theJet.pt(), theJet.mass() ) ;
        }

      }  // end else wtagRet


      histograms1d["jetPt0"]->Fill( p4_0.pt(), histoWeight_ );
      histograms1d["jetPt1"]->Fill( p4_1.pt(), histoWeight_ );
      histograms1d["jetEta0"]->Fill( p4_0.eta(), histoWeight_ );
      histograms1d["jetEta1"]->Fill( p4_1.eta(), histoWeight_ );

      histograms1d["dijetMass"]->Fill( p4.mass(), histoWeight_ );
      histograms1d["jetMass0"]->Fill( pretaggedJets[0]->mass() , histoWeight_);
      histograms1d["mu0"]->Fill(mu0, histoWeight_);
      histograms1d["y0"]->Fill(y0, histoWeight_);
      histograms1d["dR0"]->Fill(dR0, histoWeight_);
      histograms2d["jetMassVsPt0"]->Fill( pretaggedJets[0]->pt(), pretaggedJets[0]->mass() , histoWeight_);
      histograms2d["jetMassVsPt"] ->Fill( pretaggedJets[0]->pt(), pretaggedJets[0]->mass() );
      histograms2d["muVsPt0"]->Fill(pretaggedJets[0]->pt(), mu0, histoWeight_);
      histograms2d["yVsPt0"]->Fill(pretaggedJets[0]->pt(), y0, histoWeight_);
      histograms2d["dRVsPt0"]->Fill(pretaggedJets[0]->pt(), dR0, histoWeight_);
      histograms1d["nDaughters0"]   ->  Fill( pretaggedJets[0]->numberOfDaughters() );
      histograms2d["jetMassVsMu0"]  ->  Fill( mu0, pretaggedJets[0]->mass() );
      if( mu0 < mu_ )
        histograms1d["jetMass0_0"]  ->  Fill( pretaggedJets[0]->mass() );
      if( pretaggedJets[0]->mass() > wMinMass_ && mu0 < mu_ )  {
        histograms1d["y0_0"]    ->  Fill( y0 );
        histograms1d["dR0_0"]   ->  Fill( dR0 );
      }

      histograms1d["jetMass1"]->Fill( pretaggedJets[1]->mass() , histoWeight_);
      histograms1d["mu1"]->Fill(mu1, histoWeight_);
      histograms1d["y1"]->Fill(y1, histoWeight_);
      histograms1d["dR1"]->Fill(dR1, histoWeight_);
      histograms2d["jetMassVsPt1"]->Fill( pretaggedJets[1]->pt(), pretaggedJets[1]->mass() , histoWeight_);
      histograms2d["jetMassVsPt"] ->Fill( pretaggedJets[1]->pt(), pretaggedJets[1]->mass() );
      histograms2d["muVsPt1"]->Fill(pretaggedJets[1]->pt(), mu1, histoWeight_);
      histograms2d["yVsPt1"]->Fill(pretaggedJets[1]->pt(), y1, histoWeight_);
      histograms2d["dRVsPt1"]->Fill(pretaggedJets[1]->pt(), dR1, histoWeight_);
      histograms1d["nDaughters1"]   ->  Fill( pretaggedJets[1]->numberOfDaughters() );
      histograms2d["jetMassVsMu1"]  ->  Fill( mu1, pretaggedJets[1]->mass() );
      if( mu1 < mu_ )
        histograms1d["jetMass1_0"]    ->  Fill( pretaggedJets[1]->mass() );
      if( pretaggedJets[1]->mass() > wMinMass_ && mu1 < mu_ )  {
        histograms1d["y1_0"]    ->  Fill( y1 );
        histograms1d["dR1_0"]   ->  Fill( dR1 );
      }

      if ( pretaggedJets[0]->partonFlavour() == 21 ) {
        histograms1d["jetPt0_G"]->Fill( p4_0.pt(), histoWeight_ );
        histograms1d["jetMass0_G"]->Fill( pretaggedJets[0]->mass() , histoWeight_);
        histograms1d["mu0_G"]->Fill(mu0, histoWeight_);
        histograms1d["y0_G"]->Fill(y0, histoWeight_);
        histograms1d["dR0_G"]->Fill(dR0, histoWeight_);
        histograms1d["jetEta0_G"]->Fill( p4_0.eta(), histoWeight_ );
        histograms2d["dRVsPt0_G"]	->  Fill( p4_0.pt(),	dR0, histoWeight_ );
        histograms2d["jetMassVsPt0_G"]	->  Fill( p4_0.pt(),	pretaggedJets[0]->mass() , histoWeight_);

      }

      else if ( fabs(pretaggedJets[0]->partonFlavour()) < 4 ) {
        histograms1d["jetPt0_UDS"]->Fill( p4_0.pt(), histoWeight_ );
        histograms1d["jetMass0_UDS"]->Fill( pretaggedJets[0]->mass() , histoWeight_);
        histograms1d["mu0_UDS"]->Fill(mu0, histoWeight_);
        histograms1d["y0_UDS"]->Fill(y0, histoWeight_);
        histograms1d["dR0_UDS"]->Fill(dR0, histoWeight_);
        histograms1d["jetEta0_UDS"]->Fill( p4_0.eta(), histoWeight_ );
        histograms2d["dRVsPt0_UDS"]       ->  Fill( p4_0.pt(),    dR0, histoWeight_ );
        histograms2d["jetMassVsPt0_UDS"]  ->  Fill( p4_0.pt(),    pretaggedJets[0]->mass() , histoWeight_);

      }

      else if ( (fabs(pretaggedJets[0]->partonFlavour()) == 4 ||
            fabs(pretaggedJets[0]->partonFlavour()) == 5 )
          ) {
        histograms1d["jetPt0_BC"]->Fill( p4_0.pt(), histoWeight_ );
        histograms1d["jetMass0_BC"]->Fill( pretaggedJets[0]->mass() , histoWeight_);
        histograms1d["mu0_BC"]->Fill(mu0, histoWeight_);
        histograms1d["y0_BC"]->Fill(y0, histoWeight_);
        histograms1d["dR0_BC"]->Fill(dR0, histoWeight_);
        histograms1d["jetEta0_BC"]->Fill( p4_0.eta(), histoWeight_ );
        histograms2d["dRVsPt0_BC"]       ->  Fill( p4_0.pt(),    dR0, histoWeight_ );
        histograms2d["jetMassVsPt0_BC"]  ->  Fill( p4_0.pt(),    pretaggedJets[0]->mass() , histoWeight_);

      }

      if ( pretaggedJets[1]->partonFlavour() == 21 ) {
        histograms1d["jetPt1_G"]->Fill( p4_1.pt(), histoWeight_ );
        histograms1d["jetMass1_G"]->Fill( pretaggedJets[1]->mass() , histoWeight_);
        histograms1d["mu1_G"]->Fill(mu1, histoWeight_);
        histograms1d["y1_G"]->Fill(y1, histoWeight_);
        histograms1d["dR1_G"]->Fill(dR1, histoWeight_);
        histograms1d["jetEta1_G"]->Fill( p4_1.eta(), histoWeight_ );
        histograms2d["dRVsPt1_G"]       ->  Fill( p4_1.pt(),    dR1, histoWeight_ );
        histograms2d["jetMassVsPt1_G"]  ->  Fill( p4_1.pt(),    pretaggedJets[1]->mass() , histoWeight_);

      }

      else if ( fabs(pretaggedJets[1]->partonFlavour()) < 4 ) {
        histograms1d["jetPt1_UDS"]->Fill( p4_1.pt(), histoWeight_ );
        histograms1d["jetMass1_UDS"]->Fill( pretaggedJets[1]->mass() , histoWeight_);
        histograms1d["mu1_UDS"]->Fill(mu1, histoWeight_);
        histograms1d["y1_UDS"]->Fill(y1, histoWeight_);
        histograms1d["dR1_UDS"]->Fill(dR1, histoWeight_);
        histograms1d["jetEta1_UDS"]->Fill( p4_1.eta(), histoWeight_ );
        histograms2d["dRVsPt1_UDS"]       ->  Fill( p4_1.pt(),    dR1, histoWeight_ );
        histograms2d["jetMassVsPt1_UDS"]  ->  Fill( p4_1.pt(),    pretaggedJets[1]->mass() , histoWeight_);

      }

      else if ( (fabs(pretaggedJets[1]->partonFlavour()) == 4 ||
            fabs(pretaggedJets[1]->partonFlavour()) == 5 )
          ) {
        histograms1d["jetPt1_BC"]->Fill( p4_1.pt(), histoWeight_ );
        histograms1d["jetMass1_BC"]->Fill( pretaggedJets[1]->mass() , histoWeight_);
        histograms1d["mu1_BC"]->Fill(mu1, histoWeight_);
        histograms1d["y1_BC"]->Fill(y1, histoWeight_);
        histograms1d["dR1_BC"]->Fill(dR1, histoWeight_);
        histograms1d["jetEta1_BC"]->Fill( p4_1.eta(), histoWeight_ );
        histograms2d["dRVsPt1_BC"]       ->  Fill( p4_1.pt(),    dR1, histoWeight_ );
        histograms2d["jetMassVsPt1_BC"]  ->  Fill( p4_1.pt(),    pretaggedJets[1]->mass() , histoWeight_);

      }


      summary.push_back( EventSummary( p4.mass(), mu0, mu1, y0, y1,
            iEvent.id().run(), iEvent.id().event(), iEvent.luminosityBlock() ) );

      if ( ret ) {
        std::vector<edm::Ptr<pat::Jet> > const & taggedJets = hadronicSelection_.taggedJets();

        if ( taggedJets.size() >= 1 ) {
          histograms1d["dijetMassSingleTagged"]->Fill( p4.mass(), histoWeight_ );

          if ( taggedJets.size() >= 2 ) {	    
            histograms1d["dijetMassDoubleTagged"]->Fill( p4.mass(), histoWeight_ );
          }
        }
      }  // end if ret
    }
  }
}

void HadronicAnalysis::analyzeWJet( const edm::EventBase& iEvent )
{
  //Get genParticles
  edm::Handle< vector<reco::GenParticle> >  h_genParticles;
  iEvent.getByLabel( edm::InputTag("genParticles") , h_genParticles );
  if( !h_genParticles.isValid() )   return ;
  //Get jets
  edm::Handle<vector<pat::Jet>  >   jetHandle;
  iEvent.getByLabel( edm::InputTag("selectedPatJetsCA8PrunedPF") , jetHandle );
  vector<const reco::GenParticle *>     Ws;
  double wPt0, wPt1;
  for( vector<reco::GenParticle>::const_iterator igen = h_genParticles->begin(); igen != h_genParticles->end(); igen++ )
  {
    int pdgId = fabs( igen->pdgId() );
    //cout<<igen->pt()<<endl;
    if( igen->status() == 3 && pdgId == 24 && igen->pt() > 80 )
      Ws.push_back( &(*igen) );
  }

  //cout<<Ws.size()<<endl;
  if( Ws.size() != 2 )   return;
  wPt0 = Ws[0]->pt();
  wPt1 = Ws[1]->pt();

  double minDr0 = 9999., minDr1 = 9999.;
  const pat::Jet * jet0=NULL, *jet1=NULL;
  for( vector<pat::Jet>::const_iterator ijet = jetHandle->begin(); ijet != jetHandle->end(); ijet++ ) {
    if( ijet->pt() > jetPtMin_ )
      histograms2d["W_jetMassVsPt"]     ->  Fill( ijet->pt(), ijet->mass() );
    double dR0 = reco::deltaR<double>( ijet->eta(), ijet->phi(), Ws[0]->eta(), Ws[0]->phi() );
    double dR1 = reco::deltaR<double>( ijet->eta(), ijet->phi(), Ws[1]->eta(), Ws[1]->phi() );
    if( dR0 < minDr0 )  {
      minDr0 = dR0;
      jet0 = &(*ijet);
    }
    if( dR1 < minDr1 ) {
      minDr1 = dR1;
      jet1 = &(*ijet);
    }
  }

  if( !jet0 || !jet1 )   return;
  double ptD0 = fabs( wPt0 - jet0->pt() );
  double ptD1 = fabs( wPt1 - jet1->pt() );

  if( minDr0 <= 1.0 && ptD0 < 15 ) {
    //cout<<"Found match "<<jet0<<endl;
    int n = jet0->numberOfDaughters();
    double pt = jet0->pt();
    double mass = jet0->mass();
    double mu =0, y=0, dR=0;
    pat::subjetHelper( *jet0, y, mu, dR );
    if( pt > jetPtMin_ ) {
      histograms1d["WPt"]       ->  Fill( pt );
      histograms1d["WMass"]     ->  Fill( mass );
      histograms1d["W_nD"]      ->  Fill( n );
      histograms1d["W_mu"]      ->  Fill( mu );
      histograms1d["W_y"]       ->  Fill( y );
      histograms1d["W_dR"]      ->  Fill( dR );
      histograms1d["jetPartonDr"]   ->  Fill( minDr0 );
      histograms2d["W_jetMassVsMu"] ->  Fill( mu, mass );
      if( mu < mu_ )
        histograms1d["WMass_0"]     ->  Fill( mass );
      if( mu < mu_ && mass > wMinMass_ ) {
        histograms1d["W_y_0"]   ->  Fill( y );
        histograms1d["W_dR_0"]  ->  Fill( dR );
      } // mu && mass
    } // pt > 150
  }
  if( minDr1 <= 1.0 && ptD1 < 15 ) {
    //cout<<"Found match "<<jet1<<endl;
    int n = jet1->numberOfDaughters();
    double pt = jet1->pt();
    double mass = jet1->mass();
    double mu =0, y=0, dR=0;
    pat::subjetHelper( *jet1, y, mu, dR );
    if( pt > jetPtMin_ )  {
      histograms1d["WPt"]       ->  Fill( pt );
      histograms1d["WMass"]     ->  Fill( mass );
      histograms1d["W_nD"]      ->  Fill( n );
      histograms1d["W_mu"]      ->  Fill( mu );
      histograms1d["W_y"]       ->  Fill( y );
      histograms1d["W_dR"]      ->  Fill( dR );
      histograms1d["jetPartonDr"]   ->  Fill( minDr1 );
      histograms2d["W_jetMassVsMu"] ->  Fill( mu, mass );
      if( mu < mu_ )
        histograms1d["WMass_0"]   ->  Fill( mass );
      if( mu < mu_ && mass > wMinMass_ ) {
        histograms1d["W_y_0"]   ->  Fill( y );
        histograms1d["W_dR_0"]  ->  Fill( dR );
      } // mu and mass
    } // pt > 150 
  }

}
