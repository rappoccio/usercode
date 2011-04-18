#! /bin/python

from string import *
import subprocess

from optparse import OptionParser


parser = OptionParser()

parser.add_option('--inputCfg', metavar='C', type='string', action='store',
                  default='crab_dummy_anashyft_ele.cfg',
                  dest='inputCfg',
                  help='input config tag to be used')

parser.add_option('--inputCMSSW', metavar='C', type='string', action='store',
                  default='shyftEDAnalyzer_allsys_ele.py',
                  #default = 'shyftEDAnalyzer_ele.py', #for data:
                  dest='inputCMSSW',
                  help='input CMSSW py to be used')

parser.add_option('--outLabel', metavar='L', type='string', action='store',
                  default='_shyftana_414_v1',
                  dest='outLabel',
                  help='output tag to be used')

(options, args) = parser.parse_args()


crabFileStrs = [
#Central samples
    
['/TTJets_TuneD6T_7TeV-madgraph-tauola/skhalil-shyft_414_v1-c43141acf8ecb16bf2b2a65d482d5d16/USER',              15, 0, 'Top',         1, 1],
['/WJetsToLNu_TuneD6T_7TeV-madgraph-tauola/makouski-shyft_414_v1-4102b2143a05266d07e3ed7d177f56c8/USER',         15, 1, 'Wjets',       1, 1],
['/DYJetsToLL_TuneD6T_M-50_7TeV-madgraph-tauola/skhalil-shyft_414_v1-c43141acf8ecb16bf2b2a65d482d5d16/USER',     15, 1, 'Zjets',       1, 1],
['/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/skhalil-shyft_414_v1-c43141acf8ecb16bf2b2a65d482d5d16/USER',           15, 0, 'SingleTopT',  1, 1],
['/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/skhalil-shyft_414_v1-c43141acf8ecb16bf2b2a65d482d5d16/USER',          15, 0, 'SingleToptW', 1, 1],
['/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/skhalil-shyft_414_v1-c43141acf8ecb16bf2b2a65d482d5d16/USER',           15, 0, 'SingleTopS',  1, 1],
#['/SingleElectron/skhalil-SingleElectron_Run2011A-PromptReco_shyft_414_v1-6d0f840ee9d905cf3aa2d7f7eaf89508/USER', 20, 0, 'Data',       1, 0],#please change the config

    ]

for crabFileStr in crabFileStrs :
    print '------------------------- Operating on sample ' + crabFileStr[0] + ' ---------------------------'
    f = open(options.inputCfg, 'r')
    instring = f.read()

    # Get the dataset name, without the user-level stuff
    baseList = crabFileStr[0].split('/')

    # baseList contains, e.g. ['', 'TTJets_TuneD6T_7TeV-madgraph-tauola', 'srappocc-shyft_387_v1-806866a699de2045917e2f88bbb597f4', 'USER']
    # so we want baseList[1]
    outname = baseList[1] + options.outLabel
    outlocation = '/uscms_data/d2/skhalil/ShyftTemplates6/'+baseList[1] + options.outLabel
    # now do all of the substitutions
    a0 = instring.replace( 'DUMMY_DATASET', crabFileStr[0] )
    a1 = a0.replace( 'DUMMY_UI_DIR', outlocation)
    a2 = a1.replace( 'DUMMY_NJOBS', str(crabFileStr[1]) )    
    a3 = a2.replace( 'DUMMY_CMSSW', options.inputCMSSW )
    a4 = a3.replace( 'DUMMY_USEFLAVORHISTORY', str(crabFileStr[2]) )
    a5 = a4.replace( 'DUMMY_SAMPLENAMEINPUT', crabFileStr[3] )
    a6 = a5.replace( 'DUMMY_IGNORETRIGGER', str(crabFileStr[4]) )
    a7 = a6.replace( 'DUMMY_ALLSYS', str(crabFileStr[5]) )

    if options.inputCMSSW == 'shyftEDAnalyzer_allsys_ele.py' and baseList[1] != 'SingleElectron':
        a8 = a7.replace( 'lumi_mask=Cert_160404-161312_7TeV_PromptReco_Collisions11_JSON.txt', '')
    elif  options.inputCMSSW == 'shyftEDAnalyzer_ele.py' and baseList[1] == 'SingleElectron':
        a8 = (a7.replace( 'allSys=0', '')).replace('total_number_of_events = -1', 'total_number_of_lumis = -1')
        
    # Dump the contents of the crab config to the screen
    print '------ Config : ------- '
    print a8
    

    # open the output file
    crabName = 'crab_' + outname + '.cfg'
    fout = open( crabName, 'w')
    # write the text to the output file
    fout.write( a8 )
    fout.close()
    print '------ CRAB starting up! ------'
    # now create the job:
    s = 'crab -create -cfg ' + crabName
    print s
    # and submit:
    subprocess.call( [s], shell=True )
    s = 'crab -submit -c ' + outlocation
    print s
    subprocess.call( [s], shell=True )

