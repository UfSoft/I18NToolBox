#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: setup.py 19 2007-01-04 00:08:32Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/trunk/setup.py $
# $LastChangedDate: 2007-01-04 00:08:32 +0000 (Thu, 04 Jan 2007) $
# $Rev: 19 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from setuptools import setup, find_packages

import I18NToolBox

setup(
    name = "I18NToolBox",
    version = I18NToolBox.__version__,
    license = "BSD",
    author = "Pedro Algarvio",
    author_email = "ufs@ufsoft.org",
    packages = find_packages(),
    test_suite = 'I18NToolBox.tests.suite',
    entry_points = {
        'console_scripts': [
            'i18n-toolbox = I18NToolBox.commands.base:main',
        ],
        'I18NToolBox.command': [
            'extract = I18NToolBox.commands.extract:ExtractionTool',
            'add = I18NToolBox.commands.add:NewTranslationCatalogTool',
            'compile = I18NToolBox.commands.compile:CompilationTool',
        ],
    },
)
