# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools import float_is_zero, ustr
import itertools


class AccountChartOfAccountReport(models.AbstractModel):
    _inherit = "account.coa.report"

    @api.model
    def _get_lines(self, options, line_id=None):
        # Create new options with 'unfold_all' to compute the initial balances.
        # Then, the '_do_query' will compute all sums/unaffected earnings/initial balances for all comparisons.
        """
        This Method Ovverride for Change Structure in Trial Balance Report
        """
        new_options = options.copy()
        new_options['unfold_all'] = True
        options_list = self._get_options_periods_list(new_options)
        accounts_results, taxes_results = self.env['account.general.ledger']._do_query(
            options_list, fetch_lines=False)

        lines = []
        totals = [0.0] * (2 * (len(options_list) + 2))

        # Add lines, one per account.account record.
        list_of_account = [data[0].id for data in accounts_results]
        accounts_list = self.env['account.account'].sudo().search(
            [('id', 'in', list_of_account)], order='parent_id')
        having_parent = False
        for parent_account_recs, chld_accounts_recs in itertools.groupby(accounts_list, lambda g: g['parent_id']):
            if parent_account_recs:
                having_parent = True
            parent_lines = {
                'id': 'grouped_accounts_total',
                'name': _(parent_account_recs.display_name or 'Undefined'),
                'class': 'total',
                'level': 1,
            }
            parent_column = [0.0] * (2 * (len(options_list) + 2))
            child_vals = []
            for child_accounts in chld_accounts_recs:
                final_data = [
                    accounts_data for accounts_data in accounts_results if accounts_data[0].id == child_accounts.id]
                # for accounts_data in accounts_results:
                for account, periods_results in final_data:
                    sums = []
                    account_balance = 0.0
                    for i, period_values in enumerate(reversed(periods_results)):
                        account_sum = period_values.get('sum', {})
                        account_un_earn = period_values.get(
                            'unaffected_earnings', {})
                        account_init_bal = period_values.get(
                            'initial_balance', {})

                        if i == 0:
                            # Append the initial balances.
                            initial_balance = account_init_bal.get(
                                'balance', 0.0) + account_un_earn.get('balance', 0.0)
                            sums += [
                                initial_balance > 0 and initial_balance or 0.0,
                                initial_balance < 0 and -initial_balance or 0.0,
                            ]
                            account_balance += initial_balance

                        # Append the debit/credit columns.
                        sums += [
                            account_sum.get('debit', 0.0) -
                            account_init_bal.get('debit', 0.0),
                            account_sum.get('credit', 0.0) -
                            account_init_bal.get('credit', 0.0),
                        ]
                        account_balance += sums[-2] - sums[-1]

                    # Append the totals.
                    sums += [
                        account_balance > 0 and account_balance or 0.0,
                        account_balance < 0 and -account_balance or 0.0,
                    ]

                    # account.account report line.
                    columns = []
                    for i, value in enumerate(sums):
                        # Update totals.
                        totals[i] += value
                        parent_column[i] += value
                        # Create columns.
                        columns.append({'name': self.format_value(
                            value, blank_if_zero=True), 'class': 'number', 'no_format_name': value})

                    name = account.name_get()[0][1]
                    if len(name) > 40 and not self._context.get('print_mode'):
                        name = name[:40]+'...'

                    child_vals.append({
                        'id': account.id,
                        'name': name,
                        'title_hover': name,
                        'columns': columns,
                        'unfoldable': False,
                        'caret_options': 'account.account',
                    })
            parent_lines.update({'columns': [{'name': self.format_value(parent_col), 'class': 'number'} for parent_col in parent_column]})
            if having_parent:
                lines.append(parent_lines)
            lines.extend(child_vals)
        lines.append({
            'id': 'grouped_accounts_total',
            'name': _('Total'),
            'class': 'total',
            'columns': [{'name': self.format_value(total), 'class': 'number'} for total in totals],
            'level': 1,
        })
        return lines
