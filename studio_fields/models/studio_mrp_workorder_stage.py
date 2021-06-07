from odoo import fields, models


class WorkorderStage(models.Model):
    _name = "studio.mrp.workorder.stage"
    _description = "Studio Mrp Workorder Stage"

    name = fields.Char(string="Name")
