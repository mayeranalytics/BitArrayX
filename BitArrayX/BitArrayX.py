#!/usr/bin/env python2
__author__ = 'mmayer'

import re


class BitArrayXException(Exception):
    pass


class BitArrayX(object):
    """ Simple operations on bit arrays
    """

    _re_string = re.compile(r"^\s*(0b[01x\?_]+|0o[0-7_]+|0x[0-9aAbBcCdDeEfF_]+)\s*$")

    _and = {'0': {'0':'0', '1':'0', 'x':'0'}, '1': {'0':'0', '1':'1', 'x':'x'}, 'x': {'0':'0', '1':'x', 'x':'x'}}
    _or  = {'0': {'0':'0', '1':'1', 'x':'x'}, '1': {'0':'1', '1':'1', 'x':'1'}, 'x': {'0':'x', '1':'1', 'x':'x'}}
    _xor = {'0': {'0':'0', '1':'1', 'x':'x'}, '1': {'0':'1', '1':'0', 'x':'x'}, 'x': {'0':'x', '1':'x', 'x':'x'}}
    _not = {'0': '1', '1':'0', 'x':'x'}

    @staticmethod
    def undef():
        return BitArrayX('0bx')

    @staticmethod
    def true():
        return BitArrayX('0b1')

    @staticmethod
    def false():
        return BitArrayX('0b')

    def __init__(self, x, array_len=None):
        """ Construct BitArrayX
        :param x:
        :param array_len:
        :return:
        """
        self._array = ''        # bit arrays are stored as strings of '0', '1', 'x'

        # validate the properness of the input and convert to a positive int if necessary
        if isinstance(x, int):
            if x < 0:
                raise BitArrayXException("BitArrayX: Cannot instantiate from '{}': Negative number.".format(str(x)))
            number_string = bin(x)[2:]
        elif isinstance(x, str):
            match = BitArrayX._re_string.match(x)
            if match is None:
                raise BitArrayXException("BitArrayX: Cannot instantiate from {}. Cannot parse.".format(x))
            s = match.group(1).replace("_", "").replace('?', 'x')
            number_type = s[1]  # one of b, o, x
            number_string = s[2:]
            if number_type == 'x' or number_type == 'o':
                if array_len is None:
                    if number_type == 'o':
                        array_len = 3 * len(number_string)
                    elif number_type == 'x':
                        array_len = 4 * len(number_string)
                number_string = bin(eval(x))[2:]
        else:
            raise BitArrayXException("BitArrayX: Cannot instantiate from {}".format(str(x)))

        # now we are at the point where number_string is a valid bit string
        if array_len is None:
            array_len = len(number_string)
        elif array_len < len(number_string):
            raise BitArrayXException("BitArrayX: Cannot instantiate from '{0}': len('{0}')={2} > {1}."
                                    .format(str(x), array_len, len(number_string)))
        if array_len is None:
            array_len = len(number_string)
        self._array = '0'*(array_len-len(number_string)) + number_string

    def __len__(self):
        return len(self._array)

    def __int__(self):
        'x.__int__() <==> int(x)'
        try:
            return eval('0b'+self._array)
        except SyntaxError as e:
            # by construction this can only happen if _array has a 'x'. In this case the value is undef,
            # but we must raise an exception because __int__ must return an integer.
            raise BitArrayXException("{} is not an integer".format(self._array))

    def __str__(self):
        return '0b'+self._array

    def __repr__(self):
        return 'BitArrayX(' + self._array + ')'

    def __add__(self, other):
        return BitArrayX('0b' + self._array + other._array)

    def __mul__(self, n):
        return BitArrayX('0b' + self._array * n)

    def __eq__(self, other):
        if isinstance(other, BitArrayX):
            return self._array == other._array
        else:
            return int(self) == other

    def __setitem__(self, key, item):
        """ 'x[i, y] <==> x[i]=y' (but not x[i:j:step]=y) """
        if item is not None and type(item).__name__ != 'BitArrayX':
            raise BitArrayXException("Can only assign BitArrayX, you tried to assign {}.".format(type(item).__name__))

        try:
            start = key.start
            stop = key.stop
        except AttributeError:
            # single item
            if not 0 <= key <= len(self):
                raise IndexError('list index out of range')
            else:
                l = [s for s in reversed(self._array)]
                rhs = [s for s in reversed(item._array)]
                l[key:(key+1)] = tuple(rhs)
                self._array = ''.join(reversed(l))
                return self
        else:
            # slice
            if start is None:
                start = 0
            if stop is None:
                stop = len(self)
            l = [s for s in reversed(self._array)]
            rhs = [s for s in reversed(item._array)]
            l[start:stop] = tuple(rhs)
            self._array = ''.join(reversed(l))
            return self

    def __getitem__(self, key):
        """ <==> x[i] or x[i:j] (but not x[i:j:step]) """
        try:
            start = key.start
            stop = key.stop
        except AttributeError:
            # single item
            if not 0 <= key <= len(self):
                raise IndexError('list index out of range')
            else:
                return BitArrayX('0b' + self._array[len(self)-key-1])
        else:
            # slice
            if start is None:
                start = 0
            if stop is None:
                stop = len(self)
            return BitArrayX('0b' + self._array[::-1][start:stop][::-1])


    def toList(self):
        """ Convert bitarray to a list of 0, 1, None.

            Note: This may have to be revisited when 'z' is introduced! """
        return map(lambda x: 0 if x == '0' else 1 if x == '1' else None, self._array)

    def __xor__(self, other):
        'x.__xor__(y) <==> x|y'
        return BitArrayX('0b' + ''.join(map(lambda x: BitArrayX._xor[x[0]][x[1]], zip(self._array, other._array))))

    def __and__(self, other):
        'x.__and__(y) <==> x&y'
        return BitArrayX('0b' + ''.join(map(lambda x: BitArrayX._and[x[0]][x[1]], zip(self._array, other._array))))

    def __or__(self, other):
        'x.__or__(y) <==> x&y'
        return BitArrayX('0b' + ''.join(map(lambda x: BitArrayX._or[x[0]][x[1]], zip(self._array, other._array))))

    def __invert__(self):
        'x.__invert__() <==> ~x'
        return BitArrayX('0b' + ''.join(map(lambda x: BitArrayX._not[x], self._array)))

    def __lshift__(self, n):
        'x.__lshift__(n) <==> x<<n'
        if n > len(self):
            return BitArrayX(0, len(self))
        else:
            return BitArrayX('0b'+self._array[n:len(self)]+'0'*n)

    def __rshift__(self, n):
        'x.__rshift__(n) <==> x>>n'
        if n > len(self):
            return BitArrayX(0, len(self))
        else:
            return BitArrayX('0b' + '0'*n + self._array[0:(len(self)-n)])

    def __oct__(self):
        'x.__oct__() <==> oct(x)'
        return oct(int(self))

    def __hex__(self):
        'x.__hex__() <==> hex(x)'
        return hex(int(self))

    def __hash__(self):
        'x.__hash__() <==> hash(x)'
        return hash(self._array)

