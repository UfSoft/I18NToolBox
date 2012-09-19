# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: catalog.py 25 2007-01-06 19:05:17Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/trunk/I18NToolBox/lib/tests/catalog.py $
# $LastChangedDate: 2007-01-06 19:05:17 +0000 (Sat, 06 Jan 2007) $
# $Rev: 25 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import os
import unittest
import doctest

from I18NToolBox.lib.catalog import CatalogHeader, CatalogMessage, Catalog, \
        CatalogParser, check_input

# I'm using Portuguese as the language to test the module because it contains
# accented characters which minimally covers possible unicode problems

class MinimalCM(unittest.TestCase):
    def setUp(self):
        """Setup a minimal CatalogMessage to reuse."""
        cm = CatalogMessage()
        cm.msgid = u"Só para testar a classe CatalogMessage"
        self.cm = cm

    def test_StrOutputType(self):
        assert isinstance(str(self.cm), str)

    def test_StrActualOutput(self):
        assert str(self.cm) == 'msgid "S\xc3\xb3 para testar a classe CatalogMessage"\nmsgstr ""\n\n'

    def test_UnicodeOutputType(self):
        assert isinstance(unicode(self.cm), unicode)

    def test_UnicodeActualOutput(self):
        assert unicode(self.cm) == u'msgid "S\xf3 para testar a classe CatalogMessage"\nmsgstr ""\n\n'


class SimpleCM(unittest.TestCase):
    def setUp(self):
        """Setup a simple CatalogMessage to reuse."""
        cm = CatalogMessage(u"Só para testar a classe CatalogMessage")
        # Add a comment
        cm.add_comment(u"Um comentário normal")
        # Add a reference
        cm.add_reference("/some/path/to/file.py:22")
        self.cm = cm

    def test_StrActualOutput(self):
        assert str(self.cm) == '# Um coment\xc3\xa1rio normal\n' + \
                '#: /some/path/to/file.py:22\n#, fuzzy\n' + \
                'msgid "S\xc3\xb3 para testar a classe CatalogMessage"\nmsgstr ""\n\n'

    def test_UnicodeActualOutput(self):
        assert unicode(self.cm) == u'# Um coment\xe1rio normal\n' + \
                u'#: /some/path/to/file.py:22\n#, fuzzy\n' + \
                u'msgid "S\xf3 para testar a classe CatalogMessage"\nmsgstr ""\n\n'

    def test_Comments(self):
        assert self.cm.comments() == [u'Um coment\xe1rio normal']

    def test_DuplicatingSameComment(self):
        self.cm.add_comment(u"Um comentário normal")
        assert self.cm.comments() == [u'Um coment\xe1rio normal']

    def test_References(self):
        assert self.cm.references() == [u'/some/path/to/file.py:22']


