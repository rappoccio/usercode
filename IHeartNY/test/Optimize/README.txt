README for commit to github

This directory contains the code and histograms needed to perform the selection optimization.
The code to produce the histograms is optimize_topxs.py, and is modified from iheartny_topxs_fwlite.py. 
It can be run on all files using 
> python run_all_optimize.py
or run on MC only using 
> run_MC_optimize.py 
The histograms produced by optimize_topxs.py are included in this directory for convenience.

To determine the QCD normalization, run
root> .x QCDminfit_3.cc+    if there is a significant contribution from W+jets (i.e. for the 0 tag case)    
or 
root> .x QCDminfit.cc+      to include the W+jets component in the top template
This produces plots containing the fitted MET distribution, the templates used to fit the MET distribution, and breakdowns of the templates (both with the contributions stacked together, and with the contributions seperately normalized to 1) when relevant.  
There are some user-defined parameters to input to the fitter.  Because I am lazy, these need to be changed in the code, rather than being input at the command line.  The code header describes the location of all user inputs.

Once the QCD normalization has been obtained, the relevant plots for optimization can be produced by running
root> .x OptSel.cc+
This produces 2D correlation plots of the cuts being optimized, as well as signal, background, and significance distributions for each cut quantity.  
As previously, there are some options which need to be set by the user in the code.  Again, the relevant lines are listed in the code header.
