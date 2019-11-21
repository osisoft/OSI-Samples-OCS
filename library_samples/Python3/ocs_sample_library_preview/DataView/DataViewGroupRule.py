import json


class DataViewGroupRule(object):
    """
    DataViewGroupRule
    """

    def __init__(self, id=None, resource="Streams", field=None, values=[]):
        self.__id = id
        self.__resource = resource
        self.__field = field
        self.__values = values

    @property
    def Id(self):
        """
        unique id   required
        :return:
        """
        return self.__id

    @Id.setter
    def Id(self, id):
        """
        unique id   required
        :param id:
        :return:
        """
        self.__id = id

    @property
    def Resource(self):
        """
        Resource   required
        :return:
        """
        return self.__resource

    @Id.setter
    def Resource(self, resource):
        """
        Resource   required
        :param resource:
        :return:
        """
        self.__resource = resource

    @property
    def Field(self):
        """
        Stream property to base grouping on   not required
        :return:
        """
        return self.__field

    @Field.setter
    def Field(self, field):
        """
        Stream property to base grouping on   not required
        :param field:
        :return:
        """
        self.__field = field

    @property
    def Values(self):
        """
        Values that create patterns for groups  not required
        :return:
        """
        return self.__values

    @Values.setter
    def Values(self, values):
        """
        Values that create patterns for groups  not required
        :param values:
        :return:
        """
        self.__values = values

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = {'Id': self.Id, 'Resource': self.Resource}

        if hasattr(self, 'Field'):
            dictionary['Field'] = self.Field

        if hasattr(self, 'Values'):
            dictionary['Values'] = self.Values

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return DataViewGroupRule.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        dataViewGroupRule = DataViewGroupRule()

        if not content:
            return dataViewGroupRule

        if 'Id' in content:
            dataViewGroupRule.Id = content['Id']

        if 'Resource' in content:
            dataViewGroupRule.Resource = content['Resource']

        if 'Field' in content:
            dataViewGroupRule.Field = content['Field']

        if 'Values' in content:
            dataViewGroupRule.Values = content['Values']

        return dataViewGroupRule
