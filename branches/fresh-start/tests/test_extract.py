# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: test_extract.py 76 2007-04-16 18:56:35Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/branches/fresh-start/tests/test_extract.py $
# $LastChangedDate: 2007-04-16 19:56:35 +0100 (Mon, 16 Apr 2007) $
# $Rev: 76 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import os
import unittest

from i18ntoolbox.commands.extract import ExtractionTool
from helpers import fakeit, build_defaults

class TestExtractionTool(unittest.TestCase):
    "Test the `extract` command"

    def setUp(self):
        t = ExtractionTool
        t.defaults = build_defaults()
        self.t = t()
        self.p = self.t.parser

    def test_HasOutputFileOption(self):
        "ExtractionTool: Has '--output-file' option"
        assert self.p.has_option('--output-file')

    def test_OutputFileOptionType(self):
        "ExtractionTool: The '--output-file' option is a string"
        opt = '-output-file=%s' % self.t.defaults.project.potfile_path
        (opts, args) = self.t.parser.parse_args([opt])
        assert isinstance(opts.output_file, basestring)

    def test_SetOutputFileOption(self):
        "ExtractionTool: Set '--output-file' option"
        opt = '-output-file=%s' % self.t.defaults.project.potfile_path
        (opts, args) = self.t.parser.parse_args([opt])
        assert opts.output_file

    def test_SetOutputFileOptionUpdatesGettextOpts(self):
        "ExtractionTool: Set '--output-file' option updates the gettext opt list"
        opt = '--output-file=%s' % self.t.defaults.project.potfile_path
        gtopt = '--output=%s' % self.t.defaults.project.potfile_path
        fakeit(opt, self.t.run)
        assert gtopt in self.t.defaults.gettext_opts
        assert opt not in self.t.defaults.gettext_opts


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

    def test_OutputDirOptionType(self):
        "ExtractionTool: The '--output-dir' option value is a string"
        opt = '--output-dir=%s' % self.t.defaults.project.i18n_path
        (opts, args) = self.t.parser.parse_args([opt])
        assert isinstance(opts.output_dir, basestring)

    def test_SetOutputDirOption(self):
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

    def test_ExcludeFileOptionType(self):
        "ExtractionTool: The '--exclude-file' option value is a string"
        opt = '--exclude-file=%s' % self.t.defaults.project.potfile
        (opts, args) = self.t.parser.parse_args([opt])
        assert isinstance(opts.exclude_file, basestring)

    def test_SetExcludeFile(self):
        "ExtractionTool: Set '--exclude-file' option"
        opt = '--exclude-file=%s' % self.t.defaults.project.potfile
        (opts, args) = self.t.parser.parse_args([opt])
        assert opts.exclude_file

    def test_SetExcludeFileUpdatesGettextOpts(self):
        "ExtractionTool: Set '--exclude-file' option updates the gettext opt list"
        opt = '--exclude-file=%s' % self.t.defaults.project.potfile_path.replace(
            '.pot', '.exclude.pot'
        )
        fakeit(opt, self.t.run)
        assert opt in self.t.defaults.gettext_opts


    def test_HasAddCommentsOption(self):
        "ExtractionTool: Has '--add-comments' option"
        assert self.p.has_option('--add-comments')

    def test_AddCommentsOptionType(self):
        "ExtractionTool: The '--add-comments' option value is a string"
        opt = '--add-comments=TRANSLATORS'
        (opts, args) = self.t.parser.parse_args([opt])
        assert isinstance(opts.add_comments, basestring)

    def test_SetAddComments(self):
        "ExtractionTool: Set '--add-comments' option"
        opt = '--add-comments=TRANSLATORS'
        (opts, args) = self.t.parser.parse_args([opt])
        assert opts.add_comments

    def test_SetAddCommentsUpdatesGettextOpts(self):
        "ExtractionTool: Set '--add-comments' option updates the gettext opt list"
        opt = '--add-comments=TRANSLATORS'
        fakeit(opt, self.t.run, self.t.defaults.project.path)
        assert opt in self.t.defaults.gettext_opts


    def test_HasKeywordOption(self):
        "ExtractionTool: Has '--keyword' option"
        assert self.p.has_option('--keyword')

    def test_KeywordOptionType(self):
        "ExtractionTool: The '--keyword' option value is a list"
        opt = '--keyword=foobar'
        (opts, args) = self.t.parser.parse_args([opt])
        assert isinstance(opts.keywords, list)

    def test_SetKeyword(self):
        "ExtractionTool: Set extra '--keyword' option"
        opt = '--keyword=foobar'
        (opts, args) = self.t.parser.parse_args([opt])
        assert opts.keywords

    def test_SetKeywordUpdatesGettextOpts(self):
        "ExtractionTool: Set '--keyword' option updates the gettext opt list"
        from i18ntoolbox.commands.extract import DEFAULT_KEYWORDS
        opt = '--keyword=foobar'
        fakeit(opt, self.t.run, self.t.defaults.project.path)
        for kw in list(DEFAULT_KEYWORDS) + ['foobar']:
            assert '--keyword=%s' % kw in self.t.defaults.gettext_opts


    def test_HasDebugOption(self):
        "ExtractionTool: Has '--debug' option"
        assert self.p.has_option('--debug')

    def test_DebugOptionType(self):
        "ExtractionTool: The '--debug' option value is a bolean"
        opt = '--debug'
        (opts, args) = self.t.parser.parse_args([opt])
        assert isinstance(opts.debug, bool)

    def test_SetDebugOption(self):
        "ExtractionTool: Set '--debug' option"
        opt = '--debug'
        (opts, args) = self.t.parser.parse_args([opt])
        assert opts.debug

    def test_SetDebugUpdatesGettextOpts(self):
        "ExtractionTool: Set '--debug' option updates the gettext opt list"
        opt = '--debug'
        fakeit(opt, self.t.run, self.t.defaults.project.path)
        assert opt in self.t.defaults.gettext_opts


    def test_HasCopyrightHolderOption(self):
        "ExtractionTool: Has '--copyright-holder' option"
        assert self.p.has_option('--copyright-holder')

    def test_CopyrightHolderOptionType(self):
        "ExtractionTool: The '--copyright-holder' option value is a string"
        opt = '--copyright-holder=FOOBAR'
        (opts, args) = self.t.parser.parse_args([opt])
        assert isinstance(opts.copyright_holder, basestring)

    def test_SetCopyrightHolderOption(self):
        "ExtractionTool: Set '--copyright-holder' option"
        opt = '--copyright-holder=FOOBAR'
        (opts, args) = self.t.parser.parse_args([opt])
        assert opts.copyright_holder

    def test_SetCopyrightHolderUpdatesGettextOpts(self):
        "ExtractionTool: Set '--copyright-holder' option updates the gettext opt list"
        opt = '--copyright-holder=FOOBAR'
        fakeit(opt, self.t.run, self.t.defaults.project.path)
        assert opt in self.t.defaults.gettext_opts


    def test_HasForeignUserOption(self):
        "ExtractionTool: Has '--foreign-user' option"
        assert self.p.has_option('--foreign-user')

    def test_ForeignUserOptionType(self):
        "ExtractionTool: The '--foreign-user' option value is a bool"
        opt = '--foreign-user'
        (opts, args) = self.t.parser.parse_args([opt])
        assert isinstance(opts.foreign_user, bool)

    def test_SetForeignUserOption(self):
        "ExtractionTool: Set '--foreign-user' option"
        opt = '--foreign-user'
        (opts, args) = self.t.parser.parse_args([opt])
        assert opts.foreign_user

    def test_SetForeignUserUpdatesGettextOpts(self):
        "ExtractionTool: Set '--foreign-user' option updates the gettext opt list"
        opt = '--foreign-user'
        fakeit(opt, self.t.run, self.t.defaults.project.path)
        assert opt in self.t.defaults.gettext_opts


    def test_HasMsgidBugsAddressOption(self):
        "ExtractionTool: Has '--msgid-bugs-address' option"
        assert self.p.has_option('--msgid-bugs-address')

    def test_MsgidBugsAddressOptionType(self):
        "ExtractionTool: The '--msgid-bugs-address' option value is a string"
        opt = '--msgid-bugs-address=FOO@BAR.TLD'
        (opts, args) = self.t.parser.parse_args([opt])
        assert isinstance(opts.msgid_bugs_address, basestring)

    def test_SetMsgidBugsAddressOption(self):
        "ExtractionTool: Set '--msgid-bugs-address' option"
        opt = '--msgid-bugs-address=FOO@BAR.TLD'
        (opts, args) = self.t.parser.parse_args([opt])
        assert opts.msgid_bugs_address

    def test_SetMsgidBugsAddressUpdatesGettextOpts(self):
        "ExtractionTool: Set '--msgid-bugs-address' option updates the gettext opt list"
        opt = '--msgid-bugs-address=FOO@BAR.TLD'
        fakeit(opt, self.t.run, self.t.defaults.project.path)
        assert opt in self.t.defaults.gettext_opts


    def test_HasMsgstrPrefixOption(self):
        "ExtractionTool: Has '--msgstr-prefix' option"
        assert self.p.has_option('--msgstr-prefix')

    def test_MsgstrPrefixOptionType(self):
        "ExtractionTool: The '--msgstr-prefix' option value is a string"
        opt = '--msgstr-prefix=MSGSTR'
        (opts, args) = self.t.parser.parse_args([opt])
        assert isinstance(opts.msgstr_prefix, basestring)

    def test_SetMsgstrPrefixOption(self):
        "ExtractionTool: Set '--msgstr-prefix' option"
        opt = '--msgstr-prefix=MSGSTR'
        (opts, args) = self.t.parser.parse_args([opt])
        assert opts.msgstr_prefix

    def test_SetMsgstrPrefixUpdatesGettextOpts(self):
        "ExtractionTool: Set '--msgstr-prefix' option updates the gettext opt list"
        opt = '--msgstr-prefix=MSGSTR'
        fakeit(opt, self.t.run, self.t.defaults.project.path)
        assert opt in self.t.defaults.gettext_opts


    def test_HasMsgstrSuffixOption(self):
        "ExtractionTool: Has '--msgstr-suffix' option"
        assert self.p.has_option('--msgstr-suffix')

    def test_MsgstrSuffixOptionType(self):
        "ExtractionTool: The '--msgstr-suffix' option value is a string"
        opt = '--msgstr-suffix=MSGSTR'
        (opts, args) = self.t.parser.parse_args([opt])
        assert isinstance(opts.msgstr_suffix, basestring)

    def test_SetMsgstrSuffixOption(self):
        "ExtractionTool: Set '--msgstr-suffix' option"
        opt = '--msgstr-suffix=MSGSTR'
        (opts, args) = self.t.parser.parse_args([opt])
        assert opts.msgstr_suffix

    def test_SetMsgstrSuffixUpdatesGettextOpts(self):
        "ExtractionTool: Set '--msgstr-suffix' option updates the gettext opt list"
        opt = '--msgstr-suffix=MSGSTR'
        fakeit(opt, self.t.run, self.t.defaults.project.path)
        assert opt in self.t.defaults.gettext_opts


    def test_HasTemplatesDirNameOption(self):
        "ExtractionTool: Has '--templates-dir-name' option"
        assert self.p.has_option('--templates-dir-name')

    def test_TemplatesDirNameOptionType(self):
        "ExtractionTool: The '--templates-dir-name' option value is a string"
        opt = '--templates-dir-name=templates'
        (opts, args) = self.t.parser.parse_args([opt])
        assert isinstance(opts.templates_dir_name, basestring)

    def test_SetTemplatesDirNameOption(self):
        "ExtractionTool: Set '--templates-dir-name' option"
        opt = '--templates-dir-name=templates'
        (opts, args) = self.t.parser.parse_args([opt])
        assert opts.templates_dir_name

    def test_SetTemplatesDirNameUpdatesGettextOpts(self):
        "ExtractionTool: The '--templates-dir-name' option updates the parsed_opts dict"
        opt = '--templates-dir-name=templates'
        fakeit(opt, self.t.run, self.t.defaults.project.path)
        assert self.t.defaults.parsed_opts.has_key('templates_dir_name')
        assert self.t.defaults.parsed_opts['templates_dir_name'] == 'templates'


    def test_HasTemplatesExtensionOption(self):
        "ExtractionTool: Has '--templates-extension' option"
        assert self.p.has_option('--templates-extension')

    def test_TemplatesExtensionOptionType(self):
        "ExtractionTool: The '--templates-extension' option value is a list"
        fakeit([], self.t.run, self.t.defaults.project.path)
        print self.t.defaults.parsed_opts
        assert isinstance(self.t.defaults.parsed_opts['templates_extensions'], list)

    def test_SetTemplatesExtensionOption(self):
        "ExtractionTool: Set '--templates-extension' option"
        opt = '--templates-extension=.ghtml'
        (opts, args) = self.t.parser.parse_args([opt])
        print opts.templates_extensions
        assert opts.templates_extensions == ['.ghtml']

    def test_TemplatesExtensionOptionDefaultValues(self):
        "ExtractionTool: Defaults values for '--templates-extension' option are correct"
        fakeit([], self.t.run, self.t.defaults.project.path)
        assert self.t.defaults.parsed_opts['templates_extensions'] == ['.html']


    def test_TemplatingEnginesEnableOption(self):
        "ExtractionTool: Templating Engines have '--<engine>-support' option"
        fakeit([], self.t.run, self.t.defaults.project.path)
        print self.t.templating_engines
        for engine in self.t.templating_engines.keys():
            assert self.p.has_option('--%s-support' % engine.lower())

    def test_SetTemplatingEnginesEnableOption(self):
        "ExtractionTool: Set '--<engine>-support' for each templating engine"
        for engine in self.t.templating_engines.keys():
            opt = '%s_support' % engine.lower()
            fakeit('--'+opt.replace('_', '-'), self.t.run, self.t.defaults.project.path)
            assert self.t.defaults.parsed_opts.has_key(opt)

    def test_TemplatingEnginesEnableOptionType(self):
        "ExtractionTool: Each of the '--<engine>-support' option value is a boolean"
        for engine in self.t.templating_engines.keys():
            opt = '%s_support' % engine.lower()
            fakeit('--'+opt.replace('_', '-'), self.t.run, self.t.defaults.project.path)
            assert isinstance(self.t.defaults.parsed_opts[opt], bool)


    def test_ScanSourceFilesAndHtmlTemplates(self):
        "ExtractionTool: test scan_files() and '.html' templates"
        lstriplen = len(os.path.dirname(self.t.defaults.project.path))+1
        source_files, templates = self.t.scan_files(
            self.t.defaults.project.path,  'html_templates', ('.html',)
        )
        for fname in ('file1.py', 'file2.py'):
            fpath = os.path.join(self.t.defaults.project.path[lstriplen:], fname)
            print 'Python File Path:', fpath
            print 'Source Files List:', source_files
            assert fpath in source_files
        for fname in ('layout.html', 'index.html'):
            tpath = os.path.join(
                self.t.defaults.project.path, 'html_templates', fname
            )
            print 'Template File Path:', tpath
            print 'Templates List:', templates
            assert tpath in templates


    def test_ScanSourceFilesAndXhtmlTemplates(self):
        "ExtractionTool: test scan_files() and '.xhtml' templates"
        source_files, templates = self.t.scan_files(
            self.t.defaults.project.path, 'xhtml_templates', ('.xhtml',)
        )
        lstriplen = len(os.path.dirname(self.t.defaults.project.path))+1
        for fname in ('file1.py', 'file2.py'):
            fpath = os.path.join(self.t.defaults.project.path[lstriplen:], fname)
            print 'Python File Path:', fpath
            print 'Source Files List:', source_files
            assert fpath in source_files
        for fname in ('layout.xhtml', 'index.xhtml'):
            tpath = os.path.join(
                self.t.defaults.project.path,  'xhtml_templates', fname
            )
            print 'Template File Path:', tpath
            print 'Templates List:', templates
            assert tpath in templates





if __name__ == '__main__':
    unittest.main()

