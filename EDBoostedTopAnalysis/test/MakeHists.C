{
	gROOT->Reset();
	gROOT->ProcessLine(".L ../BoostedTop414/PlotFunctions.C");
	
	TFile *FILE = new TFile("Output_Jet_2011A_v3_cmssw416_PTCut450_newMistag.root");	
	if ( FILE->IsOpen() ) cout<<"FILE is open"<<endl;
	
	MakeHistogram(
		FILE,
		"ttMassType11_measured", 									// data histogram
		"ttMassType11_predicted", 									// qcd histogram
		"ttMassType11_TTJets_TuneD6T", 								// ttbar histogram
		";Type 1+1 t#bar{t} mass (GeV/c^{2}); Number of Events", 	// histogram title
		"May 24 JSON",														// legend_header
		"Data", 													// legend label 1
		"QCD estimation", 											// legend label 2
		"t#bar{t} Madgraph + Pythia Tune D6T  ", 					// legend label 3
		 0.48, 0.72, 0.92,0.91, 									// legend coordinates
		1.4, 														// Y axis label offset
		"REPLACEME_DIRECTORY/ttMassType11_JetPD", 					// savename
		10, 														// rebin
		500, 														// X axis lowerbound
		3000);														// X axis upperbound
}
	
