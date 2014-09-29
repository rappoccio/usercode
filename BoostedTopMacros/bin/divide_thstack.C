#include "THStack.h"
#include "TList.h"

TH1D * divide_thstack( THStack * h1, THStack * h2, const char * name, const char * title )
{

  TList * l1 = h1->GetHists();
  TList * l2 = h2->GetHists();

  TH1 * num = (TH1*)l1->Last();
  TH1 * den = (TH1*)l2->Last();

//   num->Sumw2();
//   den->Sumw2();

  TH1D * frac = (TH1D*)num->Clone();
  frac->SetName(name);
  frac->SetTitle(title);


  frac->Divide( den );

  return frac;
}
