from .BaseClient import BaseClient
from .DataViews import DataViews
from .Types import Types
from .Streams import Streams


class EDSClient:
    """
    A client that handles communication with EDS
    """

    def __init__(self, apiversion="v1", url='http://localhost:5590', acceptVerbosity=False):
        """
        Use this to help communinication with EDS
        :param url: The base URL for EDS, default is http://localhost:5590
        :param apiversion: Version of the api you are communicating with, default is v1
        :param acceptVerbosity: Sets whether in value calls you get all values
                or just non-default values
        """
        self.__baseClient = BaseClient(
            apiversion, 'default', url, None, None, acceptVerbosity)
        self.__Types = Types(self.__baseClient)
        self.__Streams = Streams(self.__baseClient)

    @property
    def uri(self):
        """
        :return: The uri of this EDS client as a string
        """
        return self.__baseClient.uri

    @property
    def acceptverbosity(self):
        """
        :return: Whether this will include the accept verbosity header
        """
        return self.__baseClient.AcceptVerbosity

    @acceptverbosity.setter
    def acceptverbosity(self, AcceptVerbosity):
        self.__baseClient.AcceptVerbosity = AcceptVerbosity

    @property
    def request_timeout(self):
        """
        :return: Request timeout in seconds (default 30 secs)
        """
        return self.__baseClient.RequestTimeout

    @request_timeout.setter
    def request_timeout(self, timeout):
        self.__baseClient.RequestTimeout = timeout

    @property
    def Types(self):
        """
        :return: A client for interacting with Types
        """
        return self.__Types

    @property
    def Streams(self):
        """
        :return: A client for interacting with Streams
        """
        return self.__Streams