class ComplexCM(unittest.TestCase):
    def setUp(self):
        """Setup a complex CatalogMessage to reuse."""
        cm = CatalogMessage(u"Só para testar a classe CatalogMessage")
        # Add a comment
        cm.add_comment(u"Um comentário normal")
        # Add a reference
        cm.add_reference("/some/path/to/file.py:22")
        # override msgid to contain some python-formats
        cm.msgid = u"Só para testar %d classe CatalogMessage"
        # Set debug to true to change the python-formats formatting
        cm.debug = True
        # Add an "auto" comment
        cm.add_comment(u"Um comentário automático", auto=True)
        # One more reference
        cm.add_reference("/another/path/to/file.py:44")
        # Let's add a translation
        cm.add_translation("Just to test %d class CatalogMessage")
        self.cm = cm

    def test_StrOutputType(self):
        assert isinstance(str(self.cm), str)

    def test_UnicodeOutput(self):
        assert isinstance(unicode(self.cm), unicode)

    def test_GenerateOutputsUnicode(self):
        assert isinstance(self.cm.generate(), unicode)

    def test_StrActualOutput(self):
        assert str(self.cm) == '# Um coment\xc3\xa1rio normal\n' + \
                '#. Um coment\xc3\xa1rio autom\xc3\xa1tico\n' + \
                '#: /some/path/to/file.py:22 /another/path/to/file.py:44\n' + \
                '#, fuzzy, possible-python-format\n' + \
                'msgid "S\xc3\xb3 para testar %d classe CatalogMessage"\n' + \
                'msgstr "Just to test %d class CatalogMessage"\n\n'

    def test_UnicodeActualOuput(self):
        assert unicode(self.cm) == u'# Um coment\xe1rio normal\n' + \
                u'#. Um coment\xe1rio autom\xe1tico\n' + \
                u'#: /some/path/to/file.py:22 /another/path/to/file.py:44\n' + \
                u'#, fuzzy, possible-python-format\n' + \
                u'msgid "S\xf3 para testar %d classe CatalogMessage"\n' + \
                u'msgstr "Just to test %d class CatalogMessage"\n\n'

    def test_ReprOutput(self):
        # This will ouput an UTF-8 encoded string
        assert repr(self.cm) == '<CatalogMessage "Só para testar %d classe CatalogMessage">'

    def test_References(self):
        assert self.cm.references() == [u'/some/path/to/file.py:22', u'/another/path/to/file.py:44']

    def test_Comments(self):
        # Normal Comments
        assert self.cm.comments() == [u'Um coment\xe1rio normal']
        # Auto comments come first
        assert self.cm.comments(show_auto=True)[0] == u'Um coment\xe1rio autom\xe1tico'
        # All comments
        assert self.cm.comments(show_auto=True) == [
            u'Um coment\xe1rio autom\xe1tico', u'Um coment\xe1rio normal'
        ]

class CatalogHeaderTest(unittest.TestCase):
    """We'll just set some headers and see if they are actually set.
    This test will be completed by the CatalogHeader class doctests.
    """
    def setUp(self):
        ch = CatalogHeader()
        ch.add_comment("I18NToolBox Project")
        ch.add_comment("Copyright 2010 FoBar")
        self.ch = ch

    def test_Comments(self):
        assert self.ch.comments() == [u'I18NToolBox Project', u'Copyright 2010 FoBar']

    def test_StrOuputType(self):
        assert isinstance(str(self.ch), str)

    def test_UnicodeOutputType(self):
        assert isinstance(unicode(self.ch), unicode)

    def test_GenerateOutputsUnicode(self):
        assert isinstance(self.ch.generate(), unicode)

    def test_StrActualOutput(self):
        assert str(self.ch) == '# I18NToolBox Project\n' + \
                '# Copyright 2010 FoBar\n#\nmsgid ""\nmsgstr ""\n' + \
                '"Project-Id-Version: PROJECT VERSION\\n"\n' + \
                '"Report-Msgid-Bugs-To: ADDRESS@EMAIL\\n"\n' + \
                '"POT-Creation-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n' + \
                '"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n' + \
                '"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"\n' + \
                '"Language-Team: LANGUAGE <LL@li.org>\\n"\n' + \
                '"MIME-Version: 1.0\\n"\n' + \
                '"Content-Type: text/plain; charset=UTF-8\\n"\n' + \
                '"Content-Transfer-Encoding: 8bit\\n"\n' + \
                '"Plural-Forms: nplurals=INTEGER; plural=EXPRESSION;\\n"\n'

    def test_UnicodeActualOutput(self):
        assert unicode(self.ch) == u'# I18NToolBox Project\n' + \
                u'# Copyright 2010 FoBar\n#\nmsgid ""\nmsgstr ""\n' + \
                u'"Project-Id-Version: PROJECT VERSION\\n"\n' + \
                u'"Report-Msgid-Bugs-To: ADDRESS@EMAIL\\n"\n' + \
                u'"POT-Creation-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n' + \
                u'"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n' + \
                u'"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"\n' + \
                u'"Language-Team: LANGUAGE <LL@li.org>\\n"\n' + \
                u'"MIME-Version: 1.0\\n"\n' + \
                u'"Content-Type: text/plain; charset=UTF-8\\n"\n' + \
                u'"Content-Transfer-Encoding: 8bit\\n"\n' + \
                u'"Plural-Forms: nplurals=INTEGER; plural=EXPRESSION;\\n"\n'

    def test_GenerateActualOutput(self):
        assert self.ch.generate() == u'# I18NToolBox Project\n' + \
                u'# Copyright 2010 FoBar\n#\nmsgid ""\nmsgstr ""\n' + \
                u'"Project-Id-Version: PROJECT VERSION\\n"\n' + \
                u'"Report-Msgid-Bugs-To: ADDRESS@EMAIL\\n"\n' + \
                u'"POT-Creation-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n' + \
                u'"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n' + \
                u'"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"\n' + \
                u'"Language-Team: LANGUAGE <LL@li.org>\\n"\n' + \
                u'"MIME-Version: 1.0\\n"\n' + \
                u'"Content-Type: text/plain; charset=UTF-8\\n"\n' + \
                u'"Content-Transfer-Encoding: 8bit\\n"\n' + \
                u'"Plural-Forms: nplurals=INTEGER; plural=EXPRESSION;\\n"\n'

    def test_Comments(self):
        assert self.ch.comments() == [u'I18NToolBox Project', u'Copyright 2010 FoBar']

    def test_SetFuzzy(self):
        self.ch.set_fuzzy()
        assert self.ch.generate().splitlines()[3] == u'#, fuzzy'


