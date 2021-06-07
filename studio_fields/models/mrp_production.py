from odoo import fields, models

class MrpProduction(models.Model):
    _inherit = "mrp.production"

    sale_order_id = fields.Many2one('sale.order', string="Sale Order", related='mrp_config_id.order_id')
    customer_po_1 = fields.Char(string="Customer PO#", related="sale_order_id.customer_reference")
    job_name = fields.Char(string="Job Name", related="sale_order_id.job_name")
    mo_so_opening = fields.Char(string="MO_SO opening #", related="so_line_id.opening_number")
    account_exec_crm_so = fields.Many2one(
        'hr.employee', string="Account Exec crm_so", related='sale_order_id.account_exec_crm_so')