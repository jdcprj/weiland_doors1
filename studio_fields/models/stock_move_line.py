from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    initial_demand = fields.Float(string="Initial Demand", related="move_id.product_uom_qty")
    sale_order_id = fields.Many2one('sale.order', string="MO SO Link",
        related="production_id.sale_order_id")
    job_name = fields.Char(string="SO Job Name",related="sale_order_id.job_name")
    forecast_qty = fields.Float(string="Forecast QTY", related="product_id.virtual_available")
    product_type = fields.Selection(
        [('consu', 'Consumable'), ('service', 'Service'),
        ('product', 'Storable Product')], string="Product Type",
        related="product_id.type")
    internal_reference = fields.Char(string="Internal Reference",
        related="product_id.default_code")
    studio_on_hand_qty = fields.Float(string="On hand QTY", related="product_id.qty_available")
    so_customer = fields.Char(string="SO Customer")
    so_line_opening_number = fields.Char(
        string="Product Move SO line Opening #", related="sale_order_id.order_line.opening_number")
    invoice_status = fields.Selection(
        [('upselling', 'Upselling Opportunity'),
        ('invoiced', 'Fully Invoiced'),
        ('to invoice', 'To Invoice'),('no', 'Nothing to Invoice')],
        string="SO Invoice Status", related="sale_order_id.invoice_status")
