from odoo import fields, models


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    stage_id = fields.Many2one('studio_mrp.workorder_stage', string="Stage")
    customer_po = fields.Char(string="Customer PO#", related="production_id.customer_po_1")
    job_name = fields.Char(string="Job Name", related="production_id.job_name")
    sale_order_id = fields.Many2one('sale.order', string="Sales Order #WO", related="production_id.sale_order_id")
    sale_order_line_id = fields.Many2one('sale.order.line', string="Sales Order #WO", related="production_id.so_line_id")
    opening_number = fields.Char(string="Opening Number", related="production_id.mo_so_opening")
