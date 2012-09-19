# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: extract.py 41 2007-01-18 19:05:34Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/branches/bitten/i18ntoolbox/commands/extract.py $
# $LastChangedDate: 2007-01-18 19:05:34 +0000 (Thu, 18 Jan 2007) $
# $Rev: 41 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import os
import imp
import pkg_resources

from i18ntoolbox.commands import CommonOptsGettextTool
from i18ntoolbox.utils import AttrsDict


DEFAULT_KEYWORDS = [
    'gettext', 'gettext:1,2', 'ungettext:1,2', 'ugettext', 'dgettext:2',
    'dngettext:2,3', '_', 'N_', 'ngettext_noop'
]

XGETTEXT_DEFAULTS = [
    '-L', 'Python'
]


class ExtractionTool(CommonOptsGettextTool):
    """Extraction command, scan source files to gather translatable strings in
    a .pot file"""

    desc = "Scan source files to gather translatable strings in a .pot file"
    name = "extract"

    def __init__(self):
        CommonOptsGettextTool.__init__(self)
        # Output file location options
        output_file_location = self.parser.output_file_location
        output_file_location.add_option(
            '-d', '--default-domain',
            dest = 'default_domain',
            default = self.defaults.project.potfile,
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
            default = DEFAULT_KEYWORDS,
            metavar = 'WORD',
            help = "additional keyword to be looked for. "
            "(Default: %s)" % ', '.join([repr(kw) for kw in DEFAULT_KEYWORDS])
        )
        language_options.add_option(
            '--debug',
            dest = 'debug',
            action = 'store_true',
            default = False,
            help = "more detailed formatstring recognition result. "
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
            dest = 'templates_extension',
            metavar = '.EXT',
            help = "The file extension of the template files. "
            "(Default: %s)" % '; '.join(
                [eng +': ' + ', '.join(
                    [repr(ext) for ext in self.defaults.engines[eng].extensions]
                ) for eng in self.defaults.engines.keys()]
            )
        )

        # Setup any options the templating engine wan't to add to our parser
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


    def scan_source_files(self, srcdir, tpl_dir_name, extensions):
        """Scan the source files for the provided `srcdir`."""
        exclude_dirs = ('.appledouble', '.svn', 'cvs', '_darcs', 'i18ntoolbox')
        source_files = []
        templates = []
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
                elif ext in extensions:
                    # Templates
                    templates.append(srcfile)
                else:
                    # Everything Else, Do Nothing
                    pass
        # Only include templates if path contains `tpl_dir_name`
        templates = [
            fname for fname in templates if fname.find(tpl_dir_name) != -1
        ]
        return source_files, templates


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
            xgettext_opts.append('--msgstr-suffix=%s' % options.msgstr_prefix)
        if options.msgstr_suffix:
            xgettext_opts.append('--msgstr-suffix=%s' % options.msgstr_suffix)
        # --[ Operation Mode Options Group ]-----------------------------------
        if options.join_existing:
            xgettext_opts.append('--join-existing')
        if options.exclude_file:
            xgettext_opts.append('--exclude-file=%s' % options.exclude_file)
        if options.add_comments:
            xgettext_opts.append('--add-message=%s' % options.add_comments)
        # --[ Language Specific Options Group ]--------------------------------
        if options.keywords:
            for keyword in options.keywords:
                if keyword not in DEFAULT_KEYWORDS:
                    DEFAULT_KEYWORDS.append(keyword)
            for keyword in DEFAULT_KEYWORDS:
                xgettext_opts.append('--keyword=%s' % keyword)
        if options.debug:
            xgettext_opts.append('--debug')

        # Call self.build_parser_opts with the options from the parser so we
        # can also pass them to the templating engines.
        # This is of course called after we do the options checking because
        # we might change some of the options after they're passed to our parser
        self.build_parser_opts(options)

        pass



