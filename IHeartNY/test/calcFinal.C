
void calcFinal() {

  float particle_nom[3] = {1.42312, 1.40652, 1.41482};
  float parton_nom[3]   = {1.58565, 1.57645, 1.58105};

  float data[3] = {0.65, 0.82, 0.88};
  float err_data[3] = {0.09, 0.09, 0.06};

  float particle_pdfup[3] = {1.4808, 1.46017, 1.47049};
  float parton_pdfup[3]   = {1.61083, 1.59747, 1.60415};
  float particle_pdfdown[3] = {1.39423, 1.38017, 1.38720};
  float parton_pdfdown[3]   = {1.56987, 1.56319, 1.56653};
  float particle_scaleup[3] = {1.53471, 1.50954, 1.52212};
  float parton_scaleup[3]   = {1.73895, 1.71178, 1.72537};
  float particle_scaledown[3] = {1.35697, 1.29876, 1.32787};
  float parton_scaledown[3]   = {1.40849, 1.39677, 1.40263};

  float particle_MG[3] = {1.42186, 1.39482, 1.40834};
  float parton_MG[3]   = {1.73534, 1.72472, 1.73003};

  float data_MG[3] = {0.64, 0.84, 0.87};
  float err_data_MG[3] = {0.09, 0.09, 0.06};

  float lumi = 0.026;

  std::cout.precision(3);

  for (int i=0; i<3; i++) {
    if (i==0) cout << "muon, particle level" << endl;
    if (i==1) cout << "electron, particle level" << endl;
    if (i==2) cout << "combined, particle level" << endl;
    cout << particle_nom[i]*data[i] << " +/- " << err_data[i]*particle_nom[i] << " (stat) "
	 << "+" << (particle_pdfup[i]-particle_nom[i])*data[i] << "" 
	 << "/-" << (particle_nom[i]-particle_pdfdown[i])*data[i] << " (PDF) " 
	 << " +/- " << ((particle_pdfup[i]-particle_nom[i])*data[i] + (particle_nom[i]-particle_pdfdown[i])*data[i])/2 << " (av. PDF) " 
	 << "+" << (particle_scaleup[i]-particle_nom[i])*data[i] << "" 
	 << "/-" << (particle_nom[i]-particle_scaledown[i])*data[i] << " (Q2) " 
	 << " +/- " << ((particle_scaleup[i]-particle_nom[i])*data[i] + (particle_nom[i]-particle_scaledown[i])*data[i])/2 << " (av. Q2) " 
	 << "+/- " << particle_nom[i]*data[i]*lumi << " (lumi) "
	 << endl;

    if (i==0) cout << "muon, parton level" << endl;
    if (i==1) cout << "electron, parton level" << endl;
    if (i==2) cout << "combined, parton level" << endl;
    cout << parton_nom[i]*data[i] << " +/- " << err_data[i]*parton_nom[i] << " (stat) "
	 << "+" << (parton_pdfup[i]-parton_nom[i])*data[i] << "" 
	 << "/-" << (parton_nom[i]-parton_pdfdown[i])*data[i] << " (PDF) " 
	 << " +/- " << ((parton_pdfup[i]-parton_nom[i])*data[i] + (parton_nom[i]-parton_pdfdown[i])*data[i])/2 << " (av. PDF) " 
	 << "+" << (parton_scaleup[i]-parton_nom[i])*data[i] << "" 
	 << "/-" << (parton_nom[i]-parton_scaledown[i])*data[i] << " (Q2) " 
	 << " +/- " << ((parton_scaleup[i]-parton_nom[i])*data[i] + (parton_nom[i]-parton_scaledown[i])*data[i])/2 << " (av. Q2) " 
	 << "+/- " << parton_nom[i]*data[i]*lumi << " (lumi) "
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

}
