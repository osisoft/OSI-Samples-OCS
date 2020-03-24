import json
from .FieldKind  import FieldKind
from .DataMapping import DataMapping


class FieldMapping(object):

    def __init__(
        self,
        id=None,
        label=None,
        fieldKind=None,
        fieldSetIndex=None,
        fieldIndex=None,
        dataMappings=None
    ):
        """

        :param id: not required
        :param label: not required
        :param fieldKind: not required
        :param fieldSetIndex: not required
        :param fieldIndex: not required
        :param dataMappings: not required
        """
        self.__id = id
        self.__label= label
        if fieldKind:
            self.__fieldKind = fieldKind
        else:
            self.__fieldKind = FieldKind.IndexField
        self.__fieldSetIndex = fieldSetIndex
        self.__fieldIndex = fieldIndex
        self.__dataMappings = dataMappings

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

    @property
    def FieldKind(self):
        """
        Get the fieldKind  required
        :return:
        """
        return self.__fieldKind

    @FieldKind.setter
    def FieldKind(self, fieldKind):
        """
        Set the fieldKind  required
        :param fieldKind:
        :return:
        """
        self.__fieldKind = fieldKind

    @property
    def FieldSetIndex(self):
        """
        Get the fieldSetIndex  required
        :return:
        """
        return self.__fieldSetIndex

    @FieldSetIndex.setter
    def FieldSetIndex(self, fieldSetIndex):
        """
        Set the fieldSetIndex  required
        :param fieldSetIndex:
        :return:
        """
        self.__fieldSetIndex = fieldSetIndex

    @property
    def FieldIndex(self):
        """
        Get the fieldIndex  required
        :return:
        """
        return self.__fieldIndex

    @FieldIndex.setter
    def FieldIndex(self, fieldIndex):
        """
        Set the fieldIndex  required
        :param fieldIndex:
        :return:
        """
        self.__fieldIndex = fieldIndex

    @property
    def DataMappings(self):
        """
        Get the dataMappings  required
        :return:
        """
        return self.__dataMappings

    @DataMappings.setter
    def DataMappings(self, dataMappings):
        """
        Set the dataMappings  required
        :param dataMappings:
        :return:
        """
        self.__dataMappings = dataMappings

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = {}

        # optional properties
        if hasattr(self, 'Id'):
            dictionary['Id'] = self.Id

        if hasattr(self, 'Label'):
            dictionary['Label'] = self.Label

        if hasattr(self, 'FieldKind'):
            dictionary['FieldKind'] = self.FieldKind.name

        if hasattr(self, 'FieldSetIndex'):
            dictionary['FieldSetIndex'] = self.FieldSetIndex

        if hasattr(self, 'FieldIndex'):
            dictionary['FieldIndex'] = self.FieldIndex

        if hasattr(self, "DataMappings"):
            dictionary["DataMappings"] = []
            for value in self.DataMappings:
                dictionary["DataMappings"].append(value.toDictionary())

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return FieldMapping.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        fieldMapping = FieldMapping()

        if not content:
            return fieldMapping

        if 'Id' in content:
            fieldMapping.Id = content['Id']

        if 'Label' in content:
            fieldMapping.Label = content['Label']

        if 'FieldKind' in content:
            fieldMapping.FieldKind = FieldKind[content['FieldKind']] 

        if 'FieldSetIndex' in content:
            fieldMapping.FieldSetIndex = content['FieldSetIndex']

        if 'FieldIndex' in content:
            fieldMapping.FieldIndex = content['FieldIndex']

        if "DataMapping" in content:
            DataMapping_ = content["DataMapping"]
            if DataMapping_ is not None and len(DataMapping_) > 0:
                fieldMapping.DataFields = []
                for value in DataMapping_:
                    fieldMapping.DataFields.append(
                        DataMapping.fromDictionary(value))

        return fieldMapping
