{

  TFile * forlibs = new TFile("ca_pat_slim_220.root");
  gSystem->CompileMacro("make_mistag_rate_fwlite_noweight.C", "k");

//   make_mistag_rate_fwlite("qcd_230");
//   make_mistag_rate_fwlite("qcd_300");
//   make_mistag_rate_fwlite("qcd_380");
//   make_mistag_rate_fwlite("qcd_470");
//   make_mistag_rate_fwlite("qcd_600");
  make_mistag_rate_fwlite("qcd_800");
//   make_mistag_rate_fwlite("qcd_1000");
//   make_mistag_rate_fwlite("qcd_1400");
//   make_mistag_rate_fwlite("qcd_1800");
//   make_mistag_rate_fwlite("qcd_2200");
//   make_mistag_rate_fwlite("qcd_2600");
//   make_mistag_rate_fwlite("qcd_3000");
//   make_mistag_rate_fwlite("qcd_3500");


}
