from odoo import fields, models

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    medical_conditions = fields.Char(string="Medical Conditions")
    prescription_safety_glasses = fields.Boolean(string="Prescription Safety Glasses")
