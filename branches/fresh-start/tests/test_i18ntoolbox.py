# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: test_i18ntoolbox.py 67 2007-01-30 22:55:41Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/branches/fresh-start/tests/test_i18ntoolbox.py $
# $LastChangedDate: 2007-01-30 22:55:41 +0000 (Tue, 30 Jan 2007) $
# $Rev: 67 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import unittest

import i18ntoolbox

class TestI18NToolBox__INIT__(unittest.TestCase):

    def setUp(self):
        self.attrs = (
            '__version__', '__package__', '__license__', '__author__',
            '__email__'
        )

    def test_NeededVars(self):
        "i18ntoolbox.__init__: Make sure the needed variables are set"
        for attr in self.attrs:
            assert hasattr(i18ntoolbox, attr)


    def test_NeededVarsType(self):
        "i18ntoolbox.__init__: Make sure the needed variables are strings"
        for attr in self.attrs:
            assert isinstance(getattr(i18ntoolbox, attr), basestring)


if __name__ == '__main__':
    unittest.main()

