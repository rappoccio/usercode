{

  gSystem->CompileMacro("BinomialEff.cc", "k");
  gSystem->CompileMacro("PredictedDistribution.cc", "k");

  TFile * forlibs = new TFile("ca_pat_slim_220.root");
  gSystem->CompileMacro("xcheck_mistag_rate_fwlite.C", "k");
  gSystem->CompileMacro("combine_mistag_predictions.C", "k");


  TFile * f = new TFile("mistag_parameterization_100pb.root");
  TH1D * hist = (TH1D*)f->Get("mistag_rate");

  xcheck_mistag_rate_fwlite(hist, "qcd_230", false, true, 100);
  xcheck_mistag_rate_fwlite(hist, "qcd_300", false, true, 100);
  xcheck_mistag_rate_fwlite(hist, "qcd_380", false, true, 100);
  xcheck_mistag_rate_fwlite(hist, "qcd_470", false, true, 100);
  xcheck_mistag_rate_fwlite(hist, "qcd_600", false, true, 100);
  xcheck_mistag_rate_fwlite(hist, "qcd_800", false, true, 100);
  xcheck_mistag_rate_fwlite(hist, "qcd_1000", false, true, 100);
  xcheck_mistag_rate_fwlite(hist, "qcd_1400", false, true, 100);
  xcheck_mistag_rate_fwlite(hist, "qcd_1800", false, true, 100);
  xcheck_mistag_rate_fwlite(hist, "qcd_2200", false, true, 100);
  xcheck_mistag_rate_fwlite(hist, "qcd_2600", false, true, 100);
  xcheck_mistag_rate_fwlite(hist, "qcd_3000", false, true, 100);
  xcheck_mistag_rate_fwlite(hist, "qcd_3500", false, true, 100);
 

  combine_mistag_predictions();
}
