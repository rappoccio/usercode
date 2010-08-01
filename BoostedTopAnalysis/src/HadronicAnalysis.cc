#include "Analysis/BoostedTopAnalysis/interface/HadronicAnalysis.h"


using namespace std;


HadronicAnalysis::HadronicAnalysis(const edm::ParameterSet& iConfig, TFileDirectory& iDir) :
  plotTracks_(false),
  histoWeight_(1.0),
  weightHist_(0),
  hadronicSelection_(iConfig.getParameter<edm::ParameterSet>("hadronicAnalysis")),
  theDir(iDir)
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


  histograms1d["jetMass0"] = theDir.make<TH1F>("jetMass0", "Jet Mass of First Jet", 500, 0, 250 );
  histograms1d["jetMass1"] = theDir.make<TH1F>("jetMass1", "Jet Mass of Second Jet", 500, 0, 250 );
  histograms1d["mu0"]     = theDir.make<TH1F>("mu0", "Mass Drop of First Jet", 500, 0.0, 1.0 );
  histograms1d["mu1"]     = theDir.make<TH1F>("mu1", "Mass Drop of Second Jet", 500, 0.0, 1.0 );
  histograms1d["y0"]     = theDir.make<TH1F>("y0", "Asymmetry of First Jet", 500, 0.0, 1.0 );
  histograms1d["y1"]     = theDir.make<TH1F>("y1", "Asymmetry of Second Jet", 500, 0.0, 1.0 );
  histograms1d["dR0"]     = theDir.make<TH1F>("dR0", "#Delta R of First Jet", 500, 0.0, 1.0 );
  histograms1d["dR1"]     = theDir.make<TH1F>("dR1", "#Delta R of Second Jet", 500, 0.0, 1.0 );

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

  histograms2d["jetMassVsPt0"] = theDir.make<TH2F>("jetMassVsPt0", "First Jet Mass Versus Jet Pt", 50, 0, 500, 50, 0, 250 );
  histograms2d["jetMassVsPt1"] = theDir.make<TH2F>("jetMassVsPt1", "Second Jet Mass Versus Jet Pt", 50, 0, 500, 50, 0, 250 );
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


}

void HadronicAnalysis::analyze(const edm::EventBase& iEvent)
{
  histograms1d["run"]->Fill( iEvent.id().run() );

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

    if ( pretaggedJets.size() >= 2 ) {
      reco::Candidate::LorentzVector p4_0( pretaggedJets[0]->p4() );
      reco::Candidate::LorentzVector p4_1( pretaggedJets[1]->p4() );

      reco::Candidate::LorentzVector p4 = p4_0 + p4_1;

      double mu0 = 0.0, y0 = 0.0, dR0 = 0.0;
      pat::subjetHelper( *pretaggedJets[0], y0, mu0, dR0);
      double mu1 = 0.0, y1 = 0.0, dR1 = 0.0;
      pat::subjetHelper( *pretaggedJets[1], y1, mu1, dR1);	  

      if ( weightHist_ != 0 ) {
	int ibin = weightHist_->GetXaxis()->FindBin( p4_0.pt() );
	double iweight = weightHist_->GetBinContent(ibin);
      
	histoWeight_ = iweight;
      
      }


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
      histograms2d["muVsPt0"]->Fill(pretaggedJets[0]->pt(), mu0, histoWeight_);
      histograms2d["yVsPt0"]->Fill(pretaggedJets[0]->pt(), y0, histoWeight_);
      histograms2d["dRVsPt0"]->Fill(pretaggedJets[0]->pt(), dR0, histoWeight_);

      histograms1d["jetMass1"]->Fill( pretaggedJets[1]->mass() , histoWeight_);
      histograms1d["mu1"]->Fill(mu1, histoWeight_);
      histograms1d["y1"]->Fill(y1, histoWeight_);
      histograms1d["dR1"]->Fill(dR1, histoWeight_);
      histograms2d["jetMassVsPt1"]->Fill( pretaggedJets[1]->pt(), pretaggedJets[1]->mass() , histoWeight_);
      histograms2d["muVsPt1"]->Fill(pretaggedJets[1]->pt(), mu1, histoWeight_);
      histograms2d["yVsPt1"]->Fill(pretaggedJets[1]->pt(), y1, histoWeight_);
      histograms2d["dRVsPt1"]->Fill(pretaggedJets[1]->pt(), dR1, histoWeight_);



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
      }
    }
  }
}
