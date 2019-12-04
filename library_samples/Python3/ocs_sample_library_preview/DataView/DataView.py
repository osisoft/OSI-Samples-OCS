import json
from .DataViewQuery import DataViewQuery
from .DataViewMappings import DataViewMappings
from .DataViewIndexConfig import DataViewIndexConfig
from .DataViewGroupRule import DataViewGroupRule


class DataView(object):
    """
    DataView definition
    """

    def __init__(
        self,
        id=None,
        name=None,
        description=None,
        queries=None,
        mappings=None,
        indexConfig=None,
        indexDataType=None,
        groupRules=[],
    ):
        """

        :param id: required
        :param name: not required
        :param description:  not required
        :param queries: query string  required
        :param mappings: array of DataViewmapping   not required
        :param indexConfig:  DataViewindexConfig   not required
        :param indexDataType: Currently limited to "DateTime"   required
        :param groupRules:  Array of DataViewGroupRule   not required
        """
        self.__id = id
        self.__name = name
        self.__description = description
        if queries:
            self.__queries = queries
        else:
            self.__queries = DataViewQuery()
        if mappings:
            self.__mappings = mappings
        self.__indexConfig = indexConfig
        self.__indexDataType = indexDataType
        self.__groupRules = groupRules

    @property
    def Id(self):
        """
        Get the id  required
        :return:
        """
        return self.__id

    @Id.setter
    def Id(self, id):
        """
        Set the id  required
        :param id:
        :return:
        """
        self.__id = id

    @property
    def Name(self):
        """
        Name can be duplicated in a namespace   not required
        :return:
        """
        return self.__name

    @Name.setter
    def Name(self, name):
        """
        Name can be duplicated in a namespace   not required
        :param name:
        :return:
        """
        self.__name = name

    @property
    def Description(self):
        """
        Add an esy to understand description not required
        :return:
        """
        return self.__description

    @Description.setter
    def Description(self, description):
        """
        Add an esy to understand description not required
        :param description:
        :return:
        """
        self.__description = description

    @property
    def Queries(self):
        """
        Query string  required
        :return:
        """
        return self.__queries

    @Queries.setter
    def Queries(self, queries):
        """
        Array of dataviequery  required
        :param queries:
        :return:
        """
        self.__queries = queries

    @property
    def Mappings(self):
        """
        array of DataViewmapping   not required
        :return:
        """
        return self.__mappings

    @Mappings.setter
    def Mappings(self, mappings):
        """
        array of DataViewmapping   not required
        :param mappings:
        :return:
        """
        self.__mappings = mappings

    @property
    def IndexConfig(self):
        """
        DataViewindexConfig   not required
        :return:
        """
        return self.__indexConfig

    @IndexConfig.setter
    def IndexConfig(self, indexConfig):
        """
        DataViewindexConfig   not required
        :param indexConfig:
        :return:
        """
        self.__indexConfig = indexConfig

    @property
    def IndexDataType(self):
        """
        Currently limited to "DateTime"   required
        :return:
        """
        return self.__indexDataType

    @IndexDataType.setter
    def IndexDataType(self, indexDataType):
        """
        Currently limited to "DateTime"   required
        :param indexDataType:
        :return:
        """
        self.__indexDataType = indexDataType

    @property
    def GroupRules(self):
        """
        Array of DataViewGroupRule   not required
        :return:
        """
        return self.__groupRules

    @GroupRules.setter
    def GroupRules(self, groupRules):
        """
        Array of DataViewGroupRule   not required
        :param groupRules:
        :return:
        """
        self.__groupRules = groupRules

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = {"Id": self.Id}
        dictionary["Queries"] = self.Queries.toDictionary()

        # optional properties
        if hasattr(self, "Name"):
            dictionary["Name"] = self.Name

        if hasattr(self, "Description"):
            dictionary["Description"] = self.Description

        if hasattr(self, "Mappings") and self.Mappings is not None:
            dictionary["Mappings"] = self.Mappings.toDictionary()

        if hasattr(self, "IndexConfig") and self.IndexConfig is not None:
            dictionary["IndexConfig"] = self.IndexConfig.toDictionary()

        if hasattr(self, "IndexDataType"):
            dictionary["IndexDataType"] = self.IndexDataType

        if hasattr(self, "GroupRules"):
            dictionary["GroupRules"] = []
            for value in self.GroupRules:
                dictionary["GroupRules"].append(value.toDictionary())

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return DataView.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        dataView = DataView()

        if not content:
            return dataView

        if "Id" in content:
            dataView.Id = content["Id"]

        if "Name" in content:
            dataView.Name = content["Name"]

        if "Description" in content:
            dataView.Description = content["Description"]

        if "Queries" in content:
            dataView.Queries = DataViewQuery.fromDictionary(content["Queries"])

        if "Mappings" in content:
            dataView.Mappings = DataViewMappings.fromDictionary(
                content["Mappings"])

        if "IndexConfig" in content:
            dataView.IndexConfig = DataViewIndexConfig.fromDictionary(
                content["IndexConfig"]
            )

        if "IndexDataType" in content:
            dataView.IndexDataType = content["IndexDataType"]

        if "GroupRules" in content:
            groupRules = content["GroupRules"]
            if groupRules is not None and len(groupRules) > 0:
                dataView.GroupRules = []
                for value in groupRules:
                    dataView.GroupRules.append(
                        DataViewGroupRule.fromDictionary(value))

        return dataView
