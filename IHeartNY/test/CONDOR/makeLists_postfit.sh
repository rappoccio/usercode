rm listofjobs_post_*

python run_pdfs_CT10_iheartny.py --postfit="comb" > listofjobs_post_CT10_mu
python run_pdfs_NS_CT10_iheartny.py --postfit="comb" > listofjobs_post_CT10_NS_mu
python run_pdfs_CT10_el_iheartny.py --postfit="comb" > listofjobs_post_CT10_el
python run_pdfs_NS_CT10_el_iheartny.py --postfit="comb" > listofjobs_post_CT10_NS_el

python run_pdfs_MSTW_iheartny.py --postfit="comb" > listofjobs_post_MSTW_mu
python run_pdfs_NS_MSTW_iheartny.py --postfit="comb" > listofjobs_post_MSTW_NS_mu
python run_pdfs_MSTW_el_iheartny.py --postfit="comb" > listofjobs_post_MSTW_el
python run_pdfs_NS_MSTW_el_iheartny.py --postfit="comb" > listofjobs_post_MSTW_NS_el

python run_pdfs_NNPDF_iheartny.py --postfit="comb" > listofjobs_post_NNPDF_mu
python run_pdfs_NS_NNPDF_iheartny.py --postfit="comb" > listofjobs_post_NNPDF_NS_mu
python run_pdfs_NNPDF_el_iheartny.py --postfit="comb" > listofjobs_post_NNPDF_el
python run_pdfs_NS_NNPDF_el_iheartny.py --postfit="comb" > listofjobs_post_NNPDF_NS_el

python run_q2_iheartny.py --postfit="comb" > listofjobs_post_q2_mu
python run_q2_NS_iheartny.py --postfit="comb" > listofjobs_post_q2_NS_mu
python run_q2_el_iheartny.py --postfit="comb" > listofjobs_post_q2_el
python run_q2_NS_el_iheartny.py --postfit="comb" > listofjobs_post_q2_NS_el

python run_pdfs_MG_iheartny.py --postfit="comb" > listofjobs_post_MG
python run_pdfs_mcnlo_iheartny.py --postfit="comb" > listofjobs_post_mcnlo


rm commands_post_*

./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_post_CT10_mu commands_post_CT10_mu
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_post_CT10_el commands_post_CT10_el
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_post_CT10_NS_mu commands_post_CT10_NS_mu
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_post_CT10_NS_el commands_post_CT10_NS_el

./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_post_MSTW_mu commands_post_MSTW_mu
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_post_MSTW_NS_mu commands_post_MSTW_NS_mu
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_post_MSTW_el commands_post_MSTW_el
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_post_MSTW_NS_el commands_post_MSTW_NS_el

./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_post_NNPDF_mu commands_post_NNPDF_mu
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_post_NNPDF_el commands_post_NNPDF_el
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_post_NNPDF_NS_mu commands_post_NNPDF_NS_mu
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_post_NNPDF_NS_el commands_post_NNPDF_NS_el

./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_post_q2_mu commands_post_q2_mu
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_post_q2_el commands_post_q2_el
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_post_q2_NS_mu commands_post_q2_NS_mu
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_post_q2_NS_el commands_post_q2_NS_el

./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_post_MG commands_post_MG
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_post_mcnlo commands_post_mcnlo

