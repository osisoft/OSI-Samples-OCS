import json
from .DataViewMappingColumn import DataViewMappingColumn


class DataViewMappings(object):

    def __init__(self, columns=None):

        self.__columns = columns

    @property
    def Columns(self):
        """
        array of DataViewMappingColumn   required  unless IsDefault is true
        :return:
        """
        return self.__columns

    @Columns.setter
    def Columns(self, columns):
        """
        array of DataViewMappingColumn   required  unless IsDefault is true
        :param columns:
        :return:
        """
        self.__columns = columns

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        dictionary = {}
        if hasattr(self, 'Columns') and self.Columns is not None:
            dictionary['Columns'] = []
            for value in self.Columns:
                dictionary['Columns'].append(value.toDictionary())

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return DataViewMappings.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        dataViewMapping = DataViewMappings()

        if not content:
            return dataViewMapping

        if 'Columns' in content:
            columns = content['Columns']
            if columns is not None and len(columns) > 0:
                dataViewMapping.Columns = []
                for value in columns:
                    dataViewMapping.Columns.append(
                        DataViewMappingColumn.fromDictionary(value))

        return dataViewMapping
