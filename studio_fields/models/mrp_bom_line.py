from odoo import fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    product_attribute_ids = fields.Many2many(
        'product.attribute.value', string="Attribute Value")
    bom_reference = fields.Char(string="BoM Reference", related="bom_id.code")
