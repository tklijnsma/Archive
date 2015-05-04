#!/usr/bin/env python
#
# Revision: 1.3 $"
# Id: DBSXMLParser.java,v 1.3 2006/10/26 18:26:04 afaq Exp $"
#
# DBS API class. Interfacing to Server using http/https or local
#

# system modules
import os, re, string, socket, xml.sax, xml.sax.handler
import base64
from xml.sax.saxutils import escape
from cStringIO import StringIO

# DBS specific modules
from dbsHttpService import DbsHttpService
from dbsExecService import DbsExecService

from dbsException import DbsException
from dbsApiException import *
from xml.sax import SAXParseException

from dbsConfig import DbsConfig
import urlparse
import urllib2

import inspect

from dbsUtil import *

#DBS Api version, set from the CVS checkout tag, for HEAD version, set it in dbs.config


class DbsApi(DbsConfig):
  """
  DbsApi class, provides access to DBS Server, 
  all clients must use this interface 
  """ 

  def __init__(self, Args={}):
    """ 
    Constructor. 
    Initializes the DBS Api by reading configuration 
    parameters from dbs.config file OR from the parameters 
    passed through Args as a Python dictionary.
    Parameters passed through Args take precedence 
    over parameters in dbs.config
    
    For MODE=POST (Default Mode): Creates a http proxy, to be able to talk to DBS Server
    """

    DbsConfig.__init__(self,Args)

    if not self.configDict.has_key('version'):
       self.configDict['version'] = self.setApiVersion()

 
    if self.configDict.has_key('retry'):
       Args['retry'] = self.configDict['retry']

    if self.configDict.has_key('url') and self.configDict.has_key('alias'):
	raise DbsApiException(args="Incorrect parameters: You cannot use 'url' and 'alias' together", code="6991")

    if self.configDict.has_key('alias'):
       self.configDict['url']=self.setServerUrl()

    if self.verbose():
       print "configuration dictionary:", self.configDict
       print "using version",self.version()
       print "using mode   ",self.mode()
    #Store info about current user
    if not self.configDict.has_key('userID'):
    	#Args['userID'] = os.getlogin()+'@'+socket.gethostname()
    	Args['userID'] = os.environ['USER']+'@'+socket.gethostname()
    # Connect to the Server proxy
    self._server = ""
    if not self.configDict.has_key('mode'):
	self.configDict['mode'] = "POST"  
    if self.mode() == "EXEC" :
	    self._server = DbsExecService(self.dbshome(), self.javahome(), self.version(), Args)
    else :
            self._server = DbsHttpService(self.url(), self.version(), Args)

    # Set the default Client Type to NORMAL
    if not self.configDict.has_key('clienttype'):
	self.configDict['clienttype'] = "NORMAL"
 
  def getServerUrl(self):
    """
    Returns the server URL

    """
    return self.url()


  def setServerUrl(self):
    """
    Sets Server URL from Registration Service, an unnecessary indirection :=)

    """
    print "setServerUrl is DEPRECATED"

  def setApiVersion(self):
    """
    Sets DBS Client Api Version
    Reading for __version__ tag

    Note: Config (dbs.config) and Constructor 
      arguments have higher presedence 
    """

    version = __version__.replace("$Name: ", "")
    version = version.replace("$", "")
    version = version.strip()
    if version.find("pre") != -1: 
	version=version.split("_pre")[0]
    if version.find("patch") != -1:
	version=version.split("_patch")[0]
    if version in (""):
	raise DbsApiException(args="Incorrect parameters: client version not specified use 'version' in dbs.config or pass in CTOR")
	return
    return version

  def getApiVersion(self):
    """
    Returns the API version of the API
    """
    return self.version()
  #------------------------------------------------------------
	    # DBS General APIs
  #------------------------------------------------------------
  def getServerInfo(self):
     try:
       #Calling the Implementation function
       from dbsApiGetServerInfo import dbsApiImplGetServerInfo
       return  dbsApiImplGetServerInfo(self)

     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex, SAXParseException)):
                raise ex
	else:
		raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
		# DBS - QL APIs

  #------------------------------------------------------------

  def executeQuery(self, query, begin="", end="", type="exe", case=True):
     try:
       #Calling the Implementation function
       from dbsApiExecuteQuery import dbsApiImplExecuteQuery
       return dbsApiImplExecuteQuery(self, query, begin, end, type, case)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
		
  #------------------------------------------------------------
  def countQuery(self, query, case=True):
     try:
       #Calling the Implementation function
       from dbsApiExecuteQuery import dbsApiImplCountQuery
       return dbsApiImplCountQuery(self, query, case)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def executeSummary(self, query, begin="", end="", sortKey="", sortOrder=""):
     try:
       #Calling the Implementation function
       from dbsApiExecuteQuery import dbsApiImplExecuteSummary
       return dbsApiImplExecuteSummary(self, query, begin, end, sortKey, sortOrder)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def getHelp(self, entity = ""):
     try:
        #Calling the Implementation function
        from dbsApiHelp import dbsApiImplGetHelp
        return  dbsApiImplGetHelp(self, entity)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
		# DBS - LIST APIs
  #------------------------------------------------------------
  def listPrimaryDatasets(self, pattern="*"):
     try:
       #Calling the Implementation function
       from dbsApiListPrimaryDatasets import dbsApiImplListPrimaryDatasets
       return  dbsApiImplListPrimaryDatasets(self, pattern)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def listProcessedDatasets(self, patternPrim="*", patternDT="*", patternProc="*",  patternVer="*", patternFam="*", patternExe="*", patternPS="*"):
     try:
       #Calling the Implementation function
       from dbsApiListProcessedDatasets import dbsApiImplListProcessedDatasets
       return  dbsApiImplListProcessedDatasets(self, patternPrim, patternDT, patternProc,  patternVer, patternFam, patternExe, patternPS)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def listDatasetPaths(self):
     try:
       #Calling the Implementation function
       from dbsApiListDatasetPaths import dbsApiImplListDatasetPaths
       return  dbsApiImplListDatasetPaths(self)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def listAlgorithms(self, patternVer="*", patternFam="*", patternExe="*", patternPS="*"):
     try:
       #Calling the Implementation function
       from dbsApiListAlgorithms import dbsApiImplListAlgorithms
       return  dbsApiImplListAlgorithms(self, patternVer, patternFam, patternExe, patternPS)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def listRuns(self, dataset="", block=""):
     try:
       #Calling the Implementation function
       from dbsApiListRuns import dbsApiImplListRuns
       return  dbsApiImplListRuns(self, dataset, block)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def listTiers(self, dataset):
     try:
       #Calling the Implementation function
       from dbsApiListTiers import dbsApiImplListTiers
       return  dbsApiImplListTiers(self, dataset)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def listBlocks(self, dataset=None, block_name="*", storage_element_name="*", nosite=False):
     try:
       #Calling the Implementation function
       from dbsApiListBlocks import dbsApiImplListBlocks
       #print self.configDict
       return  dbsApiImplListBlocks(self, dataset, block_name, storage_element_name, self.configDict['clienttype'], nosite=nosite)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def listBlockParents(self, block_name="*"):
     try:
       #Calling the Implementation function
       from dbsApiListBlockParents import dbsApiImplListBlockParents
       #print self.configDict
       return  dbsApiImplListBlockParents(self, block_name)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def listBlockChildren(self, block_name="*"):
     try:
       #Calling the Implementation function
       from dbsApiListBlockChildren import dbsApiImplListBlockChildren
       #print self.configDict
       return  dbsApiImplListBlockChildren(self, block_name)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def listStorageElements(self, storage_element_name="*"):
     try:
       #Calling the Implementation function
       from dbsApiListStorageElements import dbsApiImplListStorageElements
       return  dbsApiImplListStorageElements(self, storage_element_name)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def listLFNs(self, path="", queryableMetaData=""):
     try:
       #Calling the Implementation function
       from dbsApiListLFNs import dbsApiImplListLFNs
       return  dbsApiImplListLFNs(self, path, queryableMetaData)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def listDatasetFiles(self, datasetPath):
     try:
       #Calling the Implementation function
       from dbsApiListDatasetFiles import dbsApiImplListDatasetFiles
       return  dbsApiImplListDatasetFiles(self, datasetPath)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def listFiles(self, path="", primary="", proc="", tier_list=[], analysisDataset="",blockName="", patternLFN="", runNumber="", details=None, retriveList=(), otherDetails = False):
     try:
       #Calling the Implementation function
       from dbsApiListFiles import dbsApiImplListFiles
       return  dbsApiImplListFiles(self, path, primary, proc, tier_list, analysisDataset,blockName, patternLFN, runNumber, details, retriveList, otherDetails)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def listFileParents(self, lfn):
     try:
       #Calling the Implementation function
       from dbsApiListFileParents import dbsApiImplListFileParents
       return  dbsApiImplListFileParents(self, lfn)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def listFileAlgorithms(self, lfn):
     try:
       #Calling the Implementation function
       from dbsApiListFileAlgorithms import dbsApiImplListFileAlgorithms
       return  dbsApiImplListFileAlgorithms(self, lfn)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def listFileTiers(self, lfn):
     try:
       #Calling the Implementation function
       from dbsApiListFileTiers import dbsApiImplListFileTiers
       return  dbsApiImplListFileTiers(self, lfn)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def listFileLumis(self, lfn):
     try:
       #Calling the Implementation function
       from dbsApiListFileLumis import dbsApiImplListFileLumis
       return  dbsApiImplListFileLumis(self, lfn)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def listDatasetParents(self, dataset):
     try:
       #Calling the Implementation function
       from dbsApiListDatasetParents import dbsApiImplListDatasetParents
       return  dbsApiImplListDatasetParents(self, dataset)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def listPathParents(self, dataset):
     try:
       #Calling the Implementation function
       from dbsApiListPathParents import dbsApiImplListPathParents
       return  dbsApiImplListPathParents(self, dataset)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def listDatasetContents(self, path, block_name):
     try:
       #Calling the Implementation function
       from dbsApiListDatasetContents import dbsApiImplListDatasetContents
       return  dbsApiImplListDatasetContents(self, path, block_name)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def getSummary(self, dataset="", block=""):
     try:
       #Calling the Implementation function
       from dbsApiGetSummary import dbsApiImplGetSummary
       return  dbsApiImplGetSummary(self, dataset, block)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------

  def listDatasetSummary(self, path):
     try:
       #Calling the Implementation function
       from dbsApiListDatasetSummary import dbsApiImplListDatasetSummary
       return  dbsApiImplListDatasetSummary(self, path)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def listProcDSRunStatus(self,path, run):
     try:
       #Calling the Implementation function
       from dbsApiListProcDSRunStatus import dbsApiImplListProcDSRunStatus
       return  dbsApiImplListProcDSRunStatus(self, path, run)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
		# DBS-INSERT  APIs 
  #------------------------------------------------------------
  def insertTier(self, tier_name):
     try:
       #Calling the Implementation function
       from dbsApiInsertTier import dbsApiImplInsertTier
       return  dbsApiImplInsertTier(self, tier_name)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def insertLumiSection(self, lumi):
     try:
       #Calling the Implementation function
       from dbsApiInsertLumiSection import dbsApiImplInsertLumiSection
       return  dbsApiImplInsertLumiSection(self, lumi)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def insertMergedDataset(self, dataset, merege_ds_name, merge_algo):
     try:
       #Calling the Implementation function
       from dbsApiInsertMergedDataset import dbsApiImplInsertMergedDataset
       return  dbsApiImplInsertMergedDataset(self, dataset, merege_ds_name, merge_algo)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def insertMergedFile(self, parents, outputFile):
     try:
       #Calling the Implementation function
       from dbsApiInsertMergedFile import dbsApiImplInsertMergedFile
       return  dbsApiImplInsertMergedFile(self, parents, outputFile)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def insertPrimaryDataset(self, dataset):
     try:
       #Calling the Implementation function
       from dbsApiInsertPrimaryDataset import dbsApiImplInsertPrimaryDataset
       return  dbsApiImplInsertPrimaryDataset(self, dataset)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def insertAlgorithm(self, algorithm):
     try:
       #Calling the Implementation function
       from dbsApiInsertAlgorithm import dbsApiImplInsertAlgorithm
       return  dbsApiImplInsertAlgorithm(self, algorithm)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def insertProcessedDataset(self, dataset):
     try:
       #Calling the Implementation function
       from dbsApiInsertProcessedDataset import dbsApiImplInsertProcessedDataset
       return  dbsApiImplInsertProcessedDataset(self, dataset)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def insertRun(self, run):
     try:
       #Calling the Implementation function
       from dbsApiInsertRun import dbsApiImplInsertRun
       return  dbsApiImplInsertRun(self, run)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def insertFiles(self, dataset=None, files=[], block=None):
     try:
       #Calling the Implementation function
       from dbsApiInsertFiles import dbsApiImplInsertFiles
       return  dbsApiImplInsertFiles(self, dataset, files, block)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def insertBlock(self, dataset, block=None, storage_element_list=None, open_for_writing='y'):
     try:
       #Calling the Implementation function
       from dbsApiInsertBlock import dbsApiImplInsertBlock
       return  dbsApiImplInsertBlock(self, dataset, block, storage_element_list, open_for_writing)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def insertFileParent(self, file, parentFile):
     try:
       #Calling the Implementation function
       from dbsApiInsertFiles import dbsApiImplInsertFileParent
       return  dbsApiImplInsertFileParent(self, file, parentFile)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")

  #------------------------------------------------------------
  def insertRunInPD(self, dataset, run):
    try:
	#Calling the Implementation function
	from dbsApiInsertRunInPD import dbsApiImplInsertRunInPD
	return  dbsApiImplInsertRunInPD(self, dataset, run)
    except Exception, ex:
	if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
	    raise ex
	else:
	    raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
	
  def insertAlgoInPD(self, dataset, algorithm):
     try:
       #Calling the Implementation function
       from dbsApiInsertAlgoInPD import dbsApiImplInsertAlgoInPD
       return  dbsApiImplInsertAlgoInPD(self, dataset, algorithm)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")

  #------------------------------------------------------------
	    # DBS UPDATE APIS
  #------------------------------------------------------------

  def updateFileStatus(self, lfn, status, description=""):
     try:
       #Calling the Implementation function
       from dbsApiUpdateFileStatus import dbsApiImplUpdateFileStatus
       return  dbsApiImplUpdateFileStatus(self, lfn, status, description)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def updateProcDSDesc(self, dataset, desc):
     try:
       #Calling the Implementation function
       from dbsApiUpdateProcDSDesc import dbsApiImplUpdateProcDSDesc
       return  dbsApiImplUpdateProcDSDesc(self, dataset, desc)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def updateProcDSStatus(self, dataset, status):
     try:
       #Calling the Implementation function
       from dbsApiUpdateProcDSStatus import dbsApiImplUpdateProcDSStatus
       return  dbsApiImplUpdateProcDSStatus(self, dataset, status)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def updateRun(self, run):
     try:
       #Calling the Implementation function
       from dbsApiUpdateRun import dbsApiImplUpdateRun
       return  dbsApiImplUpdateRun(self, run)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")     
  #------------------------------------------------------------
  def renameSE(self, storage_element_from, storage_element_to):
     try:
       #Calling the Implementation function
       from dbsApiRenameSE import dbsApiImplRenameSE
       return  dbsApiImplRenameSE(self, storage_element_from, storage_element_to)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def updateSEBlock(self, blockName, storage_element_from, storage_element_to):
     try:
       #Calling the Implementation function
       from dbsApiUpdateSEBlock import dbsApiImplUpdateSEBlock
       return  dbsApiImplUpdateSEBlock(self, blockName, storage_element_from, storage_element_to)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def updateSEBlockRole(self, blockName, storage_element, role):
     try:
       #Calling the Implementation function
       from dbsApiUpdateSEBlock import dbsApiImplUpdateSEBlockRole
       return  dbsApiImplUpdateSEBlockRole(self, blockName, storage_element, role)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def openBlock(self, block=None ):
     try:
       #Calling the Implementation function
       from dbsApiOpenBlock import dbsApiImplOpenBlock
       return  dbsApiImplOpenBlock(self, block )
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def closeBlock(self, block=None ):
     try:
       #Calling the Implementation function
       from dbsApiCloseBlock import dbsApiImplCloseBlock
       return  dbsApiImplCloseBlock(self, block )
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def markPDRunDone(self,path, run):
     try:
       #Calling the Implementation function
       from dbsApiMarkPDRunDone import dbsApiImplMarkPDRunDone
       return  dbsApiImplMarkPDRunDone(self, path, run)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def markPDRunNotDone(self,path, run):
     try:
       #Calling the Implementation function
       from dbsApiMarkPDRunNotDone import dbsApiImplMarkPDRunNotDone
       return  dbsApiImplMarkPDRunNotDone(self, path, run)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
		# DBS-Migration APIs 
  #------------------------------------------------------------
  def insertDatasetContents(self, xmlinput, ignore_parent = False):
     try:
       #Calling the Implementation function
       from dbsApiInsertDatasetContents import dbsApiImplInsertDatasetContents
       return  dbsApiImplInsertDatasetContents(self, xmlinput, ignore_parent)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def migrateDatasetContents(self, srcURL, dstURL, path, block_name="", noParentsReadOnly = False, pruneBranches = False, srcVersion = None, dstVersion = None):
    """
	****************** DEPRECATED *************
        AA : 05/18/2010
        In the latest implementation, all migrations are done WITH parents, and Branch information is NOT saved by DBS so following parameters are DON'T care
                noParentsReadOnly, pruneBranches
        ALSO: it is HIGHLY ENCOURAGED to use dbsMigrateBlock and dbsMigrateDataset, instead of this DEPRECATED API
    """
    print "migrateDatasetContents() is ********  DEPRECATED   ******** , please use dbsMigrateBlock or dbsMigrateDataset instead"

    try:
        #Calling the Implementation function
        from dbsMigrateApi import DbsMigrateApi
        migrateapi = DbsMigrateApi(srcURL, dstURL)
        return migrateapi.migrateDataset(path)
    except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
            raise ex
        else:
            raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def dbsMigrateDataset(self, srcURL, dstURL, path):
    try:
        #Calling the Implementation function
        from dbsMigrateApi import DbsMigrateApi
        migrateapi = DbsMigrateApi(srcURL, dstURL)
        return migrateapi.migrateDataset(path)
    except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
            raise ex
        else:
            raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def dbsMigrateBlock(self, srcURL, dstURL, block_name="", srcVersion = None, dstVersion = None):
    try:
        #Calling the Implementation function
        from dbsMigrateApi import DbsMigrateApi
        migrateapi = DbsMigrateApi(srcURL, dstURL)
        return migrateapi.migrateBlock(block_name)
    except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
            raise ex
        else:
            raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
		# DBS - DELETE / Recycle Bin APIs
  #------------------------------------------------------------
  def undeleteBlock(self, path, block):
     try:
        #Calling the Implementation function
        from dbsApiDeleteBlock import dbsApiImplUndeleteBlock
        return  dbsApiImplUndeleteBlock(self, path, block)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def deleteProcDS(self, path):
     try:
        #Calling the Implementation function
        from dbsApiDeleteProcDS import dbsApiImplDeleteProcDS
        return  dbsApiImplDeleteProcDS(self, path)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def deleteRecycleBin(self, path, block):
     try:
        #Calling the Implementation function
        from dbsApiDeleteProcDS import dbsApiImplDeleteRecycleBin
        return  dbsApiImplDeleteRecycleBin(self, path, block)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def undeleteProcDS(self, path):
     try:
        #Calling the Implementation function
        from dbsApiDeleteProcDS import dbsApiImplUndeleteProcDS
        return  dbsApiImplUndeleteProcDS(self, path)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def deleteBlock(self, path, block):
     try:
        #Calling the Implementation function
        from dbsApiDeleteBlock import dbsApiImplDeleteBlock
        return  dbsApiImplDeleteBlock(self, path, block)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def listRecycleBin(self, path=""):
    try:
	#Calling the Implementation function
	from dbsApiListRecycleBin import dbsApiImplListRecycleBin
       	if(path==""):    
	    return  dbsApiImplListRecycleBin(self)
	else:
	    return dbsApiImplListRecycleBin(self, path)
    except Exception, ex:
	if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
	    raise ex
        else:
	    raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")
  #------------------------------------------------------------
  def deleteRecycleBin(self, path, block):
     try:
        #Calling the Implementation function
        from dbsApiDeleteRecycleBin import dbsApiImplDeleteRecycleBin
        return  dbsApiImplDeleteRecycleBin(self, path, block)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")

  #------------------------------------------------------------

  def addReplicaToBlock(self, block, storageElement):
     try:
       #Calling the Implementation function
       from dbsApiAddReplicaToBlock import dbsApiImplAddReplicaToBlock
       return  dbsApiImplAddReplicaToBlock(self, block, storageElement)
     except Exception, ex:
        if (isinstance(ex,DbsApiException) or isinstance(ex,SAXParseException)):
                raise ex
        else:
                raise DbsApiException(args="Unhandled Exception: "+str(ex), code="5991")


