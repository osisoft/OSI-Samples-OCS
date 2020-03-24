import json


class DataItemField(object):

    def __init__(
        self,
        id=None,
        name=None,
        typeCode=None,
        isKey=None,
    ):
        """

        """
        self.__id = id
        self.__name = name
        self.__typeCode = typeCode
        self.__isKey = isKey

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

    @property
    def IsKey(self):
        """
        Get the isKey  required
        :return:
        """
        return self.__isKey

    @IsKey.setter
    def IsKey(self, isKey):
        """
        Set the isKey  required
        :param isKey:
        :return:
        """
        self.__isKey = isKey

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = {}

        # optional properties
        if hasattr(self, 'Id'):
            dictionary['Id'] = self.Id

        if hasattr(self, 'Name'):
            dictionary['Name'] = self.Name

        if hasattr(self, 'TypeCode'):
            dictionary['TypeCode'] = self.TypeCode

        if hasattr(self, 'IsKey'):
            dictionary['IsKey'] = self.IsKey

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return DataItemField.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        dataItem = DataItemField()

        if not content:
            return dataItem

        if 'Id' in content:
            dataItem.Id = content['Id']

        if 'Name' in content:
            dataItem.Name = content['Name']

        if 'TypeCode' in content:
            dataItem.TypeCode = content['TypeCode']

        if 'IsKey' in content:
            dataItem.IsKey = content['IsKey']

        return dataItem
