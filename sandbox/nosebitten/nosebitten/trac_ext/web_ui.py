# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: web_ui.py 75 2007-02-05 23:03:20Z s0undt3ch $
# =============================================================================
#             $URL: http://i18ntoolbox.ufsoft.org/svn/sandbox/nosebitten/nosebitten/trac_ext/web_ui.py $
# $LastChangedDate: 2007-02-05 23:03:20 +0000 (Mon, 05 Feb 2007) $
#             $Rev: 75 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import pkg_resources
#from bitten.trac_ext.web_ui import BittenChrome
#from trac.web.chrome import ITemplateProvider, INavigationContributor
from trac.core import *
from trac.web.chrome import add_script, add_stylesheet, ITemplateProvider
#                            ITemplateProvider, INavigationContributor
#                           ITemplateProvider, IRequestFilter
from trac.web.api import IRequestFilter


#class NoseBittenChrome(BittenChrome):
class NoseBittenChrome(Component):
    #implements(ITemplateProvider, INavigationContributor)
    #implements(ITemplateProvider) #, IRequestFilter)
    implements(ITemplateProvider, IRequestFilter)

    # ITemplateProvider methods

    def get_htdocs_dirs(self):
        return [('nosebitten', pkg_resources.resource_filename(__name__, 'htdocs'))]
        #return []

    def get_templates_dirs(self):
        return [pkg_resources.resource_filename(__name__, 'templates')]


    # INavigationContributor methods

#    def get_active_navigation_item(self, req):
        #add_script(req, '/'.join(['nosebitten', 'jquery-latest.js']))
        #add_script(req, '/'.join(['nosebitten', 'jquery.tablesorter.js']))
        #add_script(req, '/'.join(['nosebitten', 'nosebitten.js']))
        #add_stylesheet(req, 'nosebitten/nosebitten.css')
#        add_script(req, 'nosebitten/jquery-latest.js')
#        add_script(req, 'nosebitten/jquery.tablesorter.js')
#        add_script(req, 'nosebitten/nosebitten.js')
#        return 'build'
        #return BittenChrome.get_active_navigation_item(self, req)

#    def get_navigation_items(self, req):
#        return []

    # IRequestFilter methods
    def pre_process_request(self, req, handler):
        return handler

    def post_process_request(self, req, template, content_type):
        if req.path_info.startswith('/build'):
            add_stylesheet(req, 'nosebitten/nosebitten.css')
            #add_script(req, 'nosebitten/jquery-latest.js')
            #add_script(req, 'nosebitten/jquery.tablesorter.js')
            #add_script(req, 'nosebitten/nosebitten.js')
            add_script(req, 'nosebitten/jquery.hovertip.js')
        return template, content_type
