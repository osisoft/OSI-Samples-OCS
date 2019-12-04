import json


class DataViewMappingColumn(object):

    """Sds DataView definition"""
    @property
    def Name(self):
        """
        Name   required
        :return:
        """
        return self.__name

    @Name.setter
    def Name(self, name):
        """
        Name   required
        :param name:
        :return:
        """
        self.__name = name

    @property
    def IsKey(self):
        """
        Bool    required   required one true in columns set
        :return:
        """
        return self.__isKey

    @IsKey.setter
    def IsKey(self, isKey):
        """
        Bool    required   required one true in columns set
        :param isKey:
        :return:
        """
        self.__isKey = isKey

    @property
    def DataType(self):
        """
        type of the mapped data source   not required
        :return:
        """
        return self.__dataType

    @DataType.setter
    def DataType(self, dataType):
        """
        type of the mapped data source   not required
        :param dataType:
        :return:
        """
        self.__dataType = dataType

    @property
    def MappingRule(self):
        """
        Mapping to the data source   required
        :return:
        """
        return self.__MappingRule

    @MappingRule.setter
    def MappingRule(self, MappingRule):
        """
        Mapping to the data source   required
        :param MappingRule:
        :return:
        """
        self.__MappingRule = MappingRule

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = {'Name': self.Name}
        dictionary['IsKey'] = self.IsKey

        if hasattr(self, 'DataType'):
            dictionary['DataType'] = self.DataType

        if hasattr(self, 'MappingRule'):
            dictionary['MappingRule'] = self.MappingRule

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return DataViewMappingColumn.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        dataViewMappingColumn = DataViewMappingColumn()

        if not content:
            return dataViewMappingColumn

        if 'Name' in content:
            dataViewMappingColumn.Name = content['Name']

        if 'IsKey' in content:
            dataViewMappingColumn.IsKey = content['IsKey']
        else:
            dataViewMappingColumn.IsKey = False

        if 'DataType' in content:
            dataViewMappingColumn.DataType = content['DataType']

        if 'MappingRule' in content:
            dataViewMappingColumn.MappingRule = content['MappingRule']

        return dataViewMappingColumn
