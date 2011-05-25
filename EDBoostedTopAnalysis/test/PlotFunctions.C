void MakeHistogram(
	TFile* file,
	std::string histname1,//TH1D* h_DATA,
	std::string histname2,//TH1D* h_QCD,
	std::string histname3,//TH1D* h_TTBAR, 
	std::string title,
	std::string legend_header,
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
	if (histname3!="none") TH1F* h_TTBAR =  file -> Get( histname3.c_str() );	
	if (histname3=="none") TH1F* h_TTBAR = new TH1F("h","h",500,0,4000);	
	
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
	cout<<"h_DATA "<<h_DATA->GetNbinsX()<<endl;
	cout<<"h_QCD "<<h_QCD->GetNbinsX()<<endl;
	cout<<"h_QCD_noErrors "<<h_QCD_noErrors->GetNbinsX()<<endl;
	cout<<"h_STACK "<<h_STACK->GetNbinsX()<<endl;
	cout<<"h_STACK_noErrors "<<h_STACK_noErrors->GetNbinsX()<<endl;
	
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
	h_QCD->SetLineColor(0);
	h_QCD->SetLineWidth(0);
	h_QCD->SetFillColor(kGreen);
	h_QCD->SetFillStyle(3354);
	h_QCD_noErrors->SetLineColor(kGreen);
	h_QCD_noErrors->SetLineWidth(3);
	
	cout<<"h_DATA "<<h_DATA->GetNbinsX()<<endl;
	cout<<"h_QCD "<<h_QCD->GetNbinsX()<<endl;
	cout<<"h_QCD_noErrors "<<h_QCD_noErrors->GetNbinsX()<<endl;
	
	h_DATA->Draw("PE");
	h_QCD->Draw("9E2same");
	h_QCD_noErrors->Draw("same");

	h_QCD->Draw("Lsame");
	h_DATA->Draw("PEsame");
	
	leg = new TLegend(legXmin,legYmin,legXmax,legYmax);
	if (legend_header!="none") leg->SetHeader( legend_header.c_str() );
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
	h_STACK->SetLineWidth(1);
	h_STACK->SetFillColor((16)); //old way->kRed
	h_STACK->SetFillStyle(3654); //3XYZ. X=(1-9) space between hatch, Y=(0-9) angle between 0 and 90 degrees (5 = Not drawn). Z= opposite line
	h_STACK_noErrors->SetLineColor((kRed));
	h_STACK_noErrors->SetFillColor((kRed)); //old way->Delete this
	h_STACK_noErrors->SetLineWidth(1); //3
	
	h_QCD_noErrors->SetLineWidth(1);//2
	h_QCD_noErrors->SetLineColor(kYellow); //1
	h_QCD_noErrors->SetFillColor(kYellow);
	
	cout<<"h_DATA "<<h_DATA->GetNbinsX()<<endl;
	cout<<"h_QCD "<<h_QCD->GetNbinsX()<<endl;
	cout<<"h_QCD_noErrors "<<h_QCD_noErrors->GetNbinsX()<<endl;
	cout<<"h_STACK "<<h_STACK->GetNbinsX()<<endl;
	cout<<"h_STACK_noErrors "<<h_STACK_noErrors->GetNbinsX()<<endl;
	
	/*
	h_STACK->Draw("9E2");
	h_DATA->Draw("PEsame");
	h_QCD_noErrors->Draw("same");
	h_STACK->Draw("9E2same");
	h_STACK_noErrors->Draw("same");
	h_DATA->Draw("PEsame");
*/
	h_DATA->Draw("PE");
	h_STACK->Draw("9E2same");
	h_DATA->Draw("PEsame");
	h_QCD_noErrors->Draw("same");
	h_STACK->Draw("9E2same");
	h_STACK_noErrors->Draw("same");
	h_QCD_noErrors->Draw("same");
	h_STACK->Draw("9E2same");
	h_DATA->Draw("PEsame");

	leg = new TLegend(legXmin,legYmin,legXmax,legYmax);
	leg->SetBorderSize(1);
	leg->SetFillColor(0);
	if (legend_header!="none") leg->SetHeader( legend_header.c_str() );
	leg->AddEntry(	h_DATA,				L1.c_str(),"LP");
	leg->AddEntry(	h_QCD_noErrors,		L2.c_str(),"F");
	leg->AddEntry(	h_STACK_noErrors,	L3.c_str(),"F");
	leg->Draw("same");

	//TPaveText *textbox = new TPaveText(legXmin-0.01,legYmin-0.11,legXmax-0.05,legYmin-0.01,"NDC");
	TPaveText *textbox = new TPaveText(legXmin-0.02,legYmin-0.09,legXmax-0.06,legYmin-0.01,"NDC");
	textbox->SetFillColor(0);
	textbox->SetLineColor(0);
	TText *line1 = textbox->AddText("CMS Preliminary");
	line1->SetTextColor(1);
	line1->SetTextAlign(12); //first number = horizontal alignment (1 left, 2 center, 3 right). second number =vertical alignment (1 top, 2 center, 3 bottom)
	TText *line2 = textbox->AddText("187.8 pb^{-1} at #sqrt{s} = 7 TeV");
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

void Draw3EffPlots(
	TH1D* h1,
	TH1D* h2,
	TH1D* h3, 
	std::string title,
	std::string legend_header,
	std::string L1, 
	std::string L2, 
	std::string L3, 
	double legXmin, double legYmin, double legXmax, double legYmax, 
	std::string savename, )
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
	
	
	
	string savenamepdf = savename + ".pdf";
	string savenamepng = savename + ".png";
	string savenameeps = savename + ".eps";
	
	h1->SetMarkerStyle(20);
	h1->SetMarkerColor(1);
	h1->SetLineColor(1);
	
	h2->SetMarkerStyle(21);
	h2->SetMarkerColor(2);
	h2->SetLineColor(2);
	
	h3->SetMarkerStyle(22);
	h3->SetMarkerColor(4);
	h3->SetLineColor(4);
	

	h1->Draw();
	h2->Draw("same");
	h3->Draw("same");

	leg3 = new TLegend(0.2,0.7,0.5,0.92);
	leg3->SetHeader(legend_header.c_str());
	leg3->SetBorderSize(1);
	leg3->SetFillColor(0);
	leg3->AddEntry(h1,L1.c_str(),"LP");
	leg3->AddEntry(h2,L2.c_str(),"LP");
	leg3->AddEntry(h3,L3.c_str(),"LP");
	leg3->Draw("same");
	
	gPad->RedrawAxis();

	c1000->SaveAs(savenamepdf.c_str());
	c1000->SaveAs(savenamepng.c_str());
	c1000->SaveAs(savenameeps.c_str());

	//--------------------------------------------------------------------

	delete c1000;
	rebin = -1;	
}






void DivideTwoHists(
	TFile* file1,
	TFile* file2,
	TFile* file3,
	std::string histname,//TH1D* h_DATA,
	std::string title, 
	std::string L2, 
	std::string L3, 
	double legXmin, double legYmin, double legXmax, double legYmax, 
	double YaxisTitleOffset, 
	std::string savename, 
	int rebin, 
	double lowerbound, 
	double upperbound,
	double ymin, 
	double ymax,
	int color1,
	int color2)
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
	


	
	TH1D * h1	=  file1 -> Get( histname.c_str() );
	TH1D * h2	=  file2 -> Get( histname.c_str() );
	TH1D * h3	=  file3 -> Get( histname.c_str() );

	h1->Rebin(rebin);
	h2->Rebin(rebin);
	h3->Rebin(rebin);

	h2->SetLineColor(color1);
	h3->SetLineColor(color2);
	
	h1->SetTitle(title.c_str());
	h2->SetTitle(title.c_str());
	h3->SetTitle(title.c_str());
	
	cout<<h1->GetEntries()<<endl;
	cout<<h2->GetEntries()<<endl;
	cout<<h3->GetEntries()<<endl;


	h1->Sumw2();
	h2->Sumw2();
	h3->Sumw2();

	h1->Scale(1/h1->GetEntries() );
	h2->Scale(1/h2->GetEntries() );
	h3->Scale(1/h3->GetEntries() );

	cout<<savename<<endl;
	
	double cut1_count1 = h1->Integral(  h1->FindBin(140.),h1->FindFirstBinAbove(250.) );
	double cut1_count2 = h2->Integral(  h2->FindBin(140.),h2->FindFirstBinAbove(250.) );
	double cut1_count3 = h3->Integral(  h3->FindBin(140.),h3->FindFirstBinAbove(250.) );
	
	double cut2_count1 = h1->Integral(  h1->FindBin(50), h1->GetNbinsX() );
	double cut2_count2 = h2->Integral(  h2->FindBin(50), h2->GetNbinsX() );
	double cut2_count3 = h3->Integral(  h3->FindBin(50), h3->GetNbinsX() );
	
	double cut3_count1 = h1->Integral(  h1->FindBin(200), h1->GetNbinsX() );
	double cut3_count2 = h2->Integral(  h2->FindBin(200), h2->GetNbinsX() );
	double cut3_count3 = h3->Integral(  h3->FindBin(200), h3->GetNbinsX() );
	
	double cut4_count1 = h1->Integral(  h1->FindBin(250), h1->GetNbinsX() );
	double cut4_count2 = h2->Integral(  h2->FindBin(250), h2->GetNbinsX() );
	double cut4_count3 = h3->Integral(  h3->FindBin(250), h3->GetNbinsX() );
		
	if (cut1_count1!=0)
	{
		double div2 = cut1_count2/cut1_count1;
		double div3 = cut1_count3/cut1_count1;
		cout<<"140-250   div2 "<<div2<<"  div3 "<<div3<<endl;
	}
	
	if (cut2_count1!=0)
	{
		double div2 = cut2_count2/cut2_count1;
		double div3 = cut2_count3/cut2_count1;
		cout<<"50->inf   div2 "<<div2<<"  div3 "<<div3<<endl;
	}
		
	if (cut3_count1!=0)
	{
		double div2 = cut3_count2/cut3_count1;
		double div3 = cut3_count3/cut3_count1;
		cout<<"200->inf   div2 "<<div2<<"  div3 "<<div3<<endl;
	}
		
	if (cut4_count1!=0)
	{
		double div2 = cut4_count2/cut4_count1;
		double div3 = cut4_count3/cut4_count1;
		cout<<"250-inf   div2 "<<div2<<"  div3 "<<div3<<endl;
	}
	
	
	
	
	
	
	
	
	h2->Divide(h2,h1,1,1,"B");
	h3->Divide(h3,h1,1,1,"B");
	/*
	vector<double> v;
	v.push_back(h2->GetMaximum());
	v.push_back(h3->GetMaximum());
	vector<double>::const_iterator largest = max_element(v.begin(),v.end());	
	double max  = *largest;

	vector<double> w;
	w.push_back(h2->GetMinimum());
	w.push_back(h3->GetMinimum());
	vector<double>::const_iterator smallest = min_element(w.begin(),w.end());	
	double min  = *smallest;

	cout<<"h2->GetMaximum() "<<h2->GetMaximum()<<endl;
	cout<<"h3->GetMaximum() "<<h3->GetMaximum()<<endl;
	cout<<"h2->GetMinimum() "<<h2->GetMinimum()<<endl;
	cout<<"h3->GetMinimum() "<<h3->GetMinimum()<<endl;
	cout<<"max "<<max<<"  min "<<min<<endl;
	
	h2->GetYaxis()->SetRangeUser(min,max);
	h3->GetYaxis()->SetRangeUser(min,max);
*/
	h1->GetYaxis()->SetRangeUser(ymin,ymax);
	h2->GetYaxis()->SetRangeUser(ymin,ymax);
	h3->GetYaxis()->SetRangeUser(ymin,ymax);

	if ( lowerbound!=-1 && upperbound!=-1)
	{
		h1->GetXaxis()->SetRangeUser(lowerbound,upperbound);
		h2->GetXaxis()->SetRangeUser(lowerbound,upperbound);
		h3->GetXaxis()->SetRangeUser(lowerbound,upperbound);
	}

	h2->Draw("E");
	h3->Draw("Esame");
	leg3 = new TLegend(legXmin,legYmin,legXmax,legYmax);
	leg3->SetBorderSize(1);
	leg3->SetFillColor(0);
	leg3->AddEntry(h2,L2.c_str(),"L");
	leg3->AddEntry(h3,L3.c_str(),"L");
	leg3->Draw("same");
	
		
	string savename_pdf = savename + ".pdf";
	string savename_png = savename + ".png";
	string savename_eps = savename + ".eps";

	
	c1000->SaveAs(savename_png.c_str());
	c1000->SaveAs(savename_pdf.c_str());
	c1000->SaveAs(savename_eps.c_str());

	//--------------------------------------------------------------------

	delete c1000;
	delete h1;
	delete h2;
	delete h3;
	rebin = -1;	
}




int countinrange(vector<double>& table,double lo,double hi)
{
    int num=0;
    for (int i=0;i<table.size();i++)
        if ((lo <= table[i]) && (table[i] < hi))
            num++;
    return(num);
}


void CompareHists(vector<A> &test)
{
	for (int i = 0; i<test.size();i++)
	{
		cout<<test<<endl;
	}
}

