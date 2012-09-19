# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: __init__.py 43 2007-01-21 08:24:29Z pjenvey $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/branches/bitten/i18ntoolbox/commands/__init__.py $
# $LastChangedDate: 2007-01-21 08:24:29 +0000 (Sun, 21 Jan 2007) $
# $Rev: 43 $
# $LastChangedBy: pjenvey $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import os
import sys
from optparse import OptionParser
import pkg_resources

from i18ntoolbox import __version__ as i18ntoolbox_version
from i18ntoolbox.utils import AttrsDict


#GETTEXT_POSSIBLE_OPTIONS = (
#    '--default-domain', '--output', '--output-file', '--output-dir',
#    '--join-existing', '--exclude-file' ..... 
# XXX TO BE THOUGHT IF IT SHOULD BE DONE THIS WAY



class CustomOptionParser(OptionParser):
    """A custom optparse.OptionParser whose option groups can be accessed
    by attribute."""
    optiongroups = {}
    def __init__(self, *args, **kwargs):
        OptionParser.__init__(self, *args, **kwargs)

    def __getattr__(self, attr):
        if not self.optiongroups.has_key(attr):
            raise ValueError, "No Option Group by that name: %r" % attr
        return self.optiongroups[attr]

    def add_option_group(self, name, description=None):
        shortname = name.replace(' ', '_').replace('-', '_').lower()
        self.optiongroups[shortname] = \
                OptionParser.add_option_group(self, name, description)
        return self.optiongroups[shortname]

    def get_option_group(self, short_name):
        return self.optiongroups[short_name]


class BaseGettextTool(object):
    """Simple gettext command base class, with common output file location
    options."""
    __version__     = "0.1"
    __author__      = "Pedro Algarvio"
    __email__       = "ufs@ufsoft.org"
    __copyright__   = "Copyright 2006 Pedro Algarvio"
    __license__     = "BSD"

    defaults = None
    desc = name = "If you're reading this, it means the command did not " + \
                  "override all the necessary stuff"

    def __init__(self):
        parser = CustomOptionParser(
            usage="%prog " + self.name + " [options]",
            version="%prog " + self.__version__
        )
        parser.description = self.desc
        output_file_location = parser.add_option_group('Output File Location')
        output_file_location.add_option(
            '--destructive',
            dest = 'destructive',
            action = 'store_true',
            default = False,
            help = "Force destructive actions. This enables existing files "
            "to be overridden. (Default: %default)"
        )
        output_file_location.add_option(
            '-o', '--output-file',
            dest = 'output_file',
            metavar = 'FILE',
            help = "write output to specified file."
        )
        self.parser = parser


    def parse_args(self):
        """Parse the arguments and options and set the parser defaults with
        whatever the user has set on the project's `setup.cfg`."""
        parser_defaults = {}
        if self.defaults.has_key('cfgfile'):
            for name, value in self.defaults.cfgfile.items():
                opt = '--%s' % name
                name = name.replace('-', '_')
                if self.parser.has_option(opt):
                    parser_defaults[name] = value
        if parser_defaults:
            self.parser.set_defaults(**parser_defaults)
        return self.parser.parse_args()

    def build_parser_opts(self, options):
        for opt in options.__dict__:
            self.defaults.parsed_opts[opt] = getattr(options, opt)

    def run(self):
        (options, args) = self.parse_args()
        # --[ Output File Location Options Group ]-----------------------------
        if options.output_file:
            self.defaults.gettext_opts.append(
                '--output-file=%s' % options.output_file
            )
        # Return parsed args to inheriting optparsers
        return (options, args)


