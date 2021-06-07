from odoo import fields, models


class ProjectStage(models.Model):
    _name = "studio.project.project.stage"
    _description = "Studio Project Project Stage"

    name = fields.Char(string="Name")
