"""WaveData type definitions for SDS Python sample"""

import json
import inspect


class WaveData:
    """Represents a data point to be injected into Sds Service"""

    def __init__(self):
        self._order = None
        self._tau = None
        self._radians = None
        self._sin = None
        self._cos = None
        self._tan = None
        self._sinh = None
        self._cosh = None
        self._tanh = None

    @property
    def order(self):
        """Sets the property value"""
        return self._order

    @order.setter
    def order(self, order):
        self._order = order

    @property
    def tau(self):
        """Sets the property value"""
        return self._tau

    @tau.setter
    def tau(self, tau):
        self._tau = tau

    @property
    def radians(self):
        """Sets the property value"""
        return self._radians

    @radians.setter
    def radians(self, radians):
        self._radians = radians

    @property
    def sin(self):
        """Sets the property value"""
        return self._sin

    @sin.setter
    def sin(self, sin):
        self._sin = sin

    @property
    def cos(self):
        """Sets the property value"""
        return self._cos

    @cos.setter
    def cos(self, cos):
        self._cos = cos

    @property
    def tan(self):
        """Sets the property value"""
        return self._tan

    @tan.setter
    def tan(self, tan):
        self._tan = tan

    @property
    def sinh(self):
        """Sets the property value"""
        return self._sinh

    @sinh.setter
    def sinh(self, sinh):
        self._sinh = sinh

    @property
    def cosh(self):
        """Sets the property value"""
        return self._cosh

    @cosh.setter
    def cosh(self, cosh):
        self._cosh = cosh

    @property
    def tanh(self):
        """Sets the property value"""
        return self._tanh

    @tanh.setter
    def tanh(self, tanh):
        self._tanh = tanh

    def isprop(self):
        """Check whether a field is a property of an object"""
        return isinstance(self, property)

    def toJson(self):
        """Converts the object into JSON"""
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        """Converts the object into a dictionary"""
        dictionary = {}
        for prop in inspect.getmembers(type(self),
                                       lambda v: isinstance(v, property)):
            if hasattr(self, prop[0]):
                dictionary[prop[0]] = prop[1].fget(self)

        return dictionary

    @staticmethod
    def fromJson(json_obj):
        """Creates the object from JSON"""
        return WaveData.fromDictionary(json_obj)

    @staticmethod
    def fromDictionary(content):
        """Creates the object from a dictionary"""
        wave = WaveData()

        if len(content) == 0:
            return wave

        for prop in inspect.getmembers(type(wave),
                                       lambda v: isinstance(v, property)):
            # Pre-Assign the default
            prop[1].fset(wave, 0)

            # If found in JSON object, then set
            if prop[0] in content:
                value = content[prop[0]]
                if value is not None:
                    prop[1].fset(wave, value)

        return wave


class WaveDataInteger:
    """Represents a data point to be injected into Sds Service"""

    def __init__(self):
        self._order_target = None
        self._sin_int = None
        self._cos_int = None
        self._tan_int = None

    @property
    def order_target(self):
        """Sets the property value"""
        return self._order_target

    @order_target.setter
    def order_target(self, order_target):
        self._order_target = order_target

    @property
    def sin_int(self):
        """Sets the property value"""
        return self._sin_int

    @sin_int.setter
    def sin_int(self, sin_int):
        self._sin_int = sin_int

    @property
    def cos_int(self):
        """Sets the property value"""
        return self._cos_int

    @cos_int.setter
    def cos_int(self, cos_int):
        self._cos_int = cos_int

    @property
    def tan_int(self):
        """Sets the property value"""
        return self._tan_int

    @tan_int.setter
    def tan_int(self, tan_int):
        self._tan_int = tan_int

    def isprop(self):
        """Check whether a field is a property of an object"""
        return isinstance(self, property)

    def toJson(self):
        """Converts the object into JSON"""
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        """Converts the object into a dictionary"""
        dictionary = {}
        for prop in inspect.getmembers(type(self),
                                       lambda v: isinstance(v, property)):
            if hasattr(self, prop[0]):
                dictionary[prop[0]] = prop[1].fget(self)

        return dictionary

    @staticmethod
    def fromJson(json_obj):
        """Creates the object from JSON"""
        return WaveDataInteger.fromDictionary(json_obj)

    @staticmethod
    def fromDictionary(content):
        """Creates the object from a dictionary"""
        wave = WaveDataInteger()

        if len(content) == 0:
            return wave

        for prop in inspect.getmembers(type(wave),
                                       lambda v: isinstance(v, property)):
            # Pre-Assign the default
            prop[1].fset(wave, 0)

            # If found in JSON object, then set
            if prop[0] in content:
                value = content[prop[0]]
                if value is not None:
                    prop[1].fset(wave, value)
        return wave


