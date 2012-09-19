# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: __init__.py 26 2007-01-07 16:50:51Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/trunk/I18NToolBox/commands/__init__.py $
# $LastChangedDate: 2007-01-07 16:50:51 +0000 (Sun, 07 Jan 2007) $
# $Rev: 26 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import pkg_resources

def check_formencode_support(parser):
    """Helper to check if the user has a recent version of formencode."""
    try:
        import formencode
    except ImportError:
        parser.error(
            "You need to have the FormEncode Package installed to be "
            "able to use FormEncode support"
        )
    try:
        pkg_resources.require('formencode==dev,>=0.6.1dev_r2153')
        return True
    except pkg_resources.VersionConflict, error:
        parser.error(
            "FormEncode support can't be enabled because it's required"
            " that you have %s and you have %s" % (error[1], error[0])
        )
    return False
