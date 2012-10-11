#!/usr/bin/env python

import subprocess

cPath = '/pnfs/cms/WAX/11/store/user/lpctlbsm/skhalil'
options = [
    [cPath+'/BprimeBprimeToTWTWinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v1_sv1/492787f5dd5ca403ce99ce9536ef4dbc',   'BprimeBprimeToTWTWinc_M-650'],
    [cPath+'/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v1_sv1/492787f5dd5ca403ce99ce9536ef4dbc',   'BprimeBprimeToTWTWinc_M-700'],
    [cPath+'/BprimeBprimeToTWTWinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v1_sv1/492787f5dd5ca403ce99ce9536ef4dbc',   'BprimeBprimeToTWTWinc_M-750'],
    [cPath+'/BprimeBprimeToBZTWinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v1_sv1/492787f5dd5ca403ce99ce9536ef4dbc',   'BprimeBprimeToBZTWinc_M-700'],
    [cPath+'/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v1_sv1/492787f5dd5ca403ce99ce9536ef4dbc',   'BprimeBprimeToBZTWinc_M-750'],
    [cPath+'/BprimeBprimeToBZTWinc_M-600_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v1_sv1/492787f5dd5ca403ce99ce9536ef4dbc',   'BprimeBprimeToBZTWinc_M-600'],
    [cPath+'/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/BPrimeEDMNtuples_53x_v1/ae567d5fa2b1517ba8c8f2c9b67b3086',     'TTJets_MassiveBinDECAY'],
    [cPath+'/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/BPrimeEDMNtuples_53x_v1/ae567d5fa2b1517ba8c8f2c9b67b3086',                'WJetsToLNu'], 
    [cPath+'/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/BPrimeEDMNtuples_53x_v1/645894227ab69f2885b12f7678dad1aa',           'DYJetsToLL_M-50'],
    [cPath+'/T_s-channel_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v1/ae567d5fa2b1517ba8c8f2c9b67b3086',                  'T_s-channel'],
    [cPath+'/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v1/ae567d5fa2b1517ba8c8f2c9b67b3086',               'Tbar_s-channel'],
    [cPath+'/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v1/ae567d5fa2b1517ba8c8f2c9b67b3086',              'T_tW-channel'],
    [cPath+'/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v1/ae567d5fa2b1517ba8c8f2c9b67b3086',           'Tbar_tW-channel'],
    [cPath+'/T_t-channel_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v1/ae567d5fa2b1517ba8c8f2c9b67b3086',                  'T_t-channel'],
    [cPath+'/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v1/ae567d5fa2b1517ba8c8f2c9b67b3086',               'Tbar_t-channel'],
    [cPath+'/WW_TuneZ2star_8TeV_pythia6_tauola/BPrimeEDMNtuples_53x_v1/ae567d5fa2b1517ba8c8f2c9b67b3086',                          'WW'],
    [cPath+'/WZ_TuneZ2star_8TeV_pythia6_tauola/BPrimeEDMNtuples_53x_v1/ae567d5fa2b1517ba8c8f2c9b67b3086',                          'WZ'],
    ]
command = 'python listFiles.py --path={0:s} --outputText={1:s} '

for option in options :
    
    s = command.format(option[0], option[1])
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    subprocess.call( ["echo %s"%s,""], shell=True)
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    
    subprocess.call( [s, ""], shell=True )
    
