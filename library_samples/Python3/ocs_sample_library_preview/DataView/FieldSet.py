import json
from .Field import Field


class FieldSet(object):

    def __init__(
        self,
        queryId=None,
        datafields=None,
        distinguisher=None
    ):
        """

        :param queryId: not required
        :param fields: not required
        :param distinguisher: not required
        """
        self.__queryId = queryId
        if datafields:
            self.__datafields = datafields
        else:
            self.__datafields = []
        self.__distinguisher = distinguisher

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

    @Fields.setter
    def DataFields(self, datafields):
        """
        Set the fields  required
        :param fields:
        :return:
        """
        self.__datafields = datafields

    @property
    def Distinguisher(self):
        """
        Get the distinguisher  required
        :return:
        """
        return self.__distinguisher

    @Distinguisher.setter
    def Distinguisher(self, distinguisher):
        """
        Set the distinguisher  required
        :param distinguisher:
        :return:
        """
        self.__distinguisher = distinguisher

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

        if hasattr(self, 'Distinguisher'):
            if self.Distinguisher is not None:
                dictionary['Distinguisher'] = self.Distinguisher.toDictionary()

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

        if 'Distinguisher' in content:
            fieldSet.Distinguisher = Field.fromDictionary(
                content['Distinguisher'])

        return fieldSet
