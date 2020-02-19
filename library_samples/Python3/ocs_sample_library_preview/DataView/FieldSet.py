import json
from .FieldSetSourceType import FieldSetSourceType
from .Field import Field


class FieldSet(object):

    def __init__(
        self,
        sourcetype=None,
        queryId=None,
        fields=None,
        distinguisher=None
    ):
        """

        :param sourcetype: required
        :param name: not required
        :param queryId: not required
        :param fields: not required
        :param distinguisher: not required
        """
        self.__sourcetype = sourcetype
        self.__queryId = queryId
        if fields:
            self.__fields = fields
        else:
            self.__fields = []
        self.__distinguisher = distinguisher

    @property
    def SourceType(self):
        """
        Get the sourcetype  required
        :return:
        """
        return self.__sourcetype

    @SourceType.setter
    def SourceType(self, sourcetype):
        """
        Set the sourcetype  required
        :param sourcetype:
        :return:
        """
        self.__sourcetype = sourcetype

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
    def Fields(self):
        """
        Get the fields  required
        :return:
        """
        return self.__fields

    @Fields.setter
    def Fields(self, fields):
        """
        Set the fields  required
        :param fields:
        :return:
        """
        self.__fields = fields

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
        dictionary = {'SourceType': self.SourceType.name}

        # optional properties
        if hasattr(self, 'QueryId'):
            dictionary['QueryId'] = self.QueryId

        if hasattr(self, "Fields"):
            dictionary["Fields"] = []
            for value in self.Fields:
                dictionary["Fields"].append(value.toDictionary())

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

        fieldSet.SourceType = FieldSetSourceType[content['SourceType']]

        if 'QueryId' in content:
            fieldSet.QueryId = content['QueryId']

        if "Fields" in content:
            Fields = content["Fields"]
            if Fields is not None and len(Fields) > 0:
                fieldSet.Fields = []
                for value in Fields:
                    fieldSet.Fields.append(
                        Field.fromDictionary(value))

        if 'Distinguisher' in content:
            fieldSet.Distinguisher = Field.fromDictionary(
                content['Distinguisher'])

        return fieldSet
