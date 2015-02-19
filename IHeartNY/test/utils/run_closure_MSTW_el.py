#!/usr/bin/env python

import time
import Queue
import subprocess
import threading


samples = [
    '--files=/uscms_data/d3/sdittmer/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_el/res/*root',
    '--files=/uscms_data/d3/sdittmer/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_el/res/*root',
    '--files=/uscms_data/d3/sdittmer/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_el/res/*root'
]
outname = [
    '--outname=TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_',
    '--outname=TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_',
    '--outname=TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_'
]

oddeven = [ '--oddeven=1', '--oddeven=2' ]
name_oddeven = [ 'odd', 'even' ]

pdfsysts = [ '--pdfSys=0.0', '--pdfSys=1.0', '--pdfSys=-1.0' ]
name_pdfsysts = [ "_nom", "_pdfup", "_pdfdown" ]

#pdfsets = [ '--pdfSet=0.0', '--pdfSet=1.0', '--pdfSet=2.0' ]
#name_pdfsets = [ 'CT10', 'MSTW', 'NNPDF' ]
pdfsets = [ '--pdfSet=1.0' ]
name_pdfsets = [ 'MSTW' ]


def worker(q):
    while True:
        args = q.get()
        subprocess.call(args)
        q.task_done()

def run_threads (samples) :
    q = Queue.Queue()
    num_worker_threads = 8
    for i in range(num_worker_threads):        
         t = threading.Thread(target=worker, args=(q,))
         t.daemon = True
         t.start()

    for isample in range(0,len(samples)): 
        for ioe in range(0,len(oddeven)):
            for isyst in range(0,len(pdfsysts)):
                for iset in range(0,len(pdfsets)):
                    s = [ 'python', 'iheartny_topxs_fwlite.py', samples[isample], oddeven[ioe], pdfsysts[isyst], pdfsets[iset], 
                          '--makeResponse', '--semilep=1', '--pileup=ttbar', '--jerSys=0.1', '--use2Dcut', '--lepType=ele',
                          outname[isample]+name_pdfsets[iset]+name_pdfsysts[isyst]+"_2Dcut_nom_"+name_oddeven[ioe] ]
                    if isample==0:
                        s.append('--mttGenMax=700.')
                    q.put(s)    
    q.join()


print "Starting running threads ..."
run_threads( samples )
print "... all done with running threads!!"

