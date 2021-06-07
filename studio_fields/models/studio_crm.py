from odoo import fields, models

class StudioCrm(models.Model):
    _name="studio.crm"
    _description="Studio CRM"

    name = fields.Char(string="Name")
