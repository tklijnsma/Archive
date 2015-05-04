import os
from psource_basic import *
from psource_meta import *
from psource_file import *
from psource_data import *
from padapter import *
from config_param import ParameterConfig
from grid_control import AbstractObject, QM, utils

class ParameterFactory(AbstractObject):
	def __init__(self, config, sections):
		self.adapter = config.get(sections, 'parameter adapter', 'TrackedParameterAdapter')
		self.paramConfig = ParameterConfig(config, sections, self.adapter != 'TrackedParameterAdapter')


	def _getRawSource(self, parent):
		return parent


	def getSource(self, config):
		source = self._getRawSource(RNGParameterSource())
		if DataParameterSource.datasetsAvailable and not DataParameterSource.datasetsUsed:
			source = CrossParameterSource(DataParameterSource.create(), source)
		return ParameterAdapter.open(self.adapter, config, source)
ParameterFactory.dynamicLoaderPath()


class BasicParameterFactory(ParameterFactory):
	def __init__(self, config, sections):
		(self.constSources, self.lookupSources) = ([], [])
		ParameterFactory.__init__(self, config, sections)

		# Get constants from [constants]
		for cName in filter(lambda o: not o.endswith(' lookup'), config.getOptions('constants')):
			self._addConstantPlugin(config, 'constants', cName, cName.upper())
		# Get constants from [<Module>] constants
		for cName in map(str.strip, config.getList(sections, 'constants', [])):
			self._addConstantPlugin(config, sections, cName, cName)
		# Random number variables
		for (idx, seed) in enumerate(self._getSeeds(config)):
			self.constSources.append(CounterParameterSource('SEED_%d' % idx, seed))
		self.repeat = config.getInt(sections, 'repeat', 1, mutable=True) # ALL config.x -> paramconfig.x !


	def _addConstantPlugin(self, config, sections, cName, varName):
		lookupVar = config.get(sections, '%s lookup' % cName, '')
		if lookupVar:
			self.lookupSources.append(LookupParameterSource(varName, config.getDict(sections, cName, {}), lookupVar))
		else:
			self.constSources.append(ConstParameterSource(varName, config.get(sections, cName, '').strip()))


	def _getSeeds(self, config):
		seeds = map(int, config.getList('jobs', 'seeds', []))
		nseeds = config.getInt('jobs', 'nseeds', 10)
		if len(seeds) == 0:
			# args specified => gen seeds
			newSeeds = str.join(' ', map(lambda x: str(random.randint(0, 10000000)), range(nseeds)))
			seeds = map(int, str(config.getTaskDict().get('seeds', newSeeds)).split())
			utils.vprint('Using random seeds... %s' % seeds, once = True)
		config.getTaskDict().write({'seeds': str.join(' ', map(str, seeds))})
		return seeds


	def _getRawSource(self, parent):
		source_list = self.constSources + [parent, RequirementParameterSource()]
		source = ZipLongParameterSource(*source_list)
		if self.repeat > 1:
			source = RepeatParameterSource(source, self.repeat)
		return ParameterFactory._getRawSource(self, source)