void CompareHistsBackup(
	TFile* file,
	std::string histname1,//TH1D* h_DATA,
	std::string histname2,//TH1D* h_QCD,
	std::string histname3,//TH1D* h_TTBAR, 
	std::string title,
	std::string legend_header,
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
	if (histname3!="none") TH1F* h_TTBAR =  file -> Get( histname3.c_str() );	
	if (histname3=="none") TH1F* h_TTBAR = new TH1F("h","h",500,0,4000);	
	
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
	cout<<"h_DATA "<<h_DATA->GetNbinsX()<<endl;
	cout<<"h_QCD "<<h_QCD->GetNbinsX()<<endl;
	cout<<"h_QCD_noErrors "<<h_QCD_noErrors->GetNbinsX()<<endl;
	cout<<"h_STACK "<<h_STACK->GetNbinsX()<<endl;
	cout<<"h_STACK_noErrors "<<h_STACK_noErrors->GetNbinsX()<<endl;
	
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
	h_QCD->SetLineColor(0);
	h_QCD->SetLineWidth(0);
	h_QCD->SetFillColor(kGreen);
	h_QCD->SetFillStyle(3354);
	h_QCD_noErrors->SetLineColor(kGreen);
	h_QCD_noErrors->SetLineWidth(3);
	
	cout<<"h_DATA "<<h_DATA->GetNbinsX()<<endl;
	cout<<"h_QCD "<<h_QCD->GetNbinsX()<<endl;
	cout<<"h_QCD_noErrors "<<h_QCD_noErrors->GetNbinsX()<<endl;
	
	h_DATA->Draw("PE");
	h_QCD->Draw("9E2same");
	h_QCD_noErrors->Draw("same");

	h_QCD->Draw("Lsame");
	h_DATA->Draw("PEsame");
	
	leg = new TLegend(legXmin,legYmin,legXmax,legYmax);
	if (legend_header!="none") leg->SetHeader( legend_header.c_str() );
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
	
	cout<<"h_DATA "<<h_DATA->GetNbinsX()<<endl;
	cout<<"h_QCD "<<h_QCD->GetNbinsX()<<endl;
	cout<<"h_QCD_noErrors "<<h_QCD_noErrors->GetNbinsX()<<endl;
	cout<<"h_STACK "<<h_STACK->GetNbinsX()<<endl;
	cout<<"h_STACK_noErrors "<<h_STACK_noErrors->GetNbinsX()<<endl;
	
	
	h_DATA->Draw("PE");
	h_QCD_noErrors->Draw("same");
	h_STACK->Draw("9E2same");
	h_STACK_noErrors->Draw("same");
	h_DATA->Draw("PEsame");

	leg = new TLegend(legXmin,legYmin,legXmax,legYmax);
	leg->SetBorderSize(1);
	leg->SetFillColor(0);
	if (legend_header!="none") leg->SetHeader( legend_header.c_str() );
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


void Draw4HistogramsNormalized(TH1F* h1, TH1F* h2, TH1F* h3, TH1F* h4, std::string title, std::string L1, std::string L2, std::string L3, std::string L4, double legXmin, double legYmin, double legXmax, double legYmax, std::string savename){
	
	using namespace std;
	
	//make ROOT pretty
	gROOT->SetStyle("Plain");
	//gStyle->SetOptStat(111111);
	//gStyle->SetStatColor();
	gStyle->SetOptStat(0);
	//gStyle->SetPalette(52,0); // if you want to make a PINK palette, comment out this line
	gStyle->SetPadLeftMargin(0.11);
	gStyle->SetPadRightMargin(0.03);
	gStyle->SetTitleYOffset(1.4);
	//gStyle->SetTitleXOffset(0.85);
	//gStyle->SetTitleXSize(0.05);
	//gStyle->SetTitleYSize(0.05);
	//gStyle->SetStatBorderSize(5);
	gStyle->SetHistLineWidth(2);
	gStyle->SetTitleBorderSize(0);
	//gStyle->SetTitleFontSize(0.06);//just added
	//gStyle->SetTitleSize(30);
	gStyle->SetTitleX(0.17);
	gStyle->SetTitleY(0.99);
	gROOT->UseCurrentStyle();
	gROOT->ForceStyle();
	
	
	
	TCanvas *c1 = new TCanvas("c1","",10,10,700,550);
	
	
	double m1=h1->GetMaximum()/h1->Integral();
	double m2=h2->GetMaximum()/h2->Integral();
	double m3=h3->GetMaximum()/h3->Integral();
	double m4=h4->GetMaximum()/h4->Integral();
	
	vector<double> v;
	v.push_back(m1);
	v.push_back(m2);
	v.push_back(m3);
	v.push_back(m4);
	/*for(vector<double>::const_iterator it = v.begin(); it != v.end(); ++it)
	 {
	 cout << *it << " ";
	 }*/
	vector<double>::const_iterator largest = max_element(v.begin(),v.end());
	
	double max  = *largest;
	
	cout<<m1<<" "<<m2<<" "<<m3<<" "<<m4<<" max = "<<max<<endl;
	
	h1->SetLineColor(1);
	h2->SetLineColor(2);
	h3->SetLineColor(3);
	h4->SetLineColor(4);
	
	
	
	if(m1==max){
		h1->SetTitle(title.c_str());
		h1->Draw();
		h2->Draw("same");
		h3->Draw("same");
		h4->Draw("same");
		
	}	
	if(m2==max){
		h2->SetTitle(title.c_str());
		h2->Draw();
		h1->Draw("same");
		h3->Draw("same");
		h4->Draw("same");
	}
	if(m3==max){
		h3->SetTitle(title.c_str());
		h3->Draw();
		h2->Draw("same");
		h1->Draw("same");
		h4->Draw("same");
	}
	if(m4==max){
		h4->SetTitle(title.c_str());
		h4->Draw();
		h2->Draw("same");
		h3->Draw("same");
		h1->Draw("same");
	}
	
	leg = new TLegend(legXmin,legYmin,legXmax,legYmax);
	leg->SetBorderSize(0);
	leg->SetFillColor(0);
	leg->AddEntry(h1,L1.c_str(),"L");
	leg->AddEntry(h2,L2.c_str(),"L");
	leg->AddEntry(h3,L3.c_str(),"L");
	leg->AddEntry(h4,L4.c_str(),"L");
	leg->Draw("same");
	
	
	c1->Update();
	c1->Print(savename.c_str(),"png");
	delete c1;
	
}













void PrintCounts( TFile* file )
{


	TH1D * Nevents_analyzed							=  file -> Get("cascadingQCDAna15/Nevents_analyzed");
	TH1D * Nevents_preselected						=  file -> Get("cascadingQCDAna15/Nevents_preselected");
	
	TH1D * Nevents_hasTaggedTopJet0					=  file -> Get("cascadingQCDAna15/Nevents_hasTaggedTopJet0");
	TH1D * Nevents_hasTaggedTopJet1					=  file -> Get("cascadingQCDAna15/Nevents_hasTaggedTopJet1");
	TH1D * Nevents_hasZeroTopTags					=  file -> Get("cascadingQCDAna15/Nevents_hasZeroTopTags");
	TH1D * Nevents_hasOneTopTag						=  file -> Get("cascadingQCDAna15/Nevents_hasOneTopTag");
	TH1D * Nevents_hasTwoTopTags					=  file -> Get("cascadingQCDAna15/Nevents_hasTwoTopTags");
	
	TH1D * Nevents_hasWTag0							=  file -> Get("cascadingQCDAna15/Nevents_hasWTag0");
	TH1D * Nevents_hasWTag1							=  file -> Get("cascadingQCDAna15/Nevents_hasWTag1");
	TH1D * Nevents_hasZeroWTags						=  file -> Get("cascadingQCDAna15/Nevents_hasZeroWTags");
	TH1D * Nevents_hasOneWTag						=  file -> Get("cascadingQCDAna15/Nevents_hasOneWTag");
	TH1D * Nevents_hasTwoWTags						=  file -> Get("cascadingQCDAna15/Nevents_hasTwoWTags");
	
	TH1D * Nevents_hasBTag0							=  file -> Get("cascadingQCDAna15/Nevents_hasBTag0");
	TH1D * Nevents_hasBTag1							=  file -> Get("cascadingQCDAna15/Nevents_hasBTag1");
	TH1D * Nevents_hasZeroBTags						=  file -> Get("cascadingQCDAna15/Nevents_hasZeroBTags");
	TH1D * Nevents_hasOneBTag						=  file -> Get("cascadingQCDAna15/Nevents_hasOneBTag");
	TH1D * Nevents_hasTwoBTags						=  file -> Get("cascadingQCDAna15/Nevents_hasTwoBTags");
	
	TH1D * Nevents_hasTightTop0						=  file -> Get("cascadingQCDAna15/Nevents_hasTightTop0");
	TH1D * Nevents_hasTightTop1						=  file -> Get("cascadingQCDAna15/Nevents_hasTightTop1");
	TH1D * Nevents_hasZeroTightTops					=  file -> Get("cascadingQCDAna15/Nevents_hasZeroTightTops");
	TH1D * Nevents_hasOneTightTop					=  file -> Get("cascadingQCDAna15/Nevents_hasOneTightTop");
	TH1D * Nevents_hasTwoTightTops					=  file -> Get("cascadingQCDAna15/Nevents_hasTwoTightTops");
	
	TH1D * Nevents_hasLooseTop0						=  file -> Get("cascadingQCDAna15/Nevents_hasLooseTop0");
	TH1D * Nevents_hasLooseTop1						=  file -> Get("cascadingQCDAna15/Nevents_hasLooseTop1");
	TH1D * Nevents_hasZeroLooseTops					=  file -> Get("cascadingQCDAna15/Nevents_hasZeroLooseTops");
	TH1D * Nevents_hasOneLooseTop					=  file -> Get("cascadingQCDAna15/Nevents_hasOneLooseTop");
	TH1D * Nevents_hasTwoLooseTops					=  file -> Get("cascadingQCDAna15/Nevents_hasTwoLooseTops");
	
	TH1D * Nevents_hasOneLooseOneTightTop			=  file -> Get("cascadingQCDAna15/Nevents_hasOneLooseOneTightTop");
	TH1D * Nevents_hemiWithWandB					=  file -> Get("cascadingQCDAna15/Nevents_hemiWithWandB");
	TH1D * Nevents_hemiWithWandUntagged				=  file -> Get("cascadingQCDAna15/Nevents_hemiWithWandUntagged");

	TH1D * Nevents_TopTagAndTightTop				=  file -> Get("cascadingQCDAna15/Nevents_TopTagAndTightTop");
	TH1D * Nevents_TopTagAndLooseTop				=  file -> Get("cascadingQCDAna15/Nevents_TopTagAndLooseTop");
	TH1D * Nevents_TopTagAndWandB					=  file -> Get("cascadingQCDAna15/Nevents_TopTagAndWandB");
	TH1D * Nevents_hasTwoWTags_hasOneBTag			=  file -> Get("cascadingQCDAna15/Nevents_hasTwoWTags_hasOneBTag");
	TH1D * Nevents_hasTwoWTags_hasTwoBTags			=  file -> Get("cascadingQCDAna15/Nevents_hasTwoWTags_hasTwoBTags");
	TH1D * Nevents_TightTopAndLooseTop				=  file -> Get("cascadingQCDAna15/Nevents_TightTopAndLooseTop");
	TH1D * Nevents_hasOneTopJet_noNonLeadingBjet	=  file -> Get("cascadingQCDAna15/Nevents_hasOneTopJet_noNonLeadingBjet");

	TH1D * Nevents_hemiTop_hemiBnoW					=  file -> Get("cascadingQCDAna15/Nevents_hemiTop_hemiBnoW");
	TH1D * Nevents_hasBTag							=  file -> Get("cascadingQCDAna15/Nevents_hasBTag");
	TH1D * Nevents_hasBTag_noWTag					=  file -> Get("cascadingQCDAna15/Nevents_hasBTag_noWTag");

	TH1D * Nevents_type11sig						=  file -> Get("cascadingQCDAna15/Nevents_type11sig");
	TH1D * Nevents_type12sig						=  file -> Get("cascadingQCDAna15/Nevents_type12sig");
	TH1D * Nevents_type22sig						=  file -> Get("cascadingQCDAna15/Nevents_type22sig");
	TH1D * Nevents_type11bkg						=  file -> Get("cascadingQCDAna15/Nevents_type11bkg");
	TH1D * Nevents_type12bkg						=  file -> Get("cascadingQCDAna15/Nevents_type12bkg");
	TH1D * Nevents_type22bkg						=  file -> Get("cascadingQCDAna15/Nevents_type22bkg");

	TH1D * Nevents_cascade12sig						=  file -> Get("cascadingQCDAna15/Nevents_cascade12sig");
	TH1D * Nevents_cascade22sig						=  file -> Get("cascadingQCDAna15/Nevents_cascade22sig");
	TH1D * Nevents_cascade11bkg						=  file -> Get("cascadingQCDAna15/Nevents_cascade11bkg");
	TH1D * Nevents_cascade12bkg						=  file -> Get("cascadingQCDAna15/Nevents_cascade12bkg");
	TH1D * Nevents_cascade22bkg						=  file -> Get("cascadingQCDAna15/Nevents_cascade22bkg");

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

	cout<<"Nevents_TopTagAndTightTop                "<<Nevents_TopTagAndTightTop->GetEntries()<<endl;
	cout<<"Nevents_TopTagAndLooseTop                "<<Nevents_TopTagAndLooseTop->GetEntries()<<endl;
	cout<<"Nevents_TopTagAndWandB                   "<<Nevents_TopTagAndWandB->GetEntries()<<endl;
	cout<<"Nevents_hasTwoWTags_hasOneBTag           "<<Nevents_hasTwoWTags_hasOneBTag->GetEntries()<<endl;
	cout<<"Nevents_hasTwoWTags_hasTwoBTags          "<<Nevents_hasTwoWTags_hasTwoBTags->GetEntries()<<endl;
	cout<<"Nevents_TightTopAndLooseTop              "<<Nevents_TightTopAndLooseTop->GetEntries()<<endl;
	cout<<"Nevents_hasOneTopJet_noNonLeadingBjet    "<<Nevents_hasOneTopJet_noNonLeadingBjet->GetEntries()<<endl<<endl;

	cout<<"Nevents_hemiTop_hemiBnoW    "<<Nevents_hemiTop_hemiBnoW->GetEntries()<<endl;
	cout<<"Nevents_hasBTag             "<<Nevents_hasBTag->GetEntries()<<endl;
	cout<<"Nevents_hasBTag_noWTag      "<<Nevents_hasBTag_noWTag->GetEntries()<<endl<<endl;

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
	
	
	TH1D * Nevents_succesiveCuts_type12bkg	= file -> Get("cascadingQCDAna15/Nevents_succesiveCuts_type12bkg");
	cout<<"type12bkg before cuts                                "<<Nevents_succesiveCuts_type12bkg->GetBinContent(1)<<endl;
	cout<<"type12bkg cascade cuts                               "<<Nevents_succesiveCuts_type12bkg->GetBinContent(2)<<endl;
	cout<<"type12bkg hasBTag && !hasWTag0 && !hasWTag1          "<<Nevents_succesiveCuts_type12bkg->GetBinContent(3)<<endl;
	cout<<"type12bkg hasTaggedTopJet0  && !hasWTag1 && hasBTag1 "<<Nevents_succesiveCuts_type12bkg->GetBinContent(4)<<endl;
	cout<<"type12bkg noTags1.size() !=0                         "<<Nevents_succesiveCuts_type12bkg->GetBinContent(5)<<endl;
	cout<<"type12bkg mass cuts                                  "<<Nevents_succesiveCuts_type12bkg->GetBinContent(6)<<endl;
	cout<<"type12bkg pt cuts                                    "<<Nevents_succesiveCuts_type12bkg->GetBinContent(7)<<endl<<endl;
	
	TH1D * Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg_DATA	= file -> Get("cascadingQCDAna15/Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg");
	cout<<"11sig "<<Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg_DATA->GetBinContent(1)<<endl;
	cout<<"12sig "<<Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg_DATA->GetBinContent(2)<<endl;
	cout<<"22sig "<<Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg_DATA->GetBinContent(3)<<endl;
	cout<<"11bkg "<<Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg_DATA->GetBinContent(4)<<endl;
	cout<<"12bkg "<<Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg_DATA->GetBinContent(5)<<endl;
	cout<<"22bkg "<<Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg_DATA->GetBinContent(6)<<endl<<endl;

				
	TH1D * Nevents_22_tighttight_tightloose			=  file -> Get("cascadingQCDAna15/Nevents_22_tighttight_tightloose");
	cout<<"Nevents_22_tighttight_tightloose tight-tight "<<Nevents_22_tighttight_tightloose->GetBinContent(1)<<endl;
	cout<<"Nevents_22_tighttight_tightloose tight-loose "<<Nevents_22_tighttight_tightloose->GetBinContent(2)<<endl<<endl;

	TH1D * Nevents_12_tight_loose					=  file -> Get("cascadingQCDAna15/Nevents_12_tight_loose");
	cout<<"Nevents_12_tight_loose tight "<<Nevents_12_tight_loose->GetBinContent(1)<<endl;
	cout<<"Nevents_12_tight_loose loose "<<Nevents_12_tight_loose->GetBinContent(2)<<endl<<endl;


	TH1D * Nevents_Type22_Case123					=  file -> Get("cascadingQCDAna15/Nevents_Type22_Case123");
	cout<<"Nevents_Type22_Case123 1 "<<Nevents_Type22_Case123->GetBinContent(1)<<endl;
	cout<<"Nevents_Type22_Case123 2 "<<Nevents_Type22_Case123->GetBinContent(2)<<endl;
	cout<<"Nevents_Type22_Case123 3 "<<Nevents_Type22_Case123->GetBinContent(3)<<endl<<endl;
	
	TH1D * Nevents_PassCuts_DATA					=  file -> Get("cascadingQCDAna15/Nevents_PassCuts");
	cout<<"Nevents_PassCuts 1 "<<Nevents_PassCuts_DATA->GetBinContent(1)<<"  = number considered by analyzer "<<endl;
	cout<<"Nevents_PassCuts 2 "<<Nevents_PassCuts_DATA->GetBinContent(2)<<"  = passType11 && passType22 && ca8Jets_.size()>=2"<<endl;
	cout<<"Nevents_PassCuts 3 "<<Nevents_PassCuts_DATA->GetBinContent(3)<<"  = preselected_event"<<endl;
	cout<<"Nevents_PassCuts 4 "<<Nevents_PassCuts_DATA->GetBinContent(4)<<"  = pass type 1+2"<<endl;
	cout<<"Nevents_PassCuts 5 "<<Nevents_PassCuts_DATA->GetBinContent(5)<<"  = pass type 2+2"<<endl;
	cout<<"Nevents_PassCuts 6 "<<Nevents_PassCuts_DATA->GetBinContent(6)<<"  = 1+1 bkdg estimation"<<endl<<endl;
	
	
	cout<<"LaTeX table format"<<endl;
	
	
	cout<<"Nevents_analyzed         "<<Nevents_analyzed->GetEntries()<<endl;
	cout<<"Nevents_preselected      "<<Nevents_preselected->GetEntries()<<endl<<endl;

	cout<<"Nevents_hasTaggedTopJet0 "<<Nevents_hasTaggedTopJet0->GetEntries()<<endl;
	cout<<"Nevents_hasTaggedTopJet1 "<<Nevents_hasTaggedTopJet1->GetEntries()<<endl;
	cout<<"Nevents_hasZeroTopTags   "<<Nevents_hasZeroTopTags->GetEntries()<<endl;
	cout<<"Nevents_hasOneTopTag     "<<Nevents_hasOneTopTag->GetEntries()<<endl;
	cout<<"Nevents_hasTwoTopTags    "<<Nevents_hasTwoTopTags->GetEntries()<<endl;
	cout<<"0+1+2                    "<<Nevents_hasZeroTopTags->GetEntries() + Nevents_hasOneTopTag->GetEntries()+ Nevents_hasTwoTopTags->GetEntries() <<endl<<endl;

	
	cout << "\hline"<<endl;
	cout << " Total & "<< Nevents_analyzed->GetEntries() << " & " << Nevents_analyzed->GetEntries() << " \\ \hline"<<endl;
   
	

}


void PrintLatexTable( TFile* file1, TFile* file2, TFile* file3, TFile* file4, TFile* file5, TFile* file6 )
{


	TH1D * Nevents1_analyzed						=  file1 -> Get("cascadingQCDAna15/Nevents_analyzed");
	TH1D * Nevents1_preselected						=  file1 -> Get("cascadingQCDAna15/Nevents_preselected");
	
	TH1D * Nevents1_hasTaggedTopJet0				=  file1 -> Get("cascadingQCDAna15/Nevents_hasTaggedTopJet0");
	TH1D * Nevents1_hasTaggedTopJet1				=  file1 -> Get("cascadingQCDAna15/Nevents_hasTaggedTopJet1");
	TH1D * Nevents1_hasZeroTopTags					=  file1 -> Get("cascadingQCDAna15/Nevents_hasZeroTopTags");
	TH1D * Nevents1_hasOneTopTag					=  file1 -> Get("cascadingQCDAna15/Nevents_hasOneTopTag");
	TH1D * Nevents1_hasTwoTopTags					=  file1 -> Get("cascadingQCDAna15/Nevents_hasTwoTopTags");
	
	TH1D * Nevents1_hasWTag0						=  file1 -> Get("cascadingQCDAna15/Nevents_hasWTag0");
	TH1D * Nevents1_hasWTag1						=  file1 -> Get("cascadingQCDAna15/Nevents_hasWTag1");
	TH1D * Nevents1_hasZeroWTags					=  file1 -> Get("cascadingQCDAna15/Nevents_hasZeroWTags");
	TH1D * Nevents1_hasOneWTag						=  file1 -> Get("cascadingQCDAna15/Nevents_hasOneWTag");
	TH1D * Nevents1_hasTwoWTags						=  file1 -> Get("cascadingQCDAna15/Nevents_hasTwoWTags");
	       
	TH1D * Nevents1_hasBTag0						=  file1 -> Get("cascadingQCDAna15/Nevents_hasBTag0");
	TH1D * Nevents1_hasBTag1						=  file1 -> Get("cascadingQCDAna15/Nevents_hasBTag1");
	TH1D * Nevents1_hasZeroBTags					=  file1 -> Get("cascadingQCDAna15/Nevents_hasZeroBTags");
	TH1D * Nevents1_hasOneBTag						=  file1 -> Get("cascadingQCDAna15/Nevents_hasOneBTag");
	TH1D * Nevents1_hasTwoBTags						=  file1 -> Get("cascadingQCDAna15/Nevents_hasTwoBTags");
	
	TH1D * Nevents1_hasTightTop0					=  file1 -> Get("cascadingQCDAna15/Nevents_hasTightTop0");
	TH1D * Nevents1_hasTightTop1					=  file1 -> Get("cascadingQCDAna15/Nevents_hasTightTop1");
	TH1D * Nevents1_hasZeroTightTops				=  file1 -> Get("cascadingQCDAna15/Nevents_hasZeroTightTops");
	TH1D * Nevents1_hasOneTightTop					=  file1 -> Get("cascadingQCDAna15/Nevents_hasOneTightTop");
	TH1D * Nevents1_hasTwoTightTops					=  file1 -> Get("cascadingQCDAna15/Nevents_hasTwoTightTops");
	
	TH1D * Nevents1_hasLooseTop0					=  file1 -> Get("cascadingQCDAna15/Nevents_hasLooseTop0");
	TH1D * Nevents1_hasLooseTop1					=  file1 -> Get("cascadingQCDAna15/Nevents_hasLooseTop1");
	TH1D * Nevents1_hasZeroLooseTops				=  file1 -> Get("cascadingQCDAna15/Nevents_hasZeroLooseTops");
	TH1D * Nevents1_hasOneLooseTop					=  file1 -> Get("cascadingQCDAna15/Nevents_hasOneLooseTop");
	TH1D * Nevents1_hasTwoLooseTops					=  file1 -> Get("cascadingQCDAna15/Nevents_hasTwoLooseTops");
	
	TH1D * Nevents1_hasOneLooseOneTightTop			=  file1 -> Get("cascadingQCDAna15/Nevents_hasOneLooseOneTightTop");
	TH1D * Nevents1_hemiWithWandB					=  file1 -> Get("cascadingQCDAna15/Nevents_hemiWithWandB");
	TH1D * Nevents1_hemiWithWandUntagged			=  file1 -> Get("cascadingQCDAna15/Nevents_hemiWithWandUntagged");

	TH1D * Nevents1_TopTagAndTightTop				=  file1 -> Get("cascadingQCDAna15/Nevents_TopTagAndTightTop");
	TH1D * Nevents1_TopTagAndLooseTop				=  file1 -> Get("cascadingQCDAna15/Nevents_TopTagAndLooseTop");
	TH1D * Nevents1_TopTagAndWandB					=  file1 -> Get("cascadingQCDAna15/Nevents_TopTagAndWandB");
	TH1D * Nevents1_hasTwoWTags_hasOneBTag			=  file1 -> Get("cascadingQCDAna15/Nevents_hasTwoWTags_hasOneBTag");
	TH1D * Nevents1_hasTwoWTags_hasTwoBTags			=  file1 -> Get("cascadingQCDAna15/Nevents_hasTwoWTags_hasTwoBTags");
	TH1D * Nevents1_TightTopAndLooseTop				=  file1 -> Get("cascadingQCDAna15/Nevents_TightTopAndLooseTop");
	TH1D * Nevents1_hasOneTopJet_noNonLeadingBjet	=  file1 -> Get("cascadingQCDAna15/Nevents_hasOneTopJet_noNonLeadingBjet");

	TH1D * Nevents1_hemiTop_hemiBnoW				=  file1 -> Get("cascadingQCDAna15/Nevents_hemiTop_hemiBnoW");
	TH1D * Nevents1_hasBTag							=  file1 -> Get("cascadingQCDAna15/Nevents_hasBTag");
	TH1D * Nevents1_hasBTag_noWTag					=  file1 -> Get("cascadingQCDAna15/Nevents_hasBTag_noWTag");

	TH1D * Nevents1_type11sig						=  file1 -> Get("cascadingQCDAna15/Nevents_type11sig");
	TH1D * Nevents1_type12sig						=  file1 -> Get("cascadingQCDAna15/Nevents_type12sig");
	TH1D * Nevents1_type22sig						=  file1 -> Get("cascadingQCDAna15/Nevents_type22sig");
	TH1D * Nevents1_type11bkg						=  file1 -> Get("cascadingQCDAna15/Nevents_type11bkg");
	TH1D * Nevents1_type12bkg						=  file1 -> Get("cascadingQCDAna15/Nevents_type12bkg");
	TH1D * Nevents1_type22bkg						=  file1 -> Get("cascadingQCDAna15/Nevents_type22bkg");

	TH1D * Nevents1_cascade12sig					=  file1 -> Get("cascadingQCDAna15/Nevents_cascade12sig");
	TH1D * Nevents1_cascade22sig					=  file1 -> Get("cascadingQCDAna15/Nevents_cascade22sig");
	TH1D * Nevents1_cascade11bkg					=  file1 -> Get("cascadingQCDAna15/Nevents_cascade11bkg");
	TH1D * Nevents1_cascade12bkg					=  file1 -> Get("cascadingQCDAna15/Nevents_cascade12bkg");
	TH1D * Nevents1_cascade22bkg					=  file1 -> Get("cascadingQCDAna15/Nevents_cascade22bkg");

	//---------------------------------------------------------------
	

	TH1D * Nevents2_analyzed						=  file2 -> Get("cascadingQCDAna15/Nevents_analyzed");
	TH1D * Nevents2_preselected						=  file2 -> Get("cascadingQCDAna15/Nevents_preselected");
	
	TH1D * Nevents2_hasTaggedTopJet0				=  file2 -> Get("cascadingQCDAna15/Nevents_hasTaggedTopJet0");
	TH1D * Nevents2_hasTaggedTopJet1				=  file2 -> Get("cascadingQCDAna15/Nevents_hasTaggedTopJet1");
	TH1D * Nevents2_hasZeroTopTags					=  file2 -> Get("cascadingQCDAna15/Nevents_hasZeroTopTags");
	TH1D * Nevents2_hasOneTopTag					=  file2 -> Get("cascadingQCDAna15/Nevents_hasOneTopTag");
	TH1D * Nevents2_hasTwoTopTags					=  file2 -> Get("cascadingQCDAna15/Nevents_hasTwoTopTags");
	
	TH1D * Nevents2_hasWTag0						=  file2 -> Get("cascadingQCDAna15/Nevents_hasWTag0");
	TH1D * Nevents2_hasWTag1						=  file2 -> Get("cascadingQCDAna15/Nevents_hasWTag1");
	TH1D * Nevents2_hasZeroWTags					=  file2 -> Get("cascadingQCDAna15/Nevents_hasZeroWTags");
	TH1D * Nevents2_hasOneWTag						=  file2 -> Get("cascadingQCDAna15/Nevents_hasOneWTag");
	TH1D * Nevents2_hasTwoWTags						=  file2 -> Get("cascadingQCDAna15/Nevents_hasTwoWTags");
	
	TH1D * Nevents2_hasBTag0						=  file2 -> Get("cascadingQCDAna15/Nevents_hasBTag0");
	TH1D * Nevents2_hasBTag1						=  file2 -> Get("cascadingQCDAna15/Nevents_hasBTag1");
	TH1D * Nevents2_hasZeroBTags					=  file2 -> Get("cascadingQCDAna15/Nevents_hasZeroBTags");
	TH1D * Nevents2_hasOneBTag						=  file2 -> Get("cascadingQCDAna15/Nevents_hasOneBTag");
	TH1D * Nevents2_hasTwoBTags						=  file2 -> Get("cascadingQCDAna15/Nevents_hasTwoBTags");
	
	TH1D * Nevents2_hasTightTop0					=  file2 -> Get("cascadingQCDAna15/Nevents_hasTightTop0");
	TH1D * Nevents2_hasTightTop1					=  file2 -> Get("cascadingQCDAna15/Nevents_hasTightTop1");
	TH1D * Nevents2_hasZeroTightTops				=  file2 -> Get("cascadingQCDAna15/Nevents_hasZeroTightTops");
	TH1D * Nevents2_hasOneTightTop					=  file2 -> Get("cascadingQCDAna15/Nevents_hasOneTightTop");
	TH1D * Nevents2_hasTwoTightTops					=  file2 -> Get("cascadingQCDAna15/Nevents_hasTwoTightTops");
	
	TH1D * Nevents2_hasLooseTop0					=  file2 -> Get("cascadingQCDAna15/Nevents_hasLooseTop0");
	TH1D * Nevents2_hasLooseTop1					=  file2 -> Get("cascadingQCDAna15/Nevents_hasLooseTop1");
	TH1D * Nevents2_hasZeroLooseTops				=  file2 -> Get("cascadingQCDAna15/Nevents_hasZeroLooseTops");
	TH1D * Nevents2_hasOneLooseTop					=  file2 -> Get("cascadingQCDAna15/Nevents_hasOneLooseTop");
	TH1D * Nevents2_hasTwoLooseTops					=  file2 -> Get("cascadingQCDAna15/Nevents_hasTwoLooseTops");
	
	TH1D * Nevents2_hasOneLooseOneTightTop			=  file2 -> Get("cascadingQCDAna15/Nevents_hasOneLooseOneTightTop");
	TH1D * Nevents2_hemiWithWandB					=  file2 -> Get("cascadingQCDAna15/Nevents_hemiWithWandB");
	TH1D * Nevents2_hemiWithWandUntagged			=  file2 -> Get("cascadingQCDAna15/Nevents_hemiWithWandUntagged");

	TH1D * Nevents2_TopTagAndTightTop				=  file2 -> Get("cascadingQCDAna15/Nevents_TopTagAndTightTop");
	TH1D * Nevents2_TopTagAndLooseTop				=  file2 -> Get("cascadingQCDAna15/Nevents_TopTagAndLooseTop");
	TH1D * Nevents2_TopTagAndWandB					=  file2 -> Get("cascadingQCDAna15/Nevents_TopTagAndWandB");
	TH1D * Nevents2_hasTwoWTags_hasOneBTag			=  file2 -> Get("cascadingQCDAna15/Nevents_hasTwoWTags_hasOneBTag");
	TH1D * Nevents2_hasTwoWTags_hasTwoBTags			=  file2 -> Get("cascadingQCDAna15/Nevents_hasTwoWTags_hasTwoBTags");
	TH1D * Nevents2_TightTopAndLooseTop				=  file2 -> Get("cascadingQCDAna15/Nevents_TightTopAndLooseTop");
	TH1D * Nevents2_hasOneTopJet_noNonLeadingBjet	=  file2 -> Get("cascadingQCDAna15/Nevents_hasOneTopJet_noNonLeadingBjet");

	TH1D * Nevents2_hemiTop_hemiBnoW				=  file2 -> Get("cascadingQCDAna15/Nevents_hemiTop_hemiBnoW");
	TH1D * Nevents2_hasBTag							=  file2 -> Get("cascadingQCDAna15/Nevents_hasBTag");
	TH1D * Nevents2_hasBTag_noWTag					=  file2 -> Get("cascadingQCDAna15/Nevents_hasBTag_noWTag");

	TH1D * Nevents2_type11sig						=  file2 -> Get("cascadingQCDAna15/Nevents_type11sig");
	TH1D * Nevents2_type12sig						=  file2 -> Get("cascadingQCDAna15/Nevents_type12sig");
	TH1D * Nevents2_type22sig						=  file2 -> Get("cascadingQCDAna15/Nevents_type22sig");
	TH1D * Nevents2_type11bkg						=  file2 -> Get("cascadingQCDAna15/Nevents_type11bkg");
	TH1D * Nevents2_type12bkg						=  file2 -> Get("cascadingQCDAna15/Nevents_type12bkg");
	TH1D * Nevents2_type22bkg						=  file2 -> Get("cascadingQCDAna15/Nevents_type22bkg");

	TH1D * Nevents2_cascade12sig					=  file2 -> Get("cascadingQCDAna15/Nevents_cascade12sig");
	TH1D * Nevents2_cascade22sig					=  file2 -> Get("cascadingQCDAna15/Nevents_cascade22sig");
	TH1D * Nevents2_cascade11bkg					=  file2 -> Get("cascadingQCDAna15/Nevents_cascade11bkg");
	TH1D * Nevents2_cascade12bkg					=  file2 -> Get("cascadingQCDAna15/Nevents_cascade12bkg");
	TH1D * Nevents2_cascade22bkg					=  file2 -> Get("cascadingQCDAna15/Nevents_cascade22bkg");

	//---------------------------------------------------------------
	

	TH1D * Nevents3_analyzed						=  file3 -> Get("cascadingQCDAna15/Nevents_analyzed");
	TH1D * Nevents3_preselected						=  file3 -> Get("cascadingQCDAna15/Nevents_preselected");
	
	TH1D * Nevents3_hasTaggedTopJet0				=  file3 -> Get("cascadingQCDAna15/Nevents_hasTaggedTopJet0");
	TH1D * Nevents3_hasTaggedTopJet1				=  file3 -> Get("cascadingQCDAna15/Nevents_hasTaggedTopJet1");
	TH1D * Nevents3_hasZeroTopTags					=  file3 -> Get("cascadingQCDAna15/Nevents_hasZeroTopTags");
	TH1D * Nevents3_hasOneTopTag					=  file3 -> Get("cascadingQCDAna15/Nevents_hasOneTopTag");
	TH1D * Nevents3_hasTwoTopTags					=  file3 -> Get("cascadingQCDAna15/Nevents_hasTwoTopTags");
	
	TH1D * Nevents3_hasWTag0						=  file3 -> Get("cascadingQCDAna15/Nevents_hasWTag0");
	TH1D * Nevents3_hasWTag1						=  file3 -> Get("cascadingQCDAna15/Nevents_hasWTag1");
	TH1D * Nevents3_hasZeroWTags					=  file3 -> Get("cascadingQCDAna15/Nevents_hasZeroWTags");
	TH1D * Nevents3_hasOneWTag						=  file3 -> Get("cascadingQCDAna15/Nevents_hasOneWTag");
	TH1D * Nevents3_hasTwoWTags						=  file3 -> Get("cascadingQCDAna15/Nevents_hasTwoWTags");
	
	TH1D * Nevents3_hasBTag0						=  file3 -> Get("cascadingQCDAna15/Nevents_hasBTag0");
	TH1D * Nevents3_hasBTag1						=  file3 -> Get("cascadingQCDAna15/Nevents_hasBTag1");
	TH1D * Nevents3_hasZeroBTags					=  file3 -> Get("cascadingQCDAna15/Nevents_hasZeroBTags");
	TH1D * Nevents3_hasOneBTag						=  file3 -> Get("cascadingQCDAna15/Nevents_hasOneBTag");
	TH1D * Nevents3_hasTwoBTags						=  file3 -> Get("cascadingQCDAna15/Nevents_hasTwoBTags");
	
	TH1D * Nevents3_hasTightTop0					=  file3 -> Get("cascadingQCDAna15/Nevents_hasTightTop0");
	TH1D * Nevents3_hasTightTop1					=  file3 -> Get("cascadingQCDAna15/Nevents_hasTightTop1");
	TH1D * Nevents3_hasZeroTightTops				=  file3 -> Get("cascadingQCDAna15/Nevents_hasZeroTightTops");
	TH1D * Nevents3_hasOneTightTop					=  file3 -> Get("cascadingQCDAna15/Nevents_hasOneTightTop");
	TH1D * Nevents3_hasTwoTightTops					=  file3 -> Get("cascadingQCDAna15/Nevents_hasTwoTightTops");
	
	TH1D * Nevents3_hasLooseTop0					=  file3 -> Get("cascadingQCDAna15/Nevents_hasLooseTop0");
	TH1D * Nevents3_hasLooseTop1					=  file3 -> Get("cascadingQCDAna15/Nevents_hasLooseTop1");
	TH1D * Nevents3_hasZeroLooseTops				=  file3 -> Get("cascadingQCDAna15/Nevents_hasZeroLooseTops");
	TH1D * Nevents3_hasOneLooseTop					=  file3 -> Get("cascadingQCDAna15/Nevents_hasOneLooseTop");
	TH1D * Nevents3_hasTwoLooseTops					=  file3 -> Get("cascadingQCDAna15/Nevents_hasTwoLooseTops");
	
	TH1D * Nevents3_hasOneLooseOneTightTop			=  file3 -> Get("cascadingQCDAna15/Nevents_hasOneLooseOneTightTop");
	TH1D * Nevents3_hemiWithWandB					=  file3 -> Get("cascadingQCDAna15/Nevents_hemiWithWandB");
	TH1D * Nevents3_hemiWithWandUntagged			=  file3 -> Get("cascadingQCDAna15/Nevents_hemiWithWandUntagged");

	TH1D * Nevents3_TopTagAndTightTop				=  file3 -> Get("cascadingQCDAna15/Nevents_TopTagAndTightTop");
	TH1D * Nevents3_TopTagAndLooseTop				=  file3 -> Get("cascadingQCDAna15/Nevents_TopTagAndLooseTop");
	TH1D * Nevents3_TopTagAndWandB					=  file3 -> Get("cascadingQCDAna15/Nevents_TopTagAndWandB");
	TH1D * Nevents3_hasTwoWTags_hasOneBTag			=  file3 -> Get("cascadingQCDAna15/Nevents_hasTwoWTags_hasOneBTag");
	TH1D * Nevents3_hasTwoWTags_hasTwoBTags			=  file3 -> Get("cascadingQCDAna15/Nevents_hasTwoWTags_hasTwoBTags");
	TH1D * Nevents3_TightTopAndLooseTop				=  file3 -> Get("cascadingQCDAna15/Nevents_TightTopAndLooseTop");
	TH1D * Nevents3_hasOneTopJet_noNonLeadingBjet	=  file3 -> Get("cascadingQCDAna15/Nevents_hasOneTopJet_noNonLeadingBjet");

	TH1D * Nevents3_hemiTop_hemiBnoW				=  file3 -> Get("cascadingQCDAna15/Nevents_hemiTop_hemiBnoW");
	TH1D * Nevents3_hasBTag							=  file3 -> Get("cascadingQCDAna15/Nevents_hasBTag");
	TH1D * Nevents3_hasBTag_noWTag					=  file3 -> Get("cascadingQCDAna15/Nevents_hasBTag_noWTag");

	TH1D * Nevents3_type11sig						=  file3 -> Get("cascadingQCDAna15/Nevents_type11sig");
	TH1D * Nevents3_type12sig						=  file3 -> Get("cascadingQCDAna15/Nevents_type12sig");
	TH1D * Nevents3_type22sig						=  file3 -> Get("cascadingQCDAna15/Nevents_type22sig");
	TH1D * Nevents3_type11bkg						=  file3 -> Get("cascadingQCDAna15/Nevents_type11bkg");
	TH1D * Nevents3_type12bkg						=  file3 -> Get("cascadingQCDAna15/Nevents_type12bkg");
	TH1D * Nevents3_type22bkg						=  file3 -> Get("cascadingQCDAna15/Nevents_type22bkg");

	TH1D * Nevents3_cascade12sig					=  file3 -> Get("cascadingQCDAna15/Nevents_cascade12sig");
	TH1D * Nevents3_cascade22sig					=  file3 -> Get("cascadingQCDAna15/Nevents_cascade22sig");
	TH1D * Nevents3_cascade11bkg					=  file3 -> Get("cascadingQCDAna15/Nevents_cascade11bkg");
	TH1D * Nevents3_cascade12bkg					=  file3 -> Get("cascadingQCDAna15/Nevents_cascade12bkg");
	TH1D * Nevents3_cascade22bkg					=  file3 -> Get("cascadingQCDAna15/Nevents_cascade22bkg");

	//---------------------------------------------------------------
	

	TH1D * Nevents4_analyzed						=  file4 -> Get("cascadingQCDAna15/Nevents_analyzed");
	TH1D * Nevents4_preselected						=  file4 -> Get("cascadingQCDAna15/Nevents_preselected");
	
	TH1D * Nevents4_hasTaggedTopJet0				=  file4 -> Get("cascadingQCDAna15/Nevents_hasTaggedTopJet0");
	TH1D * Nevents4_hasTaggedTopJet1				=  file4 -> Get("cascadingQCDAna15/Nevents_hasTaggedTopJet1");
	TH1D * Nevents4_hasZeroTopTags					=  file4 -> Get("cascadingQCDAna15/Nevents_hasZeroTopTags");
	TH1D * Nevents4_hasOneTopTag					=  file4 -> Get("cascadingQCDAna15/Nevents_hasOneTopTag");
	TH1D * Nevents4_hasTwoTopTags					=  file4 -> Get("cascadingQCDAna15/Nevents_hasTwoTopTags");
	
	TH1D * Nevents4_hasWTag0						=  file4 -> Get("cascadingQCDAna15/Nevents_hasWTag0");
	TH1D * Nevents4_hasWTag1						=  file4 -> Get("cascadingQCDAna15/Nevents_hasWTag1");
	TH1D * Nevents4_hasZeroWTags					=  file4 -> Get("cascadingQCDAna15/Nevents_hasZeroWTags");
	TH1D * Nevents4_hasOneWTag						=  file4 -> Get("cascadingQCDAna15/Nevents_hasOneWTag");
	TH1D * Nevents4_hasTwoWTags						=  file4 -> Get("cascadingQCDAna15/Nevents_hasTwoWTags");
	
	TH1D * Nevents4_hasBTag0						=  file4 -> Get("cascadingQCDAna15/Nevents_hasBTag0");
	TH1D * Nevents4_hasBTag1						=  file4 -> Get("cascadingQCDAna15/Nevents_hasBTag1");
	TH1D * Nevents4_hasZeroBTags					=  file4 -> Get("cascadingQCDAna15/Nevents_hasZeroBTags");
	TH1D * Nevents4_hasOneBTag						=  file4 -> Get("cascadingQCDAna15/Nevents_hasOneBTag");
	TH1D * Nevents4_hasTwoBTags						=  file4 -> Get("cascadingQCDAna15/Nevents_hasTwoBTags");
	
	TH1D * Nevents4_hasTightTop0					=  file4 -> Get("cascadingQCDAna15/Nevents_hasTightTop0");
	TH1D * Nevents4_hasTightTop1					=  file4 -> Get("cascadingQCDAna15/Nevents_hasTightTop1");
	TH1D * Nevents4_hasZeroTightTops				=  file4 -> Get("cascadingQCDAna15/Nevents_hasZeroTightTops");
	TH1D * Nevents4_hasOneTightTop					=  file4 -> Get("cascadingQCDAna15/Nevents_hasOneTightTop");
	TH1D * Nevents4_hasTwoTightTops					=  file4 -> Get("cascadingQCDAna15/Nevents_hasTwoTightTops");
	
	TH1D * Nevents4_hasLooseTop0					=  file4 -> Get("cascadingQCDAna15/Nevents_hasLooseTop0");
	TH1D * Nevents4_hasLooseTop1					=  file4 -> Get("cascadingQCDAna15/Nevents_hasLooseTop1");
	TH1D * Nevents4_hasZeroLooseTops				=  file4 -> Get("cascadingQCDAna15/Nevents_hasZeroLooseTops");
	TH1D * Nevents4_hasOneLooseTop					=  file4 -> Get("cascadingQCDAna15/Nevents_hasOneLooseTop");
	TH1D * Nevents4_hasTwoLooseTops					=  file4 -> Get("cascadingQCDAna15/Nevents_hasTwoLooseTops");
	
	TH1D * Nevents4_hasOneLooseOneTightTop			=  file4 -> Get("cascadingQCDAna15/Nevents_hasOneLooseOneTightTop");
	TH1D * Nevents4_hemiWithWandB					=  file4 -> Get("cascadingQCDAna15/Nevents_hemiWithWandB");
	TH1D * Nevents4_hemiWithWandUntagged			=  file4 -> Get("cascadingQCDAna15/Nevents_hemiWithWandUntagged");

	TH1D * Nevents4_TopTagAndTightTop				=  file4 -> Get("cascadingQCDAna15/Nevents_TopTagAndTightTop");
	TH1D * Nevents4_TopTagAndLooseTop				=  file4 -> Get("cascadingQCDAna15/Nevents_TopTagAndLooseTop");
	TH1D * Nevents4_TopTagAndWandB					=  file4 -> Get("cascadingQCDAna15/Nevents_TopTagAndWandB");
	TH1D * Nevents4_hasTwoWTags_hasOneBTag			=  file4 -> Get("cascadingQCDAna15/Nevents_hasTwoWTags_hasOneBTag");
	TH1D * Nevents4_hasTwoWTags_hasTwoBTags			=  file4 -> Get("cascadingQCDAna15/Nevents_hasTwoWTags_hasTwoBTags");
	TH1D * Nevents4_TightTopAndLooseTop				=  file4 -> Get("cascadingQCDAna15/Nevents_TightTopAndLooseTop");
	TH1D * Nevents4_hasOneTopJet_noNonLeadingBjet	=  file4 -> Get("cascadingQCDAna15/Nevents_hasOneTopJet_noNonLeadingBjet");

	TH1D * Nevents4_hemiTop_hemiBnoW				=  file4 -> Get("cascadingQCDAna15/Nevents_hemiTop_hemiBnoW");
	TH1D * Nevents4_hasBTag							=  file4 -> Get("cascadingQCDAna15/Nevents_hasBTag");
	TH1D * Nevents4_hasBTag_noWTag					=  file4 -> Get("cascadingQCDAna15/Nevents_hasBTag_noWTag");

	TH1D * Nevents4_type11sig						=  file4 -> Get("cascadingQCDAna15/Nevents_type11sig");
	TH1D * Nevents4_type12sig						=  file4 -> Get("cascadingQCDAna15/Nevents_type12sig");
	TH1D * Nevents4_type22sig						=  file4 -> Get("cascadingQCDAna15/Nevents_type22sig");
	TH1D * Nevents4_type11bkg						=  file4 -> Get("cascadingQCDAna15/Nevents_type11bkg");
	TH1D * Nevents4_type12bkg						=  file4 -> Get("cascadingQCDAna15/Nevents_type12bkg");
	TH1D * Nevents4_type22bkg						=  file4 -> Get("cascadingQCDAna15/Nevents_type22bkg");

	TH1D * Nevents4_cascade12sig					=  file4 -> Get("cascadingQCDAna15/Nevents_cascade12sig");
	TH1D * Nevents4_cascade22sig					=  file4 -> Get("cascadingQCDAna15/Nevents_cascade22sig");
	TH1D * Nevents4_cascade11bkg					=  file4 -> Get("cascadingQCDAna15/Nevents_cascade11bkg");
	TH1D * Nevents4_cascade12bkg					=  file4 -> Get("cascadingQCDAna15/Nevents_cascade12bkg");
	TH1D * Nevents4_cascade22bkg					=  file4 -> Get("cascadingQCDAna15/Nevents_cascade22bkg");

	//---------------------------------------------------------------
	

	TH1D * Nevents5_analyzed						=  file5 -> Get("cascadingQCDAna15/Nevents_analyzed");
	TH1D * Nevents5_preselected						=  file5 -> Get("cascadingQCDAna15/Nevents_preselected");
	
	TH1D * Nevents5_hasTaggedTopJet0				=  file5 -> Get("cascadingQCDAna15/Nevents_hasTaggedTopJet0");
	TH1D * Nevents5_hasTaggedTopJet1				=  file5 -> Get("cascadingQCDAna15/Nevents_hasTaggedTopJet1");
	TH1D * Nevents5_hasZeroTopTags					=  file5 -> Get("cascadingQCDAna15/Nevents_hasZeroTopTags");
	TH1D * Nevents5_hasOneTopTag					=  file5 -> Get("cascadingQCDAna15/Nevents_hasOneTopTag");
	TH1D * Nevents5_hasTwoTopTags					=  file5 -> Get("cascadingQCDAna15/Nevents_hasTwoTopTags");
	
	TH1D * Nevents5_hasWTag0						=  file5 -> Get("cascadingQCDAna15/Nevents_hasWTag0");
	TH1D * Nevents5_hasWTag1						=  file5 -> Get("cascadingQCDAna15/Nevents_hasWTag1");
	TH1D * Nevents5_hasZeroWTags					=  file5 -> Get("cascadingQCDAna15/Nevents_hasZeroWTags");
	TH1D * Nevents5_hasOneWTag						=  file5 -> Get("cascadingQCDAna15/Nevents_hasOneWTag");
	TH1D * Nevents5_hasTwoWTags						=  file5 -> Get("cascadingQCDAna15/Nevents_hasTwoWTags");
	
	TH1D * Nevents5_hasBTag0						=  file5 -> Get("cascadingQCDAna15/Nevents_hasBTag0");
	TH1D * Nevents5_hasBTag1						=  file5 -> Get("cascadingQCDAna15/Nevents_hasBTag1");
	TH1D * Nevents5_hasZeroBTags					=  file5 -> Get("cascadingQCDAna15/Nevents_hasZeroBTags");
	TH1D * Nevents5_hasOneBTag						=  file5 -> Get("cascadingQCDAna15/Nevents_hasOneBTag");
	TH1D * Nevents5_hasTwoBTags						=  file5 -> Get("cascadingQCDAna15/Nevents_hasTwoBTags");
	
	TH1D * Nevents5_hasTightTop0					=  file5 -> Get("cascadingQCDAna15/Nevents_hasTightTop0");
	TH1D * Nevents5_hasTightTop1					=  file5 -> Get("cascadingQCDAna15/Nevents_hasTightTop1");
	TH1D * Nevents5_hasZeroTightTops				=  file5 -> Get("cascadingQCDAna15/Nevents_hasZeroTightTops");
	TH1D * Nevents5_hasOneTightTop					=  file5 -> Get("cascadingQCDAna15/Nevents_hasOneTightTop");
	TH1D * Nevents5_hasTwoTightTops					=  file5 -> Get("cascadingQCDAna15/Nevents_hasTwoTightTops");
	
	TH1D * Nevents5_hasLooseTop0					=  file5 -> Get("cascadingQCDAna15/Nevents_hasLooseTop0");
	TH1D * Nevents5_hasLooseTop1					=  file5 -> Get("cascadingQCDAna15/Nevents_hasLooseTop1");
	TH1D * Nevents5_hasZeroLooseTops				=  file5 -> Get("cascadingQCDAna15/Nevents_hasZeroLooseTops");
	TH1D * Nevents5_hasOneLooseTop					=  file5 -> Get("cascadingQCDAna15/Nevents_hasOneLooseTop");
	TH1D * Nevents5_hasTwoLooseTops					=  file5 -> Get("cascadingQCDAna15/Nevents_hasTwoLooseTops");
	
	TH1D * Nevents5_hasOneLooseOneTightTop			=  file5 -> Get("cascadingQCDAna15/Nevents_hasOneLooseOneTightTop");
	TH1D * Nevents5_hemiWithWandB					=  file5 -> Get("cascadingQCDAna15/Nevents_hemiWithWandB");
	TH1D * Nevents5_hemiWithWandUntagged			=  file5 -> Get("cascadingQCDAna15/Nevents_hemiWithWandUntagged");

	TH1D * Nevents5_TopTagAndTightTop				=  file5 -> Get("cascadingQCDAna15/Nevents_TopTagAndTightTop");
	TH1D * Nevents5_TopTagAndLooseTop				=  file5 -> Get("cascadingQCDAna15/Nevents_TopTagAndLooseTop");
	TH1D * Nevents5_TopTagAndWandB					=  file5 -> Get("cascadingQCDAna15/Nevents_TopTagAndWandB");
	TH1D * Nevents5_hasTwoWTags_hasOneBTag			=  file5 -> Get("cascadingQCDAna15/Nevents_hasTwoWTags_hasOneBTag");
	TH1D * Nevents5_hasTwoWTags_hasTwoBTags			=  file5 -> Get("cascadingQCDAna15/Nevents_hasTwoWTags_hasTwoBTags");
	TH1D * Nevents5_TightTopAndLooseTop				=  file5 -> Get("cascadingQCDAna15/Nevents_TightTopAndLooseTop");
	TH1D * Nevents5_hasOneTopJet_noNonLeadingBjet	=  file5 -> Get("cascadingQCDAna15/Nevents_hasOneTopJet_noNonLeadingBjet");

	TH1D * Nevents5_hemiTop_hemiBnoW				=  file5 -> Get("cascadingQCDAna15/Nevents_hemiTop_hemiBnoW");
	TH1D * Nevents5_hasBTag							=  file5 -> Get("cascadingQCDAna15/Nevents_hasBTag");
	TH1D * Nevents5_hasBTag_noWTag					=  file5 -> Get("cascadingQCDAna15/Nevents_hasBTag_noWTag");

	TH1D * Nevents5_type11sig						=  file5 -> Get("cascadingQCDAna15/Nevents_type11sig");
	TH1D * Nevents5_type12sig						=  file5 -> Get("cascadingQCDAna15/Nevents_type12sig");
	TH1D * Nevents5_type22sig						=  file5 -> Get("cascadingQCDAna15/Nevents_type22sig");
	TH1D * Nevents5_type11bkg						=  file5 -> Get("cascadingQCDAna15/Nevents_type11bkg");
	TH1D * Nevents5_type12bkg						=  file5 -> Get("cascadingQCDAna15/Nevents_type12bkg");
	TH1D * Nevents5_type22bkg						=  file5 -> Get("cascadingQCDAna15/Nevents_type22bkg");

	TH1D * Nevents5_cascade12sig					=  file5 -> Get("cascadingQCDAna15/Nevents_cascade12sig");
	TH1D * Nevents5_cascade22sig					=  file5 -> Get("cascadingQCDAna15/Nevents_cascade22sig");
	TH1D * Nevents5_cascade11bkg					=  file5 -> Get("cascadingQCDAna15/Nevents_cascade11bkg");
	TH1D * Nevents5_cascade12bkg					=  file5 -> Get("cascadingQCDAna15/Nevents_cascade12bkg");
	TH1D * Nevents5_cascade22bkg					=  file5 -> Get("cascadingQCDAna15/Nevents_cascade22bkg");

	//---------------------------------------------------------------
		

	TH1D * Nevents6_analyzed						=  file6 -> Get("cascadingQCDAna15/Nevents_analyzed");
	TH1D * Nevents6_preselected						=  file6 -> Get("cascadingQCDAna15/Nevents_preselected");
	
	TH1D * Nevents6_hasTaggedTopJet0				=  file6 -> Get("cascadingQCDAna15/Nevents_hasTaggedTopJet0");
	TH1D * Nevents6_hasTaggedTopJet1				=  file6 -> Get("cascadingQCDAna15/Nevents_hasTaggedTopJet1");
	TH1D * Nevents6_hasZeroTopTags					=  file6 -> Get("cascadingQCDAna15/Nevents_hasZeroTopTags");
	TH1D * Nevents6_hasOneTopTag					=  file6 -> Get("cascadingQCDAna15/Nevents_hasOneTopTag");
	TH1D * Nevents6_hasTwoTopTags					=  file6 -> Get("cascadingQCDAna15/Nevents_hasTwoTopTags");
	
	TH1D * Nevents6_hasWTag0						=  file6 -> Get("cascadingQCDAna15/Nevents_hasWTag0");
	TH1D * Nevents6_hasWTag1						=  file6 -> Get("cascadingQCDAna15/Nevents_hasWTag1");
	TH1D * Nevents6_hasZeroWTags					=  file6 -> Get("cascadingQCDAna15/Nevents_hasZeroWTags");
	TH1D * Nevents6_hasOneWTag						=  file6 -> Get("cascadingQCDAna15/Nevents_hasOneWTag");
	TH1D * Nevents6_hasTwoWTags						=  file6 -> Get("cascadingQCDAna15/Nevents_hasTwoWTags");
	
	TH1D * Nevents6_hasBTag0						=  file6 -> Get("cascadingQCDAna15/Nevents_hasBTag0");
	TH1D * Nevents6_hasBTag1						=  file6 -> Get("cascadingQCDAna15/Nevents_hasBTag1");
	TH1D * Nevents6_hasZeroBTags					=  file6 -> Get("cascadingQCDAna15/Nevents_hasZeroBTags");
	TH1D * Nevents6_hasOneBTag						=  file6 -> Get("cascadingQCDAna15/Nevents_hasOneBTag");
	TH1D * Nevents6_hasTwoBTags						=  file6 -> Get("cascadingQCDAna15/Nevents_hasTwoBTags");
	
	TH1D * Nevents6_hasTightTop0					=  file6 -> Get("cascadingQCDAna15/Nevents_hasTightTop0");
	TH1D * Nevents6_hasTightTop1					=  file6 -> Get("cascadingQCDAna15/Nevents_hasTightTop1");
	TH1D * Nevents6_hasZeroTightTops				=  file6 -> Get("cascadingQCDAna15/Nevents_hasZeroTightTops");
	TH1D * Nevents6_hasOneTightTop					=  file6 -> Get("cascadingQCDAna15/Nevents_hasOneTightTop");
	TH1D * Nevents6_hasTwoTightTops					=  file6 -> Get("cascadingQCDAna15/Nevents_hasTwoTightTops");
	
	TH1D * Nevents6_hasLooseTop0					=  file6 -> Get("cascadingQCDAna15/Nevents_hasLooseTop0");
	TH1D * Nevents6_hasLooseTop1					=  file6 -> Get("cascadingQCDAna15/Nevents_hasLooseTop1");
	TH1D * Nevents6_hasZeroLooseTops				=  file6 -> Get("cascadingQCDAna15/Nevents_hasZeroLooseTops");
	TH1D * Nevents6_hasOneLooseTop					=  file6 -> Get("cascadingQCDAna15/Nevents_hasOneLooseTop");
	TH1D * Nevents6_hasTwoLooseTops					=  file6 -> Get("cascadingQCDAna15/Nevents_hasTwoLooseTops");
	
	TH1D * Nevents6_hasOneLooseOneTightTop			=  file6 -> Get("cascadingQCDAna15/Nevents_hasOneLooseOneTightTop");
	TH1D * Nevents6_hemiWithWandB					=  file6 -> Get("cascadingQCDAna15/Nevents_hemiWithWandB");
	TH1D * Nevents6_hemiWithWandUntagged			=  file6 -> Get("cascadingQCDAna15/Nevents_hemiWithWandUntagged");

	TH1D * Nevents6_TopTagAndTightTop				=  file6 -> Get("cascadingQCDAna15/Nevents_TopTagAndTightTop");
	TH1D * Nevents6_TopTagAndLooseTop				=  file6 -> Get("cascadingQCDAna15/Nevents_TopTagAndLooseTop");
	TH1D * Nevents6_TopTagAndWandB					=  file6 -> Get("cascadingQCDAna15/Nevents_TopTagAndWandB");
	TH1D * Nevents6_hasTwoWTags_hasOneBTag			=  file6 -> Get("cascadingQCDAna15/Nevents_hasTwoWTags_hasOneBTag");
	TH1D * Nevents6_hasTwoWTags_hasTwoBTags			=  file6 -> Get("cascadingQCDAna15/Nevents_hasTwoWTags_hasTwoBTags");
	TH1D * Nevents6_TightTopAndLooseTop				=  file6 -> Get("cascadingQCDAna15/Nevents_TightTopAndLooseTop");
	TH1D * Nevents6_hasOneTopJet_noNonLeadingBjet	=  file6 -> Get("cascadingQCDAna15/Nevents_hasOneTopJet_noNonLeadingBjet");

	TH1D * Nevents6_hemiTop_hemiBnoW				=  file6 -> Get("cascadingQCDAna15/Nevents_hemiTop_hemiBnoW");
	TH1D * Nevents6_hasBTag							=  file6 -> Get("cascadingQCDAna15/Nevents_hasBTag");
	TH1D * Nevents6_hasBTag_noWTag					=  file6 -> Get("cascadingQCDAna15/Nevents_hasBTag_noWTag");

	TH1D * Nevents6_type11sig						=  file6 -> Get("cascadingQCDAna15/Nevents_type11sig");
	TH1D * Nevents6_type12sig						=  file6 -> Get("cascadingQCDAna15/Nevents_type12sig");
	TH1D * Nevents6_type22sig						=  file6 -> Get("cascadingQCDAna15/Nevents_type22sig");
	TH1D * Nevents6_type11bkg						=  file6 -> Get("cascadingQCDAna15/Nevents_type11bkg");
	TH1D * Nevents6_type12bkg						=  file6 -> Get("cascadingQCDAna15/Nevents_type12bkg");
	TH1D * Nevents6_type22bkg						=  file6 -> Get("cascadingQCDAna15/Nevents_type22bkg");

	TH1D * Nevents6_cascade12sig					=  file6 -> Get("cascadingQCDAna15/Nevents_cascade12sig");
	TH1D * Nevents6_cascade22sig					=  file6 -> Get("cascadingQCDAna15/Nevents_cascade22sig");
	TH1D * Nevents6_cascade11bkg					=  file6 -> Get("cascadingQCDAna15/Nevents_cascade11bkg");
	TH1D * Nevents6_cascade12bkg					=  file6 -> Get("cascadingQCDAna15/Nevents_cascade12bkg");
	TH1D * Nevents6_cascade22bkg					=  file6 -> Get("cascadingQCDAna15/Nevents_cascade22bkg");

	//---------------------------------------------------------------
	
	cout<<"LaTeX table format"<<endl;

	
	cout << "\\begin{center}"<<endl;
	cout << "\\begin{tabular}{ | l | c | c | c | c | c | c | }"<<endl;
	
	cout << "\\hline"<<endl;
	cout << "  &  Data & QCD & ttbar & Z'(750) & Z'(1000) & Z'(1500) \\\\  \\hline"<<endl;
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	cout << "Total & "<< Nevents1_analyzed->GetEntries() << " & " << Nevents2_analyzed->GetEntries() << " & " << Nevents3_analyzed->GetEntries() <<" & " << Nevents4_analyzed->GetEntries() <<" & " << Nevents5_analyzed->GetEntries() <<" & " << Nevents6_analyzed->GetEntries() <<" \\\\ \\hline"<<endl;
	cout << "Preselected & "<< Nevents1_preselected->GetEntries() << " & " << Nevents2_preselected->GetEntries() << " & " << Nevents3_preselected->GetEntries() <<" & " << Nevents4_preselected->GetEntries() <<" & " << Nevents5_preselected->GetEntries() <<" & " << Nevents5_preselected->GetEntries() <<" \\\\ \\hline"<<endl;
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	cout << "0 top tags & " << Nevents1_hasZeroTopTags->GetEntries() << " & " << Nevents2_hasZeroTopTags->GetEntries() << " & " << Nevents3_hasZeroTopTags->GetEntries() << " & " << Nevents4_hasZeroTopTags->GetEntries() << " & " << Nevents5_hasZeroTopTags->GetEntries() << " & " << Nevents6_hasZeroTopTags->GetEntries() << " \\\\ \\hline"<<endl;
	cout << "1 top tag & " << Nevents1_hasOneTopTag->GetEntries() << " & " << Nevents2_hasOneTopTag->GetEntries() << " & " << Nevents3_hasOneTopTag->GetEntries() << " & " << Nevents4_hasOneTopTag->GetEntries() << " & " << Nevents5_hasOneTopTag->GetEntries() << " & " << Nevents6_hasOneTopTag->GetEntries() << " \\\\ \\hline"<<endl;
	cout << "2 top tags & " << Nevents1_hasTwoTopTags->GetEntries() << " & " << Nevents2_hasTwoTopTags->GetEntries() << " & " << Nevents3_hasTwoTopTags->GetEntries() << " & " << Nevents4_hasTwoTopTags->GetEntries() << " & " << Nevents5_hasTwoTopTags->GetEntries() << " & " << Nevents6_hasTwoTopTags->GetEntries() << " \\\\ \\hline"<<endl;
	

	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	cout << "0 W tags & " << Nevents1_hasZeroWTags->GetEntries() << " & " << Nevents2_hasZeroWTags->GetEntries() << " & " << Nevents3_hasZeroWTags->GetEntries() << " & " << Nevents4_hasZeroWTags->GetEntries() << " & " << Nevents5_hasZeroWTags->GetEntries() <<  " & " << Nevents6_hasZeroWTags->GetEntries() << " \\\\ \\hline"<<endl;
	cout << "1 W tag & " << Nevents1_hasOneWTag->GetEntries() 
	            << " & " << Nevents2_hasOneWTag->GetEntries() 
	            << " & " << Nevents3_hasOneWTag->GetEntries() 
	            << " & " << Nevents4_hasOneWTag->GetEntries() 
	            << " & " << Nevents5_hasOneWTag->GetEntries() 
	            << " & " << Nevents6_hasOneWTag->GetEntries() << " \\\\ \\hline"<<endl;
	cout << "2 W tags & " << Nevents1_hasTwoWTags->GetEntries() << " & " << Nevents2_hasTwoWTags->GetEntries() << " & " << Nevents3_hasTwoWTags->GetEntries() << " & " << Nevents4_hasTwoWTags->GetEntries() << " & " << Nevents5_hasTwoWTags->GetEntries() << " & " << Nevents6_hasTwoWTags->GetEntries() << " \\\\ \\hline"<<endl;
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	cout << "0 B tags & " << Nevents1_hasZeroBTags->GetEntries() << " & " << Nevents2_hasZeroBTags->GetEntries() << " & " << Nevents3_hasZeroBTags->GetEntries() << " & " << Nevents4_hasZeroBTags->GetEntries() << " & " << Nevents5_hasZeroBTags->GetEntries() <<  " & " << Nevents6_hasZeroBTags->GetEntries() << " \\\\ \\hline"<<endl;
	cout << "1 B tag & " << Nevents1_hasOneBTag->GetEntries() << " & " << Nevents2_hasOneBTag->GetEntries() << " & " << Nevents3_hasOneBTag->GetEntries() << " & " << Nevents4_hasOneBTag->GetEntries() << " & " << Nevents5_hasOneBTag->GetEntries() << " & " << Nevents6_hasOneBTag->GetEntries() << " \\\\ \\hline"<<endl;
	cout << "2 B tags & " << Nevents1_hasTwoBTags->GetEntries() << " & " << Nevents2_hasTwoBTags->GetEntries() << " & " << Nevents3_hasTwoBTags->GetEntries() << " & " << Nevents4_hasTwoBTags->GetEntries() << " & " << Nevents5_hasTwoBTags->GetEntries() << " & " << Nevents6_hasTwoBTags->GetEntries() << " \\\\ \\hline"<<endl;
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	cout << "0 Tight Tops & " << Nevents1_hasZeroTightTops->GetEntries() << " & " << Nevents2_hasZeroTightTops->GetEntries() << " & " << Nevents3_hasZeroTightTops->GetEntries() << " & " << Nevents4_hasZeroTightTops->GetEntries() << " & " << Nevents5_hasZeroTightTops->GetEntries() <<  " & " << Nevents6_hasZeroTightTops->GetEntries() << " \\\\ \\hline"<<endl;
	cout << "1 Tight Top & " << Nevents1_hasOneTightTop->GetEntries() << " & " << Nevents2_hasOneTightTop->GetEntries() << " & " << Nevents3_hasOneTightTop->GetEntries() << " & " << Nevents4_hasOneTightTop->GetEntries() << " & " << Nevents5_hasOneTightTop->GetEntries() << " & " << Nevents6_hasOneTightTop->GetEntries() << " \\\\ \\hline"<<endl;
	cout << "2 Tight Tops & " << Nevents1_hasTwoTightTops->GetEntries() << " & " << Nevents2_hasTwoTightTops->GetEntries() << " & " << Nevents3_hasTwoTightTops->GetEntries() << " & " << Nevents4_hasTwoTightTops->GetEntries() << " & " << Nevents5_hasTwoTightTops->GetEntries() << " & " << Nevents6_hasTwoTightTops->GetEntries() << " \\\\ \\hline"<<endl;
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	cout << "0 Loose Tops & " << Nevents1_hasZeroLooseTops->GetEntries() << " & " << Nevents2_hasZeroLooseTops->GetEntries() << " & " << Nevents3_hasZeroLooseTops->GetEntries() << " & " << Nevents4_hasZeroLooseTops->GetEntries() << " & " << Nevents5_hasZeroLooseTops->GetEntries() <<  " & " << Nevents6_hasZeroLooseTops->GetEntries() << " \\\\ \\hline"<<endl;
	cout << "1 Loose Top & " << Nevents1_hasOneLooseTop->GetEntries() << " & " << Nevents2_hasOneLooseTop->GetEntries() << " & " << Nevents3_hasOneLooseTop->GetEntries() << " & " << Nevents4_hasOneLooseTop->GetEntries() << " & " << Nevents5_hasOneLooseTop->GetEntries() << " & " << Nevents6_hasOneLooseTop->GetEntries() << " \\\\ \\hline"<<endl;
	cout << "2 Loose Tops & " << Nevents1_hasTwoLooseTops->GetEntries() << " & " << Nevents2_hasTwoLooseTops->GetEntries() << " & " << Nevents3_hasTwoLooseTops->GetEntries() << " & " << Nevents4_hasTwoLooseTops->GetEntries() << " & " << Nevents5_hasTwoLooseTops->GetEntries() << " & " << Nevents6_hasTwoLooseTops->GetEntries() << " \\\\ \\hline"<<endl;
	
	
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	cout << "top tag in leading hemisphere & " << Nevents1_hasTaggedTopJet0->GetEntries() << " & " << Nevents2_hasTaggedTopJet0->GetEntries() << " & " << Nevents3_hasTaggedTopJet0->GetEntries() << " & " << Nevents4_hasTaggedTopJet0->GetEntries() << " & " << Nevents5_hasTaggedTopJet0->GetEntries() << " & " << Nevents6_hasTaggedTopJet0->GetEntries() << " \\\\ \\hline"<<endl;
	cout << "top tag in second leading hemisphere & " << Nevents1_hasTaggedTopJet1->GetEntries() << " & " << Nevents2_hasTaggedTopJet1->GetEntries() << " & " << Nevents3_hasTaggedTopJet1->GetEntries() << " & " << Nevents4_hasTaggedTopJet1->GetEntries() << " & " << Nevents5_hasTaggedTopJet1->GetEntries() << " & " << Nevents6_hasTaggedTopJet1->GetEntries() << " \\\\ \\hline"<<endl;

	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	cout << "W tag in leading hemisphere & " << Nevents1_hasWTag0->GetEntries() << " & " << Nevents2_hasWTag0->GetEntries() << " & " << Nevents3_hasWTag0->GetEntries() << " & " << Nevents4_hasWTag0->GetEntries() << " & " << Nevents5_hasWTag0->GetEntries() << " & " << Nevents6_hasWTag0->GetEntries() << " \\\\ \\hline"<<endl;
	cout << "W tag in second leading hemisphere & " << Nevents1_hasWTag1->GetEntries() << " & " << Nevents2_hasWTag1->GetEntries() << " & " << Nevents3_hasWTag1->GetEntries() << " & " << Nevents4_hasWTag1->GetEntries() << " & " << Nevents5_hasWTag1->GetEntries() << " & " << Nevents6_hasWTag1->GetEntries() << " \\\\ \\hline"<<endl;

	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	cout << "B tag in leading hemisphere & " << Nevents1_hasBTag0->GetEntries() << " & " << Nevents2_hasBTag0->GetEntries() << " & " << Nevents3_hasBTag0->GetEntries() << " & " << Nevents4_hasBTag0->GetEntries() << " & " << Nevents5_hasBTag0->GetEntries() << " & " << Nevents6_hasBTag0->GetEntries() << " \\\\ \\hline"<<endl;
	cout << "B tag in second leading hemisphere & " << Nevents1_hasBTag1->GetEntries() << " & " << Nevents2_hasBTag1->GetEntries() << " & " << Nevents3_hasBTag1->GetEntries() << " & " << Nevents4_hasBTag1->GetEntries() << " & " << Nevents5_hasBTag1->GetEntries() << " & " << Nevents6_hasBTag1->GetEntries() << " \\\\ \\hline"<<endl;

	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	cout << "Tight top in leading hemisphere & " << Nevents1_hasTightTop0->GetEntries() << " & " << Nevents2_hasTightTop0->GetEntries() << " & " << Nevents3_hasTightTop0->GetEntries() << " & " << Nevents4_hasTightTop0->GetEntries() << " & " << Nevents5_hasTightTop0->GetEntries() << " & " << Nevents6_hasTightTop0->GetEntries() << " \\\\ \\hline"<<endl;
	cout << "Tight top in second leading hemisphere & " << Nevents1_hasTightTop1->GetEntries() << " & " << Nevents2_hasTightTop1->GetEntries() << " & " << Nevents3_hasTightTop1->GetEntries() << " & " << Nevents4_hasTightTop1->GetEntries() << " & " << Nevents5_hasTightTop1->GetEntries() << " & " << Nevents6_hasTightTop1->GetEntries() << " \\\\ \\hline"<<endl;

	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	cout << "Loose top in leading hemisphere & " << Nevents1_hasLooseTop0->GetEntries() << " & " << Nevents2_hasLooseTop0->GetEntries() << " & " << Nevents3_hasLooseTop0->GetEntries() << " & " << Nevents4_hasLooseTop0->GetEntries() << " & " << Nevents5_hasLooseTop0->GetEntries() << " & " << Nevents6_hasLooseTop0->GetEntries() << " \\\\ \\hline"<<endl;
	cout << "Loose top in second leading hemisphere & " << Nevents1_hasLooseTop1->GetEntries() << " & " << Nevents2_hasLooseTop1->GetEntries() << " & " << Nevents3_hasLooseTop1->GetEntries() << " & " << Nevents4_hasLooseTop1->GetEntries() << " & " << Nevents5_hasLooseTop1->GetEntries() << " & " << Nevents6_hasLooseTop1->GetEntries() << " \\\\ \\hline"<<endl;

	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	cout << "Type 11 pass events & " << Nevents1_type11sig->GetEntries() << " & " << Nevents2_type11sig->GetEntries() << " & " << Nevents3_type11sig->GetEntries() << " & " << Nevents4_type11sig->GetEntries() << " & " << Nevents5_type11sig->GetEntries() << " & " << Nevents6_type11sig->GetEntries() << " \\\\ \\hline"<<endl;
	cout << "Type 12 pass events & " << Nevents1_type12sig->GetEntries() << " & " << Nevents2_type12sig->GetEntries() << " & " << Nevents3_type12sig->GetEntries() << " & " << Nevents4_type12sig->GetEntries() << " & " << Nevents5_type12sig->GetEntries() << " & " << Nevents6_type12sig->GetEntries() << " \\\\ \\hline"<<endl;
	cout << "Type 22 pass events & " << Nevents1_type22sig->GetEntries() << " & " << Nevents2_type22sig->GetEntries() << " & " << Nevents3_type22sig->GetEntries() << " & " << Nevents4_type22sig->GetEntries() << " & " << Nevents5_type22sig->GetEntries() << " & " << Nevents6_type22sig->GetEntries() << " \\\\ \\hline"<<endl;
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	cout << "Type 11 bkg estimation & " << Nevents1_type11bkg->GetEntries() << " & & & & &  \\\\ \\hline"<<endl;
	cout << "Type 12 bkg estimation & " << Nevents1_type12bkg->GetEntries() << " & & & & &  \\\\ \\hline"<<endl;
	cout << "Type 22 bkg estimation & " << Nevents1_type22bkg->GetEntries() << " & & & & &  \\\\ \\hline"<<endl;


	cout << "\\end{tabular}"<<endl;
	cout << "\\end{center}"<<endl;


}



void PrintEntries( string histname, string text, TFile* file1, TFile* file2, TFile* file3, TFile* file4, TFile* file5, TFile* file6 )
{

	string histpath = "cascadingQCDAna15/"+histname;
	TH1D * h1 =  file1 -> Get(histpath.c_str());
	TH1D * h2 =  file2 -> Get(histpath.c_str());
	TH1D * h3 =  file3 -> Get(histpath.c_str());
	TH1D * h4 =  file4 -> Get(histpath.c_str());
	TH1D * h5 =  file5 -> Get(histpath.c_str());
	TH1D * h6 =  file6 -> Get(histpath.c_str());
	cout << text <<" & " << h1->GetEntries() << " & " << setprecision(9) <<h2->GetEntries() << " & " << h3->GetEntries() << " & " << h4->GetEntries() << " & " << h5->GetEntries() << " & " << h6->GetEntries() << " \\\\ \\hline"<<endl;
}

void PrintEfficiency2( string histname, string text, TFile* file1, TFile* file2, TFile* file3, TFile* file4, TFile* file5, TFile* file6 )
{
	double d1 = 47233078;
	double d2 = 10876000;
	double d3 = 1394548;
	double d4 = 204819;
	double d5 = 213384;
	double d6 = 193779;
	
	string histpath = "cascadingQCDAna15/"+histname;
	TH1D * h1 =  file1 -> Get(histpath.c_str());
	TH1D * h2 =  file2 -> Get(histpath.c_str());
	TH1D * h3 =  file3 -> Get(histpath.c_str());
	TH1D * h4 =  file4 -> Get(histpath.c_str());
	TH1D * h5 =  file5 -> Get(histpath.c_str());
	TH1D * h6 =  file6 -> Get(histpath.c_str());
	cout << text <<" & "<< setprecision(3) << h1->GetEntries()/d1 << " & "  <<h2->GetEntries()/d2 << " & " << h3->GetEntries()/d3 << " & " << h4->GetEntries()/d4 << " & " << h5->GetEntries()/d5 << " & " << h6->GetEntries()/d6 << " \\\\ \\hline"<<endl;
}

void PrintBinContent( string histname, string text, int bin, TFile* file1, TFile* file2, TFile* file3, TFile* file4, TFile* file5, TFile* file6 )
{

	string histpath = "cascadingQCDAna15/"+histname;
	TH1D * h1 =  file1 -> Get(histpath.c_str());
	TH1D * h2 =  file2 -> Get(histpath.c_str());
	TH1D * h3 =  file3 -> Get(histpath.c_str());
	TH1D * h4 =  file4 -> Get(histpath.c_str());
	TH1D * h5 =  file5 -> Get(histpath.c_str());
	TH1D * h6 =  file6 -> Get(histpath.c_str());
	cout << text <<" & " << h1->GetBinContent(bin) << " & " << h2->GetBinContent(bin) << " & " << h3->GetBinContent(bin) << " & " << h4->GetBinContent(bin) << " & " << h5->GetBinContent(bin) << " & " << h6->GetBinContent(bin) << " \\\\ \\hline"<<endl;
}

void PrintEfficiency3( string histname, string text, int bin, TFile* file1, TFile* file2, TFile* file3, TFile* file4, TFile* file5, TFile* file6 )
{

	double d1 = 47233078;
	double d2 = 10876000;
	double d3 = 1394548;
	double d4 = 204819;
	double d5 = 213384;
	double d6 = 193779;

	string histpath = "cascadingQCDAna15/"+histname;
	TH1D * h1 =  file1 -> Get(histpath.c_str());
	TH1D * h2 =  file2 -> Get(histpath.c_str());
	TH1D * h3 =  file3 -> Get(histpath.c_str());
	TH1D * h4 =  file4 -> Get(histpath.c_str());
	TH1D * h5 =  file5 -> Get(histpath.c_str());
	TH1D * h6 =  file6 -> Get(histpath.c_str());
	cout << text <<" & " << setprecision(3)<< h1->GetBinContent(bin)/d1 << " & " << h2->GetBinContent(bin)/d2 << " & " << h3->GetBinContent(bin)/d3 << " & " << h4->GetBinContent(bin)/d4 << " & " << h5->GetBinContent(bin)/d5 << " & " << h6->GetBinContent(bin)/d6 << " \\\\ \\hline"<<endl;
}


void PrintBinContent2hists( string histname, string text, int bin1, int bin2, TFile* file1, TFile* file2, TFile* file3, TFile* file4, TFile* file5, TFile* file6 )
{
	string histpath = "cascadingQCDAna15/"+histname;
	TH1D * h1 =  file1 -> Get(histpath.c_str());
	TH1D * h2 =  file2 -> Get(histpath.c_str());
	TH1D * h3 =  file3 -> Get(histpath.c_str());
	TH1D * h4 =  file4 -> Get(histpath.c_str());
	TH1D * h5 =  file5 -> Get(histpath.c_str());
	TH1D * h6 =  file6 -> Get(histpath.c_str());
	cout << text <<" & " << h1->GetBinContent(bin1) <<"\\textbackslash"<< h1->GetBinContent(bin2) << " & " << h2->GetBinContent(bin1) <<"\\textbackslash"<< h2->GetBinContent(bin2) << " & " << h3->GetBinContent(bin1)<<"\\textbackslash"<< h3->GetBinContent(bin2)  << " & " << h4->GetBinContent(bin1)<<"\\textbackslash"<< h4->GetBinContent(bin2)  << " & " << h5->GetBinContent(bin1)<<"\\textbackslash"<< h5->GetBinContent(bin2)  << " & " << h6->GetBinContent(bin1)<<"\\textbackslash"<< h6->GetBinContent(bin2)  << " \\\\ \\hline"<<endl;
}

void PrintEfficiency2hists( string histname, string text, int bin1, int bin2, TFile* file1, TFile* file2, TFile* file3, TFile* file4, TFile* file5, TFile* file6 )
{
	double d1 = 47233078;
	double d2 = 10876000;
	double d3 = 1394548;
	double d4 = 204819;
	double d5 = 213384;
	double d6 = 193779;
	

	string histpath = "cascadingQCDAna15/"+histname;
	TH1D * h1 =  file1 -> Get(histpath.c_str());
	TH1D * h2 =  file2 -> Get(histpath.c_str());
	TH1D * h3 =  file3 -> Get(histpath.c_str());
	TH1D * h4 =  file4 -> Get(histpath.c_str());
	TH1D * h5 =  file5 -> Get(histpath.c_str());
	TH1D * h6 =  file6 -> Get(histpath.c_str());
	
	cout<<"\\multirow{2}{*}{ "<<text<<"} & "<<h1->GetBinContent(bin1)/d1 <<"\\textbackslash & " << h2->GetBinContent(bin1)/d2 << "\\textbackslash & " << h3->GetBinContent(bin1)/d3<< "\\textbackslash & " << h4->GetBinContent(bin1)/d4<< "\\textbackslash & " << h5->GetBinContent(bin1)/d5<< "\\textbackslash & " << h6->GetBinContent(bin1)/d6   << " \\\\ "<<endl;
	cout<<" & "<<h1->GetBinContent(bin2)/d1 << " & " << h2->GetBinContent(bin2)/d2 << " & " << h3->GetBinContent(bin2)/d3<< " & " << h4->GetBinContent(bin2)/d4<< " & " << h5->GetBinContent(bin2)/d5<< " & " << h6->GetBinContent(bin2)/d6  << " \\\\ \\hline"<<endl;
	
	//cout<< h1->GetBinContent(bin2)/d1 << " & " << h2->GetBinContent(bin1)/d2 <<"\\textbackslash"<< h2->GetBinContent(bin2)/d2 << " & " << h3->GetBinContent(bin1)/d3<<"\\textbackslash"<< h3->GetBinContent(bin2)/d3  << " & " << h4->GetBinContent(bin1)/d4<<"\\textbackslash"<< h4->GetBinContent(bin2)/d4  << " & " << h5->GetBinContent(bin1)/d5<<"\\textbackslash"<< h5->GetBinContent(bin2)/d5  << " & " << h6->GetBinContent(bin1)/d6<<"\\textbackslash"<< h6->GetBinContent(bin2)/d6  << " \\\\ \\hline"<<endl;

	
	//cout << text <<" & " << setprecision(3)<< h1->GetBinContent(bin1)/d1 <<"\\textbackslash"<< h1->GetBinContent(bin2)/d1 << " & " << h2->GetBinContent(bin1)/d2 <<"\\textbackslash"<< h2->GetBinContent(bin2)/d2 << " & " << h3->GetBinContent(bin1)/d3<<"\\textbackslash"<< h3->GetBinContent(bin2)/d3  << " & " << h4->GetBinContent(bin1)/d4<<"\\textbackslash"<< h4->GetBinContent(bin2)/d4  << " & " << h5->GetBinContent(bin1)/d5<<"\\textbackslash"<< h5->GetBinContent(bin2)/d5  << " & " << h6->GetBinContent(bin1)/d6<<"\\textbackslash"<< h6->GetBinContent(bin2)/d6  << " \\\\ \\hline"<<endl;
}

void PrintBinContent3hists( string histname, string text, int bin1, int bin2,int bin3, TFile* file1, TFile* file2, TFile* file3, TFile* file4, TFile* file5, TFile* file6 )
{
	string histpath = "cascadingQCDAna15/"+histname;
	TH1D * h1 =  file1 -> Get(histpath.c_str());
	TH1D * h2 =  file2 -> Get(histpath.c_str());
	TH1D * h3 =  file3 -> Get(histpath.c_str());
	TH1D * h4 =  file4 -> Get(histpath.c_str());
	TH1D * h5 =  file5 -> Get(histpath.c_str());
	TH1D * h6 =  file6 -> Get(histpath.c_str());
	cout << text <<" & " << h1->GetBinContent(bin1) <<"\\textbackslash"<< h1->GetBinContent(bin2)<<"\\textbackslash"<< h1->GetBinContent(bin3) << " & " << h2->GetBinContent(bin1) <<"\\textbackslash"<< h2->GetBinContent(bin2)<<"\\textbackslash"<< h2->GetBinContent(bin3) << " & " << h3->GetBinContent(bin1)<<"\\textbackslash"<< h3->GetBinContent(bin2) <<"\\textbackslash"<< h3->GetBinContent(bin3) << " & " << h4->GetBinContent(bin1)<<"\\textbackslash"<< h4->GetBinContent(bin2) <<"\\textbackslash"<< h4->GetBinContent(bin3)<< " & " << h5->GetBinContent(bin1)<<"\\textbackslash"<< h5->GetBinContent(bin2) <<"\\textbackslash"<< h5->GetBinContent(bin3) << " & " << h6->GetBinContent(bin1)<<"\\textbackslash"<< h6->GetBinContent(bin2) <<"\\textbackslash"<< h6->GetBinContent(bin3) << " \\\\ \\hline"<<endl;
}
void PrintEfficiency( string hist_numer, string hist_denom, string text, TFile* file1, TFile* file2, TFile* file3, TFile* file4, TFile* file5, TFile* file6 )
{
	string histpath_numer = "cascadingQCDAna15/"+hist_numer;
	TH1D * h1 =  file1 -> Get(histpath_numer.c_str());
	TH1D * h2 =  file2 -> Get(histpath_numer.c_str());
	TH1D * h3 =  file3 -> Get(histpath_numer.c_str());
	TH1D * h4 =  file4 -> Get(histpath_numer.c_str());
	TH1D * h5 =  file5 -> Get(histpath_numer.c_str());
	TH1D * h6 =  file6 -> Get(histpath_numer.c_str());
	
	string histpath_denom = "cascadingQCDAna15/"+hist_denom;

	TH1D * d1 =  file1 -> Get(histpath_denom.c_str());
	TH1D * d2 =  file2 -> Get(histpath_denom.c_str());
	TH1D * d3 =  file3 -> Get(histpath_denom.c_str());
	TH1D * d4 =  file4 -> Get(histpath_denom.c_str());
	TH1D * d5 =  file5 -> Get(histpath_denom.c_str());
	TH1D * d6 =  file6 -> Get(histpath_denom.c_str());
	
	cout << text <<" & " << h1->GetEntries()/d1->GetEntries() << " & " << h2->GetEntries()/d2->GetEntries() << " & " << h3->GetEntries()/d3->GetEntries() << " & " << h4->GetEntries()/d4->GetEntries() << " & " << h5->GetEntries()/d5->GetEntries() << " & " << h6->GetEntries()/d6->GetEntries() << " \\\\ \\hline"<<endl;
}

void PrintLatexTableEntries( TFile* file1, TFile* file2, TFile* file3, TFile* file4, TFile* file5, TFile* file6 )
{
	//---------------------------------------------------------------
	
	cout<<"Table 1: Number of Events"<<endl;

	
	cout << "\\begin{center}"<<endl;
	cout << "\\begin{tabular}{ | l | c | c | c | c | c | c | }"<<endl;
	
	cout << "\\hline"<<endl;
	cout << "  &  Data & QCD & ttbar & Z'(750) & Z'(1000) & Z'(1500) \\\\  \\hline"<<endl;
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	//cout << "Dataset  &   &  &  & 87243 & 133249 & 152561 \\\\  \\hline"<<endl;
	//cout << "HLT  &   &  &  & "<<87243-343<<" & "<<133249<<" & "<<152561<<" & \\\\  \\hline"<<endl;
	//cout << "Primary vertex filter  &   &  &  & "<<87243-343-24<<" & "<<133249<<" & "<<152561<<" & \\\\  \\hline"<<endl;
	//cout << "Primary vertex filter  &   &  &  & "<<87243-343-24-97<<" & "<<133249<<" & "<<152561<<" & \\\\  \\hline"<<endl;
	//cout << "Primary vertex filter  &   &  &  & "<<87243-343-24-97-79671<<" & "<<133249<<" & "<<152561<<" & \\\\  \\hline"<<endl;

	
	PrintEntries( "Nevents_analyzed", "Analyzer", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_preselected", "Preselected", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;

	PrintEntries( "Nevents_cascade12sig", "Cascading events 1+2 signal", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_cascade22sig", "Cascading events 2+2 signal", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_cascade11bkg", "Cascading events 1+1 bkg est", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_cascade12bkg", "Cascading events 1+2 bkg est", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_cascade22bkg", "Cascading events 2+2 bkg est", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	
		cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	PrintEntries( "Nevents_type11sig", "Type 11 pass events", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_type12sig", "Type 12 pass events", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_type22sig", "Type 22 pass events", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	
	
	TH1D * Nevents1_type11bkg						=  file1 -> Get("cascadingQCDAna15/Nevents_type11bkg");
	TH1D * Nevents1_type12bkg						=  file1 -> Get("cascadingQCDAna15/Nevents_type12bkg");
	TH1D * Nevents1_type22bkg						=  file1 -> Get("cascadingQCDAna15/Nevents_type22bkg");


	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	cout << "Type 11 bkg estimation & " << Nevents1_type11bkg->GetEntries() << " & & & & &  \\\\ \\hline"<<endl;
	cout << "Type 12 bkg estimation & " << Nevents1_type12bkg->GetEntries() << " & & & & &  \\\\ \\hline"<<endl;
	cout << "Type 22 bkg estimation & " << Nevents1_type22bkg->GetEntries() << " & & & & &  \\\\ \\hline"<<endl;

	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	PrintEntries( "Nevents_hasZeroTopTags", "0 top tags", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_hasOneTopTag", "1 top tag", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_hasTwoTopTags", "2 top tags", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );

	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	PrintEntries( "Nevents_hasZeroWTags", "0 W tags", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_hasOneWTag", "1 W tag", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_hasTwoWTags", "2 W tags", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	PrintEntries( "Nevents_hasZeroBTags", "0 B tags", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_hasOneBTag", "1 B tag", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_hasTwoBTags", "2 B tags", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	PrintEntries( "Nevents_hasZeroTightTops", "0 Tight Tops", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_hasOneTightTop", "1 Tight Top", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_hasTwoTightTops", "2 Tight Tops", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	PrintEntries( "Nevents_hasZeroLooseTops", "0 Loose Tops", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_hasOneLooseTop", "1 Loose Top", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_hasTwoLooseTops", "2 Loose Tops", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	PrintEntries( "Nevents_hasTaggedTopJet0", "top tag in leading hemisphere", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_hasTaggedTopJet1", "top tag in second leading hemisphere", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );	
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	PrintEntries( "Nevents_hasWTag0", "W tag in leading hemisphere", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_hasWTag1", "W tag in second leading hemisphere", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	PrintEntries( "Nevents_hasBTag0", "B tag in leading hemisphere", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_hasBTag1", "B tag in second leading hemisphere", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );

	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	PrintEntries( "Nevents_hasTightTop0", "Tight top in leading hemisphere", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_hasTightTop1", "Tight top in second leading hemisphere", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );

	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	PrintEntries( "Nevents_hasLooseTop0", "Loose top in leading hemisphere", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_hasLooseTop1", "Loose top in second leading hemisphere", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );



	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;

	PrintEntries( "Nevents_TopTagAndTightTop", "1 top tag 1 tight top", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_TopTagAndLooseTop", "1 top tag 1 loose top", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_TopTagAndWandB", "1 top 1 W 1 B", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_hasTwoWTags_hasOneBTag", "2 W tags 1 B tag", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_hasTwoWTags_hasTwoBTags", "2 W tags 2 B tags", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_hemiTop_hemiBnoW", "top tag, opposite hemi B no W", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );







	cout << "\\end{tabular}"<<endl;
	cout << "\\end{center}"<<endl;


}

void PrintLatexTableEfficiency( TFile* file1, TFile* file2, TFile* file3, TFile* file4, TFile* file5, TFile* file6 )
{
	//---------------------------------------------------------------
	cout<<"\\clearpage"<<endl;
	cout<<"Table 2: Efficiency"<<endl<<endl;
	cout<<"Denominator = preselected events"<<endl<<endl;

	
	cout << "\\begin{center}"<<endl;
	cout << "\\begin{tabular}{ | l | c | c | c | c | c | c | }"<<endl;
	
	cout << "\\hline"<<endl;
	cout << "  &  Data &QCD(flat pt)& ttbar & Z'(750) & Z'(1000) & Z'(1500) \\\\  \\hline"<<endl;
	
		cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;

	PrintEfficiency( "Nevents_cascade12sig", "Nevents_preselected", "Cascading events 1+2 signal", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_cascade22sig", "Nevents_preselected", "Cascading events 2+2 signal", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_cascade11bkg", "Nevents_preselected", "Cascading events 1+1 bkg est", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_cascade12bkg", "Nevents_preselected", "Cascading events 1+2 bkg est", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_cascade22bkg", "Nevents_preselected", "Cascading events 2+2 bkg est", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );

	
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	PrintEfficiency( "Nevents_type11sig", "Nevents_preselected", "Type 11 pass events", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_type12sig", "Nevents_preselected", "Type 12 pass events", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_type22sig", "Nevents_preselected", "Type 22 pass events", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	
	
	TH1D * Nevents1_type11bkg						=  file1 -> Get("cascadingQCDAna15/Nevents_type11bkg");
	TH1D * Nevents1_type12bkg						=  file1 -> Get("cascadingQCDAna15/Nevents_type12bkg");
	TH1D * Nevents1_type22bkg						=  file1 -> Get("cascadingQCDAna15/Nevents_type22bkg");
	TH1D * Nevents1_preselected						=  file1 -> Get("cascadingQCDAna15/Nevents_preselected");


	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	cout << "Type 11 bkg estimation & " << Nevents1_type11bkg->GetEntries()/Nevents1_preselected->GetEntries()  << " & & & & &  \\\\ \\hline"<<endl;
	cout << "Type 12 bkg estimation & " << Nevents1_type12bkg->GetEntries()/Nevents1_preselected->GetEntries()  << " & & & & &  \\\\ \\hline"<<endl;
	cout << "Type 22 bkg estimation & " << Nevents1_type22bkg->GetEntries()/Nevents1_preselected->GetEntries()  << " & & & & &  \\\\ \\hline"<<endl;


	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	PrintEfficiency( "Nevents_hasZeroTopTags", "Nevents_preselected", "0 top tags", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_hasOneTopTag", "Nevents_preselected", "1 top tag", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_hasTwoTopTags", "Nevents_preselected", "2 top tags", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );

	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	PrintEfficiency( "Nevents_hasZeroWTags", "Nevents_preselected", "0 W tags", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_hasOneWTag", "Nevents_preselected", "1 W tag", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_hasTwoWTags", "Nevents_preselected", "2 W tags", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	PrintEfficiency( "Nevents_hasZeroBTags", "Nevents_preselected", "0 B tags", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_hasOneBTag", "Nevents_preselected", "1 B tag", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_hasTwoBTags", "Nevents_preselected", "2 B tags", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	PrintEfficiency( "Nevents_hasZeroTightTops", "Nevents_preselected", "0 Tight Tops", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_hasOneTightTop", "Nevents_preselected", "1 Tight Top", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_hasTwoTightTops", "Nevents_preselected", "2 Tight Tops", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	PrintEfficiency( "Nevents_hasZeroLooseTops", "Nevents_preselected", "0 Loose Tops", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_hasOneLooseTop", "Nevents_preselected", "1 Loose Top", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_hasTwoLooseTops", "Nevents_preselected", "2 Loose Tops", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	PrintEfficiency( "Nevents_hasTaggedTopJet0", "Nevents_preselected", "top tag in leading hemisphere", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_hasTaggedTopJet1", "Nevents_preselected", "top tag in second leading hemisphere", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );	
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	PrintEfficiency( "Nevents_hasWTag0", "Nevents_preselected", "W tag in leading hemisphere", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_hasWTag1", "Nevents_preselected", "W tag in second leading hemisphere", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	PrintEfficiency( "Nevents_hasBTag0", "Nevents_preselected", "B tag in leading hemisphere", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_hasBTag1", "Nevents_preselected", "B tag in second leading hemisphere", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );

	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	PrintEfficiency( "Nevents_hasTightTop0", "Nevents_preselected", "Tight top in leading hemisphere", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_hasTightTop1", "Nevents_preselected", "Tight top in second leading hemisphere", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );

	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	
	PrintEfficiency( "Nevents_hasLooseTop0", "Nevents_preselected", "Loose top in leading hemisphere", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_hasLooseTop1", "Nevents_preselected", "Loose top in second leading hemisphere", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );


	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;

	PrintEfficiency( "Nevents_TopTagAndTightTop", "Nevents_preselected", "1 top tag 1 tight top", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_TopTagAndLooseTop", "Nevents_preselected", "1 top tag 1 loose top", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_TopTagAndWandB", "Nevents_preselected", "1 top 1 W 1 B", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_hasTwoWTags_hasOneBTag", "Nevents_preselected", "2 W tags 1 B tag", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_hasTwoWTags_hasTwoBTags", "Nevents_preselected", "2 W tags 2 B tags", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency( "Nevents_hemiTop_hemiBnoW", "Nevents_preselected", "top tag, opposite hemi B no W", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );





	cout << "\\end{tabular}"<<endl;
	cout << "\\end{center}"<<endl;


}






void PrintLatexTableCutFlow( TFile* file1, TFile* file2, TFile* file3, TFile* file4, TFile* file5, TFile* file6 )
{
	//---------------------------------------------------------------
	
	cout<<"Table 1: Cut flow - number of events passing succesive cuts"<<endl;

	
	cout << "\\begin{center}"<<endl;
	cout << "\\begin{tabular}{ | l | c | c | c | c | c | c | }"<<endl;
	
	cout << "\\hline"<<endl;

	cout << "  &  \\textbf\{Data\} & \\textbf\{QCD(flat pt)\} & \\textbf\{ttbar\} & \\textbf\{Z'(750)\} & \\textbf\{Z'(1000)\} & \\textbf\{Z'(1500)\} \\\\  \\hline"<<endl;
	
	//cout << "\\noalign{\\smallskip}"<<endl;
	//cout << "\\noalign{\\smallskip}"<<endl;
	//cout << "\\noalign{\\smallskip}"<<endl;
	//cout << "\\hline"<<endl;
	
	
	/*
	
	
	-------------------Jet--------------------------
        hltSelection  : visited   16670180 , pass    9484713 , fail    7185467
        scrapingVeto  : visited    9484713 , pass    9483317 , fail       1396
 primaryVertexFilter  : visited    9483317 , pass    8373976 , fail    1109341
     HBHENoiseFilter  : visited    8373976 , pass    8338229 , fail      35747
           jetFilter  : visited    8338229 , pass     878319 , fail    7459910
-------------------JetMET--------------------------
        hltSelection  : visited   21800179 , pass    7670844 , fail   14129335
        scrapingVeto  : visited    7670844 , pass    7670797 , fail         47
 primaryVertexFilter  : visited    7670797 , pass    7183970 , fail     486827
     HBHENoiseFilter  : visited    7183970 , pass    7157825 , fail      26145
           jetFilter  : visited    7157825 , pass      92392 , fail    7065433
-------------------JetMETTau--------------------------
        hltSelection  : visited    8762719 , pass     750095 , fail    8012624
        scrapingVeto  : visited     750095 , pass     750082 , fail         13
 primaryVertexFilter  : visited     750082 , pass     700089 , fail      49993
     HBHENoiseFilter  : visited     700089 , pass     697396 , fail       2693
           jetFilter  : visited     697396 , pass       8820 , fail     688576
           
           -------------------Total--------------------------
        hltSelection  : visited   47233078 , pass     17905652 , fail    
        scrapingVeto  : visited            , pass     17904196 , fail         
 primaryVertexFilter  : visited            , pass     16258035 , fail      
     HBHENoiseFilter  : visited            , pass     16193450 , fail       
           jetFilter  : visited            , pass       979531 , fail     
	*/
	// data 15042368+ 24064576 + 20267734
	//                                         data     QCD herwig  ttbarD6T  750       1000     1500
	cout << "Dataset                        &  47233078 & 10876000 & 1394548 & 204819 & 213384 & 193779 \\\\  \\hline"<<endl;
	cout << "HLT                            &  17905652 & 7546508  & 1366122 & 204091 & 213041 & 193637 \\\\  \\hline"<<endl;
	cout << "Scraping veto                  &  17904196 & 7546508  & 1366122 & 204091 & 213041 & 193637 \\\\  \\hline"<<endl;
	cout << "Primary vertex filter          &  16258035 & 7545471  & 1365931 & 204054 & 213017 & 193611 \\\\  \\hline"<<endl;
	cout << "HBHE Noise Filter              &  16193450 & 7543613  & 1365777 & 203998 & 212920 & 193490 \\\\  \\hline"<<endl;
	cout << "2 jets with pt$>$200 and $|$eta$|$ $<$ 2.4 &  979531   & 2639162  & 98974   & 87243  & 133249 & 152561 \\\\  \\hline"<<endl;
	////cout << "HLT  &   &  &  & "<<87243-343<<" & "<<133249<<" & "<<152561<<" & \\\\  \\hline"<<endl;
	////cout << "Primary vertex filter  &   &  &  & "<<87243-343-24<<" & "<<133249<<" & "<<152561<<" & \\\\  \\hline"<<endl;
	////cout << "Primary vertex filter  &   &  &  & "<<87243-343-24-97<<" & "<<133249<<" & "<<152561<<" & \\\\  \\hline"<<endl;
	////cout << "Primary vertex filter  &   &  &  & "<<87243-343-24-97-79671<<" & "<<133249<<" & "<<152561<<" & \\\\  \\hline"<<endl;

	
	//PrintEntries( "Nevents_analyzed", "Analyzer", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEntries( "Nevents_preselected", "$\\ge$ 1 jet per hemisphere", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	//cout << "\\hline"<<endl;
	//cout << "\\textbf{Type 1+1 signal cut flow &  &  &  &  &   \\\\  \\hline"<<endl;
	//cout << "\\textbf{Type 1+1 signal cut flow\\} &  Data & QCD & ttbar & Z'(750) & Z'(1000) & Z'(1500)   \\\\  \\hline"<<endl;
	//cout<<"\\multicolumn{7}{|c|}{Type 1+1 signal cut flow} \\\\ \\hline"<<endl;
	cout<<"\\multicolumn{7}{c}{\\textbf\{Type 1+1 signal\}\} \\\\ \\hline"<<endl;
	PrintBinContent( "Nevents_type11sig_cutflow", "Hemi0 has top jet", 4, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type11sig_cutflow", "Hemi1 has top jet", 5, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type11sig_cutflow", "Deltaphi $>$ 2.1", 6, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );


	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	//cout << "\\hline"<<endl;
	cout<<"\\multicolumn{7}{c}{\\textbf\{Type 1+2 signal\}\} \\\\ \\hline"<<endl;
	PrintBinContent( "Nevents_type12sig_cutflow", "Cascading selection", 4, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type12sig_cutflow", "Has 1 W tag", 5, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type12sig_cutflow", "Has a tight top", 6, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type12sig_cutflow", "Has a top jet in opposite hemi", 7, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	//cout << "\\hline"<<endl;
	cout<<"\\multicolumn{7}{c}{\\textbf\{Type 2+2 signal\}\} \\\\ \\hline"<<endl;
	PrintBinContent( "Nevents_type22sig_cutflow", "Cascading selection", 4, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type22sig_cutflow", "Has a tight top", 5, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent2hists( "Nevents_type22sig_cutflow", "\{2 tight\}\\textbackslash\{1 tight 1 loose\}", 6,7, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	//PrintBinContent( "Nevents_type22sig_cutflow", "Has two tight tops", 6, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	//PrintBinContent( "Nevents_type22sig_cutflow", "Has a tight and a loose top", 7, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	//cout << "\\hline"<<endl;
	cout<<"\\multicolumn{7}{c}{\\textbf\{Type 1+1 background estimation\}\} \\\\ \\hline"<<endl;
	PrintBinContent( "Nevents_type11bkg_cutflow", "Cascading selection", 4, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type11bkg_cutflow", "Deltaphi $>$ 2.1", 5, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type11bkg_cutflow", "has a top tag", 6, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type11bkg_cutflow", "opposite hemi anti-tagged", 7, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type11bkg_cutflow", "opposite hemi no 2nd leading btag", 8, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type11bkg_cutflow", "probe jet pt$>$250", 9, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );

	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	//cout << "\\hline"<<endl;
	cout<<"\\multicolumn{7}{c}{\\textbf\{Type 1+2 background estimation\}\} \\\\ \\hline"<<endl;
	PrintBinContent( "Nevents_type12bkg_cutflow", "Cascading selection", 4, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type12bkg_cutflow", "No W tags", 5, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type12bkg_cutflow", "1 top jet", 6, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type12bkg_cutflow", "has a b tag", 7, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type12bkg_cutflow", "b tag in hemi opposite top jet", 8, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type12bkg_cutflow", "there is a 2nd jet in the b-tag hemi", 9, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type12bkg_cutflow", "top mass window", 10, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type12bkg_cutflow", "W probe pT$>$200", 11, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );

	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	//cout << "\\hline"<<endl;
	cout<<"\\multicolumn{7}{c}{\\textbf\{Type 2+2 background estimation\}\} \\\\ \\hline"<<endl;
	PrintBinContent( "Nevents_type22bkg_cutflow", "Cascading selection", 3, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type22bkg_cutflow", "1 W tag", 4, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type22bkg_cutflow", "has a b tag", 5, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	cout<<"\\multicolumn{7}{|c|}{Case A - 2 b tags, 1 tight top} \\\\ \\hline"<<endl;
	PrintBinContent( "Nevents_type22bkg_cutflow", "has a tight top", 6, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type22bkg_cutflow", "has a b tag in hemi opposite tight top", 7, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type22bkg_cutflow", "opposite hemi passes top mass window", 8, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type22bkg_cutflow", "W probe pt$>$200", 9, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	cout<<"\\multicolumn{7}{|c|}{Case B - 1 b tag, 1 tight top} \\\\ \\hline"<<endl;
	PrintBinContent( "Nevents_type22bkg_cutflow", "has a tight top", 6, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type22bkg_cutflow", "does not have b in opposite hemi", 10, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type22bkg_cutflow", "has at least two jets in opposite hemi", 11, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type22bkg_cutflow", "opposite hemi passes top mass window", 12, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type22bkg_cutflow", "W probe pt$>$200", 13, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	cout<<"\\multicolumn{7}{|c|}{Case C - 1 b tag, 1 loose top} \\\\ \\hline"<<endl;
	PrintBinContent( "Nevents_type22bkg_cutflow", "has a loose top", 14, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type22bkg_cutflow", "opposite hemi passes top mass window", 15, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintBinContent( "Nevents_type22bkg_cutflow", "W probe pt$>$200", 16, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	
	
	//PrintBinContent2hists( "Nevents_type22bkg_cutflow", "\{case A and B - has a tight top\}\\textbackslash\{case C - has a loose top\}", 6,7, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	//PrintBinContent3hists( "Nevents_type22bkg_cutflow", "\{case A and B - has a tight top\}\\textbackslash\{case C - has a loose top\}", 6,7, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );


	cout << "\\end{tabular}"<<endl;
	cout << "\\end{center}"<<endl;


}



void PrintLatexTableCutFlowEfficiency( TFile* file1, TFile* file2, TFile* file3, TFile* file4, TFile* file5, TFile* file6 )
{
	//---------------------------------------------------------------
	
	cout<<"Table 2: Cut flow Efficiency- denominator = number of events in dataset"<<endl;

	
	cout << "\\begin{center}"<<endl;
	cout << "\\begin{tabular}{ | l | c | c | c | c | c | c | }"<<endl;
	
	cout << "\\hline"<<endl;

	cout << "  &  \\textbf\{Data\} & \\textbf\{QCD(flat pt)\} & \\textbf\{ttbar\} & \\textbf\{Z'(750)\} & \\textbf\{Z'(1000)\} & \\textbf\{Z'(1500)\} \\\\  \\hline"<<endl;
	
	//cout << "\\noalign{\\smallskip}"<<endl;
	//cout << "\\noalign{\\smallskip}"<<endl;
	//cout << "\\noalign{\\smallskip}"<<endl;
	//cout << "\\hline"<<endl;
	
	
	/*
	
	
	-------------------Jet--------------------------
        hltSelection  : visited   16670180 , pass    9484713 , fail    7185467
        scrapingVeto  : visited    9484713 , pass    9483317 , fail       1396
 primaryVertexFilter  : visited    9483317 , pass    8373976 , fail    1109341
     HBHENoiseFilter  : visited    8373976 , pass    8338229 , fail      35747
           jetFilter  : visited    8338229 , pass     878319 , fail    7459910
-------------------JetMET--------------------------
        hltSelection  : visited   21800179 , pass    7670844 , fail   14129335
        scrapingVeto  : visited    7670844 , pass    7670797 , fail         47
 primaryVertexFilter  : visited    7670797 , pass    7183970 , fail     486827
     HBHENoiseFilter  : visited    7183970 , pass    7157825 , fail      26145
           jetFilter  : visited    7157825 , pass      92392 , fail    7065433
-------------------JetMETTau--------------------------
        hltSelection  : visited    8762719 , pass     750095 , fail    8012624
        scrapingVeto  : visited     750095 , pass     750082 , fail         13
 primaryVertexFilter  : visited     750082 , pass     700089 , fail      49993
     HBHENoiseFilter  : visited     700089 , pass     697396 , fail       2693
           jetFilter  : visited     697396 , pass       8820 , fail     688576
           
           -------------------Total--------------------------
        hltSelection  : visited   47233078 , pass     17905652 , fail    
        scrapingVeto  : visited            , pass     17904196 , fail         
 primaryVertexFilter  : visited            , pass     16258035 , fail      
     HBHENoiseFilter  : visited            , pass     16193450 , fail       
           jetFilter  : visited            , pass       979531 , fail     
	*/
	// data 15042368+ 24064576 + 20267734
	//                                         data     QCD herwig  ttbarD6T  750       1000     1500
	cout << "Dataset                        &  "<<setprecision(3)<<47233078.0/47233078.0 <<"& "<<10876000.0/10876000.0 <<" & "<< 1394548.0/1394548.0 <<" &"<<  204819.0/204819.0 <<"&"<<  213384.0/213384.0 <<" &"<<   193779.0/193779.0 <<" \\\\  \\hline"<<endl;
	cout << "HLT                            &  "<<17905652.0/47233078.0 <<"& "<<7546508.0/10876000.0 <<"  & "<< 1366122.0/1394548.0 <<" &"<<  204091.0/204819.0 <<" &"<<  213041.0/213384.0 <<" &"<<   193637.0/193779.0 <<" \\\\  \\hline"<<endl;
	cout << "Scraping veto                  &  "<<17904196.0/47233078.0 <<"& "<<7546508.0/10876000.0 <<"  & "<< 1366122.0/1394548.0 <<" &"<<  204091.0/204819.0 <<" &"<<  213041.0/213384.0 <<" &"<<   193637.0/193779.0 <<" \\\\  \\hline"<<endl;
	cout << "Primary vertex filter          &  "<<16258035.0/47233078.0 <<"& "<<7545471.0/10876000.0 <<"  & "<< 1365931.0/1394548.0 <<" &"<<  204054.0/204819.0 <<" &"<<  213017.0/213384.0 <<" &"<<   193611.0/193779.0 <<" \\\\  \\hline"<<endl;
	cout << "HBHE Noise Filter              &  "<<16193450.0/47233078.0 <<"& "<<7543613.0/10876000.0 <<"  & "<< 1365777.0/1394548.0 <<" &"<<  203998.0/204819.0 <<" &"<<  212920.0/213384.0 <<" &"<<   193490.0/193779.0 <<" \\\\  \\hline"<<endl;
	cout << "2 jets with pt$>$200 and $|$eta$|$ $<$ 2.4 &"<<  979531.0/47233078.0   <<"&"<< 2639162.0/10876000.0 <<"  & "<< 98974.0/1394548.0 <<"   &"<<  87243.0/204819.0 <<"  &"<<  133249.0/213384.0 <<" &"<<   152561.0/193779.0 <<" \\\\  \\hline"<<endl;
	////cout << "HLT  &   &  &  & "<<87243-343<<" & "<<133249<<" & "<<152561<<" & \\\\  \\hline"<<endl;
	////cout << "Primary vertex filter  &   &  &  & "<<87243-343-24<<" & "<<133249<<" & "<<152561<<" & \\\\  \\hline"<<endl;
	////cout << "Primary vertex filter  &   &  &  & "<<87243-343-24-97<<" & "<<133249<<" & "<<152561<<" & \\\\  \\hline"<<endl;
	////cout << "Primary vertex filter  &   &  &  & "<<87243-343-24-97-79671<<" & "<<133249<<" & "<<152561<<" & \\\\  \\hline"<<endl;

	
	//PrintEntries( "Nevents_analyzed", "Analyzer", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency2( "Nevents_preselected", "$\\ge$ 1 jet per hemisphere", FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	//cout << "\\hline"<<endl;
	//cout << "\\textbf{Type 1+1 signal cut flow &  &  &  &  &   \\\\  \\hline"<<endl;
	//cout << "\\textbf{Type 1+1 signal cut flow\\} &  Data & QCD & ttbar & Z'(750) & Z'(1000) & Z'(1500)   \\\\  \\hline"<<endl;
	//cout<<"\\multicolumn{7}{|c|}{Type 1+1 signal cut flow} \\\\ \\hline"<<endl;
	cout<<"\\multicolumn{7}{c}{\\textbf\{Type 1+1 signal\}\} \\\\ \\hline"<<endl;
	PrintEfficiency3( "Nevents_type11sig_cutflow", "Hemi0 has top jet", 4, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type11sig_cutflow", "Hemi1 has top jet", 5, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type11sig_cutflow", "Deltaphi $>$ 2.1", 6, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );


	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	//cout << "\\hline"<<endl;
	cout<<"\\multicolumn{7}{c}{\\textbf\{Type 1+2 signal\}\} \\\\ \\hline"<<endl;
	PrintEfficiency3( "Nevents_type12sig_cutflow", "Cascading selection", 4, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type12sig_cutflow", "Has 1 W tag", 5, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type12sig_cutflow", "Has a tight top", 6, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type12sig_cutflow", "Has a top jet in opposite hemi", 7, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	//cout << "\\hline"<<endl;
	cout<<"\\multicolumn{7}{c}{\\textbf\{Type 2+2 signal\}\} \\\\ \\hline"<<endl;
	PrintEfficiency3( "Nevents_type22sig_cutflow", "Cascading selection", 4, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type22sig_cutflow", "Has a tight top", 5, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency2hists( "Nevents_type22sig_cutflow", "\{2 tight\}\\textbackslash\{1 tight 1 loose\}", 6,7, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	//PrintEfficiency3( "Nevents_type22sig_cutflow", "Has two tight tops", 6, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	//PrintEfficiency3( "Nevents_type22sig_cutflow", "Has a tight and a loose top", 7, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	//cout << "\\hline"<<endl;
	cout<<"\\multicolumn{7}{c}{\\textbf\{Type 1+1 background estimation\}\} \\\\ \\hline"<<endl;
	PrintEfficiency3( "Nevents_type11bkg_cutflow", "Cascading selection", 4, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type11bkg_cutflow", "Deltaphi $>$ 2.1", 5, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type11bkg_cutflow", "has a top tag", 6, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type11bkg_cutflow", "opposite hemi anti-tagged", 7, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type11bkg_cutflow", "opposite hemi no 2nd leading btag", 8, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type11bkg_cutflow", "probe jet pt$>$250", 9, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );

	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	//cout << "\\hline"<<endl;
	cout<<"\\multicolumn{7}{c}{\\textbf\{Type 1+2 background estimation\}\} \\\\ \\hline"<<endl;
	PrintEfficiency3( "Nevents_type12bkg_cutflow", "Cascading selection", 4, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type12bkg_cutflow", "No W tags", 5, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type12bkg_cutflow", "1 top jet", 6, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type12bkg_cutflow", "has a b tag", 7, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type12bkg_cutflow", "b tag in hemi opposite top jet", 8, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type12bkg_cutflow", "there is a 2nd jet in the b-tag hemi", 9, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type12bkg_cutflow", "top mass window", 10, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type12bkg_cutflow", "W probe pT$>$200", 11, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );

	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\noalign{\\smallskip}"<<endl;
	//cout << "\\hline"<<endl;
	cout<<"\\multicolumn{7}{c}{\\textbf\{Type 2+2 background estimation\}\} \\\\ \\hline"<<endl;
	PrintEfficiency3( "Nevents_type22bkg_cutflow", "Cascading selection", 3, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type22bkg_cutflow", "1 W tag", 4, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type22bkg_cutflow", "has a b tag", 5, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	cout<<"\\multicolumn{7}{|c|}{Case A - 2 b tags, 1 tight top} \\\\ \\hline"<<endl;
	PrintEfficiency3( "Nevents_type22bkg_cutflow", "has a tight top", 6, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type22bkg_cutflow", "has a b tag in hemi opposite tight top", 7, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type22bkg_cutflow", "opposite hemi passes top mass window", 8, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type22bkg_cutflow", "W probe pt$>$200", 9, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	cout<<"\\multicolumn{7}{|c|}{Case B - 1 b tag, 1 tight top} \\\\ \\hline"<<endl;
	PrintEfficiency3( "Nevents_type22bkg_cutflow", "has a tight top", 6, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type22bkg_cutflow", "does not have b in opposite hemi", 10, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type22bkg_cutflow", "has at least two jets in opposite hemi", 11, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type22bkg_cutflow", "opposite hemi passes top mass window", 12, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type22bkg_cutflow", "W probe pt$>$200", 13, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	cout << "\\noalign{\\smallskip}"<<endl;
	cout << "\\hline"<<endl;
	cout<<"\\multicolumn{7}{|c|}{Case C - 1 b tag, 1 loose top} \\\\ \\hline"<<endl;
	PrintEfficiency3( "Nevents_type22bkg_cutflow", "has a loose top", 14, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type22bkg_cutflow", "opposite hemi passes top mass window", 15, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	PrintEfficiency3( "Nevents_type22bkg_cutflow", "W probe pt$>$200", 16, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	
	
	//PrintBinContent2hists( "Nevents_type22bkg_cutflow", "\{case A and B - has a tight top\}\\textbackslash\{case C - has a loose top\}", 6,7, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );
	//PrintBinContent3hists( "Nevents_type22bkg_cutflow", "\{case A and B - has a tight top\}\\textbackslash\{case C - has a loose top\}", 6,7, FILE, ROOT_QCD_herwigpp, ROOT_TTJets_TuneD6T, ROOT_Zprime_M750GeV_W7500MeV, ROOT_Zprime_M1000GeV_W10GeV, ROOT_Zprime_M1500GeV_W15GeV );


	cout << "\\end{tabular}"<<endl;
	cout << "\\end{center}"<<endl;


}
