# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: helpers.py 76 2007-04-16 18:56:35Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/branches/fresh-start/tests/helpers.py $
# $LastChangedDate: 2007-04-16 19:56:35 +0100 (Mon, 16 Apr 2007) $
# $Rev: 76 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import os
import sys
from i18ntoolbox.utils import AttrsDict

def fakeit(new_argv, runfunc, proj_dir=None):
    if proj_dir:
        old_dir = os.getcwd()
        os.chdir(proj_dir)

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
    if proj_dir:
        os.chdir(old_dir)


def build_defaults():
    defaults = AttrsDict()
    defaults.project = AttrsDict()
    defaults.project.name = 'TestProject'
    defaults.project.potfile = 'testproject.pot'
    defaults.project.basedir = os.path.join(os.path.dirname(__file__), 'data')
    defaults.project.path = os.path.join(defaults.project.basedir, 'project')
    defaults.project.i18n_path = os.path.join(defaults.project.path, 'i18n')
    defaults.project.version = '0.1'
    defaults.project.potfile_path = os.path.join(
        defaults.project.i18n_path, 'testproject.pot'
    )
    #XXX
    defaults.cfgfile = AttrsDict()
    defaults.parsed_opts = AttrsDict()
    defaults.gettext_opts = []
    defaults.computed = AttrsDict()
    #XXX
    defaults = defaults
    defaults.parsed_opts = AttrsDict()
    defaults.gettext_opts = []
    return defaults
