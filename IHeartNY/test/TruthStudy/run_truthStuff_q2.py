#!/usr/bin/env python

import time
import Queue
import subprocess
import threading


samples = [
    '--files=/uscms/home/skinnari/nobackup/TopXS_slc6/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_max700_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola_iheartNY_truth_mu/res/*root',
    '--files=/uscms/home/skinnari/nobackup/TopXS_slc6/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_max700_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola_iheartNY_truth_mu/res/*root',
    '--files=/uscms/home/skinnari/nobackup/TopXS_Feb15/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola_truth_mu/res/*root',
    '--files=/uscms/home/skinnari/nobackup/TopXS_Feb15/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola_truth_mu/res/*root',
    '--files=/uscms/home/skinnari/nobackup/TopXS_Feb15/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola_truth_mu/res/*root',
    '--files=/uscms/home/skinnari/nobackup/TopXS_Feb15/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola_truth_mu/res/*root'
]
outname = [
    '--outname=TT_max700_scaleup_',
    '--outname=TT_max700_scaledown_',
    '--outname=TT_Mtt-700to1000_scaleup_',
    '--outname=TT_Mtt-700to1000_scaledown_',
    '--outname=TT_Mtt-1000toInf_scaleup_',
    '--outname=TT_Mtt-1000toInf_scaledown_'
]

#oddeven = [ '', '--oddeven=1', '--oddeven=2' ]
#name_oddeven = [ '', '_odd', '_even' ]
oddeven = [ '' ]
name_oddeven = [ '' ]


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
			s = [ 'python', 'runTruth.py', samples[isample], oddeven[ioe], outname[isample]+"fullTruth"+name_oddeven[ioe] ]
			if isample==0:
				s.append('--mttGenMax=700.')
				s.append('--pileup=ttbarQ2up')
			elif isample==1:
				s.append('--mttGenMax=700.')
				s.append('--pileup=ttbarQ2dn')
			else: 
				s.append('--pileup=ttbar')
			q.put(s)    
    q.join()


print "Starting running threads ..."
run_threads( samples )
print "... all done with running threads!!"

