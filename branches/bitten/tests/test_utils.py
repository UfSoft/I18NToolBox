# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: test_utils.py 53 2007-01-22 21:55:33Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/branches/bitten/tests/test_utils.py $
# $LastChangedDate: 2007-01-22 21:55:33 +0000 (Mon, 22 Jan 2007) $
# $Rev: 53 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import unittest
from i18ntoolbox import utils

class TestAttrsDict(unittest.TestCase):

    def setUp(self):
        self.ad = utils.AttrsDict()

    def test_AddValueByAttribute(self):
        """utils.AttrsDict: Add a value to dict by attribute"""
        self.ad.foo = 'bar'
        assert hasattr(self.ad, 'foo')

    def test_GetValueByAttribute(self):
        """utils.AttrsDict: Get a value from dict by attribute"""
        self.ad.foo = 'bar'
        assert getattr(self.ad, 'foo') == 'bar'

    def test_AddValueByKey(self):
        """utils.AttrsDict: Add a value to dict by key"""
        self.ad['foo'] = 'bar'
        assert self.ad.has_key('foo')

    def test_GetValueByKey(self):
        """utils.AttrsDict: Get a value from dict by key"""
        self.ad['foo'] = 'bar'
        assert self.ad['foo'] == 'bar'

    def test_AttrsDictKeys(self):
        """utils.AttrsDict: Assure we have the 2 keys we've set"""
        self.ad.foo = 'bar'
        self.ad.bar = 'foo'
        assert 'bar' and 'foo' in self.ad.keys()

    def test_AttrsDictValues(self):
        """utils.AttrsDict: Assure we have the 2 values we've set"""
        self.ad.foo = 'bar'
        self.ad.bar = 'foo'
        assert 'bar' and 'foo' in self.ad.values()


if __name__ == '__main__':
    unittest.main()
