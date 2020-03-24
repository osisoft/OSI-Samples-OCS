import json
from .Field import Field


class FieldSet(object):

    def __init__(
        self,
        queryId=None,
        datafields=None,
        identifyingfield=None
    ):
        """

        :param queryId: not required
        :param datafields: not required
        :param identifyingfield: not required
        """
        self.__queryId = queryId
        if datafields:
            self.__datafields = datafields
        else:
            self.__datafields = []
        self.__identifyingfield = identifyingfield

    @property
    def QueryId(self):
        """
        Get the queryid  required
        :return:
        """
        return self.__queryid

    @QueryId.setter
    def QueryId(self, queryid):
        """
        Set the queryid  required
        :param queryid:
        :return:
        """
        self.__queryid = queryid

    @property
    def DataFields(self):
        """
        Get the fields  required
        :return:
        """
        return self.__datafields

    @DataFields.setter
    def DataFields(self, datafields):
        """
        Set the fields  required
        :param fields:
        :return:
        """
        self.__datafields = datafields

    @property
    def IdentifyingField(self):
        """
        Get the identifyingfield  required
        :return:
        """
        return self.__identifyingfield

    @IdentifyingField.setter
    def IdentifyingField(self, identifyingfield):
        """
        Set the identifyingfield  required
        :param identifyingfield:
        :return:
        """
        self.__identifyingfield = identifyingfield

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
