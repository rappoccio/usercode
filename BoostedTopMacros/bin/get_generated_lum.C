{

  const char * names[] = {
    "qcd_230", 
    "qcd_300", 
    "qcd_380", 
    "qcd_470", 
    "qcd_600", 
    "qcd_800", 
    "qcd_1000",
    "qcd_1400",
    "qcd_1800",
    "qcd_2200",
    "qcd_2600",
    "qcd_3000",
    "qcd_3500"
  };

  double weights[] = {
    10623.2,
    2634.94,
    722.099,
    240.983,
    62.4923,
    9.42062,
    2.34357,
    0.1568550,
    0.013811,
    0.00129608,
    0.00011404,
    0.0000084318,
    0.00000018146,
  };


  int nevents[] = {
    54000,
    54000,
    51840,
    27648,
    28620,
    20880,
    24640,
    27744,
    22848,
    22560,
    22800,
    20880,
    34320,
  };

  const int N = sizeof(nevents) / sizeof(int);

  cout << "Effective luminosity: " << endl;
  for (int i = 0; i < N; ++i ) {
    char buff[1000];
    sprintf(buff, "%10s : xs = %10.2e pb, gen events = %6i, Lum = %20.2f", names[i], weights[i], nevents[i], nevents[i] / weights[i] );
    cout << buff << endl;
  }


}
