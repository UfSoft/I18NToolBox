# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: test_extract.py 53 2007-01-22 21:55:33Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/branches/bitten/tests/test_extract.py $
# $LastChangedDate: 2007-01-22 21:55:33 +0000 (Mon, 22 Jan 2007) $
# $Rev: 53 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import unittest

from i18ntoolbox.utils import AttrsDict
from i18ntoolbox.commands.extract import ExtractionTool
from helpers import fakeit


class TestExtractionTool(unittest.TestCase):
    "Test the `extract` command"
    def setUp(self):
        #t = ExtractionTool
        defaults = AttrsDict()
        defaults.project = AttrsDict()
        defaults.project.name = 'TestProject'
        defaults.project.potfile = 'testproject.pot'
        defaults.project.basedir = '.'
        defaults.project.path = './testproject'
        defaults.project.i18n_path = './testproject/i18n'
        defaults.project.version = '0.1'
        defaults.project.potfile_path = './testproject/i18n/testproject.pot'
        defaults.parsed_opts = AttrsDict()
        defaults.gettext_opts = []
        t = ExtractionTool
        t.defaults = defaults
        self.t = t()
        self.p = self.t.parser

    def test_HasDefaultDomainOption(self):
        "ExtractionTool: Has '--default-domain' option"
        assert self.p.has_option('--default-domain')

    def test_DefaultDomainType(self):
        "ExtractionTool: The '--default-domain' option value is a string"
        opt = '--default-domain=%s' % self.t.defaults.project.potfile
        (opts, args) = self.t.parser.parse_args([opt])
        assert isinstance(opts.default_domain, basestring)

    def test_SetDefaultDomain(self):
        "ExtractionTool: Set '--default-domain' option"
        opt = '--default-domain=%s' % self.t.defaults.project.potfile
        (opts, args) = self.t.parser.parse_args([opt])
        assert opts.default_domain

    def test_SetDefaultDomainUpdatesGettextOpts(self):
        "ExtractionTool: Set '--default-domain' option updates the gettext opt list"
        opt = '--default-domain=%s' % self.t.defaults.project.potfile
        fakeit(opt, self.t.run)
        assert opt in self.t.defaults.gettext_opts


    def test_HasOutputDirOption(self):
        "ExtractionTool: Has '--output-dir' option"
        assert self.p.has_option('--output-dir')

    def test_OutputDirType(self):
        "ExtractionTool: The '--output-dir' option value is a string"
        opt = '--output-dir=%s' % self.t.defaults.project.i18n_path
        (opts, args) = self.t.parser.parse_args([opt])
        assert isinstance(opts.output_dir, basestring)

    def test_SetOutputDir(self):
        "ExtractionTool: Set '--output-dir' option"
        opt = '--output-dir=%s' % self.t.defaults.project.i18n_path
        (opts, args) = self.t.parser.parse_args([opt])
        assert opts.output_dir

    def test_SetOutputDirUpdatesGettextOpts(self):
        "ExtractionTool: Set '--output-dir' option updates the gettext opt list"
        opt = '--output-dir=%s' % self.t.defaults.project.i18n_path
        fakeit(opt, self.t.run)
        assert opt in self.t.defaults.gettext_opts

    def test_HasJoinExistingOption(self):
        "ExtractionTool: Has '--join-existing' option"
        assert self.p.has_option('--join-existing')

    def test_JoinExistingType(self):
        "ExtractionTool: The '--join-existing' option value is a bolean"
        opt = '--join-existing'
        (opts, args) = self.t.parser.parse_args([opt])
        assert isinstance(opts.join_existing, bool)

    def test_SetJoinExisting(self):
        "ExtractionTool: Set '--join-existing' option"
        opt = '--join-existing'
        (opts, args) = self.t.parser.parse_args([opt])
        assert opts.join_existing

    def test_SetJoinExistingUpdatesGettextOpts(self):
        "ExtractionTool: Set '--join-existing' option updates the gettext opt list"
        opt = '--join-existing'
        fakeit(opt, self.t.run)
        assert opt in self.t.defaults.gettext_opts

    def test_HasExcludeFileOption(self):
        "ExtractionTool: Has '--exclude-file' option"
        assert self.p.has_option('--exclude-file')

    def test_ExcludeFileType(self):
        "ExtractionTool: The '--exclude-file' option value is a string"
        opt = '--exclude-file=%s' % self.t.defaults.project.potfile
        (opts, args) = self.t.parser.parse_args([opt])
        assert isinstance(opts.exclude_file, basestring)

    def test_SetExcludeFile(self):
        "ExtractionTool: Set '--exclude-file' option"
        opt = '--exclude-file=%s' % self.t.defaults.project.potfile
        (opts, args) = self.t.parser.parse_args([opt])
        assert opts.output_dir

    def test_SetExcludeFileUpdatesGettextOpts(self):
        "ExtractionTool: Set '--exclude-file' option updates the gettext opt list"
        opt = '--exclude-file=%s' % self.t.defaults.project.potfile
        fakeit(opt, self.t.run)
        assert opt in self.t.defaults.gettext_opts


if __name__ == '__main__':
    unittest.main()

