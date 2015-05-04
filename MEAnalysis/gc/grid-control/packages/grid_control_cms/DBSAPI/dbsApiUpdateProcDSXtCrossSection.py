
import os, re, string, socket, xml.sax, xml.sax.handler
import base64
from xml.sax.saxutils import escape
from cStringIO import StringIO

from dbsException import DbsException
from dbsApiException import *

import inspect

from dbsUtil import *

def dbsApiImplUpdateProcDSXtCrossSection(self, dataset, xSection):
    """
    Updates the Xternal X-Section filed of a Dataset

    dataset: Dataset to be updated
    xSection: X-Section 
  
    """

    funcInfo = inspect.getframeinfo(inspect.currentframe())

    data = self._server._call ({ 'api' : 'updateProcDSXtCrossSection',
                         'path' : get_path(dataset),
                         'xSection' : str(xSection),
                         }, 'POST')