class CatalogTest(unittest.TestCase):
    def setUp(self):
        ch = CatalogHeader()
        ch.add_comment("I18NToolBox Project")
        ch.add_comment("Copyright 2010 FoBar")

        cm1 = CatalogMessage(u"Só para testar a classe Catalog")
        cm1.add_comment(u"Um comentário normal")
        cm1.add_reference("/some/path/to/file.py:22")

        cm2 = CatalogMessage(u"Só para testar %d classe CatalogMessage")
        cm2.add_comment(u"Um comentário automático", auto=True)
        cm2.add_reference("/another/path/to/file.py:44")
        cm2.add_translation("Just to test %d class CatalogMessage")

        cat = Catalog()
        cat.set_header(ch)
        cat.add_message(cm1)
        cat.add_message(cm2)
        self.cat = cat

    def test_StrOutputType(self):
        assert isinstance(str(self.cat), str)

    def test_UnicodeOutputType(self):
        assert isinstance(unicode(self.cat), unicode)

    def test_GenerateOutputsUnicode(self):
        assert isinstance(self.cat.generate(), unicode)

    def test_StrActualOutput(self):
        assert str(self.cat) == '# I18NToolBox Project\n' + \
                '# Copyright 2010 FoBar\n' + \
                '#\n' + \
                'msgid ""\n' + \
                'msgstr ""\n' + \
                '"Project-Id-Version: PROJECT VERSION\\n"\n' + \
                '"Report-Msgid-Bugs-To: ADDRESS@EMAIL\\n"\n' + \
                '"POT-Creation-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n' + \
                '"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n' + \
                '"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"\n' + \
                '"Language-Team: LANGUAGE <LL@li.org>\\n"\n' + \
                '"MIME-Version: 1.0\\n"\n' + \
                '"Content-Type: text/plain; charset=UTF-8\\n"\n' + \
                '"Content-Transfer-Encoding: 8bit\\n"\n' + \
                '"Plural-Forms: nplurals=INTEGER; plural=EXPRESSION;\\n"\n' + \
                '\n' + \
                '# Um coment\xc3\xa1rio normal\n' + \
                '#: /some/path/to/file.py:22\n' + \
                '#, fuzzy\n' + \
                'msgid "S\xc3\xb3 para testar a classe Catalog"\n' + \
                'msgstr ""\n' + \
                '\n' + \
                '#. Um coment\xc3\xa1rio autom\xc3\xa1tico\n' + \
                '#: /another/path/to/file.py:44\n' + \
                '#, fuzzy, python-format\n' + \
                'msgid "S\xc3\xb3 para testar %d classe CatalogMessage"\n' + \
                'msgstr "Just to test %d class CatalogMessage"\n' + \
                '\n'

    def test_UnicodeActualOutput(self):
        assert unicode(self.cat) == u'# I18NToolBox Project\n' + \
                u'# Copyright 2010 FoBar\n' + \
                u'#\n' + \
                u'msgid ""\n' + \
                u'msgstr ""\n' + \
                u'"Project-Id-Version: PROJECT VERSION\\n"\n' + \
                u'"Report-Msgid-Bugs-To: ADDRESS@EMAIL\\n"\n' + \
                u'"POT-Creation-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n' + \
                u'"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n' + \
                u'"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"\n' + \
                u'"Language-Team: LANGUAGE <LL@li.org>\\n"\n' + \
                u'"MIME-Version: 1.0\\n"\n' + \
                u'"Content-Type: text/plain; charset=UTF-8\\n"\n' + \
                u'"Content-Transfer-Encoding: 8bit\\n"\n' + \
                u'"Plural-Forms: nplurals=INTEGER; plural=EXPRESSION;\\n"\n' + \
                u'\n' + \
                u'# Um coment\xe1rio normal\n' + \
                u'#: /some/path/to/file.py:22\n' + \
                u'#, fuzzy\n' + \
                u'msgid "S\xf3 para testar a classe Catalog"\n' + \
                u'msgstr ""\n' + \
                u'\n' + \
                u'#. Um coment\xe1rio autom\xe1tico\n' + \
                u'#: /another/path/to/file.py:44\n' + \
                u'#, fuzzy, python-format\n' + \
                u'msgid "S\xf3 para testar %d classe CatalogMessage"\n' + \
                u'msgstr "Just to test %d class CatalogMessage"\n' + \
                u'\n'

    def test_GenerateAndUnicodeOutputEqual(self):
        assert self.cat.generate() == unicode(self.cat)

    def test_SetHeaderFuzzyFromCatalog(self):
        self.cat.set_fuzzy()
        ch = self.cat.header()
        assert ch.fuzzy

    def test_UnSetHeaderFuzzyFromCatalog(self):
        self.cat.set_fuzzy()
        ch = self.cat.header()
        assert ch.fuzzy == self.cat.fuzzy
        self.cat.unset_fuzzy()
        ch = self.cat.header()
        assert not ch.fuzzy and not self.cat.fuzzy

    def test_CatalogMessages(self):
        msgs = self.cat.messages()
        # Returns Lists?
        assert isinstance(msgs, list)
        # We only defined two CatalogMessages, doe it return two?
        assert len(msgs) == 2
        # And each of them are CatalogMessages
        for msg in msgs:
            assert isinstance(msg, CatalogMessage)


