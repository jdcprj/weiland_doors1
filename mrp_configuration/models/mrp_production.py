# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    mrp_config_id = fields.Many2one(
        'mrp.bom.configuration',
        string="MRP Configuration")
    so_line_id = fields.Many2one(
        'sale.order.line',
        related='mrp_config_id.so_line_id',
        string="Sale Order Line"
    )
    cost_price = fields.Float(
        related='mrp_config_id.total_cost',
        string="Cost Price"
    )
    sale_price = fields.Float(
        related='mrp_config_id.total_sale',
        string="Sale Price"
    )
    mrp_production_count = fields.Integer(
        compute='_compute_mrp_production_count')
    drawing = fields.Binary("Drawing")
    drawing_name = fields.Char("Drawing Filename")
    partner_id = fields.Many2one("res.partner", "Customer")
    partner_shipping_id = fields.Many2one("res.partner", "Customer Delivery Address")
    description = fields.Text("Product Description")

    def _compute_mrp_production_count(self):
        for prod in self:
            production_ids = self.search([('name', '=', prod.origin)])
            if production_ids:
                prod.mrp_production_count = len(production_ids)
            else:
                prod.mrp_production_count = 0

    def display_parent_mrp_production(self):
        bom_config_list = []
        for prod in self:
            production_ids = self.search([('name', '=', prod.origin)])
            bom_config_list.append(production_ids.id)
        return {
            'name': "MRP Production",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'mrp.production',
            'domain': [('id', 'in', bom_config_list)],
            'target': 'current',
        }

    @api.onchange('product_id')
    def _onchange_products_id(self):
        list_attribute = []
        domain = []
        if self.product_id:
            mrp_config_ids = self.env['mrp.bom.configuration'].search([
                ('name', '=', self.product_id.name)
            ])
            if mrp_config_ids:
                for mrp_conf in mrp_config_ids:
                    list_attribute.append(mrp_conf.id)
                    domain = [('id', 'in', list_attribute)]
            else:
                domain = [('id', 'in', [])]
            return {'domain': {'mrp_config_id': domain}}

    def action_confirm(self):
        self._check_company()
        for production in self:
            if not production.move_raw_ids:
                raise UserError(
                    _("Add some materials to consume before marking this MO as to do."))
            for move_raw in production.move_raw_ids:
                move_raw.write({
                    'unit_factor': move_raw.product_uom_qty / production.product_qty,
                })
            product_origin = production.search([
                ('name', '=', production.origin)])
            if product_origin:
                production.update({
                    'mrp_config_id': product_origin.mrp_config_id.id})
            production._generate_finished_moves()
            production.move_raw_ids._adjust_procure_method()
            (production.move_raw_ids | production.move_finished_ids)._action_confirm()
        return True

    @api.onchange('bom_id', 'product_id', 'product_qty', 'product_uom_id')
    def _onchange_move_raw(self):
        # Clear move raws if we are changing the product. In case of creation (self._origin is empty),
        # we need to avoid keeping incorrect lines, so clearing is necessary too.
        if self.product_id != self._origin.product_id:
            self.move_raw_ids = [(5,)]
        if self.bom_id and self.product_qty > 0:
            # keep manual entries
            list_move_raw = [(4, move.id) for move in self.move_raw_ids.filtered(lambda m: not m.bom_line_id)]
            moves_raw_values = self._get_moves_raw_values()
            move_raw_dict = {move.bom_line_id.id: move for move in self.move_raw_ids.filtered(lambda m: m.bom_line_id)}
            move_raw_dict_tmpl = {move.product_tmpl_id.id: move for move in self.move_raw_ids.filtered(lambda m: m.product_tmpl_id.additional_ok)}
            for move_raw_values in moves_raw_values:
                if move_raw_values['product_tmpl_id'] in move_raw_dict_tmpl:
                    list_move_raw += [(1, move_raw_dict_tmpl[move_raw_values['product_tmpl_id']].id, move_raw_values)]
                elif move_raw_values['bom_line_id'] in move_raw_dict:
                    # update existing entries
                    list_move_raw += [(1, move_raw_dict[move_raw_values['bom_line_id']].id, move_raw_values)]
                else:
                    # add new entries
                    list_move_raw += [(0, 0, move_raw_values)]
            self.move_raw_ids = list_move_raw
        else:
            self.move_raw_ids = [(2, move.id) for move in self.move_raw_ids.filtered(lambda m: m.bom_line_id)]

    @api.onchange('mrp_config_id')
    def onchange_mrp_config_id(self):
        if self.move_raw_ids:
            self.update({'move_raw_ids': [(5, 0, 0)]})
        if self.mrp_config_id and self.product_qty > 0:
            # keep manual entries
            list_move_raw = [(4, move.id) for move in self.move_raw_ids.filtered(lambda m: not m.bom_line_id)]
            moves_raw_values = self._get_moves_raw_values()
            move_raw_dict = {move.bom_line_id.id: move for move in self.move_raw_ids.filtered(lambda m: m.bom_line_id)}
            for move_raw_values in moves_raw_values:
                product_tmpl_id = self.env['product.template'].browse(move_raw_values['product_tmpl_id'])
                if product_tmpl_id.additional_ok:
                    list_move_raw += [(0, 0, move_raw_values)]
                elif move_raw_values['bom_line_id'] in move_raw_dict:
                    # update existing entries
                    list_move_raw += [(1, move_raw_dict[move_raw_values['bom_line_id']].id, move_raw_values)]
                else:
                    # add new entries
                    list_move_raw += [(0, 0, move_raw_values)]
            self.move_raw_ids = list_move_raw
        else:
            self.move_raw_ids = [(2, move.id) for move in self.move_raw_ids.filtered(lambda m: m.bom_line_id)]

    def _get_moves_mrp_config_raw_values(self, moves_raw_values):
        for move_raw_val in moves_raw_values:
            for line in self.mrp_config_id.bom_product_ids:
                if move_raw_val['product_tmpl_id'] == line.product_tmpl_id.id:
                    if not line.product_variant_id:
                        raise UserError(_("Please configure the product variants and it's attribute."))
                    move_raw_val.update({
                        'name': line.product_variant_id.name,
                        'product_id': line.product_variant_id.id,
                        'product_tmpl_id': line.product_variant_id.product_tmpl_id.id,
                        'product_uom_qty': line.total_qty})
        for line in self.mrp_config_id.bom_product_ids:
            if line.product_tmpl_id and line.product_tmpl_id.additional_ok:
                moves_raw_values.append({
                    'name': line.product_variant_id.name,
                    'product_id': line.product_variant_id.id,
                    'product_tmpl_id': line.product_variant_id.product_tmpl_id.id,
                    'product_uom_qty': line.total_qty,
                    'product_uom': line.product_variant_id.product_tmpl_id.uom_id.id,
                    'location_dest_id': self.location_dest_id.id,
                    'location_id': self.location_src_id.id,
                    'reference': self.name,
                    'state': 'draft',
                    'raw_material_production_id': self.id,
                    'warehouse_id': self.location_src_id.get_warehouse().id,
                    'group_id': self.procurement_group_id.id,
                    'propagate_cancel': self.propagate_cancel})
        return moves_raw_values

    def _get_moves_raw_values(self):
        res = super(MrpProduction, self)._get_moves_raw_values()
        # for production in self:
        #     if production and production.mrp_config_id:
                # moves_raw_values = production._get_moves_mrp_config_raw_values(res)
                # return moves_raw_values
        return res

    def _get_move_raw_values(self, bom_line, line_data):
        data = super(MrpProduction, self)._get_move_raw_values(bom_line, line_data)
        config_line = self.mrp_config_id.bom_product_ids.filtered(lambda r: r.product_tmpl_id == bom_line.product_template_id)
        if config_line.product_variant_id:
            data['product_id'] = config_line.product_variant_id.id
        return data
