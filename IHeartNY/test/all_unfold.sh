#python run_all_unfolding.py --closureTests --ttbarPDF="CT10_nom"

python run_all_unfolding.py --ttbarPDF="CT10_nom" 
python run_all_unfolding.py --ttbarPDF="CT10_pdfup"
python run_all_unfolding.py --ttbarPDF="CT10_pdfdown"
#python run_all_unfolding.py --ttbarPDF="MSTW_nom"
#python run_all_unfolding.py --ttbarPDF="MSTW_pdfup"
#python run_all_unfolding.py --ttbarPDF="MSTW_pdfdown"
#python run_all_unfolding.py --ttbarPDF="NNPDF_nom"
#python run_all_unfolding.py --ttbarPDF="NNPDF_pdfup"
#python run_all_unfolding.py --ttbarPDF="NNPDF_pdfdown"
python run_all_unfolding.py --ttbarPDF="scaleup"
python run_all_unfolding.py --ttbarPDF="scaledown"
python run_all_unfolding.py --ttbarPDF="MG" 
python run_all_unfolding.py --ttbarPDF="mcnlo" 

python run_all_unfolding.py --ttbarPDF="CT10_nom" --oneRegion
python run_all_unfolding.py --ttbarPDF="CT10_pdfup" --oneRegion
python run_all_unfolding.py --ttbarPDF="CT10_pdfdown" --oneRegion
python run_all_unfolding.py --ttbarPDF="scaleup" --oneRegion
python run_all_unfolding.py --ttbarPDF="scaledown" --oneRegion
python run_all_unfolding.py --ttbarPDF="MG" --oneRegion
python run_all_unfolding.py --ttbarPDF="mcnlo" --oneRegion

