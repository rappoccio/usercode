import subprocess



for s in [ "python unfoldTopPt.py --unfoldType=pt400 --addNoBtag",           
           #"python unfoldTopPt.py --unfoldType=pt400 --addNoBtag --systVariation=toptagup",
           #"python unfoldTopPt.py --unfoldType=pt400 --addNoBtag --systVariation=toptagdn",
           "python unfoldTopPt.py --unfoldType=pt400 --addNoBtag --systVariation=toptagFITup",
           "python unfoldTopPt.py --unfoldType=pt400 --addNoBtag --systVariation=toptagFITdn",
           "python unfoldTopPt.py --unfoldType=pt400 --addNoBtag --systVariation=jerup",
           "python unfoldTopPt.py --unfoldType=pt400 --addNoBtag --systVariation=jerdn",
           "python unfoldTopPt.py --unfoldType=pt400 --addNoBtag --systVariation=jecup",
           "python unfoldTopPt.py --unfoldType=pt400 --addNoBtag --systVariation=jecdn",
           "python unfoldTopPt.py --unfoldType=pt400 --addNoBtag --systVariation=btagup",
           "python unfoldTopPt.py --unfoldType=pt400 --addNoBtag --systVariation=btagdn",
           "python unfoldTopPt.py --unfoldType=pt400 --addNoBtag --ttbarPDF=CT10_pdfup",
           "python unfoldTopPt.py --unfoldType=pt400 --addNoBtag --ttbarPDF=CT10_pdfdown",
           #"python unfoldTopPt.py --unfoldType=pt400 --addNoBtag --ttbarPDF=scaleup",
           #"python unfoldTopPt.py --unfoldType=pt400 --addNoBtag --ttbarPDF=scaledown",
           "python unfoldTopPt.py --unfoldType=pt400 --addNoBtag --ttbarPDF=MSTW_nom",
           "python unfoldTopPt.py --unfoldType=pt400 --addNoBtag --ttbarPDF=MSTW_pdfup",
           "python unfoldTopPt.py --unfoldType=pt400 --addNoBtag --ttbarPDF=MSTW_pdfdown",
           "python unfoldTopPt.py --unfoldType=pt400 --addNoBtag --ttbarPDF=NNPDF_nom",
           "python unfoldTopPt.py --unfoldType=pt400 --addNoBtag --ttbarPDF=NNPDF_pdfup",
           "python unfoldTopPt.py --unfoldType=pt400 --addNoBtag --ttbarPDF=NNPDF_pdfdown",

           "python unfoldTopPt.py --unfoldType=full --addNoBtag",           
           #"python unfoldTopPt.py --unfoldType=full --addNoBtag --systVariation=toptagup",
           #"python unfoldTopPt.py --unfoldType=full --addNoBtag --systVariation=toptagdn",
           "python unfoldTopPt.py --unfoldType=full --addNoBtag --systVariation=toptagFITup",
           "python unfoldTopPt.py --unfoldType=full --addNoBtag --systVariation=toptagFITdn",
           "python unfoldTopPt.py --unfoldType=full --addNoBtag --systVariation=jerup",
           "python unfoldTopPt.py --unfoldType=full --addNoBtag --systVariation=jerdn",
           "python unfoldTopPt.py --unfoldType=full --addNoBtag --systVariation=jecup",
           "python unfoldTopPt.py --unfoldType=full --addNoBtag --systVariation=jecdn",
           "python unfoldTopPt.py --unfoldType=full --addNoBtag --systVariation=btagup",
           "python unfoldTopPt.py --unfoldType=full --addNoBtag --systVariation=btagdn",
           "python unfoldTopPt.py --unfoldType=full --addNoBtag --ttbarPDF=CT10_pdfup",
           "python unfoldTopPt.py --unfoldType=full --addNoBtag --ttbarPDF=CT10_pdfdown",
           #"python unfoldTopPt.py --unfoldType=full --addNoBtag --ttbarPDF=scaleup",
           #"python unfoldTopPt.py --unfoldType=full --addNoBtag --ttbarPDF=scaledown",
           "python unfoldTopPt.py --unfoldType=full --addNoBtag --ttbarPDF=MSTW_nom",
           "python unfoldTopPt.py --unfoldType=full --addNoBtag --ttbarPDF=MSTW_pdfup",
           "python unfoldTopPt.py --unfoldType=full --addNoBtag --ttbarPDF=MSTW_pdfdown",
           "python unfoldTopPt.py --unfoldType=full --addNoBtag --ttbarPDF=NNPDF_nom",
           "python unfoldTopPt.py --unfoldType=full --addNoBtag --ttbarPDF=NNPDF_pdfup",
           "python unfoldTopPt.py --unfoldType=full --addNoBtag --ttbarPDF=NNPDF_pdfdown",
            ] : 
    print s
    subprocess.call( [s, ""], shell=True )
    
    
