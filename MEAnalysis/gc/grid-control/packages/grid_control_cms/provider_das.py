from grid_control import QM, utils, DatasetError, RethrowError, datasets
from grid_control.datasets import DataProvider
from provider_cms import CMSProvider
from python_compat import *
from webservice_api import *
import time

# required format: <dataset path>[@<instance>][#<block>]
class DASProvider(CMSProvider):
	def __init__(self, config, section, datasetExpr, datasetNick, datasetID = 0):
		CMSProvider.__init__(self, config, section, datasetExpr, datasetNick, datasetID)
		self.url = QM(self.url == '', 'https://cmsweb.cern.ch/das/cache', self.url)


	def queryDAS(self, query):
		(start, sleep) = (time.time(), 0.4)
		while time.time() - start < 60:
			tmp = readURL(self.url, {"input": query}, {"Accept": "application/json"})
			if len(tmp) != 32:
				return parseJSON(tmp)['data']
			time.sleep(sleep)
			sleep += 0.4


	def getCMSDatasetsImpl(self, datasetPath):
		for ds1 in self.queryDAS("dataset dataset=%s" % datasetPath):
			for ds2 in ds1['dataset']:
				yield ds2['name']


	def getCMSBlocksImpl(self, datasetPath, getSites):
		for b1 in self.queryDAS("block dataset=%s" % datasetPath):
			for b2 in b1['block']:
				if 'replica' in b2:
					listSE = []
					for replica in b2['replica']:
						if self.nodeFilter(replica['site'], replica['complete'] == 'y'):
							listSE.append(replica['se'])
					yield (b2['name'], listSE)


	def getCMSFilesImpl(self, blockPath, onlyValid, queryLumi):
		for f1 in self.queryDAS("file block=%s" % blockPath):
			for f2 in f1['file']:
				if "nevents" in f2:
					yield ({DataProvider.URL: f2['name'], DataProvider.NEntries: f2['nevents']}, None)


	def getBlocksInternal(self):
		return self.getGCBlocks(usePhedex = False)
