{

  const char * files[] = {
    "kinematic_histos_rs_1250_fastsim.root",
    "kinematic_histos_rs_1250_fastsim_heavyfrag_up.root",
    "kinematic_histos_rs_1250_fastsim_heavyfrag_down.root",
    "kinematic_histos_rs_1250_fastsim_isrfsr_down.root",
    "kinematic_histos_rs_1250_fastsim_isrfsr_up.root",
    "kinematic_histos_rs_1250_fastsim_lightfrag_down.root",
    "kinematic_histos_rs_1250_fastsim_lightfrag_up.root",
    "kinematic_histos_rs_1250_fastsim_renorm_down.root",
    "kinematic_histos_rs_1250_fastsim_renorm_up.root"
  };


  const int NFILES = sizeof(files)/sizeof(const char *);

  for (int i = 0; i < NFILES; ++i ) {
    cout << "Processing i = " << i << ",  file = " << files[i] << endl;
    TFile * f = new TFile(files[i]);
    TH1D * h1 = (TH1D*)f->Get("hist_tagged_top_jetEt");
    TH1D * h2 = (TH1D*)f->Get("hist_top_jetEt");

    double num = h1->GetEntries();
    double den = h2->GetEntries();

    double eff = num / den;
    double deff = sqrt(eff*(1-eff)/den);

    cout << files[i] << " = " << eff << " +- " << deff << endl;

  }

}
