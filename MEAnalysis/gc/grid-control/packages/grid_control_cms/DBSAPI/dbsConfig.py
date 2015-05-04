#!/usr/bin/env python
#-*- coding: ISO-8859-1 -*-
#
# Copyright 2006 Cornell University, Ithaca, NY 14853.
#
# Author:  Valentin Kuznetsov, 2006
#

# system modules
import os, sys, string, stat, re, types

# DBS specific modules
from dbsException    import DbsException
from dbsApiException import *

class DbsConfig(object):
  def __init__(self,iConfig={}):
    """
       Read and parse content of configuration file
       The following syntax is supported in configuration file:
       # ESDB configuration file
       login:password
       # ESDB Master
       Comments are started with '#' letter. User can specify login and password
       to provide access to underlying DB, if SQLite is used they're ignored.
       If DBS_CLIENT_CONFIG is noty set then the configuration is not attempted to be read.
    """
 
    uFileName=""
    iList=['url','alias','log', 'version','clienttype','verbose','mode','dbshome','javahome','adshome','retry']
    #iList=['user','password','driver','url','host','port','log', 'servlet','version','dbname','dbsDB','clienttype',	'dbtype','verbose','mode', 'dbshome', 'javahome', 'adshome','retry']
    self.configDict={}

    #for item in iList:
	#print item    
    #	if iConfig.has_key(item) and iConfig[item]:
    #		self.configDict[item] = iConfig[item]


    if os.environ.has_key('DBS_CLIENT_CONFIG'):
       if not os.path.isfile(os.environ['DBS_CLIENT_CONFIG']):
          raise DbsException(args="The '%s' config file does not exists"%os.environ['DBS_CLIENT_CONFIG'])
       uFileName=os.environ['DBS_CLIENT_CONFIG']
       #else:
       #   raise DbsException(args="No DBS_CLIENT_CONFIG environment is defined")
       #else:
       #   uFileName = os.path.normpath(os.environ["HOME"]+"/.dbs.conf")
       self.configFile=uFileName
       if not os.path.isfile(uFileName):
          raise DbsException(args="The DBS_CLIENT_CONFIG='%s' config file does not exists"%uFileName)
       #mode = os.stat(uFileName)[stat.ST_MODE]
       #if mode!=33152:
          # mode is not -rw-------
          #print "WARNING: permission of %s is set to 0600 mode (-rw-------)"%uFileName
          #os.chmod(uFileName,0600)
          print ""
       #login = masterHost =  masterName = masterPort = masterSocket = admin = ""
       for read in open(uFileName).readlines():
           line = string.split(read,"\n")[0]
           line = line.strip()
           if not len(line): continue
           if line[0]=="#": continue
           for item in iList:
               keyword=string.upper(item)
               if re.search(keyword,line):
		  #print item, line, keyword     
                  self.configDict[item] = string.split(line,"%s="%keyword)[1]
               #if iConfig.has_key(item) and iConfig[item]:
               #   self.configDict[item] = iConfig[item]

    # Over-write the values from the Passed in dict. OR use them if no config file is specified
    for item in iList:
        if iConfig.has_key(item) and iConfig[item]:
                self.configDict[item] = iConfig[item]


  def verbose(self):
    if not self.configDict.has_key('verbose'):
       return 0
    return 1
  def mode(self):
    if not self.configDict.has_key('mode'):
       raise DbsException(args="DBS configuration missing mode parameter")
    return self.configDict['mode']
  def clienttype(self):
    if not self.configDict.has_key('clienttype'):
       raise DbsException(args="DBS configuration missing user_type parameter")
    return self.configDict['clienttype']
  def dbshome(self):
    if not self.configDict.has_key('dbshome'):
       raise DbsException(args="DBS configuration missing mode parameter")
    return self.configDict['dbshome']
  def version(self):
    if not self.configDict.has_key('version'):
       raise DbsException(args="DBS configuration missing (Clent API) version parameter")
    return self.configDict['version']
  def javahome(self):
    if not self.configDict.has_key('javahome'):
       raise DbsException(args="DBS configuration missing javahome parameter")
    return self.configDict['javahome']
  def url(self):
    if not self.configDict.has_key('url'):
       raise DbsException(args="DBS configuration missing url/alias parameter")
    return self.configDict['url']
  def log(self):
    if not self.configDict.has_key('log'):
       raise DbsException(args="DBS configuration missing log parameter")
    return self.configDict['log']
  def adshome(self):
    if not self.configDict.has_key('adshome'):
       raise DbsException(args="DBS configuration missing adshome parameter")
    return self.configDict['adshome']
  def retry(self):
    if not self.configDict.has_key('retry'):
       raise DbsException(args="DBS configuration missing retry parameter")
    return self.configDict['retry']
#
# main
#
if __name__ == "__main__":
   dbsConfig = DbsConfig()
   print "Config file",dbsConfig.configFile
   print dbsConfig.configDict

