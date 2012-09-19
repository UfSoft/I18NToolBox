# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: catalog.py 24 2007-01-06 16:47:00Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/trunk/I18NToolBox/lib/catalog.py $
# $LastChangedDate: 2007-01-06 16:47:00 +0000 (Sat, 06 Jan 2007) $
# $Rev: 24 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

"Pythonic Representation of a Gettext message catalog and it's parts."

__all__ = ['CatalogHeader', 'CatalogMessage', 'Catalog']

import sys
from I18NToolBox.lib.utils import check_python_format, detect_unicode_encoding
from I18NToolBox.lib.utils import normalize


class FlagError(ValueError):
    """Signals an error when setting a flag to an incorrect value."""


class ParseError(ValueError):
    """Signals an error reading .pot/.po file."""

def check_input(string):
    ur"""Helper function to "force" unicode user input. If the user still passes
    a non unicode object, we try to convert if it belongs to the `basestring`
    class. If unicode coversion fails we raise a error.
    >>> ci1 = check_input('This should covert fine.')
    >>> ci1
    u'This should covert fine.'
    >>> ci2 = check_input('Isto não deve passar.')
    Traceback (most recent call last):
        ...
    UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 6: ordinal not in range(128)
    >>> ci3 = check_input(u'Isto já não deve ter problemas.')
    >>> ci3
    u'Isto j\xe1 n\xe3o deve ter problemas.'
    """
    if isinstance(string, basestring) and not isinstance(string, unicode):
        try:
            string = unicode(string)
        except UnicodeDecodeError, error:
            raise UnicodeError, error
    return string


PROJECT_ID_VERSION = 0
REPORT_MSGID_BUGS_TO = 1
POT_CREATION_DATE = 2
PO_REVISION_DATE = 3
LAST_TRANSLATOR = 4
LANGUAGE_TEAM = 5
MIME_VERSION = 6
CONTENT_TYPE = 7
CONTENT_TRANSFER_ENCODING = 8
PLURAL_FORMS = 9


