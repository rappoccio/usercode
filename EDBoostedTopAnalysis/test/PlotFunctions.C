void MakeHistogram(
	TFile* file,
	std::string histname1,//TH1D* h_DATA,
	std::string histname2,//TH1D* h_QCD,
	std::string histname3,//TH1D* h_TTBAR, 
	std::string title, 
	std::string L1, 
	std::string L2, 
	std::string L3, 
	double legXmin, double legYmin, double legXmax, double legYmax, 
	double YaxisTitleOffset, 
	std::string savename, 
	int rebin, 
	double lowerbound, 
	double upperbound)
	{
	
	using namespace std;

	//////////////////////////////////////////////////////////////////////////////////////////
	gROOT->SetStyle("Plain");
	//-----------------------------------------
	//    Canvas
	//-----------------------------------------
	//gStyle->SetCanvasBorderMode(0);
	//gStyle->SetCanvasColor(10);
	//-----------------------------------------
	//   StatsBox
	//-----------------------------------------
	gStyle->SetOptStat(0);
	//gStyle->SetOptStat("eou");
	//gStyle->SetOptStat(111111);
	//gStyle->SetStatColor(10);
	//gStyle->SetStatBorderSize(5);
	//gStyle->SetStatFontSize(0.08);
	//-----------------------------------------
	//    Histogram Attributes
	//-----------------------------------------
	gStyle->SetHistLineWidth(2);
	//gStyle->SetPalette(52,0); 
	gStyle->SetHatchesSpacing(0.5);
	gStyle->SetHatchesLineWidth(1.7);
	//-----------------------------------------
	//    Pad .  Use Canvas->SetLeftMargin(0.08) to do individually 
	//-----------------------------------------
	gStyle->SetPadTopMargin(0.05);
	gStyle->SetPadBottomMargin(0.13);
	gStyle->SetPadLeftMargin(0.16);
	gStyle->SetPadRightMargin(0.04); 
	//gStyle->SetPadBorderMode(0);
	//-----------------------------------------
	//    Title, axis labels, and axis numbers
	//-----------------------------------------
	//gStyle->SetTitleColor();
	gStyle->SetTitleBorderSize(0);
	gStyle->SetTitleXOffset(1.2);
	gStyle->SetTitleYOffset(1.7);  //gStyle->SetTitleOffset(2.9,"Y"); also works
	//gStyle->SetTitleXSize(0.05);
	//gStyle->SetTitleYSize(0.05);
	//gStyle->SetTitleSize(30);
	gStyle->SetTitleX(0.02); 
	gStyle->SetTitleY(0.99);
	gStyle->SetTitleW(0.5);
	//gStyle->SetTitleFontSize(0.06);	// Change size of histogram title
	//gStyle->SetTitleSize(0.05,"XY");	// Change the size of the axis labels    
	//gStyle->SetTitleOffset(10,"Y");
	//gStyle->SetTitleOffset(2,"X");
	//gStyle->SetLabelSize(0.08,"XY");	// Change size of axis numbers
	gStyle->SetLabelOffset(0.012,"X");
	gStyle->SetPadTickX(1);  
	gStyle->SetPadTickY(1);
	gStyle->SetTickLength(0.03, "XYZ");
	//-----------------------------------------
	//--- Force Style
	//-----------------------------------------
	gROOT->UseCurrentStyle();
	gROOT->ForceStyle();// forces the style chosen above to be used, not the style the rootfile was made with
    /////////////////////////////////////////////////////////////////////////////////////////
	

	TCanvas *c1000= new TCanvas("c1000","",200,10,700,650);	
	
	
	TH1F* h_DATA	=  file -> Get( histname1.c_str() );
	TH1F* h_QCD		=  file -> Get( histname2.c_str() );
	TH1F* h_TTBAR 	=  file -> Get( histname3.c_str() );	
	
	string savename1pdf = savename + "_QCDonly.pdf";
	string savename1png = savename + "_QCDonly.png";
	string savename1eps = savename + "_QCDonly.eps";
	string savename2pdf = savename + "_QCDplusTTBAR.pdf";
	string savename2png = savename + "_QCDplusTTBAR.png";
	string savename2eps = savename + "_QCDplusTTBAR.eps";
	
	double nbinsx = h_DATA->GetNbinsX();
	double lower  = h_DATA->GetBinLowEdge(1);
	double upper  = h_DATA->GetBinLowEdge(nbinsx)+h_DATA->GetBinWidth(nbinsx);
	
	cout<<"nbinsx "<<nbinsx<<"  lower "<<lower<<"  upper "<<upper<<endl;
	
	TH1F *h_STACK = new TH1F("h_STACK","h_STACK", nbinsx, lower, upper);		
	h_STACK->Add( h_STACK, h_QCD,1,1);
	h_STACK->Add( h_STACK, h_TTBAR,1,1);
		
	
	TH1D *h_QCD_noErrors = new TH1D("h_QCD_noErrors","",nbinsx,lower,upper);
	TH1F *h_STACK_noErrors= new TH1F("h_STACK_noErrors","h_STACK_noErrors", nbinsx, lower, upper);	


	for (int i=1; i< h_QCD->GetNbinsX(); i++)
	{
	
		h_STACK_noErrors->SetBinContent( i, h_STACK->GetBinContent(i) );
		h_STACK_noErrors->SetBinError( i, 0 );
	
		h_QCD_noErrors->SetBinContent(i,h_QCD->GetBinContent(i) );
		h_QCD_noErrors->SetBinError(i,0);
	}

	h_DATA				->SetTitle(title.c_str());
	h_QCD				->SetTitle(title.c_str());
	h_TTBAR				->SetTitle(title.c_str());
	h_STACK				->SetTitle(title.c_str());
	h_QCD_noErrors		->SetTitle(title.c_str());
	h_STACK_noErrors	->SetTitle(title.c_str());
		
	h_DATA				->SetTitleOffset( YaxisTitleOffset,"Y");
	h_QCD				->SetTitleOffset( YaxisTitleOffset,"Y");
	h_TTBAR				->SetTitleOffset( YaxisTitleOffset,"Y");
	h_STACK				->SetTitleOffset( YaxisTitleOffset,"Y");
	h_QCD_noErrors		->SetTitleOffset( YaxisTitleOffset,"Y");
	h_STACK_noErrors	->SetTitleOffset( YaxisTitleOffset,"Y");
	
	h_DATA				->Rebin(rebin);
	h_QCD 				->Rebin(rebin);
	h_TTBAR 			->Rebin(rebin);
	h_STACK 			->Rebin(rebin);
	h_QCD_noErrors		->Rebin(rebin);
	h_STACK_noErrors	->Rebin(rebin);
	
	if ( lowerbound!=-1 && upperbound!=-1)
	{
		h_DATA				->GetXaxis()->SetRangeUser(lowerbound,upperbound);
		h_QCD				->GetXaxis()->SetRangeUser(lowerbound,upperbound);
		h_TTBAR				->GetXaxis()->SetRangeUser(lowerbound,upperbound);
		h_STACK				->GetXaxis()->SetRangeUser(lowerbound,upperbound);
		h_QCD_noErrors		->GetXaxis()->SetRangeUser(lowerbound,upperbound);
		h_STACK_noErrors	->GetXaxis()->SetRangeUser(lowerbound,upperbound);
	}
	
	cout<<"h_DATA  ->GetEntries() "<<h_DATA->GetEntries()<<endl;	
	cout<<"h_DATA  ->Integral()   "<<h_DATA->Integral()<<endl;		
	cout<<"h_QCD   ->GetEntries() "<<h_QCD->GetEntries()<<endl;
	cout<<"h_QCD   ->Integral()   "<<h_QCD->Integral()<<endl;
	cout<<"h_TTBAR ->GetEntries() "<<h_TTBAR->GetEntries()<<endl;	
	cout<<"h_TTBAR ->Integral()   "<<h_TTBAR->Integral()<<endl;
	cout<<"h_STACK ->GetEntries() "<<h_STACK->GetEntries()<<endl;	
	cout<<"h_STACK ->Integral()   "<<h_STACK->Integral()<<endl;

	//--------------------------------------------------------------------
	
	h_DATA	->SetMarkerStyle(20);	
	h_DATA	->SetLineWidth(2);
	
	h_QCD->SetLineColor(kGreen);
	h_QCD->SetLineWidth(0);
	h_QCD->SetFillColor(kGreen);
	h_QCD->SetFillStyle(3354);
	h_QCD_noErrors->SetLineColor(kGreen);
	h_QCD_noErrors->SetLineWidth(3);
	
	h_DATA->Draw("PE");
	h_QCD->Draw("9E2same");
	h_QCD_noErrors->Draw("same");

	h_QCD->Draw("Lsame");
	h_DATA->Draw("PEsame");
	
	leg = new TLegend(legXmin,legYmin,legXmax,legYmax);
	leg->SetBorderSize(1);
	leg->SetFillColor(0);
	leg->AddEntry(h_DATA,			L1.c_str(),"P");
	leg->AddEntry(h_QCD_noErrors,	L2.c_str(),"L");
	leg->Draw("same");

	gPad->RedrawAxis();
	
	c1000->SaveAs(savename1pdf.c_str());
	c1000->SaveAs(savename1png.c_str());
	c1000->SaveAs(savename1eps.c_str());
	//--------------------------------------------------------------------
	
	h_STACK->SetLineColor(kRed);
	h_STACK->SetLineWidth(0);
	h_STACK->SetFillColor((kRed));
	h_STACK->SetFillStyle(3354);
	h_STACK_noErrors->SetLineColor((kRed));
	h_STACK_noErrors->SetLineWidth(3);
	
	h_QCD_noErrors->SetLineWidth(2);
	h_QCD_noErrors->SetLineColor(1);
	h_QCD_noErrors->SetFillColor(kYellow);
	
	h_DATA->Draw("PE");
	h_QCD_noErrors->Draw("same");
	h_STACK->Draw("9E2same");
	h_STACK_noErrors->Draw("same");
	h_DATA->Draw("PEsame");

	leg = new TLegend(legXmin,legYmin,legXmax,legYmax);
	leg->SetBorderSize(1);
	leg->SetFillColor(0);
	leg->AddEntry(	h_DATA,				L1.c_str(),"P");
	leg->AddEntry(	h_QCD_noErrors,		L2.c_str(),"F");
	leg->AddEntry(	h_STACK,			L3.c_str(),"L");
	leg->Draw("same");

	TPaveText *textbox = new TPaveText(legXmin-0.01,legYmin-0.11,legXmax-0.05,legYmin-0.01,"NDC");
	textbox->SetFillColor(0);
	textbox->SetLineColor(0);
	TText *line1 = textbox->AddText("CMS Preliminary");
	line1->SetTextColor(1);
	line1->SetTextAlign(12); //first number = horizontal alignment (1 left, 2 center, 3 right). second number =vertical alignment (1 top, 2 center, 3 bottom)
	TText *line2 = textbox->AddText("35.97 pb^{-1} at #sqrt{s} = 7 TeV");
	line2->SetTextColor(1);
	line2->SetTextAlign(12); //first number = horizontal alignment (1 left, 2 center, 3 right). second number =vertical alignment (1 top, 2 center, 3 bottom)
	textbox->Draw("same");
	
	gPad->RedrawAxis();

	c1000->SaveAs(savename2pdf.c_str());
	c1000->SaveAs(savename2png.c_str());
	c1000->SaveAs(savename2eps.c_str());

	//--------------------------------------------------------------------

	delete c1000;
	rebin = -1;	
}


