from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    source_doc_invoice_ref = fields.Char(string="source doc invoice ref", 
    	related='move_id.invoice_origin')
    invoice_opening_number = fields.Char(string="Invoice opening #")
    sale_order_reference_id = fields.Many2one('sale.order', 
    	string="Sale Order reference")
    job_name = fields.Char(string="job name")
    # invoice_opening_number = fields.Char(string="invoice opening #")