class WaveDataTarget:
    """Represents a data point to be injected into Sds Service"""

    def __init__(self):
        self._order_target = None
        self._tau_target = None
        self._radians_target = None
        self._sin_target = None
        self._cos_target = None
        self._tan_target = None
        self._sinh_target = None
        self._cosh_target = None
        self._tanh_target = None

    @property
    def order_target(self):
        """Sets the property value"""
        return self._order_target

    @order_target.setter
    def order_target(self, order_target):
        self._order_target = order_target

    @property
    def tau_target(self):
        """Sets the property value"""
        return self._tau_target

    @tau_target.setter
    def tau_target(self, tau_target):
        self._tau_target = tau_target

    @property
    def radians_target(self):
        """Sets the property value"""
        return self._radians_target

    @radians_target.setter
    def radians_target(self, radians_target):
        self._radians_target = radians_target

    @property
    def sin_target(self):
        """Sets the property value"""
        return self._sin_target

    @sin_target.setter
    def sin_target(self, sin_target):
        self._sin_target = sin_target

    @property
    def cos_target(self):
        """Sets the property value"""
        return self._cos_target

    @cos_target.setter
    def cos_target(self, cos_target):
        self._cos_target = cos_target

    @property
    def tan_target(self):
        """Sets the property value"""
        return self._tan_target

    @tan_target.setter
    def tan_target(self, tan_target):
        self._tan_target = tan_target

    @property
    def sinh_target(self):
        """Sets the property value"""
        return self._sinh_target

    @sinh_target.setter
    def sinh_target(self, sinh_target):
        self._sinh_target = sinh_target

    @property
    def cosh_target(self):
        """Sets the property value"""
        return self._cosh_target

    @cosh_target.setter
    def cosh_target(self, cosh_target):
        self._cosh_target = cosh_target

    @property
    def tanh_target(self):
        """Sets the property value"""
        return self._tanh_target

    @tanh_target.setter
    def tanh_target(self, tanh_target):
        self._tanh_target = tanh_target

    def isprop(self):
        """Check whether a field is a property of an object"""
        return isinstance(self, property)

    def toJson(self):
        """Converts the object into JSON"""
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        """Converts the object into a dictionary"""
        dictionary = {}
        for prop in inspect.getmembers(type(self),
                                       lambda v: isinstance(v, property)):
            if hasattr(self, prop[0]):
                dictionary[prop[0]] = prop[1].fget(self)

        return dictionary

    @staticmethod
    def fromJson(json_obj):
        """Creates the object from JSON"""
        return WaveDataTarget.fromDictionary(json_obj)

    @staticmethod
    def fromDictionary(content):
        """Creates the object from a dictionary"""
        wave = WaveDataTarget()

        if len(content) == 0:
            return wave

        for prop in inspect.getmembers(type(wave),
                                       lambda v: isinstance(v, property)):
            # Pre-Assign the default
            prop[1].fset(wave, 0)

            # If found in JSON object, then set
            if prop[0] in content:
                value = content[prop[0]]
                if value is not None:
                    prop[1].fset(wave, value)

        return wave


class WaveDataCompound:
    """Represents a data point to be injected into Sds Service"""

    def __init__(self):
        self._order = None
        self._multiplier = None
        self._tau = None
        self._radians = None
        self._sin = None
        self._cos = None
        self._tan = None
        self._sinh = None
        self._cosh = None
        self._tanh = None

    @property
    def order(self):
        """Sets the property value"""
        return self._order

    @order.setter
    def order(self, order):
        self._order = order

    @property
    def multiplier(self):
        """Sets the property value"""
        return self._multiplier

    @multiplier.setter
    def multiplier(self, multiplier):
        self._multiplier = multiplier

    @property
    def tau(self):
        """Sets the property value"""
        return self._tau

    @tau.setter
    def tau(self, tau):
        self._tau = tau

    @property
    def radians(self):
        """Sets the property value"""
        return self._radians

    @radians.setter
    def radians(self, radians):
        self._radians = radians

    @property
    def sin(self):
        """Sets the property value"""
        return self._sin

    @sin.setter
    def sin(self, sin):
        self._sin = sin

    @property
    def cos(self):
        """Sets the property value"""
        return self._cos

    @cos.setter
    def cos(self, cos):
        self._cos = cos

    @property
    def tan(self):
        """Sets the property value"""
        return self._tan

    @tan.setter
    def tan(self, tan):
        self._tan = tan

    @property
    def sinh(self):
        """Sets the property value"""
        return self._sinh

    @sinh.setter
    def sinh(self, sinh):
        self._sinh = sinh

    @property
    def cosh(self):
        """Sets the property value"""
        return self._cosh

    @cosh.setter
    def cosh(self, cosh):
        self._cosh = cosh

    @property
    def tanh(self):
        """Sets the property value"""
        return self._tanh

    @tanh.setter
    def tanh(self, tanh):
        self._tanh = tanh

    def isprop(self):
        """Check whether a field is a property of an object"""
        return isinstance(self, property)

    def toJson(self):
        """Converts the object into JSON"""
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        """Converts the object into a dictionary"""
        dictionary = {}
        for prop in inspect.getmembers(type(self),
                                       lambda v: isinstance(v, property)):
            if hasattr(self, prop[0]):
                dictionary[prop[0]] = prop[1].fget(self)

        return dictionary

    @staticmethod
    def fromJson(json_obj):
        """Creates the object from JSON"""
        return WaveData.fromDictionary(json_obj)

    @staticmethod
    def fromDictionary(content):
        """Creates the object from a dictionary"""
        wave = WaveData()

        if len(content) == 0:
            return wave

        for prop in inspect.getmembers(type(wave),
                                       lambda v: isinstance(v, property)):
            # Pre-Assign the default
            prop[1].fset(wave, 0)

            # If found in JSON object, then set
            if prop[0] in content:
                value = content[prop[0]]
                if value is not None:
                    prop[1].fset(wave, value)

        return wave
