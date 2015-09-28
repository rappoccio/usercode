#!/bin/bash

./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz listofjobs_CT10_mu commands_CT10_mu
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz listofjobs_CT10_el commands_CT10_el
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz listofjobs_q2_mu commands_q2_mu
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz listofjobs_q2_el commands_q2_el
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz listofjobs_CT10_NS_mu commands_CT10_NS_mu
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz listofjobs_CT10_NS_el commands_CT10_NS_el
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz listofjobs_q2_NS_mu commands_q2_NS_mu
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz listofjobs_q2_NS_el commands_q2_NS_el
./runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz listofjobs_MG commands_MG

./runManySections.py --submitCondor commands_CT10_mu
./runManySections.py --submitCondor commands_CT10_el
./runManySections.py --submitCondor commands_q2_mu
./runManySections.py --submitCondor commands_q2_el
./runManySections.py --submitCondor commands_CT10_NS_mu
./runManySections.py --submitCondor commands_CT10_NS_el
./runManySections.py --submitCondor commands_q2_NS_mu
./runManySections.py --submitCondor commands_q2_NS_el
./runManySections.py --submitCondor commands_MG

condor_q skinnari