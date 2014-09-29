{

  TFile * forlibs = new TFile("ca_pat_slim_220.root");
  gSystem->CompileMacro("make_mistag_rate_fwlite.C", "k");
  gSystem->CompileMacro("combine_mistag_rates.C", "k");

  bool processAll = true;

  if ( processAll ) {
    ofstream output1("mistag_rate_output.txt");
  } else {
    ofstream output2("mistag_rate_output_odd.txt");
  }

  make_mistag_rate_fwlite("qcd_230", processAll);
  make_mistag_rate_fwlite("qcd_300", processAll);
  make_mistag_rate_fwlite("qcd_380", processAll);
  make_mistag_rate_fwlite("qcd_470", processAll);
  make_mistag_rate_fwlite("qcd_600", processAll);
  make_mistag_rate_fwlite("qcd_800", processAll);
  make_mistag_rate_fwlite("qcd_1000", processAll);
  make_mistag_rate_fwlite("qcd_1400", processAll);
  make_mistag_rate_fwlite("qcd_1800", processAll);
  make_mistag_rate_fwlite("qcd_2200", processAll);
  make_mistag_rate_fwlite("qcd_2600", processAll);
  make_mistag_rate_fwlite("qcd_3000", processAll);
  make_mistag_rate_fwlite("qcd_3500", processAll);

  combine_mistag_rates(processAll);

}
