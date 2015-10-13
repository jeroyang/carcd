#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from carcd import constants
import pinyin
import string
import re
from collections import OrderedDict
import sys

def beautify(context):
    """
    Keep better looking in ascii-chinese combined context
    add space between ascii_letters and Chinese
    avoid multiple spaces, 
    avoid space between chinese and symbols,

    """
    if sys.hexversion >= 0x03000000:
        chinese = r'(?a)[^{}]'.format(re.escape(string.printable))
    else: 
        chinese = r'[^{}]'.format(re.escape(string.printable))
    symbols = r'[{}]'.format(re.escape(string.punctuation))
    ascii = r'\w'
    context = re.sub(r'({0})({1})'.format(chinese, ascii), r'\1 \2', context)
    context = re.sub(r'({1})({0})'.format(chinese, ascii), r'\1 \2', context)
    context = re.sub(r'({0}) ({1})'.format(chinese, symbols), r'\1\2', context)
    context = re.sub(r'({1}) ({0})'.format(chinese, symbols), r'\1\2', context)
    remove_multispace = re.sub(r'\s+', ' ', context)
    return remove_multispace

def asciilize(context):
    """
    Transform Chinese characters to pinyin, 
    multibyte symbol to unibyte symbol
    """
    output = []
    for ch in context:
        if ch in string.printable:
            output.append(ch)
        elif ch in constants.FULL2HALF:
            output.append(constants.FULL2HALF.get(ch, ''))
        else:
            output.append(' ')
            output.extend(pinyin.get(ch).capitalize())
    return ''.join(output).replace('  ', ' ')

def name_split(name):
    """
    Split a cd filename to multiple parts
    return as a OrderedDict:
    {
        <category>: <string>, 
    }
    the categories are following:
    `number` for leading numbers
    `title` for title name
    `ext` for file extension
    'space' for space ' '
    """
    categories = ['number', 'space', 'title', 'ext']
    pattern = (r'(?P<number>\d+(-?\d+))'
                '(?P<space> )?'
                '(?P<title>.*?)'
                '(?P<ext>\....)')

    itemdict = re.match(pattern, name).groupdict()
    itemlist = [(category, itemdict[category]) for category in categories]
    return OrderedDict(itemlist)

def name_join(items):
    """
    Join nameitems, eleminate None in the OrderedDict
    """
    return ''.join([item for item in items.values() if item is not None])

def number_format(number_string, fill=2):
    """
    add padding zeros to make alinged numbers
    ex. 

    >>> number_format('2')
    '02'

    >>> number_format('1-2')
    '01-02'
    """
    output = []
    digits_spliter = r'(?P<digit>\d+)|(?P<nondigit>.)'
    for token in [m.groups() for m in re.finditer(digits_spliter, number_string)]:
        if token[0] is None:
            output.append(token[1])
        else:
            output.append(token[0].zfill(2))
    return ''.join(output)

def name_handle(name):
    """
    Complicated processes to manipulate a given filename
    """
    items = name_split(name)
    output = []
    for item in items.items():
        if (item[0] == 'number') & (item[1] is not None):
            output.append(('number', number_format(item[1])))
        if (item[0] == 'space') & (item[1] is not None):
            output.append(('space', ' '))
        if (item[0] == 'title') & len(set(item[1]) - set(string.printable)) > 0:
            output.append(('title', asciilize(item[1]) + item[1]))
        if (item[0] == 'ext') & (item[1] is not None):
            output.append(('ext', item[1]))
    items = OrderedDict(output)
    return beautify(name_join(items))



