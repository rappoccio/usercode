
void calcOne(TString which, bool parton, bool doel);

void calcXS() {
  
  calcOne("CT10_nom",false,false);
  calcOne("CT10_nom",false,true);
  calcOne("CT10_nom",true,false);
  calcOne("CT10_nom",true,true);

  calcOne("CT10_pdfup",false,false);
  calcOne("CT10_pdfup",false,true);
  calcOne("CT10_pdfup",true,false);
  calcOne("CT10_pdfup",true,true);

  calcOne("CT10_pdfdown",false,false);
  calcOne("CT10_pdfdown",false,true);
  calcOne("CT10_pdfdown",true,false);
  calcOne("CT10_pdfdown",true,true);

  calcOne("scaleup",false,false);
  calcOne("scaleup",false,true);
  calcOne("scaleup",true,false);
  calcOne("scaleup",true,true);

  calcOne("scaledown",false,false);
  calcOne("scaledown",false,true);
  calcOne("scaledown",true,false);
  calcOne("scaledown",true,true);

  calcOne("MG",false,false);
  calcOne("MG",false,true);
  calcOne("MG",true,false);
  calcOne("MG",true,true);

}

void calcOne(TString which, bool parton, bool doel) {

  if (which=="MG") {  
    if (doel) TFile* f1 = new TFile("histfiles_MG/TTJets_SemiLeptMGDecays_8TeV-madgraph_iheartNY_V1_el_2Dcut_nom.root");
    else TFile* f1 = new TFile("histfiles_MG/TTJets_SemiLeptMGDecays_8TeV-madgraph_iheartNY_V1_mu_2Dcut_nom.root");
  }
  else if (doel) {
    TFile* f1 = new TFile("histfiles_"+which+"/qcd_el/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_"+which+"_2Dcut_nom.root");
    TFile* f2 = new TFile("histfiles_"+which+"/qcd_el/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_"+which+"_2Dcut_nom.root");
    TFile* f3 = new TFile("histfiles_"+which+"/qcd_el/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_"+which+"_2Dcut_nom.root");
    // additional normalization
    TFile* fn1 = new TFile("histfiles_CT10_nom/qcd_el/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_CT10_nom_2Dcut_nom.root");
    TFile* fn2 = new TFile("histfiles_CT10_nom/qcd_el/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_CT10_nom_2Dcut_nom.root");
    TFile* fn3 = new TFile("histfiles_CT10_nom/qcd_el/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_CT10_nom_2Dcut_nom.root");
  }
  else {
    TFile* f1 = new TFile("histfiles_"+which+"/2Dhists/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+which+"_2Dcut_nom.root");
    TFile* f2 = new TFile("histfiles_"+which+"/2Dhists/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+which+"_2Dcut_nom.root");
    TFile* f3 = new TFile("histfiles_"+which+"/2Dhists/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+which+"_2Dcut_nom.root");
    // additional normalization
    TFile* fn1 = new TFile("histfiles_CT10_nom/2Dhists/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_2Dcut_nom.root");
    TFile* fn2 = new TFile("histfiles_CT10_nom/2Dhists/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_2Dcut_nom.root");
    TFile* fn3 = new TFile("histfiles_CT10_nom/2Dhists/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_2Dcut_nom.root");
  }

  TString what = "ptGenTop_passParton";
  if (!parton) what = "ptPartTop_passParticle";

  if (which=="MG") {
    TH1F* h1 = (TH1F*) f1->Get(what);
  }
  else {
    TH1F* h1 = (TH1F*) f1->Get(what);
    TH1F* h2 = (TH1F*) f2->Get(what);
    TH1F* h3 = (TH1F*) f3->Get(what);
  }

  float norm1 = 1.0;
  float norm2 = 1.0;
  float norm3 = 1.0;

  if (which=="CT10_pdfup" || which=="CT10_pdfdown") {
    TH1F* h1_den = (TH1F*) f1->Get("mttbarGen0");
    TH1F* h2_den = (TH1F*) f2->Get("mttbarGen0");
    TH1F* h3_den = (TH1F*) f3->Get("mttbarGen0");
    TH1F* h1_num = (TH1F*) fn1->Get("mttbarGen0");
    TH1F* h2_num = (TH1F*) fn2->Get("mttbarGen0");
    TH1F* h3_num = (TH1F*) fn3->Get("mttbarGen0");

    norm1 = h1_num->GetSum()/h1_den->GetSum();
    norm2 = h2_num->GetSum()/h2_den->GetSum();
    norm3 = h3_num->GetSum()/h3_den->GetSum();

    cout << "additional sample normalizations for " << which << " = " << norm1 << " (m<700), " << norm2 << " (700<m<1000), " << norm3 << " (m>1000), " << endl;
  }

  int iwhich = 0;
  if (which=="CT10_pdfup") iwhich = 1;
  else if (which=="CT10_pdfdown") iwhich = 2;
  else if (which=="scaleup") iwhich = 3;
  else if (which=="scaledown") iwhich = 4;

  double ttbar_xs[5] = {
    245.8,  // nominal
    245.8,  // CT10 up
    245.8,  // CT10 down
    252.0,  // q2 up
    237.4   // q2 down
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
    double ttbar_norm = 245.8/25424818.*4./9.;
    h1->Scale(ttbar_norm);
  }
  else {
    h1->Sumw2();
    h2->Sumw2();
    h3->Sumw2();
    
    h1->Scale(ttbar_xs[iwhich] * ttbar_eff[iwhich][0] * norm1 / ttbar_nevents[iwhich][0]); 
    h2->Scale(ttbar_xs[iwhich] * ttbar_eff[iwhich][1] * norm2 / ttbar_nevents[iwhich][1]); 
    h3->Scale(ttbar_xs[iwhich] * ttbar_eff[iwhich][2] * norm3 / ttbar_nevents[iwhich][2]); 
    
    h1->Add(h2);
    h1->Add(h3);
  }

  TString level = "particle";
  if (parton) level = "parton";
  TString lepton = "muon";
  if (doel) lepton = "electron";

  cout << endl;
  cout << "Inclusive cross section at " << level << " level for " << which << " = " << h1->GetSum()*27/4 << " pb (" << lepton << ")" << endl;
  cout << endl;
  

}