class CommonOptsGettextTool(BaseGettextTool):
    """Gettext command class with common options."""
    def __init__(self):
        BaseGettextTool.__init__(self)
        output_details = self.parser.add_option_group('Output details')
        output_details.add_option(
            '-e', '--no-escape',
            dest = 'no_escape',
            action = 'store_false',
            default = True,
            help = "do not use C escapes in output. (Default: %default)"
        )
        output_details.add_option(
            '-E', '--escape',
            dest = 'escape',
            action = 'store_true',
            default = False,
            help = "use C escapes in output, no extended chars. "
            "(Default: %default)"
        )
        output_details.add_option(
            '-i', '--indent',
            dest = 'indent',
            action = 'store_true',
            default = False,
            help = "write the .po file using indented style. (Default: %default)"
        )
        output_details.add_option(
            '--no-location',
            dest = 'no_location',
            action = 'store_true',
            default = False,
            help = "do not write '#: filename:line' lines. (Default: %default)"
        )
        output_details.add_option(
            '-n', '--add-location',
            dest = 'add_location',
            action = 'store_false',
            default = True,
            help = "generate '#: filename:line' lines. (Default: %default)"
        )
        output_details.add_option(
            '--strict',
            dest = 'strict',
            action = 'store_true',
            default = False,
            help = "Write out a strict Uniforum conforming PO file.  Note that "
            "this Uniforum format should be avoided because it doesn't support "
            "the GNU extensions. (Default: %default)"
        )
        output_details.add_option(
            '-w', '--width',
            dest = 'width',
            type = 'int',
            metavar = 'NUMBER',
            help = "set output page width."
        )
        output_details.add_option(
            '--no-wrap',
            dest = 'no_wrap',
            action = 'store_true',
            default = False,
            help = "do not break long message lines, longer than the output "
            "page width, into several lines. (Default: %default)"
        )
        output_details.add_option(
            '-s', '--sort-output',
            dest = 'sort_output',
            action = 'store_true',
            default = False,
            help = "generate sorted output. (Default: %default)"
        )
        output_details.add_option(
            '-F', '--sort-by-file',
            dest = 'sort_by_file',
            action = 'store_true',
            default = False,
            help = "sort output by file location. (Default: %default)"
        )

    def parse_args(self):
        return BaseGettextTool.parse_args(self)

    def run(self):
        (options, args) = BaseGettextTool.run(self)
        if options.escape and not options.no_escape:
            self.parser.error(
                "'--escape' and '--no-escape' are mutually exclusive."
            )
        elif options.escape and options.no_escape:
            options.no_escape = False
        if not options.add_location and options.no_location:
            self.parser.error(
                "'--add-location' and '--no-location' are mutually exclusive."
            )
        elif options.no_location and options.add_location:
            options.add_location = False
        if options.no_wrap and options.width:
            self.parser.error(
                "'--no-wrap' and '--width' are mutually exclusive."
            )
        if options.sort_output and options.sort_by_file:
            self.parser.error(
                "'--sort-output' and '--sort-by-file' are mutually exclusive."
            )
        if options.width and options.no_wrap:
            self.parser.error(
                "'--width' and '--no-wrap' are mutually exclusive"
            )

        # Let's update our gettext options
        gettext_opts = self.defaults.gettext_opts
        # --[ Output Details Options Group ] ----------------------------------
        # XXX TO BE THOUGHT IF IT SHOULD BE DONE THIS WAY
        #for option in options.__dict__:
        #    option = '--%s' % option.replace('_', '-')
        #    if option in GETTEXT_POSSIBLE_OPTIONS:
        #        value = getattr(options, option)
        #        if value:
        #            if isinstance(value, bool):
        #                gettext_opts.append(option)
        #            elif isinstance(value, (list, tuple)):
        #                for item in value:
        #                    gettext_opts.append(opt + '=%s' % item)
        #            else:
        #                gettext_opts.append(opt + '=%s ' % value)
        # So, We'll just do it the hard way

        if options.no_escape:
            gettext_opts.append('--no-escape')
        if options.escape:
            gettext_opts.append('--escape')
        if options.indent:
            gettext_opts.append('--indent')
        if options.no_location:
            gettext_opts.append('--no-location')
        if options.add_location:
            gettext_opts.append('--add-location')
        if options.strict:
            gettext_opts.append('--strict')
        if options.width:
            gettext_opts.append('--width=%s' % options.width)
        if options.no_wrap:
            gettext_opts.append('--no-wrap')
        if options.sort_output:
            gettext_opts.append('--sort-output')
        if options.sort_by_file:
            gettext_opts.append('--sort-by-file')

        # Return parsed args to inheriting optparsers
        return (options, args)


