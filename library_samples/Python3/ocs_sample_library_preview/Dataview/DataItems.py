import json
from .DataItem import DataItem


class DataItems(object):

    def __init__(
        self,
        timeOfResolution=None,
        items=None
    ):
        """

        :param timeOfResolution: not required
        :param items: not required
        """
        self.__timeOfResolution = timeOfResolution
        if items:
            self.__items = items
        else:
            self.__items = []

    @property
    def TimeOfResolution(self):
        """
        Get the timeOfResolution  required
        :return:
        """
        return self.__timeOfResolution

    @TimeOfResolution.setter
    def TimeOfResolution(self, timeOfResolution):
        """
        Set the timeOfResolution  required
        :param timeOfResolution:
        :return:
        """
        self.__timeOfResolution = timeOfResolution

    @property
    def Items(self):
        """
        Get the items  required
        :return:
        """
        return self.__items

    @Items.setter
    def Items(self, items):
        """
        Set the items  required
        :param items:
        :return:
        """
        self.__items = items

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = {}

        # optional properties
        if hasattr(self, 'TimeOfResolution'):
            dictionary['TimeOfResolution'] = self.TimeOfResolution

        if hasattr(self, "Items"):
            dictionary["Items"] = []
            for value in self.Items:
                dictionary["Items"].append(value.toDictionary())

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return DataItems.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        dataItems = DataItems()

        if not content:
            return dataItems

        if 'TimeOfResolution' in content:
            dataItems.TimeOfResolution = content['TimeOfResolution']

        if "Items" in content:
            Items = content["Items"]
            if Items is not None and len(Items) > 0:
                dataItems.Items = []
                for value in Items:
                    dataItems.Items.append(
                        DataItem.fromDictionary(value))

        return dataItems
