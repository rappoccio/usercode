#!/usr/bin/env python

import time
import Queue
import subprocess
import threading


samples = [
    '--files=/uscms/home/skinnari/nobackup/TopXS_slc6/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_truth_mu/res/*root',
    '--files=/uscms/home/skinnari/nobackup/TopXS_slc6/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_truth_mu/res/*root',
    '--files=/uscms/home/skinnari/nobackup/TopXS_slc6/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_truth_mu/res/*root'
]
outname = [
    '--outname=TT_max700_',
    '--outname=TT_Mtt-700to1000_',
    '--outname=TT_Mtt-1000toInf_'
]

oddeven = [ '', '--oddeven=1', '--oddeven=2' ]
name_oddeven = [ '', '_odd', '_even' ]

pdfsysts = [ '--pdfSys=0.0', '--pdfSys=1.0', '--pdfSys=-1.0' ]
name_pdfsysts = [ "_nom", "_pdfup", "_pdfdown" ]

#pdfsets = [ '--pdfSet=0.0', '--pdfSet=1.0', '--pdfSet=2.0' ]
#name_pdfsets = [ 'CT10', 'MSTW', 'NNPDF' ]
pdfsets = [ '--pdfSet=0.0' ]
name_pdfsets = [ 'CT10' ]

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
                    s = [ 'python', 'runTruth.py', samples[isample], oddeven[ioe], pdfsysts[isyst], pdfsets[iset], 
                          '--pileup=ttbar',
                          outname[isample]+name_pdfsets[iset]+name_pdfsysts[isyst]+"_fullTruth"+name_oddeven[ioe] ]
                    if isample==0:
                        s.append('--mttGenMax=700.')
                    q.put(s)    
    q.join()


print "Starting running threads ..."
run_threads( samples )
print "... all done with running threads!!"

