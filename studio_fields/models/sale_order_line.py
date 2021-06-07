from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_parts_order = fields.Boolean(string="Is a Parts Order", related="order_id.is_a_parts_order")
    sales_description = fields.Text(string="Sales Description", related="product_id.description_sale")
    opening_number = fields.Char(string="Opening #")
    notes = fields.Text(string="Notes")
    total = fields.Monetary(string="Total", related="order_id.amount_total")
    serial_number = fields.Text(string="Serial #")

    def _prepare_invoice_line(self):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        res.update({
            'invoice_opening_number': self.opening_number
            })
        return res

    def _purchase_get_date_order(self, supplierinfo):
        if self.order_id.on_site_date:
            self.order_id.commitment_date = self.order_id.on_site_date
        return super(SaleOrderLine, self)._purchase_get_date_order(supplierinfo)