class CatalogHeader:
    """Representation of a gettext catalog header"""
    def __init__(self):
        self._comments = []
        self._headers = {
            PROJECT_ID_VERSION: (
                u'Project-Id-Version', u'PROJECT VERSION'
            ),
            REPORT_MSGID_BUGS_TO: (
                u'Report-Msgid-Bugs-To', u'ADDRESS@EMAIL'
            ),
            POT_CREATION_DATE: (
                u'POT-Creation-Date', u'YEAR-MO-DA HO:MI+ZONE'
            ),
            PO_REVISION_DATE: (
                u'PO-Revision-Date', u'YEAR-MO-DA HO:MI+ZONE'
            ),
            LAST_TRANSLATOR: (
                u'Last-Translator', u'FULL NAME <EMAIL@ADDRESS>'
            ),
            LANGUAGE_TEAM: (
                u'Language-Team', u'LANGUAGE <LL@li.org>'
            ),
            MIME_VERSION: (
                u'MIME-Version', u'1.0'
            ),
            CONTENT_TYPE: (
                u'Content-Type', u'text/plain; charset=UTF-8'
            ),
            CONTENT_TRANSFER_ENCODING: (
                u'Content-Transfer-Encoding', u'8bit'
            ),
            PLURAL_FORMS: (
                u'Plural-Forms', u'nplurals=INTEGER; plural=EXPRESSION;'
            )
        }
        self.fuzzy = False

    def __str__(self):
        return self.generate().encode('utf-8')

    def __unicode__(self):
        return self.generate()

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def generate(self):
        """Generates the catalog header output."""
        txt = u''.join([u'# %s\n' % x for x in self._comments]) + u'#\n'
        if self.fuzzy:
            txt += u'#, fuzzy\n'
        txt += u'msgid ""\nmsgstr ""\n'
        for key, val in self._headers.values():
            txt += u'"%s: %s\\n"\n' % (key, val)
        return txt

    def comments(self):
        """Get the comments the header has

        >>> ch = CatalogHeader()
        >>> ch.add_comment('Translation Template for Project XY')
        >>> ch.add_comment('Copyright FooBar 2010')
        >>> ch.comments()
        [u'Translation Template for Project XY', u'Copyright FooBar 2010']
        """
        return self._comments

    def headers(self):
        """Returns the headers.

        >>> ch = CatalogHeader()
        >>> for header in ch.headers():
        ...     print header
        ...
        (u'Project-Id-Version', u'PROJECT VERSION')
        (u'Report-Msgid-Bugs-To', u'ADDRESS@EMAIL')
        (u'POT-Creation-Date', u'YEAR-MO-DA HO:MI+ZONE')
        (u'PO-Revision-Date', u'YEAR-MO-DA HO:MI+ZONE')
        (u'Last-Translator', u'FULL NAME <EMAIL@ADDRESS>')
        (u'Language-Team', u'LANGUAGE <LL@li.org>')
        (u'MIME-Version', u'1.0')
        (u'Content-Type', u'text/plain; charset=UTF-8')
        (u'Content-Transfer-Encoding', u'8bit')
        (u'Plural-Forms', u'nplurals=INTEGER; plural=EXPRESSION;')
        """
        return self._headers.values()

    def add_comment(self, comment):
        r"""Add comments to the catalog header.

        >>> ch = CatalogHeader()
        >>> ch.add_comment('Translation Template for Project XY')
        >>> ch.add_comment('Copyright FooBar 2010')
        >>> print ch
        # Translation Template for Project XY
        # Copyright FooBar 2010
        #
        msgid ""
        msgstr ""
        "Project-Id-Version: PROJECT VERSION\n"
        "Report-Msgid-Bugs-To: ADDRESS@EMAIL\n"
        "POT-Creation-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
        "Language-Team: LANGUAGE <LL@li.org>\n"
        "MIME-Version: 1.0\n"
        "Content-Type: text/plain; charset=UTF-8\n"
        "Content-Transfer-Encoding: 8bit\n"
        "Plural-Forms: nplurals=INTEGER; plural=EXPRESSION;\n"
        <BLANKLINE>
        """
        comment = check_input(comment)
        if comment not in self._comments:
            self._comments.append(comment)

    def set_project_id_version(self, project, version):
        r"""Set the 'Project-Id-Version' header.

        >>> ch = CatalogHeader()
        >>> ch.set_project_id_version('Foo Project', 0.2)
        >>> print ch
        #
        msgid ""
        msgstr ""
        "Project-Id-Version: Foo Project 0.2\n"
        "Report-Msgid-Bugs-To: ADDRESS@EMAIL\n"
        "POT-Creation-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
        "Language-Team: LANGUAGE <LL@li.org>\n"
        "MIME-Version: 1.0\n"
        "Content-Type: text/plain; charset=UTF-8\n"
        "Content-Transfer-Encoding: 8bit\n"
        "Plural-Forms: nplurals=INTEGER; plural=EXPRESSION;\n"
        <BLANKLINE>
        """
        project = check_input(project)
        if isinstance(version, basestring):
            version = check_input(version)

        self._headers[PROJECT_ID_VERSION] = (
            self._headers[PROJECT_ID_VERSION][0], u'%s %s' % (project, version)
        )

    def get_project_id_version(self):
        """Get the 'Project-Id-Version' header."""
        raise NotImplementedError

    def set_report_msgid_bugs_to(self, value):
        r"""Set the Report-Msgid-Bugs-To header.

        >>> ch = CatalogHeader()
        >>> ch.set_report_msgid_bugs_to('nowhere@somehow.tld')
        >>> print ch
        #
        msgid ""
        msgstr ""
        "Project-Id-Version: PROJECT VERSION\n"
        "Report-Msgid-Bugs-To: nowhere@somehow.tld\n"
        "POT-Creation-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
        "Language-Team: LANGUAGE <LL@li.org>\n"
        "MIME-Version: 1.0\n"
        "Content-Type: text/plain; charset=UTF-8\n"
        "Content-Transfer-Encoding: 8bit\n"
        "Plural-Forms: nplurals=INTEGER; plural=EXPRESSION;\n"
        <BLANKLINE>
        """
        value = check_input(value)
        self._headers[REPORT_MSGID_BUGS_TO] = (
            self._headers[REPORT_MSGID_BUGS_TO][0], value
        )

    def get_report_msgid_bugs_to(self):
        """Get the Report-Msgid-Bugs-To header."""
        raise NotImplementedError

    def set_pot_creation_date(self, value):
        r"""Set the POT-Creation-Date header.
        >>> ch = CatalogHeader()
        >>> ch.set_pot_creation_date('2010-01-01 00:00+000')
        >>> print ch
        #
        msgid ""
        msgstr ""
        "Project-Id-Version: PROJECT VERSION\n"
        "Report-Msgid-Bugs-To: ADDRESS@EMAIL\n"
        "POT-Creation-Date: 2010-01-01 00:00+000\n"
        "PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
        "Language-Team: LANGUAGE <LL@li.org>\n"
        "MIME-Version: 1.0\n"
        "Content-Type: text/plain; charset=UTF-8\n"
        "Content-Transfer-Encoding: 8bit\n"
        "Plural-Forms: nplurals=INTEGER; plural=EXPRESSION;\n"
        <BLANKLINE>
        """
        value = check_input(value)
        self._headers[POT_CREATION_DATE] = (
            self._headers[POT_CREATION_DATE][0], value
        )

    def get_pot_creation_date(self):
        """Get the POT-Creation-Date header."""
        raise NotImplementedError

    def set_po_revision_date(self, value):
        r"""Set the PO-Revision-Date header.

        >>> ch = CatalogHeader()
        >>> ch.set_po_revision_date('2010-01-01 01:00+000')
        >>> print ch
        #
        msgid ""
        msgstr ""
        "Project-Id-Version: PROJECT VERSION\n"
        "Report-Msgid-Bugs-To: ADDRESS@EMAIL\n"
        "POT-Creation-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "PO-Revision-Date: 2010-01-01 01:00+000\n"
        "Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
        "Language-Team: LANGUAGE <LL@li.org>\n"
        "MIME-Version: 1.0\n"
        "Content-Type: text/plain; charset=UTF-8\n"
        "Content-Transfer-Encoding: 8bit\n"
        "Plural-Forms: nplurals=INTEGER; plural=EXPRESSION;\n"
        <BLANKLINE>
        """
        value = check_input(value)
        self._headers[PO_REVISION_DATE] = (
            self._headers[PO_REVISION_DATE][0], value
        )

    def get_po_revision_date(self):
        """Get the PO-Revision-Date header."""
        raise NotImplementedError

    def set_last_translator(self, value):
        r"""Set the Last-Tranlstor header.

        >>> ch = CatalogHeader()
        >>> ch.set_last_translator('Who? Me? <nowhere@somewere.tld>')
        >>> print ch
        #
        msgid ""
        msgstr ""
        "Project-Id-Version: PROJECT VERSION\n"
        "Report-Msgid-Bugs-To: ADDRESS@EMAIL\n"
        "POT-Creation-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "Last-Translator: Who? Me? <nowhere@somewere.tld>\n"
        "Language-Team: LANGUAGE <LL@li.org>\n"
        "MIME-Version: 1.0\n"
        "Content-Type: text/plain; charset=UTF-8\n"
        "Content-Transfer-Encoding: 8bit\n"
        "Plural-Forms: nplurals=INTEGER; plural=EXPRESSION;\n"
        <BLANKLINE>
        """
        value = check_input(value)
        self._headers[LAST_TRANSLATOR] = (
            self._headers[LAST_TRANSLATOR][0], value
        )

    def get_last_translator(self):
        """Get the Last-Tranlstor header."""
        raise NotImplementedError

    def set_language_team(self, value):
        r"""Set the Language-Team header

        >>> ch = CatalogHeader()
        >>> ch.set_language_team('English <nowhere@somewhere.tld>')
        >>> print ch
        #
        msgid ""
        msgstr ""
        "Project-Id-Version: PROJECT VERSION\n"
        "Report-Msgid-Bugs-To: ADDRESS@EMAIL\n"
        "POT-Creation-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
        "Language-Team: English <nowhere@somewhere.tld>\n"
        "MIME-Version: 1.0\n"
        "Content-Type: text/plain; charset=UTF-8\n"
        "Content-Transfer-Encoding: 8bit\n"
        "Plural-Forms: nplurals=INTEGER; plural=EXPRESSION;\n"
        <BLANKLINE>
        """
        value = check_input(value)
        self._headers[LANGUAGE_TEAM] = (
            self._headers[LANGUAGE_TEAM][0], value
        )

    def get_language_team(self):
        """Get the Language-Team header."""
        raise NotImplementedError

    def set_mime_version(self, value):
        r"""Set the MIME-Version header.

        >>> ch = CatalogHeader()
        >>> ch.set_mime_version(5)
        >>> print ch
        #
        msgid ""
        msgstr ""
        "Project-Id-Version: PROJECT VERSION\n"
        "Report-Msgid-Bugs-To: ADDRESS@EMAIL\n"
        "POT-Creation-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
        "Language-Team: LANGUAGE <LL@li.org>\n"
        "MIME-Version: 5\n"
        "Content-Type: text/plain; charset=UTF-8\n"
        "Content-Transfer-Encoding: 8bit\n"
        "Plural-Forms: nplurals=INTEGER; plural=EXPRESSION;\n"
        <BLANKLINE>
        """
        value = check_input(value)
        self._headers[MIME_VERSION] = (
            self._headers[MIME_VERSION][0], value
        )

    def get_mime_version(self):
        """Get the MIME-Version header."""
        raise NotImplementedError

    def set_content_type(self, ctype='text/plain', charset='UTF-8'):
        r"""Set the Content-Type header.

        >>> ch = CatalogHeader()
        >>> ch.set_content_type(charset='ISO-8859-15')
        >>> print ch
        #
        msgid ""
        msgstr ""
        "Project-Id-Version: PROJECT VERSION\n"
        "Report-Msgid-Bugs-To: ADDRESS@EMAIL\n"
        "POT-Creation-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
        "Language-Team: LANGUAGE <LL@li.org>\n"
        "MIME-Version: 1.0\n"
        "Content-Type: text/plain; charset=ISO-8859-15\n"
        "Content-Transfer-Encoding: 8bit\n"
        "Plural-Forms: nplurals=INTEGER; plural=EXPRESSION;\n"
        <BLANKLINE>
        """
        ctype = check_input(ctype)
        charset = check_input(charset)
        self._headers[CONTENT_TYPE] = (
            self._headers[CONTENT_TYPE][0], u'%s; charset=%s' % (ctype, charset)
        )

    def get_content_type(self):
        """Get the Content-Type header."""
        raise NotImplementedError

    def set_content_transfer_encoding(self, encoding='8bit'):
        r"""Set the Contetn-Transfer-Encoding header.

        >>> ch = CatalogHeader()
        >>> ch.set_content_transfer_encoding('7bit')
        >>> print ch
        #
        msgid ""
        msgstr ""
        "Project-Id-Version: PROJECT VERSION\n"
        "Report-Msgid-Bugs-To: ADDRESS@EMAIL\n"
        "POT-Creation-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
        "Language-Team: LANGUAGE <LL@li.org>\n"
        "MIME-Version: 1.0\n"
        "Content-Type: text/plain; charset=UTF-8\n"
        "Content-Transfer-Encoding: 7bit\n"
        "Plural-Forms: nplurals=INTEGER; plural=EXPRESSION;\n"
        <BLANKLINE>
        """
        value = check_input(encoding)
        self._headers[CONTENT_TRANSFER_ENCODING] = (
            self._headers[CONTENT_TRANSFER_ENCODING][0], value
        )

    def get_content_transfer_encoding(self):
        """Get the Contetn-Transfer-Encoding header."""
        raise NotImplementedError

    def set_plural_forms(self, nplurals, expression):
        r"""Set the Plural-Forms header.

        >>> ch = CatalogHeader()
        >>> ch.set_plural_forms(2, '(n != 1)')
        >>> print ch
        #
        msgid ""
        msgstr ""
        "Project-Id-Version: PROJECT VERSION\n"
        "Report-Msgid-Bugs-To: ADDRESS@EMAIL\n"
        "POT-Creation-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
        "Language-Team: LANGUAGE <LL@li.org>\n"
        "MIME-Version: 1.0\n"
        "Content-Type: text/plain; charset=UTF-8\n"
        "Content-Transfer-Encoding: 8bit\n"
        "Plural-Forms: nplurals=2; plural=(n != 1);\n"
        <BLANKLINE>
        >>> ch.set_plural_forms(2, 'n != 1')
        >>> print ch
        #
        msgid ""
        msgstr ""
        "Project-Id-Version: PROJECT VERSION\n"
        "Report-Msgid-Bugs-To: ADDRESS@EMAIL\n"
        "POT-Creation-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
        "Language-Team: LANGUAGE <LL@li.org>\n"
        "MIME-Version: 1.0\n"
        "Content-Type: text/plain; charset=UTF-8\n"
        "Content-Transfer-Encoding: 8bit\n"
        "Plural-Forms: nplurals=2; plural=(n != 1);\n"
        <BLANKLINE>
        """

        nplurals = check_input(nplurals)
        expression = check_input(expression)
        if not expression.startswith('(') and expression != 'EXPRESSION':
            expression = u'(%s' % expression
        if not expression.endswith(')') and expression != 'EXPRESSION':
            expression = u'%s)' % expression
        self._headers[PLURAL_FORMS] = (
            self._headers[PLURAL_FORMS][0],
            u'nplurals=%s; plural=%s;' % (nplurals, expression)
        )

    def get_plural_forms(self):
        """Get the Plural-Forms header."""
        raise NotImplementedError

    def set_custom_header(self, name, value):
        r"""Set's a custom header.

        >>> ch = CatalogHeader()
        >>> ch.set_custom_header('Built-With', 'I18NToolBox 0.1')
        >>> print ch
        #
        msgid ""
        msgstr ""
        "Project-Id-Version: PROJECT VERSION\n"
        "Report-Msgid-Bugs-To: ADDRESS@EMAIL\n"
        "POT-Creation-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
        "Language-Team: LANGUAGE <LL@li.org>\n"
        "MIME-Version: 1.0\n"
        "Content-Type: text/plain; charset=UTF-8\n"
        "Content-Transfer-Encoding: 8bit\n"
        "Plural-Forms: nplurals=INTEGER; plural=EXPRESSION;\n"
        "Built-With: I18NToolBox 0.1\n"
        <BLANKLINE>
        """
        name = check_input(name)
        value = check_input(value)
        self._headers[len(self._headers)+1] = (name, value)

    def get_custom_header(self, name):
        """Get's the value of a custom header by it's name."""
        raise NotImplementedError

    def set_fuzzy(self):
        """Mark the catalog that wil use this header as fuzzy."""
        self.fuzzy = True

    def unset_fuzzy(self):
        """Un-mark the catalog that wil use this header as fuzzy."""
        self.fuzzy = False


