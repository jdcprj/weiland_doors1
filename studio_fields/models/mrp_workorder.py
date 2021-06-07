from odoo import fields, models


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    task_id = fields.Many2one('project.task', string="Task", related="production_id.task_id")
    stage_id = fields.Many2one('studio_mrp.workorder_stage', string="Stage")
    customer_po = fields.Char(string="Customer PO#", related="production_id.customer_po_1")
    job_name = fields.Char(string="Job Name", related="production_id.job_name")
    sale_order_wo = fields.Char(string="Sales Order #WO")
    related = fields.Char(string="New Related Field", 
    	related="production_id.sale_order_id.order_line.opening_number")
    sale_order_line_id = fields.Many2one('sale.order.line', string="Sales Order Line")
