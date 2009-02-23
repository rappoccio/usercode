#include "TColor.h"
#include "TStyle.h"


void palette( int colNum )
{
   //example of new colors (greys) and definition of a new palette
   
   Int_t * palette = new Int_t [colNum];
   for (Int_t i=0;i<colNum;i++) {
     TColor *color = new TColor(251+i,
				1.0,
				(float)(i+1)/(float)colNum, 
				(float)(i+1)/(float)colNum,
				"");
     palette[i] = 251+i;
   }
   gStyle->SetPalette(colNum,palette);
   
   delete [] palette; 
}

