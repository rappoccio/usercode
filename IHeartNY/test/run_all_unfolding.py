import subprocess



for s in [ "python unfoldTopPt.py",           
           "python unfoldTopPt.py --systVariation=toptagup",
           "python unfoldTopPt.py --systVariation=toptagdn",
           "python unfoldTopPt.py --systVariation=toptagFITup",
           "python unfoldTopPt.py --systVariation=toptagFITdn",
           "python unfoldTopPt.py --systVariation=jerup",
           "python unfoldTopPt.py --systVariation=jerdn",
           "python unfoldTopPt.py --systVariation=jecup",
           "python unfoldTopPt.py --systVariation=jecdn",
           "python unfoldTopPt.py --systVariation=btagup",
           "python unfoldTopPt.py --systVariation=btagdn",
           "python unfoldTopPt.py --ttbarPDF=CT10_pdfup",
           "python unfoldTopPt.py --ttbarPDF=CT10_pdfdown",
           "python unfoldTopPt.py --ttbarPDF=scaleup",
           "python unfoldTopPt.py --ttbarPDF=scaledown",
           "python unfoldTopPt.py --ttbarPDF=MSTW_nom",
           "python unfoldTopPt.py --ttbarPDF=MSTW_pdfup",
           "python unfoldTopPt.py --ttbarPDF=MSTW_pdfdown",
           "python unfoldTopPt.py --ttbarPDF=NNPDF_nom",
           "python unfoldTopPt.py --ttbarPDF=NNPDF_pdfup",
           "python unfoldTopPt.py --ttbarPDF=NNPDF_pdfdown",
            ] : 
    print s
    subprocess.call( [s, ""], shell=True )
    
    
