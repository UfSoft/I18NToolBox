# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: genshigte.py 76 2007-04-16 18:56:35Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/branches/fresh-start/i18ntoolbox/templating/genshigte.py $
# $LastChangedDate: 2007-04-16 19:56:35 +0100 (Mon, 16 Apr 2007) $
# $Rev: 76 $
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

from i18ntoolbox.templating import TEGettextExtractInterface
from i18ntoolbox.utils import get_bool_opt, get_list_opt

class GenshiGettextExtract(TEGettextExtractInterface):
    """Genshi Templating Engine Gettext Extract class that provides the
    extraction code."""

    name = 'Genshi'
    exts = ('.html',)

    ignore_tags = ['script', 'style']
    include_attribs =  ['title', 'alt', 'longdesc']
    gettext_funcs = {}

    LOAD_NAME = chr(opmap['LOAD_NAME'])
    LOAD_CONST = chr(opmap['LOAD_CONST'])
    CALL_FUNCTION = chr(opmap['CALL_FUNCTION'])
    BINARY_ADD = chr(opmap['BINARY_ADD'])

    def setup(self, options):
        self.debug = get_bool_opt(options.parsed_opts, 'debug', False)
        self.templates_path = options.computed.templates_path
        self.files = get_list_opt(
            options.computed, 'template_files', []
        )
        self.gettext_funcs = options.computed.gettext_funcs


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
                                  self.extract_strings(opcodes, code)))
        return loaded_consts


    def extract_from_template(self, template, search_text=True):
        """helper to extract linenumber and key pairs from a given template"""
        return self.extract_from_stream(template.stream, search_text)


    def extract_from_stream(self, stream, search_text=True):
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
                    if tag.localname in self.ignore_tags:
                        skip_level += 1
                if kind is genshi.core.END:
                    tag = data
                    if tag.localname in self.ignore_tags:
                        skip_level -= 1
                continue
            if kind is genshi.core.START:
                tag, attrs = data
                tagname = tag.localname
                if tagname in self.ignore_tags:
                    # skip the substream
                    skip_level += 1
                    continue
                for name, value in attrs:
                    if isinstance(value, basestring):
                        if search_text and name in self.include_attribs:
                            yield linenum, value
                    else:
                        for dummy, key in self.extract_from_stream(
                                            value, name in self.include_attribs):
                            yield linenum, key
            elif kind is genshi.template.EXPR:
                if data.source != "?":
                    keys = self.find_gettext(data.code)
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
            except genshi.input.ParseError, error:
                if self.debug:
                    print 'Skipping extracting l10n keys from %s: %s' % \
                            (fname, error)
                continue
            for linenum, key in self.extract_from_template(
                template, search_text=False):
                yield fname, linenum, key


