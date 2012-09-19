# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: genshi_gettext.py 27 2007-01-11 00:20:45Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/trunk/I18NToolBox/lib/genshi_gettext.py $
# $LastChangedDate: 2007-01-11 00:20:45 +0000 (Thu, 11 Jan 2007) $
# $Rev: 27 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import re
import genshi.template
import genshi.input
import genshi.core
from opcode import opmap
from I18NToolBox.lib.utils import check_python_format, normalize

LOAD_NAME = chr(opmap['LOAD_NAME'])
LOAD_CONST = chr(opmap['LOAD_CONST'])
CALL_FUNCTION = chr(opmap['CALL_FUNCTION'])
BINARY_ADD = chr(opmap['BINARY_ADD'])

ignore_tags = ['script', 'style']
include_attribs = ['title', 'alt', 'longdesc']

GETTEXT_FUNCS = {}

def build_gettext_functions(func_list):
    """Build the gettext function to parse.
    Credits to Matt Good."""
    for func in func_list:
        if func.find(':') != -1:
            func_name, func_args = func.split(':')
        else:
            func_name, func_args = func, None
        if not GETTEXT_FUNCS.has_key(func_name):
            if func_args:
                str_indexes = [(int(x) -1 ) for x in func_args.split(',')]
            else:
                str_indexes = None
            GETTEXT_FUNCS[func_name] = str_indexes


def to_code(num):
    return chr(num) + '\x00'


def extract_strings(opcodes, code):
    """Extract the strings from the code.
    Credits to Matt Good"""
    strings = []
    opcodes = iter(opcodes)
    for op in opcodes:
        if op == BINARY_ADD:
            arg = strings.pop()
            strings[-1] += arg
        else:
            arg = code.co_consts[ord(opcodes.next())]
            opcodes.next() # skip second byte
            if not isinstance(arg, basestring):
                break
            strings.append(arg)
    return strings


def find_gettext(code):
    """Find the gettext calls.
    Credits to Matt Good"""
    names = dict([(n,to_code(i)) for i,n in enumerate(code.co_names)])
    consts = dict([(n,to_code(i)) for i,n in enumerate(code.co_consts)])
    gettext_locs = [consts[n] for n in GETTEXT_FUNCS.keys() if n in consts]
    ops = [LOAD_CONST, '(', '|'.join(gettext_locs), ')',
           CALL_FUNCTION, '.\x00',
           '((?:', BINARY_ADD, '|', LOAD_CONST, '.\x00)+)']
    load_consts = re.findall(''.join(ops), code.co_code)
    loaded_consts = []
    for func_loc, opcodes in load_consts:
        loaded_consts.append((code.co_consts[ord(func_loc[0])],
                              extract_strings(opcodes, code)))
    return loaded_consts


def extract_from_template(template, search_text=True):
    """helper to extract linenumber and key pairs from a given template"""
    return extract_from_stream(template.stream)


def extract_from_stream(stream, search_text=True):
    """takes a MatchTemplate.stream (not a normal XML Stream) and searches for
    localizable text, yielding linenumber, text tuples"""

    stream = iter(stream)
    tagname = None
    skip_level = 0

    for kind, data, pos in stream:
        linenum = pos[1]
        if skip_level:
            if kind is genshi.core.START:
                tag, attrs = data
                if tag.localname in ignore_tags:
                    skip_level += 1
            if kind is genshi.core.END:
                tag = data
                if tag.localname in ignore_tags:
                    skip_level -= 1
            continue
        if kind is genshi.core.START:
            tag, attrs = data
            tagname = tag.localname
            if tagname in ignore_tags:
                # skip the substream
                skip_level += 1
                continue
            for name, value in attrs:
                if isinstance(value, basestring):
                   if search_text and name in include_attribs:
                       yield linenum, value
                else:
                    for dummy, key in extract_from_stream(
                                            value, name in include_attribs):
                        yield linenum, key
        elif kind is genshi.template.EXPR:
            if data.source != "?":
                keys = find_gettext(data.code)
                if keys:
                    for key in keys:
                        yield linenum, key
        elif kind is genshi.core.TEXT and search_text:
            key = data.strip()
            if key:
                yield linenum, key
        elif kind is genshi.template.SUB:
            sub_kind, sub_stream = data
            for linenum, key in extract_from_stream(sub_stream, search_text):
                yield linenum, key


def extract_keys(files, search_path=['.'], debug=False):
    """finds all the text keys in the given files"""
    loader = genshi.template.TemplateLoader(search_path)
    for fname in files:
        try:
            template = loader.load(fname)
        except genshi.input.ParseError, e:
            if debug:
                print 'Skipping extracting l10n keys from %s: %s' % (fname, e)
            continue
        for linenum, key in extract_from_template(template, search_text=False):
            yield fname, linenum, key


def write_pot_file(pot_path, files, debug=False):
    fd = open(pot_path, 'at+')
    try:
        keys_found = {}
        key_order = []
        for fname, linenum, key in extract_keys(files, debug=debug):
            str_indexes = GETTEXT_FUNCS[key[0]]
            if not str_indexes:
                # We now know these are simple gettext fucntions,
                # So assing key to the string field
                key = key[1][0]
                if key in keys_found:
                    keys_found[key].append((fname, linenum))
                else:
                    keys_found[key] = [(fname, linenum)]
                    key_order.append(key)
            elif len(str_indexes) == 1:
                key = key[1][str_indexes[0]]
                if key in keys_found:
                    keys_found[key].append((fname, linenum))
                else:
                    keys_found[key] = [(fname, linenum)]
                    key_order.append(key)
            else:
                # We're in the presence of plurals
                singular = key[1][str_indexes[0]]
                plural = key[1][str_indexes[1]]
                fd.write('#: %s:%s\n' % (fname, linenum))
                if check_python_format(singular) or check_python_format(plural):
                    fd.write('#, ')
                    if debug:
                        fd.write('possible-')
                    fd.write('python-format\n')
                fd.write('msgid %s\n' % normalize(singular))
                fd.write('msgid_plural %s\n' % normalize(plural))
                fd.write('msgstr[0] ""\n')
                fd.write('msgstr[1] ""\n\n')
                continue
        for key in key_order:
            for fname, linenum in keys_found[key]:
                fd.write('#: %s:%s\n' % (fname, linenum))
            if check_python_format(key):
                fd.write('#, ')
                if debug:
                    fd.write('possible-')
                fd.write('python-format\n')
            fd.write('msgid %s\n' % normalize(key))
            fd.write('msgstr ""\n\n')
    finally:
        fd.close()


__all__ = ['write_pot_file']
