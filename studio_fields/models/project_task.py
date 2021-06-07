from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    sale_order_line_id = fields.Many2one('sale.order.line', string="Sales Order Line")
    opening_number = fields.Char(string="Opening #", related="sale_order_line_id.opening_number")
    work_orders_ids = fields.One2many('mrp.workorder', 'task_id', string="Work Orders")
    related = fields.Integer(string="New Related Field", related="project_id.id")
    new_related_field_2 = fields.Integer(string="New Related Field", 
    	related="project_id.sale_id.id")
    new_related_field_3 = fields.Char(string="New Related Field", 
    	related="sale_order_line_id.sale_id.name")
    new_related_field_4 = fields.Char(string="New Related Field", 
    	related="sale_order_line_id.sale_id.customer_reference")
