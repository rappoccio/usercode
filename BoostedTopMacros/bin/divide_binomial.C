#include <TH1D.h>

TH1D * divide_binomial( TH1D * num, TH1D * den )
{
  num->Sumw2();
  den->Sumw2();

  TH1D * ret = new TH1D(*num);

  for ( int i = 0; i <= num->GetNbinsX(); i++ ) {
    double f1 = num->GetBinContent(i);
    double f2 = den->GetBinContent(i);


    double f = 0.;
    double e = 0.;
    if ( f2 > 0 ) {
      f  = f1 / f2;
      e = sqrt( f * (1-f) / f2 );

      cout << "f1 = " << f1 << ", f2 = " << f2 << ", f = " << f << ", e = " << e << endl;
    } else {
      f = 0.0;
      e = 0.0;
    }

    ret->SetBinContent( i, f );
    ret->SetBinError ( i, e );
  }
}
