# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: genshigte.py 43 2007-01-21 08:24:29Z pjenvey $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/branches/bitten/i18ntoolbox/templating/genshigte.py $
# $LastChangedDate: 2007-01-21 08:24:29 +0000 (Sun, 21 Jan 2007) $
# $Rev: 43 $
# $LastChangedBy: pjenvey $
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

from i18ntoolbox.templating import TEGettextExtractInterface
from i18ntoolbox.utils import get_bool_opt, get_list_opt

class GenshiGettextExtract(TEGettextExtractInterface):
    """Genshi Templating Engine Gettext Extract class that provides the
    extraction code."""

    name = 'Genshi'
    exts = ('.html',)

    ignore_tags = ['script', 'style']
    include_attribs =  ['title', 'alt', 'longdesc']

    LOAD_NAME = chr(opmap['LOAD_NAME'])
    LOAD_CONST = chr(opmap['LOAD_CONST'])
    CALL_FUNCTION = chr(opmap['CALL_FUNCTION'])
    BINARY_ADD = chr(opmap['BINARY_ADD'])

    def setup(self, **options):
        self.debug = get_bool_opt(options['parsed_opts'], 'debug', False)


    def build_gettext_functions(func_list):
        """Build the gettext function to parse.
        Credits to Matt Good."""
        for func in func_list:
            if func.find(':') != -1:
                func_name, func_args = func.split(':')
            else:
                func_name, func_args = func, None
            if not self.gettext_funcs.has_key(func_name):
                if func_args:
                    str_indexes = [(int(x) -1 ) for x in func_args.split(',')]
                else:
                    str_indexes = None
                self.gettext_funcs[func_name] = str_indexes


    def to_code(self, num):
        return chr(num) + '\x00'


    def extract_strings(self, opcodes, code):
        """Extract the strings from the code.
        Credits to Matt Good"""
        strings = []
        opcodes = iter(opcodes)
        for op in opcodes:
            if op == self.BINARY_ADD:
                arg = strings.pop()
                strings[-1] += arg
            else:
                arg = code.co_consts[ord(opcodes.next())]
                opcodes.next() # skip second byte
                if not isinstance(arg, basestring):
                    break
                strings.append(arg)
        return strings

    def find_gettext(self, code):
        """Find the gettext calls.
        Credits to Matt Good"""
        names = dict(
            [(n,self.to_code(i)) for i,n in enumerate(code.co_names)]
        )
        consts = dict(
            [(n,self.to_code(i)) for i,n in enumerate(code.co_consts)]
        )
        gettext_locs = [
            consts[n] for n in self.gettext_funcs.keys() if n in consts
        ]
        ops = [self.LOAD_CONST, '(', '|'.join(gettext_locs), ')',
               self.CALL_FUNCTION, '.\x00',
               '((?:', self.BINARY_ADD, '|', self.LOAD_CONST, '.\x00)+)']
        load_consts = re.findall(''.join(ops), code.co_code)
        loaded_consts = []
        for func_loc, opcodes in load_consts:
            loaded_consts.append((code.co_consts[ord(func_loc[0])],
                                  extract_strings(opcodes, code)))
        return loaded_consts


    def extract_from_template(self, template, search_text=True):
        """helper to extract linenumber and key pairs from a given template"""
        return extract_from_stream(template.stream)


    def extract_from_stream(stream, search_text=True):
        """takes a MatchTemplate.stream (not a normal XML Stream) and searches
        for localizable text, yielding linenumber, text tuples"""

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
                       if search_text and name in self.include_attribs:
                           yield linenum, value
                    else:
                        for dummy, key in self.extract_from_stream(
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
                for linenum, key in self.extract_from_stream(
                                            sub_stream, search_text):
                    yield linenum, key


    def extract_keys(self):
        loader = genshi.template.TemplateLoader(self.templates_path)
        for fname in self.files:
            try:
                template = loader.load(fname)
            except genshi.input.ParseError, e:
                if self.debug:
                    print 'Skipping extracting l10n keys from %s: %s' % (fname, e)
                continue
            for linenum, key in self.extract_from_template(
                template, search_text=False):
                yield fname, linenum, key


