""" Splunk default values for import

@author: dcsteve24
__python_version__ = Py2/Py3
__os__ =  All
__updated__ = '2021-09-05'
"""

import os

# TODO: Need to establish the SPLUNK_HOME path somewhere. Used to hard code this in a splunk_locals
# file but it'd be better in a configuration file or something similar. Should probably tie this to
# the connector configs. Code won't work til that's resolved. Meantime could just hard set here when
# I import this for use somewhere til I get around to this.
FORWARDER_HOME = ''
SPLUNK_HOME = ''
UNIVERSAL_FORWARDER = ''
SPLUNK_USER = ''


# Splunk command absolute paths
FORWARDER_SPLUNK_COMMAND = os.path.join(FORWARDER_HOME, 'bin', 'splunk')
SPLUNK_COMMAND = os.path.join(SPLUNK_HOME, 'bin', 'splunk')

# Splunk log variables
_SPLUNK_LOG_FILE_NAME = 'splunk_python_code.log'
SPLUNK_LOGGER_NAME = 'splunk_ops'
FORWARDER_LOGGER_NAME = 'splunk_forwarder_ops'
SPLUNK_PYTHON_LOGGER_LOCATION = os.path.join(SPLUNK_HOME, _SPLUNK_LOG_FILE_NAME)
FORWARDER_PYTHON_LOGGER_LOCATION = os.path.join(FORWARDER_HOME, _SPLUNK_LOG_FILE_NAME)
