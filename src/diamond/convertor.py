# Copyright (C) 2011-2012 by Ivan Pouzyrevsky.
# Copyright (C) 2010-2011 by Brightcove Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from diamond import *

_RE_FIND_FIRST_CAP = re.compile('(.)([A-Z][a-z]+)')
_RE_SPAN_OF_CAPS = re.compile('([a-z0-9])([A-Z])')

def camelcase_to_underscore(name):
    return _RE_SPAN_OF_CAPS.sub(r'\1_\2',
        _RE_FIND_FIRST_CAP.sub(r'\1_\2', name)
    ).lower()

def bytes_to_kbytes(value):
    return (float(value) / 1024.0)

def bytes_to_mbytes(value):
    return (float(value) / 1024.0 / 1024.0)

def bytes_to_gbytes(value):
    return (float(value) / 1024.0 / 1024.0 / 1024.0)
