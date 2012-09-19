# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: base.py 4 2006-12-26 19:24:29Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/trunk/I18NToolBox/commands/base.py $
# $LastChangedDate: 2006-12-26 19:24:29 +0000 (Tue, 26 Dec 2006) $
# $Rev: 4 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import os
import sys
import optparse
import pkg_resources

import I18NToolBox

sys.path.insert(0, os.getcwd())

__doc__ = """i18n-toolbox - Pylons I18N Toolbox
I18NToolBox is intented to provide some centralized helper fucntion for
gettext translatable strings extraction and compilation.

Usage:
    i18n-toolbox [command] [command-options]

Commands:
    extract     Extract all strings marked for translation.
                Pass `--help` to get more help about this action.

    compile     Compile pot file.
                Pass `--help` to get more help about this action.

    new         Create a new PO file.
                Pass `--help` to get more help about this action.
"""

import sys

def usage(code, msg=""):
    print >> sys.stderr, __doc__
    if msg:
        print >> sys.stderr, msg
    sys.exit(code)

def run():
    if len(sys.argv) < 2:
        usage(1, "No action specified")
    elif len(sys.argv) == 2:
        print "Action is ", sys.argv[1]
    elif len(sys.argv) > 2:
        print "Please specify only one action"


def main():
    """"Main command runner. Manages primary command line arguments."""
    commands = {}
    defaults = {}
    for entrypoint in pkg_resources.iter_entry_points("I18NToolBox.command"):
        command = entrypoint.load()
        commands[entrypoint.name] = (command.desc, entrypoint)

    def _help():
        """Custom help for i18n-toolbox"""
        print """
I18N ToolBox %s command line interface

Usage:
    %s [options] <command>

Options:
    -b DIR, --base=DIR          Project Base Directory.
                                Defaults to current directory.

    -p DIR, --package-dir=DIR   Package's path.

    -i DIR, --i18n-dir=DIR      Path to package's i18n dir.

Commands:""" % (I18NToolBox.__version__, sys.argv[0])

        longest = max([len(key) for key in commands.keys()])
        format = "    %" + str(longest) + "s  %s"
        commandlist = commands.keys()
        commandlist.sort()
        for key in commandlist:
            print format % (key, commands[key][0])

    parser = optparse.OptionParser()
    parser.allow_interspersed_args = False
    parser.add_option("-b", "--base", dest="basedir", default=os.getcwd())
    parser.add_option("-p", "--package-dir", dest="package_dir")
    parser.add_option("-i", "--i18n-dir", dest="i18n_path")
    parser.print_help = _help
    (options, args) = parser.parse_args(sys.argv[1:])

    # if no command is found display help
    if not args or not commands.has_key(args[0]):
        _help()
        sys.exit()

    def transform_value(parser, section, option):
        try:
            # Booleans first
            return parser.getboolean(section, option)
        except ValueError:
            pass
        try:
            # Now ints
            return parser.getint(section, option)
        except ValueError:
            pass
        # The above failed, just get the value
        return parser.get(section, option)

    def get_package_info():
        for project in pkg_resources.find_distributions(defaults['basedir'], only=True):
            defaults['name'] = project.project_name
            defaults['version'] = project.version
            if project.has_resource('setup.cfg'):
                from ConfigParser import SafeConfigParser
                cfg_stream = project.get_resource_stream(project, 'setup.cfg')
                cfg_parser = SafeConfigParser()
                cfg_parser.readfp(cfg_stream)
                if cfg_parser.has_section('i18ntoolbox'):
                    defaults['config'] = []
                    for option in cfg_parser.options('i18ntoolbox'):
                        defaults['config'].append((
                            option, transform_value(
                                cfg_parser, 'i18ntoolbox', option
                            )
                        ))

            # There should be only one
            break

    def set_package_path():
        package_path = os.path.join(defaults['basedir'], defaults['name'].lower())
        if not os.path.isdir(package_path):
            print "Can't setup package path %r" % package_path
            print 'Pass `-p` or `--help` for more help'
            sys.exit()
        defaults['path'] = package_path

    def set_i18n_path():
        i18n_path = os.path.join(defaults['path'], 'i18n')
        if not os.path.isdir(i18n_path):
            print "Can't setup i18n path %r" % i18n_path
            print "Pass `-i` or `--help` for more help"
        defaults['i18n_path'] = i18n_path

    def get_project_defaults():

        package_path = os.path.join(defaults['basedir'], defaults['project_name'])
        if not os.path.isdir(package_path):
            print 'Pass `-p` or `--help` for more help'
            sys.exit()
        defaults['path'] = package_path

        i18n_path = os.path.join(package_path, 'i18n')
        if not os.path.isdir(i18n_path):
            print "Pass `-i` or `--help` for more help"
        defaults['i18n_path'] = i18n_path
        defaults['potfile'] = defaults['project_name'].lower() + '.pot'
        print defaults


    commandname = args[0]
    # strip command and any global options from the sys.argv
    sys.argv = [sys.argv[0],] + args[1:]
    command = commands[commandname][1]
    command = command.load()

#    get_project_defaults()

    if options.basedir:
        defaults['basedir'] = options.basedir

    get_package_info()
    if not defaults.has_key('name'):
        print "Could not find a setup tools distribution on %r" % \
                options.basedir
        sys.exit()

    if options.package_dir:
        defaults['path'] = options.package_dir
    elif not options.package_dir:
        set_package_path()

    if options.i18n_path:
        defaults['i18n_path'] = options.i18n_path
    elif not options.i18n_path:
        set_i18n_path()

    for key in ('path', 'i18n_path'):
        if not os.path.isdir(defaults[key]):
            print "The path you passed for %r(%r) does not exist" % \
                    (key, defaults[key])
            sys.exit()

    defaults['potfile'] = defaults['name'].lower() + '.pot'
    defaults['potfile_path'] = os.path.join(defaults['i18n_path'], defaults['potfile'])

    command.defaults = defaults
    command = command(I18NToolBox.__version__)
    command.run()


__all__ = ["main"]
