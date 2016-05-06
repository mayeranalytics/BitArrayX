#!/usr/bin/env python2
__author__ = 'mmayer'

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from BitArrayX import BitArrayX, BitArrayXException
import unittest2


def load_truth_table(filename):
    """ Loads a truthtable and returns input and target output strings
    """
    with open(filename, 'r') as f:
        d = dict()
        states = f.readline().strip().split(' ')[1:]
        for line in f:
            line = line.strip().split(' ')
            if line[0] in states:
                d[line[0]] = dict(zip(states, line[1:]))
        a, b, t = zip(*[(e1, e2, d[e1][e2]) for e1 in states for e2 in states])
        return ''.join(a), ''.join(b), ''.join(t)
    raise Exception("Could not read/parse file '{}'.".format(filename))

if __name__ == '__main__':

    class TestBitArrayX(unittest2.TestCase):

        def test_constructor_raises(self):
            with self.assertRaises(BitArrayXException):
                BitArrayX(object())
            with self.assertRaises(BitArrayXException):
                BitArrayX(-1)
            with self.assertRaises(BitArrayXException):
                BitArrayX('blah')
            with self.assertRaises(BitArrayXException):
                BitArrayX(15, 3)
            with self.assertRaises(BitArrayXException):
                BitArrayX('0b0x0', 2)
            with self.assertRaises(BitArrayXException):
                BitArrayX('0b0q0', 2)

        def test_constructor_correctness(self):
            x = BitArrayX(15)
            self.assertEqual(x, 15)
            self.assertEqual(len(x), 4)
            x = BitArrayX('0b000')
            self.assertEqual(int(x), 0)
            self.assertEqual(len(x), 3)
            x = BitArrayX('0b?00')
            with self.assertRaises(BitArrayXException):
                int(x)
            self.assertEqual(len(x), 3)
            x = BitArrayX('0b0x00')
            with self.assertRaises(BitArrayXException):
                int(x)
            self.assertEqual(len(x), 4)
            x = BitArrayX('0x00')
            self.assertEqual(len(x), 8)
            self.assertEqual(int(x), 0)
            x = BitArrayX('0o000')
            self.assertEqual(len(x), 9)
            self.assertEqual(int(x), 0)

        def test_concat(self):
            b = BitArrayX('0b111') + BitArrayX('0b000')
            self.assertEqual(int(b), 0b111000)
            self.assertEqual(int(b), BitArrayX('0b111000'))

        def test_logic(self):
            # and
            a, b, t = [BitArrayX('0b'+s) for s in load_truth_table("truthtables/and.txt")]
            self.assertEqual(a & b, t)
            # or
            a, b, t = [BitArrayX('0b'+s) for s in load_truth_table("truthtables/or.txt")]
            self.assertEqual(a | b, t)
            # xor
            a, b, t = [BitArrayX('0b'+s) for s in load_truth_table("truthtables/xor.txt")]
            self.assertEqual(a ^ b, t)
            # not
            self.assertEqual(~BitArrayX('0bx1010'), BitArrayX('0bx0101'))

        def test_DeMorgan(self):
            states = ['0', '1', 'x']
            a, b = map(lambda x: BitArrayX('0b'+''.join(x)), zip(*[(e1, e2) for e1 in states for e2 in states]))
            self.assertEqual(~(a & b), ~a | ~b)
            self.assertEqual(~(a | b), ~a & ~b)

        def test_xor(self):
            states = ['0', '1', 'x']
            a, b = map(lambda x: BitArrayX('0b'+''.join(x)), zip(*[(e1, e2) for e1 in states for e2 in states]))
            self.assertEqual(a ^ b, (a|b) & ~(a&b))

        def test_shift(self):
            x = BitArrayX('0b1010')
            self.assertEqual(x >> 1, BitArrayX('0b0101'))
            self.assertEqual(x >> 4, BitArrayX('0b0000'))
            self.assertEqual(x << 1, BitArrayX('0b0100'))
            self.assertEqual(x << 4, BitArrayX('0b0000'))

        def test_getitem(self):
            x = BitArrayX('0b1010')
            self.assertEqual(x[0], 0)
            self.assertEqual(x[1], 1)
            self.assertEqual(x[3], 1)
            self.assertEqual(x[0:2], BitArrayX('0b10'))
            self.assertEqual(x[0:3], BitArrayX('0b010'))
            with self.assertRaises(IndexError):
                x[5]

        def test_setitem(self):
            x = BitArrayX('0b1010')
            x[0:1] = BitArrayX('0bxx')
            self.assertEqual(x, BitArrayX('0b101xx'))
            x[0:2] = BitArrayX('0b00')
            self.assertEqual(x, BitArrayX('0b10100'))

        def test_conversions(self):
            x = BitArrayX('0b1010')
            self.assertEqual(oct(x), '012')
            self.assertEqual(hex(x), '0xa')


    unittest2.main()
