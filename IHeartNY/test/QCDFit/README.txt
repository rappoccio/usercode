README for commit to github

This directory contains the code needed to perform the QCD normalization.
To determine the QCD normalization, run
root> .x QCDminfit_3.cc+    if there is a significant contribution from W+jets    
or 
root> .x QCDminfit.cc+      to include the W+jets component in the top template

This produces plots containing the fitted MET distribution, the templates used to fit the MET distribution, and breakdowns of the top and QCD templates (both with the contributions stacked together, and with the contributions seperately normalized to 1).  
There are some user-defined parameters to input to the fitter.  Because I am lazy, these need to be changed in the code, rather than being input at the command line.  The code header describes the location of all user inputs.

Edit, 7/24/14:
QCDminfit_3.cc is currently slightly out of date.  It needs to be updated to include W+(1/2/3/4)Jets samples, the correct TTJets efficiencies, and (possibly) the correct location of the histogram files.  It also needs to have a 2D option added, as in QCDminfit.cc.

Edit, 10/20/14:
QCDminfit.cc has been updated to have options for varying the amount of non-QCD contribution subtracted from the sideband to get the QCD template.  There is also an option to use exclusive regions or inclusive.
