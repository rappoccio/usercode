#!/usr/bin/env python

import subprocess

cPath = '/pnfs/cms/WAX/11/store/user/skhalil'
cPathM = '/pnfs/cms/WAX/11/store/user/lpcbprime/cjenkins'
cPathJ = '/pnfs/cms/WAX/11/store/user/lpcbprime/jpilot'
cPathS = '/pnfs/cms/WAX/11/store/user/lpcbprime/skhalil'
cPathD = '/pnfs/cms/WAX/11/store/user/lpcbprime/ferencek'
options = [
##     [cPathS+'/BprimeBprimeToBZTWinc_M-450_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/376aa4cf9917fa8e7f6c23b8f1e3c7b4',   'BprimeBprimeToBZTWinc_M-450'],
##     [cPathS+'/BprimeBprimeToBZTWinc_M-500_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/24786706eecc169913d2706f31262db7',   'BprimeBprimeToBZTWinc_M-500'],   
##     [cPathS+'/BprimeBprimeToBZTWinc_M-550_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/ea181689290a33672c58f989b051faf5',   'BprimeBprimeToBZTWinc_M-550'],
##     [cPathS+'/BprimeBprimeToBZTWinc_M-600_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/647f7edc6d96c61beb21c5fcecd4cc64',   'BprimeBprimeToBZTWinc_M-600'],
##     [cPathS+'/BprimeBprimeToBZTWinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/334d2e618096f3382e2c2ee05b150704',   'BprimeBprimeToBZTWinc_M-650'],
##     [cPathS+'/BprimeBprimeToBZTWinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/5b7bb4b885a2426e6a4c2a9e2493a5a9',   'BprimeBprimeToBZTWinc_M-700'],
##     [cPathS+'/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/cb5b720ba47f508c962b1b6dea9fbee3',   'BprimeBprimeToBZTWinc_M-750'],
##     [cPathS+'/BprimeBprimeToBZTWinc_M-800_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/58e5df7bc8fa8c73bfa1e95722c6679a',   'BprimeBprimeToBZTWinc_M-800'],
##     [cPathS+'/BprimeBprimeToBZTWinc_M-850_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/3febcd3249a69f4fa9fa403a0b4d62ff',   'BprimeBprimeToBZTWinc_M-850'],    
##     [cPathS+'/BprimeBprimeToBZTWinc_M-900_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/de5dd64730900378f028b9d64c6669c8',   'BprimeBprimeToBZTWinc_M-900'],
##     [cPathS+'/BprimeBprimeToBZTWinc_M-950_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/de5dd64730900378f028b9d64c6669c8',   'BprimeBprimeToBZTWinc_M-950'],
##     [cPathS+'/BprimeBprimeToBZTWinc_M-1000_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/2534c6d8a0b3aea1dc9c9f62887d7098',  'BprimeBprimeToBZTWinc_M-1000'],
##     [cPathS+'/BprimeBprimeToBZTWinc_M-1100_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/e8674f8b205f6a6d793b1a631bad675f',  'BprimeBprimeToBZTWinc_M-1100'],
##     [cPathS+'/BprimeBprimeToBZTWinc_M-1200_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/8386b3fa18250c945e8402786daf8403',  'BprimeBprimeToBZTWinc_M-1200'],
##     [cPathS+'/BprimeBprimeToBZTWinc_M-1300_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/b59fcc610f94f9a6e96aa3bbc3fec10d',  'BprimeBprimeToBZTWinc_M-1300'],
##     [cPathS+'/BprimeBprimeToBZTWinc_M-1400_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/4205fac5fc797e8d45cc972db558f2fb',  'BprimeBprimeToBZTWinc_M-1400'],
##     [cPathS+'/BprimeBprimeToBZTWinc_M-1500_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/3d61ba3ff2b724a8a5a9909dc2c361f7',  'BprimeBprimeToBZTWinc_M-1500'],
    
##     [cPathS+'/BprimeBprimeToTWTWinc_M-450_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/8bae8b0f4744febb8ef57bbbd93f3dc2',   'BprimeBprimeToTWTWinc_M-450'],
##     [cPathS+'/BprimeBprimeToTWTWinc_M-500_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/45b787f4d0ba8a55a4f06113ea98ce49',   'BprimeBprimeToTWTWinc_M-500'],
##     [cPathS+'/BprimeBprimeToTWTWinc_M-550_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/1ddc385099b2f0138fb65ed205418a99',   'BprimeBprimeToTWTWinc_M-550'],
##     [cPathS+'/BprimeBprimeToTWTWinc_M-600_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/ed28c54e48c0750b60030228bb9fc5fe',   'BprimeBprimeToTWTWinc_M-600'],
##     [cPathS+'/BprimeBprimeToTWTWinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/d64b2893b8d1ded7d23eed68f72e8326',   'BprimeBprimeToTWTWinc_M-650'],
##     [cPathS+'/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/d7d013bc3a5f2c393a21104694a8c881',   'BprimeBprimeToTWTWinc_M-700'],
##     [cPathS+'/BprimeBprimeToTWTWinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/bb0266c8ae7d5e12d35ba92d9cccb76f',   'BprimeBprimeToTWTWinc_M-750'],
##     [cPathS+'/BprimeBprimeToTWTWinc_M-800_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/e715e34d49be77c52dea9940569a1273',   'BprimeBprimeToTWTWinc_M-800'],
##     [cPathS+'/BprimeBprimeToTWTWinc_M-850_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/439d36ec2cba40ef791ad7177e04ccb3',   'BprimeBprimeToTWTWinc_M-850'],
##     [cPathS+'/BprimeBprimeToTWTWinc_M-900_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/11b15cf339194a643f79cd2b951ff25f',   'BprimeBprimeToTWTWinc_M-900'],
##     [cPathS+'/BprimeBprimeToTWTWinc_M-950_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/c18db86cb605f4e1ef2d79a603c82d2e',   'BprimeBprimeToTWTWinc_M-950'],
##     [cPathS+'/BprimeBprimeToTWTWinc_M-1000_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/37138faa7f125773f6c14c28827ac248',  'BprimeBprimeToTWTWinc_M-1000'],
##     [cPathS+'/BprimeBprimeToTWTWinc_M-1100_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/0462354190d13ec3350dbb7c961ed83b',  'BprimeBprimeToTWTWinc_M-1100'],
##     [cPathS+'/BprimeBprimeToTWTWinc_M-1200_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/d32556381a16bbc4163430ef62128d20',  'BprimeBprimeToTWTWinc_M-1200'],
##     [cPathS+'/BprimeBprimeToTWTWinc_M-1300_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/8c2f8cf139a51c252dd3029a3dd8cd1e',  'BprimeBprimeToTWTWinc_M-1300'],
##     [cPathS+'/BprimeBprimeToTWTWinc_M-1400_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/01ca2611ea8383e05e8ee949bcea1265',  'BprimeBprimeToTWTWinc_M-1400'],
##     [cPathS+'/BprimeBprimeToTWTWinc_M-1500_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/178c1ce0c0bfdcf9c6d97dc98dd76e75',  'BprimeBprimeToTWTWinc_M-1500'],

##     [cPathS+'/BprimeBprimeToBHBHinc_M-450_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/c2a7175639d319cead313f7c6ae861e5',   'BprimeBprimeToBHBHinc_M-450'],
##     [cPathS+'/BprimeBprimeToBHBHinc_M-500_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/d701e29b085d32a4f4014495788512cb',   'BprimeBprimeToBHBHinc_M-500'],
##     [cPathS+'/BprimeBprimeToBHBHinc_M-550_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/8233e84567c1598230d40ef4384069f6',   'BprimeBprimeToBHBHinc_M-550'],
##     [cPathS+'/BprimeBprimeToBHBHinc_M-600_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/f66a3523f2144a33bce28669f2467fbf',   'BprimeBprimeToBHBHinc_M-600'],
##     [cPathS+'/BprimeBprimeToBHBHinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/d06917618a3e352fb91b64c78f93ec75',   'BprimeBprimeToBHBHinc_M-650'],
##     [cPathS+'/BprimeBprimeToBHBHinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/d354b545b0934406af388aa20441493f',   'BprimeBprimeToBHBHinc_M-700'],
##     [cPathS+'/BprimeBprimeToBHBHinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/5d07a2350deb409ee6ea4a85e4065148',   'BprimeBprimeToBHBHinc_M-750'],
##     [cPathS+'/BprimeBprimeToBHBHinc_M-800_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/3dd8217c20bfbf923a2c27cf9dc7ff19',   'BprimeBprimeToBHBHinc_M-800'],
     
##     [cPathS+'/BprimeBprimeToBHBZinc_M-450_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/bf996d692ea77a107c70564a15b2082d',   'BprimeBprimeToBHBZinc_M-450'], 
##     [cPathS+'/BprimeBprimeToBHBZinc_M-500_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/c261b7c90e978125e82e84050132fbb7',   'BprimeBprimeToBHBZinc_M-500'],
##     [cPathS+'/BprimeBprimeToBHBZinc_M-550_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/9b518832036dc98f7af434ebb094208a',   'BprimeBprimeToBHBZinc_M-550'],
##     [cPathS+'/BprimeBprimeToBHBZinc_M-600_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/50fe28af95dab26e101ecfd6839649ce',   'BprimeBprimeToBHBZinc_M-600'],
##     [cPathS+'/BprimeBprimeToBHBZinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/2182940a6265f1b955696c0d64ecc706',   'BprimeBprimeToBHBZinc_M-650'],
##     [cPathS+'/BprimeBprimeToBHBZinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/84e4a67b9fb0a4642df31c9c02a2f6e0',   'BprimeBprimeToBHBZinc_M-700'],
##     [cPathS+'/BprimeBprimeToBHBZinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/8e0830fb022dc756e2751c1b338d2f4b',   'BprimeBprimeToBHBZinc_M-750'],
##     [cPathS+'/BprimeBprimeToBHBZinc_M-800_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/2a6036612d73b360553f570f176bea97',   'BprimeBprimeToBHBZinc_M-800'],

##     [cPathS+'/BprimeBprimeToBHTWinc_M-450_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/115895f2264f60f44330f05916d3a574',   'BprimeBprimeToBHTWinc_M-450'],
##     [cPathS+'/BprimeBprimeToBHTWinc_M-500_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/db4f3ef8b8ca1c7b0c5c7612dedaf85b',   'BprimeBprimeToBHTWinc_M-500'],
##     [cPathS+'/BprimeBprimeToBHTWinc_M-550_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/d591a73ac9413ee26e305568f4a089b0',   'BprimeBprimeToBHTWinc_M-550'],
##     [cPathS+'/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/6f21f72358ce2066a7b5b7ee62e21127',   'BprimeBprimeToBHTWinc_M-600'],
##     [cPathS+'/BprimeBprimeToBHTWinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/004c1a75881db4f0bdfbc8b463c4aa8e',   'BprimeBprimeToBHTWinc_M-650'],
##     [cPathS+'/BprimeBprimeToBHTWinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/e523baa4665ceb11a1f046b441185182',   'BprimeBprimeToBHTWinc_M-700'],
##     [cPathS+'/BprimeBprimeToBHTWinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/19a3db3aeda3b83f802f51b61665aa73',   'BprimeBprimeToBHTWinc_M-750'],
##     [cPathS+'/BprimeBprimeToBHTWinc_M-800_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/b14e61c13fd6f1b4599c1fc5a21d6530',   'BprimeBprimeToBHTWinc_M-800'],
##     [cPathS+'/BprimeBprimeToBHTWinc_M-1000_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/db828b6b3a8de17914c0d15248ae6586',  'BprimeBprimeToBHTWinc_M-1000'],
##     [cPathS+'/BprimeBprimeToBHTWinc_M-1100_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/c6650c935cf3eb59f68d4335077d530a',  'BprimeBprimeToBHTWinc_M-1100'],
##     [cPathS+'/BprimeBprimeToBHTWinc_M-1300_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/9058caf9808429b358697f522f3969a3',  'BprimeBprimeToBHTWinc_M-1300'],
##     [cPathS+'/BprimeBprimeToBHTWinc_M-1400_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/25f35a02f368d84d98b119b34b7c3a4a',  'BprimeBprimeToBHTWinc_M-1400'],
      
##     [cPathS+'/BprimeBprimeToBZBZinc_M-450_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/c42f25a0f2b309c500b75c8cb323e018',   'BprimeBprimeToBZBZinc_M-450'],
##     [cPathS+'/BprimeBprimeToBZBZinc_M-500_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/2d426e0cf413338520c5807b6564b68a',   'BprimeBprimeToBZBZinc_M-500'],
##     [cPathS+'/BprimeBprimeToBZBZinc_M-550_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/ec7c90d828f726e8f05b03efd7f09401',   'BprimeBprimeToBZBZinc_M-550'],    
##     [cPathS+'/BprimeBprimeToBZBZinc_M-600_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/06190dd3abcb720121fa5650696fecb3',   'BprimeBprimeToBZBZinc_M-600'],
##     [cPathS+'/BprimeBprimeToBZBZinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/09174f0e6f7bf2bb0c7b7bb60eb1dbfc',   'BprimeBprimeToBZBZinc_M-650'],
##     [cPathS+'/BprimeBprimeToBZBZinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/4753d42bc6afdc931cab505093da4f9e',   'BprimeBprimeToBZBZinc_M-700'],
##     [cPathS+'/BprimeBprimeToBZBZinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/16edc56e9d7e2739626712849f3e878e',   'BprimeBprimeToBZBZinc_M-750'],
##     [cPathS+'/BprimeBprimeToBZBZinc_M-800_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/cbbef6e5c13f41e74564e639c75c2795',   'BprimeBprimeToBZBZinc_M-800'],
##     [cPathS+'/BprimeBprimeToBZBZinc_M-850_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/d3b22a21d14ddb3a28208a679806d7e7',   'BprimeBprimeToBZBZinc_M-850'],
##     [cPathS+'/BprimeBprimeToBZBZinc_M-1000_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/69a920f3de6e30bf180188b6ebf06d81',  'BprimeBprimeToBZBZinc_M-1000'],

##     [cPathD+'/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/BPrimeEDMNtuples_53x_v3/c2c5ab1f900a09372ddd6cdc9816dd24', 'TTJets_MassiveBinDECAY'],
##     [cPathD+'/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/BPrimeEDMNtuples_53x_v3_WJets_v1/7dd843baaf47d9c9e7be7d2189664474',   'WJetsToLNu_v1'],
##     [cPathD+'/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/BPrimeEDMNtuples_53x_v3_WJets_v2/7dd843baaf47d9c9e7be7d2189664474',   'WJetsToLNu_v2'], # --> larger
##     [cPathD+'/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/BPrimeEDMNtuples_53x_v3/6270fef3204d707ea6d8492ed2d85111',       'DYJetsToLL_M-50'],
##     [cPathD+'/T_s-channel_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v3/8a251fbbce5b413c83ac56ba8ace6922',              'T_s-channel'],
##     [cPathD+'/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v3/04a4217f2ba2d94a51cce1ca17e9da5b',           'Tbar_s-channel'],
##     [cPathD+'/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v3/02a17928cfa3f19cdc14030b92ed3110',          'T_tW-channel'],
##     [cPathD+'/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v3/d1ddf57585ff65b8db638ded4a314f6f',       'Tbar_tW-channel'],
##     [cPathD+'/T_t-channel_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v3/660ec975142d9554d2bb5b041a75fe24',              'T_t-channel'],
##     [cPathD+'/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v3/f36b1e8315963f20e9fefd69a7db5ac5',           'Tbar_t-channel'],
##     [cPathD+'/WW_TuneZ2star_8TeV_pythia6_tauola/BPrimeEDMNtuples_53x_v3/78efea8b2d04711ddbcc971deb025fe8',                      'WW'],
##     [cPathD+'/ZZ_TuneZ2star_8TeV_pythia6_tauola/BPrimeEDMNtuples_53x_v3/79e120421446c5064083dfa34af8b69c',                      'ZZ'],
##     [cPathD+'/WZ_TuneZ2star_8TeV_pythia6_tauola/BPrimeEDMNtuples_53x_v3/0d02545e84745b3f2dfbdcd5a8c4b143',                      'WZ'],
##     [cPathD+'/TTWJets_8TeV-madgraph/BPrimeEDMNtuples_53x_v3/852d994bf8ed2a253ef4e3305fef7cff',                                  'TTWJets'],
##     [cPathD+'/TTZJets_8TeV-madgraph_v2/BPrimeEDMNtuples_53x_v3/7bbf6f71a15b0f7aa9aa57f70f23dcdc',                               'TTZJets'],
##     [cPathS+'/TTJets_matchingdown_TuneZ2star_8TeV-madgraph-tauola/BPrimeEDMNtuples_53x_v3/c2c5ab1f900a09372ddd6cdc9816dd24',    'TTJets_matchingdown'],
##     [cPathS+'/TTJets_matchingup_TuneZ2star_8TeV-madgraph-tauola/BPrimeEDMNtuples_53x_v3/c2c5ab1f900a09372ddd6cdc9816dd24',      'TTJets_matchingup'],
##     [cPathS+'/TTJets_scaledown_TuneZ2star_8TeV-madgraph-tauola/BPrimeEDMNtuples_53x_v3/c2c5ab1f900a09372ddd6cdc9816dd24',       'TTJets_scaledown'],
##     [cPathS+'/TTJets_scaleup_TuneZ2star_8TeV-madgraph-tauola/BPrimeEDMNtuples_53x_v3/c2c5ab1f900a09372ddd6cdc9816dd24',         'TTJets_scaleup'],
##     [cPathS+'/TT_CT10_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v3/e4ad015580f4ff8411c7e2bfe62102b9',                  'TTJets_Powheg'],
##     [cPathS+'/TT_8TeV-mcatnlo/BPrimeEDMNtuples_53x_v3/920e08774c123fa1e5bf77dc73fd6158',                                        'TTJets_MCatnlo'],

##      [cPathM+'/QCD_Pt_20_30_BCtoE_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/ffd29c63b5a1f9e80b067685dd610a49',             'BCtoE_2030'],
##      [cPathM+'/QCD_Pt_30_80_BCtoE_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/c8255d2d0832cecfbf79e4f5ef0926c3',             'BCtoE_3080'],
##      [cPathM+'/QCD_Pt_80_170_BCtoE_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/a6aa0b2416b65147a5babc8b1cb3edf9',            'BCtoE_80170'],
##      [cPathM+'/QCD_Pt_170_250_BCtoE_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/2475da4b9f0f8b7789726349ee79d0f8',           'BCtoE_170250'],
##      [cPathM+'/QCD_Pt_250_350_BCtoE_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/1ad78c80da2d57c533ae83f97e4f2f2b',           'BCtoE_250350'],
##      [cPathM+'/QCD_Pt_350_BCtoE_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/11cb661eccb8fbe9decb9d719207a266',               'BCtoE_350Inf'],
##      [cPathM+'/QCD_Pt_20_30_EMEnriched_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/86d3cefa621f6632b6d61795778f103a',        'EMEn_2030'],   
##      [cPathM+'/QCD_Pt_30_80_EMEnriched_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/287f9aa5bf02fbbe520bcd42d138ec4d',        'EMEn_3080'],
##      [cPathM+'/QCD_Pt_80_170_EMEnriched_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/d8aacb9358e4a014397777f0bb6fd44c',       'EMEn_80170'],
##      [cPathM+'/QCD_Pt_170_250_EMEnriched_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/78768ab93cda9eefba39507dcbe6eece',      'EMEn_170250'],
##      [cPathM+'/QCD_Pt_250_350_EMEnriched_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/d513caca50cb4c99ea5254757f460570',      'EMEn_250350'],
##      [cPathM+'/QCD_Pt_350_EMEnriched_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/d6ab52add1988aa4ffe708310785a35c',          'EMEn_350Inf'],
##      [cPathM+'/GJets_HT-200To400_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/9d4dd0dae445118249c26e782131802c',                        'PhoJets_200400'],
##      [cPathM+'/GJets_HT-400ToInf_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/f8b9ac468a52f28ed02d0a7715c166ac',                        'PhoJets_400Inf'],

##      [cPathM+'/QCD_Pt-15to20_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/898d23db7d32216727581e0953a31537',    'MuEn_1520'],
##      [cPathM+'/QCD_Pt-20to30_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/213bae01f95033d17fac112fd9e42a85',    'MuEn2030'],
##      [cPathM+'/QCD_Pt-30to50_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/dcb14c7df95de4b6aa3dc3f8c3b7ebde',    'MuEn3050'],
##      [cPathM+'/QCD_Pt-50to80_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/34119da82148b363b767377e0328382e',    'MuEn5080'],
##      [cPathM+'/QCD_Pt-80to120_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/052e2652d185fd337b7e37b9b578ac28',   'MuEn80120'],
##      [cPathM+'/QCD_Pt-120to170_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/5fb505874ba8962042ac4e4c559fe7ef',  'MuEn120170'],
##      [cPathM+'/QCD_Pt-170to300_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/6c90de453480a2f0813e29c4a2f69fdf',  'MuEn170300'],
##      [cPathM+'/QCD_Pt-300to470_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/8959944491213181ebb434ac6d03e2eb',  'MuEn300470'],
##      [cPathM+'/QCD_Pt-470to600_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/4db2c572925c5dcd84604aa34f1f9c91',  'MuEn470600'],
##      [cPathM+'/QCD_Pt-600to800_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/432083130d5bc32a0a0510cc9246053c',  'MuEn600800'],
##      [cPathM+'/QCD_Pt-800to1000_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/BPrimeEDMNtuples_53x_v2/48295a90a23c63ed86180ba35c26388b', 'MuEn8001000'],
     
####  Data
     
##     [cPath+'/SingleElectron/BPrimeEDMNtuples_53x_v2_Data-Run2012A-13Jul2012-v1/dc4e5f86dc698f8df05464eb1d2fb82f',   'SingleEle-Run2012A-13Jul2012'],
##     [cPath+'/SingleElectron/BPrimeEDMNtuples_53x_v2_Data-Run2012A-06Aug2012-v1/dc4e5f86dc698f8df05464eb1d2fb82f',   'SingleEle-Run2012A-06Aug2012'],
##     [cPath+'/SingleElectron/BPrimeEDMNtuples_53x_v2_Data_Run2012B-13Jul2012-v1/dc4e5f86dc698f8df05464eb1d2fb82f',   'SingleEle-Run2012B-13Jul2012'],
##     [cPath+'/SingleElectron/BPrimeEDMNtuples_53x_v2_Data-Run2012C-24Aug2012-v1/dc4e5f86dc698f8df05464eb1d2fb82f',   'SingleEle-Run2012C-24Aug2012'],
##     [cPathS+'/SingleElectron/BPrimeEDMNtuples_53x_v2_Data-Run2012C-EcalRecover_11Dec2012-v1/dc4e5f86dc698f8df05464eb1d2fb82f', 'SingleEle-Run2012C-EcalRecover_11Dec2012'],
##     [cPath+'/SingleElectron/BPrimeEDMNtuples_53x_v2_Data-Run2012C-PromptReco-v2-a/dc4e5f86dc698f8df05464eb1d2fb82f', 'SingleEle-Run2012C-PromptReco-v2-a'],
##     [cPath+'/SingleElectron/BPrimeEDMNtuples_53x_v2_Data-Run2012C-PromptReco-v2-b/dc4e5f86dc698f8df05464eb1d2fb82f', 'SingleEle-Run2012C-PromptReco-v2-b'],
##     [cPath+'/SingleElectron/BPrimeEDMNtuples_53x_v2_Data-Run2012D-PromptReco-v1-a/dc4e5f86dc698f8df05464eb1d2fb82f', 'SingleEle-Run2012D-PromptReco-v2-a'],
##     [cPath+'/SingleElectron/BPrimeEDMNtuples_53x_v2_Data-Run2012D-PromptReco-v1-b/dc4e5f86dc698f8df05464eb1d2fb82f', 'SingleEle-Run2012D-PromptReco-v2-b'],

##     [cPathJ+'/SingleMu/BPrimeEDMNtuples_53x_v2_Data-Run2012A-13Jul2012-v1/dc4e5f86dc698f8df05464eb1d2fb82f',   'SingleMu-Run2012A-13Jul2012'],
##     [cPathJ+'/SingleMu/BPrimeEDMNtuples_53x_v2_Data-Run2012A-06Aug2012-v1/dc4e5f86dc698f8df05464eb1d2fb82f',   'SingleMu-Run2012A-06Aug2012'],
##     [cPathJ+'/SingleMu/BPrimeEDMNtuples_53x_v2_Data-Run2012B-13Jul2012-v1/dc4e5f86dc698f8df05464eb1d2fb82f',   'SingleMu-Run2012B-13Jul2012'],
##     [cPathJ+'/SingleMu/BPrimeEDMNtuples_53x_v2_Data-Run2012C-24Aug2012-v1/dc4e5f86dc698f8df05464eb1d2fb82f',   'SingleMu-Run2012C-24Aug2012'],
##     [cPathJ+'/SingleMu/BPrimeEDMNtuples_53x_v2_Data-Run2012C-PromptReco-v2-a/dc4e5f86dc698f8df05464eb1d2fb82f',   'SingleMu-Run2012C-PromptReco-v2-a'],
##     [cPathJ+'/SingleMu/BPrimeEDMNtuples_53x_v2_Data-Run2012C-PromptReco-v2-b/dc4e5f86dc698f8df05464eb1d2fb82f',   'SingleMu-Run2012C-PromptReco-v2-b'],
##     [cPathJ+'/SingleMu/BPrimeEDMNtuples_53x_v2_Data-Run2012C-PromptReco-v2-c/dc4e5f86dc698f8df05464eb1d2fb82f',   'SingleMu-Run2012C-PromptReco-v2-c'],
##     [cPathJ+'/SingleMu/BPrimeEDMNtuples_53x_v2_Data-Run2012D-PromptReco-v1/dc4e5f86dc698f8df05464eb1d2fb82f',     'SingleMu-Run2012D-PromptReco-v1'],
##     [cPathJ+'/SingleMu/BPrimeEDMNtuples_53x_v2_Data-Run2012D-PromptReco-v1-ex1/dc4e5f86dc698f8df05464eb1d2fb82f', 'SingleMu-Run2012D-PromptReco-v1-ex1'],
##     [cPathJ+'/SingleMu/BPrimeEDMNtuples_53x_v2_Data-Run2012D-PromptReco-v1-ex2/dc4e5f86dc698f8df05464eb1d2fb82f', 'SingleMu-Run2012D-PromptReco-v1-ex2'],
    ]
command = 'python listFiles.py --path={0:s} --outputText={1:s} '

for option in options :
    
    s = command.format(option[0], option[1])
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    subprocess.call( ["echo %s"%s,""], shell=True)
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    
    subprocess.call( [s, ""], shell=True )
    
