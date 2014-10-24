from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'WD_TTJets_MSDecaysCKM'
config.General.workArea = 'crab_TTH_Oct22'
config.General.saveLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/home/joosep/Dropbox/tthbb13/CMSSW/src/TTH/TTHNtupleAnalyzer/python/Main_cfg.py'
#job runtime in minutes
config.JobType.maxjobruntime = 60*47

config.section_("Data")
config.Data.inputDataset = '/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v2/MINIAODSIM'
config.Data.dbsUrl = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.publication = False
#config.Data.publishDbsUrl = 'phys03'
#config.Data.publishDataName = 'tth_ntp_test1'

config.section_("Site")
config.Site.storageSite = "T2_CH_CSCS"
