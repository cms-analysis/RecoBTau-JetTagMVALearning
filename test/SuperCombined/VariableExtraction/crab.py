from CRABClient.UserUtilities import config
config = config()

#config.General.requestName = 'cMVA_default_filterOn'
#config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'VariableExtractor_cMVA_cfg.py'
config.JobType.outputFiles = ['combinedMVA_B.root','combinedMVA_C.root','combinedMVA_D.root','combinedMVA_U.root','combinedMVA_S.root','combinedMVA_G.root']
#config.JobType.inputFiles = ['myLatestTraining.db']

config.Data.inputDataset = '/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.totalUnits = 120
config.Data.outLFN = '/store/user/pvmulder/Trees_cMVA_740pre8/cMVA_default_filterOn_fix/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_Phys14DR-PU20bx25_PHYS14_25_V1-v1_AODSIM/'
config.Data.publication = False
config.Data.publishDataName = 'cMVA_default_filterOn'
#config.Data.ignoreLocality = True # if true better to provide a whitelist of sites physically close to where the input sample is to reduce latency

config.Site.storageSite = 'T2_BE_IIHE'
#config.Site.whitelist = ['T2_CH_CERN','T2_IT_Bari']

config.User.voGroup = 'becms'