#############################################################################
# Unit testing: see $PWD/UnitTests
############################################################################

from dbsException import *
from dbsApiException import *
from dbsOptions import DbsOptionParser
import time

if __name__ == "__main__":

  try:

    optManager  = DbsOptionParser()
    (opts,args) = optManager.getOpt()
    args={}
    url_list_alias=[ 
		'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_global_writer/servlet/DBSServlet', 
		'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_local_01_writer/servlet/DBSServlet',
		'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_local_01_writer/servlet/DBSServlet',
		'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_local_02_writer/servlet/DBSServlet',
		'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_local_03_writer/servlet/DBSServlet',
		'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_local_04_writer/servlet/DBSServlet',
		'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_local_05_writer/servlet/DBSServlet',
		'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_local_06_writer/servlet/DBSServlet',
		'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_local_07_writer/servlet/DBSServlet',
		'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_local_08_writer/servlet/DBSServlet',
		'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_local_09_writer/servlet/DBSServlet',
		'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_local_10_writer/servlet/DBSServlet',
		'https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_01_writer/servlet/DBSServlet',
		'https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet',
		'https://cmsdbsprod.cern.ch:8443/cms_dbs_caf_analysis_01_writer/servlet/DBSServlet',

		'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_global_admin/servlet/DBSServlet',
                'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_local_01_admin/servlet/DBSServlet',
                'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_local_01_admin/servlet/DBSServlet',
                'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_local_02_admin/servlet/DBSServlet',
                'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_local_03_admin/servlet/DBSServlet',
                'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_local_04_admin/servlet/DBSServlet',
                'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_local_05_writer/servlet/DBSServlet',
                'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_local_06_admin/servlet/DBSServlet', 
                'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_local_07_admin/servlet/DBSServlet',
                'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_local_08_admin/servlet/DBSServlet',
                'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_local_09_admin/servlet/DBSServlet',
                'https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_local_10_admin/servlet/DBSServlet',
                'https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_01_admin/servlet/DBSServlet',
                'https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_admin/servlet/DBSServlet',
                'https://cmsdbsprod.cern.ch:8443/cms_dbs_caf_analysis_01_admin/servlet/DBSServlet',

		'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet',
		'http://cmsdbsprod.cern.ch/cms_dbs_prod_local_01/servlet/DBSServlet',
		'http://cmsdbsprod.cern.ch/cms_dbs_prod_local_02/servlet/DBSServlet',
		'http://cmsdbsprod.cern.ch/cms_dbs_prod_local_03/servlet/DBSServlet',
		'http://cmsdbsprod.cern.ch/cms_dbs_prod_local_04/servlet/DBSServlet',
		'http://cmsdbsprod.cern.ch/cms_dbs_prod_local_05/servlet/DBSServlet',
		'http://cmsdbsprod.cern.ch/cms_dbs_prod_local_06/servlet/DBSServlet',
		'http://cmsdbsprod.cern.ch/cms_dbs_prod_local_07/servlet/DBSServlet',
		'http://cmsdbsprod.cern.ch/cms_dbs_prod_local_08/servlet/DBSServlet',
		'http://cmsdbsprod.cern.ch/cms_dbs_prod_local_09/servlet/DBSServlet',
		'http://cmsdbsprod.cern.ch/cms_dbs_prod_local_10/servlet/DBSServlet',
                'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_01/servlet/DBSServlet',
                'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_01/servlet/DBSServlet',
		'https://cmsdbsprod.cern.ch:8443/cms_dbs_caf_analysis_01_writer/servlet/DBSServlet',
		]
    url_list_73=[
                'https://vocms73.cern.ch:8443/cms_dbs_prod_global_writer/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_prod_local_01_writer/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_prod_local_01_writer/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_prod_local_02_writer/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_prod_local_03_writer/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_prod_local_04_writer/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_prod_local_05_writer/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_prod_local_06_writer/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_prod_local_07_writer/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_prod_local_08_writer/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_prod_local_09_writer/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_prod_local_10_writer/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_ph_analysis_01_writer/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_caf_analysis_01_writer/servlet/DBSServlet',

                'https://vocms73.cern.ch:8443/cms_dbs_prod_global_admin/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_prod_local_01_admin/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_prod_local_01_admin/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_prod_local_02_admin/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_prod_local_03_admin/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_prod_local_04_admin/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_prod_local_05_writer/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_prod_local_06_admin/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_prod_local_07_admin/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_prod_local_08_admin/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_prod_local_09_admin/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_prod_local_10_admin/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_ph_analysis_01_admin/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_ph_analysis_02_admin/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_caf_analysis_01_admin/servlet/DBSServlet',

                'http://vocms73.cern.ch/cms_dbs_prod_global/servlet/DBSServlet',
                'http://vocms73.cern.ch/cms_dbs_prod_local_01/servlet/DBSServlet',
                'http://vocms73.cern.ch/cms_dbs_prod_local_02/servlet/DBSServlet',
                'http://vocms73.cern.ch/cms_dbs_prod_local_03/servlet/DBSServlet',
                'http://vocms73.cern.ch/cms_dbs_prod_local_04/servlet/DBSServlet',
                'http://vocms73.cern.ch/cms_dbs_prod_local_05/servlet/DBSServlet',
                'http://vocms73.cern.ch/cms_dbs_prod_local_06/servlet/DBSServlet',
                'http://vocms73.cern.ch/cms_dbs_prod_local_07/servlet/DBSServlet',
                'http://vocms73.cern.ch/cms_dbs_prod_local_08/servlet/DBSServlet',
                'http://vocms73.cern.ch/cms_dbs_prod_local_09/servlet/DBSServlet',
                'http://vocms73.cern.ch/cms_dbs_prod_local_10/servlet/DBSServlet',
                'http://vocms73.cern.ch/cms_dbs_ph_analysis_01/servlet/DBSServlet',
                'http://vocms73.cern.ch/cms_dbs_ph_analysis_01/servlet/DBSServlet',
                'https://vocms73.cern.ch:8443/cms_dbs_caf_analysis_01_writer/servlet/DBSServlet',
		]

    url_list_74=[
                'https://vocms74.cern.ch:8443/cms_dbs_prod_global_writer/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_prod_local_01_writer/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_prod_local_01_writer/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_prod_local_02_writer/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_prod_local_03_writer/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_prod_local_04_writer/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_prod_local_05_writer/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_prod_local_06_writer/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_prod_local_07_writer/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_prod_local_08_writer/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_prod_local_09_writer/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_prod_local_10_writer/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_ph_analysis_01_writer/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_caf_analysis_01_writer/servlet/DBSServlet',

                'https://vocms74.cern.ch:8443/cms_dbs_prod_global_admin/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_prod_local_01_admin/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_prod_local_01_admin/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_prod_local_02_admin/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_prod_local_03_admin/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_prod_local_04_admin/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_prod_local_05_writer/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_prod_local_06_admin/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_prod_local_07_admin/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_prod_local_08_admin/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_prod_local_09_admin/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_prod_local_10_admin/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_ph_analysis_01_admin/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_ph_analysis_02_admin/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_caf_analysis_01_admin/servlet/DBSServlet',

                'http://vocms74.cern.ch/cms_dbs_prod_global/servlet/DBSServlet',
                'http://vocms74.cern.ch/cms_dbs_prod_local_01/servlet/DBSServlet',
                'http://vocms74.cern.ch/cms_dbs_prod_local_02/servlet/DBSServlet',
                'http://vocms74.cern.ch/cms_dbs_prod_local_03/servlet/DBSServlet',
                'http://vocms74.cern.ch/cms_dbs_prod_local_04/servlet/DBSServlet',
                'http://vocms74.cern.ch/cms_dbs_prod_local_05/servlet/DBSServlet',
                'http://vocms74.cern.ch/cms_dbs_prod_local_06/servlet/DBSServlet',
                'http://vocms74.cern.ch/cms_dbs_prod_local_07/servlet/DBSServlet',
                'http://vocms74.cern.ch/cms_dbs_prod_local_08/servlet/DBSServlet',
                'http://vocms74.cern.ch/cms_dbs_prod_local_09/servlet/DBSServlet',
                'http://vocms74.cern.ch/cms_dbs_prod_local_10/servlet/DBSServlet',
                'http://vocms74.cern.ch/cms_dbs_ph_analysis_01/servlet/DBSServlet',
                'http://vocms74.cern.ch/cms_dbs_ph_analysis_01/servlet/DBSServlet',
                'https://vocms74.cern.ch:8443/cms_dbs_caf_analysis_01_writer/servlet/DBSServlet',
		]


    url_list_t0_alias=[
		'https://cmst0dbs.cern.ch:8443/cms_dbs_prod_tier0_writer/servlet/DBSServlet',
		'https://cmst0dbs.cern.ch:8443/cms_dbs_int_tier0_writer/servlet/DBSServlet',
		'http://cmst0dbs.cern.ch/cms_dbs_prod_tier0/servlet/DBSServlet',
		'http://cmst0dbs.cern.ch/cms_dbs_int_tier0/servlet/DBSServlet',
                'https://cmst0dbs.cern.ch:8443/cms_dbs_prod_tier0_admin/servlet/DBSServlet',
                'https://cmst0dbs.cern.ch:8443/cms_dbs_int_tier0_admin/servlet/DBSServlet',
    		]
    #cmst0dbs2
    url_list_t0_95=[
	        'https://vocms95.cern.ch:8443/cms_dbs_prod_tier0_writer/servlet/DBSServlet',
		'https://vocms95.cern.ch:8443/cms_dbs_int_tier0_writer/servlet/DBSServlet',
		'http://vocms95.cern.ch/cms_dbs_prod_tier0/servlet/DBSServlet',
		'http://vocms95.cern.ch/cms_dbs_int_tier0/servlet/DBSServlet',
		'https://vocms95.cern.ch:8443/cms_dbs_prod_tier0_admin/servlet/DBSServlet',
	        'https://vocms95.cern.ch:8443/cms_dbs_int_tier0_admin/servlet/DBSServlet',
                ]
    #cmst0dbs1
    url_list_t0_96=[
                'https://vocms96.cern.ch:8443/cms_dbs_prod_tier0_writer/servlet/DBSServlet',
	        'https://vocms96.cern.ch:8443/cms_dbs_int_tier0_writer/servlet/DBSServlet',
		'http://vocms96.cern.ch/cms_dbs_prod_tier0/servlet/DBSServlet',
		'http://vocms96.cern.ch/cms_dbs_int_tier0/servlet/DBSServlet',
		'https://vocms96.cern.ch:8443/cms_dbs_prod_tier0_admin/servlet/DBSServlet',
		'https://vocms96.cern.ch:8443/cms_dbs_int_tier0_admin/servlet/DBSServlet',
		]		    
 

    url_list=[]
    url_list.extend(url_list_alias)
    url_list.extend(url_list_73)
    url_list.extend(url_list_74)
    url_list.extend(url_list_t0_alias)
    url_list.extend(url_list_t0_95)
    url_list.extend(url_list_t0_96)

    
    args['mode']='POST'
    args['version']='DBS_2_0_8'
    args['level']='DBSINFO'
    #api = DbsApi(args)

    for aurl in url_list:
       args['url']=aurl
       print aurl
       api = DbsApi(args) 
       t1=time.time()   
       serverInfo = api.getServerInfo()
       t2=time.time()   
       print api.getServerUrl()
       print "Server Version : ", serverInfo['ServerVersion']
       print "Schema Version : ", serverInfo['SchemaVersion']
       print "Time taken by call : %s seconds" %(t2-t1)
      #print api.listSubSystems()
      #print api.listDQVersions()

  except DbsApiException, ex:
    print "Caught API Exception %s: %s "  % (ex.getClassName(), ex.getErrorMessage() )
    if ex.getErrorCode() not in (None, ""):
      print "DBS Exception Error Code: ", ex.getErrorCode()