class CmdLineInterface:
    """I18NToolBox command line interface."""
    def __init__(self):
        parser = OptionParser(
            usage = "%prog [options] <command> [command-options]",
            version = "%prog " + i18ntoolbox_version
        )
        parser.description = "I18NToolBox is intented to provide some " + \
                "centralized helper function for gettext translatable " + \
                "strings extraction and compilation."
        parser.allow_interspersed_args = False
        parser.add_option(
            '-b', '--base',
            dest='basedir',
            default='.', #os.getcwd(),
            help = "Project Base Directory. Defaults to current directory."
        )
        parser.add_option(
            '-p', '--package-dir',
            dest="package_dir",
            help = "Package's path."
        )
        parser.add_option(
            "-i", "--i18n-path",
            dest="i18n_path",
            help = "Path to package's i18n dir."
        )

        commands = {}
        for entrypoint in pkg_resources.iter_entry_points("I18NToolBox.command"):
            command = entrypoint.load()
            commands[entrypoint.name] = (command.desc, entrypoint)
        self.commands = commands
        # Setup The Needed Default Dicts
        defaults = AttrsDict()
        defaults.project = AttrsDict()
        defaults.cfgfile = AttrsDict()
        defaults.parsed_opts = AttrsDict()
        defaults.gettext_opts = []
        self.defaults = defaults
        # Setup our custom parser help message
        parser.print_help = self._help
        self.parser = parser


    def _help(self):
        print self.parser.format_help()
        print "commands:"
        longest = max([len(key) for key in self.commands.keys()])
        format = "    %" + str(longest) + "s  %s"
        commandlist = self.commands.keys()
        commandlist.sort()
        for key in commandlist:
            print format % (key, self.commands[key][0])

    def transform_value(self, cfg_parser, section, option):
        try:
            # Booleans first
            return cfg_parser.getboolean(section, option)
        except ValueError:
            pass
        try:
            # Now ints
            return cfg_parser.getint(section, option)
        except ValueError:
            pass
        # The above failed, just get the value
        return cfg_parser.get(section, option)

    def get_package_info(self):
        project = self.defaults.project
        cfgfile = self.defaults.cfgfile
        for dist in pkg_resources.find_distributions(
            project.basedir, only=True):
            project.name = dist.project_name
            project.version = dist.version
            if dist.has_resource('setup.cfg'):
                from ConfigParser import SafeConfigParser
                cfg_stream = dist.get_resource_stream(dist, 'setup.cfg')
                cfg_parser = SafeConfigParser()
                cfg_parser.readfp(cfg_stream)
                if cfg_parser.has_section('i18ntoolbox'):
                    #self.defaults['config'] = []
                    for option in cfg_parser.options('i18ntoolbox'):
                        cfgfile[option] = self.transform_value(
                            cfg_parser, 'i18ntoolbox', option
                        )
            # There should be only one
            break

    def set_package_path(self):
        project = self.defaults.project
        package_path = os.path.join(
            project.basedir,
            project.name.lower()
        )
        if not os.path.isdir(package_path):
            print "Can't setup package path %r" % package_path
            print 'Pass `-p` or `--help` for more help'
            sys.exit()
        project.path = package_path

    def set_i18n_path(self):
        i18n_path = os.path.join(self.defaults.project.path, 'i18n')
        if not os.path.isdir(i18n_path):
            print "Can't setup i18n path %r" % i18n_path
            print "Pass `-i` or `--help` for more help"
            sys.exit(1)
        self.defaults.project.i18n_path = i18n_path

    def run(self):
        (options, args) = self.parser.parse_args(sys.argv[1:])
        defaults = self.defaults['project']
        # if no command is found display help
        if not args or not self.commands.has_key(args[0]):
            self._help()
            sys.exit(1)
        commandname = args[0]
        # strip command and any global options from the sys.argv
        sys.argv = [sys.argv[0],] + args[1:]
        command = self.commands[commandname][1]
        command = command.load()

        if options.basedir:
            self.defaults.project.basedir = options.basedir

        self.get_package_info()

        if not self.defaults.project.has_key('name'):
            self.parser.error(
                "Could not find a setup tools distribution on %r" % \
                options.basedir
            )

        if options.package_dir:
            self.defaults.project.path = options.package_dir
        elif not options.package_dir:
            self.set_package_path()

        if options.i18n_path:
            self.defaults.project.i18n_path = options.i18n_path
        elif not options.i18n_path:
            self.set_i18n_path()

        for key in ('path', 'i18n_path'):
            if not os.path.isdir(self.defaults.project[key]):
                self.parser.error(
                    "The path you passed for %r(%r) does not exist" % \
                    (key, self.defaults.project[key])
                )

        self.defaults.project.potfile = \
                self.defaults.project.name.lower() + '.pot'
        self.defaults.project.potfile_path = os.path.join(
            self.defaults.project.i18n_path,
            self.defaults.project.potfile
        )

        command.defaults = self.defaults
        command = command()
        command.run()


def main():
    parser = CmdLineInterface()
    parser.run()


__all__ = ["main"]
