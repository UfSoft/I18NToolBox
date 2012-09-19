# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: __init__.py 19 2007-01-04 00:08:32Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/trunk/I18NToolBox/lib/tests/__init__.py $
# $LastChangedDate: 2007-01-04 00:08:32 +0000 (Thu, 04 Jan 2007) $
# $Rev: 19 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import unittest

def suite():
    from I18NToolBox.lib.tests import catalog

    suite = unittest.TestSuite()
    suite.addTest(catalog.suite())

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')

