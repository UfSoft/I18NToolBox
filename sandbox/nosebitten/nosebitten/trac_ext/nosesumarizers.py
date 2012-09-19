# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: nosesumarizers.py 74 2007-02-05 22:29:00Z s0undt3ch $
# =============================================================================
#             $URL: http://i18ntoolbox.ufsoft.org/svn/sandbox/nosebitten/nosebitten/trac_ext/nosesumarizers.py $
# $LastChangedDate: 2007-02-05 22:29:00 +0000 (Mon, 05 Feb 2007) $
#             $Rev: 74 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from trac.core import *
from trac.web.chrome import Chrome
from trac.web.clearsilver import HDFWrapper
from bitten.trac_ext.api import IReportSummarizer


class NoseTestCoverageSummarizer(Component):
    implements(IReportSummarizer)

    def get_supported_categories(self):
        return ['nosecoverage']

    def render_summary(self, req, config, build, step, category):
        self.log.debug('Category: %s', category)
        assert category == 'nosecoverage'

        db = self.env.get_db_cnx()
        cursor = db.cursor()
        cursor.execute("""
SELECT item_name.value AS unit, item_file.value AS file,
       MAX(item_lines.value) AS loc, MAX(exec_lines.value) AS exec,
       MAX(item_percentage.value) AS cov, MAX(miss_lines.value) AS miss
FROM bitten_report AS report
 LEFT OUTER JOIN bitten_report_item AS item_name
  ON (item_name.report=report.id AND item_name.name='name')
 LEFT OUTER JOIN bitten_report_item AS item_file
  ON (item_file.report=report.id AND item_file.item=item_name.item AND
      item_file.name='file')
 LEFT OUTER JOIN bitten_report_item AS item_lines
  ON (item_lines.report=report.id AND item_lines.item=item_name.item AND
      item_lines.name='lines')
 LEFT OUTER JOIN bitten_report_item AS exec_lines
  ON (exec_lines.report=report.id AND
      exec_lines.item=item_name.item AND
      exec_lines.name='executed')
 LEFT OUTER JOIN bitten_report_item AS item_percentage
  ON (item_percentage.report=report.id AND
      item_percentage.item=item_name.item AND
      item_percentage.name='percentage')
 LEFT OUTER JOIN bitten_report_item AS miss_lines
  ON (miss_lines.report=report.id AND
      miss_lines.item=item_name.item AND
      miss_lines.name='miss')
WHERE category='nosecoverage' AND build=%s AND step=%s
GROUP BY file, unit ORDER BY unit""", (build.id, step.name))

        data = []
        total_loc, total_cov, total_exe = 0, 0, 0
        for unit, file, loc, exe, cov, miss in cursor:
            loc, cov, exe = int(loc), float(cov), int(exe)
            if loc:
                d = {'name': unit, 'loc': loc, 'cov': int(cov), 'exe': exe} #, 'miss': miss}
                if file:
                    d['href'] = self.env.href.browser(config.path, file)
                if miss and file:
                    missed = []
                    #misses = miss.split()
                    for lines in miss.split():
                        m = {'lines': lines}
                        #missed['lines'] = lines
                        m['href'] = self.env.href.browser(config.path, file) +  '#L%s' % \
                                lines.split('-')[0]
                        missed.append(m)
                    d['miss'] = missed
                else:
                    d['miss'] = {'lines': miss}

                self.log.debug('DATA ROW:', d)

                data.append(d)
                total_loc += loc
                total_exe += exe
                total_cov += loc * cov

        hdf = HDFWrapper(loadpaths=Chrome(self.env).get_all_templates_dirs())
        hdf['data'] = data
        hdf['totals'] = {'loc': total_loc, 'cov': int(total_cov / total_loc), 'exe': total_exe}

        return hdf.render('bitten_summary_nosecoverage.cs')


class PyLintSumaryzer(Component):
    implements(IReportSummarizer)

    def get_supported_categories(self):
        return ['lint'] #, 'pylint']

    def render_summary(self, req, config, build, step, category):
        assert category == 'lint'
        #assert category in ('lint', 'pylint', 'nblint')

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
                    'href': self.env.href.browser(config.path, fname),
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

