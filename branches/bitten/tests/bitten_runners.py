# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: bitten_runners.py 58 2007-01-23 03:32:23Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/branches/bitten/tests/bitten_runners.py $
# $LastChangedDate: 2007-01-23 03:32:23 +0000 (Tue, 23 Jan 2007) $
# $Rev: 58 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import sys

OLD_SYSARGV = ''

def runnose():
    """Fucntion just to simulate a shell call, to be used when called from
    bitten."""
    import nose
    nose.main(argv=sys.argv)
    sys.argv = OLD_SYSARGV

def runlint():
    from pylint.lint import Run
    sys.stderr = sys.stdout
    if sys.argv[0].startswith('--output'):
        outfname = sys.argv.pop(0).split('=')[1]
        print outfname
        sys.stdout = open(outfname, 'w')
    Run(sys.argv)
    sys.argv = OLD_SYSARGV

if __name__ == '__main__':
    OLD_SYSARGV = sys.argv
    if sys.argv[1] in ('lint', 'pylint'):
        #sys.argv = [sys.argv[0]] + sys.argv[2:]
        sys.argv = sys.argv[2:]
        print sys.argv
        runlint()
    elif sys.argv[1] in ('nose', 'nosetests'):
        #sys.argv = [sys.argv[0]] + sys.argv[2:]
        sys.argv = sys.argv[2:]
        print sys.argv
        runnose()
    else:
        print "First arg must be one of 'lint' or 'pylint' to run pylint," + \
                " and, 'nose', 'nosetests' to run the nose unittests"
        sys.exit(1)
