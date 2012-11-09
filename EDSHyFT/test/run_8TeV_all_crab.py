import subprocess, os, ConfigParser


dummy_config_name = 'crab_dummy_anashyft_ele.cfg'

dummy_config = ConfigParser.RawConfigParser()
dummy_config.read(dummy_config_name)

pset = 'edmNtupleMaker.py'
working_dir = os.environ['HOME'] + '/nobackup/BPrimeEDM_8TeV/Sep24/'
dir_suffix = '_tlbsm_53x_v1_sv2'

# one pset for all jobs
dummy_config.set('CMSSW','pset',pset)

joblist = [
   # ==========  MC ===========
    {'datasetpath':'/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/jpilot-TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola-Summer12_DR53X-PU_S10-fe5dcf8cf2a24180bf030f68a7d97dda/USER',
     'number_of_jobs':'15', 'pycfg_params':'runData=0', '#sample_name': 'Top', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },
    
    {'datasetpath':'/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/StoreResults-Summer12-PU_S7_START52_V9-v1_TLBSM_52x_v5-2bcc6fdd1e664d93e9026c3764d0b403/USER',
    'number_of_jobs':'25', 'pycfg_params':'runData=0', '#sample_name': 'Wjets','dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },
    
    {'datasetpath':'/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/StoreResults-Summer12-PU_S7_START52_V9-v2_TLBSM_52x_v5-2bcc6fdd1e664d93e9026c3764d0b403/USER',
    'number_of_jobs':'100', 'pycfg_params':'runData=0', '#sample_name': 'ZJets','dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },
    
    {'datasetpath':'/T_t-channel_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12-PU_S7_START52_V9-v1_TLBSM_52x_v5-2bcc6fdd1e664d93e9026c3764d0b403/USER',
     'number_of_jobs':'10', 'pycfg_params':'runData=0', '#sample_name': 'SingleTopT','dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },
    
    {'datasetpath':'/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12-PU_S7_START52_V9-v1_TLBSM_52x_v5-2bcc6fdd1e664d93e9026c3764d0b403/USER',
     'number_of_jobs':'10', 'pycfg_params':'runData=0', '#sample_name': 'SingleTopbarT', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },
    
    {'datasetpath':'/T_s-channel_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12-PU_S7_START52_V9-v1_TLBSM_52x_v5-2bcc6fdd1e664d93e9026c3764d0b403/USER',
     'number_of_jobs':'10', 'pycfg_params':'runData=0', '#sample_name': 'SingleTopS', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },
    
    {'datasetpath':'/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12-PU_S7_START52_V9-v1_TLBSM_52x_v5-9d0a7909356b982da78efb4e9a7a51de/USER',
     'number_of_jobs':'10', 'pycfg_params':'runData=0', '#sample_name': 'SingleTopbarS','dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },
    
    {'datasetpath':'/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12-PU_S7_START52_V9-v1_TLBSM_52x_v5-2bcc6fdd1e664d93e9026c3764d0b403/USER',
     'number_of_jobs':'10', 'pycfg_params':'runData=0', '#sample_name': 'SingleToptW','dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },
    
    {'datasetpath':'/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12-PU_S7_START52_V9-v1_TLBSM_52x_v5-2bcc6fdd1e664d93e9026c3764d0b403/USER',
     'number_of_jobs':'10', 'pycfg_params':'runData=0', '#sample_name': 'SingleTopbartW','dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},
    
    {'datasetpath':'/WW_TuneZ2star_8TeV_pythia6_tauola/StoreResults-Summer12-PU_S7_START52_V9-v1_TLBSM_52x_v5-9d0a7909356b982da78efb4e9a7a51de/USER',
     'number_of_jobs':'15', 'pycfg_params':'runData=0', '#sample_name': 'DibosonWW', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },
    
    {'datasetpath':'/WZ_TuneZ2star_8TeV_pythia6_tauola/pturner-Summer12-PU_S7_START52_V9-v1_TLBSM_52x_v5-2bcc6fdd1e664d93e9026c3764d0b403/USER',
     'number_of_jobs':'15', 'pycfg_params':'runData=0', '#sample_name': 'DibosonWZ', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },
    
    {'datasetpath':'/ZZ_TuneZ2star_8TeV_pythia6_tauola/pturner-Summer12-PU_S7_START52_V9-v1_TLBSM_52x_v5-2bcc6fdd1e664d93e9026c3764d0b403/USER',
     'number_of_jobs':'15', 'pycfg_params':'runData=0', '#sample_name': 'DibosonZZ', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

   {'datasetpath':'/BprimeBprimeToTWTWinc_M-450_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M450_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2-fe5dcf8cf2a24180bf030f68a7d97dda/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToTWTW_450', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet'},

    {'datasetpath':'/BprimeBprimeToTWTWinc_M-650_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M650_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2-fe5dcf8cf2a24180bf030f68a7d97dda/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToTWTW_650', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },
    
    {'datasetpath':'/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/skhalil-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1-fe5dcf8cf2a24180bf030f68a7d97dda/USER','number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToTWTW_700', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

    {'datasetpath':'/BprimeBprimeToTWTWinc_M-750_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M750_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2-fe5dcf8cf2a24180bf030f68a7d97dda/USER','number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToTWTW_750', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },
    
    {'datasetpath':'/BprimeBprimeToBZTWinc_M-600_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M600_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2-fe5dcf8cf2a24180bf030f68a7d97dda/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZTW_600', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet'},
    
    {'datasetpath':'/BprimeBprimeToBZTWinc_M-700_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M700_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2-fe5dcf8cf2a24180bf030f68a7d97dda/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZTW_700', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet'},

    {'datasetpath':'/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M750_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2-fe5dcf8cf2a24180bf030f68a7d97dda/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZTW_750', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet'},
    

   # ==========  electron data
    {'datasetpath':'/SingleElectron/StoreResults-Run2012A-PromptReco-v1_TLBSM_52x_v5-37420123b49b4f52358fad22bcc775a4/USER',
     'number_of_jobs':'50', 'pycfg_params':'runData=1','runselection':'190450-193686' ,'lumi_mask':'Cert_190456-203002_8TeV_PromptReco_Collisions12_JSON.txt' ,
     '#sample_name': 'DataA', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},
    
    {'datasetpath':'/SingleElectron/StoreResults-Run2012B1-PromptReco-v1_TLBSM_52x_v5-37420123b49b4f52358fad22bcc775a4/USER',
     'number_of_jobs':'50', 'pycfg_params':'runData=1','runselection':'193752-194678' ,'lumi_mask':'Cert_190456-203002_8TeV_PromptReco_Collisions12_JSON.txt' ,
     '#sample_name': 'DataB1', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},
    
    {'datasetpath':'/SingleElectron/StoreResults-Run2012B2-PromptReco-v1_TLBSM_52x_v5-37420123b49b4f52358fad22bcc775a4/USER',
     'number_of_jobs':'50', 'pycfg_params':'runData=1','runselection':'194679-195604' ,'lumi_mask':'Cert_190456-203002_8TeV_PromptReco_Collisions12_JSON.txt' ,
     '#sample_name': 'DataB2', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},

    {'datasetpath':'/SingleElectron/StoreResults-Run2012B3-PromptReco-v1_TLBSM_52x_v5-37420123b49b4f52358fad22bcc775a4/USER',
     'number_of_jobs':'50', 'pycfg_params':'runData=1','runselection':'195605-196531' ,'lumi_mask':'Cert_190456-203002_8TeV_PromptReco_Collisions12_JSON.txt' ,
     '#sample_name': 'DataB3', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},
    
    {'datasetpath':'/ElectronHad/StoreResults-Run2012A-23May2012-v2_TLBSM_52x_v5-37420123b49b4f52358fad22bcc775a4/USER',
     'number_of_jobs': '20','pycfg_params':'runData=1','runselection':'190782-190949' ,'lumi_mask':'Cert_190456-203002_8TeV_PromptReco_Collisions12_JSON.txt' ,
     '#sample_name': 'DataA1', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},
    
    {'datasetpath':'/ElectronHad/StoreResults-Run2012A-PromptReco-v1_TLBSM_52x_v5-37420123b49b4f52358fad22bcc775a4/USER',
     'number_of_jobs': '80','pycfg_params':'runData=1','runselection':'190450-193686' ,'lumi_mask':'Cert_190456-203002_8TeV_PromptReco_Collisions12_JSON.txt' ,
     '#sample_name': 'DataA2', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},
    
    {'datasetpath':'/ElectronHad/StoreResults-Run2012B-PromptReco-v1_TLBSM_52x_v5-37420123b49b4f52358fad22bcc775a4/USER',
     'number_of_jobs': '400','pycfg_params':'runData=1','runselection':'193752-197044' ,'lumi_mask':'Cert_190456-203002_8TeV_PromptReco_Collisions12_JSON.txt' ,
     '#sample_name': 'DataB', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},
    
    ]

for job in joblist:
    config = dummy_config

    config.set('USER', 'additional_input_files', 'Jec12_V2_L1FastJet_AK5PFchs.txt,Jec12_V2_L2Relative_AK5PFchs.txt,Jec12_V2_L3Absolute_AK5PFchs.txt,Jec12_V2_L2L3Residual_AK5PFchs.txt,Jec12_V2_Uncertainty_AK5PFchs.txt,PUMC_dist_flat10.root,PUData_finebin_dist.root')
 
    # for MC we don't need this
    config.remove_option('CMSSW','runselection')
    config.remove_option('CMSSW','lumi_mask')

    # plug for data
    if 'Data' in job['#sample_name']:
        config.remove_option('CMSSW','total_number_of_events')
        config.set('CMSSW','total_number_of_lumis','-1')
    
    
    for p in job:
        config.set('CMSSW', p, job[p])
 



    if 'Data' not in job['#sample_name']:
        print 'here'
	btagFile_ak5 = job['datasetpath'].split('/')[1] + "_AK5PF_CSVM_bTaggingEfficiencyMap.root"
        btagFile_ca8 = job['datasetpath'].split('/')[1] + "_CA8PrunedPF_CSVM_bTaggingEfficiencyMap.root"
   	config.set('USER', 'additional_input_files', config.get('USER', 'additional_input_files')+','+btagFile_ak5+','+btagFile_ca8)  
	c1 = 'cp ../data/'+btagFile_ak5+' .'
	c2 = 'cp ../data/'+btagFile_ca8+' .'
	subprocess.call( [c1], shell=True)
	subprocess.call( [c2], shell=True)
	config.set('CMSSW', 'pycfg_params', config.get('CMSSW', 'pycfg_params')+" btagMap="+job['datasetpath'].split('/')[1])  



        
    if 'Data' in job['#sample_name'] or 'Bprime' in job['#sample_name']:
        ui_working_dir = working_dir + job['datasetpath'].split('/')[1] + '_' + job['#sample_name'] + dir_suffix
    else:    
        ui_working_dir = working_dir + job['datasetpath'].split('/')[1] + dir_suffix
    config.set('USER','ui_working_dir',ui_working_dir)
    
    # write cfg file and run crab
    cfgname = 'crab_'+job['#sample_name']+'.cfg'
    with open(cfgname, 'wb') as configfile:
        config.write(configfile)
       
    s = 'crab -create -cfg ' + cfgname
    print s
    #subprocess.call( [s], shell=True )

    s = 'crab -submit -c ' + ui_working_dir
    print s
    #subprocess.call( [s], shell=True )

    
    r1 = 'rm '+btagFile_ak5
    r2 = 'rm '+btagFile_ca8
    subprocess.call( [r1], shell=True)
    subprocess.call( [r2], shell=True)


