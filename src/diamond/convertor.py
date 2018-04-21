# coding=utf-8

import re

_RE_FIND_FIRST_CAP = re.compile('(.)([A-Z][a-z]+)')
_RE_SPAN_OF_CAPS = re.compile('([a-z0-9])([A-Z])')
# Lists are in the order of increasing magnitude
_LIST_OF_UNITS_BIT = [['bit', 'b'],
                      ['kilobit', 'kbit', 'Kibit'],
                      ['megabit', 'Mbit', 'Mibit', 'Mbit'],
                      ['gigabit', 'Gbit', 'Gibit'],
                      ['terabit', 'Tbit', 'Tibit'],
                      ['petabit', 'Pbit', 'Pibit'],
                      ['exabit', 'Ebit', 'Eibit'],
                      ['zettabit', 'Zbit', 'Zibit'],
                      ['yottabit', 'Ybit', 'Yibit']]
_LIST_OF_UNITS_BYTE = [['byte', 'B'],
                       ['kilobyte', 'kB', 'KiB'],
                       ['megabyte', 'MB', 'MiB', 'Mbyte'],
                       ['gigabyte', 'GB', 'GiB'],
                       ['terabyte', 'TB', 'TiB'],
                       ['petabyte', 'PB', 'PiB'],
                       ['exabyte', 'EB', 'EiB'],
                       ['zettabyte', 'ZB', 'ZiB'],
                       ['yottabyte', 'YB', 'YiB']]


def camelcase_to_underscore(name):
    return _RE_SPAN_OF_CAPS.sub(r'\1_\2',
                                _RE_FIND_FIRST_CAP.sub(r'\1_\2', name)
                                ).lower()


class binary:
    """
    Store the value in bits so we can convert between things easily
    """
    value = None

    def __init__(self, value=None, unit=None):
        self.do(value=value, unit=unit)

    @staticmethod
    def convert(value=None, oldUnit=None, newUnit=None):
        convertor = binary(value=value, unit=oldUnit)
        return convertor.get(unit=newUnit)

    def set(self, value, unit=None):
        return self.do(value=value, unit=unit)

    def get(self, unit=None):
        return self.do(unit=unit)

    def _object_mapper(self, unit, value, mapping_list, object_type):
        for counter, units in enumerate(mapping_list):
            if unit in units:
                # returning self.type_of_unit
                return self.convertb(value, object_type, counter)
        return None

    def do(self, value=None, unit=None):
        if not unit:
            return self.bit(value=value)

        if unit in ['bit', 'b']:
            return self.bit(value=value)
        obj = self._object_mapper(unit, value, _LIST_OF_UNITS_BIT, self.bit)
        if not obj:
            return obj

        if unit in ['byte', 'B']:
            return self.byte(value=value)
        obj = self._object_mapper(unit, value, _LIST_OF_UNITS_BYTE, self.byte)
        if not obj:
            return obj

        raise NotImplementedError("unit %s" % unit)

    def bit(self, value=None):
        if value is not None:
            self.value = float(value)
        return self.value

    def convertb(self, value, source, offset=1):
        if value is None:
            return source() / pow(1024, offset)
        else:
            source(value * pow(1024, offset))

    def byte(self, value=None):
        if value is None:
            return self.value / 8
        else:
            self.value = float(value) * 8


class time:
    """
    Store the value in miliseconds so we can convert between things easily
    """
    value = None

    def __init__(self, value=None, unit=None):
        self.do(value=value, unit=unit)

    @staticmethod
    def convert(value=None, oldUnit=None, newUnit=None):
        convertor = time(value=value, unit=oldUnit)
        return convertor.get(unit=newUnit)

    def set(self, value, unit=None):
        return self.do(value=value, unit=unit)

    def get(self, unit=None):
        return self.do(unit=unit)

    def do(self, value=None, unit=None):
        if not unit:
            v = self.millisecond(value=value)
        elif unit.lower() in ['millisecond', 'milliseconds', 'ms']:
            v = self.millisecond(value=value)
        elif unit.lower() in ['second', 'seconds', 's']:
            v = self.second(value=value)
        elif unit.lower() in ['minute', 'minutes', 'm']:
            v = self.minute(value=value)
        elif unit.lower() in ['hour', 'hours', 'h']:
            v = self.hour(value=value)
        elif unit.lower() in ['day', 'days', 'd']:
            v = self.day(value=value)
        elif unit.lower() in ['year', 'years', 'y']:
            v = self.year(value=value)
        elif unit.lower() in ['microsecond', 'microseconds', 'us']:
            v = self.microsecond(value=value)
        elif unit.lower() in ['nanosecond', 'nanoseconds', 'ns']:
            v = self.nanosecond(value=value)
        else:
            raise NotImplementedError("unit %s" % unit)

        return v

    def millisecond(self, value=None):
        if value is None:
            return self.value
        else:
            self.value = float(value)

    def second(self, value=None):
        if value is None:
            return self.millisecond() / 1000
        else:
            self.millisecond(value * 1000)

    def minute(self, value=None):
        if value is None:
            return self.second() / 60
        else:
            self.millisecond(self.second(value * 60))

    def hour(self, value=None):
        if value is None:
            return self.minute() / 60
        else:
            self.millisecond(self.minute(value * 60))

    def day(self, value=None):
        if value is None:
            return self.hour() / 24
        else:
            self.millisecond(self.hour(value * 24))

    def year(self, value=None):
        """
        We do *NOT* know for what year we are converting so lets assume the
        year has 365 days.
        """
        if value is None:
            return self.day() / 365
        else:
            self.millisecond(self.day(value * 365))

    def microsecond(self, value=None):
        if value is None:
            return self.millisecond() * 1000
        else:
            self.millisecond(value / 1000)

    def nanosecond(self, value=None):
        if value is None:
            return self.microsecond() * 1000
        else:
            self.millisecond(self.microsecond(value / 1000))
