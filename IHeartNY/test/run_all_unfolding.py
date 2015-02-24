import subprocess



for s in [ 
           "python unfoldTopPt.py --lepType=ele --addNoBtag",           
           "python unfoldTopPt.py --lepType=ele --addNoBtag --systVariation=toptagFITup",
           "python unfoldTopPt.py --lepType=ele --addNoBtag --systVariation=toptagFITdn",
           "python unfoldTopPt.py --lepType=ele --addNoBtag --systVariation=jerup",
           "python unfoldTopPt.py --lepType=ele --addNoBtag --systVariation=jerdn",
           "python unfoldTopPt.py --lepType=ele --addNoBtag --systVariation=jecup",
           "python unfoldTopPt.py --lepType=ele --addNoBtag --systVariation=jecdn",
           "python unfoldTopPt.py --lepType=ele --addNoBtag --systVariation=btagup",
           "python unfoldTopPt.py --lepType=ele --addNoBtag --systVariation=btagdn",
           "python unfoldTopPt.py --lepType=ele --addNoBtag --ttbarPDF=CT10_pdfup",
           "python unfoldTopPt.py --lepType=ele --addNoBtag --ttbarPDF=CT10_pdfdown",

           "python unfoldTopPt.py --addNoBtag",           
           "python unfoldTopPt.py --addNoBtag --systVariation=toptagFITup",
           "python unfoldTopPt.py --addNoBtag --systVariation=toptagFITdn",
           "python unfoldTopPt.py --addNoBtag --systVariation=jerup",
           "python unfoldTopPt.py --addNoBtag --systVariation=jerdn",
           "python unfoldTopPt.py --addNoBtag --systVariation=jecup",
           "python unfoldTopPt.py --addNoBtag --systVariation=jecdn",
           "python unfoldTopPt.py --addNoBtag --systVariation=btagup",
           "python unfoldTopPt.py --addNoBtag --systVariation=btagdn",
           "python unfoldTopPt.py --addNoBtag --ttbarPDF=CT10_pdfup",
           "python unfoldTopPt.py --addNoBtag --ttbarPDF=CT10_pdfdown",

           "python unfoldTopPt.py --twoStep --lepType=ele --addNoBtag",           
           "python unfoldTopPt.py --twoStep --lepType=ele --addNoBtag --systVariation=toptagFITup",
           "python unfoldTopPt.py --twoStep --lepType=ele --addNoBtag --systVariation=toptagFITdn",
           "python unfoldTopPt.py --twoStep --lepType=ele --addNoBtag --systVariation=jerup",
           "python unfoldTopPt.py --twoStep --lepType=ele --addNoBtag --systVariation=jerdn",
           "python unfoldTopPt.py --twoStep --lepType=ele --addNoBtag --systVariation=jecup",
           "python unfoldTopPt.py --twoStep --lepType=ele --addNoBtag --systVariation=jecdn",
           "python unfoldTopPt.py --twoStep --lepType=ele --addNoBtag --systVariation=btagup",
           "python unfoldTopPt.py --twoStep --lepType=ele --addNoBtag --systVariation=btagdn",
           "python unfoldTopPt.py --twoStep --lepType=ele --addNoBtag --ttbarPDF=CT10_pdfup",
           "python unfoldTopPt.py --twoStep --lepType=ele --addNoBtag --ttbarPDF=CT10_pdfdown",

           "python unfoldTopPt.py --twoStep --addNoBtag",           
           "python unfoldTopPt.py --twoStep --addNoBtag --systVariation=toptagFITup",
           "python unfoldTopPt.py --twoStep --addNoBtag --systVariation=toptagFITdn",
           "python unfoldTopPt.py --twoStep --addNoBtag --systVariation=jerup",
           "python unfoldTopPt.py --twoStep --addNoBtag --systVariation=jerdn",
           "python unfoldTopPt.py --twoStep --addNoBtag --systVariation=jecup",
           "python unfoldTopPt.py --twoStep --addNoBtag --systVariation=jecdn",
           "python unfoldTopPt.py --twoStep --addNoBtag --systVariation=btagup",
           "python unfoldTopPt.py --twoStep --addNoBtag --systVariation=btagdn",
           "python unfoldTopPt.py --twoStep --addNoBtag --ttbarPDF=CT10_pdfup",
           "python unfoldTopPt.py --twoStep --addNoBtag --ttbarPDF=CT10_pdfdown",
           ] : 
    print s
    subprocess.call( [s, ""], shell=True )
    
    
