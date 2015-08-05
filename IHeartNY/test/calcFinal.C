
void calcFinal() {

  float particle_nom[3] = {1.46056, 1.44206, 0.};
  float parton_nom[3]   = {1.62736, 1.61629, 0.};
  particle_nom[2] = (particle_nom[0]+particle_nom[1])/2.;
  parton_nom[2] = (parton_nom[0]+parton_nom[1])/2.;

  float particle_pdfup[3] = {1.60231, 1.57759, 0.};
  float parton_pdfup[3]   = {1.79039, 1.77282, 0.};
  particle_pdfup[2] = (particle_pdfup[0]+particle_pdfup[1])/2.;
  parton_pdfup[2] = (parton_pdfup[0]+parton_pdfup[1])/2.;
  float particle_pdfdown[3] = {1.36372, 1.34908, 0.};
  float parton_pdfdown[3]   = {1.50358, 1.49607, 0.};
  particle_pdfdown[2] = (particle_pdfdown[0]+particle_pdfdown[1])/2.;
  parton_pdfdown[2] = (parton_pdfdown[0]+parton_pdfdown[1])/2.;
  float particle_scaleup[3] = {1.55751, 1.53262, 0.};
  float parton_scaleup[3]   = {1.76479, 1.73796, 0.};
  particle_scaleup[2] = (particle_scaleup[0]+particle_scaleup[1])/2.;
  parton_scaleup[2] = (parton_scaleup[0]+parton_scaleup[1])/2.;
  float particle_scaledown[3] = {1.3693, 1.31044, 0.};
  float parton_scaledown[3]   = {1.4213, 1.40934, 0.};
  particle_scaledown[2] = (particle_scaledown[0]+particle_scaledown[1])/2.;
  parton_scaledown[2] = (parton_scaledown[0]+parton_scaledown[1])/2.;

  float particle_MG[3] = {1.35881, 1.33966, 0.};
  float parton_MG[3]   = {1.65839, 1.65651, 0.};
  particle_MG[2] = (particle_MG[0]+particle_MG[1])/2.;
  parton_MG[2] = (parton_MG[0]+parton_MG[1])/2.;

  // beta_signal's from theta fit
  float data[3] = {0.65, 0.82, 0.88};
  float err_data[3] = {0.09, 0.09, 0.06};
  float data_MG[3] = {0.64, 0.84, 0.87};
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
