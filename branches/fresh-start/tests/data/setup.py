#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: setup.py 72 2007-02-05 03:06:20Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/branches/fresh-start/tests/data/setup.py $
# $LastChangedDate: 2007-02-05 03:06:20 +0000 (Mon, 05 Feb 2007) $
# $Rev: 72 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

# THIS IS A BOGUS PROJECT

from setuptools import setup, find_packages

setup(
    name = 'TestProject',
    version = '0.1',
    license = 'BSD',
    author = 'Pedro Algarvio',
    author_email = 'foo@bar.tld',
    packages = find_packages(),
)
