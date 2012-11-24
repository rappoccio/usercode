#!/usr/bin/env python

import subprocess

cPath = '/pnfs/cms/WAX/11/store/user/lpctlbsm/skhalil'
cPathD = '/pnfs/cms/WAX/11/store/user/lpctlbsm/ferencek'
options = [
##     [cPath+'/BprimeBprimeToBZTWinc_M-450_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/01b8d643d1747e9159cdaa2c64bf68b8',   'BprimeBprimeToBZTWinc_M-450'],
##     [cPath+'/BprimeBprimeToBZTWinc_M-600_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/3c2c4b6bef0371cc74c1a7b2008870f3',   'BprimeBprimeToBZTWinc_M-600'],
##     [cPath+'/BprimeBprimeToBZTWinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/7563d7876e1a15bf9b8679ba1b3da97d',   'BprimeBprimeToBZTWinc_M-650'],
##     [cPath+'/BprimeBprimeToBZTWinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/c52973fd17cd4fa97ca8453fb65bd4bb',   'BprimeBprimeToBZTWinc_M-700'],
##     [cPath+'/BprimeBprimeToBZTWinc_M-800_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/90832cd4d1ba2b4caa47ecf0bd3d4427',   'BprimeBprimeToBZTWinc_M-800'],
##     [cPath+'/BprimeBprimeToTWTWinc_M-450_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/7bf8927a6431e5aefad7af7b77aded3b',   'BprimeBprimeToTWTWinc_M-450'],
##     [cPath+'/BprimeBprimeToTWTWinc_M-550_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/ea4ad54b428dc29e524c10137de170d5',   'BprimeBprimeToTWTWinc_M-550'],
##     [cPath+'/BprimeBprimeToTWTWinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/02895d388b1ea79e62432deaf0604ab7',   'BprimeBprimeToTWTWinc_M-650'],
##     [cPath+'/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/ce6202f7b26fd2baae775ae4de8fa21a',   'BprimeBprimeToTWTWinc_M-700'],
##     #[cPath+'/BprimeBprimeToTWTWinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/ce6202f7b26fd2baae775ae4de8fa21a',   'BprimeBprimeToTWTWinc_M-750'],# no PAT tuple
##     [cPath+'/BprimeBprimeToTWTWinc_M-800_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/77ab2b6b752dfb20b5b7d3bed3a54008',   'BprimeBprimeToTWTWinc_M-800'],
##     [cPath+'/BprimeBprimeToBHBZinc_M-500_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/e0c9d2b3fd71a450a7976751820f2413',   'BprimeBprimeToBHBZinc_M-500'],
##     [cPath+'/BprimeBprimeToBHBZinc_M-550_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/e09b379c51c91341d0ce846afc4b509d',   'BprimeBprimeToBHBZinc_M-550'],
##     [cPath+'/BprimeBprimeToBHBZinc_M-600_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/0701bb8b6fc0451e1f080397a5c5f3a3',   'BprimeBprimeToBHBZinc_M-600'],
##     [cPath+'/BprimeBprimeToBHBZinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/edfd95d1abfbc33d829d66f977730c5f',   'BprimeBprimeToBHBZinc_M-650'],
##     [cPath+'/BprimeBprimeToBHBZinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/9e5624a593d05b2cb22909b7cbf489e4',   'BprimeBprimeToBHBZinc_M-750'],
##     [cPath+'/BprimeBprimeToBHBZinc_M-800_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/28c7fe0813f9e122650f8da72779b9f9',   'BprimeBprimeToBHBZinc_M-800'],
##     [cPath+'/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/fd5e693f0a583445f14e337f6d5fe006',   'BprimeBprimeToBHTWinc_M-600'],
##     [cPath+'/BprimeBprimeToBHTWinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/91f08e542f5234ba0ab5c55ee222b8ce',   'BprimeBprimeToBHTWinc_M-650'],
##     [cPath+'/BprimeBprimeToBHTWinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/84e49ae07b8d008e9bd01b083795bc90',   'BprimeBprimeToBHTWinc_M-700'],
##     [cPath+'/BprimeBprimeToBHTWinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/6f0038f806c6688dcd51146165fe8545',   'BprimeBprimeToBHTWinc_M-750'],
##     [cPath+'/BprimeBprimeToBZBZinc_M-450_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/04196eae6c0ff2a36140a2341889d74a',   'BprimeBprimeToBZBZinc_M-450'],
##     [cPath+'/BprimeBprimeToBZBZinc_M-550_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/a79bc5f4dc7450eac1ac5c05511da999',   'BprimeBprimeToBZBZinc_M-550'],
##     [cPath+'/BprimeBprimeToBZBZinc_M-600_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/c4e944f385240f0d4e4ed9f821a08373',   'BprimeBprimeToBZBZinc_M-600'],
##     [cPath+'/BprimeBprimeToBZBZinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/2bf3529a06e21cb20ebbc8e54b6cbc34',   'BprimeBprimeToBZBZinc_M-650'],
##     [cPath+'/BprimeBprimeToBZBZinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/cb1ba62717d878e006efbfa43d0e9a5f',   'BprimeBprimeToBZBZinc_M-700'],
##     [cPath+'/BprimeBprimeToBZBZinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/77234f1150c8925def5b05c662d4685f',   'BprimeBprimeToBZBZinc_M-750'],
##     [cPath+'/BprimeBprimeToBZBZinc_M-800_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/b0715275d100cd8919ea58ee7708f9ed',   'BprimeBprimeToBZBZinc_M-800'],
    
##     [cPath+'/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/BPrimeEDMNtuples_53x_v2/7000854d42c24f65de61849943369a7e', 'TTJets_MassiveBinDECAY'],
##     [cPath+'/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/BPrimeEDMNtuples_53x_v2/38eddd5ef342de22cab5bd8e80290480',            'WJetsToLNu_v1'],
##     [cPathD+'/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/BPrimeEDMNtuples_53x_v1_sv1/38eddd5ef342de22cab5bd8e80290480',       'WJetsToLNu_v2'], 
##     [cPath+'/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/BPrimeEDMNtuples_53x_v2/a60a0dd9b60ef43d8211bd3e6a37948a',       'DYJetsToLL_M-50'],  
##     [cPath+'/T_s-channel_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v2/c490bef7a116783745a0fc2ba7f5829b',              'T_s-channel'],
##     [cPath+'/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v2/3634d5bfbe2330f532661942ded293f4',           'Tbar_s-channel'],
##     [cPath+'/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v2/c114355b592a64421cb88659f78c20a0',          'T_tW-channel'],
##     [cPath+'/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v2/1108f988efee6a1b56cf8d0589ec1413',       'Tbar_tW-channel'],
##     [cPath+'/T_t-channel_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v2/f6badf5a99a305089a615312bdc01cd8',              'T_t-channel'],     
##     [cPathD+'/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v1_sv1/b2920ed0e9546a75cd957af99944e3fd',      'Tbar_t-channel'],  
##     [cPath+'/WW_TuneZ2star_8TeV_pythia6_tauola/BPrimeEDMNtuples_53x_v2/3eae0fe03c18a4e6b1efa738288ae25a',                      'WW'],
##     [cPath+'/ZZ_TuneZ2star_8TeV_pythia6_tauola/BPrimeEDMNtuples_53x_v2/9e3db7760160cf554941b3d39faaff0f',                      'ZZ'],
##     [cPath+'/WZ_TuneZ2star_8TeV_pythia6_tauola/BPrimeEDMNtuples_53x_v2/ae567d5fa2b1517ba8c8f2c9b67b3086',                      'WZ'], # no PAT tuple
##     [cPathD+'/TTWJets_8TeV-madgraph/BPrimeEDMNtuples_53x_v1_sv1/1113526d4b87e89003d8033323f9ae66',                             'TTWJets'],
##     [cPathD+'/TTZJets_8TeV-madgraph_v2/BPrimeEDMNtuples_53x_v1_sv1/cbbbb92a19d127b8966f23067be98b6a',                          'TTZJets'],
##     #[cPath+'/TTJets_matchingdown_TuneZ2star_8TeV-madgraph-tauola/BPrimeEDMNtuples_53x_v2/7000854d42c24f65de61849943369a7e',     'TTJets_matchingdown'], # missisng 2 files
##     [cPathD+'/TTJets_matchingup_TuneZ2star_8TeV-madgraph-tauola/BPrimeEDMNtuples_53x_v1_sv1/7000854d42c24f65de61849943369a7e',  'TTJets_matchingup'], #--> from Dinko
##     [cPath+'/TTJets_scaledown_TuneZ2star_8TeV-madgraph-tauola/BPrimeEDMNtuples_53x_v2/7000854d42c24f65de61849943369a7e',        'TTJets_scaledown'],
##     [cPath+'/TTJets_scaleup_TuneZ2star_8TeV-madgraph-tauola/BPrimeEDMNtuples_53x_v2/7000854d42c24f65de61849943369a7e',          'TTJets_scaleup'],
    ]
command = 'python listFiles.py --path={0:s} --outputText={1:s} '

for option in options :
    
    s = command.format(option[0], option[1])
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    subprocess.call( ["echo %s"%s,""], shell=True)
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    
    subprocess.call( [s, ""], shell=True )
    
