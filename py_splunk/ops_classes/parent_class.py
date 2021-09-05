""" Splunk parent class containing generic functions for the children inheritance.

__classes__:
    MissingConfigError
    SplunkParentClass

@author: dcsteve24
__python_version__ = Py2/Py3
__os__ =  All
__updated__ = '2021-09-05'
"""

from py_splunk.globals import FORWARDER_SPLUNK_COMMAND, FORWARDER_LOGGER_NAME, \
    FORWARDER_PYTHON_LOGGER_LOCATION, SPLUNK_COMMAND, SPLUNK_LOGGER_NAME, \
    SPLUNK_PYTHON_LOGGER_LOCATION, SPLUNK_USER, UNIVERSAL_FORWARDER
from py_utilities.configuration_operations import get_config_object, DEFAULT_APP_FILE_LOCATION, \
    MissingConfigError, MissingSettingError, read_config
from py_utilities.dynamic_logger import create_logger, log_message
from py_utilities.remote_operations import remote_operations


# TODO: Tie in authentication or better use cases than only those mentioned in the
#    restart_splunk_service
# TODO: Should be a clean/secure way of password storing in memory vs being able to see in
#    debug/etc. Look into. I know SQLAlchemy manages to do this so might be worth digging into how
#    there.

class SplunkParentClass(object):
    """ Parent class for Splunk operations classes. This class holds all the common functions,
    attributes, etc. for all Splunk operations classes.

    Functions:
        read_connector_config
        restart_splunk_service

    Attributes:
        host: Str. The host which we connect to for the specific actions we are conducting. Can be
            IP or hostname.
        port: Int. The port used for the connection of the host.
        username: Str. The username to connect to the Splunk services. Not all children require
            this. Defaults to None.
        password: Str. The password for the passed username. Not all children require this.
            Defaults to None.
        logger_name: Str. The name of the logger this class uses to log to.
    """
    def __init__(self,
                 host,
                 port,
                 username=None,
                 password=None,
                 read_connector_config=False,
                 log_level='info',
                 log_console_output=False):
        """ Initializes the class assigning args as attributes.

        Args:
            Optional:
                read_connector_config: Bool. If true will fill in missing values with the values in
                    the connector config.
                log_level: Str. The classes will log to their loggers at this level. Defaults to
                    'info'.
                log_console_output: Bool. If True, the classes will output their logs to the
                    console.
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        if UNIVERSAL_FORWARDER in self.host:
            self.logger_name = FORWARDER_LOGGER_NAME
            create_logger(FORWARDER_PYTHON_LOGGER_LOCATION, log_level, self.logger_name,
                          console_output=log_console_output)
        else:
            self.logger_name = SPLUNK_LOGGER_NAME
            create_logger(SPLUNK_PYTHON_LOGGER_LOCATION, log_level, self.logger_name,
                          console_output=log_console_output)
        if read_connector_config:
            if not self.host and not self.port and not self.username and not self.password:
                try:
                    self.read_connector_config()
                except EnvironmentError:
                    log_message('warn', 'One or more values of host, port, username, or password'
                                ' not passed and no app connector file detected at %s. Values have'
                                ' not been set.' % DEFAULT_APP_FILE_LOCATION, self.logger_name)
                except MissingSettingError:
                    log_message('warn', 'Missing the Splunk INI setting in the %s file' %
                                DEFAULT_APP_FILE_LOCATION, self.logger_name)

    def restart_splunk_service(self, host=None, port=None, splunk_user=SPLUNK_USER):
        """ Restarts the splunk service. Can be on a remote server instance.

        NOTE: This only works if you are able to sudo into the splunk service account without
        password prompts (edit the sudo config as needed). If you can run splunk commands, just use
        yourself. Improper permissions result in a single line return annotating to run it from the
        correct user (neither generates an error and doesn't restart splunk)

        Args:
            Optional:
                host: Str. The host we are restarting the service on. Defaults to self.host.
                port: Int. The port used to SSH into the host. Defaults to self.port.
                splunk_user: The user able to run the splunk restart command. Defaults to the global
                    setting.
        """
        host = self.host if not host else host
        port = self.port if not port else port
        splunk_command = FORWARDER_SPLUNK_COMMAND if UNIVERSAL_FORWARDER in host else SPLUNK_COMMAND
        command = ['sudo -u %s %s restart' % (splunk_user, splunk_command)]
        remote_operations(host, command, port, catch_errors=False, tty_session=True)

    def read_connector_config(self, config_path=DEFAULT_APP_FILE_LOCATION, overwrite=False):
        """ Reads in the application connector configuration to find your Splunk settings and
        assigns them to the corresponding attributes. By default this will not overwrite attributes
        already set, but you can flip a flag to do so.

        Args:
            Optional:
                config_path: Str. The absolute path to the application connector configuration.
                    Defaults to the default home path location.
                overwrite: Bool. If set will overwrite the attribute with the read in configuration
                    values regardless if the attribute values are already set or not. Defaults to
                    False.

        Raises:
            MissingConfigError: The splunk connector config settings were not detected.
        """
        config_object_list = read_config(config_path)
        splunk_connector = get_config_object(config_object_list, 'splunk')
        if not splunk_connector:
            raise MissingConfigError('No splunk connector settings detected in the file.',
                                     self.logger_name)
        else:
            if overwrite or not self.host:
                self.host = splunk_connector.host
            if overwrite or not self.port:
                self.port = splunk_connector.port
            if overwrite or not self.username:
                self.username = splunk_connector.username
            if overwrite or not self.password:
                self.password = splunk_connector.password
