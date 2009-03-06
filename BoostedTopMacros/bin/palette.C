#include "TColor.h"
#include "TStyle.h"


void palette( int colNum, int offset = 251, int nAppend = 0, TColor * appended = 0 )
{
   //example of new colors (greys) and definition of a new palette
   
   Int_t * palette = new Int_t [colNum + nAppend];
   Int_t i = 0;
   for (;i<colNum;i++) {
     TColor *color = new TColor(offset+i,
				1.0,
				(float)(i+1)/(float)colNum, 
				(float)(i+1)/(float)colNum,
				"");
     palette[i] = 251+i;
   }
   for ( ; i < colNum + nAppend; ++i ){
     TColor * color = new TColor( appended[i-colNum] );
     palette[i] = 251 + i;
   }
   gStyle->SetPalette(colNum,palette);
   
   delete [] palette; 
}

