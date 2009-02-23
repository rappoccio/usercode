#include "TROOT.h"
#include <iostream>
#include <cmath>

#include "PredictedDistribution.h"

using namespace std;

/*----------------------------------------------*/
/* CONSTRUCTORS                                 */
/*----------------------------------------------*/

//=============sets 1D histograms with fixed bins
PredictedDistribution::PredictedDistribution(const char* name, const char* title, Int_t nbinsx, Axis_t xlow, Axis_t xup) : 
  _fNDataHisto(nbinsx + 2),
  h1_r(0), 
  a2_taggable(), _errsSet(false)
{
  h1_o = new TH1D(name, title, nbinsx, xlow, xup);
  h1_o->Sumw2();
  char name2[20]; sprintf(name2,"%s_pred\0",name);
  h1_p = new TH1D(name2, title, nbinsx, xlow, xup);
  h1_p->Sumw2();
  char name3[20]; sprintf(name3,"%s_tgb\0",name);
  h1_tgb = new TH1D(name3, title, nbinsx, xlow, xup);
  h1_tgb->Sumw2();
}
   
//=============sets histograms with bin array
PredictedDistribution::PredictedDistribution(const char* name, const char* title, Int_t nbinsx, const Float_t* xbins) : 
  _fNDataHisto(nbinsx + 2),
  h1_r(0), 
  a2_taggable(0)
{
  h1_o = new TH1D(name, title, nbinsx, xbins);
  h1_o->Sumw2();
  char name2[20]; sprintf(name2,"%s_pred\0",name);
  h1_p = new TH1D(name2, title, nbinsx, xbins);
  h1_p->Sumw2();
  char name3[20]; sprintf(name3,"%s_tgb\0",name);
  h1_tgb = new TH1D(name3, title, nbinsx, xbins);
  h1_tgb->Sumw2();
}

/*----------------------------------------------*/
/*  DESTRUCTORS                                 */
/*----------------------------------------------*/
PredictedDistribution::~PredictedDistribution() {
  delete h1_p;	 h1_p=0;
  delete h1_o;	 h1_o=0;
  delete h1_tgb; h1_tgb=0;
  for (int i=0; i<a2_taggable.size(); i++) {
    delete a2_taggable[i]; a2_taggable[i]=0;
  }
}

void PredictedDistribution::SetRateMatrix(TH1D * mtx){
  if (!mtx) return;
  h1_r = mtx;
  a2_taggable.clear();
  a2_taggable.resize(_fNDataHisto,0); // allocate upon demand
}


//=============fill all per-jet histograms
// This method is broken for Sal's new matrix with phi as separate histogram
void PredictedDistribution::Accumulate(Float_t X, Float_t et, Bool_t tagged, Float_t weightFactor ) {
  //Fill returns the bin, but returns -1 for both over/underflow, so you must do two steps
  
  // Remember to include the weight factor, in case we are looping over
  // the jets multiple times
  
  Int_t bin = h1_r->FindBin( et );
  Float_t rate   = h1_r->GetBinContent(bin);
  Float_t err    = h1_r->GetBinError(bin);
  int maxIndex = h1_r->GetSize();

   //fill observed
  if ( weightFactor > 0.0 ) {
    h1_o->Fill(X,tagged ? weightFactor : 0.);
    //fill predicted
    h1_p->Fill(X,rate * weightFactor ); 
    // always fill taggable
    h1_tgb->Fill(X, weightFactor);
  
   
    //fill temporary error-weighting histogram
    // Errors are essentially
    // Pred = weightFactor * rate * N_tgb
    // dPred = weightFactor * sqrt( (R*dNtgb)^2 + (dR*Ntgb)^2)
    // As we fill it, though, Ntgb = 1, so this reduces numerically to
    // dPred += weightFactor * sqrt( (err*err + rate*rate)
    Int_t binx= h1_o->FindBin(X);
    if (a2_taggable[binx]==0) a2_taggable[binx] = new std::map<unsigned int, Float_t>;
//     cout << "dist bin = " << binx << endl;
//     cout << "rate bin = " << bin << endl;
//     cout << "rate     = " << rate << endl;
//     cout << "err      = " << err << endl;
//     cout << "weight   = " << weightFactor << endl;
//     cout << "quad sum = " << (*a2_taggable[binx])[bin] << endl;
//     cout << "dR*Ntgb  = " << weightFactor*weightFactor*err*err << endl;
//     cout << "R*dNtgb  = " << rate*rate*weightFactor << endl;
    (*a2_taggable[binx])[bin]+= weightFactor*weightFactor* ( err*err + rate*rate);
//     (*a2_taggable[binx])[bin]+= 1.0;  

  }
  
}

