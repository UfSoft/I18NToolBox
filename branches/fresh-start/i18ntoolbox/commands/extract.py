# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: extract.py 76 2007-04-16 18:56:35Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/branches/fresh-start/i18ntoolbox/commands/extract.py $
# $LastChangedDate: 2007-04-16 19:56:35 +0100 (Mon, 16 Apr 2007) $
# $Rev: 76 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import os
import imp
import codecs
import subprocess

import pytz
import pkg_resources

from datetime import datetime

from i18ntoolbox.commands import CommonOptsGettextTool
from i18ntoolbox.utils import AttrsDict, silent_backup, check_python_format, \
                              normalize, print_developer_info


DEFAULT_KEYWORDS = (
    'gettext', 'gettext:1,2', 'ungettext:1,2', 'ugettext', 'dgettext:2',
    'dngettext:2,3', '_', 'N_', 'ngettext_noop'
)

XGETTEXT_DEFAULTS = [
    'xgettext', '-L', 'Python', '--omit-header'
]


class ExtractionTool(CommonOptsGettextTool):
    """Extraction command, scan source files to gather translatable strings in
    a .pot file"""

    desc = "Scan source files to gather translatable strings in a .pot file"
    name = "extract"
    gettext_funcs = {}

    def __init__(self):
        CommonOptsGettextTool.__init__(self)
        # Output file location options
        output_file_location = self.parser.output_file_location
        output_file_location.add_option(
            '-d', '--default-domain',
            dest = 'default_domain',
            default = self.defaults.project.name.lower(),
            help = "use NAME.pot for output. "
            "(Project specific default: %default)"
        )
        output_file_location.add_option(
            '-p', '--output-dir',
            dest = 'output_dir',
            default = self.defaults.project.i18n_path,
            help = "output files will be placed in directory DIR. "
            "(Project specific default: %default)"
        )
        # Operation mode options
        operation_mode = self.parser.add_option_group("Operation Mode")
        operation_mode.add_option(
            '-j', '--join-existing',
            dest = 'join_existing',
            action = 'store_true',
            default = False,
            help = "join messages with existing file. (Default: %default)"
        )
        operation_mode.add_option(
            '-x', '--exclude-file',
            dest = 'exclude_file',
            metavar = 'FILE.po',
            help = "entries from FILE.po are not extracted"
        )
        operation_mode.add_option(
            '-c', '--add-comments',
            dest = 'add_comments',
            metavar = 'TAG',
            help = "place comment block with TAG (or those preceding keyword "
            "lines) in output file"
        )
        # Language specific options
        language_options = self.parser.add_option_group(
            "Language specific options"
        )
        language_options.add_option(
            '-k', '--keyword',
            dest = 'keywords',
            action = 'append',
            #default = list(DEFAULT_KEYWORDS),
            metavar = 'WORD',
            help = "additional keyword to be looked for. "
            "(Default: %s)" % ', '.join([repr(kw) for kw in DEFAULT_KEYWORDS])
        )
        language_options.add_option(
            '--debug',
            dest = 'debug',
            action = 'store_true',
            default = False,
            help = "more detailed format string recognition result. "
            "(Default: %default)"
        )
        # Extend output details
        output_details = self.parser.output_details
        output_details.add_option(
            '--copyright-holder',
            dest = 'copyright_holder',
            metavar = 'STRING',
            help = "set copyright holder in output"
        )
        output_details.add_option(
            '--foreign-user',
            dest = 'foreign_user',
            default = False,
            action = 'store_true',
            help = "omit FSF copyright in output for foreign user. "
            "Default: %default"
        )
        output_details.add_option(
            '--msgid-bugs-address',
            dest = 'msgid_bugs_address',
            metavar = 'EMAIL@ADDRESS',
            help = "set report address for msgid bugs"
        )
        output_details.add_option(
            '-m', '--msgstr-prefix',
            dest = "msgstr_prefix",
            metavar = 'STRING',
            help = 'Use STRING (or "" if not specified) as prefix for msgstr entries.'
        )
        output_details.add_option(
            '-M', '--msgstr-suffix',
            dest = "msgstr_suffix",
            metavar = "STRING",
            help = 'Use STRING (or "" if not specified) as suffix for msgstr entries.'
        )
        # Load any templating engines using our entry point
        templating_engines = {}
        self.defaults.engines = AttrsDict()
        for entrypoint in pkg_resources.iter_entry_points(
            "I18NToolBox.templating.extract"):
            engine = entrypoint.load()
            templating_engines[engine.name] = engine()
            self.defaults.engines[engine.name] = AttrsDict()
            self.defaults.engines[engine.name].extensions = engine.exts

        self.templating_engines = templating_engines
        engines_options = self.parser.add_option_group(
            "Templating Engines Options",
            "Templating engines that compile the templates " + \
            "to python code are naturally supported by 'xgettext'. " + \
            "Current supported templating engines: %s.\n" % \
            ', '.join(templating_engines.keys())
        )
        # Some default options for templating engines
        engines_options.add_option(
            '--templates-dir-name',
            dest = 'templates_dir_name',
            metavar = 'DIR_NAME',
            default = 'templates',
            help = "Templates dir name. (Default: %default)"
        )
        engines_options.add_option(
            '--templates-extension',
            dest = 'templates_extensions',
            metavar = '.EXT',
            action = 'append',
            help = "The file extension of the template files. "
            "(Default: %s)" % '; '.join(
                [eng +': ' + ', '.join(
                    [repr(ext) for ext in self.defaults.engines[eng].extensions]
                ) for eng in self.defaults.engines.keys()]
            )
        )

        # Setup any options the templating engine want to add to our parser
        self.setup_templating_engines_options()

    def setup_templating_engines_options(self):
        engines_options = self.parser.templating_engines_options
        for engine in self.templating_engines.keys():
            engines_options.add_option(
                '--%s-support' % engine.lower(),
                action = 'store_true',
                default = False,
                help = "Enable %s templating engine support" % engine
            )
            self.templating_engines[engine].setup_parser(engines_options)


    def scan_files(self, srcdir, templates_dir_name, extensions):
        """Scan the source files for the provided `srcdir`."""
        exclude_dirs = ('.appledouble', '.svn', 'cvs', '_darcs', 'i18ntoolbox')
        source_files = []
        templates = []
        for root, dirs, files in os.walk(srcdir):
            if root.startswith('./'):
                root = root[2:]
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
                elif ext in extensions:
                    # Templates
                    templates.append(srcfile)
                else:
                    # Everything Else, Do Nothing
                    pass
        # Only include templates if path contains `tpl_dir_name`
        templates = [
            fname for fname in templates if fname.find(templates_dir_name) != -1
        ]
        # Compute size of "/path/to/project_basedir" + "/" to make relative
        # paths apear in the pot instead of absolute paths.
        # The templates path's are kept absolute because some engines(Genshi
        # for example) requires the absolute path to be able to load the template.
        lstriplen = len(os.path.dirname(self.defaults.project.path))+1
        return [fpath[lstriplen:] for fpath in source_files], templates


    def build_pot_header(self):
        pot_header = r"""# Translation Template for the %(package)s %(version)s package.
# Copyright (C) %(year)s, %(package)s copyright holder.
# This file is distributed under the same license as the
# %(package)s %(version)s package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: %(package)s %(version)s\n"
"Report-Msgid-Bugs-To: %(msgid_bugs)s\n"
"POT-Creation-Date: %(creation_date)s\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"

"""
        now = datetime.now(pytz.utc)
        header = AttrsDict()
        header.package = self.defaults.project.name
        header.version = self.defaults.project.version
        header.year = now.strftime('%Y')
        header.creation_date = now.strftime('%Y-%m-%d %H:%M:%S %Z%z')
        if self.defaults.parsed_opts.has_key('msgid_bugs_address'):
            header.msgid_bugs = self.defaults.parsed_opts.msgid_bugs_address
        else:
            header.msgid_bugs = 'EMAIL@ADDRESS'

        # pot_header is passed the header dict twice to be able to parse stuff
        # from the setup.cfg file, like for example:
        # msgid-bugs-address = \
        #   http://ccp.ufsoft.org/newticket?component=translations&version=%%(version)s
        return pot_header % header % header

    def build_gettext_functions(self, func_list):
        """Build the gettext function to parse.
        Credits to Matt Good."""
        print func_list
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
        print self.gettext_funcs

    def write_template_msgs(self, engine):
        fd = codecs.open(self.defaults.project.potfile_path, 'a', 'utf-8')
        try:
            keys_found = {}
            key_order = []
            # Compute size of "/path/to/project_basedir" + "/" to make relative
            # paths apear in the pot instead of absolute paths
            lstriplen = len(os.path.dirname(self.defaults.project.path))+1
            for fname, linenum, key in engine.extract_keys():
                print 'KEY', key
                if fname.startswith(self.defaults.project.path):
                    # make it a relative path(to project home dir)
                    fname = fname[lstriplen:]
                str_indexes = self.gettext_funcs[key[0]]
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
                    if check_python_format(singular) or \
                       check_python_format(plural):
                        fd.write('#, ')
                        if self.defaults.parsed_opts.debug:
                            fd.write('possible-')
                        fd.write('python-format\n')
                    fd.write('msgid %s\n' % normalize(singular))
                    fd.write('msgid_plural %s\n' % normalize(plural))
                    fd.write('msgstr[0] ""\n')
                    fd.write('msgstr[1] ""\n\n')
                    continue

            for key in key_order:
                for fname, linenum in keys_found[key]:
                    for fname, linenum in keys_found[key]:
                        fd.write('#: %s:%s\n' % (fname, linenum))
                    if check_python_format(key):
                        fd.write('#, ')
                        if self.defaults.parsed_opts.debug:
                            fd.write('possible-')
                        fd.write('python-format\n')
                    fd.write('msgid %s\n' % normalize(key))
                    fd.write('msgstr ""\n\n')
        finally:
            fd.close()


    def run(self):
        """Run the tool."""
        (options, args) = CommonOptsGettextTool.run(self)
        xgettext_opts = self.defaults.gettext_opts
        # --[ Output File Location Options Group ]-----------------------------
        # ----[ Defined on BaseGettextTool ]-----------------------------------
        if options.output_file:
            # xgettext is the only one with a different way to set the option
            # let's replace it with the correct way for it
            opt = '--output-file=%s' % options.output_file
            if opt in xgettext_opts:
                index = xgettext_opts.index(opt)
                xgettext_opts.pop(index)
            xgettext_opts.append('--output=%s' % options.output_file)
        # ----[ Extended by the tool ]-----------------------------------------
        if options.default_domain:
            xgettext_opts.append('--default-domain=%s' % options.default_domain)
        if options.output_dir:
            xgettext_opts.append('--output-dir=%s' % options.output_dir)
        # --[ Output Details Options Group - Extended by the tool ]------------
        if options.copyright_holder:
            xgettext_opts.append(
                '--copyright-holder=%s' % options.copyright_holder
            )
        if options.foreign_user:
            xgettext_opts.append('--foreign-user')
        if options.msgid_bugs_address:
            xgettext_opts.append(
                '--msgid-bugs-address=%s' % options.msgid_bugs_address
            )
        if options.msgstr_prefix:
            xgettext_opts.append('--msgstr-prefix=%s' % options.msgstr_prefix)
        if options.msgstr_suffix:
            xgettext_opts.append('--msgstr-suffix=%s' % options.msgstr_suffix)
        # --[ Operation Mode Options Group ]-----------------------------------
        if options.join_existing:
            xgettext_opts.append('--join-existing')
        if options.exclude_file:
            xgettext_opts.append('--exclude-file=%s' % options.exclude_file)
        if options.add_comments:
            xgettext_opts.append('--add-comments=%s' % options.add_comments)
        # --[ Language Specific Options Group ]--------------------------------
        kwds = list(DEFAULT_KEYWORDS)
        if options.keywords:
            for kw in options.keywords:
                if kw not in kwds:
                    kwds.append(kw)
        options.keywords = kwds
        for keyword in options.keywords:
            xgettext_opts.append('--keyword=%s' % keyword)
        if options.debug:
            xgettext_opts.append('--debug')

        # --[ Templating Engines Options ]-------------------------------------
        if not options.templates_extensions:
            extensions = []
            for eng in self.defaults.engines:
                for ext in self.defaults.engines[eng].extensions:
                    extensions.append(ext)
            options.templates_extensions = extensions

        # Call self.build_parser_opts with the options from the parser so we
        # can also pass them to the templating engines.
        # This is of course called after we do the options checking because
        # we might change some of the options after they're passed to our parser
        self.build_parser_opts(options)

        # Let's get a list of files to use
        source_files, template_files = self.scan_files(
            srcdir = self.defaults.project.path,
            templates_dir_name = options.templates_dir_name,
            extensions = options.templates_extensions
        )

        computed_opts = self.defaults.computed
        computed_opts.source_files = source_files
        computed_opts.template_files = template_files
        computed_opts.templates_path = options.templates_dir_name

        #self.build_gettext_functions(self.defaults.parsed_opts.keywords)
        self.build_gettext_functions(options.keywords)
        computed_opts.gettext_funcs = self.gettext_funcs

        # Backup existing .pot file
        if options.debug:
            print 'Backup %r if present.' % self.defaults.project.potfile_path
        silent_backup(self.defaults.project.potfile_path)

        # Write Header
        potfile = file(self.defaults.project.potfile_path, 'r').read()
        potfile = self.build_pot_header() + potfile
<<<<<<< .mine
        print potfile
        codecs.open(self.defaults.project.potfile_path, 'w', 'utf-8').write(potfile)
=======
        codecs.open(
            self.defaults.project.potfile_path, 'w', 'utf-8'
        ).write(potfile)
>>>>>>> .r76


        # Take care of templating engines string extraction
        for engine in self.templating_engines.values():
            # Populate engine with our defaults
            engine.setup(self.defaults)
            self.write_template_msgs(engine)

        # Take care of xgettext extraction
        retcode = subprocess.call(
            XGETTEXT_DEFAULTS + self.defaults.gettext_opts + source_files
        )

        if retcode:
            import sys
            sys.exit('xgettext call returned an error, %r' % retcode)

        print_developer_info(self.defaults)
        pass