class CatalogParserTest(unittest.TestCase):
    def setUp(self):
        potfile = os.path.join(os.path.dirname(__file__), 'data', 'test.pot')
        parser = CatalogParser(potfile)
        parser.parse()
        self.potfile = potfile
        self.parser = parser

    def test_CorrectParsedHeaderOutput(self):
        header = self.parser.get_header()
        assert header.generate() == u'# I18NToolBox Project\n' + \
                u'# Copyright 2010 FoBar\n' + \
                u'#\n' + \
                u'#, fuzzy\n' + \
                u'msgid ""\n' + \
                u'msgstr ""\n' + \
                u'"Project-Id-Version: PROJECT VERSION\\n"\n' + \
                u'"Report-Msgid-Bugs-To: ADDRESS@EMAIL\\n"\n' + \
                u'"POT-Creation-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n' + \
                u'"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n' + \
                u'"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"\n' + \
                u'"Language-Team: LANGUAGE <LL@li.org>\\n"\n' + \
                u'"MIME-Version: 1.0\\n"\n' + \
                u'"Content-Type: text/plain; charset=UTF-8\\n"\n' + \
                u'"Content-Transfer-Encoding: 8bit\\n"\n' + \
                u'"Plural-Forms: nplurals=2; plural=(n != 1);\\n"\n' + \
                u'"Built-With: I18NToolBox 0.1\\n"\n'

    def test_CorrentLenOfMessagesList(self):
        assert len(self.parser.get_messages()) == 3

    def test_CorrectParsedMessagesOutput(self):
        messages = self.parser.get_messages()
        assert messages[0].generate() == u'# Um coment\xe1rio normal\n' + \
                u'#: /some/path/to/file.py:22\n' + \
                u'#, fuzzy\n' + \
                u'msgid "S\xf3 para testar a classe Catalog"\n' + \
                u'msgstr ""\n' + \
                u'\n'
        assert messages[1].generate() == u'#. Um coment\xe1rio autom\xe1tico\n' + \
                u'#: /another/path/to/file.py:44\n' + \
                u'#, fuzzy, python-format\n' + \
                u'msgid "S\xf3 para testar %d classe CatalogMessage"\n' + \
                u'msgstr "Just to test %d class CatalogMessage"\n' + \
                u'\n'
        assert messages[2].generate() == u'# A message in plural Form\n' + \
                u'#: /some/path/to/file.py:66\n' + \
                u'#, fuzzy, python-format\n' + \
                u'msgid "S\xf3 para outra vez testar %d classe CatalogMessage"\n' + \
                u'msgid_plural "S\xf3 para outra vez testar %d classes CatalogMessage"\n' + \
                u'msgstr[0] "Just to test again %d CatalogMessage class"\n' + \
                u'msgstr[1] "Just to test again %d CatalogMessage classes"\n' + \
                u'\n'

    def test_GeneratedOutputEqualsFile(self):
        # Opened and Generated files might have a different number of
        # new lines on the end of the file, we just rstrip them
        r_potfile = open(self.potfile).read().rstrip().splitlines()
        g_potfile = str(self.parser.get_catalog()).rstrip().splitlines()
        try:
            assert len(r_potfile) == len(g_potfile)
        except AssertionError, error:
            print "Number of lines do not match; file:%d, generated:%d" % \
                    (len(r_potfile), len(g_potfile))
            raise AssertionError, error
        for n in range(len(r_potfile)):
            # We know the the python-formats are different on one of the lines
            # because we didn't pass debug=True to the CatalogParser
            if r_potfile[n] == '#, fuzzy, possible-python-format' and \
               g_potfile[n] == '#, fuzzy, python-format':
                continue
            else:
                try:
                    assert r_potfile[n] == g_potfile[n]
                except AssertionError, error:
                    print 'Failed Assertion in line %d. Lines do not match.' % n
                    print repr(r_potfile[n]), '\n', repr(g_potfile[n])
                    raise AssertionError, error


