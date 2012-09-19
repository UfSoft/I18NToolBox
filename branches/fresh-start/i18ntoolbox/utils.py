# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: utils.py 76 2007-04-16 18:56:35Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/branches/fresh-start/i18ntoolbox/utils.py $
# $LastChangedDate: 2007-04-16 19:56:35 +0100 (Mon, 16 Apr 2007) $
# $Rev: 76 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import os
import re

class AttrsDict(dict):
    """A dictionary that can be accessed by attribute.
    Thanks coderanger and pacopablo on irc.freenode.net #trac for the helpful
    suggestion.

    >>> d = AttrsDict()
    >>> d.foo = AttrsDict()
    >>> d.bar = AttrsDict()
    >>> d.foo.bar = 'FOO'
    >>> d.bar.foo = 'BAR'
    >>> d
    {'foo': {'bar': 'FOO'}, 'bar': {'foo': 'BAR'}}
    >>> d.foo
    {'bar': 'FOO'}
    >>> d.foo.bar
    'FOO'
    >>> d.bar
    {'foo': 'BAR'}
    >>> d.bar.foo
    'BAR'
    >>> d.bar.fooo
    Traceback (most recent call last):
        ...
    AttributeError
    """
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError
    def __setattr__(self, name, value):
        self[name] = value


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


def normalize(s): #, encoding='utf-8', escape=False):
    ur"""This converts the various Python string types into a format that is
    appropriate for .po files, namely much closer to C style.

    >>> tests = [
    ... u'Isto é uma String unicode.',
    ... u'This is an unicode String',
    ... u'Só para ver que são os caracteres acentuados que são "escapados"',
    ... u'And this is a\nmultiple lines\nstring.',
    ... u'\n',
    ... u'',
    ... ]
    >>> for test in tests:
    ...     normalize(test)
    ...
    u'"Isto \xe9 uma String unicode."'
    u'"This is an unicode String"'
    u'"S\xf3 para ver que s\xe3o os caracteres acentuados que s\xe3o \\"escapados\\""'
    u'""\n"And this is a\\n"\n"multiple lines\\n"\n"string."'
    u'""\n"\\n"'
    u'""'
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


class OptionError(Exception):
    """From pygments.util code <http://pygments.pocoo.org/>"""
    pass


def get_bool_opt(options, optname, default=None):
    """From pygments.util code <http://pygments.pocoo.org/>"""
    string = options.get(optname, default)
    if isinstance(string, bool):
        return string
    elif string.lower() in ('1', 'yes', 'true', 'on', 'enabled'):
        return True
    elif string.lower() in ('0', 'no', 'false', 'off', 'disabled'):
        return False
    else:
        raise OptionError('Invalid value %r for option %s; use '
                          '1/0, yes/no, true/false, on/off, '
                          'enabled/disabled' % (
                          string, optname))


def get_int_opt(options, optname, default=None):
    """From pygments.util code <http://pygments.pocoo.org/>"""
    string = options.get(optname, default)
    try:
        return int(string)
    except ValueError:
        raise OptionError('Invalid value %r for option %s; you '
                          'must give an integer value' % (
                          string, optname))


def get_list_opt(options, optname, default=None):
    """From pygments.util code <http://pygments.pocoo.org/>"""
    val = options.get(optname, default)
    if isinstance(val, basestring):
        return val.split()
    elif isinstance(val, (list, tuple)):
        return list(val)
    else:
        raise OptionError('Invalid value %r for option %s; you '
                          'must give a list value' % (
                          val, optname))


def silent_backup(path):
    """Silently backup(if present) the passed path."""

    if os.path.exists(path):
        backup_path = path + '.bak'
        if os.path.exists(backup_path):
            try:
                os.unlink(backup_path)
            except OSError:
                pass
        try:
            os.rename(path, backup_path)
        except OSError, error:
            print error

    # Write an empty file so we don't get any errors when using
    # `--join-existing`
    file(path, 'wb').write('')


def print_developer_info(defaults):
    """If the 'I18NTB_DEFAULTS_DICT' environment variable is set to
    '1', 'yes', 'true', 'on' or 'enabled', the defaults dict created to pass
    information for templating engine plugins will be displayed to the user
    so a developer knows what info I18NToolBox gathers that can help them
    build their plugin.

    To get the info, while on a shell do:
        export I18NTB_DEFAULTS_DICT=true

    Then run the i18ntoolbox binary for a project.
    """
    if os.environ.has_key('I18NTB_DEFAULTS_DICT'):
        if get_bool_opt(os.environ, 'I18NTB_DEFAULTS_DICT', False):
            print "Info that I18NToolBox gathered:"
            for key, val in defaults.iteritems():
                print
                print 'KEY:', key
                print 'VALUE(S):\n', val
