{

  gSystem->CompileMacro("BinomialEff.cc", "k");
  gSystem->CompileMacro("PredictedDistribution.cc", "k");

  TFile * forlibs = new TFile("ca_pat_slim_220.root");
  gSystem->CompileMacro("xcheck_mistag_rate_fwlite.C", "k");
  gSystem->CompileMacro("combine_mistag_predictions.C", "k");


  TFile * f = new TFile("mistag_parameterization.root");
  TH1D * hist = (TH1D*)f->Get("mistag_rate");

  xcheck_mistag_rate_fwlite(hist, "zjets", true, 1);
 
}
