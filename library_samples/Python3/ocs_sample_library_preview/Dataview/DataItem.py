import json
from .DataItemField import DataItemField


class DataItem(object):

    def __init__(
        self,
        resourceType=None,
        id=None,
        name=None,
        typeId=None,
        tags=None,
        metadata=None,
        dataItemFields=None
    ):
        """

        """
        self.__resourceType = resourceType
        self.__id = id
        self.__name = name
        self.__typeId = typeId

        if tags:
            self.__tags = tags
        else:
            self.__tags = []

        self.__metadata = metadata

        if dataItemFields:
            self.__dataItemFields = dataItemFields
        else:
            self.__dataItemFields = []

    @property
    def ResourceType(self):
        """
        Get the resourceType  required
        :return:
        """
        return self.__resourceType

    @ResourceType.setter
    def ResourceType(self, resourceType):
        """
        Set the resourceType  required
        :param resourceType:
        :return:
        """
        self.__resourceType = resourceType

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
        Get the name  required
        :return:
        """
        return self.__name

    @Name.setter
    def Name(self, name):
        """
        Set the name  required
        :param name:
        :return:
        """
        self.__name = name

    @property
    def TypeId(self):
        """
        Get the typeId  required
        :return:
        """
        return self.__typeId

    @TypeId.setter
    def TypeId(self, typeId):
        """
        Set the typeId  required
        :param typeId:
        :return:
        """
        self.__typeId = typeId

    @property
    def Tags(self):
        """
        Get the tags  required
        :return:
        """
        return self.__tags

    @Tags.setter
    def Tags(self, tags):
        """
        Set the tags  required
        :param tags:
        :return:
        """
        self.__tags = tags

    @property
    def Metadata(self):
        """
        Get the metadata  required
        :return:
        """
        return self.__metadata

    @Metadata.setter
    def Metadata(self, metadata):
        """
        Set the metadata  required
        :param metadata:
        :return:
        """
        self.__metadata = metadata

    @property
    def DataItemFields(self):
        """
        Get the dataItemFields  required
        :return:
        """
        return self.__dataItemFields

    @DataItemFields.setter
    def DataItemFields(self, dataItemFields):
        """
        Set the dataItemFields  required
        :param dataItemFields:
        :return:
        """
        self.__dataItemFields = dataItemFields

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = {}

        # optional properties
        if hasattr(self, 'ResourceType'):
            dictionary['ResourceType'] = self.ResourceType

        if hasattr(self, 'Id'):
            dictionary['Id'] = self.Id

        if hasattr(self, 'Name'):
            dictionary['Name'] = self.Name

        if hasattr(self, 'TypeId'):
            dictionary['TypeId'] = self.TypeId

        if hasattr(self, "Tags"):
            dictionary["Tags"] = []
            for value in self.Tags:
                dictionary["Tags"].append(value)

        if hasattr(self, 'Metadata'):
            # this is an object of some form we need to deal with better #fixit
            dictionary['Metadata'] = self.Metadata

        if hasattr(self, "DataItemFields"):
            dictionary["DataItemFields"] = []
            for value in self.DataItemFields:
                dictionary["DataItemFields"].append(value.toDictionary())

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return DataItem.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        dataItem = DataItem()

        if not content:
            return dataItem

        if 'ResourceType' in content:
            dataItem.ResourceType = content['ResourceType']

        if 'Id' in content:
            dataItem.Id = content['Id']

        if 'Name' in content:
            dataItem.Name = content['Name']

        if 'TypeId' in content:
            dataItem.TypeId = content['TypeId']

        if "Tags" in content:
            Tags = content["Tags"]
            if Tags is not None and len(Tags) > 0:
                dataItem.Tags = []
                for value in Tags:
                    dataItem.Tags.append(value)

        if 'Metadata' in content:
            # this is an object of some form we need to deal with better #fixit
            dataItem.Metadata = content['Metadata']

        if "DataItemFields" in content:
            DataItemFields = content["DataItemFields"]
            if DataItemFields is not None and len(DataItemFields) > 0:
                dataItem.DataItemFields = []
                for value in DataItemFields:
                    dataItem.DataItemFields.append(
                        DataItemField.fromDictionary(value))

        return dataItem