class CheckInputTest(unittest.TestCase):

    def test_NonEncodedString(self):
        string = 'É uma string codificada'
        self.failUnlessRaises(UnicodeError, check_input, string)

    def test_UTF8_EncodedString(self):
        string = u'É uma string codificada'.encode('utf-8')
        self.failUnlessRaises(UnicodeError, check_input, string)

    def test_ISO_8859_15_EncodedString(self):
        string = u'É uma string codificada'.encode('iso-8859-15')
        self.failUnlessRaises(UnicodeError, check_input, string)

    def test_NonProblematicISO_8859_1_EncodedString(self):
        assert check_input(
            u'A Normal But Encoded String'.encode('iso-8859-15')
        ) == u'A Normal But Encoded String'

    def test_UnicodeInput(self):
        assert check_input(u'É uma string codificada') == \
                u'\xc9 uma string codificada'



def suite():
    suite = unittest.TestSuite()
    suite.addTest(doctest.DocTestSuite(CatalogMessage.__module__))
    suite.addTest(unittest.makeSuite(MinimalCM, 'test'))
    suite.addTest(unittest.makeSuite(SimpleCM, 'test'))
    suite.addTest(unittest.makeSuite(ComplexCM, 'test'))
    suite.addTest(doctest.DocTestSuite(CatalogHeader.__module__))
    suite.addTest(unittest.makeSuite(CatalogHeaderTest, 'test'))
    suite.addTest(doctest.DocTestSuite(Catalog.__module__))
    suite.addTest(unittest.makeSuite(CatalogTest, 'test'))
    suite.addTest(unittest.makeSuite(CatalogParserTest, 'test'))
    suite.addTest(unittest.makeSuite(CheckInputTest, 'test'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
