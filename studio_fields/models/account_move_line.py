from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    source_doc_invoice_ref = fields.Char(string="source doc invoice ref",
    	related='move_id.invoice_origin')
    sale_order_reference_id = fields.Many2one('sale.order',
    	string="Sale Order reference")
    invoice_opening_number = fields.Char(string="Invoice opening #")
    job_name = fields.Char(string="job name")
