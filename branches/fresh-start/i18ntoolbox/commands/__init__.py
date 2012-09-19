# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: __init__.py 76 2007-04-16 18:56:35Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/branches/fresh-start/i18ntoolbox/commands/__init__.py $
# $LastChangedDate: 2007-04-16 19:56:35 +0100 (Mon, 16 Apr 2007) $
# $Rev: 76 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import os
import sys
import pkg_resources
from optparse import OptionParser

from i18ntoolbox import __version__ as i18ntoolbox_version
from i18ntoolbox.utils import AttrsDict, get_bool_opt, get_int_opt, get_list_opt


BOOLEAN_OPTIONS = (
    'destructive', 'no-escape', 'escape', 'indent', 'no-location',
    'add-location', 'strict', 'no-wrap', 'sort-output', 'sort-by-file',
    'join-existing', 'debug', 'foreign-user'
)
LIST_OPTIONS = ('keywords', 'templates-extensions')
INT_OPTIONS = ('width')


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
            default = self.defaults.project.potfile,
            metavar = 'FILE',
            help = "write output to specified file."
        )
        output_file_location.add_option(
            '-D', '--directory',
            dest = 'directory',
            default = self.defaults.project.basedir,
            metavar = 'DIR',
            help = "add DIR to list for input files search"
        )
        self.parser = parser


    def parse_args(self):
        """Parse the arguments and options and set the parser defaults with
        whatever the user has set on the project's `setup.cfg`."""
        parser_defaults = {}
        if self.defaults.has_key('cfgfile'):
            for name, value in self.defaults.cfgfile.iteritems():
                opt = '--%s' % name
                for special_case in ('keywords', 'templates-extensions'):
                    # Special plural to singular opt name case
                    if name == special_case:
                        opt = '--%s' % special_case[:-1]
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
        if options.directory:
            self.defaults.gettext_opts.append(
                '--directory=%s' % options.directory
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
            usage = "%prog [options] <command> [command options]",
            version = "%prog " + i18ntoolbox_version
        )
        parser.description = "I18NToolBox is intented to provide some " + \
                "centralized helper function for gettext translatable " + \
                "strings extraction and compilation."
        parser.allow_interspersed_args = False
        parser.add_option(
            '-b', '--base',
            dest='basedir',
            default='.',
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
        defaults.computed = AttrsDict()
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

    def parse_config_section(self, options):
        cfgfile = self.defaults.cfgfile
        for option, value in options.iteritems():
            if option in LIST_OPTIONS:
                value = get_list_opt(options, option, None)
                cfgfile[option] = value
            elif option in INT_OPTIONS:
                value = get_int_opt(options, option, None)
                cfgfile[option] = value
            elif option in BOOLEAN_OPTIONS or option.endswith('-support'):
                value = get_bool_opt(options, option, None)
                cfgfile[option] = value
            else:
                cfgfile[option] = value

    def get_package_info(self):
        project = self.defaults.project
        # Grab all possible distributions on current path
        dists = list(pkg_resources.find_distributions(project.basedir, only=True))
        if not dists:
            # There we no distributions found, try to find a setup.py
            # and run `egg_info` on it
            print 'Could not find any `.egg-info` directory.'
            print 'Trying to find a setuptools project and build it.'
            import subprocess
            dirlist = os.listdir(project.basedir)
            if 'setup.py' in dirlist:
                print 'Looking in %r' % os.path.abspath(project.basedir)
                subprocess.call(['python', 'setup.py', 'egg_info'])
                self.get_package_info()
            else:
                for item in dirlist:
                    if os.path.isdir(item):
                        print 'Looking in %r' % os.path.abspath(item)
                        if os.path.isfile(os.path.join(item, 'setup.py')):
                            os.chdir(item)
                            subprocess.call(['python', 'setup.py', 'egg_info'])
                            os.chdir(project.basedir)
                            self.get_package_info()
        for dist in dists:
            project.name = dist.project_name
            project.version = dist.version
            if dist.location == project.basedir:
                project.basedir = ''
            else:
                project.basedir = dist.location

            if not project.has_key('path'):
                if dist._provider.__dict__.has_key('egg_info'):
                    egg_info_path = dist._provider.__dict__['egg_info']
                project.path = os.path.join(
                    project.basedir,
                    file(os.path.join(
                        dist._provider.__dict__['egg_info'],
                        'top_level.txt'
                    )).readline().strip()
                )
                if not os.path.isdir(project.path):
                    print "Can't setup the package path %r" % project.path
                    print "Pass `-i` or `--help` for more help"
                    sys.exit(1)

            if not project.has_key('i18n_path'):
                i18n_path = os.path.join(project.path, 'i18n')
                if os.path.isdir(i18n_path):
                    project.i18n_path = i18n_path
                else:
                    print "Can't setup i18n path %r" % i18n_path
                    print "Pass `-i` or `--help` for more help"
                    sys.exit(1)

            if dist.has_resource('setup.cfg'):
                from ConfigParser import SafeConfigParser
                cfg_stream = dist.get_resource_stream(dist, 'setup.cfg')
                cfg_parser = SafeConfigParser()
                cfg_parser.readfp(cfg_stream)
                if cfg_parser.has_section('i18ntoolbox'):
                    self.parse_config_section(
                        dict(cfg_parser.items('i18ntoolbox'))
                    )
            # There should be only one
            break

    def run(self):
        (options, args) = self.parser.parse_args(sys.argv[1:])
        defaults = self.defaults.project
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
        if options.package_dir:
            self.defaults.project.path = options.package_dir
        if options.i18n_path:
            self.defaults.project.i18n_path = options.i18n_path
        self.get_package_info()

        if not self.defaults.project.has_key('name'):
            self.parser.error(
                "Could not find a setup tools distribution on %r" % \
                os.path.abspath(options.basedir)
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
