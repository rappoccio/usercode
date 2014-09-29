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
    def __init__(self, directory, title, noms=True, jersys=True, jecsys=True, btagsys=False, qcd=False, pu='ttbar', flags='' ) :
        self.directory=directory
        self.title=title
        if flags != '' : 
            self.flags=flags.split(' ')
        else :
            self.flags = []
        self.systs = []
        if pu is not None :
            self.flags.append('--pileup=' + pu )
        if jersys is not None :
            self.jerflag = ['--jerSys=0.1']
        else :
            self.jerflag = []
            
        nom = [
            SystVar(name='_nom', flags=self.flags + self.jerflag)
            ]
        qcds = [
            SystVar(name='_qcd', flags=['--useLoose'] + self.flags + self.jerflag)
            ]
        jersysts = [
            SystVar(name='_jerup', flags=['--jerSys=0.2']+self.flags),
            SystVar(name='_jerdn', flags=['--jerSys=0.0']+self.flags)
            ]
        jecsysts = [
            SystVar(name='_jecup', flags=['--jecSys=1.0']+self.flags + self.jerflag),
            SystVar(name='_jecdn', flags=['--jecSys=-1.0']+self.flags + self.jerflag)
            ]
        btagsysts = [
            SystVar(name='_btagup', flags=['--btagSys=1.0']+self.flags + self.jerflag),
            SystVar(name='_btagdn', flags=['--btagSys=-1.0']+self.flags + self.jerflag)
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
        if btagsys == True :
            self.systs = self.systs + btagsysts


def test( s ) :
    print 'hello from test!'
    print s
    print 'test done!'
    time.sleep(3)

def work( s ) :
    print 'processing command : '
    print s
    subprocess.call(s)
    print 'work done!'


def worker(q):
    while True:
        args = q.get()
        #test(args)
        work(args)
        q.task_done()


def run_threads ( samples ) :
    print 'running threads'
    q = Queue.Queue()
    num_worker_threads = 8
    print 'making threads'
    for i in range(num_worker_threads):        
         t = threading.Thread(target=worker, args=(q,))
         t.daemon = True
         t.start()

    print 'adding samples to queue'
    for sample in samples : 
        for isyst in sample.systs :
            flags = isyst.flags
            s = ['python', 'optimize_topxs.py','--files=' + sample.directory, '--outname=' + sample.title + isyst.name]            
            for flag in flags :
                s.append(flag)
            print 'adding to queue : '
            for tok in s :
                print tok + ' ',
            print ''
            q.put(s)

    q.join()       # block until all tasks are done