class CatalogMessage:
    """Representation of a gettext catalog message

    @param msgid: The catalog message id, ie, the string to be translated
    @param plural: The plural form of the message id
    @param debug: If True, and `check_python_format` also returns True,
    set's the flag 'possible-python-format' instead of 'python-format' on
    the message.

    Contruct a catalog message by passing the message as the first
    argument:

    >>> cm = CatalogMessage('A Testing Message')
    >>> print cm
    msgid "A Testing Message"
    msgstr ""
    <BLANKLINE>
    <BLANKLINE>

    A catalog message's msgid can also be set after instantiation:

    >>> cm = CatalogMessage()
    >>> cm.msgid = 'A Testing Message'
    >>> print cm
    msgid "A Testing Message"
    msgstr ""
    <BLANKLINE>
    <BLANKLINE>
    """

    def __init__(self, msgid=None, plural=None, debug=False):
        self.debug = debug
        self._translator_comments = []
        self._auto_comments = []
        self._references = []
        self._flags = {}
        self._msgstrs = []
        self.msgid = check_input(msgid)
        self.plural = check_input(plural)

    def __str__(self):
        return self.generate().encode('utf-8')

    def __unicode__(self):
        return self.generate()

    def __repr__(self):
        return '<%s "%s">' % (self.__class__.__name__, self.msgid.encode('utf-8'))

    def generate(self):
        """Generates the catalog message's output."""
        msgid = self.msgid
        plural = self.plural
        if not msgid:
            msgid = u'""'
        else:
            msgid = normalize(msgid)
        if plural:
            plural = check_input(normalize(plural))

        if check_python_format(msgid):
            if self.debug:
                self.set_flag(u'possible-python-format')
            else:
                self.set_flag(u'python-format')
        tcomments = [u'# %s\n' % x for x in self._translator_comments if x]
        acomments = [u'#. %s\n' % x for x in self._auto_comments if x]
        references = [u' %s' % x for x in self._references if x]
        if acomments or tcomments:
            self.set_flag(u'fuzzy')
        txt = u''.join(tcomments + acomments)
        if references:
            txt += u'#:%s\n' % u''.join(references)
        if self._flags:
            txt += u'#, %s\n' % u', '.join(
                [key for key in self._flags.keys() if self._flags[key]]
            )
        txt += u'msgid %s\n' % msgid
        if plural:
            txt += u'msgid_plural %s\n' % plural
            msgstrs_len = len(self._msgstrs)
            if self._msgstrs:
                for msg in self._msgstrs:
                    txt += u'msgstr[%d] %s\n' % (
                        self._msgstrs.index(msg),
                        self._msgstrs[self._msgstrs.index(msg)]
                    )
                if msgstrs_len < 2:
                    txt += u'msgstr[1] ""\n'
                txt += u'\n'
            else:
                txt += u'msgstr[0] ""\n'
                txt += u'msgstr[1] ""\n\n'
        else:
            if self._msgstrs:
                txt += u'msgstr %s\n\n' % self._msgstrs[0]
            else:
                txt += u'msgstr ""\n\n'
        return txt

    def _get_comments_list(self, auto=False):
        """Return the correct list of comments.
        translator comments or if `auto` is True, the automatic comments."""
        if auto:
            return self._auto_comments
        return self._translator_comments

    def add_comment(self, comment, auto=False):
        """Adds a comment to the catalog message.

        @param comment: The comment to add to the message.
        @param auto: Marks the comment as an auto-comment.

        >>> cm = CatalogMessage('A Testing Message')
        >>> cm.add_comment('Added a normal comment')
        >>> print cm
        # Added a normal comment
        #, fuzzy
        msgid "A Testing Message"
        msgstr ""
        <BLANKLINE>
        <BLANKLINE>
        >>> cm.add_comment('Added an "auto" comment', auto=True)
        >>> print cm
        # Added a normal comment
        #. Added an "auto" comment
        #, fuzzy
        msgid "A Testing Message"
        msgstr ""
        <BLANKLINE>
        <BLANKLINE>
        """
        comment_list = self._get_comments_list(auto)
        comment = check_input(comment)
        if comment not in comment_list:
            comment_list.append(comment)

    def comments(self, show_auto=False):
        """ Get the list of comments set on the message.
        Adding comments auto-sets the `fuzzy` flag.

        @param show_auto: Display comments marked as automatic.
        Automatic comments come first in the list.

        >>> cm = CatalogMessage('A Testing Message')
        >>> cm.add_comment('Added a normal comment')
        >>> cm.add_comment('Added an "auto" comment', auto=True)
        >>> print cm.comments()
        [u'Added a normal comment']
        >>> print cm.comments(show_auto=True)
        [u'Added an "auto" comment', u'Added a normal comment']
        """
        if show_auto:
            return self._auto_comments + self._translator_comments
        return self._translator_comments

    def add_translation(self, message):
        """ Add a translation to the catalog message
        @param message: The translated message

        >>> cm = CatalogMessage('A Testing Message')
        >>> cm.add_translation('Uma mensagem de teste')
        >>> print cm
        msgid "A Testing Message"
        msgstr "Uma mensagem de teste"
        <BLANKLINE>
        <BLANKLINE>
        """
        #message = to_unicode(message)
        message = check_input(message.strip())
        if message not in self._msgstrs:
            self._msgstrs.append(
                normalize(message.strip())
            )

    def add_reference(self, reference):
        """ Add a reference to the message.

        @param reference: The reference to add

        >>> cm = CatalogMessage('A Testing Message')
        >>> cm.add_reference('/path/to/some/file.py:45')
        >>> print cm
        #: /path/to/some/file.py:45
        msgid "A Testing Message"
        msgstr ""
        <BLANKLINE>
        <BLANKLINE>
        """
        reference = check_input(reference)
        if reference not in self._references:
            self._references.append(reference.strip())

    def references(self):
        """Returns the reference for the message.

        >>> cm = CatalogMessage('A Testing Message')
        >>> cm.add_reference('/path/to/some/file.py:45')
        >>> print cm.references()
        [u'/path/to/some/file.py:45']
        """
        return self._references

    def set_flag(self, flag):
        """Set a flag for the message.

        @param flag: The flag to set. Must be one of 'fuzzy', 'python-format',
        'possible-python-format'.

        >>> cm = CatalogMessage('A Testing Message')
        >>> cm.set_flag('python-format')
        >>> print cm
        #, python-format
        msgid "A Testing Message"
        msgstr ""
        <BLANKLINE>
        <BLANKLINE>
        """
        if flag not in (u'fuzzy', u'python-format', u'possible-python-format'):
            raise FlagError, flag
        if flag == u'python-format' and self._flags.has_key(u'possible-python-format'):
            self.unset_flag(u'possible-python-format')
        elif flag == u'possible-python-format' and self._flags.has_key(u'python-format'):
            self.unset_flag(u'python-format')
        self._flags[flag] = True


    def unset_flag(self, flag):
        """Removes a flag from the message.

        @param flag: The flag to set. Must be one of 'fuzzy', 'python-format',
        'possible-python-format'.

        >>> cm = CatalogMessage('A Testing Message')
        >>> cm.set_flag('python-format')
        >>> print cm
        #, python-format
        msgid "A Testing Message"
        msgstr ""
        <BLANKLINE>
        <BLANKLINE>
        >>> cm.unset_flag('python-format')
        >>> print cm
        msgid "A Testing Message"
        msgstr ""
        <BLANKLINE>
        <BLANKLINE>
        """
        if flag not in (u'fuzzy', u'python-format', u'possible-python-format'):
            raise FlagError, flag
        del(self._flags[flag])


    def flags(self):
        """Returns the list of flags set on the message.

        >>> cm = CatalogMessage('A Testing Message')
        >>> cm.set_flag('fuzzy')
        >>> print cm
        #, fuzzy
        msgid "A Testing Message"
        msgstr ""
        <BLANKLINE>
        <BLANKLINE>
        >>> cm.flags()
        [u'fuzzy']
        """
        return [unicode(flag) for flag in self._flags.keys() if self._flags[flag]]


