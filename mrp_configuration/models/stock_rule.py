# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _prepare_mo_vals(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values, bom):
        res = super(StockRule, self)._prepare_mo_vals(product_id, product_qty, product_uom, location_id, name, origin, company_id, values, bom)
        if res['origin'] and res['product_id']:
            order_id = self.env['sale.order'].search([('name', '=', res['origin'])])
            if order_id:
                bom_config_id = self.env['mrp.bom.configuration'].search(
                                        [('order_id', '=', order_id.id),
                                         ('product_id', '=', res['product_id'])])
                if bom_config_id:
                    res.update({'mrp_config_id': bom_config_id.id,
                                'drawing': bom_config_id.so_line_id.drawing,
                                'drawing_name': bom_config_id.so_line_id.drawing_name,
                                'partner_id': order_id.partner_id.id,
                                'partner_shipping_id': order_id.partner_shipping_id.id,
                                'description': bom_config_id.so_line_id.name,})
        return res