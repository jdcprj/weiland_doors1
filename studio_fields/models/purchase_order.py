from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    memo = fields.Char(string="Memo")
    job_name_for_vendor = fields.Char(string="Job Name for Vendor")
    analytic_tag_ids = fields.Many2many(
        'account.analytic.tag', 'x_account_analytic_tag_purchase_order_rel', string="Analytic Tags")
