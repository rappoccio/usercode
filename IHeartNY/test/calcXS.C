
void calcOne(TString which, bool parton, bool doel);

void calcXS() {
  
  // CT10
  cout << endl;
  calcOne("CT10_nom",false,false);
  calcOne("CT10_nom",false,true);
  calcOne("CT10_nom",true,false);
  calcOne("CT10_nom",true,true);

  cout << endl;
  calcOne("CT10_pdfup",false,false);
  calcOne("CT10_pdfup",false,true);
  calcOne("CT10_pdfup",true,false);
  calcOne("CT10_pdfup",true,true);

  cout << endl;
  calcOne("CT10_pdfdown",false,false);
  calcOne("CT10_pdfdown",false,true);
  calcOne("CT10_pdfdown",true,false);
  calcOne("CT10_pdfdown",true,true);

  // MSTW
  cout << endl;
  calcOne("MSTW_nom",false,false);
  calcOne("MSTW_nom",false,true);
  calcOne("MSTW_nom",true,false);
  calcOne("MSTW_nom",true,true);

  cout << endl;
  calcOne("MSTW_pdfup",false,false);
  calcOne("MSTW_pdfup",false,true);
  calcOne("MSTW_pdfup",true,false);
  calcOne("MSTW_pdfup",true,true);

  cout << endl;
  calcOne("MSTW_pdfdown",false,false);
  calcOne("MSTW_pdfdown",false,true);
  calcOne("MSTW_pdfdown",true,false);
  calcOne("MSTW_pdfdown",true,true);

  // NNPDF
  cout << endl;
  calcOne("NNPDF_nom",false,false);
  calcOne("NNPDF_nom",false,true);
  calcOne("NNPDF_nom",true,false);
  calcOne("NNPDF_nom",true,true);

  cout << endl;
  calcOne("NNPDF_pdfup",false,false);
  calcOne("NNPDF_pdfup",false,true);
  calcOne("NNPDF_pdfup",true,false);
  calcOne("NNPDF_pdfup",true,true);

  cout << endl;
  calcOne("NNPDF_pdfdown",false,false);
  calcOne("NNPDF_pdfdown",false,true);
  calcOne("NNPDF_pdfdown",true,false);
  calcOne("NNPDF_pdfdown",true,true);

  // Q2
  cout << endl;
  calcOne("scaleup",false,false);
  calcOne("scaleup",false,true);
  calcOne("scaleup",true,false);
  calcOne("scaleup",true,true);

  cout << endl;
  calcOne("scaledown",false,false);
  calcOne("scaledown",false,true);
  calcOne("scaledown",true,false);
  calcOne("scaledown",true,true);

  cout << endl;
  calcOne("MG",false,false);
  calcOne("MG",false,true);
  calcOne("MG",true,false);
  calcOne("MG",true,true);

  cout << endl;
  calcOne("mcnlo",false,false);
  calcOne("mcnlo",false,true);
  calcOne("mcnlo",true,false);
  calcOne("mcnlo",true,true);
  cout << endl;

}

