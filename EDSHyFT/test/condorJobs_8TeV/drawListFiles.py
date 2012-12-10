#!/usr/bin/env python

import subprocess

cPath = '/pnfs/cms/WAX/11/store/user/lpctlbsm/skhalil'
cPathD = '/pnfs/cms/WAX/11/store/user/lpctlbsm/ferencek'
options = [
    [cPath+'/BprimeBprimeToBZTWinc_M-450_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/a7077e606dfe7f7e0f72c4e007d9e6de',   'BprimeBprimeToBZTWinc_M-450'],
    [cPath+'/BprimeBprimeToBZTWinc_M-600_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/4fdda4306321856da59075dad73499e2',   'BprimeBprimeToBZTWinc_M-600'],
    [cPath+'/BprimeBprimeToBZTWinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/7170a863f2542c177d49ed84ed9421bc',   'BprimeBprimeToBZTWinc_M-650'],
    [cPath+'/BprimeBprimeToBZTWinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/ae7a781c7f8dcfce0a9c559f5f6adc18',   'BprimeBprimeToBZTWinc_M-700'],
    [cPath+'/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/fc549314e4436ea2607408950864d3c2',   'BprimeBprimeToBZTWinc_M-750'],
    [cPath+'/BprimeBprimeToBZTWinc_M-800_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/329d9bff9b20d385310905e444bfc40f',   'BprimeBprimeToBZTWinc_M-800'],
    
    [cPath+'/BprimeBprimeToTWTWinc_M-450_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/a3f5134f8319c443f64eda1133b2421d',   'BprimeBprimeToTWTWinc_M-450'],
    [cPath+'/BprimeBprimeToTWTWinc_M-550_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/dadd2e28ea7daa14b7f639e3de5b787c',   'BprimeBprimeToTWTWinc_M-550'],
    [cPath+'/BprimeBprimeToTWTWinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/38141bdc55f30c2c56a9460b720113a3',   'BprimeBprimeToTWTWinc_M-650'],
    [cPath+'/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/12a0b97a21f28e19ea39363dc83c3155',   'BprimeBprimeToTWTWinc_M-700'],
    [cPath+'/BprimeBprimeToTWTWinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/8a6d992a518a728490eba84beef8027f',   'BprimeBprimeToTWTWinc_M-750'],
    [cPath+'/BprimeBprimeToTWTWinc_M-800_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/6bb49829128bd1322a52efe11099e684',   'BprimeBprimeToTWTWinc_M-800'],

    [cPath+'/BprimeBprimeToBHBHinc_M-450_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/a622e26c57dd524ed0d74d32e5063c16',   'BprimeBprimeToBHBHinc_M-450'],
    [cPath+'/BprimeBprimeToBHBHinc_M-500_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/675e002d15487c153afa08c247ddbeaf',   'BprimeBprimeToBHBHinc_M-500'],
    [cPath+'/BprimeBprimeToBHBHinc_M-550_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/69bb89717182ba7e0b50ce4b70992913',   'BprimeBprimeToBHBHinc_M-550'],
    [cPath+'/BprimeBprimeToBHBHinc_M-600_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/1f1b3be02a09dad93178032a7b964131',   'BprimeBprimeToBHBHinc_M-600'],
    [cPath+'/BprimeBprimeToBHBHinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/d03670d46b3fad9d40d94d45e7b356b1',   'BprimeBprimeToBHBHinc_M-650'],
    [cPath+'/BprimeBprimeToBHBHinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/1b898a7bb28957dad69053f7c94a756c',   'BprimeBprimeToBHBHinc_M-700'],
    [cPath+'/BprimeBprimeToBHBHinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/7a0a3539ab0277921bde63df04752f1d',   'BprimeBprimeToBHBHinc_M-750'],
    [cPath+'/BprimeBprimeToBHBHinc_M-800_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/87da84e0cf5e4138b0ff3f0c5898b0d1',   'BprimeBprimeToBHBHinc_M-800'],
      
    [cPath+'/BprimeBprimeToBHBZinc_M-500_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/786e9e06ea38a6d1c9293f60cf24b5d2',   'BprimeBprimeToBHBZinc_M-500'],
    [cPath+'/BprimeBprimeToBHBZinc_M-550_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/0dbb284316a8b4538bf4c3dc1b7cbb08',   'BprimeBprimeToBHBZinc_M-550'],
    [cPath+'/BprimeBprimeToBHBZinc_M-600_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/75696b02bcd0c7a0ce54aef97deae66c',   'BprimeBprimeToBHBZinc_M-600'],
    [cPath+'/BprimeBprimeToBHBZinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/6fa0623370efd56ecc3997b58546a859',   'BprimeBprimeToBHBZinc_M-650'],
    [cPathD+'/BprimeBprimeToBHBZinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/13885fc74ce5e26c20cd20ec08329de3',  'BprimeBprimeToBHBZinc_M-700'],
    [cPath+'/BprimeBprimeToBHBZinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/c3b081bafc7a0460915ae8185939f6a3',   'BprimeBprimeToBHBZinc_M-750'],
    [cPath+'/BprimeBprimeToBHBZinc_M-800_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/ababdb1f14b9bc77734178d90f897553',   'BprimeBprimeToBHBZinc_M-800'],
      
    [cPath+'/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/9ff1e5c2e8036b877055207c7f25004d',   'BprimeBprimeToBHTWinc_M-600'],
    [cPath+'/BprimeBprimeToBHTWinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/326deeff67f8cb8ab2fec2ad0b43b620',   'BprimeBprimeToBHTWinc_M-650'],
    [cPath+'/BprimeBprimeToBHTWinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/72385cd9b2a8f355364130b68d8a2552',   'BprimeBprimeToBHTWinc_M-700'],
    [cPath+'/BprimeBprimeToBHTWinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/c2b25b609ac89ddb767eedf93a7a3ba5',   'BprimeBprimeToBHTWinc_M-750'],
      
    [cPath+'/BprimeBprimeToBZBZinc_M-450_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/4c10daf45939f7ccea2c98c152f20d47',   'BprimeBprimeToBZBZinc_M-450'],
    [cPath+'/BprimeBprimeToBZBZinc_M-550_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/44a9cfe250f01c93e1825cff477e51ad',   'BprimeBprimeToBZBZinc_M-550'],
    [cPath+'/BprimeBprimeToBZBZinc_M-600_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/48e3f1f621b58ffc454e0a09690558da',   'BprimeBprimeToBZBZinc_M-600'],
    [cPath+'/BprimeBprimeToBZBZinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/d2f7a71352d43b06a62b82a6552e8b89',   'BprimeBprimeToBZBZinc_M-650'],
    [cPath+'/BprimeBprimeToBZBZinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/04d2d1de625ad015f11d349fc757a8b0',   'BprimeBprimeToBZBZinc_M-700'],
    [cPath+'/BprimeBprimeToBZBZinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/9e0363da7fed5fbc93182e6fede10d23',   'BprimeBprimeToBZBZinc_M-750'],
    [cPath+'/BprimeBprimeToBZBZinc_M-800_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/b22efc72c80b5827fa284b479f6c1b9c',   'BprimeBprimeToBZBZinc_M-800'],


    [cPathD+'/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/BPrimeEDMNtuples_53x_v2/d95e55af553259cb72fbafcf4f1f2bdb', 'TTJets_MassiveBinDECAY'],
    [cPathD+'/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/BPrimeEDMNtuples_53x_v2/91435b98cf375fbe8c8dcbdc027490d4',            'WJetsToLNu_v1'],
    [cPathD+'/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/BPrimeEDMNtuples_53x_v1_sv1/38eddd5ef342de22cab5bd8e80290480',        'WJetsToLNu_v2'], # --> larger WJetsToLNu sample
    [cPathD+'/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/BPrimeEDMNtuples_53x_v2/e184f426b9e371513ebbcdc43ee13fbe',       'DYJetsToLL_M-50'],
    [cPathD+'/T_s-channel_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v2/b61497b73b34be5cee8bbddb137b5ec0',              'T_s-channel'],
    [cPathD+'/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v2/2784054ec94358360b51d6624df1f6de',           'Tbar_s-channel'],
    [cPathD+'/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v1_sv1/c114355b592a64421cb88659f78c20a0',      'T_tW-channel'],
    [cPathD+'/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v2/76fb3988e2de0ac0f416a197aec31f4b',       'Tbar_tW-channel'],
    [cPathD+'/T_t-channel_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v2/2e77eaf0ef9aaae6b24a793d6a6ce6f9',              'T_t-channel'],
    [cPathD+'/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v2/cbffc5c24f5b2c6f7cd2533f2708fe2f',           'Tbar_t-channel'],
    [cPathD+'/WW_TuneZ2star_8TeV_pythia6_tauola/BPrimeEDMNtuples_53x_v2/9e3f42c8ee3a5f17b7caca37f495d0b6',                      'WW'],
    [cPathD+'/ZZ_TuneZ2star_8TeV_pythia6_tauola/BPrimeEDMNtuples_53x_v2/25781fc03aed6941de2c00608448d699',                      'ZZ'],
    [cPath+'/WZ_TuneZ2star_8TeV_pythia6_tauola/BPrimeEDMNtuples_53x_v2/ae567d5fa2b1517ba8c8f2c9b67b3086',                      'WZ'], # no PAT tuple

    [cPathD+'/TTWJets_8TeV-madgraph/BPrimeEDMNtuples_53x_v1_sv1/1113526d4b87e89003d8033323f9ae66',                              'TTWJets'],
    [cPathD+'/TTZJets_8TeV-madgraph_v2/BPrimeEDMNtuples_53x_v1_sv1/cbbbb92a19d127b8966f23067be98b6a',                           'TTZJets'],
    [cPathD+'/TTJets_matchingdown_TuneZ2star_8TeV-madgraph-tauola/BPrimeEDMNtuples_53x_v2/d95e55af553259cb72fbafcf4f1f2bdb',    'TTJets_matchingdown'],
    [cPathD+'/TTJets_matchingup_TuneZ2star_8TeV-madgraph-tauola/BPrimeEDMNtuples_53x_v1_sv1/7000854d42c24f65de61849943369a7e',  'TTJets_matchingup'],
    [cPathD+'/TTJets_scaledown_TuneZ2star_8TeV-madgraph-tauola/BPrimeEDMNtuples_53x_v1_sv1/7000854d42c24f65de61849943369a7e',   'TTJets_scaledown'],
    [cPathD+'/TTJets_scaleup_TuneZ2star_8TeV-madgraph-tauola/BPrimeEDMNtuples_53x_v2/d95e55af553259cb72fbafcf4f1f2bdb',         'TTJets_scaleup'],

    [cPath+'/SingleElectron/BPrimeEDMNtuples_53x_v2_Data-Run2012A-13Jul2012-v1/275c5fe237cf9316feedf3ccd300c5b0',   'SingleEle-Run2012A-13Jul2012'],
    [cPath+'/SingleElectron/BPrimeEDMNtuples_53x_v2_Data-Run2012A-06Aug2012-v1/275c5fe237cf9316feedf3ccd300c5b0',   'SingleEle-Run2012A-06Aug2012'],
    [cPath+'/SingleElectron/BPrimeEDMNtuples_53x_v2_Data_Run2012B-13Jul2012-v1/275c5fe237cf9316feedf3ccd300c5b0',   'SingleEle-Run2012B-13Jul2012'],
    [cPath+'/SingleElectron/BPrimeEDMNtuples_53x_v2_Data-Run2012C-24Aug2012-v1/275c5fe237cf9316feedf3ccd300c5b0',   'SingleEle-Run2012C-24Aug2012'],
    
    ]
command = 'python listFiles.py --path={0:s} --outputText={1:s} '

for option in options :
    
    s = command.format(option[0], option[1])
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    subprocess.call( ["echo %s"%s,""], shell=True)
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    
    subprocess.call( [s, ""], shell=True )
    
