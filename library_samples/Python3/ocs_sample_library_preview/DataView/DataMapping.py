import json
from .Field import Field


class DataMapping(object):

    def __init__(
        self,
        targetId=None,
        targetFieldKey=None,
        typeCode=None
    ):
        """
        :param targetId: not required
        :param targetFieldKey: not required
        :param typeCode: not required
        """
        self.__targetId = targetId
        self.__targetFieldKey = targetFieldKey
        self.__typeCode = typeCode

    @property
    def TargetId(self):
        """
        Get the targetId  required
        :return:
        """
        return self.__targetId

    @TargetId.setter
    def TargetId(self, targetId):
        """
        Set the __targetId  required
        :param __targetId:
        :return:
        """
        self.__targetId= targetId

    @property
    def TargetFieldKey(self):
        """
        Get the targetFieldKey  required
        :return:
        """
        return self.__targetFieldKey

    @TargetFieldKey.setter
    def TargetFieldKey(self, targetFieldKey):
        """
        Set the targetFieldKey  required
        :param targetFieldKey:
        :return:
        """
        self.__targetFieldKey = targetFieldKey

    @property
    def TypeCode(self):
        """
        Get the typeCode  required
        :return:
        """
        return self.__typeCode

    @TypeCode.setter
    def TypeCode(self, typeCode):
        """
        Set the typeCode  required
        :param typeCode:
        :return:
        """
        self.__typeCode = typeCode

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = {}

        # optional properties
        if hasattr(self, 'TargetId'):
            dictionary['TargetId'] = self.TargetId

        if hasattr(self, 'TargetFieldKey'):
            dictionary['TargetFieldKey'] = self.TargetFieldKey

        if hasattr(self, 'TypeCode'):
            dictionary['TypeCode'] = self.TypeCode

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return DataMapping.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        dataMapping = DataMapping()

        if not content:
            return dataMapping

        if 'TargetId' in content:
            dataMapping.TargetId = content['TargetId']            

        if 'TargetFieldKey' in content:
            dataMapping.TargetFieldKey = content['TargetFieldKey']            

        if 'TypeCode' in content:
            dataMapping.TypeCode = content['TypeCode']

        return dataMapping