class Catalog:
    """Representation of a gettext translations catalog"""
    def __init__(self):
        self._header = None
        self._messages = {}
        self.fuzzy = False

    def __str__(self):
        return self.generate().encode('utf-8')

    def __unicode__(self):
        return self.generate()

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def generate(self):
        """Generates the catalog's output."""
        txt = u'%s\n' % self._header
        for msg in self.messages():
            txt += msg.generate()
        return txt

    def set_header(self, header):
        """Set a header to a CatalogHeader instance."""
        if not isinstance(header, CatalogHeader):
            raise Exception, "header must be an instance of CatalogHeader"
        self._header = header

    def header(self):
        """Return the CatalogHeader instance."""
        return self._header

    def set_fuzzy(self):
        """Mark the catalog as fuzzy."""
        if not isinstance(self._header, CatalogHeader):
            raise Exception, "header is not set yet."
        self._header.set_fuzzy()
        self.fuzzy = True

    def unset_fuzzy(self):
        """Remove the fuzzy atribute from the catalog."""
        if not isinstance(self._header, CatalogHeader):
            raise Exception, "header is not set yet."
        self._header.unset_fuzzy()
        self.fuzzy = False

    def add_message(self, message):
        """Add a CatalogMessage instance to the catalog."""
        if not isinstance(message, CatalogMessage):
            raise Exception, "message must be an instance of CatalogMessage"
        if message.msgid not in self._messages.keys():
            self._messages[message.msgid] = (len(self._messages), message)

    def messages(self):
        """Returns the list of CatalogMessage instances the catalog has."""
        messages = self._messages.values()
        messages.sort()
        return [msg for index, msg in messages]


