debug:
	cd $(CMSSW_BASE); scram b -j16 USER_CXXFLAGS="-DEDM_ML_DEBUG"

run_debug:
	cmsRun $(CMSSW_BASE)/python/TTH/TTHNtupleAnalyzer/ConfFile_cfg.py