
void calcFinal() {

  float particle_nom[3] = {1.50269, 1.48366, 0.};
  float parton_nom[3]   = {1.6743, 1.66291, 0.};
  particle_nom[2] = (particle_nom[0]+particle_nom[1])/2.;
  parton_nom[2] = (parton_nom[0]+parton_nom[1])/2.;

  float particle_pdfup[3] = {1.64853, 1.6231, 0.};
  float parton_pdfup[3]   = {1.84204, 1.82396, 0.};
  particle_pdfup[2] = (particle_pdfup[0]+particle_pdfup[1])/2.;
  parton_pdfup[2] = (parton_pdfup[0]+parton_pdfup[1])/2.;
  float particle_pdfdown[3] = {1.40305, 1.38799, 0.};
  float parton_pdfdown[3]   = {1.54695, 1.53923, 0.};
  particle_pdfdown[2] = (particle_pdfdown[0]+particle_pdfdown[1])/2.;
  parton_pdfdown[2] = (parton_pdfdown[0]+parton_pdfdown[1])/2.;
  float particle_scaleup[3] = {1.60251, 1.5769, 0.};
  float parton_scaleup[3]   = {1.81578, 1.78817, 0.};
  particle_scaleup[2] = (particle_scaleup[0]+particle_scaleup[1])/2.;
  parton_scaleup[2] = (parton_scaleup[0]+parton_scaleup[1])/2.;
  float particle_scaledown[3] = {1.40881, 1.34825, 0.};
  float parton_scaledown[3]   = {1.46231, 1.45, 0.};
  particle_scaledown[2] = (particle_scaledown[0]+particle_scaledown[1])/2.;
  parton_scaledown[2] = (parton_scaledown[0]+parton_scaledown[1])/2.;

  float particle_MG[3] = {1.513, 1.49167, 0.};
  float parton_MG[3]   = {1.84656, 1.84447, 0.};
  particle_MG[2] = (particle_MG[0]+particle_MG[1])/2.;
  parton_MG[2] = (parton_MG[0]+parton_MG[1])/2.;

  // beta_signal's from theta fit
  float data[3] = {0.63, 0.80, 0.86};
  float err_data[3] = {0.09, 0.09, 0.06};
  //  float data_MG[3] = {0.64, 0.84, 0.87};
  float data_MG[3] = {0.62, 0.82, 0.85};  /// temporary hack -- need to fix if showing MadGraph in public (rerun theta with updated top xs)
  float err_data_MG[3] = {0.09, 0.09, 0.06};

  // additional luminosity uncertainty
  float lumi = 0.026;

  std::cout.precision(4);

  cout << endl << "*** MC cross sections***" << endl << endl;
  cout << "CT10 nominal & " << parton_nom[2] << " & " << particle_nom[0] << " & " << particle_nom[1] << " & " << particle_nom[2] << " \\\\" << endl;
  cout << "PDF up & " << parton_pdfup[2] << " & " << particle_pdfup[0] << " & " << particle_pdfup[1] << " & " << particle_pdfup[2] << " \\\\" << endl;
  cout << "PDF down & " << parton_pdfdown[2] << " & " << particle_pdfdown[0] << " & " << particle_pdfdown[1] << " & " << particle_pdfdown[2] << " \\\\" << endl;
  cout << "$Q^2$ up & " << parton_scaleup[2] << " & " << particle_scaleup[0] << " & " << particle_scaleup[1] << " & " << particle_scaleup[2] << " \\\\" << endl;
  cout << "$Q^2$ down & " << parton_scaledown[2] << " & " << particle_scaledown[0] << " & " << particle_scaledown[1] << " & " << particle_scaledown[2] << " \\\\" << endl;
  cout << "MadGraph & " << parton_MG[2] << " & " << particle_MG[0] << " & " << particle_MG[1] << " & " << particle_MG[2] << " \\\\" << endl;
  cout << endl;

  std::cout.precision(3);

  cout << endl << "*** POWHEG ***" << endl<< endl;

  for (int i=0; i<3; i++) {

    if (i==0) cout << "muon, particle level" << endl;
    if (i==1) cout << "electron, particle level" << endl;
    if (i==2) cout << "combined, particle level" << endl;

    float stat = err_data[i]*particle_nom[i];
    float pdf = ((particle_pdfup[i]-particle_nom[i])*data[i] + (particle_nom[i]-particle_pdfdown[i])*data[i])/2;
    float q2 = ((particle_scaleup[i]-particle_nom[i])*data[i] + (particle_nom[i]-particle_scaledown[i])*data[i])/2;
    float lum = particle_nom[i]*data[i]*lumi;

    cout << particle_nom[i]*data[i] << " +/- " << stat << " (stat) "
      // << "+" << (particle_pdfup[i]-particle_nom[i])*data[i] << "" 
      // << "/-" << (particle_nom[i]-particle_pdfdown[i])*data[i] << " (PDF) " 
	 << " +/- " << pdf << " (av. PDF) " 
      // << "+" << (particle_scaleup[i]-particle_nom[i])*data[i] << "" 
      // << "/-" << (particle_nom[i]-particle_scaledown[i])*data[i] << " (Q2) " 
	 << " +/- " << q2 << " (av. Q2) " 
	 << "+/- " << lum << " (lumi) "
	 << " TOTAL uncertainty = " << sqrt(stat*stat + pdf*pdf + q2*q2 + lum*lum) 
	 << endl;

    if (i==0) cout << "muon, parton level" << endl;
    if (i==1) cout << "electron, parton level" << endl;
    if (i==2) cout << "combined, parton level" << endl;

    stat = err_data[i]*parton_nom[i];
    pdf = ((parton_pdfup[i]-parton_nom[i])*data[i] + (parton_nom[i]-parton_pdfdown[i])*data[i])/2;
    q2 = ((parton_scaleup[i]-parton_nom[i])*data[i] + (parton_nom[i]-parton_scaledown[i])*data[i])/2;
    lum = parton_nom[i]*data[i]*lumi;

    cout << parton_nom[i]*data[i] << " +/- " << stat << " (stat) "
      // << "+" << (parton_pdfup[i]-parton_nom[i])*data[i] << "" 
      // << "/-" << (parton_nom[i]-parton_pdfdown[i])*data[i] << " (PDF) " 
	 << " +/- " << pdf << " (av. PDF) " 
      // << "+" << (parton_scaleup[i]-parton_nom[i])*data[i] << "" 
      // << "/-" << (parton_nom[i]-parton_scaledown[i])*data[i] << " (Q2) " 
	 << " +/- " << q2 << " (av. Q2) " 
	 << "+/- " << lum << " (lumi) "
	 << " TOTAL uncertainty = " << sqrt(stat*stat + pdf*pdf + q2*q2 + lum*lum) 
	 << endl;
  }

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

}
