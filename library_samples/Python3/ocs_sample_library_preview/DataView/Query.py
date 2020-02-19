import json


class Query(object):

    def __init__(
        self,
        id=None,
        value=None
    ):
        """

        :param id: required
        :param value: not required
        """
        self.__id = id
        self.__value = value

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
    def Value(self):
        """
        Get the value  required
        :return:
        """
        return self.__value

    @Value.setter
    def Value(self, value):
        """
        Set the value  required
        :param value:
        :return:
        """
        self.__value = value

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = {'Id': self.Id}

        # optional properties
        if hasattr(self, 'Value'):
            dictionary['Value'] = self.Value

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return Query.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        query = Query()

        if not content:
            return query

        if 'Id' in content:
            query.Id = content['Id']

        if 'Value' in content:
            query.Value = content['Value']

        return query
