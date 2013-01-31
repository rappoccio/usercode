#!/usr/bin/env python

import subprocess

cPath = '/pnfs/cms/WAX/11/store/user/skhalil'
cPathJ = '/pnfs/cms/WAX/11/store/user/lpcbprime/jpilot'
cPathS = '/pnfs/cms/WAX/11/store/user/lpcbprime/skhalil'
cPathD = '/pnfs/cms/WAX/11/store/user/lpcbprime/ferencek'
options = [
##     [cPath+'/BprimeBprimeToBZTWinc_M-450_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/81c515bb3ba941d81613a6031becc124',   'BprimeBprimeToBZTWinc_M-450'],
##     [cPathS+'/BprimeBprimeToBZTWinc_M-500_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/c6cb597af9b901690330439a4e6cbe3a',   'BprimeBprimeToBZTWinc_M-500'],
##     [cPathS+'/BprimeBprimeToBZTWinc_M-550_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/72a8a8dffdf116dbed4357cceb0363c7',   'BprimeBprimeToBZTWinc_M-550'],
##     [cPath+'/BprimeBprimeToBZTWinc_M-600_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/55f8bf054f546bfb8d18ad9ef5b81bfb',   'BprimeBprimeToBZTWinc_M-600'],
##     [cPath+'/BprimeBprimeToBZTWinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/74a5b2b102698135d90f1e84df0801b7',   'BprimeBprimeToBZTWinc_M-650'],
##     [cPath+'/BprimeBprimeToBZTWinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/bc06182ad53b318e1651fd80cc261483',   'BprimeBprimeToBZTWinc_M-700'],
##     [cPath+'/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/47143013b632f321ead196aabb8189dc',   'BprimeBprimeToBZTWinc_M-750'],
##     [cPath+'/BprimeBprimeToBZTWinc_M-800_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/7429925751dbbedcde5ea55d633f9a95',   'BprimeBprimeToBZTWinc_M-800'],
    
##     [cPath+'/BprimeBprimeToTWTWinc_M-450_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/531c64b820f0cc09b1d188cdbea67ab2',   'BprimeBprimeToTWTWinc_M-450'],
##     [cPathS+'/BprimeBprimeToTWTWinc_M-500_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/a04087c2ce7d8acc42cba2526a47d4a2',   'BprimeBprimeToTWTWinc_M-500'],
##     [cPath+'/BprimeBprimeToTWTWinc_M-550_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/8a8ea425e0ea2c05b9d8d19e39e07236',   'BprimeBprimeToTWTWinc_M-550'],
##     [cPathS+'/BprimeBprimeToTWTWinc_M-600_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/4158ce30cc49d6d23b5df7e8d0e92a01',   'BprimeBprimeToTWTWinc_M-600'],
##     [cPath+'/BprimeBprimeToTWTWinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/3e633d763e19f4195ad7fc4401f5f7ba',   'BprimeBprimeToTWTWinc_M-650'],
##     [cPath+'/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/e5cbe08ff21c1bb34cff5523590ad32e',   'BprimeBprimeToTWTWinc_M-700'],
##     [cPath+'/BprimeBprimeToTWTWinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/cc404f459c840327c49d683abad4594a',   'BprimeBprimeToTWTWinc_M-750'],
##     [cPath+'/BprimeBprimeToTWTWinc_M-800_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/9512fed6c3fcbe6ce6c8485515408b06',   'BprimeBprimeToTWTWinc_M-800'],

##     [cPath+'/BprimeBprimeToBHBHinc_M-450_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/1023895cf1c183a8e404800d83af6aec',   'BprimeBprimeToBHBHinc_M-450'],
##     [cPath+'/BprimeBprimeToBHBHinc_M-500_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/9344b51bc8b14c6a1de0090cf5caf06a',   'BprimeBprimeToBHBHinc_M-500'],
##     [cPath+'/BprimeBprimeToBHBHinc_M-550_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/7fecc29029f00d0613341d500784776d',   'BprimeBprimeToBHBHinc_M-550'],
##     [cPath+'/BprimeBprimeToBHBHinc_M-600_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/54feee78bd05307ccf5aea8e20a2a1a1',   'BprimeBprimeToBHBHinc_M-600'],
##     [cPath+'/BprimeBprimeToBHBHinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/412242fd8684f008bca92211e891d8f8',   'BprimeBprimeToBHBHinc_M-650'],
##     [cPath+'/BprimeBprimeToBHBHinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/c4c82f52aa327ea5831d26cd16d578de',   'BprimeBprimeToBHBHinc_M-700'],
##     [cPath+'/BprimeBprimeToBHBHinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/de98865bbc651ef98756b1e0e6b63c79',   'BprimeBprimeToBHBHinc_M-750'],
##     [cPath+'/BprimeBprimeToBHBHinc_M-800_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/9f8ce7b056d7d4b0e13df24a578960a3',   'BprimeBprimeToBHBHinc_M-800'],
     
##     [cPathS+'/BprimeBprimeToBHBZinc_M-450_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/e2cf59d73a6f36695d1df3a52b4466e8',   'BprimeBprimeToBHBZinc_M-450'], 
##     [cPath+'/BprimeBprimeToBHBZinc_M-500_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/01a2d59e0ecd05827bdbca3ae0451d18',   'BprimeBprimeToBHBZinc_M-500'],
##     [cPath+'/BprimeBprimeToBHBZinc_M-550_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/731e6c988d1f45644e247c9d13b8d69e',   'BprimeBprimeToBHBZinc_M-550'],
##     [cPath+'/BprimeBprimeToBHBZinc_M-600_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/0d35bdcc49b5fc28891594607a0c5f70',   'BprimeBprimeToBHBZinc_M-600'],
##     [cPath+'/BprimeBprimeToBHBZinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/899f6d1955d66b577524302bce05ab46',   'BprimeBprimeToBHBZinc_M-650'],
##     [cPath+'/BprimeBprimeToBHBZinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/fc4df9a37cb046daacc73b1aad43e9de',   'BprimeBprimeToBHBZinc_M-700'],
##     [cPath+'/BprimeBprimeToBHBZinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/4b72590e71f0f7e0ff5a21cbc7abacb2',   'BprimeBprimeToBHBZinc_M-750'],
##     [cPath+'/BprimeBprimeToBHBZinc_M-800_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/43521b7fbb7e964fa227217527f8e6c1',   'BprimeBprimeToBHBZinc_M-800'],

##     [cPathS+'/BprimeBprimeToBHTWinc_M-450_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/ed7c66972bee6168ad4518c258864e30',   'BprimeBprimeToBHTWinc_M-450'],
##     [cPathS+'/BprimeBprimeToBHTWinc_M-500_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/447c3fbe218a964faf3b31e23d3f94c9',   'BprimeBprimeToBHTWinc_M-500'],
##     [cPathS+'/BprimeBprimeToBHTWinc_M-550_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/3e7bec871040943896af9b735f6ea43d',   'BprimeBprimeToBHTWinc_M-550'],
##     [cPath+'/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/746cec6cce824ae8182046a1620ecfd7',   'BprimeBprimeToBHTWinc_M-600'],
##     [cPath+'/BprimeBprimeToBHTWinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/28df7b815588e5198b45b3380b488bda',   'BprimeBprimeToBHTWinc_M-650'],
##     [cPath+'/BprimeBprimeToBHTWinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/ba301cbed36d6f7956290e30d8080bf6',   'BprimeBprimeToBHTWinc_M-700'],
##     [cPath+'/BprimeBprimeToBHTWinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/fec9ad97939861bb0c7c2cbbfc8cdcb0',   'BprimeBprimeToBHTWinc_M-750'],
##     [cPath+'/BprimeBprimeToBHTWinc_M-800_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/e1d25a379a95e79fb6533cb42a5ca12c',   'BprimeBprimeToBHTWinc_M-800'],
      
##     [cPath+'/BprimeBprimeToBZBZinc_M-450_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/ce3fd64a5c2dc7d35af06807c792b6ab',   'BprimeBprimeToBZBZinc_M-450'],
##     [cPath+'/BprimeBprimeToBZBZinc_M-550_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/23da2a7f39cbdf2e02b94e9a37d7ab9a',   'BprimeBprimeToBZBZinc_M-550'],
##     [cPath+'/BprimeBprimeToBZBZinc_M-600_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/d130027865fb26480084abb18440a984',   'BprimeBprimeToBZBZinc_M-600'],
##     [cPath+'/BprimeBprimeToBZBZinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/79dcc9bce8ef862ae699f9b90d336fc9',   'BprimeBprimeToBZBZinc_M-650'],
##     [cPath+'/BprimeBprimeToBZBZinc_M-700_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/1acc973c103c2e6fceda993669a44e08',   'BprimeBprimeToBZBZinc_M-700'],
##     [cPath+'/BprimeBprimeToBZBZinc_M-750_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/babd1e461009d466019ac2099de841f9',   'BprimeBprimeToBZBZinc_M-750'],
##     [cPath+'/BprimeBprimeToBZBZinc_M-800_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/bc3b6a2bea622a043c1bda1f27804c90',   'BprimeBprimeToBZBZinc_M-800'],

##     [cPathD+'/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/BPrimeEDMNtuples_53x_v2/ec1c239d99fddd6d785510b07dffd792', 'TTJets_MassiveBinDECAY'],
##     [cPathD+'/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/BPrimeEDMNtuples_53x_v2_WJets_v1/4f18779f39088c3556ae38684539fbcb',   'WJetsToLNu_v1'],
##     [cPathD+'/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/BPrimeEDMNtuples_53x_v2_WJets_v2/4f18779f39088c3556ae38684539fbcb',   'WJetsToLNu_v2'], # --> larger WJetsToLNu sample
##     [cPathD+'/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/BPrimeEDMNtuples_53x_v2/8a7e7657419d784980345f4f65dc2787',       'DYJetsToLL_M-50'],
##     [cPathD+'/T_s-channel_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v2/05fe4489ec218c7e7eda3670ab0e3a2e',              'T_s-channel'],
##     [cPathD+'/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v2/6582dbff37393b560667b91dda8dbb46',           'Tbar_s-channel'],
##     [cPathD+'/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v2/4e2c23330ba04eb477c5945d8aca94c3',          'T_tW-channel'],
##     [cPathD+'/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v2/6d8d23131337b1557ae7023ac6a235fe',       'Tbar_tW-channel'],
##     [cPathD+'/T_t-channel_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v2/6078a1cf4faf7730d23164de790801e9',              'T_t-channel'],
##     [cPathD+'/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/BPrimeEDMNtuples_53x_v2/7fa7e5dea2fea35dee5cce30e0700ecf',           'Tbar_t-channel'],
##     [cPathD+'/WW_TuneZ2star_8TeV_pythia6_tauola/BPrimeEDMNtuples_53x_v2/de74174e9a7fde15a7430d7e1cf8067b',                      'WW'],
##     [cPathD+'/ZZ_TuneZ2star_8TeV_pythia6_tauola/BPrimeEDMNtuples_53x_v2/cee07b73d31b64d945d1b37f2d1588c6',                      'ZZ'],
##     [cPathS+'/WZ_TuneZ2star_8TeV_pythia6_tauola/BPrimeEDMNtuples_53x_v2/0b0405642bd7425bf8086d4a8a777caf',                      'WZ'],

##     [cPathD+'/TTWJets_8TeV-madgraph/BPrimeEDMNtuples_53x_v2/5c59c72b540b108688e338ba6cfe657f',                                  'TTWJets'],
##     [cPathD+'/TTZJets_8TeV-madgraph_v2/BPrimeEDMNtuples_53x_v2/c88fd9005cbc44d80d207f75a57e1f21',                               'TTZJets'],
##     [cPathD+'/TTJets_matchingdown_TuneZ2star_8TeV-madgraph-tauola/BPrimeEDMNtuples_53x_v2/ec1c239d99fddd6d785510b07dffd792',    'TTJets_matchingdown'],
##     [cPathD+'/TTJets_matchingup_TuneZ2star_8TeV-madgraph-tauola/BPrimeEDMNtuples_53x_v2/ec1c239d99fddd6d785510b07dffd792',      'TTJets_matchingup'],
##     [cPathD+'/TTJets_scaledown_TuneZ2star_8TeV-madgraph-tauola/BPrimeEDMNtuples_53x_v2/ec1c239d99fddd6d785510b07dffd792',       'TTJets_scaledown'],
##     [cPathD+'/TTJets_scaleup_TuneZ2star_8TeV-madgraph-tauola/BPrimeEDMNtuples_53x_v2/ec1c239d99fddd6d785510b07dffd792',         'TTJets_scaleup'],

##     [cPath+'/SingleElectron/BPrimeEDMNtuples_53x_v2_Data-Run2012A-13Jul2012-v1/dc4e5f86dc698f8df05464eb1d2fb82f',   'SingleEle-Run2012A-13Jul2012'],
##     [cPath+'/SingleElectron/BPrimeEDMNtuples_53x_v2_Data-Run2012A-06Aug2012-v1/dc4e5f86dc698f8df05464eb1d2fb82f',   'SingleEle-Run2012A-06Aug2012'],
##     [cPath+'/SingleElectron/BPrimeEDMNtuples_53x_v2_Data_Run2012B-13Jul2012-v1/dc4e5f86dc698f8df05464eb1d2fb82f',   'SingleEle-Run2012B-13Jul2012'],
##     [cPath+'/SingleElectron/BPrimeEDMNtuples_53x_v2_Data-Run2012C-24Aug2012-v1/dc4e5f86dc698f8df05464eb1d2fb82f',   'SingleEle-Run2012C-24Aug2012'],
##     [cPath+'/SingleElectron/BPrimeEDMNtuples_53x_v2_Data-Run2012C-PromptReco-v2-a/dc4e5f86dc698f8df05464eb1d2fb82f', 'SingleEle-Run2012C-PromptReco-v2-a'],
##     [cPath+'/SingleElectron/BPrimeEDMNtuples_53x_v2_Data-Run2012C-PromptReco-v2-b/dc4e5f86dc698f8df05464eb1d2fb82f', 'SingleEle-Run2012C-PromptReco-v2-b'],
##     [cPath+'/SingleElectron/BPrimeEDMNtuples_53x_v2_Data-Run2012D-PromptReco-v1-a/dc4e5f86dc698f8df05464eb1d2fb82f', 'SingleEle-Run2012D-PromptReco-v2-a'],
##     [cPath+'/SingleElectron/BPrimeEDMNtuples_53x_v2_Data-Run2012D-PromptReco-v1-b/dc4e5f86dc698f8df05464eb1d2fb82f', 'SingleEle-Run2012D-PromptReco-v2-b'],

      [cPathJ+'/SingleMu/BPrimeEDMNtuples_53x_v2_Data-Run2012A-13Jul2012-v1/dc4e5f86dc698f8df05464eb1d2fb82f',   'SingleMu-Run2012A-13Jul2012'],
      [cPathJ+'/SingleMu/BPrimeEDMNtuples_53x_v2_Data-Run2012A-06Aug2012-v1/dc4e5f86dc698f8df05464eb1d2fb82f',   'SingleMu-Run2012A-06Aug2012'],
      [cPathJ+'/SingleMu/BPrimeEDMNtuples_53x_v2_Data-Run2012B-13Jul2012-v1/dc4e5f86dc698f8df05464eb1d2fb82f',   'SingleMu-Run2012B-13Jul2012'],
      [cPathJ+'/SingleMu/BPrimeEDMNtuples_53x_v2_Data-Run2012C-24Aug2012-v1/dc4e5f86dc698f8df05464eb1d2fb82f',   'SingleMu-Run2012C-24Aug2012'],
      [cPathJ+'/SingleMu/BPrimeEDMNtuples_53x_v2_Data-Run2012C-PromptReco-v2-a/dc4e5f86dc698f8df05464eb1d2fb82f',   'SingleMu-Run2012C-PromptReco-v2-a'],
      [cPathJ+'/SingleMu/BPrimeEDMNtuples_53x_v2_Data-Run2012C-PromptReco-v2-b/dc4e5f86dc698f8df05464eb1d2fb82f',   'SingleMu-Run2012C-PromptReco-v2-b'],
      [cPathJ+'/SingleMu/BPrimeEDMNtuples_53x_v2_Data-Run2012C-PromptReco-v2-c/dc4e5f86dc698f8df05464eb1d2fb82f',   'SingleMu-Run2012C-PromptReco-v2-c'],
      [cPathJ+'/SingleMu/BPrimeEDMNtuples_53x_v2_Data-Run2012D-PromptReco-v1/dc4e5f86dc698f8df05464eb1d2fb82f',     'SingleEle-Run2012D-PromptReco-v1'],
      [cPathJ+'/SingleMu/BPrimeEDMNtuples_53x_v2_Data-Run2012D-PromptReco-v1-ex1/dc4e5f86dc698f8df05464eb1d2fb82f', 'SingleEle-Run2012D-PromptReco-v1-ex1'],
      [cPathJ+'/SingleMu/BPrimeEDMNtuples_53x_v2_Data-Run2012D-PromptReco-v1-ex2/dc4e5f86dc698f8df05464eb1d2fb82f', 'SingleEle-Run2012D-PromptReco-v1-ex2'],
    ]
command = 'python listFiles.py --path={0:s} --outputText={1:s} '

for option in options :
    
    s = command.format(option[0], option[1])
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    subprocess.call( ["echo %s"%s,""], shell=True)
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    
    subprocess.call( [s, ""], shell=True )
    
