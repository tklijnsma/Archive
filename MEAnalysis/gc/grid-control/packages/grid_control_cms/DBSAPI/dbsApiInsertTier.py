
import os, re, string, socket, xml.sax, xml.sax.handler
import base64
from xml.sax.saxutils import escape
from cStringIO import StringIO

from dbsException import DbsException
from dbsApiException import *

import inspect

from dbsUtil import *

def dbsApiImplInsertTier(self, tier_name):
    """
    Inserts a new tier in the DBS databse. 
    
    param: 
	tier_name : The data tier name passed in as string 
			  
    raise: DbsApiException, DbsBadRequest, DbsBadData, DbsNoObject, DbsExecutionError, DbsConnectionError, 
           DbsToolError, DbsDatabaseError, DbsBadXMLData, InvalidDatasetPathName, DbsException	
	   
    examples:
         tier_name = "GEN-SIM-TEST"
         api.insertTier (tier_name)

    """

    funcInfo = inspect.getframeinfo(inspect.currentframe())
 
    xmlinput  = "<?xml version='1.0' standalone='yes'?>"
    xmlinput += "<dbs>"
    xmlinput += "<tier tier_name='"+ tier_name +"' />"
    xmlinput += "</dbs>"

    if self.verbose():
       print "insertTier, xmlinput",xmlinput

    data = self._server._call ({ 'api' : 'insertTier', 
                         'xmlinput' : xmlinput }, 'POST')

