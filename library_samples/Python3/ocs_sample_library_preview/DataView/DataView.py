import json
from ..SDS.SdsTypeCode import SdsTypeCode
from .Query import Query
from .FieldSet import FieldSet
from .Field import Field
from .DataViewShapes import DataViewShapes


class DataView(object):
    """
    Data View definition
    """

    def __init__(
        self,
        id=None,
        name=None,
        description=None,
        queries=None,
        fieldsets=None,
        sectioners=None,
        indextypecode=None,
        defaultstartindex=None,
        defaultendindex=None,
        defaultinterval=None,
        shape=None
    ):
        """

        :param id: required
        :param name: not required
        :param description:  not required
        """
        self.__id = id
        self.__name = name
        self.__description = description
        if queries:
            self.__queries = queries
        else:
            self.__queries = []
        if fieldsets:
            self.__fieldsets = fieldsets
        else:
            self.__fieldsets = []
        if sectioners:
            self.__sectioners = __sectioners
        else:
            self.__sectioners = []
        if indextypecode:
            self.__indextypecode = indextypecode
        else:
            self.indextypecode = SdsTypeCode.DateTime
        self.__defaultstartindex = defaultstartindex
        self.__defaultendindex = defaultendindex
        self.__defaultinterval = defaultinterval
        if shape:
            self.__shape = shape
        else:
            self.shape = DataViewShapes.Standard

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
    def FieldSets(self):
        """

        :return:
        """
        return self.__fieldsets

    @FieldSets.setter
    def FieldSets(self, fieldsets):
        """
        :param fieldsets:
        :return:
        """
        self.__fieldsets = fieldsets

    @property
    def Sectioners(self):
        """
           not required
        :return:
        """
        return self.__sectioners

    @Sectioners.setter
    def Sectioners(self, sectioners):
        """
        DataViewindexConfig   not required
        :param sectioners:
        :return:
        """
        self.__sectioners = sectioners

    @property
    def IndexTypeCode(self):
        """
        :return:
        """
        return self.__indextypecode

    @IndexTypeCode.setter
    def IndexTypeCode(self, indextypecode):
        """
        Currently limited to "DateTime" string  required
        :param indexDataType:
        :return:
        """
        self.__indextypecode = indextypecode

    @property
    def DefaultStartIndex(self):
        """
        DefaultStartIndex   not required
        :return:
        """
        return self.__defaultstartindex

    @DefaultStartIndex.setter
    def DefaultStartIndex(self, defaultstartindex):
        """DefaultStartIndex
        DefaultStartIndex string  not required
        :param defaultstartindex:
        :return:
        """
        self.__defaultstartindex = defaultstartindex

    @property
    def DefaultEndIndex(self):
        """
        DefaultEndIndex string  not required
        :return:
        """
        return self.__defaultendindex

    @DefaultEndIndex.setter
    def DefaultEndIndex(self, defaultendindex):
        """DefaultEndIndex
        DefaultEndIndex  string not required
        :param defaultendindex:
        :return:
        """
        self.__defaultendindex = defaultendindex

    @property
    def DefaultInterval(self):
        """
        DefaultInterval string not required
        :return:
        """
        return self.__defaultinterval

    @DefaultInterval.setter
    def DefaultInterval(self, defaultinterval):
        """DefaultStartIndex
        DefaultInterval string not required
        :param groupRules:
        :return:
        """
        self.__defaultinterval = defaultinterval

    @property
    def Shape(self):
        """
        Shape string  not required
        :return:
        """
        return self.__shape

    @Shape.setter
    def Shape(self, shape):
        """DefaultStartIndex
        Shape string  not required
        :param groupRules:
        :return:
        """
        self.__shape = shape

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = {"Id": self.Id}

        # optional properties
        if hasattr(self, "Name"):
            dictionary["Name"] = self.Name

        if hasattr(self, "Description"):
            dictionary["Description"] = self.Description

        if hasattr(self, "Queries"):
            dictionary["Queries"] = []
            for value in self.Queries:
                dictionary["Queries"].append(value.toDictionary())

        if hasattr(self, "FieldSets"):
            dictionary["FieldSets"] = []
            for value in self.FieldSets:
                dictionary["FieldSets"].append(value.toDictionary())

        if hasattr(self, "Sectioners"):
            dictionary["Sectioners"] = []
            for value in self.Sectioners:
                dictionary["Sectioners"].append(value.toDictionary())

        if hasattr(self, "IndexTypeCode"):
            dictionary["IndexTypeCode"] = self.IndexTypeCode.name

        if hasattr(self, "DefaultStartIndex"):
            dictionary["DefaultStartIndex"] = self.DefaultStartIndex

        if hasattr(self, "DefaultEndIndex"):
            dictionary["DefaultEndIndex"] = self.DefaultEndIndex

        if hasattr(self, "DefaultInterval"):
            dictionary["DefaultInterval"] = self.DefaultInterval

        if hasattr(self, "Shape"):
            dictionary["Shape"] = self.Shape.name

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
            Queries = content["Queries"]
            if Queries is not None and len(Queries) > 0:
                dataView.Queries = []
                for value in Queries:
                    dataView.Queries.append(
                        Query.fromDictionary(value))

        if "FieldSets" in content:
            FieldSets = content["FieldSets"]
            if FieldSets is not None and len(FieldSets) > 0:
                dataView.FieldSets = []
                for value in FieldSets:
                    dataView.FieldSets.append(
                        FieldSet.fromDictionary(value))

        if "Sectioners" in content:
            Sectioners = content["Sectioners"]
            if Sectioners is not None and len(Sectioners) > 0:
                dataView.Sectioners = []
                for value in Sectioners:
                    dataView.Sectioners.append(
                        Field.fromDictionary(value))

        if "IndexTypeCode" in content:
            dataView.IndexTypeCode = SdsTypeCode[content['IndexTypeCode']]

        if "DefaultStartIndex" in content:
            dataView.DefaultStartIndex = content["DefaultStartIndex"]

        if "DefaultEndIndex" in content:
            dataView.DefaultEndIndex = content["DefaultEndIndex"]

        if "DefaultInterval" in content:
            dataView.DefaultInterval = content["DefaultInterval"]

        if "Shape" in content:
            dataView.Shape = DataViewShapes[content['Shape']]

        return dataView
