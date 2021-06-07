from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    lst_price = fields.Float("Sales Price", readonly=False, compute=False, inverse=False)
