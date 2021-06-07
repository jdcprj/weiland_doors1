# -*- coding: utf-8 -*-


from odoo import fields, models


class AccountAccountType(models.Model):
    _inherit = "account.account.type"

    type = fields.Selection(selection_add=[('view', 'View')])
    internal_group = fields.Selection(selection_add=[('view', 'View')])
