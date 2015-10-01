rm listofjobs_data_mu
python run_data_iheartny.py > listofjobs_data_mu
rm listofjobs_data_el
python run_data_el_iheartny.py > listofjobs_data_el

rm listofjobs_nontop_mu
python run_nontop_iheartny.py > listofjobs_nontop_mu
rm listofjobs_nontop_el
python run_nontop_el_iheartny.py > listofjobs_nontop_el

rm listofjobs_CT10_mu
python run_pdfs_CT10_iheartny.py > listofjobs_CT10_mu
rm listofjobs_CT10_NS_mu
python run_pdfs_NS_CT10_iheartny.py > listofjobs_CT10_NS_mu
rm listofjobs_CT10_el
python run_pdfs_CT10_el_iheartny.py > listofjobs_CT10_el
rm listofjobs_CT10_NS_el
python run_pdfs_NS_CT10_el_iheartny.py > listofjobs_CT10_NS_el

rm listofjobs_q2_mu
python run_q2_iheartny.py > listofjobs_q2_mu
rm listofjobs_q2_NS_mu
python run_q2_NS_iheartny.py > listofjobs_q2_NS_mu
rm listofjobs_q2_el
python run_q2_el_iheartny.py > listofjobs_q2_el
rm listofjobs_q2_NS_el
python run_q2_NS_el_iheartny.py > listofjobs_q2_NS_el

rm listofjobs_MG
python run_pdfs_MG_iheartny.py > listofjobs_MG
rm listofjobs_mcatnlo
python run_pdfs_mcnlo_iheartny.py > listofjobs_mcatnlo

rm commands_data_mu
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_data_mu commands_data_mu
rm commands_data_el
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_data_el commands_data_el
rm commands_nontop_mu
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_nontop_mu commands_nontop_mu
rm commands_nontop_el
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_nontop_el commands_nontop_el

rm commands_CT10_mu
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_CT10_mu commands_CT10_mu
rm commands_CT10_el
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_CT10_el commands_CT10_el
rm commands_CT10_NS_mu
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_CT10_NS_mu commands_CT10_NS_mu
rm commands_CT10_NS_el
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_CT10_NS_el commands_CT10_NS_el

rm commands_q2_mu
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_q2_mu commands_q2_mu
rm commands_q2_el
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_q2_el commands_q2_el
rm commands_q2_NS_mu
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_q2_NS_mu commands_q2_NS_mu
rm commands_q2_NS_el
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_q2_NS_el commands_q2_NS_el

