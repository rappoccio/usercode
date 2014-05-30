README for commit to github

This directory contains the code needed to perform the QCD normalization.
To determine the QCD normalization, run
root> .x QCDminfit_3.cc+    if there is a significant contribution from W+jets (i.e. early in the cutflow)    
or 
root> .x QCDminfit.cc+      to include the W+jets component in the top template (i.e. late in the cutflow)
This produces plots containing the fitted MET distribution, the templates used to fit the MET distribution, and breakdowns of the top and QCD templates (both with the contributions stacked together, and with the contributions seperately normalized to 1).  
There are some user-defined parameters to input to the fitter.  Because I am lazy, these need to be changed in the code, rather than being input at the command line.  The code header describes the location of all user inputs.
