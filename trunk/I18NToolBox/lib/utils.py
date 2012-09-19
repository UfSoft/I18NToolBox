# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: utils.py 25 2007-01-06 19:05:17Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/trunk/I18NToolBox/lib/utils.py $
# $LastChangedDate: 2007-01-06 19:05:17 +0000 (Sat, 06 Jan 2007) $
# $Rev: 25 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import re
import codecs


def escape_unicode(s):
    ur"""Escapes control characters and Python literals only leaving non-ascii
    text intact.

    >>> tests = [
    ... u'Isto é uma String unicode.',
    ... u'This is an unicode String',
    ... u'Só para ver que são os caracteres acentuados que são "escapados"'
    ... ]
    >>> for test in tests:
    ...     escape_unicode(test)
    ...
    u'Isto \xe9 uma String unicode.'
    u'This is an unicode String'
    u'S\xf3 para ver que s\xe3o os caracteres acentuados que s\xe3o \\"escapados\\"'
    """
    #for sp in ('\t', '\r', '\n', '\"', '\\'):
    s = s.replace('\\', '\\\\')
    s = s.replace('\t', '\\t')
    s = s.replace('\r', '\\r')
    s = s.replace('\n', '\\n')
    s = s.replace('\"', '\\"')
    # escape control chars
    def repl(m): return "\\%03o" % ord(m.group(0))
    s = re.sub('[\001-\037]', repl, s)
    return s


def normalize(s, encoding='utf-8', escape=False):
    ur"""This converts the various Python string types into a format that is
    appropriate for .po files, namely much closer to C style.

    >>> tests = [
    ... u'Isto é uma String unicode.',
    ... u'This is an unicode String',
    ... u'Só para ver que são os caracteres acentuados que são "escapados"'
    ... ]
    >>> for test in tests:
    ...     normalize(test)
    ...
    u'"Isto \xe9 uma String unicode."'
    u'"This is an unicode String"'
    u'"S\xf3 para ver que s\xe3o os caracteres acentuados que s\xe3o \\"escapados\\""'
    """
    lines = s.split('\n')
    if len(lines) == 1:
        s = u'"' + escape_unicode(s) + '"'
    else:
        if not lines[-1]:
            del lines[-1]
            lines[-1] = lines[-1] + u'\n'
        for i in range(len(lines)):
            lines[i] = escape_unicode(lines[i])
        lineterm = u'\\n"\n"'
        s = u'""\n"' + lineterm.join(lines) + u'"'
    return s


def check_python_format(key):
    """Helper to see if the string contains any python formatting.

    >>> tests = [
    ... u"This does not have any python formating",
    ... u"%(This)s however does.",
    ... u"%d also has",
    ... u"%s also has",
    ... u"%s and %s and %s and %s and %s and %s and, also have",
    ... u"%(hex)E also has"
    ... ]
    >>> for test in tests:
    ...     check_python_format(test)
    ...
    False
    True
    True
    True
    True
    True
    """
    # Lets try for one string
    try:
        m = key % 'a'
        return True
    except TypeError: pass
    # Lets try for a single float
    try:
        m = key % 1.0
        return True
    except TypeError: pass
    # The above failed, let's see if there we're several python formats inside
    for n in range(1, 51): # 50 should be more than enough
        # Lets try strings
        try:
            test = tuple(['a']*n)
            m = key % test
            return True
        except TypeError: pass
        # Lets try floats
        try:
            test = tuple([1.0]*n)
            m = key % test
        except TypeError: pass
    # Regex match for %(dict_replacements)s
    if re.findall(r'(\%\(([\w]+)\)[d|i|o|u|x|X|e|E|f|F|g|G|c|r|s])', key):
        return True
    return False


def detect_unicode_encoding(bytes):
    """Try to detect the encoding of a file defaulting to UTF-8."""
    encodings_map = [
        (3, codecs.BOM_UTF8, 'UTF-8'),
        (4, codecs.BOM_UTF32_LE, 'UTF-32LE'),
        (4, codecs.BOM_UTF32_BE, 'UTF-32BE'),
        (2, codecs.BOM_UTF16_LE, 'UTF-16LE'),
        (2, codecs.BOM_UTF16_BE, 'UTF-16BE'),
    ]
    for (offset, bom, name) in encodings_map:
        if bytes[:offset] == bom:
            return name, offset
    return 'UTF-8', 0

