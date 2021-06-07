from odoo import fields, models

class ProjectProject(models.Model):
    _inherit = "project.project"

    sale_id = fields.Many2one('sale.order', string="Sale Order")
    customer_reference = fields.Char(string="Customer Reference", 
    	related="sale_id.client_order_ref")
    opportunity_id = fields.Many2one('crm.lead', string="Opportunity", 
    	related="sale_id.opportunity_id")
    stage_id = fields.Many2one('studio_project.project_stage', string="Stage")
    so_opening_line = fields.Char(string="SO Opening Line", 
    	related="sale_id.order_line.opening_number")
