# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class MrpConfigurationLine(models.Model):
    _name = "mrp.bom.configuration.line"
    _description = 'MRP BOM Configuration Lines'

    mrp_config_id = fields.Many2one(
        'mrp.bom.configuration',
        string="MRP Configuration")
    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Product template')
    qty = fields.Float('Bom Qty')
    total_qty = fields.Float(
        compute='_compute_total_all',
        string='Total Qty')
    total_sales = fields.Float(
        compute='_compute_total_all',
        string='Total Sales')
    total_costs = fields.Float(
        compute='_compute_total_all',
        string='Total Costs')
    sale_price = fields.Float('Sale Price')
    cost_price = fields.Float('Cost Price')
    product_variant_id = fields.Many2one(
        'product.product',
        compute='_set_product_variant',
        string='Product')
    parent_id = fields.Many2one(
        'product.template',
        string='Parent')
    one_parent_id = fields.Many2one(
        'product.template',
        compute='_display_parent_parent_id',
        string='Related Parent')
    product_attribute_line_ids = fields.One2many(
        'product.tmpl.attribute.line',
        'mrp_config_lined_id',
        string='Lines', copy=True)
    is_from_bom = fields.Boolean("Is From BOM?")
    parent_line_id = fields.Many2one("mrp.bom.configuration.line")
    child_ids = fields.One2many('mrp.bom.configuration.line', 'parent_line_id', string="Sub BOM Lines")

    def _display_parent_parent_id(self):
        for parent in self:
            parent.one_parent_id = parent.parent_id.id

    @api.depends(
        'qty',
        'total_qty',
        'mrp_config_id.so_line_id.product_uom_qty',
        'sale_price',
        'cost_price'
    )
    def _compute_total_all(self):
        print(">>>>>>>>>>>>>>>")
        for total in self:
            total.total_sales = total.total_costs = 0.0
            total.total_qty = total.qty * total.mrp_config_id.so_line_id.product_uom_qty

            a = self.env['mrp.bom.line'].search([
                ('bom_id.product_tmpl_id', '=', total.mrp_config_id.product_id.product_tmpl_id.id)]).product_tmpl_id.ids
            print(":::::::::total.product_tmpl_id::::::::::::",total.product_tmpl_id)
            print(":::::::::total.product_tmpl_id::22::::::::::",a)
            print(":::::::::total.product_tmpl_id.additional_ok::::::::::",total.product_tmpl_id.additional_ok)
            print("::::total.is_from_bom::::", total.is_from_bom)

            if total.product_tmpl_id.id in self.env['mrp.bom.line'].search([
                ('bom_id.product_tmpl_id', '=', total.mrp_config_id.product_id.product_tmpl_id.id)]).product_tmpl_id.ids \
                    or (total.product_tmpl_id.additional_ok and not total.is_from_bom):
                total.total_sales = total.total_qty * total.sale_price
                total.total_costs = total.total_qty * total.cost_price
               

    @api.depends('product_attribute_line_ids', 'product_attribute_line_ids.value_id')
    def _set_product_variant(self):
        for line in self:
            product = self.env['product.product']
            value_list = [atr.value_id.id for atr in line.product_attribute_line_ids]
            for variants in line.product_tmpl_id.product_variant_ids:
                attributes_values_list = [
                    attr.product_attribute_value_id.id
                    for attr in variants.product_template_attribute_value_ids
                ]
                if attributes_values_list == value_list:
                    product = variants.id
            line.update({
                'product_variant_id': product
            })
            # line._set_parent_sale_cost_price()

    @api.onchange('qty', 'product_variant_id')
    def _onchange_product_qty(self):
        if self.product_variant_id and self.qty:
            self.sale_price = self.qty * self.product_variant_id.lst_price

    # @api.depends('qty', 'product_variant_id', 'sale_price', 'cost_price', 'child_ids')
    # def _set_parent_sale_cost_price(self):
    #     for rec in self:
    #         sale_price = cost_price = 0.0
    #         if rec.child_ids:
    #             for line in rec.child_ids:
    #                 sale_price += line.sale_price * line.qty
    #                 cost_price += line.cost_price * line.qty
    #
    #             rec.sale_price = sale_price
    #             rec.cost_price = cost_price

    @api.onchange('product_variant_id')
    def _onchange_product_variant_id(self):
        # if self.product_variant_id.bom_ids:
        #     self.sale_price = 0
        #     self.cost_price = 0
        # else:
        self.sale_price = self.product_variant_id.lst_price
        self.cost_price = self.product_variant_id.standard_price

    def write(self, vals):
        rslt = super(MrpConfigurationLine, self).write(vals)
        if not self._context.get('copy'):
            for line in self:
                if line.product_variant_id.bom_ids:
                    for bom_line in line.product_variant_id.bom_ids.mapped('bom_line_ids'):
                        bom_line_vals = {}
                        if bom_line.product_qty > 0:
                            if not bom_line._skip_bom_line(line.product_variant_id):
                                bom_line_vals = {
                                    'product_tmpl_id': bom_line.product_tmpl_id.id,
                                    'qty': bom_line.product_qty,
                                    'mrp_config_id': line.mrp_config_id.id,
                                    'is_from_bom': True,
                                    'parent_id': line.product_tmpl_id.id,
                                    'parent_line_id': line.id,
                                }
                            elif not bom_line.bom_product_template_attribute_value_ids:
                                bom_line_vals = {
                                    'product_tmpl_id': bom_line.product_tmpl_id.id,
                                    'qty': bom_line.product_qty,
                                    'mrp_config_id': line.mrp_config_id.id,
                                    'is_from_bom': True,
                                    'parent_id': line.product_tmpl_id.id,
                                    'parent_line_id': line.id,
                                }
                        old_recs = self.env['mrp.bom.configuration.line'].search([
                            ('parent_id', '=', line.product_tmpl_id.id),
                            ('mrp_config_id', '=', self.mrp_config_id.id),
                            ('product_tmpl_id', '=', bom_line.product_tmpl_id.id)])
                        # for r_line in old_recs:
                        #     r_line.mrp_config_id.write({'bom_product_ids': [(2, r_line.id)]})
                        if not old_recs:
                            bom_config_line_ids = self.env['mrp.bom.configuration.line'].create(bom_line_vals)
                            bom_config_line_ids._onchange_product_id()
                            bom_config_line_ids._onchange_product_variant_id()
                            # bom_config_line_ids._set_parent_sale_cost_price()
        return rslt

    def update_att_value(self, attribute_ids):
        if attribute_ids:
            list_attribute = []
            for variants in self.mrp_config_id.so_line_id.product_id:
                for attr in variants.product_template_attribute_value_ids:
                    if attr.attribute_id == attribute_ids.attribute_id:
                        attribute_ids.update({
                            'value_id': attr.product_attribute_value_id.id,
                        })
                        list_attribute.append(attribute_ids.id)
                    self.with_context({'copy': 1}).product_attribute_line_ids = [(6, 0, list_attribute)]

    @api.onchange('product_tmpl_id')
    def _onchange_product_id(self):
        list_attribute = []
        product_list = []
        if self.product_tmpl_id:
            new_lines = self.env['product.tmpl.attribute.line']
            for product in self.product_tmpl_id:
                for attribute in product.attribute_line_ids:
                    attribute_vals = {
                        'attribute_id': attribute.attribute_id.id,
                        'product_tmpl_id': product.id,
                        'value_id': False,
                        'mrp_config_lined_id': self.id
                    }
                    attribute_ids = new_lines.create(attribute_vals)
                    self.update_att_value(attribute_ids)
                    list_attribute.append(attribute_ids.id)
                    self.product_attribute_line_ids = [(6, 0, list_attribute)]
                    # for variants in self.mrp_config_id.so_line_id.product_id:
                    #     for attr in variants.product_template_attribute_value_ids:
                    #         if attr.attribute_id == attribute_ids.attribute_id:
                    #             attribute_ids.update({
                    #                 'value_id': attr.product_attribute_value_id.id,
                    #                 })
                    #             list_attribute.append(attribute_ids.id)
                    #         self.product_attribute_line_ids = [(6, 0, list_attribute)]