class CatalogParser:
    """Parser to parse gettext catalog .po/.pot files."""
    def __init__(self, infile, debug=False):
        self.infile = infile
        self.debug = debug
        fd = open(infile, 'rt')
        encoding, offset = detect_unicode_encoding(fd.read(4))
        fd.seek(offset)
        self._contents = [line.decode(encoding) for line in fd.readlines()]
        self._messages = {}
        self._header = None
        self._catalog = None
        seen_first_msgid = False
        # Separate header from messages
        for line in self._contents:
            index = self._contents.index(line)
            if line.startswith('msgid'):
                seen_first_msgid = True
            elif line == '\n' and seen_first_msgid:
                self._msgs_ctx = self._contents[index:]
                self._header_ctx = self._contents[:index]
                break
        # We just need a single emtpy line starting self._msgs_ctx
        if self._msgs_ctx[0] == self._msgs_ctx[1] == '\n':
            for line in self._msgs_ctx:
                index = self._msgs_ctx.index(line)
                if self._msgs_ctx[index] == self._msgs_ctx[index+1] == '\n':
                    continue
                else:
                    self._msgs_ctx = self._msgs_ctx[index-1:]
                    break
        # We just need an empty line on the end self._msgs_ctx
        for n in range(len(self._msgs_ctx), 0, -1):
            if self._msgs_ctx[n-1] == u'\n':
                self._msgs_ctx.pop(n-1)
            else:
                # We have "rstrip'ed" all last new lines
                break
        # Now we append the single one we need
        self._msgs_ctx.append(u'\n')

    def __str__(self):
        output = self.get_catalog()
        return output.encode('utf-8')

    def __unicode__(self):
        return self.get_catalog()

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def get_messages(self):
        """Get the messages the parser has set up."""
        messages = self._messages.values()
        messages.sort()
        return [msg for index, msg in messages]

    def get_header(self):
        """Get the header the parser has set up."""
        if not self._header:
            raise Exception, "Header is still not set, plese run `parse_header()` first"
        return self._header

    def get_catalog(self):
        """Get the catalog's printable representation."""
        if not self._catalog:
            self._catalog = Catalog()

        if not self._header:
            raise Exception, "Header is still not set, please run `parse_header()` first"
        if not self._catalog._header:
            self._catalog.set_header = self._header
        if not self._messages:
            raise Exception, "Messages are still not set, please run `parse_messages()` first"
        if not self._catalog._messages:
            self._catalog.set_messages = self._messages
        return self._catalog

    def parse(self):
        """Parse both the header and the messages of a gettext catalog."""
        self.parse_header()
        self.parse_messages()
        catalog = Catalog()
        catalog._header = self._header
        catalog._messages = self._messages
        self._catalog = catalog

    def parse_header(self):
        """Parser the header of a gettext catalog."""
        # This searching behaviour will fail if a header ocupies more
        # than one line
        lines = self._header_ctx
        header = CatalogHeader()
        for line in lines:
            if line.startswith('# '):
                header.add_comment(line[2:].strip())
            elif line.startswith('#, fuzzy'):
                header.set_fuzzy()
            elif line.startswith('"Project-Id-Version: '):
                offset = len('"Project-Id-Version: ')
                info = line[offset:-4].split()
                header.set_project_id_version(''.join(info[:-1]), info[-1:][0])
            elif line.startswith('"Report-Msgid-Bugs-To: '):
                offset = len('"Report-Msgid-Bugs-To: ')
                header.set_report_msgid_bugs_to(line[offset:-4])
            elif line.startswith('"POT-Creation-Date: '):
                offset = len('"POT-Creation-Date: ')
                header.set_pot_creation_date(line[offset:-4])
            elif line.startswith('"PO-Revision-Date: '):
                offset = len('"PO-Revision-Date: ')
                header.set_po_revision_date(line[offset:-4])
            elif line.startswith('"Last-Translator: '):
                offset = len('"Last-Translator: ')
                header.set_last_translator(line[offset:-4])
            elif line.startswith('"Language-Team: '):
                offset = len('"Language-Team: ')
                header.set_language_team(line[offset:-4])
            elif line.startswith('"MIME-Version: '):
                offset = len('"MIME-Version: ')
                header.set_mime_version(line[offset:-4])
            elif line.startswith('"Content-Type: '):
                offset = len('"Content-Type: ')
                ctype, charset = line[offset:-4].split()
                ctype, charset = ctype[:-1], charset[8:]
                header.set_content_type(ctype, charset)
            elif line.startswith('"Content-Transfer-Encoding: '):
                offset = len('"Content-Transfer-Encoding: ')
                header.set_content_transfer_encoding(line[offset:-4].strip())
            elif line.startswith('"Plural-Forms: '):
                tline = eval(line)[13:].strip()
                nplurals, expression = tline.split(' ', 1)
                nplurals, expression = nplurals[9:-1], expression[7:-1]
                header.set_plural_forms(nplurals, expression)
            elif line.startswith('"'):
                tline = eval(line.strip())
                offset = tline.find(':')
                name, value = tline[:offset].strip(), tline[offset+1:].strip()
                header.set_custom_header(name, value)
            else:
                continue
        self._header = header

    def parse_messages(self):
        """asdParser the messages of a gettext catalog."""
        lines = self._msgs_ctx
        new_msgid = False
        msgid = None
        msgid_plural = None
        msgstr = []
        comments = []
        auto = []
        refs = []
        flags = None
        init_msg = False
        for line in lines:
            if line == '\n' and not new_msgid:
                new_msgid = True
                init_msg = False
                comments = []
                refs = []
                flags = []
                msgid = None
                msgid_plural = None
                msgstr = []
                auto = []
                continue
            elif line == '\n' and new_msgid:
                init_msg = True
                new_msgid = False
            if line.startswith('# '):
                comments.append(line.strip()[2:])
            elif line.startswith('#. '):
                auto.append(line.strip()[3:])
            elif line.startswith('#: '):
                for ref in line.strip()[3:].split(' '):
                    refs.append(ref.strip())
            elif line.startswith('#, '):
                for flag in line.strip()[3:].split(','):
                    flags.append(flag.strip())
            elif line.startswith('msgid '):
                try:
                    msgid = eval(line.strip()[6:])
                except Exception, error:
                    print >> sys.stderr, 'Escape error on %s:%d' % \
                            (self.infile, self._contents.index(line)), 'before:', `line[6:-1]`
                    raise ParseError(error)
                try:
                    msgid = msgid.decode('utf-8')
                except UnicodeDecodeError, error:
                    print >> sys.stderr, 'Encoding error on %s:%d' % \
                            (self.infile, self._contents.index(line)), 'before:', `line.strip()[6:]`
                    raise ParseError(error)
            elif line.startswith('msgid_plural '):
                try:
                    msgid_plural = eval(line.strip()[13:])
                except Exception, error:
                    print >> sys.stderr, 'Escape error on %s:%d' % \
                            (self.infile, self._contents.index(line)), \
                            'before:', `line.strip()[13:]`
                    raise ParseError(error)
                try:
                    msgid_plural = msgid_plural.decode('utf-8')
                except UnicodeDecodeError, error:
                    print >> sys.stderr, 'Encoding error on %s:%d' % \
                            (self.infile, self._contents.index(line)), \
                            'before:', `line.strip()`
                    raise ParseError(error)
            elif line.startswith('msgstr '):
                try:
                    tmsgstr = eval(line.strip()[7:])
                except Exception, error:
                    print >> sys.stderr, 'Escape error on %s:%d' % \
                            (self.infile, self._contents.index(line)), \
                            'before:', `line.strip()[7:]`
                    raise ParseError(error)
                try:
                    tmsgstr = tmsgstr.decode('utf-8')
                except UnicodeDecodeError, error:
                    print >> sys.stderr, 'Encoding error on %s:%d' % \
                            (self.infile, self._contents.index(line)), \
                            'before:', `tmsgstr`
                    raise ParseError(error)
                msgstr.append(tmsgstr)
            elif line.startswith('msgstr['):
                try:
                    tmsgstr = eval(line.strip()[10:])
                except Exception, error:
                    print >> sys.stderr, 'Escape error on %s:%d' % \
                            (self.infile, self._contents.index(line)), \
                            'before:', `line.strip()[10:]`
                    raise ParseError(error)
                try:
                    tmsgstr = tmsgstr.decode('utf-8')
                except UnicodeDecodeError, error:
                    print >> sys.stderr, 'Encoding error on %s:%d' % \
                            (self.infile, self._contents.index(line)), \
                            'before:', `tmsgstr`
                    raise ParseError(error)
                msgstr.append(tmsgstr)
            if init_msg:
                msg =  None
                index = None
                if msgid_plural in self._messages.keys():
                    index, msg =  self._messages[msgid_plural]
                elif msgid in self._messages.keys():
                    index, msg =  self._messages[msgid]
                else:
                    if msgid_plural:
                        msg =  CatalogMessage(msgid, msgid_plural, debug=self.debug)
                    else:
                        msg =  CatalogMessage(msgid, debug=self.debug)
                if comments:
                    for comment in comments:
                        msg.add_comment(comment)
                if auto:
                    for comment in auto:
                        msg.add_comment(comment, True)
                if flags:
                    for flag in flags:
                        msg.set_flag(flag)
                if refs:
                    for ref in refs:
                        msg.add_reference(ref)
                if msgstr:
                    if len(msgstr) == 1:
                        msg.add_translation(msgstr[0])
                    else:
                        for message in msgstr:
                            msg.add_translation(message)
                if index:
                    self._messages[msg.msgid] = (index, msg)
                else:
                    self._messages[msg.msgid] = (len(self._messages), msg)
                msg =  None
                new_msgid = True
                init_msg = False
                comments = []
                refs = []
                flags = []
                msgid = None
                msgid_plural = None
                msgstr = []
                auto = []



