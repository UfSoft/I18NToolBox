# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: add.py 26 2007-01-07 16:50:51Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/trunk/I18NToolBox/commands/add.py $
# $LastChangedDate: 2007-01-07 16:50:51 +0000 (Sun, 07 Jan 2007) $
# $Rev: 26 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import os
import codecs
import optparse
from datetime import date

from I18NToolBox.commands import check_formencode_support
from I18NToolBox.lib.catalog import CatalogParser
from I18NToolBox.lib.gettext_tables import *

class NewTranslationCatalogTool:
    desc = "Creates a message catalog for specified locale"
    name = "add"
    package = None
    defaults = None
    __version__     = "0.1"
    __author__      = "Pedro ALgarvio"
    __email__       = "ufs@ufsoft.org"
    __copyright__   = "Copyright 2006 Pedro Algarvio"
    __license__     = "BSD"

    def __init__(self, version):
        parser = optparse.OptionParser(
            usage="%prog " + self.name + " <locale> [options]", version="%prog " + self.__version__
        )
        parser.description = self.desc
        parser.add_option(
            '-l', '--locale',
            dest = 'locale',
            help = "locale to build a new message catalog for. "
            "In the form language_COUNTRY, ie, en_GB"
        )
        parser.add_option(
            '--formencode-support',
            dest = 'formencode_support',
            action = 'store_true',
            default = False,
            help = "Translatable strings from FormEncode will be included in "
            "your pot file. If translations are also available, they will "
            "also be included."
        )
        parser.add_option(
            '-F', '--force',
            dest = 'force_destructive',
            action = 'store_true',
            default = False,
            help = "Force destructive actions. This enables existing files "
            "to be overridden. Default: %default"
        )
        parser.add_option(
            '--debug',
            dest = 'debug',
            action = 'store_true',
            default = False,
            help = "more detailed formatstring recognition result. Default: %default"
        )
        self.parser = parser

    def parse_args(self):
        return self.parser.parse_args()

    def run(self):
        (options, args) = self.parse_args()
        if len(args) > 1:
            self.parser.error("The only acceptable argument is a locale")
        if not options.locale and len(args) < 1:
            self.parser.error("You must at least pass a locale")
        if len(args) == 1 and not options.locale:
            options.locale = args[0]

        if options.locale not in locales_table and options.locale not in ('en_GB', 'en_US'):
            self.parser.error("The locale %r is not known" % options.locale)

        if not os.path.isfile(self.defaults['potfile_path']):
            self.parser.error(
                "%r was found. Please run the `extract` command first" % \
                self.defaults['potfile_path']
            )

        if options.formencode_support:
            if check_formencode_support(self.parser):
                import formencode

        short_lang = options.locale.split('_')[0]
        plurals = [x for x in plurals_table if x[0] == short_lang][0]
        if not plurals:
            short_lang, long_lang, nplurals, expr = (
                short_lang,
                [x[1] for x in lang_table if x[0] == short_lang][0],
                None,
                None
            )

        else:
            short_lang, long_lang, nplurals, expr = plurals

        i18n_locale_path = os.path.join(self.defaults['i18n_path'], options.locale)
        i18n_locale_po = os.path.join(
            i18n_locale_path,
            self.defaults['potfile'].replace('.pot', '.po')
        )
        if not options.force_destructive:
            if os.path.exists(i18n_locale_po):
                self.parser.error(
                    "%r already exists. " % i18n_locale_po + \
                    "Pass '--force' or delete the file."
                )
        if not os.path.exists(i18n_locale_path):
            os.mkdir(i18n_locale_path, 0775)

        data = file(self.defaults['potfile_path'], 'rb').readlines()
        inside_translations = True
        for line in data:
            index = data.index(line)
            if line.find("#: ") != -1:
                inside_translations = True
            if inside_translations and line.find('possible-python-format') != -1:
                # gettext msginit converts these, and so should we
                data[index] = data[index].replace(
                    'possible-python-format',
                    'python-format'
                )
                continue
            if line.find('SOME DESCRIPTIVE TITLE.') != -1:
                data[index] = data[index].replace(
                    'SOME DESCRIPTIVE TITLE.',
                    '%s translations for the %s package' % \
                    (long_lang, self.defaults['name'])
                )
            if line.find('Translation Template for the %s package' % \
                         self.defaults['name']) != -1:
                data[index] = data[index].replace(
                    'Translation Template for the %s package' % \
                    self.defaults['name'],
                    '%s translations for the %s package' % \
                    (long_lang, self.defaults['name'])
                )
            if line.find('Content-Type:') != -1:
                data[index] = '"Content-Type: text/plain; charset=UTF-8\\n"\n'
            if line.find('VERSION') != -1:
                data[index] = data[index].replace(
                    'VERSION', self.defaults['version']
                )
            if line.find('PACKAGE') != -1:
                data[index] = data[index].replace(
                    'PACKAGE', self.defaults['name']
                )
            if line.find('YEAR') != -1 and not line.find('PO-Revision-Date') == 1:
                data[index] = data[index].replace(
                    'YEAR', str(date.today().year)
                )
            if line.find('#, fuzzy\n') != -1:
                # Clear the fuzzy mark else the .mo file won't
                # compile correctly
                data[index] = data[index].replace(
                    '#, fuzzy\n', ''
                )
            if line.find("nplurals=INTEGER;") != -1:
                if nplurals:
                    data[index] = data[index].replace(
                        "nplurals=INTEGER;",
                        "nplurals=%s;" % nplurals
                    )
            if line.find("plural=EXPRESSION;") != -1:
                if expr:
                    data[index] = data[index].replace(
                        "plural=EXPRESSION;",
                        "plural=%s;" % expr
                    )
        if options.formencode_support:
            fe_pot_path = os.path.join(
                formencode.api.get_localedir(),
                options.locale,
                'LC_MESSAGES',
                'FormEncode.po'
            )
            fe_comment = 'From formencode/i18n/%s/LC_MESSAGES/FormEncode.po' % options.locale
            if not os.path.exists(fe_pot_path):
                fe_pot_path = os.path.join(
                    formencode.api.get_localedir(),
                    short_lang,
                    'FormEncode.po'
                )
                fe_comment = 'From formencode/i18n/%s/LC_MESSAGES/FormEncode.po' % short_lang
            if not os.path.exists(fe_pot_path):
                fe_pot_path = os.path.join(
                    formencode.api.get_localedir(),
                    'FormEncode.pot'
                )
                fe_comment = 'From formencode/i18n/FormEncode.pot'
                print "Unfortunately there's no FormEncode translation to " + \
                        "the passed locale %r." % options.locale
                print "Copying untranslated messages from FormEncode's " + \
                        "'FormEncode.pot' template."


            parser = CatalogParser(fe_pot_path, options.debug)
            parser.parse_messages()
            fe_data = [u'\n']
            for entry in parser.get_messages():
                entry.add_comment(fe_comment)
                fe_data.append(str(entry))
            data.extend(fe_data)
        #f = codecs.open(i18n_locale_po, 'wb', 'utf-8')#.writelines(data)
        #for line in data:
        #    f.write(str(line).encode('utf-8'))
        #f.close()
        file(i18n_locale_po, 'wb').writelines(data)


def main():
    tool = NewTranslationCatalogTool()
    tool.run()

if __name__ == '__main__':
    main()
