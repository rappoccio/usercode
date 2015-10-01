#!/usr/bin/env python

import time
import Queue
import subprocess
import threading

class SystVar :
    def __init__(self,name,flags) :
        self.name = name
        self.flags = flags

class Sample :
    def __init__(self, directory, title, noms=True, jersys=True, jecsys=True, pdfsys=True, btagsys=False, toptagsys=False, qcd=False, pu='ttbar', newiso=True, flags='' ) :
        self.directory=directory

        if newiso :
            self.title=title+'_2Dcut'
        else : 
            self.title=title
		
        if flags != '' : 
            self.flags=flags.split(' ')
        else :
            self.flags = []
        self.systs = []
        if pu is not None :
            self.flags.append('--pileup=' + pu )
        if newiso :
            self.flags.append('--use2Dcut')
        
        if jersys is not None :
            self.jerflag = ['--jerSys=0.1']
        else :
            self.jerflag = []
            
        nom = [
            SystVar(name='_nom', flags=self.flags + self.jerflag)
            ]
        qcds = [
            SystVar(name='_qcd', flags=['--doQCD'] + self.flags + self.jerflag)
            ]
        jersysts = [
            SystVar(name='_jerup', flags=['--jerSys=0.2']+self.flags),
            SystVar(name='_jerdn', flags=['--jerSys=0.0']+self.flags)
            ]
        jecsysts = [
            SystVar(name='_jecup', flags=['--jecSys=1.0']+self.flags + self.jerflag),
            SystVar(name='_jecdn', flags=['--jecSys=-1.0']+self.flags + self.jerflag)
            ]
        pdfsysts = [
            SystVar(name='_pdfup_CT10', flags=['--pdfSys=1.0']+['--pdfSet=0.0']+self.flags + self.jerflag),
            SystVar(name='_pdfdn_CT10', flags=['--pdfSys=-1.0']+['--pdfSet=0.0']+self.flags + self.jerflag),
            SystVar(name='_nom_MSTW',   flags=['--pdfSys=0.0']+['--pdfSet=1.0']+self.flags + self.jerflag),
            SystVar(name='_pdfup_MSTW', flags=['--pdfSys=1.0']+['--pdfSet=1.0']+self.flags + self.jerflag),
            SystVar(name='_pdfdn_MSTW', flags=['--pdfSys=-1.0']+['--pdfSet=1.0']+self.flags + self.jerflag),
            SystVar(name='_nom_NNPDF',   flags=['--pdfSys=0.0']+['--pdfSet=2.0']+self.flags + self.jerflag),
            SystVar(name='_pdfup_NNPDF', flags=['--pdfSys=1.0']+['--pdfSet=2.0']+self.flags + self.jerflag),
            SystVar(name='_pdfdn_NNPDF', flags=['--pdfSys=-1.0']+['--pdfSet=2.0']+self.flags + self.jerflag)
            ]
        btagsysts = [
            SystVar(name='_btagup', flags=['--btagSys=1.0']+self.flags + self.jerflag),
            SystVar(name='_btagdn', flags=['--btagSys=-1.0']+self.flags + self.jerflag)
            ]
        toptagsysts = [
            SystVar(name='_toptagup', flags=['--toptagSys=0.25']+self.flags + self.jerflag),
            SystVar(name='_toptagdn', flags=['--toptagSys=-0.25']+self.flags + self.jerflag),
            SystVar(name='_toptagHIGHPTup', flags=['--toptagSys=0.17']+self.flags + self.jerflag),
            SystVar(name='_toptagHIGHPTdn', flags=['--toptagSys=-0.17']+self.flags + self.jerflag),
            ]

        self.systs = []
        if noms == True :
            self.systs = self.systs + nom
        if qcd == True :
            self.systs = self.systs + qcds      
        if jersys == True :
            self.systs = self.systs + jersysts
        if jecsys == True :
            self.systs = self.systs + jecsysts
        if pdfsys == True :
            self.systs = self.systs + pdfsysts
        if btagsys == True :
            self.systs = self.systs + btagsysts
        if toptagsys == True :
            self.systs = self.systs + toptagsysts


def test( s ) :
    print 'hello from test!'
    print s
    print 'test done!'
    time.sleep(3)

def work( s ) :
    #print 'processing command : '
    #print s
    subprocess.call(s)
    #print 'work done!'


def worker(q):
    while True:
        args = q.get()
        #test(args)
        work(args)
        q.task_done()


def run_threads ( samples ) :
    #print 'running threads'
    q = Queue.Queue()
    num_worker_threads = 8
    #print 'making threads'
    for i in range(num_worker_threads):        
         t = threading.Thread(target=worker, args=(q,))
         t.daemon = True
         t.start()

    #print 'adding samples to queue'
    for sample in samples : 
        for isyst in sample.systs :
            flags = isyst.flags
            s = ['python', './tardir/iheartny_topxs_fwlite.py','--files=' + sample.directory + '/res/*.root', '--outname=' + sample.title + isyst.name, '--condor']            
            for flag in flags :
                s.append(flag)
            #print 'adding to queue : '
            for tok in s :
                print tok + ' ',
            print ''
            #q.put(s)

    #q.join()       # block until all tasks are done


