from odoo import fields, models

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    vendor_mesage = fields.Char(string="Vendor Mesage")
    notes = fields.Char(string="Notes")
    min_qty = fields.Float(string="Min. Qty", related="product_id.reordering_min_qty")
    max_qty = fields.Float(string="Max. Qty", related="product_id.reordering_max_qty")
    order_confirmed = fields.Boolean(string="Order confirmed")
