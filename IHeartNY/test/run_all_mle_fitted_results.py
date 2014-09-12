import subprocess



for s in [ "python plot_mle_fitted_results.py --normdir=NormalizedHists_CT10_nom --file=run_theta/histos-mle-2d-CT10_nom.root",
           "python plot_mle_fitted_results.py --normdir=NormalizedHists_CT10_pdfup --file=run_theta/histos-mle-2d-CT10_pdfup.root",
           "python plot_mle_fitted_results.py --normdir=NormalizedHists_CT10_pdfdown --file=run_theta/histos-mle-2d-CT10_pdfdown.root",
           "python plot_mle_fitted_results.py --normdir=NormalizedHists_MSTW_nom --file=run_theta/histos-mle-2d-MSTW_nom.root",
           "python plot_mle_fitted_results.py --normdir=NormalizedHists_MSTW_pdfup --file=run_theta/histos-mle-2d-MSTW_pdfup.root",
           "python plot_mle_fitted_results.py --normdir=NormalizedHists_MSTW_pdfdown --file=run_theta/histos-mle-2d-MSTW_pdfdown.root",           
           "python plot_mle_fitted_results.py --normdir=NormalizedHists_NNPDF_nom --file=run_theta/histos-mle-2d-NNPDF_nom.root",
           "python plot_mle_fitted_results.py --normdir=NormalizedHists_NNPDF_pdfup --file=run_theta/histos-mle-2d-NNPDF_pdfup.root",
           "python plot_mle_fitted_results.py --normdir=NormalizedHists_NNPDF_pdfdown --file=run_theta/histos-mle-2d-NNPDF_pdfdown.root",           
           "python plot_mle_fitted_results.py --normdir=NormalizedHists_scaleup --file=run_theta/histos-mle-2d-scaleup.root",
           "python plot_mle_fitted_results.py --normdir=NormalizedHists_scaledown --file=run_theta/histos-mle-2d-scaledown.root",


                       ] : 
    print s
    subprocess.call( [s, ""], shell=True )
    
    
