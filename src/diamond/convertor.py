# coding=utf-8

import re

_RE_FIND_FIRST_CAP = re.compile('(.)([A-Z][a-z]+)')
_RE_SPAN_OF_CAPS = re.compile('([a-z0-9])([A-Z])')


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

    def do(self, value=None, unit=None):
        if not unit:
            return self.bit(value=value)

        if unit in ['bit', 'b']:
            return self.bit(value=value)
        if unit in ['kilobit', 'kbit', 'Kibit']:
            return self.kilobit(value=value)
        if unit in ['megabit', 'Mbit', 'Mibit', 'Mbit']:
            return self.megabit(value=value)
        if unit in ['gigabit', 'Gbit', 'Gibit']:
            return self.gigabit(value=value)
        if unit in ['terabit', 'Tbit', 'Tibit']:
            return self.terabit(value=value)
        if unit in ['petabit', 'Pbit', 'Pibit']:
            return self.petabit(value=value)
        if unit in ['exabit', 'Ebit', 'Eibit']:
            return self.exabit(value=value)
        if unit in ['zettabit', 'Zbit', 'Zibit']:
            return self.zettabit(value=value)
        if unit in ['yottabit', 'Ybit', 'Yibit']:
            return self.yottabit(value=value)

        if unit in ['byte', 'B']:
            return self.byte(value=value)
        if unit in ['kilobyte', 'kB', 'KiB']:
            return self.kilobyte(value=value)
        if unit in ['megabyte', 'MB', 'MiB', 'Mbyte']:
            return self.megabyte(value=value)
        if unit in ['gigabyte', 'GB', 'GiB']:
            return self.gigabyte(value=value)
        if unit in ['terabyte', 'TB', 'TiB']:
            return self.terabyte(value=value)
        if unit in ['petabyte', 'PB', 'PiB']:
            return self.petabyte(value=value)
        if unit in ['exabyte', 'EB', 'EiB']:
            return self.exabyte(value=value)
        if unit in ['zettabyte', 'ZB', 'ZiB']:
            return self.zettabyte(value=value)
        if unit in ['yottabyte', 'YB', 'YiB']:
            return self.yottabyte(value=value)

        raise NotImplementedError("unit %s" % unit)

    def bit(self, value=None):
        if value is None:
            return self.value
        else:
            self.value = float(value)

    def convertb(self, value, source, offset=1):
        if value is None:
            return source() / pow(1024, offset)
        else:
            source(value * pow(1024, offset))

    def kilobit(self, value=None):
        return self.convertb(value, self.bit)

    def megabit(self, value=None):
        return self.convertb(value, self.bit, 2)

    def gigabit(self, value=None):
        return self.convertb(value, self.bit, 3)

    def terabit(self, value=None):
        return self.convertb(value, self.bit, 4)

    def petabit(self, value=None):
        return self.convertb(value, self.bit, 5)

    def exabit(self, value=None):
        return self.convertb(value, self.bit, 6)

    def zettabit(self, value=None):
        return self.convertb(value, self.bit, 7)

    def yottabit(self, value=None):
        return self.convertb(value, self.bit, 8)

    def byte(self, value=None):
        if value is None:
            return self.value / 8
        else:
            self.value = float(value) * 8

    def kilobyte(self, value=None):
        return self.convertb(value, self.byte)

    def megabyte(self, value=None):
        return self.convertb(value, self.byte, 2)

    def gigabyte(self, value=None):
        return self.convertb(value, self.byte, 3)

    def terabyte(self, value=None):
        return self.convertb(value, self.byte, 4)

    def petabyte(self, value=None):
        return self.convertb(value, self.byte, 5)

    def exabyte(self, value=None):
        return self.convertb(value, self.byte, 6)

    def zettabyte(self, value=None):
        return self.convertb(value, self.byte, 7)

    def yottabyte(self, value=None):
        return self.convertb(value, self.byte, 8)


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
