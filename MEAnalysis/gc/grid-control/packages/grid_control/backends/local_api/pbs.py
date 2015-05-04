import sys, os
from grid_control import QM, ConfigError, RethrowError, Job, utils
from grid_control.backends import WMS
from pbsge import PBSGECommon

class PBS(PBSGECommon):
	_statusMap = {
		'H': Job.SUBMITTED, 'S': Job.SUBMITTED,
		'W': Job.WAITING,   'Q': Job.QUEUED,
		'R': Job.RUNNING,   'C': Job.DONE,
		'E': Job.DONE,      'T': Job.DONE,
		'fail':	Job.FAILED, 'success': Job.SUCCESS
	}

	def __init__(self, config, wmsName = None):
		PBSGECommon.__init__(self, config, wmsName)
		self.nodesExec = utils.resolveInstallPath('pbsnodes')
		self._server = config.get(self._getSections('backend'), 'server', '', mutable=True)
		self.fqid = lambda wmsId: QM(self._server, '%s.%s' % (wmsId, self._server), wmsId)


	def getSubmitArguments(self, jobNum, jobName, reqs, sandbox, stdout, stderr):
		reqMap = { WMS.MEMORY: ('pvmem', lambda m: '%dmb' % m) }
		params = PBSGECommon.getSubmitArguments(self, jobNum, jobName, reqs, sandbox, stdout, stderr, reqMap)
		# Job requirements
		if reqs.get(WMS.QUEUES):
			params += ' -q %s' % reqs[WMS.QUEUES][0]
		if reqs.get(WMS.SITES):
			params += ' -l host=%s' % str.join('+', reqs[WMS.SITES])
		return params


	def parseSubmitOutput(self, data):
		# 1667161.ekpplusctl.ekpplus.cluster
		return data.split('.')[0].strip()


	def parseStatus(self, status):
		for section in utils.accumulate(status, '', lambda x, buf: x == '\n'):
			try:
				lines = section.replace('\n\t', '').split('\n')
				jobinfo = utils.DictFormat(' = ').parse(lines[1:])
				jobinfo['id'] = lines[0].split(':')[1].split('.')[0].strip()
				jobinfo['status'] = jobinfo.get('job_state')
				jobinfo['dest'] = 'N/A'
				if 'exec_host' in jobinfo:
					jobinfo['dest'] = '%s/%s' % (
						jobinfo.get('exec_host').split('/')[0] + '.' + jobinfo.get('server', ''),
						jobinfo.get('queue')
					)
			except:
				raise RethrowError('Error reading job info:\n%s' % section)
			yield jobinfo


	def getCheckArguments(self, wmsIds):
		return '-f %s' % str.join(' ', map(self.fqid, wmsIds))


	def getCancelArguments(self, wmsIds):
		return str.join(' ', map(self.fqid, wmsIds))


	def getQueues(self):
		(queues, active) = ({}, False)
		keys = [WMS.MEMORY, WMS.CPUTIME, WMS.WALLTIME]
		parser = dict(zip(keys, [int, utils.parseTime, utils.parseTime]))
		for line in utils.LoggedProcess(self.statusExec, '-q').iter():
			if line.startswith('-'):
				active = True
			elif line.startswith(' '):
				active = False
			elif active:
				fields = map(str.strip, line.split()[:4])
				props = filter(lambda (k, v): not v.startswith('-'), zip(keys, fields[1:]))
				queues[fields[0]] = dict(map(lambda (k, v): (k, parser[k](v)), props))
		return queues


	def getNodes(self):
		result = []
		for line in utils.LoggedProcess(self.nodesExec).iter():
			if not line.startswith(' ') and len(line) > 1:
				node = line.strip()
			if ('state = ' in line) and ('down' not in line) and ('offline' not in line):
				result.append(node)
		if len(result) > 0:
			return result
