from enum import Enum


class FieldKind(Enum):
    """
    enum 0-2  fully inclusive
    """
    IndexField = 0
    GroupingField = 1
    DataField = 2
