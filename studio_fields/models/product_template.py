from odoo import fields, api, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    mark_up_percent = fields.Float(string="Mark-up %")
    mark_up_price = fields.Float(string="Mark-up Price")
    is_inventory= fields.Boolean(string="Is Inventory")
