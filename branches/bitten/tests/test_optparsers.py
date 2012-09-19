# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: test_optparsers.py 53 2007-01-22 21:55:33Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/branches/bitten/tests/test_optparsers.py $
# $LastChangedDate: 2007-01-22 21:55:33 +0000 (Mon, 22 Jan 2007) $
# $Rev: 53 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import sys
import unittest
from optparse import OptionGroup
from nose.tools import with_setup, raises

from i18ntoolbox.utils import AttrsDict
from i18ntoolbox.commands import CustomOptionParser, BaseGettextTool, \
        CommonOptsGettextTool
from helpers import fakeit

class TestCustomOptionParser(unittest.TestCase):
    def setUp(self):
        self.p = CustomOptionParser()

    def test_SetUpOptionGroup(self):
        """CustomOptionParser: Create option group
        Normal behaviour when creating option groups"""
        assert isinstance(self.p.add_option_group('Test Group'), OptionGroup)

    def test_GetOptionGroup(self):
        """CustomOptionParser: Test overriden get_option_group()"""
        test_group = self.p.add_option_group('Test Group')
        assert self.p.get_option_group('test_group') == test_group

    def test_GetOptionGroupByAttribute(self):
        """CustomOptionParser: Get option group by attribute"""
        test_group = self.p.add_option_group('Test Group')
        assert self.p.test_group == test_group

    def test_AddOptionToOptionGroup(self):
        """CustomOptionParser: Add an option to an option group"""
        test_group = self.p.add_option_group('Test Group')
        test_group.add_option('-f')
        assert self.p.has_option('-f')


class TestBaseGettextTool(unittest.TestCase):
    def setUp(self):
        "Setup BaseGettextTool"
        self.t = BaseGettextTool()

    def test_OutputFileLocationGroup(self):
        "BaseGettextTool: Make sure the 'Output File Location' group exists"
        assert isinstance(
            getattr(self.t.parser, 'output_file_location'), OptionGroup
        )

    def test_HasDestructiveOption(self):
        "BaseGettextTool: Has '--destructive' option"
        assert self.t.parser.has_option('--destructive')


    def test_SetDestructiveOption(self):
        "BaseGettextTool: Set '--destructive' option"
        (opts, args) = self.t.parser.parse_args(args=['--destructive'])
        assert opts.destructive

    def test_DestructiveOptionType(self):
        "BaseGettextTool: The '--destructive' option value is a bolean"
        (opts, args) = self.t.parser.parse_args(args=['--destructive'])
        assert isinstance(opts.destructive, bool)

    def test_HasOutputFileOption(self):
        "BaseGettextTool: Has '--output-file' option"
        assert self.t.parser.has_option('--output-file')

    def test_SetOutputFileOption(self):
        "BaseGettextTool: Set '--output-file' option"
        (opts, args) = self.t.parser.parse_args(args=['--output-file=foo'])
        assert opts.output_file

    def test_OutputFileType(self):
        "BaseGettextTool: The '--output-file' option value is a basestring instance"
        (opts, args) = self.t.parser.parse_args(args=['--output-file=foo'])
        assert isinstance(opts.output_file, basestring)

    def test_OutputFileUpdatesGettextDefaultsDict(self):
        "BaseGettextTool: The '--output-file' option updates the defaults gettext opt list"
        # Build the defaults attrs dict like we di from the cmdline interface
        self.t.defaults = AttrsDict()
        self.t.defaults.parsed_opts = AttrsDict()
        self.t.defaults.gettext_opts = []
        # Store old sys.argv
        old_argv = sys.argv
        # Fake the sys.argv to our needs
        sys.argv = [sys.argv[0], '--output-file=foo']
        #Run the tool
        self.t.run()
        # Make the check this test if for
        assert '--output-file=foo' in self.t.defaults.gettext_opts
        # Restore sys.argv
        sys.argv = old_argv



