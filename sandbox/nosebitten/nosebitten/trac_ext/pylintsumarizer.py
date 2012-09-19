# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id$
# =============================================================================
#             $URL$
# $LastChangedDate$
#             $Rev$
#   $LastChangedBy$
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from tac.core import *
from trac.web.chrome import Chrome
from trac.web.clearsilver import HDFWrapper
from bitten.trac_ext.api import IReportSummarizer

class PyLintSumaryzer(Component):
    implements(IReportSummarizer)

    def get_supported_categories(self):
        return ['lint', 'pylint']

    def render_summary(self, req, config, build, step, category):
        assert category in ('lint', 'pylint', 'nblint')

        db = self.env.get_db_cnx()
        cursor = db.cursor()
        cursor.execute("""
SELECT MAX(lint_file.value) AS file, MAX(CAST(lint_line.value as INT)) AS line,
       MAX(lint_type.value) AS type, MAX(lint_tag.value) AS tag,
       MAX(lint_msg.value) AS msg, MAX(lint_category.value) as cat
FROM bitten_report AS report
  LEFT OUTER JOIN bitten_report_item AS lint_file
    ON(lint_file.report=report.id AND lint_file.name='file')
  LEFT OUTER JOIN bitten_report_item AS lint_line
    ON(lint_line.report=report.id AND
       lint_line.item=lint_file.item AND lint_line.name='line')
  LEFT OUTER JOIN bitten_report_item AS lint_type
    ON(lint_type.report=report.id AND
       lint_type.item=lint_file.item AND lint_type.name='type')
  LEFT OUTER JOIN bitten_report_item AS lint_tag
    ON(lint_tag.report=report.id AND
       lint_tag.item=lint_file.item AND lint_tag.name='tag')
  LEFT OUTER JOIN bitten_report_item AS lint_msg
    ON(lint_msg.report=report.id AND
       lint_msg.item=lint_file.item AND lint_msg.name='msg')
  LEFT OUTER JOIN bitten_report_item AS lint_category
    ON(lint_category.report=report.id AND
       lint_category.item=lint_file.item AND lint_category.name='category')
WHERE category=%s AND build=%s AND step=%s
GROUP BY lint_file.value, lint_line.value, lint_type.value
ORDER BY file, line, type""", (category, build.id, step.name))

        data = []
        for fname, line, ltype, tag, msg, cat in cursor:
            data.append(
                {
                    'href': self.env.href.browser(config.path, fname)
                    'file': fname,
                    'line': line,
                     'type': ltype,
                     'tag': tag,
                     'msg': msg,
                     'cat': cat
                }
            )
        hdf = HDFWrapper(loadpaths=Chrome(self.env).get_all_templates_dirs())
        hdf['data'] = data
        return hdf.render('nosebitten_pylint_summary.cs')
