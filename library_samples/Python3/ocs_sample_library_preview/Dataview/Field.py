import json
from .FieldSource import FieldSource


class Field(object):

    def __init__(
        self,
        source=None,
        keys=None,
        label=None,
    ):
        """

        :param source: not required
        :param keys: not required
        :param label: not required
        """
        self.__source = source
        if keys:
            self.__keys = keys
        else:
            self.__keys = []
        self.__label = label

    @property
    def Source(self):
        """
        Get the source  required
        :return:
        """
        return self.__source

    @Source.setter
    def Source(self, source):
        """
        Set the source  required
        :param source:
        :return:
        """
        self.__source = source

    @property
    def Keys(self):
        """
        Get the keys  required
        :return:
        """
        return self.__keys

    @Keys.setter
    def Keys(self, keys):
        """
        Set the keys  required
        :param keys:
        :return:
        """
        self.__keys = keys

    @property
    def Label(self):
        """
        Get the label  required
        :return:
        """
        return self.__label

    @Label.setter
    def Label(self, label):
        """
        Set the label  required
        :param label:
        :return:
        """
        self.__label = label

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = {}

        # optional properties
        if hasattr(self, 'Source'):
            if hasattr(self.Source, 'name'):
                dictionary['Source'] = self.Source.name
            else:
                dictionary['Source'] = self.Source

        if hasattr(self, "Keys"):
            dictionary["Keys"] = []
            for value in self.Keys:
                dictionary["Keys"].append(value)

        if hasattr(self, 'Label'):
            dictionary['Label'] = self.Label

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return Field.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        field = Field()

        if not content:
            return field

        if 'Source' in content:
            field.Source = FieldSource[content['Source']]

        if "Keys" in content:
            Keys = content["Keys"]
            if Keys is not None and len(Keys) > 0:
                field.Keys = []
                for value in Keys:
                    field.Keys.append(value)

        if 'Label' in content:
            field.Label = content['Label']

        return field
