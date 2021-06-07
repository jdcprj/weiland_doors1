# -*- coding: utf-8 -*-

import copy
from odoo import models, _
from odoo.tools import float_is_zero
import itertools


class AccountFinancialReportLine(models.Model):
    _inherit = "account.financial.html.report.line"

    def _get_lines(self, financial_report, currency_table, options, linesDicts):
        """
        Ovveride this Method for Add changes in the Profit & Loss and Balance sheet Accounting Report
        """
        final_result_table = []
        comparison_table = [options.get('date')]
        comparison_table += options.get(
            'comparison') and options['comparison'].get('periods', []) or []
        currency_precision = self.env.company.currency_id.rounding
        # build comparison table
        for line in self:
            res = []
            debit_credit = len(comparison_table) == 1
            domain_ids = {'line'}
            k = 0

            for period in comparison_table:
                date_from = period.get('date_from', False)
                date_to = period.get(
                    'date_to', False) or period.get('date', False)
                date_from, date_to, strict_range = line.with_context(
                    date_from=date_from, date_to=date_to)._compute_date_range()

                r = line.with_context(date_from=date_from,
                                      date_to=date_to,
                                      strict_range=strict_range)._eval_formula(financial_report,
                                                                               debit_credit,
                                                                               currency_table,
                                                                               linesDicts[k],
                                                                               groups=options.get('groups'))
                debit_credit = False
                res.extend(r)
                for column in r:
                    domain_ids.update(column)
                k += 1

            res = line._put_columns_together(res, domain_ids)
            if line.hide_if_zero and all([float_is_zero(k, precision_rounding=currency_precision) for k in res['line']]):
                continue

            # Post-processing ; creating line dictionnary, building comparison, computing total for extended, formatting
            vals = {
                'id': line.id,
                'name': line.name,
                'level': line.level,
                'class': 'o_account_reports_totals_below_sections' if self.env.company.totals_below_sections else '',
                'columns': [{'name': l} for l in res['line']],
                'unfoldable': len(domain_ids) > 1 and line.show_domain != 'always',
                'unfolded': line.id in options.get('unfolded_lines', []) or line.show_domain == 'always',
                'page_break': line.print_on_new_page,
            }
            if financial_report.tax_report and line.domain and not line.action_id:
                vals['caret_options'] = 'tax.report.line'

            if line.action_id:
                vals['action_id'] = line.action_id.id
            domain_ids.remove('line')
            lines = [vals]
            groupby = line.groupby or 'aml'
            if line.id in options.get('unfolded_lines', []) or line.show_domain == 'always':
                if line.groupby:
                    domain_ids = sorted(
                        list(domain_ids), key=lambda k: line._get_gb_name(k))
                if domain_ids:
                    parent_account = self.env['account.account'].browse(
                        domain_ids)
                    for view_account, account in itertools.groupby(parent_account, lambda g: g['parent_id']):
                        if view_account:
                            name = line._get_gb_name(view_account.id)
                            if not self.env.context.get('print_mode') or not self.env.context.get('no_format'):
                                name = name[:40] + \
                                    '...' if name and len(name) >= 45 else name
                            vals = {
                                'id': view_account.id,
                                'name': name,
                                'level': line.level + 1,
                                'class': 'o_account_reports_totals_below_sections' if self.env.company.totals_below_sections else '',
                                'unfoldable': line.id in options.get('unfolded_lines', []) or line.show_domain == 'always',
                                # len(domain_ids) > 1 and line.show_domain != 'always'
                                'unfolded': line.id in options.get('unfolded_lines', []) or line.show_domain == 'always',
                                'page_break': line.print_on_new_page,
                                'parent_id': line.id,
                            }
                            if line.financial_report_id.name == 'Aged Receivable':
                                vals['trust'] = self.env['res.partner'].browse(
                                    [view_account]).trust
                        total_balance = 0.00
                        child_list = []
                        child_columns = []
                        for child_account in account:
                            child_balance = [{'name': l}
                                             for l in res[child_account.id]]
                            if child_columns:
                                for i in range(len(child_balance)):
                                    child_columns[i]['name'] = float(
                                        child_balance[i]['name'] + child_columns[i]['name'])
                            else:
                                child_columns = [{'name': l}
                                                 for l in res[child_account.id]]
                            name = line._get_gb_name(child_account.id)
                            if not self.env.context.get('print_mode') or not self.env.context.get('no_format'):
                                name = name[:40] + \
                                    '...' if name and len(name) >= 45 else name
                            child_vals = {
                                'id': child_account.id,
                                'name': name,
                                'level': line.level + 2,
                                'parent_id': view_account.id or line.id,
                                'columns': child_balance,
                                'caret_options': groupby == 'account_id' and 'account.account' or groupby,
                                'financial_group_line_id': line.id,
                            }
                            if line.financial_report_id.name == 'Aged Receivable':
                                child_vals['trust'] = self.env['res.partner'].browse(
                                    [child_account]).trust
                            child_list.append(child_vals)
                        if view_account:
                            vals.update({'columns': child_columns})
                            lines.append(vals)
                        lines.extend(child_list)

                if domain_ids and self.env.company.totals_below_sections:
                    lines.append({
                        'id': 'total_' + str(line.id),
                        'name': _('Total') + ' ' + line.name,
                        'level': line.level,
                        'class': 'o_account_reports_domain_total',
                        'parent_id': line.id,
                        'columns': copy.deepcopy(lines[0]['columns']),
                    })
            for vals in lines:
                if len(comparison_table) == 2 and not options.get('groups'):
                    vals['columns'].append(line._build_cmp(
                        vals['columns'][0]['name'], vals['columns'][1]['name']))
                    for i in [0, 1]:
                        vals['columns'][i] = line._format(vals['columns'][i])
                else:
                    vals['columns'] = [line._format(
                        v) for v in vals['columns']]
                if not line.formulas:
                    vals['columns'] = [{'name': ''} for k in vals['columns']]

            if len(lines) == 1:
                new_lines = line.children_ids._get_lines(
                    financial_report, currency_table, options, linesDicts)
                if new_lines and line.formulas:
                    if self.env.company.totals_below_sections:
                        divided_lines = self._divide_line(lines[0])
                        result = [divided_lines[0]] + \
                            new_lines + [divided_lines[-1]]
                    else:
                        result = [lines[0]] + new_lines
                else:
                    if not new_lines and not lines[0]['unfoldable'] and line.hide_if_empty:
                        lines = []
                    result = lines + new_lines
            else:
                result = lines
            final_result_table += result

        return final_result_table
