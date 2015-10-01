rm listofjobs_postEMU_*

python run_pdfs_CT10_iheartny.py --postfit="emu" > listofjobs_postEMU_CT10_mu
python run_pdfs_NS_CT10_iheartny.py --postfit="emu" > listofjobs_postEMU_CT10_NS_mu
python run_pdfs_CT10_el_iheartny.py --postfit="emu" > listofjobs_postEMU_CT10_el
python run_pdfs_NS_CT10_el_iheartny.py --postfit="emu" > listofjobs_postEMU_CT10_NS_el

python run_q2_iheartny.py --postfit="emu" > listofjobs_postEMU_q2_mu
python run_q2_NS_iheartny.py --postfit="emu" > listofjobs_postEMU_q2_NS_mu
python run_q2_el_iheartny.py --postfit="emu" > listofjobs_postEMU_q2_el
python run_q2_NS_el_iheartny.py --postfit="emu" > listofjobs_postEMU_q2_NS_el


rm commands_postEMU_*

./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_postEMU_CT10_mu commands_postEMU_CT10_mu
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_postEMU_CT10_el commands_postEMU_CT10_el
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_postEMU_CT10_NS_mu commands_postEMU_CT10_NS_mu
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_postEMU_CT10_NS_el commands_postEMU_CT10_NS_el

./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_postEMU_q2_mu commands_postEMU_q2_mu
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_postEMU_q2_el commands_postEMU_q2_el
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_postEMU_q2_NS_mu commands_postEMU_q2_NS_mu
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz  listofjobs_postEMU_q2_NS_el commands_postEMU_q2_NS_el

