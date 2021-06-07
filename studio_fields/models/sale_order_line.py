from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    part_number = fields.Char(string="Part #", related="product_id.default_code")
    internal_reference = fields.Char(string="Internal Reference", related="product_id.default_code")
    is_parts_order = fields.Boolean(string="Is a Parts Order", related="order_id.is_a_parts_order")
    sales_description = fields.Text(string="Sales Description", related="product_id.description_sale")
    part_number_1 = fields.Char(string="part #", related="product_id.default_code")
    opening_number = fields.Char(string="Opening #")
    notes = fields.Text(string="Notes")
    sale_id = fields.Many2one("sale.order", string="Sale Order")
    total = fields.Monetary(string="Total", related="order_id.amount_total")
    serial_number = fields.Text(string="Serial #")