class product_tmpl_attribute_line(models.Model):
    _name = "product.tmpl.attribute.line"
    _description = 'Product Template Attribute Line'

    @api.onchange('mrp_config_lined_id')
    def _onchange_mrp_config_lined_id(self):
        self.attribute_id = False
        return {'domain': {'attribute_id': [('product_tmpl_ids', '=', self.mrp_config_lined_id.product_tmpl_id.ids)]}}

    product_tmpl_id = fields.Many2one(
        'product.template',
        string="Product Template",
        ondelete='cascade', required=True,
        index=True)
    attribute_id = fields.Many2one(
        'product.attribute',
        string="Attribute",
        required=True, index=True)
    value_id = fields.Many2one(
        'product.attribute.value', string="Values", copy=True)
    # domain="[('attribute_id', '=', attribute_id)]"
    mrp_config_lined_id = fields.Many2one(
        'mrp.bom.configuration.line')
    variant_tmpl_id = fields.Many2one(
        'product.template',
        related='mrp_config_lined_id.product_tmpl_id',
        string="Product Template")


class MrpConfiguration(models.Model):
    _name = 'mrp.bom.configuration'
    _description = 'MRP Configuration'

    name = fields.Char()
    order_id = fields.Many2one('sale.order')
    so_line_id = fields.Many2one('sale.order.line')
    product_id = fields.Many2one(related='so_line_id.product_id', store=True)
    partner_id = fields.Many2one('res.partner')
    bom_product_ids = fields.One2many('mrp.bom.configuration.line',
        'mrp_config_id', string="BOM Products")
    total_sale = fields.Float(compute='_compute_total_sale',
        string='Total Sale')
    total_cost = fields.Float(compute='_compute_total_cost',
        string='Total Cost')

    def name_get(self):
        result = []
        for config in self:
            name = config.name + ' - ' + config.order_id.name
            result.append((config.id, name))
        return result

    # def write(self, vals):
    #     rslt = super(MrpConfiguration, self).write(vals)
    #     for rec in self.bom_product_ids:
    #         if not rec.product_variant_id:
    #             raise ValidationError(_("Please configure the product variants and it's attribute."))
    #     return rslt

    def _compute_total_cost(self):
        for config_lines in self:
            total_cost = 0.0
            for bom_lines in config_lines.bom_product_ids:
                total_cost += bom_lines.total_costs
            config_lines.total_cost = total_cost
            config_lines.so_line_id.purchase_price = total_cost

    def _compute_total_sale(self):
        for config_lines in self:
            total_sale = 0.0
            for bom_lines in config_lines.bom_product_ids:
                total_sale += bom_lines.total_sales
            config_lines.total_sale = total_sale
            config_lines.so_line_id.price_unit = total_sale
