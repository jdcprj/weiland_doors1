# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    mrp_config_count = fields.Integer(compute='_compute_mrp_config_count')
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Confirmed for Manufacturing'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    def _compute_mrp_config_count(self):
        for so in self:
            if not so.order_line:
                so.mrp_config_count = 0
            else:
                for so_line in so.order_line:
                    config_ids = self.env['mrp.bom.configuration'].search([
                        ('so_line_id', '=', so_line.id),
                        ('order_id', '=', so_line.order_id.id),
                    ])
                so.mrp_config_count = len(config_ids)

    def action_mrp_configuration(self, mrp_configurations=None):
        action = self.env.ref('mrp_configuration.mrp_configuration_action').read()[0]
        bom_config_list = []
        for so_line in self.order_line:
            config_ids = self.env['mrp.bom.configuration'].search([
                ('so_line_id', '=', so_line.id),
                ('order_id', '=', so_line.order_id.id),
            ])
            bom_config_list.append(config_ids.id)
        return {
            'name': "MRP Configuration",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'mrp.bom.configuration',
            'domain': [('id', 'in', bom_config_list)],
            'target': 'current',
        }

    def action_confirm(self):
        for rec in self:
            for so_line in rec.order_line:
                config_ids = self.env['mrp.bom.configuration'].search([
                    ('so_line_id', '=', so_line.id),
                    ('order_id', '=', so_line.order_id.id),
                ])
                for line in config_ids.mapped('bom_product_ids'):
                    if not line.product_variant_id:
                        raise ValidationError(_("Please configure the product variants and it's attribute in Product "
                                                "BOM Costing"))
        return super(SaleOrder, self).action_confirm()

    def fetch_sub_BOM_line(self, bom):
        result = [bom]
        if bom.bom_id:
            for child in bom:
                result.extend(self.fetch_sub_BOM_line(child))
        return result

    def fetch_sub_BOM(self, bom):
        result = [bom]
        if bom.bom_ids:
            for child in bom.bom_ids.mapped('bom_line_ids').mapped('product_tmpl_id'):
                result.extend(self.fetch_sub_BOM(child))
        return result

    def product_bom_costing(self):
        bom_list = []
        bom_config_list = []
        config_ids = self.env['mrp.bom.configuration']
        for so_line in self.order_line:
            config_ids = self.env['mrp.bom.configuration'].search([
                ('so_line_id', '=', so_line.id),
                ('order_id', '=', so_line.order_id.id),
            ])
            bom_config_list.append(config_ids.id)
            bom_id = so_line.product_id.product_tmpl_id.bom_ids
            if not bom_id:
                continue
            bom_kit = self.env['mrp.bom']._bom_find(product=so_line.product_id, bom_type='normal')
            bom_sub_lines = bom_kit.get_mrp_bom_line(so_line.product_id, 1)
            bom_sub_lines.insert(0, bom_kit)
            bom_line_vals = {}
            config_line = {
                'name': so_line.name,
                'so_line_id': so_line.id,
                'order_id': so_line.order_id.id,
                'partner_id': so_line.order_id.partner_id.id,
                'bom_product_ids': None
            }
            if not config_ids:
                bom_config_ids = self.env['mrp.bom.configuration'].create(config_line)
                bom_list.append(bom_config_ids.id)
                bom_line_list = []
                for bom_id in so_line.product_id.bom_ids:
                    bom_line_list.extend(self.fetch_sub_BOM(bom_id.product_tmpl_id))
                bom_line = self.env['mrp.bom.line']
                for product in bom_line_list:
                    a = bom_line.search([]).filtered(lambda x: x.product_tmpl_id.id == product.id)
                    bom_line += a
                bom_remove_list_recs = self.env['product.template']
                for bom in bom_sub_lines:
                    for line in bom.bom_line_ids:
                        bom_line_vals = {}
                        parent_line = self.env['mrp.bom.configuration.line'].search([
                            ('product_tmpl_id', '=', line.bom_id.product_tmpl_id.id),
                            ('mrp_config_id', '=', bom_config_ids.id)])
                        old_recs = self.env['mrp.bom.configuration.line'].search([
                            ('parent_id', '=', line.bom_id.product_tmpl_id.id),
                            ('mrp_config_id', '=', bom_config_ids.id),
                            ('product_tmpl_id', '=', line.product_tmpl_id.id)])
                        if line.product_qty > 0 and line.bom_id.product_tmpl_id not in bom_remove_list_recs \
                                and not old_recs:
                            if not line.bom_product_template_attribute_value_ids:
                                bom_line_vals = {
                                    'product_tmpl_id': line.product_tmpl_id.id,
                                    'qty': line.product_qty,
                                    'mrp_config_id': bom_config_ids.id,
                                    'is_from_bom': True,
                                    'parent_id': line.bom_id.product_tmpl_id.id,
                                    'parent_line_id': parent_line and parent_line.id
                                }
                            else:
                                if not line._skip_bom_line(bom_config_ids.so_line_id.product_id):
                                    bom_line_vals = {
                                        'product_tmpl_id': line.product_tmpl_id.id,
                                        'qty': line.product_qty,
                                        'mrp_config_id': bom_config_ids.id,
                                        'is_from_bom': True,
                                        'parent_id': line.bom_id.product_tmpl_id.id,
                                        'parent_line_id': parent_line and parent_line.id
                                    }
                            bom_config_line_ids = self.env['mrp.bom.configuration.line'].create(bom_line_vals)
                            bom_config_line_ids._onchange_product_id()
                            bom_config_line_ids._onchange_product_variant_id()
                            # bom_config_line_ids._set_parent_sale_cost_price()
                        else:
                            bom_remove_list_recs |= line.product_tmpl_id

        if config_ids:
            return {
                'name': "MRP Configuration",
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'mrp.bom.configuration',
                'domain': [('id', 'in', bom_config_list)],
                'target': 'current',
            }
        else:
            return {
                'name': "MRP Configuration",
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'mrp.bom.configuration',
                'domain': [('id', 'in', bom_list)],
                'target': 'current',
            }

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        res = super(SaleOrder, self).copy(default=default)
        for line in self.order_line:
            mrp_config = self.env['mrp.bom.configuration'].search([('so_line_id', '=', line.id)])
            if mrp_config:
                new_rec = mrp_config.copy()
                so_line = res.order_line.filtered(lambda r: r.product_id == new_rec.so_line_id.product_id)
                new_rec.write({'so_line_id': so_line.id, 'order_id': res.id})
                self.env.cr.commit()
                # For set attribute values---->
                for bom_line in mrp_config.bom_product_ids:
                    new_bom_line = bom_line.with_context({'copy':1}).copy()
                    new_bom_line.write({'mrp_config_id': new_rec.id})
        return res

    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        po = self.env['purchase.order'].search([('origin', '=', self.name),
                                                ('state', 'not in', ('purchase', 'done'))])
        po.button_cancel()
        for line in self.order_line:
            mo = self.env['mrp.production'].search([('so_line_id', '=', line.id),
                                                    ('state', '=', 'draft')])
            mo.action_cancel()
        return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    margin_type = fields.Selection([
        ('percentage', 'Percentage(%)'),
        ('fixed_amount', 'Fixed Amount'),
    ], string='Margin', default='percentage')
    percentage = fields.Float(
        default=0.0, copy=False)
    fixed_amount = fields.Float(
        default=0.0, copy=False)
    update_cost = fields.Boolean(
        compute="_compute_update_cost")
    drawing = fields.Binary("Drawing")
    drawing_name = fields.Char("Drawing Filename")

    @api.onchange('product_id')
    def product_id_change(self):
        for rec in self:
            desc = ""
            bom_config = self.env['mrp.bom.configuration'].search([('so_line_id', '=', rec.id),
                                                                   ('order_id', '=', rec.order_id.id)])
            for config_rec in bom_config:
                for product in config_rec.bom_product_ids.filtered(
                        lambda l: l.parent_id == config_rec.so_line_id.product_id.product_tmpl_id):
                    desc += "\n" + str(product.product_tmpl_id.name) + "-->"
                    for line in product.product_attribute_line_ids:
                        if line.value_id:
                            desc += str(line.attribute_id.name) + ":" + str(line.value_id.name) + ","
            if desc:
                rec.name = desc.lstrip()
            else:
                super(SaleOrderLine, self).product_id_change()

    def _compute_update_cost(self):
        for rec in self:
            rec.update_cost = True

    def calculate_prices(self, key=None):
        purchase_price = self.purchase_price
        mrp_config_line = self.env['mrp.bom.configuration'].search([
            ('so_line_id', '=', self.id)
        ])
        if key == 'percentage':
            price_unit = purchase_price + (
                    (purchase_price * self.percentage) / 100)
        elif key == 'fixed_amount':
            price_unit = purchase_price + self.fixed_amount
        elif key == 'margin_type':
            price_unit = self.price_unit
        else:
            price_unit = mrp_config_line.total_sale
        if price_unit and purchase_price:
            diff = price_unit - purchase_price
            self.price_unit = price_unit
            self.purchase_price = purchase_price
            self.percentage = (diff / purchase_price) * 100
            self.fixed_amount = diff

    @api.onchange('fixed_amount')
    def onchange_margin_fixed_amount(self):
        self.calculate_prices(key='fixed_amount')

    @api.onchange('percentage')
    def onchange_margin_percentage(self):
        self.calculate_prices(key='percentage')

    @api.onchange('margin_type')
    def onchange_margin_type(self):
        self.calculate_prices(key='margin_type')

    @api.onchange('price_unit')
    def onchange_price_unit(self):
        self.calculate_prices(key='margin_type')

    @api.onchange('product_uom_qty')
    def onchange_product_uom_qty(self):
        self.calculate_prices()

    @api.onchange('product_id', 'product_uom')
    def product_id_change_margin(self):
        return {}
