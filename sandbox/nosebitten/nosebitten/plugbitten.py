# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: plugbitten.py 75 2007-02-05 23:03:20Z s0undt3ch $
# =============================================================================
#             $URL: http://i18ntoolbox.ufsoft.org/svn/sandbox/nosebitten/nosebitten/plugbitten.py $
# $LastChangedDate: 2007-02-05 23:03:20 +0000 (Mon, 05 Feb 2007) $
#             $Rev: 75 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import os
import re
import logging
from bitten.util import xmlio
from bitten.build.pythontools import unittest as bitten_unittest, exec_ as pyexec

log = logging.getLogger('bitten.build.nose')

def coverage(ctxt, file_=None):
    assert file_, 'Missing required attribute "file"'
    try:
        fileobj = file(ctxt.resolve(file_), 'r')
        try:
            results = xmlio.Fragment()
            for child in xmlio.parse(fileobj).children():
                cover = xmlio.Element('coverage')
                for name, value in child.attr.items():
                    if name == 'file':
                        value = os.path.realpath(value)
                        if value.startswith(ctxt.basedir):
                            value = value[len(ctxt.basedir) + 1:]
                            value = value.replace(os.sep, '/')
                        else:
                            continue
                    cover.attr[name] = value
                    for grandchild in child.children():
                        cover.append(xmlio.Element(grandchild.name)[
                            grandchild.gettext()
                        ])
                results.append(cover)
            ctxt.report('nosecoverage', results)
        finally:
            fileobj.close()
    except IOError, e:
        log.warning('Error opening coverage results file (%s)', e)
    except xmlio.ParseError, e:
        log.warning('Error parsing coverage results file (%s)', e)


def nblint(ctxt, module=None, args=''):

    #assert file_, 'Missing required attribute "file"'
    assert module, 'Missing required attribute "module"'

    try:
        from logilab.pylint import lint
        lint_module = 'logilab.pylint.lint'
    except ImportError:
        try:
            from pylint import lint
            lint_module = 'pylint.lint'
        except ImportError:
            raise AssertionError, "Unnable to import pylint"

    try:
        mod = __import__(lint_module, globals(), locals(), [])
        components = lint_module.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        file_ = mod.__file__.replace('\\', '/')
    except ImportError, e:
        ctxt.error('Cannot execute Python module %s: %s' % (lint_module, e))

    outfile = 'pylint_%s.txt' % module
    args = args.split()
    if '--output-format=parseable' not in args:
        args.append('--output-format=parseable')
    if '--include-ids=y' not in args:
        args.append('--include-ids=y')
    if '--reports=n' not in args:
        args.append('--reports=n')
    args.append('--persistent=n')

    args = ' '.join(args) + ' %s' % module

    #log.debug('PASSING ARGS: %s', args)

    pyexec(ctxt, module=lint_module, args=args, output=outfile)

    msg_re = re.compile(r'(?P<file>.+):(?P<line>\d+): '
                        r'\[(?P<type>[A-Z]\d*)(?:, (?P<tag>[\w\.]+))?\] '
                        r'(?P<msg>.*)')
    msg_categories = dict(W='warning', E='error', C='convention', R='refactor', F='failure')

    problems = xmlio.Fragment()
    try:
        fd = open(ctxt.resolve(outfile), 'r')
        #log.debug('OUTFILE: %s', outfile)
        #log.debug('OUTFILE Resolved:%s', ctxt.resolve(outfile))
        try:
            for line in fd:
                #log.debug('LINT_LINE: %s', line)
                match = msg_re.search(line)
                if match:
                    msg_type = match.group('type')
                    category = msg_categories.get(msg_type[0])
                    if len(msg_type) == 1:
                        msg_type = None
                    #filename = os.path.abspath(match.group('file'))
                    #log.debug('File: %r', match.group('file'))
                    #log.debug('File Path: %r', filename)
                    filename = match.group('file')
                    #if filename.startswith(ctxt.basedir):
                    #    filename = filename[len(ctxt.basedir) + 1:]
                    #filename = filename.replace(os.sep, '/')
                    lineno = int(match.group('line').strip())
                    tag = match.group('tag')
                    msg = match.group('msg') or ''
                    #log.debug('Type: %s, Category: %s, Filename: %s, Line: %s, Tag: %s, Msg: %s',
                    #         msg_type, category, filename, lineno, tag, msg)
                    problems.append(xmlio.Element('problem', category=category,
                                                  type=msg_type, tag=tag,
                                                  line=lineno, file=filename,
                                                  msg=msg)
                    )
            #log.debug('PROBS', problems)
            ctxt.report('lint', problems)
        finally:
            fd.close()
    except IOError, e:
        log.warning('Error opening pylint results file (%s)', e)

unittest = bitten_unittest
