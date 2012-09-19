# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: helpers.py 53 2007-01-22 21:55:33Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/branches/bitten/tests/helpers.py $
# $LastChangedDate: 2007-01-22 21:55:33 +0000 (Mon, 22 Jan 2007) $
# $Rev: 53 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import sys

def fakeit(new_argv, runfunc):
    if isinstance(new_argv, basestring):
        new_argv = [new_argv]
    # redirect stderr to stdout
    sys.stderr = sys.stdout
    # store old sys.argv
    old_argv = sys.argv
    # Fake our sys.argv
    sys.argv = [sys.argv[0]] + new_argv
    # run the callable
    runfunc()
    # restore sys.argv
    sys.argv = old_argv
    del(old_argv)
