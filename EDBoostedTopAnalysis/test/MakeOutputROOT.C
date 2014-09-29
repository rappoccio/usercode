{
	#include <iomanip> 

	gROOT->Reset();
	gROOT->ProcessLine(".L /Users/jdolen/Documents/Code/BoostedTop414/PlotFunctions.C");

	TFile *Out;
	Out = new TFile("Output_Jet_2011A_v3_cmssw416_PTCut450_newMistag_May13cert.root","RECREATE");

	//-----------------------------------------------------------------------------------------------------------------------
	//-----------------------------------------------------------------------------------------------------------------------
	//-----------------------------------------------------------------------------------------------------------------------
	
	TFile *FILE = new TFile("combine_Results_Jet_2011A_v3_PTCut450_May13cert.root");
	
	//PrintCounts( FILE );
	
	double rebin=1;
	
	TH1D * ttMassType11_predicted	=  FILE -> Get("cascadingQCDAna15/ttMassPred11_pred");
	TH1D * ttMassType12_predicted	=  FILE -> Get("cascadingQCDAna15/ttMassPred12_pred");
	TH1D * ttMassType22_predicted	=  FILE -> Get("cascadingQCDAna15/ttMassPred22_pred");
	cout<<"ttMassType11_predicted Integral "<<ttMassType11_predicted->Integral()<<endl;
	cout<<"ttMassType12_predicted Integral "<<ttMassType12_predicted->Integral()<<endl;
	cout<<"ttMassType22_predicted Integral "<<ttMassType22_predicted->Integral()<<endl;
	cout<<"ttMassType11_predicted GetEntries "<<ttMassType11_predicted->GetEntries()<<endl;
	cout<<"ttMassType12_predicted GetEntries "<<ttMassType12_predicted->GetEntries()<<endl;
	cout<<"ttMassType22_predicted GetEntries "<<ttMassType22_predicted->GetEntries()<<endl;
	cout<<endl;

	ttMassType11_predicted->Rebin(rebin);
	ttMassType12_predicted->Rebin(rebin);
	ttMassType22_predicted->Rebin(rebin);

	ttMassType11_predicted->SetName("ttMassType11_predicted");
	ttMassType12_predicted->SetName("ttMassType12_predicted");
	ttMassType22_predicted->SetName("ttMassType22_predicted");

	TH1D * ttMassType11_measured	=  FILE -> Get("cascadingQCDAna15/ttMassType11_measured");	
	TH1D * ttMassType12_measured	=  FILE -> Get("cascadingQCDAna15/ttMassType12_measured");
	TH1D * ttMassType22_measured	=  FILE -> Get("cascadingQCDAna15/ttMassType22_measured");
	
	ttMassType11_measured->Rebin(rebin);
	ttMassType12_measured->Rebin(rebin);
	ttMassType22_measured->Rebin(rebin);
	
	//-----------------------------------------------------------------------------------------------------------------------
	//-----------------------------------------------------------------------------------------------------------------------
	//-----------------------------------------------------------------------------------------------------------------------
	TFile *ROOT_TT_mcatnlo 						= new TFile("/Users/jdolen/Documents/Code/BoostedTop387CombineTop4/root_2011_03_31_fixTypos/combine_Results_TT_7TeV-mcatnlo.root");			
	TFile *ROOT_TT_TuneZ2 						= new TFile("/Users/jdolen/Documents/Code/BoostedTop387CombineTop4/root_2011_03_31_fixTypos/combine_Results_TT_TuneZ2_7TeV-pythia6-tauola.root");			
	TFile *ROOT_TTJets_TuneD6T 					= new TFile("/Users/jdolen/Documents/Code/BoostedTop387CombineTop4/root_2011_03_31_fixTypos/combine_Results_TTJets_TuneD6T_7TeV-madgraph-tauola.root");			
	TFile *ROOT_TTJets_TuneD6T_matchingup 		= new TFile("/Users/jdolen/Documents/Code/BoostedTop387CombineTop4/root_2011_03_31_fixTypos/combine_Results_TTJets_TuneD6T_matchingup.root");			
	TFile *ROOT_TTJets_TuneD6T_matchingdown		= new TFile("/Users/jdolen/Documents/Code/BoostedTop387CombineTop4/root_2011_03_31_fixTypos/combine_Results_TTJets_TuneD6T_matchingdown.root");			
	TFile *ROOT_TTJets_TuneD6T_scaleup 			= new TFile("/Users/jdolen/Documents/Code/BoostedTop387CombineTop4/root_2011_03_31_fixTypos/combine_Results_TTJets_TuneD6T_scaleup.root");			
	TFile *ROOT_TTJets_TuneD6T_scaledown		= new TFile("/Users/jdolen/Documents/Code/BoostedTop387CombineTop4/root_2011_03_31_fixTypos/combine_Results_TTJets_TuneD6T_scaledown.root");			
	TFile *ROOT_TTJets_TuneD6T_smallerISRFSR 	= new TFile("/Users/jdolen/Documents/Code/BoostedTop387CombineTop4/root_2011_03_31_fixTypos/combine_Results_TTJets_TuneD6T_smallerISRFSR.root");			
	TFile *ROOT_TTJets_TuneD6T_largerISRFSR		= new TFile("/Users/jdolen/Documents/Code/BoostedTop387CombineTop4/root_2011_03_31_fixTypos/combine_Results_TTJets_TuneD6T_largerISRFSR.root");			
	TFile *ROOT_Zprime_M750GeV_W7500MeV 		= new TFile("/Users/jdolen/Documents/Code/BoostedTop387CombineTop4/root_2011_03_31_fixTypos/combine_Results_Zprime_M750GeV_W7500MeV.root");			
	TFile *ROOT_Zprime_M1000GeV_W10GeV 			= new TFile("/Users/jdolen/Documents/Code/BoostedTop387CombineTop4/root_2011_03_31_fixTypos/combine_Results_Zprime_M1000GeV_W10GeV.root");			
	TFile *ROOT_Zprime_M1250GeV_W1250MeV 		= new TFile("/Users/jdolen/Documents/Code/BoostedTop387CombineTop4/root_2011_03_31_fixTypos/combine_Results_Zprime_M1250GeV_W1250MeV.root");			
	TFile *ROOT_Zprime_M1500GeV_W15GeV 			= new TFile("/Users/jdolen/Documents/Code/BoostedTop387CombineTop4/root_2011_03_31_fixTypos/combine_Results_Zprime_M1500GeV_W15GeV.root");			
	TFile *ROOT_Zprime_M2000GeV_W20GeV 			= new TFile("/Users/jdolen/Documents/Code/BoostedTop387CombineTop4/root_2011_03_31_fixTypos/combine_Results_Zprime_M2000GeV_W20GeV.root");			
	TFile *ROOT_Zprime_M3000GeV_W30GeV 			= new TFile("/Users/jdolen/Documents/Code/BoostedTop387CombineTop4/root_2011_03_31_fixTypos/combine_Results_Zprime_M3000GeV_W30GeV.root");		
	TFile *ROOT_QCD_herwigpp 					= new TFile("/Users/jdolen/Documents/Code/BoostedTop387CombineTop4/root_2011_03_31_fixTypos/combine_Results_QCD_Pt-15To3000_Tune23_Flat_7TeV-herwigpp.root");		
		

	double luminosity = 187.8;//35.97;//21.910331228;

	double DataSetNevents_TT_mcatnlo   = 1000000;
	double sigma_TT_mcatnlo   =          149.6;
	double scale_TT_mcatnlo = sigma_TT_mcatnlo * luminosity / DataSetNevents_TT_mcatnlo;
	
	double DataSetNevents_TT_TuneZ2   = 1000000;
	double sigma_TT_TuneZ2   =          94;
	double scale_TT_TuneZ2 = sigma_TT_TuneZ2 * luminosity / DataSetNevents_TT_TuneZ2;
		
	double DataSetNevents_TTJets_TuneD6T   = 1500000;
	double sigma_TTJets_TuneD6T   =          94.0;
	double scale_TTJets_TuneD6T = sigma_TTJets_TuneD6T * luminosity / DataSetNevents_TTJets_TuneD6T;
	
	double DataSetNevents_TTJets_TuneD6T_matchingup   = 1000000;
	double sigma_TTJets_TuneD6T_matchingup   =          105.9;
	double scale_TTJets_TuneD6T_matchingup = sigma_TTJets_TuneD6T_matchingup * luminosity / DataSetNevents_TTJets_TuneD6T_matchingup;
	
	double DataSetNevents_TTJets_TuneD6T_matchingdown   = 1000000;
	double sigma_TTJets_TuneD6T_matchingdown   =          111.1;
	double scale_TTJets_TuneD6T_matchingdown = sigma_TTJets_TuneD6T_matchingdown * luminosity / DataSetNevents_TTJets_TuneD6T_matchingdown;
	
	double DataSetNevents_TTJets_TuneD6T_scaleup   = 1000000;
	double sigma_TTJets_TuneD6T_scaleup   =          75.0;
	double scale_TTJets_TuneD6T_scaleup = sigma_TTJets_TuneD6T_scaleup * luminosity / DataSetNevents_TTJets_TuneD6T_scaleup;
	
	double DataSetNevents_TTJets_TuneD6T_scaledown   = 1000000;
	double sigma_TTJets_TuneD6T_scaledown   =          186.6;
	double scale_TTJets_TuneD6T_scaledown = sigma_TTJets_TuneD6T_scaledown * luminosity / DataSetNevents_TTJets_TuneD6T_scaledown;
	
	double DataSetNevents_TTJets_TuneD6T_smallerISRFSR   = 1500000;
	double sigma_TTJets_TuneD6T_smallerISRFSR   =          94.6;
	double scale_TTJets_TuneD6T_smallerISRFSR = sigma_TTJets_TuneD6T_smallerISRFSR * luminosity / DataSetNevents_TTJets_TuneD6T_smallerISRFSR;
	
	double DataSetNevents_TTJets_TuneD6T_largerISRFSR   = 1500000;
	double sigma_TTJets_TuneD6T_largerISRFSR   =          100.5;
	double scale_TTJets_TuneD6T_largerISRFSR = sigma_TTJets_TuneD6T_largerISRFSR * luminosity / DataSetNevents_TTJets_TuneD6T_largerISRFSR;
	
	double DataSetNevents_QCD_herwigpp   = 10000000;
	double sigma_QCD_herwigpp   =          3378;
	double scale_QCD_herwigpp = sigma_QCD_herwigpp * luminosity / DataSetNevents_QCD_herwigpp;
	
	
	
	//-----------------------------------------------------------------------------------------------------------------------

	TH1D * ttMassType11_TT_mcatnlo					=  ROOT_TT_mcatnlo -> Get("type22QCDAna15/ttMassType11_measured");
	TH1D * ttMassType11_TT_TuneZ2					=  ROOT_TT_TuneZ2 -> Get("type22QCDAna15/ttMassType11_measured");
	TH1D * ttMassType11_TTJets_TuneD6T				=  ROOT_TTJets_TuneD6T -> Get("type22QCDAna15/ttMassType11_measured");
	TH1D * ttMassType11_TTJets_TuneD6T_matchingup	=  ROOT_TTJets_TuneD6T_matchingup -> Get("type22QCDAna15/ttMassType11_measured");
	TH1D * ttMassType11_TTJets_TuneD6T_matchingdown	=  ROOT_TTJets_TuneD6T_matchingdown -> Get("type22QCDAna15/ttMassType11_measured");
	TH1D * ttMassType11_TTJets_TuneD6T_scaleup		=  ROOT_TTJets_TuneD6T_scaleup -> Get("type22QCDAna15/ttMassType11_measured");
	TH1D * ttMassType11_TTJets_TuneD6T_scaledown	=  ROOT_TTJets_TuneD6T_scaledown -> Get("type22QCDAna15/ttMassType11_measured");
	TH1D * ttMassType11_TTJets_TuneD6T_smallerISRFSR=  ROOT_TTJets_TuneD6T_smallerISRFSR -> Get("type22QCDAna15/ttMassType11_measured");
	TH1D * ttMassType11_TTJets_TuneD6T_largerISRFSR	=  ROOT_TTJets_TuneD6T_largerISRFSR -> Get("type22QCDAna15/ttMassType11_measured");
	TH1D * ttMassType11_Zprime_M750GeV_W7500MeV		=  ROOT_Zprime_M750GeV_W7500MeV -> Get("type22QCDAna15/ttMassType11_measured");
	TH1D * ttMassType11_Zprime_M1000GeV_W10GeV		=  ROOT_Zprime_M1000GeV_W10GeV -> Get("type22QCDAna15/ttMassType11_measured");
	TH1D * ttMassType11_Zprime_M1250GeV_W1250MeV	=  ROOT_Zprime_M1250GeV_W1250MeV -> Get("type22QCDAna15/ttMassType11_measured");
	TH1D * ttMassType11_Zprime_M1500GeV_W15GeV		=  ROOT_Zprime_M1500GeV_W15GeV -> Get("type22QCDAna15/ttMassType11_measured");
	TH1D * ttMassType11_Zprime_M2000GeV_W20GeV		=  ROOT_Zprime_M2000GeV_W20GeV -> Get("type22QCDAna15/ttMassType11_measured");
	TH1D * ttMassType11_Zprime_M3000GeV_W30GeV		=  ROOT_Zprime_M3000GeV_W30GeV -> Get("type22QCDAna15/ttMassType11_measured");
	TH1D * ttMassType11_QCD_herwigpp				=  ROOT_QCD_herwigpp -> Get("type22QCDAna15/ttMassType11_measured");

	cout<<"ttMassType11_Zprime_M750GeV_W7500MeV  "<<ttMassType11_Zprime_M750GeV_W7500MeV->GetEntries()<<endl;
	cout<<"ttMassType11_Zprime_M1000GeV_W10GeV   "<<ttMassType11_Zprime_M1000GeV_W10GeV->GetEntries()<<endl;
	cout<<"ttMassType11_Zprime_M1250GeV_W1250MeV "<<ttMassType11_Zprime_M1250GeV_W1250MeV->GetEntries()<<endl;
	cout<<"ttMassType11_Zprime_M1500GeV_W15GeV   "<<ttMassType11_Zprime_M1500GeV_W15GeV->GetEntries()<<endl;
	cout<<"ttMassType11_Zprime_M2000GeV_W20GeV   "<<ttMassType11_Zprime_M2000GeV_W20GeV->GetEntries()<<endl;
	cout<<"ttMassType11_Zprime_M3000GeV_W30GeV   "<<ttMassType11_Zprime_M3000GeV_W30GeV->GetEntries()<<endl;

	ttMassType11_TT_mcatnlo						->Rebin(rebin);
	ttMassType11_TT_TuneZ2						->Rebin(rebin);
	ttMassType11_TTJets_TuneD6T					->Rebin(rebin);
	ttMassType11_TTJets_TuneD6T_matchingup		->Rebin(rebin);
	ttMassType11_TTJets_TuneD6T_matchingdown	->Rebin(rebin);
	ttMassType11_TTJets_TuneD6T_scaleup			->Rebin(rebin);
	ttMassType11_TTJets_TuneD6T_scaledown		->Rebin(rebin);
	ttMassType11_TTJets_TuneD6T_smallerISRFSR	->Rebin(rebin);
	ttMassType11_TTJets_TuneD6T_largerISRFSR	->Rebin(rebin);
	ttMassType11_Zprime_M750GeV_W7500MeV		->Rebin(rebin);
	ttMassType11_Zprime_M1000GeV_W10GeV			->Rebin(rebin);
	ttMassType11_Zprime_M1250GeV_W1250MeV		->Rebin(rebin);
	ttMassType11_Zprime_M1500GeV_W15GeV			->Rebin(rebin);
	ttMassType11_Zprime_M2000GeV_W20GeV			->Rebin(rebin);
	ttMassType11_Zprime_M3000GeV_W30GeV			->Rebin(rebin);
	ttMassType11_QCD_herwigpp					->Rebin(rebin);
	
	ttMassType11_TT_mcatnlo						->SetTitle("; Type 11 mass; Normalized Number of Events");
	ttMassType11_TT_TuneZ2						->SetTitle("; Type 11 mass; Normalized Number of Events");
	ttMassType11_TTJets_TuneD6T					->SetTitle("; Type 11 mass; Normalized Number of Events");
	ttMassType11_TTJets_TuneD6T_matchingup		->SetTitle("; Type 11 mass; Normalized Number of Events");
	ttMassType11_TTJets_TuneD6T_matchingdown	->SetTitle("; Type 11 mass; Normalized Number of Events");
	ttMassType11_TTJets_TuneD6T_scaleup			->SetTitle("; Type 11 mass; Normalized Number of Events");
	ttMassType11_TTJets_TuneD6T_scaledown		->SetTitle("; Type 11 mass; Normalized Number of Events");
	ttMassType11_TTJets_TuneD6T_smallerISRFSR	->SetTitle("; Type 11 mass; Normalized Number of Events");
	ttMassType11_TTJets_TuneD6T_largerISRFSR	->SetTitle("; Type 11 mass; Normalized Number of Events");
	ttMassType11_Zprime_M750GeV_W7500MeV		->SetTitle("; Type 11 mass; Normalized Number of Events");
	ttMassType11_Zprime_M1000GeV_W10GeV			->SetTitle("; Type 11 mass; Normalized Number of Events");
	ttMassType11_Zprime_M1250GeV_W1250MeV		->SetTitle("; Type 11 mass; Normalized Number of Events");
	ttMassType11_Zprime_M1500GeV_W15GeV			->SetTitle("; Type 11 mass; Normalized Number of Events");
	ttMassType11_Zprime_M2000GeV_W20GeV			->SetTitle("; Type 11 mass; Normalized Number of Events");
	ttMassType11_Zprime_M3000GeV_W30GeV			->SetTitle("; Type 11 mass; Normalized Number of Events");
	ttMassType11_QCD_herwigpp					->SetTitle("; Type 11 mass; Normalized Number of Events");

	ttMassType11_TT_mcatnlo						->Sumw2();
	ttMassType11_TT_TuneZ2						->Sumw2();
	ttMassType11_TTJets_TuneD6T					->Sumw2();
	ttMassType11_TTJets_TuneD6T_matchingup		->Sumw2();
	ttMassType11_TTJets_TuneD6T_matchingdown	->Sumw2();
	ttMassType11_TTJets_TuneD6T_scaleup			->Sumw2();
	ttMassType11_TTJets_TuneD6T_scaledown		->Sumw2();
	ttMassType11_TTJets_TuneD6T_smallerISRFSR	->Sumw2();
	ttMassType11_TTJets_TuneD6T_largerISRFSR	->Sumw2();
	ttMassType11_Zprime_M750GeV_W7500MeV		->Sumw2();
	ttMassType11_Zprime_M1000GeV_W10GeV			->Sumw2();
	ttMassType11_Zprime_M1250GeV_W1250MeV		->Sumw2();
	ttMassType11_Zprime_M1500GeV_W15GeV			->Sumw2();
	ttMassType11_Zprime_M2000GeV_W20GeV			->Sumw2();
	ttMassType11_Zprime_M3000GeV_W30GeV			->Sumw2();
	ttMassType11_QCD_herwigpp					->Sumw2();
	
	ttMassType11_TT_mcatnlo						->Scale(scale_TT_mcatnlo);
	ttMassType11_TT_TuneZ2						->Scale(scale_TT_TuneZ2);
	ttMassType11_TTJets_TuneD6T					->Scale(scale_TTJets_TuneD6T);
	ttMassType11_TTJets_TuneD6T_matchingup		->Scale(scale_TTJets_TuneD6T_matchingup);
	ttMassType11_TTJets_TuneD6T_matchingdown	->Scale(scale_TTJets_TuneD6T_matchingdown);
	ttMassType11_TTJets_TuneD6T_scaleup			->Scale(scale_TTJets_TuneD6T_scaleup);
	ttMassType11_TTJets_TuneD6T_scaledown		->Scale(scale_TTJets_TuneD6T_scaledown);
	ttMassType11_TTJets_TuneD6T_smallerISRFSR	->Scale(scale_TTJets_TuneD6T_smallerISRFSR);
	ttMassType11_TTJets_TuneD6T_largerISRFSR	->Scale(scale_TTJets_TuneD6T_largerISRFSR);
	ttMassType11_QCD_herwigpp					->Scale(scale_QCD_herwigpp);


	ttMassType11_TT_mcatnlo						->SetName("ttMassType11_TT_mcatnlo");
	ttMassType11_TT_TuneZ2						->SetName("ttMassType11_TT_TuneZ2");
	ttMassType11_TTJets_TuneD6T					->SetName("ttMassType11_TTJets_TuneD6T");
	ttMassType11_TTJets_TuneD6T_matchingup		->SetName("ttMassType11_TTJets_TuneD6T_matchingup");
	ttMassType11_TTJets_TuneD6T_matchingdown	->SetName("ttMassType11_TTJets_TuneD6T_matchingdown");
	ttMassType11_TTJets_TuneD6T_scaleup			->SetName("ttMassType11_TTJets_TuneD6T_scaleup");
	ttMassType11_TTJets_TuneD6T_scaledown		->SetName("ttMassType11_TTJets_TuneD6T_scaledown");
	ttMassType11_TTJets_TuneD6T_smallerISRFSR	->SetName("ttMassType11_TTJets_TuneD6T_smallerISRFSR");
	ttMassType11_TTJets_TuneD6T_largerISRFSR	->SetName("ttMassType11_TTJets_TuneD6T_largerISRFSR");
	ttMassType11_Zprime_M750GeV_W7500MeV		->SetName("ttMassType11_Zprime_M750GeV_W7500MeV");
	ttMassType11_Zprime_M1000GeV_W10GeV			->SetName("ttMassType11_Zprime_M1000GeV_W10GeV");
	ttMassType11_Zprime_M1250GeV_W1250MeV		->SetName("ttMassType11_Zprime_M1250GeV_W1250MeV");
	ttMassType11_Zprime_M1500GeV_W15GeV			->SetName("ttMassType11_Zprime_M1500GeV_W15GeV");
	ttMassType11_Zprime_M2000GeV_W20GeV			->SetName("ttMassType11_Zprime_M2000GeV_W20GeV");
	ttMassType11_Zprime_M3000GeV_W30GeV			->SetName("ttMassType11_Zprime_M3000GeV_W30GeV");
	ttMassType11_QCD_herwigpp					->SetName("ttMassType11_QCD_herwigpp");

	//-----------------------------------------------------------------------------------------------------------------------

	TH1D * ttMassType12_TT_mcatnlo					=  ROOT_TT_mcatnlo -> Get("type22QCDAna15/ttMassType12_measured");
	TH1D * ttMassType12_TT_TuneZ2					=  ROOT_TT_TuneZ2 -> Get("type22QCDAna15/ttMassType12_measured");
	TH1D * ttMassType12_TTJets_TuneD6T				=  ROOT_TTJets_TuneD6T -> Get("type22QCDAna15/ttMassType12_measured");
	TH1D * ttMassType12_TTJets_TuneD6T_matchingup	=  ROOT_TTJets_TuneD6T_matchingup -> Get("type22QCDAna15/ttMassType12_measured");
	TH1D * ttMassType12_TTJets_TuneD6T_matchingdown	=  ROOT_TTJets_TuneD6T_matchingdown -> Get("type22QCDAna15/ttMassType12_measured");
	TH1D * ttMassType12_TTJets_TuneD6T_scaleup		=  ROOT_TTJets_TuneD6T_scaleup -> Get("type22QCDAna15/ttMassType12_measured");
	TH1D * ttMassType12_TTJets_TuneD6T_scaledown	=  ROOT_TTJets_TuneD6T_scaledown -> Get("type22QCDAna15/ttMassType12_measured");
	TH1D * ttMassType12_TTJets_TuneD6T_smallerISRFSR=  ROOT_TTJets_TuneD6T_smallerISRFSR -> Get("type22QCDAna15/ttMassType12_measured");
	TH1D * ttMassType12_TTJets_TuneD6T_largerISRFSR	=  ROOT_TTJets_TuneD6T_largerISRFSR -> Get("type22QCDAna15/ttMassType12_measured");
	TH1D * ttMassType12_Zprime_M750GeV_W7500MeV		=  ROOT_Zprime_M750GeV_W7500MeV -> Get("type22QCDAna15/ttMassType12_measured");
	TH1D * ttMassType12_Zprime_M1000GeV_W10GeV		=  ROOT_Zprime_M1000GeV_W10GeV -> Get("type22QCDAna15/ttMassType12_measured");
	TH1D * ttMassType12_Zprime_M1250GeV_W1250MeV	=  ROOT_Zprime_M1250GeV_W1250MeV -> Get("type22QCDAna15/ttMassType12_measured");
	TH1D * ttMassType12_Zprime_M1500GeV_W15GeV		=  ROOT_Zprime_M1500GeV_W15GeV -> Get("type22QCDAna15/ttMassType12_measured");
	TH1D * ttMassType12_Zprime_M2000GeV_W20GeV		=  ROOT_Zprime_M2000GeV_W20GeV -> Get("type22QCDAna15/ttMassType12_measured");
	TH1D * ttMassType12_Zprime_M3000GeV_W30GeV		=  ROOT_Zprime_M3000GeV_W30GeV -> Get("type22QCDAna15/ttMassType12_measured");
	TH1D * ttMassType12_QCD_herwigpp				=  ROOT_QCD_herwigpp -> Get("type22QCDAna15/ttMassType12_measured");

	cout<<"ttMassType12_Zprime_M750GeV_W7500MeV  "<<ttMassType12_Zprime_M750GeV_W7500MeV->GetEntries()<<endl;
	cout<<"ttMassType12_Zprime_M1000GeV_W10GeV   "<<ttMassType12_Zprime_M1000GeV_W10GeV->GetEntries()<<endl;
	cout<<"ttMassType12_Zprime_M1250GeV_W1250MeV "<<ttMassType12_Zprime_M1250GeV_W1250MeV->GetEntries()<<endl;
	cout<<"ttMassType12_Zprime_M1500GeV_W15GeV   "<<ttMassType12_Zprime_M1500GeV_W15GeV->GetEntries()<<endl;
	cout<<"ttMassType12_Zprime_M2000GeV_W20GeV   "<<ttMassType12_Zprime_M2000GeV_W20GeV->GetEntries()<<endl;
	cout<<"ttMassType12_Zprime_M3000GeV_W30GeV   "<<ttMassType12_Zprime_M3000GeV_W30GeV->GetEntries()<<endl;

	ttMassType12_TT_mcatnlo						->Rebin(rebin);
	ttMassType12_TT_TuneZ2						->Rebin(rebin);
	ttMassType12_TTJets_TuneD6T					->Rebin(rebin);
	ttMassType12_TTJets_TuneD6T_matchingup		->Rebin(rebin);
	ttMassType12_TTJets_TuneD6T_matchingdown	->Rebin(rebin);
	ttMassType12_TTJets_TuneD6T_scaleup			->Rebin(rebin);
	ttMassType12_TTJets_TuneD6T_scaledown		->Rebin(rebin);
	ttMassType12_TTJets_TuneD6T_smallerISRFSR	->Rebin(rebin);
	ttMassType12_TTJets_TuneD6T_largerISRFSR	->Rebin(rebin);
	ttMassType12_Zprime_M750GeV_W7500MeV		->Rebin(rebin);
	ttMassType12_Zprime_M1000GeV_W10GeV			->Rebin(rebin);
	ttMassType12_Zprime_M1250GeV_W1250MeV		->Rebin(rebin);
	ttMassType12_Zprime_M1500GeV_W15GeV			->Rebin(rebin);
	ttMassType12_Zprime_M2000GeV_W20GeV			->Rebin(rebin);
	ttMassType12_Zprime_M3000GeV_W30GeV			->Rebin(rebin);
	ttMassType12_QCD_herwigpp					->Rebin(rebin);
	
	ttMassType12_TT_mcatnlo						->SetTitle("; Type 12 mass; Normalized Number of Events");
	ttMassType12_TT_TuneZ2						->SetTitle("; Type 12 mass; Normalized Number of Events");
	ttMassType12_TTJets_TuneD6T					->SetTitle("; Type 12 mass; Normalized Number of Events");
	ttMassType12_TTJets_TuneD6T_matchingup		->SetTitle("; Type 12 mass; Normalized Number of Events");
	ttMassType12_TTJets_TuneD6T_matchingdown	->SetTitle("; Type 12 mass; Normalized Number of Events");
	ttMassType12_TTJets_TuneD6T_scaleup			->SetTitle("; Type 12 mass; Normalized Number of Events");
	ttMassType12_TTJets_TuneD6T_scaledown		->SetTitle("; Type 12 mass; Normalized Number of Events");
	ttMassType12_TTJets_TuneD6T_smallerISRFSR	->SetTitle("; Type 12 mass; Normalized Number of Events");
	ttMassType12_TTJets_TuneD6T_largerISRFSR	->SetTitle("; Type 12 mass; Normalized Number of Events");
	ttMassType12_Zprime_M750GeV_W7500MeV		->SetTitle("; Type 12 mass; Normalized Number of Events");
	ttMassType12_Zprime_M1000GeV_W10GeV			->SetTitle("; Type 12 mass; Normalized Number of Events");
	ttMassType12_Zprime_M1250GeV_W1250MeV		->SetTitle("; Type 12 mass; Normalized Number of Events");
	ttMassType12_Zprime_M1500GeV_W15GeV			->SetTitle("; Type 12 mass; Normalized Number of Events");
	ttMassType12_Zprime_M2000GeV_W20GeV			->SetTitle("; Type 12 mass; Normalized Number of Events");
	ttMassType12_Zprime_M3000GeV_W30GeV			->SetTitle("; Type 12 mass; Normalized Number of Events");
	ttMassType12_QCD_herwigpp					->SetTitle("; Type 12 mass; Normalized Number of Events");

	ttMassType12_TT_mcatnlo						->Sumw2();
	ttMassType12_TT_TuneZ2						->Sumw2();
	ttMassType12_TTJets_TuneD6T					->Sumw2();
	ttMassType12_TTJets_TuneD6T_matchingup		->Sumw2();
	ttMassType12_TTJets_TuneD6T_matchingdown	->Sumw2();
	ttMassType12_TTJets_TuneD6T_scaleup			->Sumw2();
	ttMassType12_TTJets_TuneD6T_scaledown		->Sumw2();
	ttMassType12_TTJets_TuneD6T_smallerISRFSR	->Sumw2();
	ttMassType12_TTJets_TuneD6T_largerISRFSR	->Sumw2();
	ttMassType12_Zprime_M750GeV_W7500MeV		->Sumw2();
	ttMassType12_Zprime_M1000GeV_W10GeV			->Sumw2();
	ttMassType12_Zprime_M1250GeV_W1250MeV		->Sumw2();
	ttMassType12_Zprime_M1500GeV_W15GeV			->Sumw2();
	ttMassType12_Zprime_M2000GeV_W20GeV			->Sumw2();
	ttMassType12_Zprime_M3000GeV_W30GeV			->Sumw2();
	ttMassType12_QCD_herwigpp					->Sumw2();
	
	ttMassType12_TT_mcatnlo						->Scale(scale_TT_mcatnlo);
	ttMassType12_TT_TuneZ2						->Scale(scale_TT_TuneZ2);
	ttMassType12_TTJets_TuneD6T					->Scale(scale_TTJets_TuneD6T);
	ttMassType12_TTJets_TuneD6T_matchingup		->Scale(scale_TTJets_TuneD6T_matchingup);
	ttMassType12_TTJets_TuneD6T_matchingdown	->Scale(scale_TTJets_TuneD6T_matchingdown);
	ttMassType12_TTJets_TuneD6T_scaleup			->Scale(scale_TTJets_TuneD6T_scaleup);
	ttMassType12_TTJets_TuneD6T_scaledown		->Scale(scale_TTJets_TuneD6T_scaledown);
	ttMassType12_TTJets_TuneD6T_smallerISRFSR	->Scale(scale_TTJets_TuneD6T_smallerISRFSR);
	ttMassType12_TTJets_TuneD6T_largerISRFSR	->Scale(scale_TTJets_TuneD6T_largerISRFSR);
	ttMassType12_QCD_herwigpp					->Scale(scale_QCD_herwigpp);


	ttMassType12_TT_mcatnlo						->SetName("ttMassType12_TT_mcatnlo");
	ttMassType12_TT_TuneZ2						->SetName("ttMassType12_TT_TuneZ2");
	ttMassType12_TTJets_TuneD6T					->SetName("ttMassType12_TTJets_TuneD6T");
	ttMassType12_TTJets_TuneD6T_matchingup		->SetName("ttMassType12_TTJets_TuneD6T_matchingup");
	ttMassType12_TTJets_TuneD6T_matchingdown	->SetName("ttMassType12_TTJets_TuneD6T_matchingdown");
	ttMassType12_TTJets_TuneD6T_scaleup			->SetName("ttMassType12_TTJets_TuneD6T_scaleup");
	ttMassType12_TTJets_TuneD6T_scaledown		->SetName("ttMassType12_TTJets_TuneD6T_scaledown");
	ttMassType12_TTJets_TuneD6T_smallerISRFSR	->SetName("ttMassType12_TTJets_TuneD6T_smallerISRFSR");
	ttMassType12_TTJets_TuneD6T_largerISRFSR	->SetName("ttMassType12_TTJets_TuneD6T_largerISRFSR");
	ttMassType12_Zprime_M750GeV_W7500MeV		->SetName("ttMassType12_Zprime_M750GeV_W7500MeV");
	ttMassType12_Zprime_M1000GeV_W10GeV			->SetName("ttMassType12_Zprime_M1000GeV_W10GeV");
	ttMassType12_Zprime_M1250GeV_W1250MeV		->SetName("ttMassType12_Zprime_M1250GeV_W1250MeV");
	ttMassType12_Zprime_M1500GeV_W15GeV			->SetName("ttMassType12_Zprime_M1500GeV_W15GeV");
	ttMassType12_Zprime_M2000GeV_W20GeV			->SetName("ttMassType12_Zprime_M2000GeV_W20GeV");
	ttMassType12_Zprime_M3000GeV_W30GeV			->SetName("ttMassType12_Zprime_M3000GeV_W30GeV");
	ttMassType12_QCD_herwigpp					->SetName("ttMassType12_QCD_herwigpp");

	//-----------------------------------------------------------------------------------------------------------------------
	TH1D * ttMassType22_TT_mcatnlo					=  ROOT_TT_mcatnlo -> Get("type22QCDAna15/ttMassType22_measured");
	TH1D * ttMassType22_TT_TuneZ2					=  ROOT_TT_TuneZ2 -> Get("type22QCDAna15/ttMassType22_measured");
	TH1D * ttMassType22_TTJets_TuneD6T				=  ROOT_TTJets_TuneD6T -> Get("type22QCDAna15/ttMassType22_measured");
	TH1D * ttMassType22_TTJets_TuneD6T_matchingup	=  ROOT_TTJets_TuneD6T_matchingup -> Get("type22QCDAna15/ttMassType22_measured");
	TH1D * ttMassType22_TTJets_TuneD6T_matchingdown	=  ROOT_TTJets_TuneD6T_matchingdown -> Get("type22QCDAna15/ttMassType22_measured");
	TH1D * ttMassType22_TTJets_TuneD6T_scaleup		=  ROOT_TTJets_TuneD6T_scaleup -> Get("type22QCDAna15/ttMassType22_measured");
	TH1D * ttMassType22_TTJets_TuneD6T_scaledown	=  ROOT_TTJets_TuneD6T_scaledown -> Get("type22QCDAna15/ttMassType22_measured");
	TH1D * ttMassType22_TTJets_TuneD6T_smallerISRFSR=  ROOT_TTJets_TuneD6T_smallerISRFSR -> Get("type22QCDAna15/ttMassType22_measured");
	TH1D * ttMassType22_TTJets_TuneD6T_largerISRFSR	=  ROOT_TTJets_TuneD6T_largerISRFSR -> Get("type22QCDAna15/ttMassType22_measured");
	TH1D * ttMassType22_Zprime_M750GeV_W7500MeV		=  ROOT_Zprime_M750GeV_W7500MeV -> Get("type22QCDAna15/ttMassType22_measured");
	TH1D * ttMassType22_Zprime_M1000GeV_W10GeV		=  ROOT_Zprime_M1000GeV_W10GeV -> Get("type22QCDAna15/ttMassType22_measured");
	TH1D * ttMassType22_Zprime_M1250GeV_W1250MeV	=  ROOT_Zprime_M1250GeV_W1250MeV -> Get("type22QCDAna15/ttMassType22_measured");
	TH1D * ttMassType22_Zprime_M1500GeV_W15GeV		=  ROOT_Zprime_M1500GeV_W15GeV -> Get("type22QCDAna15/ttMassType22_measured");
	TH1D * ttMassType22_Zprime_M2000GeV_W20GeV		=  ROOT_Zprime_M2000GeV_W20GeV -> Get("type22QCDAna15/ttMassType22_measured");
	TH1D * ttMassType22_Zprime_M3000GeV_W30GeV		=  ROOT_Zprime_M3000GeV_W30GeV -> Get("type22QCDAna15/ttMassType22_measured");
	TH1D * ttMassType22_QCD_herwigpp				=  ROOT_QCD_herwigpp -> Get("type22QCDAna15/ttMassType22_measured");

	cout<<"ttMassType22_Zprime_M750GeV_W7500MeV  "<<ttMassType22_Zprime_M750GeV_W7500MeV->GetEntries()<<endl;
	cout<<"ttMassType22_Zprime_M1000GeV_W10GeV   "<<ttMassType22_Zprime_M1000GeV_W10GeV->GetEntries()<<endl;
	cout<<"ttMassType22_Zprime_M1250GeV_W1250MeV "<<ttMassType22_Zprime_M1250GeV_W1250MeV->GetEntries()<<endl;
	cout<<"ttMassType22_Zprime_M1500GeV_W15GeV   "<<ttMassType22_Zprime_M1500GeV_W15GeV->GetEntries()<<endl;
	cout<<"ttMassType22_Zprime_M2000GeV_W20GeV   "<<ttMassType22_Zprime_M2000GeV_W20GeV->GetEntries()<<endl;
	cout<<"ttMassType22_Zprime_M3000GeV_W30GeV   "<<ttMassType22_Zprime_M3000GeV_W30GeV->GetEntries()<<endl;

	ttMassType22_TT_mcatnlo						->Rebin(rebin);
	ttMassType22_TT_TuneZ2						->Rebin(rebin);
	ttMassType22_TTJets_TuneD6T					->Rebin(rebin);
	ttMassType22_TTJets_TuneD6T_matchingup		->Rebin(rebin);
	ttMassType22_TTJets_TuneD6T_matchingdown	->Rebin(rebin);
	ttMassType22_TTJets_TuneD6T_scaleup			->Rebin(rebin);
	ttMassType22_TTJets_TuneD6T_scaledown		->Rebin(rebin);
	ttMassType22_TTJets_TuneD6T_smallerISRFSR	->Rebin(rebin);
	ttMassType22_TTJets_TuneD6T_largerISRFSR	->Rebin(rebin);
	ttMassType22_Zprime_M750GeV_W7500MeV		->Rebin(rebin);
	ttMassType22_Zprime_M1000GeV_W10GeV			->Rebin(rebin);
	ttMassType22_Zprime_M1250GeV_W1250MeV		->Rebin(rebin);
	ttMassType22_Zprime_M1500GeV_W15GeV			->Rebin(rebin);
	ttMassType22_Zprime_M2000GeV_W20GeV			->Rebin(rebin);
	ttMassType22_Zprime_M3000GeV_W30GeV			->Rebin(rebin);
	ttMassType22_QCD_herwigpp					->Rebin(rebin);
	
	ttMassType22_TT_mcatnlo						->SetTitle("; Type 22 mass; Normalized Number of Events");
	ttMassType22_TT_TuneZ2						->SetTitle("; Type 22 mass; Normalized Number of Events");
	ttMassType22_TTJets_TuneD6T					->SetTitle("; Type 22 mass; Normalized Number of Events");
	ttMassType22_TTJets_TuneD6T_matchingup		->SetTitle("; Type 22 mass; Normalized Number of Events");
	ttMassType22_TTJets_TuneD6T_matchingdown	->SetTitle("; Type 22 mass; Normalized Number of Events");
	ttMassType22_TTJets_TuneD6T_scaleup			->SetTitle("; Type 22 mass; Normalized Number of Events");
	ttMassType22_TTJets_TuneD6T_scaledown		->SetTitle("; Type 22 mass; Normalized Number of Events");
	ttMassType22_TTJets_TuneD6T_smallerISRFSR	->SetTitle("; Type 22 mass; Normalized Number of Events");
	ttMassType22_TTJets_TuneD6T_largerISRFSR	->SetTitle("; Type 22 mass; Normalized Number of Events");
	ttMassType22_Zprime_M750GeV_W7500MeV		->SetTitle("; Type 22 mass; Normalized Number of Events");
	ttMassType22_Zprime_M1000GeV_W10GeV			->SetTitle("; Type 22 mass; Normalized Number of Events");
	ttMassType22_Zprime_M1250GeV_W1250MeV		->SetTitle("; Type 22 mass; Normalized Number of Events");
	ttMassType22_Zprime_M1500GeV_W15GeV			->SetTitle("; Type 22 mass; Normalized Number of Events");
	ttMassType22_Zprime_M2000GeV_W20GeV			->SetTitle("; Type 22 mass; Normalized Number of Events");
	ttMassType22_Zprime_M3000GeV_W30GeV			->SetTitle("; Type 22 mass; Normalized Number of Events");
	ttMassType22_QCD_herwigpp					->SetTitle("; Type 22 mass; Normalized Number of Events");

	ttMassType22_TT_mcatnlo						->Sumw2();
	ttMassType22_TT_TuneZ2						->Sumw2();
	ttMassType22_TTJets_TuneD6T					->Sumw2();
	ttMassType22_TTJets_TuneD6T_matchingup		->Sumw2();
	ttMassType22_TTJets_TuneD6T_matchingdown	->Sumw2();
	ttMassType22_TTJets_TuneD6T_scaleup			->Sumw2();
	ttMassType22_TTJets_TuneD6T_scaledown		->Sumw2();
	ttMassType22_TTJets_TuneD6T_smallerISRFSR	->Sumw2();
	ttMassType22_TTJets_TuneD6T_largerISRFSR	->Sumw2();
	ttMassType22_Zprime_M750GeV_W7500MeV		->Sumw2();
	ttMassType22_Zprime_M1000GeV_W10GeV			->Sumw2();
	ttMassType22_Zprime_M1250GeV_W1250MeV		->Sumw2();
	ttMassType22_Zprime_M1500GeV_W15GeV			->Sumw2();
	ttMassType22_Zprime_M2000GeV_W20GeV			->Sumw2();
	ttMassType22_Zprime_M3000GeV_W30GeV			->Sumw2();
	ttMassType22_QCD_herwigpp					->Sumw2();
	
	ttMassType22_TT_mcatnlo						->Scale(scale_TT_mcatnlo);
	ttMassType22_TT_TuneZ2						->Scale(scale_TT_TuneZ2);
	ttMassType22_TTJets_TuneD6T					->Scale(scale_TTJets_TuneD6T);
	ttMassType22_TTJets_TuneD6T_matchingup		->Scale(scale_TTJets_TuneD6T_matchingup);
	ttMassType22_TTJets_TuneD6T_matchingdown	->Scale(scale_TTJets_TuneD6T_matchingdown);
	ttMassType22_TTJets_TuneD6T_scaleup			->Scale(scale_TTJets_TuneD6T_scaleup);
	ttMassType22_TTJets_TuneD6T_scaledown		->Scale(scale_TTJets_TuneD6T_scaledown);
	ttMassType22_TTJets_TuneD6T_smallerISRFSR	->Scale(scale_TTJets_TuneD6T_smallerISRFSR);
	ttMassType22_TTJets_TuneD6T_largerISRFSR	->Scale(scale_TTJets_TuneD6T_largerISRFSR);
	ttMassType22_QCD_herwigpp					->Scale(scale_QCD_herwigpp);


	ttMassType22_TT_mcatnlo						->SetName("ttMassType22_TT_mcatnlo");
	ttMassType22_TT_TuneZ2						->SetName("ttMassType22_TT_TuneZ2");
	ttMassType22_TTJets_TuneD6T					->SetName("ttMassType22_TTJets_TuneD6T");
	ttMassType22_TTJets_TuneD6T_matchingup		->SetName("ttMassType22_TTJets_TuneD6T_matchingup");
	ttMassType22_TTJets_TuneD6T_matchingdown	->SetName("ttMassType22_TTJets_TuneD6T_matchingdown");
	ttMassType22_TTJets_TuneD6T_scaleup			->SetName("ttMassType22_TTJets_TuneD6T_scaleup");
	ttMassType22_TTJets_TuneD6T_scaledown		->SetName("ttMassType22_TTJets_TuneD6T_scaledown");
	ttMassType22_TTJets_TuneD6T_smallerISRFSR	->SetName("ttMassType22_TTJets_TuneD6T_smallerISRFSR");
	ttMassType22_TTJets_TuneD6T_largerISRFSR	->SetName("ttMassType22_TTJets_TuneD6T_largerISRFSR");
	ttMassType22_Zprime_M750GeV_W7500MeV		->SetName("ttMassType22_Zprime_M750GeV_W7500MeV");
	ttMassType22_Zprime_M1000GeV_W10GeV			->SetName("ttMassType22_Zprime_M1000GeV_W10GeV");
	ttMassType22_Zprime_M1250GeV_W1250MeV		->SetName("ttMassType22_Zprime_M1250GeV_W1250MeV");
	ttMassType22_Zprime_M1500GeV_W15GeV			->SetName("ttMassType22_Zprime_M1500GeV_W15GeV");
	ttMassType22_Zprime_M2000GeV_W20GeV			->SetName("ttMassType22_Zprime_M2000GeV_W20GeV");
	ttMassType22_Zprime_M3000GeV_W30GeV			->SetName("ttMassType22_Zprime_M3000GeV_W30GeV");
	ttMassType22_QCD_herwigpp					->SetName("ttMassType22_QCD_herwigpp");

	//-----------------------------------------------------------------------------------------------------------------------
	//-----------------------------------------------------------------------------------------------------------------------
	//-----------------------------------------------------------------------------------------------------------------------
	//-----------------------------------------------------------------------------------------------------------------------
	//-----------------------------------------------------------------------------------------------------------------------

	cout<<"ttMassType11_predicted "<<ttMassType11_predicted->Integral()<<endl;
	Out->cd();
  
	ttMassType11_measured->Write(); 
	ttMassType12_measured->Write();
	ttMassType22_measured->Write();
	
	ttMassType11_predicted->Write();
	ttMassType12_predicted->Write();
	ttMassType22_predicted->Write();	
	
	ttMassType11_TT_mcatnlo						->Write();
	ttMassType11_TT_TuneZ2						->Write();
	ttMassType11_TTJets_TuneD6T					->Write();
	ttMassType11_TTJets_TuneD6T_matchingup		->Write();
	ttMassType11_TTJets_TuneD6T_matchingdown	->Write();
	ttMassType11_TTJets_TuneD6T_scaleup			->Write();
	ttMassType11_TTJets_TuneD6T_scaledown		->Write();
	ttMassType11_TTJets_TuneD6T_smallerISRFSR	->Write();
	ttMassType11_TTJets_TuneD6T_largerISRFSR	->Write();
	ttMassType11_Zprime_M750GeV_W7500MeV		->Write();
	ttMassType11_Zprime_M1000GeV_W10GeV			->Write();
	ttMassType11_Zprime_M1250GeV_W1250MeV		->Write();
	ttMassType11_Zprime_M1500GeV_W15GeV			->Write();
	ttMassType11_Zprime_M2000GeV_W20GeV			->Write();
	ttMassType11_Zprime_M3000GeV_W30GeV			->Write();
	ttMassType11_Zprime_M3000GeV_W30GeV			->Write();
	ttMassType11_QCD_herwigpp					->Write();
	
	ttMassType12_TT_mcatnlo						->Write();
	ttMassType12_TT_TuneZ2						->Write();
	ttMassType12_TTJets_TuneD6T					->Write();
	ttMassType12_TTJets_TuneD6T_matchingup		->Write();
	ttMassType12_TTJets_TuneD6T_matchingdown	->Write();
	ttMassType12_TTJets_TuneD6T_scaleup			->Write();
	ttMassType12_TTJets_TuneD6T_scaledown		->Write();
	ttMassType12_TTJets_TuneD6T_smallerISRFSR	->Write();
	ttMassType12_TTJets_TuneD6T_largerISRFSR	->Write();
	ttMassType12_Zprime_M750GeV_W7500MeV		->Write();
	ttMassType12_Zprime_M1000GeV_W10GeV			->Write();
	ttMassType12_Zprime_M1250GeV_W1250MeV		->Write();
	ttMassType12_Zprime_M1500GeV_W15GeV			->Write();
	ttMassType12_Zprime_M2000GeV_W20GeV			->Write();
	ttMassType12_Zprime_M3000GeV_W30GeV			->Write();
	ttMassType12_QCD_herwigpp					->Write();

	ttMassType22_TT_mcatnlo						->Write();
	ttMassType22_TT_TuneZ2						->Write();
	ttMassType22_TTJets_TuneD6T					->Write();
	ttMassType22_TTJets_TuneD6T_matchingup		->Write();
	ttMassType22_TTJets_TuneD6T_matchingdown	->Write();
	ttMassType22_TTJets_TuneD6T_scaleup			->Write();
	ttMassType22_TTJets_TuneD6T_scaledown		->Write();
	ttMassType22_TTJets_TuneD6T_smallerISRFSR	->Write();
	ttMassType22_TTJets_TuneD6T_largerISRFSR	->Write();
	ttMassType22_Zprime_M750GeV_W7500MeV		->Write();
	ttMassType22_Zprime_M1000GeV_W10GeV			->Write();
	ttMassType22_Zprime_M1250GeV_W1250MeV		->Write();
	ttMassType22_Zprime_M1500GeV_W15GeV			->Write();
	ttMassType22_Zprime_M2000GeV_W20GeV			->Write();
	ttMassType22_Zprime_M3000GeV_W30GeV			->Write();
	ttMassType22_QCD_herwigpp					->Write();

	
	Out->ls();      
	Out->Write();
}
	
