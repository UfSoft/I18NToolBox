#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: setup.py 71 2007-02-03 20:31:03Z s0undt3ch $ setup.py 19 2007-01-04 00:08:32Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/branches/fresh-start/setup.py $
# $LastChangedDate: 2007-02-03 20:31:03 +0000 (Sat, 03 Feb 2007) $
# $Rev: 71 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from setuptools import setup, find_packages
import i18ntoolbox

setup(
    name    = i18ntoolbox.__package__,
    version = i18ntoolbox.__version__,
    license = i18ntoolbox.__license__,
    author  = i18ntoolbox.__author__,
    author_email = i18ntoolbox.__email__,
    packages = find_packages(),
    test_suite = 'nose.collector',
    install_requires = ['pytz'],
    entry_points = """
    [console_scripts]
    i18n-toolbox = i18ntoolbox.commands:main

    [I18NToolBox.command]
    extract = i18ntoolbox.commands.extract:ExtractionTool

    [I18NToolBox.templating.extract]
    genshi_extract = i18ntoolbox.templating.genshigte:GenshiGettextExtract
    """,
)
