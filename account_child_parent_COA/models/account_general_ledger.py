# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
import itertools


class AccountGeneralLedgerReport(models.AbstractModel):
    _inherit = "account.general.ledger"

    @api.model
    def _get_parent_total_line(self, options, parent_account, debit, credit, balance, amount_currency):
        return {
            'id': 'general_ledger_total_%s' % self.env.company.id,
            'name': _(parent_account.display_name or 'Undefined'),
            'class': 'total',
            'level': 1,
            'columns': [
                {'name': self.format_value(
                    amount_currency, currency=parent_account.currency_id, blank_if_zero=True), 'class': 'number'},
                {'name': self.format_value(debit), 'class': 'number'},
                {'name': self.format_value(credit), 'class': 'number'},
                {'name': self.format_value(balance), 'class': 'number'},
            ],
            'colspan': 4,
        }

    @api.model
    def _get_general_ledger_lines(self, options, line_id=None):
        ''' Get lines for the whole report or for a specific line.
        :param options: The report options.
        :return:        A list of lines, each one represented by a dictionary.

        Ovveride Methods For add changes in the General Ledger Accounting Report
        '''
        lines = []
        aml_lines = []
        options_list = self._get_options_periods_list(options)
        unfold_all = options.get('unfold_all') or (
            self._context.get('print_mode') and not options['unfolded_lines'])
        date_from = fields.Date.from_string(options['date']['date_from'])
        company_currency = self.env.company.currency_id

        expanded_account = line_id and self.env['account.account'].browse(
            int(line_id[8:]))
        accounts_results, taxes_results = self._do_query(
            options_list, expanded_account=expanded_account)

        total_debit = total_credit = total_balance = 0.0
        list_of_account = [data[0].id for data in accounts_results]
        accounts_list = self.env['account.account'].sudo().search(
            [('id', 'in', list_of_account)], order='parent_id')
        for parent_account_recs, chld_accounts_recs in itertools.groupby(accounts_list, lambda g: g['parent_id']):
            parent_total_debit = parent_total_credit = parent_total_balance = parent_amount_currency = 0.0
            # parent_column = [0.0] * (2 * (len(options_list) + 2))
            total_debit = total_credit = total_balance = 0.0
            child_vals = []
            for child_accounts in chld_accounts_recs:
                final_data = [
                    accounts_data for accounts_data in accounts_results if accounts_data[0].id == child_accounts.id]
                # for accounts_data in accounts_results:
                for account, periods_results in final_data:
                    # No comparison allowed in the General Ledger. Then, take only the first period.
                    results = periods_results[0]
                    is_unfolded = 'account_%s' % account.id in options['unfolded_lines']

                    # account.account record line.
                    account_sum = results.get('sum', {})
                    account_un_earn = results.get('unaffected_earnings', {})

                    # Check if there is sub-lines for the current period.
                    max_date = account_sum.get('max_date')
                    has_lines = max_date and max_date >= date_from or False

                    amount_currency = account_sum.get(
                        'amount_currency', 0.0) + account_un_earn.get('amount_currency', 0.0)
                    debit = account_sum.get(
                        'debit', 0.0) + account_un_earn.get('debit', 0.0)
                    credit = account_sum.get(
                        'credit', 0.0) + account_un_earn.get('credit', 0.0)
                    balance = account_sum.get(
                        'balance', 0.0) + account_un_earn.get('balance', 0.0)

                    child_vals.append(self._get_account_title_line(
                        options, account, amount_currency, debit, credit, balance, has_lines))

                    total_debit += debit
                    total_credit += credit
                    total_balance += balance

                    parent_total_debit += debit
                    parent_total_credit += credit
                    parent_total_balance += balance
                    parent_amount_currency += amount_currency

                    if has_lines and (unfold_all or is_unfolded):
                        # Initial balance line.
                        account_init_bal = results.get('initial_balance', {})

                        cumulated_balance = account_init_bal.get(
                            'balance', 0.0) + account_un_earn.get('balance', 0.0)

                        child_vals.append(self._get_initial_balance_line(
                            options, account,
                            account_init_bal.get(
                                'amount_currency', 0.0) + account_un_earn.get('amount_currency', 0.0),
                            account_init_bal.get(
                                'debit', 0.0) + account_un_earn.get('debit', 0.0),
                            account_init_bal.get(
                                'credit', 0.0) + account_un_earn.get('credit', 0.0),
                            cumulated_balance,
                        ))

                        # account.move.line record lines.
                        amls = results.get('lines', [])

                        load_more_remaining = len(amls)
                        load_more_counter = self._context.get(
                            'print_mode') and load_more_remaining or self.MAX_LINES

                        for aml in amls:
                            # Don't show more line than load_more_counter.
                            if load_more_counter == 0:
                                break

                            cumulated_balance += aml['balance']
                            child_vals.append(self._get_aml_line(
                                options, account, aml, company_currency.round(cumulated_balance)))

                            load_more_remaining -= 1
                            load_more_counter -= 1
                            aml_lines.append(aml['id'])

                        if load_more_remaining > 0:
                            # Load more line.
                            child_vals.append(self._get_load_more_line(
                                options, parent_account_recs or account,
                                self.MAX_LINES,
                                load_more_remaining,
                                cumulated_balance,
                            ))

                        # Account total line.
                        child_vals.append(self._get_account_total_line(
                            options, account,
                            account_sum.get('amount_currency', 0.0),
                            account_sum.get('debit', 0.0),
                            account_sum.get('credit', 0.0),
                            account_sum.get('balance', 0.0),
                        ))
            if not expanded_account:
                lines.append(self._get_parent_total_line(
                    options, parent_account_recs,
                    parent_total_debit or 0.0,
                    parent_total_credit or 0.0,
                    parent_total_balance or 0.0,
                    parent_amount_currency or 0.0,
                ))
            
            if child_vals:
                lines.extend(child_vals)
        if not line_id:
            # Report total line.
            lines.append(self._get_total_line(
                options,
                total_debit,
                total_credit,
                company_currency.round(total_balance),
            ))

            # Tax Declaration lines.
            journal_options = self._get_options_journals(options)
            if len(journal_options) == 1 and journal_options[0]['type'] in ('sale', 'purchase'):
                lines += self._get_tax_declaration_lines(
                    options, journal_options[0]['type'], taxes_results
                )
        if self.env.context.get('aml_only'):
            return aml_lines
        return lines
