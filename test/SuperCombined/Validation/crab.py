from CRABClient.UserUtilities import config
config = config()

#config.General.requestName = 'cMVA'
#config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'reco_validationfirststep_cMVA_cfg.py'
#config.JobType.outputFiles = ['combinedMVA_B.root','combinedMVA_C.root','combinedMVA_D.root','combinedMVA_U.root','combinedMVA_S.root','combinedMVA_G.root']
config.JobType.inputFiles = ['MVAJetTags_newCMVA.db']

#config.Data.inputDataset = '/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM'
config.Data.inputDataset = '/QCD_HT-100To250_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM'
#config.Data.inputDataset = '/VBF_HToBB_M-125_13TeV-powheg-pythia6/Phys14DR-PU40bx25_PHYS14_25_V1-v1/AODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.totalUnits = 10
#config.Data.outLFN = '/store/user/pvmulder/Validation_cMVA_740pre8/cMVA_default_filterOn_fix_CSVv2IVF/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_Phys14DR-PU20bx25_PHYS14_25_V1-v1_AODSIM/'
config.Data.outLFN = '/store/user/pvmulder/Validation_cMVA_740pre8/cMVA_default_filterOn_fix_CSVv2IVF/QCD_HT-100To250_13TeV-madgraph_Phys14DR-PU20bx25_PHYS14_25_V1-v1_AODSIM/'
#config.Data.outLFN = '/store/user/pvmulder/Validation_cMVA_740pre8/cMVA_default_filterOn_fix_CSVv2IVF/VBF_HToBB_M-125_13TeV-powheg-pythia6_Phys14DR-PU40bx25_PHYS14_25_V1-v1_AODSIM/'
config.Data.publication = False
config.Data.publishDataName = 'cMVA'
#config.Data.ignoreLocality = True # if true better to provide a whitelist of sites physically close to where the input sample is to reduce latency

config.Site.storageSite = 'T2_BE_IIHE'
#config.Site.whitelist = ['T2_CH_CERN','T2_IT_Bari']

config.User.voGroup = 'becms'
