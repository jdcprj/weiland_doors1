# -*- coding: utf-8 -*-


from odoo import fields, models, api
from odoo.osv import expression


class AccountAccount(models.Model):
    _inherit = "account.account"

    parent_id = fields.Many2one('account.account', string="Parent Account")

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name), ('user_type_id.type', 'not in', ['view'])]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        account_ids = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(account_ids).with_user(name_get_uid))

class JournalItems(models.Model):
    _inherit = "account.move.line"

    parent_id = fields.Many2one(related='account_id.parent_id', string="Parent Account")