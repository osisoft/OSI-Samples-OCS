import json
from .Field import Field


class FieldSet(object):

    def __init__(
        self,
        queryId=None,
        dataFields=None,
        identifyingField=None
    ):
        """
        :param queryId: not required
        :param dataFields: not required
        :param identifyingField: not required
        """
        self.__queryId = queryId
        if dataFields:
            self.__dataFields = dataFields
        else:
            self.__dataFields = []
        self.__identifyingField = identifyingField

    @property
    def QueryId(self):
        """
        Get the queryId  required
        :return:
        """
        return self.__queryId

    @QueryId.setter
    def QueryId(self, queryId):
        """
        Set the queryId  required
        :param queryId:
        :return:
        """
        self.__queryId = queryId

    @property
    def DataFields(self):
        """
        Get the dataFields  required
        :return:
        """
        return self.__dataFields

    @DataFields.setter
    def DataFields(self, dataFields):
        """
        Set the dataFields  required
        :param dataFields:
        :return:
        """
        self.__dataFields = dataFields

    @property
    def IdentifyingField(self):
        """
        Get the identifyingField  required
        :return:
        """
        return self.__identifyingField

    @IdentifyingField.setter
    def IdentifyingField(self, identifyingField):
        """
        Set the identifyingField  required
        :param identifyingField:
        :return:
        """
        self.__identifyingField = identifyingField

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = {}

        # optional properties
        if hasattr(self, 'QueryId'):
            dictionary['QueryId'] = self.QueryId

        if hasattr(self, "DataFields"):
            dictionary["DataFields"] = []
            for value in self.DataFields:
                dictionary["DataFields"].append(value.toDictionary())

        if hasattr(self, 'IdentifyingField'):
            if self.IdentifyingField is not None:
                dictionary['IdentifyingField'] = self.IdentifyingField.toDictionary()

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return FieldSet.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        fieldSet = FieldSet()

        if not content:
            return fieldSet

        if 'QueryId' in content:
            fieldSet.QueryId = content['QueryId']

        if "DataFields" in content:
            DataFields = content["DataFields"]
            if DataFields is not None and len(DataFields) > 0:
                fieldSet.DataFields = []
                for value in DataFields:
                    fieldSet.DataFields.append(
                        Field.fromDictionary(value))

        if 'IdentifyingField' in content:
            fieldSet.IdentifyingField = Field.fromDictionary(
                content['IdentifyingField'])

        return fieldSet
