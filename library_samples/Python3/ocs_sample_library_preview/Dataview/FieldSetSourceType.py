from enum import Enum


class FieldSetSourceType(Enum):
    """
    enum 0-2  fully inclusive
    """
    Index = 0
    SectionerValue = 1
    DataItem = 2
