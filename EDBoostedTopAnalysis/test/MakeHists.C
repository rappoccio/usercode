{
	gROOT->Reset();
	gROOT->ProcessLine(".L ./PlotFunctions.C");

	TFile *FILE = new TFile("ttMass_2010_03_29.root");	
	if ( FILE->IsOpen() ) cout<<"FILE is open"<<endl;
	//FILE.ls();
	

	MakeHistogram(
		FILE,
		"ttMassType11_measured", 									// data histogram
		"ttMassType11_predicted", 									// qcd histogram
		"ttMassType11_TTJets_TuneD6T", 								// ttbar histogram
		";Type 1+1 t#bar{t} mass (GeV/c^{2}); Number of Events", 	// histogram title
		"Data", 													// legend label 1
		"QCD estimation", 											// legend label 2
		"QCD estimation + t#bar{t} MC", 							// legend label 3
		 0.56, 0.74, 0.92,0.91, 									// legend coordinates
		1.4, 														// Y axis label offset
		"REPLACEME_DIRECTORY/ttMassType11", 						// savename
		10, 														// rebin
		0, 															// X axis lowerbound
		3000);														// X axis upperbound
			
	MakeHistogram(
		FILE,
		"ttMassType12_measured", 									// data histogram
		"ttMassType12_predicted", 									// qcd histogram
		"ttMassType12_TTJets_TuneD6T", 								// ttbar histogram
		";Type 1+2 t#bar{t} mass (GeV/c^{2}); Number of Events", 	// histogram title
		"Data", 													// legend label 1
		"QCD estimation", 											// legend label 2
		"QCD estimation + t#bar{t} MC", 							// legend label 3
		0.56, 0.74, 0.92,0.91,										// legend coordinates
		1.4, 														// Y axis label offset
		"REPLACEME_DIRECTORY/ttMassType12", 						// savename
		10, 														// rebin
		0, 															// X axis lowerbound
		3000);														// X axis upperbound
		
	MakeHistogram(
		FILE,
		"ttMassType22_measured", 									// data histogram
		"ttMassType22_predicted", 									// qcd histogram
		"ttMassType22_TTJets_TuneD6T", 								// ttbar histogram
		";Type 2+2 t#bar{t} mass (GeV/c^{2}); Number of Events", 	// histogram title
		"Data", 													// legend label 1
		"QCD estimation", 											// legend label 2
		"QCD estimation + t#bar{t} MC", 							// legend label 3
		0.56, 0.74, 0.92,0.91,										// legend coordinates
		1.4, 														// Y axis label offset
		"REPLACEME_DIRECTORY/ttMassType22", 						// savename
		10, 														// rebin
		0, 															// X axis lowerbound
		3000);														// X axis upperbound
		
		
	

	
	
}
	
