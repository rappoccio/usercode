{

  TFile * forlibs = new TFile("ca_pat_slim_fastsim_220.root");
  gSystem->CompileMacro("kinematics_fwlite_plots.C", "k");

// //   catop_fwlite("qcd_15");
// //   catop_fwlite("qcd_20");
// //   catop_fwlite("qcd_30");
// //   catop_fwlite("qcd_50");
// //   catop_fwlite("qcd_80");
// //   catop_fwlite("qcd_120");
// //   catop_fwlite("qcd_170");


//   catop_fwlite("ttbar");
//   catop_fwlite("rs_750");
//   catop_fwlite("rs_1000");
//   catop_fwlite("rs_1250");

//   catop_fwlite("rs_750_fastsim" ) ;
//   catop_fwlite("rs_1000_fastsim" ) ;
//   catop_fwlite("rs_1250_fastsim" ) ;
//   catop_fwlite("rs_1500_fastsim" ) ;
//   catop_fwlite("rs_2000_fastsim" ) ;
//   catop_fwlite("rs_2500_fastsim" ) ;
//   catop_fwlite("rs_3000_fastsim" ) ;
//   catop_fwlite("rs_1250_fastsim_heavyfrag_up" ) ;
//   catop_fwlite("rs_1250_fastsim_heavyfrag_down" ) ;
//   catop_fwlite("rs_1250_fastsim_isrfsr_down" ) ;
//   catop_fwlite("rs_1250_fastsim_isrfsr_up" ) ;
//   catop_fwlite("rs_1250_fastsim_lightfrag_down" ) ;
//   catop_fwlite("rs_1250_fastsim_lightfrag_up" ) ;
//   catop_fwlite("rs_1250_fastsim_renorm_down" ) ;
//   catop_fwlite("rs_1250_fastsim_renorm_up" ) ;

//   catop_fwlite("qcd_230");
//   catop_fwlite("qcd_300");
//   catop_fwlite("qcd_380");
//   catop_fwlite("qcd_470");
//   catop_fwlite("qcd_600");
//   catop_fwlite("qcd_800");
//   catop_fwlite("qcd_1000");
//   catop_fwlite("qcd_1400");
//   catop_fwlite("qcd_1800");
//   catop_fwlite("qcd_2200");
//   catop_fwlite("qcd_2600");
//   catop_fwlite("qcd_3000");
//   catop_fwlite("qcd_3500");


  catop_fwlite("zprime_m1000_w10");
  catop_fwlite("zprime_m2000_w20");
  catop_fwlite("zprime_m3000_w30");
  catop_fwlite("zprime_m4000_w40");

  catop_fwlite("zprime_m1000_w100");
  catop_fwlite("zprime_m2000_w200");
  catop_fwlite("zprime_m3000_w300");
  catop_fwlite("zprime_m4000_w400");
}
