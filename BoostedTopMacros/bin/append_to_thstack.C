#include "THStack.h"
#include "TH1.h"
#include "TLegend.h"
#include <iostream>

using namespace std;

THStack * append_to_thstack( THStack * stack, TH1 * h, TLegend * leg, const char * desc, double weight, int color )
{

  cout << "Scaling to weight " << weight;
  h->Scale( weight );
  cout << "Setting color " << color << endl;
  h->SetFillColor( color );

  cout << "Adding to stack" << endl;
  stack->Add( h );

  cout << "Adding to legend" << endl;
  leg->AddEntry( h, desc, "f");

  cout << "returning" << endl;
  return stack;
}
