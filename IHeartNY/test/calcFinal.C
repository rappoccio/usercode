
void calcFinal() {

  //float particle_nom[3] = {1.50269, 1.48366, 0.}; //this is w/o particle-level jet mass cut
  float particle_nom[3] = {0.583181, 0.576421, 0.}; //muon, electron, combined
  float parton_nom[3]   = {1.6743, 1.66291, 0.};
  particle_nom[2] = (particle_nom[0]+particle_nom[1])/2.;
  parton_nom[2] = (parton_nom[0]+parton_nom[1])/2.;

  //float particle_pdfup[3] = {1.64853, 1.6231, 0.};
  float particle_pdfup[3] = {0.643195, 0.636619, 0.};
  float parton_pdfup[3]   = {1.84204, 1.82396, 0.};
  particle_pdfup[2] = (particle_pdfup[0]+particle_pdfup[1])/2.;
  parton_pdfup[2] = (parton_pdfup[0]+parton_pdfup[1])/2.;
  //float particle_pdfdown[3] = {1.40305, 1.38799, 0.};
  float particle_pdfdown[3] = {0.536549, 0.530177, 0.};
  float parton_pdfdown[3]   = {1.54695, 1.53923, 0.};
  particle_pdfdown[2] = (particle_pdfdown[0]+particle_pdfdown[1])/2.;
  parton_pdfdown[2] = (parton_pdfdown[0]+parton_pdfdown[1])/2.;

  // MSTW
  float particle_mstw_nom[3] = {0.577921, 0.571326, 0.};
  float parton_mstw_nom[3]   = {1.6581, 1.64622, 0.};
  particle_mstw_nom[2] = (particle_mstw_nom[0]+particle_mstw_nom[1])/2.;
  parton_mstw_nom[2] = (parton_mstw_nom[0]+parton_mstw_nom[1])/2.;
  float particle_mstw_pdfup[3] = {0.597294, 0.591382, 0.};
  float parton_mstw_pdfup[3]   = {1.71095, 1.69555, 0.};
  particle_mstw_pdfup[2] = (particle_mstw_pdfup[0]+particle_mstw_pdfup[1])/2.;
  parton_mstw_pdfup[2] = (parton_mstw_pdfup[0]+parton_mstw_pdfup[1])/2.;
  float particle_mstw_pdfdown[3] = {0.540877, 0.5337, 0.};
  float parton_mstw_pdfdown[3]   = {1.55217, 1.54231, 0.};
  particle_mstw_pdfdown[2] = (particle_mstw_pdfdown[0]+particle_mstw_pdfdown[1])/2.;
  parton_mstw_pdfdown[2] = (parton_mstw_pdfdown[0]+parton_mstw_pdfdown[1])/2.;

  // NNPDF
  float particle_nnpdf_nom[3] = {0.542714, 0.535482, 0.};
  float parton_nnpdf_nom[3]   = {1.55884, 1.55028, 0.};
  particle_nnpdf_nom[2] = (particle_nnpdf_nom[0]+particle_nnpdf_nom[1])/2.;
  parton_nnpdf_nom[2] = (parton_nnpdf_nom[0]+parton_nnpdf_nom[1])/2.;
  float particle_nnpdf_pdfup[3] = {0.610029, 0.605052, 0.};
  float parton_nnpdf_pdfup[3]   = {1.75021, 1.73307, 0.};
  particle_nnpdf_pdfup[2] = (particle_nnpdf_pdfup[0]+particle_nnpdf_pdfup[1])/2.;
  parton_nnpdf_pdfup[2] = (parton_nnpdf_pdfup[0]+parton_nnpdf_pdfup[1])/2.;
  float particle_nnpdf_pdfdown[3] = {0.546872, 0.538056, 0.};
  float parton_nnpdf_pdfdown[3]   = {1.57099, 1.56756, 0.};
  particle_nnpdf_pdfdown[2] = (particle_nnpdf_pdfdown[0]+particle_nnpdf_pdfdown[1])/2.;
  parton_nnpdf_pdfdown[2] = (parton_nnpdf_pdfdown[0]+parton_nnpdf_pdfdown[1])/2.;

  //float particle_scaleup[3] = {1.60251, 1.5769, 0.};
  float particle_scaleup[3] = {0.620764, 0.610568, 0.};
  float parton_scaleup[3]   = {1.81578, 1.78817, 0.};
  particle_scaleup[2] = (particle_scaleup[0]+particle_scaleup[1])/2.;
  parton_scaleup[2] = (parton_scaleup[0]+parton_scaleup[1])/2.;
  //float particle_scaledown[3] = {1.40881, 1.34825, 0.};
  float particle_scaledown[3] = {0.512045, 0.50752, 0.};
  float parton_scaledown[3]   = {1.46231, 1.45, 0.};
  particle_scaledown[2] = (particle_scaledown[0]+particle_scaledown[1])/2.;
  parton_scaledown[2] = (parton_scaledown[0]+parton_scaledown[1])/2.;

  //float particle_MG[3] = {1.513, 1.49167, 0.};
  float particle_MG[3] = {0.679058, 0.670627, 0.};
  float parton_MG[3]   = {1.84656, 1.84447, 0.};
  particle_MG[2] = (particle_MG[0]+particle_MG[1])/2.;
  parton_MG[2] = (parton_MG[0]+parton_MG[1])/2.;

  /*
  // these are without using MC@NLO weights!!
  //float particle_mcnlo[3] = {1.19522, 1.18857, 0.};
  float particle_mcnlo[3] = {0.516523, 0.502574, 0.};
  float parton_mcnlo[3]   = {1.39571, 1.4023, 0.};
  */
  // WITH MC@NLO weights!
  float particle_mcnlo[3] = {0.506931, 0.490746, 0.};
  float parton_mcnlo[3]   = {1.41826, 1.41346, 0.};
  
  particle_mcnlo[2] = (particle_mcnlo[0]+particle_mcnlo[1])/2.;
  parton_mcnlo[2] = (parton_mcnlo[0]+parton_mcnlo[1])/2.;

  // beta_signal's from theta fit
  float data[3] = {0.63, 0.80, 0.86};
  float err_data[3] = {0.09, 0.09, 0.06};
  //  float data_MG[3] = {0.64, 0.84, 0.87};
  float data_MG[3] = {0.62, 0.82, 0.85};  /// temporary hack -- need to fix if showing MadGraph in public (rerun theta with updated top xs)
  float err_data_MG[3] = {0.09, 0.09, 0.06};

  // additional luminosity uncertainty
  float lumi = 0.026;

  std::cout.precision(4);

  cout << endl << "*** MC cross sections ***" << endl << endl;
  cout << "CT10 nominal & " << parton_nom[2] << " & " << particle_nom[0] << " & " << particle_nom[1] << " & " << particle_nom[2] << " \\\\" << endl;
  cout << "PDF up & " << parton_pdfup[2] << " & " << particle_pdfup[0] << " & " << particle_pdfup[1] << " & " << particle_pdfup[2] << " \\\\" << endl;
  cout << "PDF down & " << parton_pdfdown[2] << " & " << particle_pdfdown[0] << " & " << particle_pdfdown[1] << " & " << particle_pdfdown[2] << " \\\\" << endl;

  cout << "MSTW nominal & " << parton_mstw_nom[2] << " & " << particle_mstw_nom[0] << " & " << particle_mstw_nom[1] << " & " << particle_mstw_nom[2] << " \\\\" << endl;
  cout << "PDF up & " << parton_mstw_pdfup[2] << " & " << particle_mstw_pdfup[0] << " & " << particle_mstw_pdfup[1] << " & " << particle_mstw_pdfup[2] << " \\\\" << endl;
  cout << "PDF down & " << parton_mstw_pdfdown[2] << " & " << particle_mstw_pdfdown[0] << " & " << particle_mstw_pdfdown[1] << " & " << particle_mstw_pdfdown[2] << " \\\\" << endl;

  cout << "NNPDF nominal & " << parton_nnpdf_nom[2] << " & " << particle_nnpdf_nom[0] << " & " << particle_nnpdf_nom[1] << " & " << particle_nnpdf_nom[2] << " \\\\" << endl;
  cout << "PDF up & " << parton_nnpdf_pdfup[2] << " & " << particle_nnpdf_pdfup[0] << " & " << particle_nnpdf_pdfup[1] << " & " << particle_nnpdf_pdfup[2] << " \\\\" << endl;
  cout << "PDF down & " << parton_nnpdf_pdfdown[2] << " & " << particle_nnpdf_pdfdown[0] << " & " << particle_nnpdf_pdfdown[1] << " & " << particle_nnpdf_pdfdown[2] << " \\\\" << endl;

  cout << "$Q^2$ up & " << parton_scaleup[2] << " & " << particle_scaleup[0] << " & " << particle_scaleup[1] << " & " << particle_scaleup[2] << " \\\\" << endl;
  cout << "$Q^2$ down & " << parton_scaledown[2] << " & " << particle_scaledown[0] << " & " << particle_scaledown[1] << " & " << particle_scaledown[2] << " \\\\" << endl;
  cout << "MadGraph & " << parton_MG[2] << " & " << particle_MG[0] << " & " << particle_MG[1] << " & " << particle_MG[2] << " \\\\" << endl;
  cout << "MC@NLO & " << parton_mcnlo[2] << " & " << particle_mcnlo[0] << " & " << particle_mcnlo[1] << " & " << particle_mcnlo[2] << " \\\\" << endl;
  cout << endl;

  std::cout.precision(3);

  cout << endl << "*** POWHEG ***" << endl;

  for (int i=0; i<3; i++) {

    cout << endl;
    if (i==0) cout << "muon, particle level" << endl;
    if (i==1) cout << "electron, particle level" << endl;
    if (i==2) cout << "combined, particle level" << endl;

    float stat = err_data[i]*particle_nom[i];
    
    float pdf_maxup = particle_pdfup[i];
    if (particle_mstw_pdfup[i] > pdf_maxup) pdf_maxup = particle_mstw_pdfup[i];
    if (particle_nnpdf_pdfup[i] > pdf_maxup) pdf_maxup = particle_nnpdf_pdfup[i];
    float pdf_mindn = particle_pdfdown[i]; 
    if (particle_mstw_pdfdown[i] < pdf_mindn) pdf_mindn = particle_mstw_pdfdown[i];
    if (particle_nnpdf_pdfdown[i] < pdf_mindn) pdf_mindn = particle_nnpdf_pdfdown[i];

    float pdf = ((pdf_maxup-particle_nom[i])*data[i] + (particle_nom[i]-pdf_mindn)*data[i])/2;
    float q2 = ((particle_scaleup[i]-particle_nom[i])*data[i] + (particle_nom[i]-particle_scaledown[i])*data[i])/2;
    float ps = fabs(particle_mcnlo[i]-particle_nom[i])*data[i];
    float theory = sqrt(pdf*pdf+q2*q2+ps*ps);
    float lum = particle_nom[i]*data[i]*lumi;

    cout << particle_nom[i]*data[i] << " +/- " << stat << " (stat) "
	 << "+/- " << pdf << " (av. PDF) " 
	 << "+/- " << q2 << " (av. Q2) " 
	 << "+/- " << ps << " (av. PS) " 
	 << "+/- " << lum << " (lumi) "
	 << "+/- " << theory << " (total theory) "
	 << " TOTAL uncertainty = " << sqrt(stat*stat + pdf*pdf + q2*q2 + ps*ps + lum*lum) 
	 << endl;
    cout << "relative uncertainties: " << stat/(particle_nom[i]*data[i]) << " (stat) " << pdf/(particle_nom[i]*data[i]) << " (pdf) " 
	 << q2/(particle_nom[i]*data[i]) << " (Q2) " << ps/(particle_nom[i]*data[i]) << " (PS) " << lum/(particle_nom[i]*data[i]) << " (lumi) " << endl;

    if (i==0) cout << "muon, parton level" << endl;
    if (i==1) cout << "electron, parton level" << endl;
    if (i==2) cout << "combined, parton level" << endl;

    stat = err_data[i]*parton_nom[i];

    pdf_maxup = parton_pdfup[i];
    if (parton_mstw_pdfup[i] > pdf_maxup) pdf_maxup = parton_mstw_pdfup[i];
    if (parton_nnpdf_pdfup[i] > pdf_maxup) pdf_maxup = parton_nnpdf_pdfup[i];
    pdf_mindn = parton_pdfdown[i]; 
    if (parton_mstw_pdfdown[i] < pdf_mindn) pdf_mindn = parton_mstw_pdfdown[i];
    if (parton_nnpdf_pdfdown[i] < pdf_mindn) pdf_mindn = parton_nnpdf_pdfdown[i];

    pdf = ((pdf_maxup-parton_nom[i])*data[i] + (parton_nom[i]-pdf_mindn)*data[i])/2;
    q2 = ((parton_scaleup[i]-parton_nom[i])*data[i] + (parton_nom[i]-parton_scaledown[i])*data[i])/2;
    ps = fabs(parton_mcnlo[i]-parton_nom[i])*data[i];
    theory = sqrt(pdf*pdf+q2*q2+ps*ps);
    lum = parton_nom[i]*data[i]*lumi;

    cout << parton_nom[i]*data[i] << " +/- " << stat << " (stat) "
	 << "+/- " << pdf << " (av. PDF) " 
	 << "+/- " << q2 << " (av. Q2) " 
	 << "+/- " << ps << " (av. PS) " 
	 << "+/- " << lum << " (lumi) "
	 << "+/- " << theory << " (total theory) "
	 << " TOTAL uncertainty = " << sqrt(stat*stat + pdf*pdf + q2*q2 + ps*ps + lum*lum) 
	 << endl;
    cout << "relative uncertainties: " << stat/(parton_nom[i]*data[i]) << " (stat) " << pdf/(parton_nom[i]*data[i]) << " (pdf) " 
	 << q2/(parton_nom[i]*data[i]) << " (Q2) " << ps/(parton_nom[i]*data[i]) << " (PS) " << lum/(parton_nom[i]*data[i]) << " (lumi) " << endl;
  }

  /*
  cout << endl << "*** MADGRAPH ***" << endl<< endl;
  for (int i=0; i<3; i++) {
    if (i==0) cout << "muon, particle level" << endl;
    if (i==1) cout << "electron, particle level" << endl;
    if (i==2) cout << "combined, particle level" << endl;
    cout << particle_MG[i]*data_MG[i] << " +/- " << err_data_MG[i]*particle_MG[i] << " (stat) "
	 << "+/- " << particle_MG[i]*data_MG[i]*lumi << " (lumi) "
	 << endl;

    if (i==0) cout << "muon, parton level" << endl;
    if (i==1) cout << "electron, parton level" << endl;
    if (i==2) cout << "combined, parton level" << endl;
    cout << parton_MG[i]*data_MG[i] << " +/- " << err_data_MG[i]*parton_MG[i] << " (stat) "
	 << "+/- " << parton_MG[i]*data_MG[i]*lumi << " (lumi) "
	 << endl;
  }
  cout << endl;
  */

}