def main():
    from datetime import datetime
    header = CatalogHeader()
    header.set_project_id_version('Catalog Test', '0.1')
    header.set_report_msgid_bugs_to('noreply@nowhere.tld')
    header.set_pot_creation_date(datetime.today().strftime('%Y-%M-%d %H:%M+000'))
    header.set_plural_forms("2", "(n != 1)")
    header.add_comment('Translation File for Catalog Test')
    header.set_fuzzy()
    print 'HEADER >>>'
    print header
    print '<<< HEADER'
    print


    msg1 = CatalogMessage('Foo Bar')
    msg1.add_comment('Just Trying out a Comment')
    msg1.add_comment('This is an automated comment', True)
    msg1.add_reference('foobar.py:5')
    msg1.set_flag('fuzzy')
    print 'M1 >>>'
    print msg1
    print '<<< M1'
    print


    msg2 = CatalogMessage('Foo Bar %d', 'Foo Bars %d')
    msg2.add_comment('This is an automated comment', True)
    msg2.add_translation(u'Este é Foo Bar')
    #msg2.set_flag('python-format')
    msg2.add_reference('foo.py:2')
    print 'M2 >>>'
    print msg2
    print '<<< M2'
    print


    catalog = Catalog()
    catalog.set_header(header)
    catalog.add_message(msg1)
    catalog.add_message(msg2)

    print 'CATALOG >>>'
    print catalog
    print '<<< CATALOG'

    print 'CATALOG MESSAGES>>>'
    for message in catalog.messages():
        print message
    print '<<< CATALOG MESSAGES'

if __name__ == '__main__':
#    pass
    main()

