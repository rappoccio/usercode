{

  gSystem->CompileMacro("BinomialEff.cc", "k");
  gSystem->CompileMacro("PredictedDistribution.cc", "k");

  TFile * forlibs = new TFile("ca_pat_slim_220.root");
  gSystem->CompileMacro("dijet_analysis_mistag_prediction_fwlite.C", "k");
  gSystem->CompileMacro("combine_mistag_background.C", "k");


  TFile * f = new TFile("mistag_parameterization_100pb.root");
  TH1D * hist = (TH1D*)f->Get("mistag_rate");

  dijet_analysis_mistag_prediction_fwlite(hist, "qcd_230", true, false, 100);
  dijet_analysis_mistag_prediction_fwlite(hist, "qcd_300", true, false, 100);
  dijet_analysis_mistag_prediction_fwlite(hist, "qcd_380", true, false, 100);
  dijet_analysis_mistag_prediction_fwlite(hist, "qcd_470", true, true, 100);
  dijet_analysis_mistag_prediction_fwlite(hist, "qcd_600", true, true, 100);
  dijet_analysis_mistag_prediction_fwlite(hist, "qcd_800", true, true, 100);
  dijet_analysis_mistag_prediction_fwlite(hist, "qcd_1000", true, true, 100);
  dijet_analysis_mistag_prediction_fwlite(hist, "qcd_1400", true, true, 100);
  dijet_analysis_mistag_prediction_fwlite(hist, "qcd_1800", true, true, 100);
  dijet_analysis_mistag_prediction_fwlite(hist, "qcd_2200", true, true, 100);
  dijet_analysis_mistag_prediction_fwlite(hist, "qcd_2600", true, true, 100);
  dijet_analysis_mistag_prediction_fwlite(hist, "qcd_3000", true, true, 100);
  dijet_analysis_mistag_prediction_fwlite(hist, "qcd_3500", true, true, 100);
 

  combine_mistag_background();
}