//=============call these three functions at the end of the job
void PredictedDistribution::SetCalculatedErrors() {
  if (! _errsSet) {
    if ( h1_p == 0 ) {
      std::cout << "We have no tags in PredictedDistribution, we're bailing out" << std::endl;
      return;
    }

    for (int i=0; i<a2_taggable.size(); i++) {
      Double_t QuadSum(0);
      if(a2_taggable[i] != 0){      
	for (std::map<unsigned int, Float_t>::const_iterator j=a2_taggable[i]->begin(); j!=a2_taggable[i]->end(); j++) {
	  unsigned int bin = (*j).first;
	  Float_t corrErr = (*j).second;
	  
	  QuadSum += corrErr;
	}
      }

      h1_p->SetBinError(i,std::sqrt(QuadSum)); 
//       cout << "Setting bin : " << i << " = " << h1_p->GetBinContent(i) << " +- " << h1_p->GetBinError(i) << endl;

    }

    _errsSet=true;
  }
}

void PredictedDistribution::DivideObserved(TH1D *h) {
  DivideDists(h1_o, h, true);
}
void PredictedDistribution::DividePredicted(TH1D *h) {
  DivideDists(h1_p, h, false);
}
void PredictedDistribution::DivideDists(TH1D *h1d_1, TH1D *h1d_2, bool useBinomial ) {  
  if (h1d_1==0 || h1d_2==0) {
    std::cout << "PredictedDistribution::DivideDists has all empty hists!" << std::endl;
    return ;
  }
  else {
    if (h1d_1->GetSize() != h1d_2->GetSize()) {
      std::cout << "PredictedDistribution::DivideDists has hists of different sizes!" << std::endl;
      return ;
    }
  }

  Int_t nent  = h1d_1->GetEntries();
  Int_t Nbin  = h1d_1->GetSize();

  for ( Int_t i = 0; i < Nbin; i++ ){
    Float_t val1 = h1d_1->GetBinContent( i );
    Float_t val2 = h1d_2->GetBinContent( i );
    Float_t err1 = h1d_1->GetBinError( i );
    Float_t err2 = h1d_2->GetBinError( i );

    Float_t val, err;
    if ( val2 != 0 ){
      if (!useBinomial) {
	val = val1 / val2;
	//	if (i==0) std::cout << "Using homegrown errors for " << h1->GetName() << std::endl;
	err = std::sqrt( err1*err1 + err2*err2*val1*val1/(val2*val2) ) / val2;
      } else { // calculate binomial err a la the other holloway
	BinomialEff rate;
	rate.Np = val1;
	rate.Nt = val2;
	  
	if ( (rate.Np < 0) || (rate.Nt < 0) || (rate.Nt < rate.Np) ) {
	  std::cout << "\n INVALID INPUT FOR ERROR CALCULATION. I QUIT! " 
	       << rate.Np << " " << rate.Nt << std::endl;
	  std::sqrt(-1.);
	}
	  
	val = rate.eff();
	// Treatment of case with low statistics per bin
	// In the rare case efficiency is 1, take error from lower bound
	// error from program.
	if (rate.Nt == rate.Np) {
	  err = rate.elo();
	} // If number of tags is less than 10 take error from higher bound
	  // from program
	else if (rate.Np < 10) { 
	  err = rate.eup();
	}
	// Otherwise, just use equation:
	else {
	  err = std::sqrt( val*(1-val) / (rate.Nt - 1));
	}
      }
    } else { //denom was zero, just bail
      val=0;
      err=0;
    } 

    h1d_1->SetBinContent(i, val );
    h1d_1->SetBinError(i, err );

  } //loop
  
  // Since SetBinContent increments the number of entries, we want to
  // reset them to what they were before
  h1d_1->SetEntries( nent );
}