class TestCommonOptsGettextTool(unittest.TestCase):
    def setUp(self):
        t = CommonOptsGettextTool()
        t.defaults = AttrsDict()
        t.defaults.parsed_opts = AttrsDict()
        t.defaults.gettext_opts = []
        self.p = t.parser
        self.t = t

    def _fakeit(self, new_argv, runfunc):
        if isinstance(new_argv, basestring):
            new_argv = [new_argv]
        # redirect stderr to stdout
        sys.stderr = sys.stdout
        # store old sys.argv
        old_argv = sys.argv
        # Fake our sys.argv
        sys.argv = [sys.argv[0]] + new_argv
        # run the callable
        runfunc()
        # restore sys.argv
        sys.argv = old_argv
        del(old_argv)

    @raises(SystemExit)
    def test_SetEscapeAndNoEscapeOptions(self):
        "CommonOptsGettextTool: Set Both '--escape' and '--no-escape' raises SystemExit"
        fakeit(['--escape', '--no-escape'], self.t.run)

    @raises(SystemExit)
    def test_SetLocationAndNoLocationOptions(self):
        "CommonOptsGettextTool: Set Both '--no-location' and '--add-location' raises SystemExit"
        fakeit(['--no-location', '--add-location'], self.t.run)

    @raises(SystemExit)
    def test_SetSortOutputAndSortByFileOptions(self):
        "CommonOptsGettextTool: Set Both '--sort-output' and '--sort-by-file' raises SystemExit"
        fakeit(['--sort-output', '--sort-by-file'], self.t.run)

    @raises(SystemExit)
    def test_SetWidthAndNoWrap(self):
        "CommonOptsGettextTool: Set Both '--width' and '--no-wrap' raises SystemExit"
        fakeit(['--width=78', '--no-wrap'], self.t.run)

    def test_HasEscapeOption(self):
        "CommonOptsGettextTool: Has '--escape' option"
        assert self.p.has_option('--escape')

    def test_EscapeOptionType(self):
        "CommonOptsGettextTool: The '--escape' option value is a boolean"
        (opts, args) = self.t.parser.parse_args(args=['--escape'])
        assert isinstance(opts.escape, bool)

    def test_SetEscapeOption(self):
        "CommonOptsGettextTool: Set '--escape' option"
        (opts, args) = self.t.parser.parse_args(args=['--escape'])
        assert opts.escape

    def test_SetEscapeUpdatesGetextOpts(self):
        "CommonOptsGettextTool: Set '--escape' option updates the defaults gettext opt list"
        fakeit('--escape', self.t.run)
        assert '--escape' in self.t.defaults.gettext_opts

    def test_HasNoEscapeOption(self):
        "CommonOptsGettextTool: Has '--no-escape' option"
        assert self.p.has_option('--no-escape')

    def test_NoEscapeOptionType(self):
        "CommonOptsGettextTool: The '--no-escape' option value is a boolean"
        (opts, args) = self.t.parser.parse_args(args=['--no-escape'])
        assert isinstance(opts.escape, bool)

    def test_SetNoEscapeOption(self):
        "CommonOptsGettextTool: Set '--no-escape' option"
        (opts, args) = self.t.parser.parse_args(args=['--no-escape'])
        assert not opts.no_escape

    def test_SetNoEscapeUpdatesGetextOpts(self):
        "CommonOptsGettextTool: Set '--no-escape' option updates the defaults gettext opt list"
        fakeit('--no-escape', self.t.run)
        assert '--no-escape' not in self.t.defaults.gettext_opts

    def test_HasIndentOption(self):
        "CommonOptsGettextTool: Has '--indent' option"
        assert self.p.has_option('--indent')

    def test_IndentOptionType(self):
        "CommonOptsGettextTool: The '--indent' option value is a boolean"
        (opts, args) = self.t.parser.parse_args(args=['--indent'])
        assert isinstance(opts.indent, bool)

    def test_SetIndentOption(self):
        "CommonOptsGettextTool: Set '--indent' option"
        (opts, args) = self.t.parser.parse_args(args=['--indent'])
        assert opts.indent

    def test_SetIndentUpdatesGettextOpts(self):
        "CommonOptsGettextTool: Set '--indent' option updates the defaults gettext opt list"
        fakeit('--indent', self.t.run)
        assert '--indent' in self.t.defaults.gettext_opts

    def test_HasNoLocationOption(self):
        "CommonOptsGettextTool: Has '--no-location' option"
        assert self.p.has_option('--no-location')

    def test_NoLocationOptionType(self):
        "CommonOptsGettextTool: The '--no-location' option value is a boolean"
        (opts, args) = self.t.parser.parse_args(args=['--no-location'])
        assert isinstance(opts.no_location, bool)

    def test_SetNoLocationOption(self):
        "CommonOptsGettextTool: Set '--no-location' option"
        (opts, args) = self.t.parser.parse_args(args=['--no-location'])
        assert opts.no_location

    def test_NoLocationUpdatesGettextOpts(self):
        "CommonOptsGettextTool: Set '--no-location' option updates the defaults gettext opt list"
        fakeit('--no-location', self.t.run)
        assert '--no-location' in self.t.defaults.gettext_opts

    def test_HasAddLocationOption(self):
        "CommonOptsGettextTool: Has '--add-location' option"
        assert self.p.has_option('--add-location')

    def test_AddLocationOptionType(self):
        "CommonOptsGettextTool: The '--add-location' option value is a boolean"
        (opts, args) = self.t.parser.parse_args(args=['--add-location'])
        assert isinstance(opts.add_location, bool)

    def test_SetAddLocationOption(self):
        "CommonOptsGettextTool: Set '--add-location' option"
        (opts, args) = self.t.parser.parse_args(args=['--add-location'])
        assert not opts.add_location

    def test_SetAddLocationUpdatesGettextOpts(self):
        "CommonOptsGettextTool: Set '--add-location' option updates the defaults gettext opt list"
        fakeit('--add-location', self.t.run)
        assert '--add-location' not in self.t.defaults.gettext_opts

    def test_HasStrictOption(self):
        "CommonOptsGettextTool: Has '--strict' option"
        assert self.p.has_option('--strict')

    def test_StrictOptionType(self):
        "CommonOptsGettextTool: The '--strict' option value is a boolean"
        (opts, args) = self.t.parser.parse_args(args=['--strict'])
        assert isinstance(opts.strict, bool)

    def test_SetStrictOption(self):
        "CommonOptsGettextTool: Set '--strict' option"
        (opts, args) = self.t.parser.parse_args(args=['--strict'])
        assert opts.strict

    def test_SetStrictUpdatesGettextOpts(self):
        "CommonOptsGettextTool: Set '--strict' option updates the defaults gettext opt list"
        fakeit('--strict', self.t.run)
        assert '--strict' in self.t.defaults.gettext_opts

    def test_HasWidthOption(self):
        "CommonOptsGettextTool: Has '--width' option"
        assert self.p.has_option('--width')

    def test_WidthOptionType(self):
        "CommonOptsGettextTool: The '--width' option value is an integer"
        (opts, args) = self.t.parser.parse_args(args=['--width=76'])
        assert isinstance(opts.strict, int)

    def test_SetWidthOption(self):
        "CommonOptsGettextTool: Set '--width' option"
        (opts, args) = self.t.parser.parse_args(args=['--width=76'])
        assert opts.width

    def test_SetWidthUpdatesGettextOpts(self):
        "CommonOptsGettextTool: Set '--width' option updates the defaults gettext opt list"
        fakeit('--width=76', self.t.run)
        assert '--width=76' in self.t.defaults.gettext_opts

    def test_HasNoWrapOption(self):
        "CommonOptsGettextTool: Has '--no-wrap' option"
        assert self.p.has_option('--no-wrap')

    def test_NoWrapOptionType(self):
        "CommonOptsGettextTool: The '--no-wrap' option value is a boolean"
        (opts, args) = self.t.parser.parse_args(args=['--no-wrap'])
        assert isinstance(opts.no_wrap, bool)

    def test_SetNoWrapOption(self):
        "CommonOptsGettextTool: Set '--no-wrap' option"
        (opts, args) = self.t.parser.parse_args(args=['--no-wrap'])
        assert opts.no_wrap

    def test_SetNoWrapUpdatesGettextOpts(self):
        "CommonOptsGettextTool: Set '--no-wrap' option updates the defaults gettext opt list"
        fakeit('--no-wrap', self.t.run)
        assert '--no-wrap' in self.t.defaults.gettext_opts

    def test_HasSortOutputOption(self):
        "CommonOptsGettextTool: Has '---sort-output' option"
        assert self.p.has_option('--sort-output')

    def test_SortOutputOptionType(self):
        "CommonOptsGettextTool: The '--sort-output' option value is a boolean"
        (opts, args) = self.t.parser.parse_args(args=['--sort-output'])
        assert isinstance(opts.sort_output, bool)

    def test_SetSortOutputOption(self):
        "CommonOptsGettextTool: Set '--sort-output' option"
        (opts, args) = self.t.parser.parse_args(args=['--sort-output'])
        assert opts.sort_output

    def test_SetSortOutputUpdatesGettextOpts(self):
        "CommonOptsGettextTool: Set '--sort-output' option updates the defaults gettext opt list"
        fakeit('--sort-output', self.t.run)
        assert '--sort-output' in self.t.defaults.gettext_opts

    def test_HasSortByFileOption(self):
        "CommonOptsGettextTool: Has '---sort-by-file' option"
        assert self.p.has_option('--sort-by-file')

    def test_SortByFileOptionType(self):
        "CommonOptsGettextTool: The '--sort-by-file' option value is a boolean"
        (opts, args) = self.t.parser.parse_args(args=['--sort-by-file'])
        assert isinstance(opts.sort_by_file, bool)

    def test_SetSortByFileOption(self):
        "CommonOptsGettextTool: Set '--sort-by-file' option"
        (opts, args) = self.t.parser.parse_args(args=['--sort-by-file'])
        assert opts.sort_by_file

    def test_SetSortByFileUpdatesGettextOpts(self):
        "CommonOptsGettextTool: Set '--sort-by-file' option updates the defaults gettext opt list"
        fakeit('--sort-by-file', self.t.run)
        assert '--sort-by-file' in self.t.defaults.gettext_opts

if __name__ == '__main__':
    unittest.main()
