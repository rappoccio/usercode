import subprocess



for s in [ #"python plot_mle_fitted_results.py --normdir=NormalizedHists_CT10_nom --file=run_theta/histos-mle-2d-CT10_nom_mu.root --channel=mu",
        #"python plot_mle_fitted_results.py --normdir=NormalizedHists_CT10_pdfup --file=run_theta/histos-mle-2d-CT10_pdfup_mu.root --channel=mu",
        #"python plot_mle_fitted_results.py --normdir=NormalizedHists_CT10_pdfdown --file=run_theta/histos-mle-2d-CT10_pdfdown_mu.root --channel=mu",
        #"python plot_mle_fitted_results.py --normdir=NormalizedHists_MSTW_nom --file=run_theta/histos-mle-2d-MSTW_nom_mu.root --channel=mu",
        #"python plot_mle_fitted_results.py --normdir=NormalizedHists_MSTW_pdfup --file=run_theta/histos-mle-2d-MSTW_pdfup_mu.root --channel=mu",
        #"python plot_mle_fitted_results.py --normdir=NormalizedHists_MSTW_pdfdown --file=run_theta/histos-mle-2d-MSTW_pdfdown_mu.root --channel=mu",           
        #"python plot_mle_fitted_results.py --normdir=NormalizedHists_NNPDF_nom --file=run_theta/histos-mle-2d-NNPDF_nom_mu.root --channel=mu",
        #"python plot_mle_fitted_results.py --normdir=NormalizedHists_NNPDF_pdfup --file=run_theta/histos-mle-2d-NNPDF_pdfup_mu.root --channel=mu",
        #"python plot_mle_fitted_results.py --normdir=NormalizedHists_NNPDF_pdfdown --file=run_theta/histos-mle-2d-NNPDF_pdfdown_mu.root --channel=mu",           
        #"python plot_mle_fitted_results.py --normdir=NormalizedHists_scaleup --file=run_theta/histos-mle-2d-scaleup_mu.root --channel=mu",
        #"python plot_mle_fitted_results.py --normdir=NormalizedHists_scaledown --file=run_theta/histos-mle-2d-scaledown_mu.root --channel=mu",
        
        "python plot_mle_fitted_results.py --normdir=NormalizedHists_CT10_nom --file=run_theta/histos-mle-2d-CT10_nom_el.root --channel=el",
        "python plot_mle_fitted_results.py --normdir=NormalizedHists_CT10_pdfup --file=run_theta/histos-mle-2d-CT10_pdfup_el.root --channel=el",
        "python plot_mle_fitted_results.py --normdir=NormalizedHists_CT10_pdfdown --file=run_theta/histos-mle-2d-CT10_pdfdown_el.root --channel=el",
        #"python plot_mle_fitted_results.py --normdir=NormalizedHists_MSTW_nom --file=run_theta/histos-mle-2d-MSTW_nom_el.root --channel=el",
        #"python plot_mle_fitted_results.py --normdir=NormalizedHists_MSTW_pdfup --file=run_theta/histos-mle-2d-MSTW_pdfup_el.root --channel=el",
        #"python plot_mle_fitted_results.py --normdir=NormalizedHists_MSTW_pdfdown --file=run_theta/histos-mle-2d-MSTW_pdfdown_el.root --channel=el",           
        #"python plot_mle_fitted_results.py --normdir=NormalizedHists_NNPDF_nom --file=run_theta/histos-mle-2d-NNPDF_nom_el.root --channel=el",
        #"python plot_mle_fitted_results.py --normdir=NormalizedHists_NNPDF_pdfup --file=run_theta/histos-mle-2d-NNPDF_pdfup_el.root --channel=el",
        #"python plot_mle_fitted_results.py --normdir=NormalizedHists_NNPDF_pdfdown --file=run_theta/histos-mle-2d-NNPDF_pdfdown_el.root --channel=el",           
        #"python plot_mle_fitted_results.py --normdir=NormalizedHists_scaleup --file=run_theta/histos-mle-2d-scaleup_el.root --channel=el",
        #"python plot_mle_fitted_results.py --normdir=NormalizedHists_scaledown --file=run_theta/histos-mle-2d-scaledown_el.root --channel=el",
        

                       ] : 
    print s
    subprocess.call( [s, ""], shell=True )
    
    
