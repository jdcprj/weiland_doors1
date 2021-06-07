from odoo import fields, models

class MrpRouting(models.Model):
    _inherit = "mrp.routing"

    sequence = fields.Integer(string="Sequence")
