import subprocess



for s in [ "python unfoldTopPt.py --ttbarPDF=scaleup --systVariation=scaleup_2Dcut_nom",
           "python unfoldTopPt.py --ttbarPDF=scaledown --systVariation=scaledown_2Dcut_nom",
           "python unfoldTopPt.py --systVariation=CT10_nom_2Dcut_nom",           
           "python unfoldTopPt.py --ttbarPDF=CT10_pdfup --systVariation=CT10_pdfup_2Dcut_nom",
           "python unfoldTopPt.py --ttbarPDF=CT10_pdfdown --systVariation=CT10_pdfdown_2Dcut_nom",
           "python unfoldTopPt.py --systVariation=CT10_nom_2Dcut_toptagup",
           "python unfoldTopPt.py --systVariation=CT10_nom_2Dcut_toptagdn",
           "python unfoldTopPt.py --systVariation=CT10_nom_2Dcut_jerup",
           "python unfoldTopPt.py --systVariation=CT10_nom_2Dcut_jerdn",
           "python unfoldTopPt.py --systVariation=CT10_nom_2Dcut_jecup",
           "python unfoldTopPt.py --systVariation=CT10_nom_2Dcut_jecdn",
           "python unfoldTopPt.py --systVariation=CT10_nom_2Dcut_btagup",
           "python unfoldTopPt.py --systVariation=CT10_nom_2Dcut_btagdn",
           "python unfoldTopPt.py --ttbarPDF=MSTW_nom --systVariation=MSTW_nom_2Dcut_nom",
           "python unfoldTopPt.py --ttbarPDF=MSTW_pdfup --systVariation=MSTW_pdfup_2Dcut_nom",
           "python unfoldTopPt.py --ttbarPDF=MSTW_pdfdown --systVariation=MSTW_pdfdown_2Dcut_nom",
           "python unfoldTopPt.py --ttbarPDF=NNPDF_nom --systVariation=NNPDF_nom_2Dcut_nom",
           "python unfoldTopPt.py --ttbarPDF=NNPDF_pdfup --systVariation=NNPDF_pdfup_2Dcut_nom",
           "python unfoldTopPt.py --ttbarPDF=NNPDF_pdfdown --systVariation=NNPDF_pdfdown_2Dcut_nom",
            ] : 
    print s
    subprocess.call( [s, ""], shell=True )
    
    