void PrintCounts( TFile* file )
{


	TH1D * Nevents_analyzed							=  file -> Get("type22QCDAna15/Nevents_analyzed");
	TH1D * Nevents_preselected						=  file -> Get("type22QCDAna15/Nevents_preselected");
	
	TH1D * Nevents_hasTaggedTopJet0					=  file -> Get("type22QCDAna15/Nevents_hasTaggedTopJet0");
	TH1D * Nevents_hasTaggedTopJet1					=  file -> Get("type22QCDAna15/Nevents_hasTaggedTopJet1");
	TH1D * Nevents_hasZeroTopTags					=  file -> Get("type22QCDAna15/Nevents_hasZeroTopTags");
	TH1D * Nevents_hasOneTopTag						=  file -> Get("type22QCDAna15/Nevents_hasOneTopTag");
	TH1D * Nevents_hasTwoTopTags					=  file -> Get("type22QCDAna15/Nevents_hasTwoTopTags");
	
	TH1D * Nevents_hasWTag0							=  file -> Get("type22QCDAna15/Nevents_hasWTag0");
	TH1D * Nevents_hasWTag1							=  file -> Get("type22QCDAna15/Nevents_hasWTag1");
	TH1D * Nevents_hasZeroWTags						=  file -> Get("type22QCDAna15/Nevents_hasZeroWTags");
	TH1D * Nevents_hasOneWTag						=  file -> Get("type22QCDAna15/Nevents_hasOneWTag");
	TH1D * Nevents_hasTwoWTags						=  file -> Get("type22QCDAna15/Nevents_hasTwoWTags");
	
	TH1D * Nevents_hasBTag0							=  file -> Get("type22QCDAna15/Nevents_hasBTag0");
	TH1D * Nevents_hasBTag1							=  file -> Get("type22QCDAna15/Nevents_hasBTag1");
	TH1D * Nevents_hasZeroBTags						=  file -> Get("type22QCDAna15/Nevents_hasZeroBTags");
	TH1D * Nevents_hasOneBTag						=  file -> Get("type22QCDAna15/Nevents_hasOneBTag");
	TH1D * Nevents_hasTwoBTags						=  file -> Get("type22QCDAna15/Nevents_hasTwoBTags");
	
	TH1D * Nevents_hasTightTop0						=  file -> Get("type22QCDAna15/Nevents_hasTightTop0");
	TH1D * Nevents_hasTightTop1						=  file -> Get("type22QCDAna15/Nevents_hasTightTop1");
	TH1D * Nevents_hasZeroTightTops					=  file -> Get("type22QCDAna15/Nevents_hasZeroTightTops");
	TH1D * Nevents_hasOneTightTop					=  file -> Get("type22QCDAna15/Nevents_hasOneTightTop");
	TH1D * Nevents_hasTwoTightTops					=  file -> Get("type22QCDAna15/Nevents_hasTwoTightTops");
	
	TH1D * Nevents_hasLooseTop0						=  file -> Get("type22QCDAna15/Nevents_hasLooseTop0");
	TH1D * Nevents_hasLooseTop1						=  file -> Get("type22QCDAna15/Nevents_hasLooseTop1");
	TH1D * Nevents_hasZeroLooseTops					=  file -> Get("type22QCDAna15/Nevents_hasZeroLooseTops");
	TH1D * Nevents_hasOneLooseTop					=  file -> Get("type22QCDAna15/Nevents_hasOneLooseTop");
	TH1D * Nevents_hasTwoLooseTops					=  file -> Get("type22QCDAna15/Nevents_hasTwoLooseTops");
	
	TH1D * Nevents_hasOneLooseOneTightTop			=  file -> Get("type22QCDAna15/Nevents_hasOneLooseOneTightTop");
	TH1D * Nevents_hemiWithWandB					=  file -> Get("type22QCDAna15/Nevents_hemiWithWandB");
	TH1D * Nevents_hemiWithWandUntagged				=  file -> Get("type22QCDAna15/Nevents_hemiWithWandUntagged");

	TH1D * Nevents_TopTagAndTightTop				=  file -> Get("type22QCDAna15/Nevents_TopTagAndTightTop");
	TH1D * Nevents_TopTagAndLooseTop				=  file -> Get("type22QCDAna15/Nevents_TopTagAndLooseTop");
	TH1D * Nevents_TopTagAndWandB					=  file -> Get("type22QCDAna15/Nevents_TopTagAndWandB");
	TH1D * Nevents_hasTwoWTags_hasOneBTag			=  file -> Get("type22QCDAna15/Nevents_hasTwoWTags_hasOneBTag");
	TH1D * Nevents_hasTwoWTags_hasTwoBTags			=  file -> Get("type22QCDAna15/Nevents_hasTwoWTags_hasTwoBTags");
	TH1D * Nevents_TightTopAndLooseTop				=  file -> Get("type22QCDAna15/Nevents_TightTopAndLooseTop");
	TH1D * Nevents_hasOneTopJet_noNonLeadingBjet	=  file -> Get("type22QCDAna15/Nevents_hasOneTopJet_noNonLeadingBjet");

	TH1D * Nevents_type11sig						=  file -> Get("type22QCDAna15/Nevents_type11sig");
	TH1D * Nevents_type12sig						=  file -> Get("type22QCDAna15/Nevents_type12sig");
	TH1D * Nevents_type22sig						=  file -> Get("type22QCDAna15/Nevents_type22sig");
	TH1D * Nevents_type11bkg						=  file -> Get("type22QCDAna15/Nevents_type11bkg");
	TH1D * Nevents_type12bkg						=  file -> Get("type22QCDAna15/Nevents_type12bkg");
	TH1D * Nevents_type22bkg						=  file -> Get("type22QCDAna15/Nevents_type22bkg");

	TH1D * Nevents_cascade12sig						=  file -> Get("type22QCDAna15/Nevents_cascade12sig");
	TH1D * Nevents_cascade22sig						=  file -> Get("type22QCDAna15/Nevents_cascade22sig");
	TH1D * Nevents_cascade11bkg						=  file -> Get("type22QCDAna15/Nevents_cascade11bkg");
	TH1D * Nevents_cascade12bkg						=  file -> Get("type22QCDAna15/Nevents_cascade12bkg");
	TH1D * Nevents_cascade22bkg						=  file -> Get("type22QCDAna15/Nevents_cascade22bkg");

	cout<<"Nevents_analyzed         "<<Nevents_analyzed->GetEntries()<<endl;
	cout<<"Nevents_preselected      "<<Nevents_preselected->GetEntries()<<endl<<endl;
	
	cout<<"Nevents_hasTaggedTopJet0 "<<Nevents_hasTaggedTopJet0->GetEntries()<<endl;
	cout<<"Nevents_hasTaggedTopJet1 "<<Nevents_hasTaggedTopJet1->GetEntries()<<endl;
	cout<<"Nevents_hasZeroTopTags   "<<Nevents_hasZeroTopTags->GetEntries()<<endl;
	cout<<"Nevents_hasOneTopTag     "<<Nevents_hasOneTopTag->GetEntries()<<endl;
	cout<<"Nevents_hasTwoTopTags    "<<Nevents_hasTwoTopTags->GetEntries()<<endl;
	cout<<"0+1+2                    "<<Nevents_hasZeroTopTags->GetEntries() + Nevents_hasOneTopTag->GetEntries()+ Nevents_hasTwoTopTags->GetEntries() <<endl<<endl;

	cout<<"Nevents_hasWTag0         "<<Nevents_hasWTag0->GetEntries()<<endl;
	cout<<"Nevents_hasWTag1         "<<Nevents_hasWTag1->GetEntries()<<endl;
	cout<<"Nevents_hasZeroWTags     "<<Nevents_hasZeroWTags->GetEntries()<<endl;
	cout<<"Nevents_hasOneWTag       "<<Nevents_hasOneWTag->GetEntries()<<endl;
	cout<<"Nevents_hasTwoWTags      "<<Nevents_hasTwoWTags->GetEntries()<<endl;
	cout<<"0+1+2                    "<<Nevents_hasZeroWTags->GetEntries() + Nevents_hasOneWTag->GetEntries()+ Nevents_hasTwoWTags->GetEntries() <<endl<<endl;

	cout<<"Nevents_hasBTag0         "<<Nevents_hasBTag0->GetEntries()<<endl;
	cout<<"Nevents_hasBTag1         "<<Nevents_hasBTag1->GetEntries()<<endl;
	cout<<"Nevents_hasZeroBTags     "<<Nevents_hasZeroBTags->GetEntries()<<endl;
	cout<<"Nevents_hasOneBTag       "<<Nevents_hasOneBTag->GetEntries()<<endl;
	cout<<"Nevents_hasTwoBTags      "<<Nevents_hasTwoBTags->GetEntries()<<endl;
	cout<<"0+1+2                    "<<Nevents_hasZeroBTags->GetEntries() + Nevents_hasOneBTag->GetEntries()+ Nevents_hasTwoBTags->GetEntries() <<endl<<endl;

	cout<<"Nevents_hasTightTop0     "<<Nevents_hasTightTop0->GetEntries()<<endl;
	cout<<"Nevents_hasTightTop1     "<<Nevents_hasTightTop1->GetEntries()<<endl;
	cout<<"Nevents_hasZeroTightTops "<<Nevents_hasZeroTightTops->GetEntries()<<endl;
	cout<<"Nevents_hasOneTightTop   "<<Nevents_hasOneTightTop->GetEntries()<<endl;
	cout<<"Nevents_hasTwoTightTops  "<<Nevents_hasTwoTightTops->GetEntries()<<endl;
	cout<<"0+1+2                    "<<Nevents_hasZeroTightTops->GetEntries() + Nevents_hasOneTightTop->GetEntries()+ Nevents_hasTwoTightTops->GetEntries() <<endl<<endl;

	cout<<"Nevents_hasLooseTop0     "<<Nevents_hasLooseTop0->GetEntries()<<endl;
	cout<<"Nevents_hasLooseTop1     "<<Nevents_hasLooseTop1->GetEntries()<<endl;
	cout<<"Nevents_hasZeroLooseTops "<<Nevents_hasZeroLooseTops->GetEntries()<<endl;
	cout<<"Nevents_hasOneLooseTop   "<<Nevents_hasOneLooseTop->GetEntries()<<endl;
	cout<<"Nevents_hasTwoLooseTops  "<<Nevents_hasTwoLooseTops->GetEntries()<<endl;
	cout<<"0+1+2                    "<<Nevents_hasZeroLooseTops->GetEntries() + Nevents_hasOneLooseTop->GetEntries()+ Nevents_hasTwoLooseTops->GetEntries() <<endl<<endl;

	cout<<"Nevents_hasOneLooseOneTightTop "<<Nevents_hasOneLooseOneTightTop->GetEntries()<<endl;
	cout<<"Nevents_hemiWithWandB          "<<Nevents_hemiWithWandB->GetEntries()<<endl;
	cout<<"Nevents_hemiWithWandUntagged   "<<Nevents_hemiWithWandUntagged->GetEntries()<<endl<<endl;

	cout<<"Nevents_TopTagAndTightTop 				"<<Nevents_TopTagAndTightTop->GetEntries()<<endl;
	cout<<"Nevents_TopTagAndLooseTop 				"<<Nevents_TopTagAndLooseTop->GetEntries()<<endl;
	cout<<"Nevents_TopTagAndWandB 					"<<Nevents_TopTagAndWandB->GetEntries()<<endl;
	cout<<"Nevents_hasTwoWTags_hasOneBTag 			"<<Nevents_hasTwoWTags_hasOneBTag->GetEntries()<<endl;
	cout<<"Nevents_hasTwoWTags_hasTwoBTags 			"<<Nevents_hasTwoWTags_hasTwoBTags->GetEntries()<<endl;
	cout<<"Nevents_TightTopAndLooseTop 				"<<Nevents_TightTopAndLooseTop->GetEntries()<<endl;
	cout<<"Nevents_hasOneTopJet_noNonLeadingBjet 	"<<Nevents_hasOneTopJet_noNonLeadingBjet->GetEntries()<<endl<<endl;

	cout<<"Nevents_type11sig 	"<<Nevents_type11sig->GetEntries()<<endl;
	cout<<"Nevents_type12sig 	"<<Nevents_type12sig->GetEntries()<<endl;
	cout<<"Nevents_type22sig 	"<<Nevents_type22sig->GetEntries()<<endl;
	cout<<"Nevents_type11bkg 	"<<Nevents_type11bkg->GetEntries()<<endl;
	cout<<"Nevents_type12bkg 	"<<Nevents_type12bkg->GetEntries()<<endl;
	cout<<"Nevents_type22bkg 	"<<Nevents_type22bkg->GetEntries()<<endl<<endl;

	cout<<"Nevents_cascade12sig 	"<<Nevents_cascade12sig->GetEntries()<<endl;
	cout<<"Nevents_cascade22sig 	"<<Nevents_cascade22sig->GetEntries()<<endl;
	cout<<"Nevents_cascade11bkg 	"<<Nevents_cascade11bkg->GetEntries()<<endl;
	cout<<"Nevents_cascade12bkg 	"<<Nevents_cascade12bkg->GetEntries()<<endl;
	cout<<"Nevents_cascade22bkg 	"<<Nevents_cascade22bkg->GetEntries()<<endl<<endl;

}