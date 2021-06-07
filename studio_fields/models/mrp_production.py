from odoo import fields, models

class MrpProduction(models.Model):
    _inherit = "mrp.production"

    task_id = fields.Many2one('project.task', string="Task")
    sale_id = fields.Many2one('sale.order', string="Sale Order", related="task_id.sale_order_line_id.order_id")
    sale_order_id = fields.Many2one('sale.order', string="Sale Order", related='mrp_config_id.order_id')
    opening_number = fields.Char(string="Opening2 #", related="task_id.opening_number")
    customer_po_1 = fields.Char(string="Customer PO#", related="sale_order_id.customer_reference")
    job_name = fields.Char(string="Job Name", related="sale_order_id.job_name")
    procurement_group_id = fields.Many2one('procurement.group',string="Sales Order 3")
    procurement_group_mo_id = fields.Many2one('procurement.group',string="Sales Order 3")
    related = fields.Char(string="New Related Field",
        related="sale_order_id.order_line.opening_number")
    mo_so_opening = fields.Char(string="MO_SO opening #", related="sale_order_id.order_line.opening_number")
    new_related_field_2 = fields.Text(string="New Related Field", related="sale_order_id.order_line.name")
    new_related_field_3 = fields.Char(string="New Related Field")
    project_opening_number = fields.Char(string="Project Opening #", related="task_id.opening_number")
    project_opening2 = fields.Many2one('project.project', string="Project opening2")
    task_opening = fields.Char(string="task_opening", related="task_id.opening_number")
    new_related_field_5 = fields.Char(string="New Related Field",
        related="sale_id.order_line.opening_number")
    new_related_field_6 = fields.Char(string="New Related Field",
        related="sale_order_id.order_line.opening_number")
    new_related_field_8 = fields.Char(string="New Related Field",
        related="sale_order_id.order_line.opening_number")
    new_related_field_9 = fields.Integer(string="New Related Field",
        related="sale_id.order_line.id")
    new_related_field_10 = fields.Char(string="New Related Field",
        related="project_opening2.so_opening_line")
    so_opening_number = fields.Char(string="SO Opening #",
        related="sale_order_id.order_line.opening_number")
    sales_order_line_id = fields.Many2one('sale.order.line', string="Sales Order Line ID")
    sale_ordertest = fields.Many2one('sale.order', string="Sale Ordertest")
    sales_order_line_test = fields.Many2one('sale.order.line', string="Sales Order Line test")
    account_exec_crm_so = fields.Many2one(
        'hr.employee', string="Account Exec crm_so", related='sale_order_id.account_exec_crm_so')