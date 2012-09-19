# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: extract.py 26 2007-01-07 16:50:51Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/trunk/I18NToolBox/commands/extract.py $
# $LastChangedDate: 2007-01-07 16:50:51 +0000 (Sun, 07 Jan 2007) $
# $Rev: 26 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import os
import imp
import optparse
import subprocess

from I18NToolBox.lib import genshi_gettext
from I18NToolBox.lib.catalog import CatalogParser
from I18NToolBox.commands import check_formencode_support

DEFAULT_KEYWORDS = [
    'gettext', 'gettext:1,2', 'ungettext:1,2', 'ugettext', 'dgettext:2',
    'dngettext:2,3', '_', 'N_', 'ngettext_noop'
]

XGETTEXT_DEFAULTS = [
    '-L', 'Python'
]

class ExtractionTool:
    """Extraction command, scan source files to gather translatable strings in
    a .pot file"""

    desc = "Scan source files to gather translatable strings in a .pot file"
    name = "extract"
    package = None
    defaults = None
    __version__     = "0.1"
    __author__      = "Pedro ALgarvio"
    __email__       = "ufs@ufsoft.org"
    __copyright__   = "Copyright 2006 Pedro Algarvio"
    __license__     = "BSD"

    def __init__(self, version):
        parser = optparse.OptionParser(
            usage="%prog " + self.name + " [options]", version="%prog " + self.__version__
        )
        parser.description = self.desc
        parser.add_option(
            '-d', '--default-domain',
            dest = 'name',
            default = self.defaults['potfile'],
            help = "use NAME.pot for output. Project specific default: %default"
        )
        parser.add_option(
            '-o', '--output',
            dest = 'file',
            default = self.defaults['potfile_path'],
            help = "write output to specified file. Project specific default: %default"
        )
        parser.add_option(
            '-p', '--output-dir',
            dest = 'dir',
            default = self.defaults['i18n_path'],
            help = "output files will be placed in directory DIR Default: %default"
        )
        parser.add_option(
            '-j', '--join-existing',
            dest = 'join_existing',
            action = 'store_true',
            default = False,
            help = "join messages with existing file. Default: %default"
        )
        parser.add_option(
            '-x', '--exclude-file',
            dest = 'excludes',
            metavar = 'FILE.po',
            help = "entries from FILE.po are not extracted"
        )
        parser.add_option(
            '--keyword',
            dest = 'keywords',
            default = DEFAULT_KEYWORDS,
            metavar = 'WORD',
            help = "additional keyword to be looked for. Default: %default"
        )
        parser.add_option(
            '-E', '--escape',
            dest = 'escape',
            action = 'store_true',
            default = False,
            help = "use C escapes in output, no extended chars. Default: %default"
        )
        parser.add_option(
            '--strict',
            dest = 'strict',
            action = 'store_true',
            default = False,
            help = "Write out a strict Uniforum conforming PO file.  Note that "
            "this Uniforum format should be avoided because it doesn't support "
            "the GNU extensions. Default: %default"
        )
        parser.add_option(
            '-w', '--width',
            dest = 'width',
            metavar = 'NUMBER',
            help = "set output page width."
        )
        parser.add_option(
            '--no-wrap',
            dest = 'no_wrap',
            default = False,
            help = "do not break long message lines, longer than the output "
            "page width, into several lines. Default: %default"
        )
        parser.add_option(
            '-s', '--sort-output',
            action = 'store_true',
            dest = 'sort_output',
            default = False,
            help = "Generate sorted output.  Note that using this option makes "
            "it much harder for the translator to understand each message's "
            "context Default: %default."
        )
        parser.add_option(
            '-F', '--sort-by-file',
            action = 'store_true',
            dest = 'sort_by_file',
            default = False,
            help = 'Sort output by file location.'
        )
        parser.add_option(
            '--copyright-holder',
            dest = 'copyright_holder',
            metavar = 'STRING',
            help = "set copyright holder in output"
        )
        parser.add_option(
            '--foreign-user',
            dest = 'foreign_user',
            default = False,
            action = 'store_true',
            help = "omit FSF copyright in output for foreign user. "
            "Default: %default"
        )
        parser.add_option(
            '--msgid-bugs-address',
            dest = 'msgid_bugs_address',
            metavar = 'EMAIL@ADDRESS',
            help = "set report address for msgid bugs"
        )
        parser.add_option(
            '-m', '--msgstr-prefix',
            dest = "msgstr_prefix",
            metavar = 'STRING',
            help = 'Use STRING (or "" if not specified) as prefix for msgstr entries.'
        )
        parser.add_option(
            '-M', '--msgstr-suffix',
            dest = "msgstr_suffix",
            metavar = "STRING",
            help = 'Use STRING (or "" if not specified) as suffix for msgstr entries.'
        )
        parser.add_option(
            '--debug',
            dest = 'debug',
            action = 'store_true',
            default = False,
            help = "more detailed formatstring recognition result. Default: %default"
        )
        parser.add_option(
            '--formencode-support',
            dest = 'formencode_support',
            action = 'store_true',
            default = False,
            help = "Translatable strings from FormEncode will be included in "
            "your pot file"
        )
        parser.add_option(
            '-g', '--genshi-support',
            dest = 'genshi_support',
            action = 'store_true',
            default = False,
            help = "Enable parsing on Genshi templates. Default: %default"
        )
        parser.add_option(
            '--templates-dir-name',
            dest = 'genshi_tpl_dir_name',
            metavar = 'DIR_NAME',
            default = 'templates',
            help = "Genshi templates dir name. Default: %default"
        )
        self.parser = parser


    def parse_args(self):
        """Parse the args of the parser and set the parser defaults with
        whatever the user has set on the project's `setup.cfg`, as long as
        they're prepended with the this tool's `name`."""
        parser_defaults = {}
        if self.defaults.has_key('config'):
            for name, value in self.defaults['config']:
                if name.startswith('extract-'):
                    opt = '--' + name.replace('extract-', '')
                    name = name.replace('extract-', '').replace('-', '_')
                    if self.parser.has_option(opt):
                        parser_defaults[name] = value
        if parser_defaults != {}:
            self.parser.set_defaults(**parser_defaults)
        return self.parser.parse_args()

    def scan_source_files(self, srcdir, tpl_dir_name="templates"):
        """Scan the source files for the provided `srcdir`."""
        exclude_dirs = ('.appledouble', '.svn', 'cvs', '_darcs', 'i18ntoolbox')
        source_files = []
        genshi_files = []
        for root, dirs, files in os.walk(srcdir):
            if os.path.basename(root).lower() in exclude_dirs:
                continue
            for fname in files:
                name, ext = os.path.splitext(fname)
                del(name)
                srcfile = os.path.join(root, fname)
                _py_ext = [triple[0] for triple in imp.get_suffixes()
                           if triple[2] == imp.PY_SOURCE][0]
                if ext == _py_ext:
                    # Python Source Files
                    source_files.append(srcfile)
                elif ext == '.html':
                    # Genshi Templates
                    genshi_files.append(srcfile)
                else:
                    # Everything Else, Do Nothing
                    pass
        # Only include .html if found on a templates dir/subdir
        genshi_files = [
            fname for fname in genshi_files if fname.find(tpl_dir_name) != -1
        ]
        return source_files, genshi_files

    def run(self):
        """Run the tool."""
        xgettext_opts = []
        (options, args) = self.parse_args()
        del(args)
        if options.name:
            xgettext_opts.append('--default-domain=%s' % options.name)
        if options.file:
            xgettext_opts.append('--output=%s' % options.name)
        if options.dir:
            xgettext_opts.append('--output-dir=%s' % options.dir)
        if options.excludes:
            xgettext_opts.append('--exclude-file=%s' % options.excludes)
        if options.join_existing:
            xgettext_opts.append('--join-existing')
        if options.keywords:
            for keyword in options.keywords:
                if keyword not in DEFAULT_KEYWORDS:
                    DEFAULT_KEYWORDS.append(keyword)
        if options.width:
            xgettext_opts.append('--width=%s' % options.width)
        if options.no_wrap:
            if options.width:
                xgettext_opts.pop(xgettext_opts.index('--width=%s' % options.width))
            xgettext_opts.append('--no-wrap')
        if options.sort_output and options.sort_by_file:
            self.parser.error('--sort-output/-s and --sort-by-file/-F are mutually exclusive')
        if options.sort_output:
            xgettext_opts.append('--sort-output')
        if options.sort_by_file:
            xgettext_opts.append('--sort-by-file')
        if options.copyright_holder:
            xgettext_opts.append('--copyright-holder=%s' % options.copyright_holder)
        if options.foreign_user:
            xgettext_opts.append('--foreign-user')
        if options.msgid_bugs_address:
            xgettext_opts.append('--msgid-bugs-address=%s' % options.msgid_bugs_address)
        if options.msgstr_prefix:
            xgettext_opts.append('--msgstr-suffix=%s' % options.msgstr_prefix)
        if options.msgstr_suffix:
            xgettext_opts.append('--msgstr-suffix=%s' % options.msgstr_suffix)
        if options.debug:
            xgettext_opts.append('--debug')
        if options.formencode_support:
            if check_formencode_support(self.parser):
                import formencode
        if options.genshi_support:
            if '--join-existing' not in XGETTEXT_DEFAULTS:
                XGETTEXT_DEFAULTS.append('--join-existing')
            if options.debug:
                print "Genshi Support enabled. Forcing '--join-existing' with xgettext"

        if options.formencode_support:
            if '--join-existing' not in XGETTEXT_DEFAULTS:
                XGETTEXT_DEFAULTS.append('--join-existing')
            if options.debug:
                print "FormEncode Support enabled. Forcing '--join-existing' with xgettext"

        keywords = []
        for keyword in DEFAULT_KEYWORDS:
            keywords.append('--keyword=%s' % keyword)

        xgettext_opts.extend(keywords)
        xgettext_opts.extend(XGETTEXT_DEFAULTS)

        source_files, genshi_files = self.scan_source_files(
            self.defaults['path'], tpl_dir_name=options.genshi_tpl_dir_name)

        if os.path.exists(self.defaults['potfile_path']):
            backup_pot = self.defaults['potfile'].replace('.pot', '.pot.bak')
            backup_path = os.path.join(self.defaults['i18n_path'], backup_pot)
            if os.path.exists(self.defaults['potfile_path']):
                backup_pot = self.defaults['potfile'].replace('.pot', '.pot.bak')
                backup_path = os.path.join(self.defaults['i18n_path'], backup_pot)
                if options.debug:
                    print "Backing up %r to %r" % \
                            (self.defaults['potfile_path'], backup_path)
                try:
                    os.unlink(backup_path)
                except OSError:
                    pass
                try:
                    os.rename(self.defaults['potfile_path'], backup_path)
                    file(self.defaults['potfile_path'], 'wb').write('')
                except OSError, error:
                    print error

        if options.genshi_support:
            genshi_gettext.build_gettext_functions(DEFAULT_KEYWORDS)
            genshi_gettext.write_pot_file(options.file, genshi_files, options.debug)

        if options.formencode_support:
            fe_pot_path = os.path.join(formencode.api.get_localedir(), 'FormEncode.pot')
            parser = CatalogParser(fe_pot_path, options.debug)
            parser.parse_messages()
            final = file(options.file, 'rb').read()
            for entry in parser.get_messages():
                entry.add_comment('From FormEncode.pot')
                final += str(entry)
            file(options.file, 'wb').write(final)

        subprocess.call(['xgettext'] + xgettext_opts + source_files)

        # Set some info on the pot file
        data = file(self.defaults['potfile_path'], 'rb').read()
        data = data.replace(
            'SOME DESCRIPTIVE TITLE.',
            'Translation Template for the %s package' % self.defaults['name'],
            1
        ).replace('PACKAGE', self.defaults['name'], 1)
        file(self.defaults['potfile_path'], 'wb').write(data)

