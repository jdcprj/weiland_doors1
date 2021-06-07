from odoo import fields, models

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    medical_conditions = fields.Char(string="Medical Conditions")
    related_user = fields.Char(string="Related User")
    related_user_id = fields.Many2one('res.users', string="Related User", related='user_id')
    prescription_safety_glasses = fields.Boolean(string="Prescription Safety Glasses")
