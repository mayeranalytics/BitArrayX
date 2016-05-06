# BitArrayX 

### Overview ###

BitArrayX is a pure python module for easy manipulation of 
binary arrays of arbitrary length with *extended logic*.
For most purpuses, in particular when you don't need extended logic,
the [bitstring](http://pythonhosted.org/bitstring/) module 
should be your first choice. It is extensive and well tested.


### Extended logic ###

The extended logic used here extends the Boolean logic
with a third truth value denoted by `x`. 
Depending on the interpretation this truth value
stands for 

- indeterminate value "don't know"
- contaminated value (for example in logic circuit design when a line is driven both by a high and a low signal)
- "don't care"

See the wikipedia article on [three-valued logic](https://en.wikipedia.org/wiki/Three-valued_logic#Kleene_and_Priest_logics) for more information. 

The truth tables for `AND` and `OR` are as follows.

| `AND`   | 0 | 1 | x |
|-------|---|---|---|
| **0** | 0 | 0 | 0 |
| **1** | 0 | 1 | x |
| **x** | 0 | x | x |

| `OR`    | 0 | 1 | x |
|-------|---|---|---|
| **0** | 0 | 1 | x |
| **1** | 1 | 1 | 1 |
| **x** | x | 1 | x |

The name `BitArrayX` was chosen for two reasons.
Firstly, the terms tri-state 
(using the high-impedance state `z`) and ternary logic (using an indeterminate
`x` state) can be confusing. 
Secondly, the module may be extended
to include the `z` truth value which represents a high impedance value
in digital logic design. 

# Motivation
todo

# Documentation
The module has two classes, `BitStringX` and `BitStringXException`.

```python
>>> from BitArrayX import *
```


### Constructors ###

Objects can be instiated in many ways, and each creates a
bitarray of a  particular length.

If instantiated from a 
integer number the bitarray has the shortest necessary length:

```python
>>> b = BitArrayX(10)
>>> b
BitArrayX(1010)
```

When created from a legal binary string such as `0b0011` the 
bitstring has the given length

```python
>>> b = BitArrayX('0b0010')
>>> b
BitArrayX(0010)
```

To get a bitstring with extended logic the binary form has to be used:

```python
>>> b = BitArrayX('0bx01')
>>> b
BitArrayX(x01)
```

A hexadecimal string creates a bitstring of the exact length
given, i.e. the length is a  multiple of 4.

```python
>>> b = BitArrayX('0x0f')
>>> b
BitArrayX(00001111)
```

The length can also be given explicitly in the second argument
to the constructor:

```python
>>> b = BitArrayX('0x0f', 32)
>>> b
BitArrayX(00000000000000000000000000001111)
```
```python
>>> b = BitArrayX(1, 8)
>>> b
BitArrayX(00000001)
```

Octals are also allowed:

```python
>>> b = BitArrayX('0o077')
>>> b
BitArrayX(000111111)
>>> len(b)
9
```

### Logic ###

Negation, shifting, and, or, xor, etc. work as expected:

```python
>>> ~BitArrayX('0bx01')
BitArrayX(x10)
```
Shifts are logical (as opposed to arithmetic) and the length of the 
bitstring is preserved. I.e. the bitstring is padded with zeroes from 
left (`>>`) or right (`<<`)

```python
>>> BitArrayX('0b1001') << 1
BitArrayX(0010)
>>> BitArrayX('0b1001') >> 1
BitArrayX(0100)
```
```python
>>> a = BitArrayX('0b01x')
>>> b = BitArrayX('0b011')
>>> a & b
BitArrayX(01x)
>>> a | b
BitArrayX(011)
>>> a+b
BitArrayX(01x011)
>>> a ^ b
BitArrayX(00x)
```

### Subsetting ###
Note that the notation has the MSB is to the left and the LSB is to the right. I.e. `0b0001` = 1.

```python
>>> b = BitArrayX('0bx01')
>>> b[0]
BitArrayX(1)
>>> b[1]
BitArrayX(0)
>>> b[2]
BitArrayX(x)
```

Slices are possible, too. Just note that the bit with index 0 (the LSB) is to the right.

```python
>>> b = BitArrayX('0bxxx01')
>>> b[0:3]
BitArrayX(x01)
```

Item assgiments work as expected:

```python
>>> b = BitArrayX('0bxxx01')
>>> b[0:2] = BitArrayX('0bxx')
>>> b
BitArrayX(xxxxx)

```

# Dependencies
None.

# References
[TriBool](https://pypi.python.org/pypi/tribool/)

# Copyright and License

&copy; 2016 Mayer Analytics Ltd., All Rights Reserved.

### Short version
The license is [GNU GPL](http://www.gnu.org/licenses/gpl-3.0.en.html). 
You may copy, distribute and modify the software as long as you track changes/dates in source files. 
Any modifications to or software including (via compiler) GPL-licensed code must also be made available under 
the GPL along with build & install instructions.
([Software Licenses in Plain English](https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3))

### Long version
BitArrayX is free software: you can redistribute it and/or modify it under the terms of the 
GNU General Public License as published by the Free Software Foundation, 
either version 3 of the License, or (at your option) any later version.

BitArrayX is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details.

You can be released from the requirements of the license by obtaining a commercial license. 

You should have received a copy of the GNU General Public License
along with BitArrayX. If not, see [https://github.com/mayeranalytics/BitArrayX](https://github.com/mayeranalytics/BitArrayX).