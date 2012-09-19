# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: compile.py 15 2007-01-03 20:41:49Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/trunk/I18NToolBox/commands/compile.py $
# $LastChangedDate: 2007-01-03 20:41:49 +0000 (Wed, 03 Jan 2007) $
# $Rev: 15 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import optparse

class CompilationTool:
    desc = "Compile message catalog (.po -> .mo)"
    name = "compile"
    defaults = None
    __version__     = "0.1"
    __author__      = "Pedro ALgarvio"
    __email__       = "ufs@ufsoft.org"
    __copyright__   = "Copyright 2006 Pedro Algarvio"
    __license__     = "BSD"

    def __init__(self, version):
        parser = optparse.OptionParser(
            usage="%prog " + self.name + " [options]", version="%prog " + self.__version__
        )
        parser.description = self.desc
        parser.add_option(
            '-l', '--lang',
            type = "list",
            action = "append",
            dest = "lang",
            help = ""
        )
