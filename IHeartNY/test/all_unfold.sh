python run_all_unfolding.py --closureTests
python run_all_unfolding.py --genCheck

python run_all_unfolding.py --ttbarPDF="CT10_nom" 
python run_all_unfolding.py --ttbarPDF="CT10_pdfup"
python run_all_unfolding.py --ttbarPDF="CT10_pdfdown"
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

python run_all_unfolding.py --closureTests --toUnfold="y"
python run_all_unfolding.py --genCheck --toUnfold="y"

python run_all_unfolding.py --ttbarPDF="CT10_nom" --toUnfold="y"
python run_all_unfolding.py --ttbarPDF="CT10_pdfup" --toUnfold="y"
python run_all_unfolding.py --ttbarPDF="CT10_pdfdown" --toUnfold="y"
python run_all_unfolding.py --ttbarPDF="scaleup" --toUnfold="y"
python run_all_unfolding.py --ttbarPDF="scaledown" --toUnfold="y"
python run_all_unfolding.py --ttbarPDF="MG" --toUnfold="y"
python run_all_unfolding.py --ttbarPDF="mcnlo" --toUnfold="y"

python run_all_unfolding.py --ttbarPDF="CT10_nom" --oneRegion --toUnfold="y"
python run_all_unfolding.py --ttbarPDF="CT10_pdfup" --oneRegion --toUnfold="y"
python run_all_unfolding.py --ttbarPDF="CT10_pdfdown" --oneRegion --toUnfold="y"
python run_all_unfolding.py --ttbarPDF="scaleup" --oneRegion --toUnfold="y"
python run_all_unfolding.py --ttbarPDF="scaledown" --oneRegion --toUnfold="y"
python run_all_unfolding.py --ttbarPDF="MG" --oneRegion --toUnfold="y"
python run_all_unfolding.py --ttbarPDF="mcnlo" --oneRegion --toUnfold="y"
