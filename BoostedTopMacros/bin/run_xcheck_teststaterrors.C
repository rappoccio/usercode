{

  gSystem->CompileMacro("BinomialEff.cc", "k");
  gSystem->CompileMacro("PredictedDistribution.cc", "k");

  TFile * forlibs = new TFile("ca_pat_slim_220.root");
  gSystem->CompileMacro("xcheck_mistag_rate_fwlite_noweight.C", "k");
 


  TFile * f = new TFile("mistag_parameterization_qcd_800.root");
  TH1D * num = (TH1D*)f->Get("numerator");
  TH1D * den = (TH1D*)f->Get("denominator");

  TH1D * hist = new TH1D(*num);
  hist->SetName("mistag_rate");
  hist->Divide( num, den, 1.0, 1.0, "b");

//   xcheck_mistag_rate_fwlite(hist, "qcd_230");
//   xcheck_mistag_rate_fwlite(hist, "qcd_300");
//   xcheck_mistag_rate_fwlite(hist, "qcd_380");
//   xcheck_mistag_rate_fwlite(hist, "qcd_470");
//   xcheck_mistag_rate_fwlite(hist, "qcd_600");
  xcheck_mistag_rate_fwlite(hist, "qcd_800");
//   xcheck_mistag_rate_fwlite(hist, "qcd_1000");
//   xcheck_mistag_rate_fwlite(hist, "qcd_1400");
//   xcheck_mistag_rate_fwlite(hist, "qcd_1800");
//   xcheck_mistag_rate_fwlite(hist, "qcd_2200");
//   xcheck_mistag_rate_fwlite(hist, "qcd_2600");
//   xcheck_mistag_rate_fwlite(hist, "qcd_3000");
//   xcheck_mistag_rate_fwlite(hist, "qcd_3500");
 
}
