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
        indexField=None,
        dataFieldSets=None,
        groupingFields=None,
        indexTypeCode=None,
        defaultStartIndex=None,
        defaultEndIndex=None,
        defaultInterval=None,
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
        self.__indexField = indexField
        if dataFieldSets:
            self.__dataFieldSets = dataFieldSets
        else:
            self.__dataFieldSets = []
        if groupingFields:
            self.__groupingFields = groupingFields
        else:
            self.__groupingFields = []
        if indexTypeCode:
            self.__indexTypeCode = indexTypeCode
        else:
            self.indexTypeCode = SdsTypeCode.DateTime
        self.__defaultStartIndex = defaultStartIndex
        self.__defaultEndIndex = defaultEndIndex
        self.__defaultInterval = defaultInterval
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
        Add an easy to understand description not required
        :return:
        """
        return self.__description

    @Description.setter
    def Description(self, description):
        """
        Add an easy to understand description not required
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
        Array of queries  required
        :param queries:
        :return:
        """
        self.__queries = queries

    @property
    def IndexField (self):
        """
        IndexField field  required
        :return:
        """
        return self.__indexField

    @IndexField.setter
    def IndexField(self, indexField):
        """
        Field indexField  required
        :param indexField:
        :return:
        """
        self.__indexField = indexField

    @property
    def DataFieldSets(self):
        """
        :return:
        """
        return self.__dataFieldSets

    @DataFieldSets.setter
    def DataFieldSets(self, dataFieldSets):
        """
        :param dataFieldSets:
        :return:
        """
        self.__dataFieldSets = dataFieldSets

    @property
    def GroupingFields(self):
        """
        :return:
        """
        return self.__groupingFields

    @GroupingFields.setter
    def GroupingFields(self, groupingFields):
        """
        Array of fields   not required
        :param groupingFields:
        :return:
        """
        self.__groupingFields = groupingFields

    @property
    def IndexTypeCode(self):
        """
        :return:
        """
        return self.__indexTypeCode

    @IndexTypeCode.setter
    def IndexTypeCode(self, indexTypeCode):
        """
        Currently limited to "DateTime" string  required
        :param indexTypeCode:
        :return:
        """
        self.__indexTypeCode = indexTypeCode

    @property
    def DefaultStartIndex(self):
        """
        DefaultStartIndex   not required
        :return:
        """
        return self.__defaultStartIndex

    @DefaultStartIndex.setter
    def DefaultStartIndex(self, defaultStartIndex):
        """DefaultStartIndex
        DefaultStartIndex string  not required
        :param defaultStartIndex:
        :return:
        """
        self.__defaultStartIndex = defaultStartIndex

    @property
    def DefaultEndIndex(self):
        """
        DefaultEndIndex string  not required
        :return:
        """
        return self.__defaultEndIndex

    @DefaultEndIndex.setter
    def DefaultEndIndex(self, defaultEndIndex):
        """DefaultEndIndex
        DefaultEndIndex  string not required
        :param defaultEndIndex:
        :return:
        """
        self.__defaultEndIndex = defaultEndIndex

    @property
    def DefaultInterval(self):
        """
        DefaultInterval string not required
        :return:
        """
        return self.__defaultInterval

    @DefaultInterval.setter
    def DefaultInterval(self, defaultInterval):
        """DefaultStartIndex
        DefaultInterval string not required
        :param defaultInterval:
        :return:
        """
        self.__defaultInterval = defaultInterval

    @property
    def Shape(self):
        """
        Shape string  not required
        :return:
        """
        return self.__shape

    @Shape.setter
    def Shape(self, shape):
        """
        Shape string  not required
        :param shape:
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

        if hasattr(self, "DataFieldSets"):
            dictionary["DataFieldSets"] = []
            for value in self.DataFieldSets:
                dictionary["DataFieldSets"].append(value.toDictionary())

        if hasattr(self, "GroupingFields"):
            dictionary["GroupingFields"] = []
            for value in self.GroupingFields:
                dictionary["GroupingFields"].append(value.toDictionary())

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

        if "DataFieldSets" in content:
            DataFieldSets = content["DataFieldSets"]
            if DataFieldSets is not None and len(DataFieldSets) > 0:
                dataView.DataFieldSets = []
                for value in DataFieldSets:
                    dataView.DataFieldSets.append(
                        FieldSet.fromDictionary(value))

        if "GroupingFields" in content:
            GroupingFields = content["GroupingFields"]
            if GroupingFields is not None and len(GroupingFields) > 0:
                dataView.GroupingFields = []
                for value in GroupingFields:
                    dataView.GroupingFields.append(
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
