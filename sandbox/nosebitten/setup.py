#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: setup.py 75 2007-02-05 23:03:20Z s0undt3ch $
# =============================================================================
#             $URL: http://i18ntoolbox.ufsoft.org/svn/sandbox/nosebitten/setup.py $
# $LastChangedDate: 2007-02-05 23:03:20 +0000 (Mon, 05 Feb 2007) $
#             $Rev: 75 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from setuptools import setup, find_packages

NS = 'http://bitten.cmlenz.net/tools/nb#'

setup(
    name='NoseBitten',
    version='0.1',
    author='Pedro Algarvio',
    author_email = 'ufs@ufsoft.org',
    description = 'Bitten Nose plugin',
    license = 'BSD',
    packages = find_packages(),
    entry_points = {
        'nose.plugins': [
            'bitten#nosetests = nosebitten.plugnose:BittenNosetests',
            'bitten#nosecoverage = nosebitten.plugnose:BittenNoseCoverage'
         ],
        'bitten.recipe_commands': [
            NS + 'unittest = nosebitten.plugbitten:unittest',
            NS + 'coverage = nosebitten.plugbitten:coverage',
            NS + 'lint = nosebitten.plugbitten:nblint'
        ],
        'trac.plugins': [
            'nosebitten.sumarizers = nosebitten.trac_ext.nosesumarizers',
            'nosebitten.web_ui = nosebitten.trac_ext.web_ui'
        ]
    }
)