void calcOne(TString which, bool parton, bool doel) {

  if (which=="MG") {  
    if (doel) TFile* f1 = new TFile("histfiles_MG/TTJets_SemiLeptMGDecays_8TeV-madgraph_iheartNY_V1_el_2Dcut_nom.root");
    else TFile* f1 = new TFile("histfiles_MG/TTJets_SemiLeptMGDecays_8TeV-madgraph_iheartNY_V1_mu_2Dcut_nom.root");
  }
  else if (which=="mcnlo") {  
    //if (doel) TFile* f1 = new TFile("histfiles_mcnlo/TT_mcatnlo_iheartNY_V1_el_2Dcut_nom.root");
    //else TFile* f1 = new TFile("histfiles_mcnlo/TT_mcatnlo_iheartNY_V1_mu_2Dcut_nom.root");
    if (doel) TFile* f1 = new TFile("histfiles_mcnlo_weight/TT_mcatnlo_iheartNY_V1_el_2Dcut_nom.root");
    else TFile* f1 = new TFile("histfiles_mcnlo_weight/TT_mcatnlo_iheartNY_V1_mu_2Dcut_nom.root");
  }
  else if (doel) {
    TFile* f1 = new TFile("histfiles_"+which+"/postfit_combfit/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_"+which+"_2Dcut_postfit_nom.root");
    TFile* f2 = new TFile("histfiles_"+which+"/postfit_combfit/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_"+which+"_2Dcut_postfit_nom.root");
    TFile* f3 = new TFile("histfiles_"+which+"/postfit_combfit/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_"+which+"_2Dcut_postfit_nom.root");

    /*
    // additional normalization
    TFile* fn1 = new TFile("histfiles_CT10_nom/qcd_el/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_CT10_nom_2Dcut_nom.root");
    TFile* fn2 = new TFile("histfiles_CT10_nom/qcd_el/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_CT10_nom_2Dcut_nom.root");
    TFile* fn3 = new TFile("histfiles_CT10_nom/qcd_el/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_CT10_nom_2Dcut_nom.root");
    */
  }
  else {
    TFile* f1 = new TFile("histfiles_"+which+"/postfit_combfit/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+which+"_2Dcut_postfit_nom.root");
    TFile* f2 = new TFile("histfiles_"+which+"/postfit_combfit/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+which+"_2Dcut_postfit_nom.root");
    TFile* f3 = new TFile("histfiles_"+which+"/postfit_combfit/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+which+"_2Dcut_postfit_nom.root");

    /*
    // additional normalization
    TFile* fn1 = new TFile("histfiles_CT10_nom/2Dhists/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_2Dcut_nom.root");
    TFile* fn2 = new TFile("histfiles_CT10_nom/2Dhists/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_2Dcut_nom.root");
    TFile* fn3 = new TFile("histfiles_CT10_nom/2Dhists/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_2Dcut_nom.root");
    */
  }

  TString whatDEN = "ptGenTop";
  TString whatNUM = "ptGenTop_passParton";
  if (!parton) whatNUM = "ptPartTop_passParticle";

  if (which=="MG" || which=="mcnlo") {
    TH1F* h1 = (TH1F*) f1->Get(whatDEN);
    TH1F* h11 = (TH1F*) f1->Get(whatNUM);
  }
  else {
    TH1F* h1 = (TH1F*) f1->Get(whatDEN);
    TH1F* h2 = (TH1F*) f2->Get(whatDEN);
    TH1F* h3 = (TH1F*) f3->Get(whatDEN);
    TH1F* h11 = (TH1F*) f1->Get(whatNUM);
    TH1F* h22 = (TH1F*) f2->Get(whatNUM);
    TH1F* h33 = (TH1F*) f3->Get(whatNUM);
  }

  float normPDF = 1.0;
  
  int iwhich = 0;
  if (which.Contains("_pdfup")) iwhich = 1;
  else if (which.Contains("_pdfdown")) iwhich = 2;
  else if (which=="scaleup") iwhich = 3;
  else if (which=="scaledown") iwhich = 4;
  
  double ttbar_xs[5] = {
    252.89,  // nominal
    252.89,  // CT10 up
    252.89,  // CT10 down
    (252.89+6.39),  // q2 up
    (252.89-8.64)   // q2 down
  };
  double ttbar_nevents[5][3] = {
    {21675970.,3082812.,1249111.},  // nominal
    {21675970.,3082812.,1249111.},  // CT10 up
    {21675970.,3082812.,1249111.},  // CT10 down
    {14983686.,2243672.,1241650.},  // q2 up
    {14545715*89./102.,2170074.,1308090.}   // q2 down
  };
  double ttbar_eff[5][3] = {
    {1.0, 0.074, 0.015},  // nominal
    {1.0, 0.074, 0.015},  // CT10 up
    {1.0, 0.074, 0.015},  // CT10 down
    {1.0, 0.074, 0.014},  // q2 up
    {1.0, 0.081, 0.016}   // q2 down
  };
  
  
  if (which=="MG") {
    double ttbar_norm = 252.89/25424818.*0.438;
    h1->Scale(ttbar_norm);
    h11->Scale(ttbar_norm);
  }
  else if (which=="mcnlo") {
    // weights!
    TH1F* hw = (TH1F*) f1->Get("nevt");
    float ntot = (float) nevt->GetEntries();
    float nw =  (float) nevt->GetSum();
    float adjust = (float)nw/ntot;
    cout << "adjust mc@nlo total by " << adjust << " (= " << (int)nw << " / " << (int)ntot << ")" << endl;
    
    double ttbar_norm = 252.89/(32852589*adjust);
    h1->Scale(ttbar_norm);
    h11->Scale(ttbar_norm);
  }
  else {

    /*
    // correcting the inclusive cross section for PDF up/down is not really needed when taking the ratio in (pass pt>400)/(all)
    if (which=="CT10_pdfup" || which=="CT10_pdfdown") {

      TH1F* h1_den = (TH1F*) f1->Get("mttbarGen0");
      TH1F* h2_den = (TH1F*) f2->Get("mttbarGen0");
      TH1F* h3_den = (TH1F*) f3->Get("mttbarGen0");
      TH1F* h1_num = (TH1F*) fn1->Get("mttbarGen0");
      TH1F* h2_num = (TH1F*) fn2->Get("mttbarGen0");
      TH1F* h3_num = (TH1F*) fn3->Get("mttbarGen0");

      h1_num->Sumw2();
      h2_num->Sumw2();
      h3_num->Sumw2();
      h1_num->Scale(ttbar_xs[iwhich] * ttbar_eff[iwhich][0] / ttbar_nevents[iwhich][0]); 
      h2_num->Scale(ttbar_xs[iwhich] * ttbar_eff[iwhich][1] / ttbar_nevents[iwhich][1]); 
      h3_num->Scale(ttbar_xs[iwhich] * ttbar_eff[iwhich][2] / ttbar_nevents[iwhich][2]); 
      h1_num->Add(h2_num);
      h1_num->Add(h3_num);
      h1_den->Sumw2();
      h2_den->Sumw2();
      h3_den->Sumw2();
      h1_den->Scale(ttbar_xs[iwhich] * ttbar_eff[iwhich][0] / ttbar_nevents[iwhich][0]); 
      h2_den->Scale(ttbar_xs[iwhich] * ttbar_eff[iwhich][1] / ttbar_nevents[iwhich][1]); 
      h3_den->Scale(ttbar_xs[iwhich] * ttbar_eff[iwhich][2] / ttbar_nevents[iwhich][2]); 
      h1_den->Add(h2_den);
      h1_den->Add(h3_den);
      
      normPDF = h1_num->GetSum()/h1_den->GetSum();
      //cout << "additional sample normalization for " << which << " = " << normPDF << endl;
    }
    */

    h1->Sumw2();
    h2->Sumw2();
    h3->Sumw2();
    h1->Scale(ttbar_xs[iwhich] * ttbar_eff[iwhich][0] * normPDF / ttbar_nevents[iwhich][0]); 
    h2->Scale(ttbar_xs[iwhich] * ttbar_eff[iwhich][1] * normPDF / ttbar_nevents[iwhich][1]); 
    h3->Scale(ttbar_xs[iwhich] * ttbar_eff[iwhich][2] * normPDF / ttbar_nevents[iwhich][2]); 
    h1->Add(h2);
    h1->Add(h3);
    
    h11->Sumw2();
    h22->Sumw2();
    h33->Sumw2();
    h11->Scale(ttbar_xs[iwhich] * ttbar_eff[iwhich][0] * normPDF / ttbar_nevents[iwhich][0]); 
    h22->Scale(ttbar_xs[iwhich] * ttbar_eff[iwhich][1] * normPDF / ttbar_nevents[iwhich][1]); 
    h33->Scale(ttbar_xs[iwhich] * ttbar_eff[iwhich][2] * normPDF / ttbar_nevents[iwhich][2]); 
    h11->Add(h22);
    h11->Add(h33);
  }
  
  TString level = "particle";
  if (parton) level = "parton";
  TString lepton = "muon";
  if (doel) lepton = "electron";
  
  
  float total_xsec = ttbar_xs[iwhich];

  cout << "Inclusive cross section at " << level << " level for " << which << " = " << total_xsec*h11->GetSum()/h1->GetSum() << " pb (" << lepton << ")" << endl;  

}

