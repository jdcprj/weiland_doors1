from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    po_memo = fields.Char(string="PO Memo", related="purchase_id.memo")
    bill_date = fields.Datetime(string="BIll Created Date",
        related="purchase_id.invoice_ids.create_date")
    is_bill_box = fields.Boolean(string="Bill Created box")
    sales_tax_city = fields.Char(string="Sales Tax City", related="partner_id.city")
    sales_tax_state = fields.Char(string="Sales Tax State", related="partner_id.state_id.name")
    so_invoice_status = fields.Selection(
    	[('upselling', 'Upselling Opportunity'), ('invoiced', 'Fully Invoiced'),
    	('to invoice', 'To Invoice'), ('no', 'Nothing to Invoice')],
        string="Sales Tax State", related="sale_id.invoice_status")
    job_name = fields.Char(string='Job Name', related='sale_id.job_name')
    customer_reference = fields.Char(string="Customer PO#", related="sale_id.customer_reference")
