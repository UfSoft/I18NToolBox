# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: __init__.py 70 2007-02-03 15:38:02Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/branches/fresh-start/i18ntoolbox/templating/__init__.py $
# $LastChangedDate: 2007-02-03 15:38:02 +0000 (Sat, 03 Feb 2007) $
# $Rev: 70 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

class TEGettextExtractInterface(object):
    """Templating Engines Gettext Extract interface that needs to be inherited
    by a templating engine to provide the extraction code."""

    # The templating engine name, this MUST be set
    name = None
    # A tuple of file type extensions the engine uses. Please include the dot
    exts = None

    def __init__(self, **options):
        """The setup of the inheriting class. A dictionary with the full parser
        options will be passed and could be retrieved like:

            from i18ntoolbox.utils import get_bool_opt, get_list_opt
            self.options = options
            self.debug = get_bool_opt(options, 'debug', False)
            self.files = get_list_opt(options, 'files', None)
            self.templates_path = options.get('search_path', './')
            self.gettext_funcs = get_list_opt(options, 'gettext_funcs', None)
        """
        pass

    def setup_parser(self, parser):
        """Here you define any needed extra options to include in the tool's
        parser under "Templating Engines Options".
        """
        pass

    def extract_keys(self):
        """Here you define the actual code which returns the following tuple:
            (filename, linenum, [key(s)])

        filename:   the filename were the key was found.
        linenum:    the line number where the key was found.
        key:        the list of key or keys(for example when returning a
                    ngettext key, ie, a plural form gettext call).
                    This should always be a list object, even if with only
                    one entry.
        """
        raise NotImplementedError


