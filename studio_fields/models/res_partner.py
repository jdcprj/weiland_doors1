# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_customer = fields.Boolean(string="Is a customer", default=True)
    is_supplier = fields.Boolean(string="Is a supplier")
    customer_type = fields.Selection([("design_build","Design/Build"),
        ("panel_contractor","Panel Contractor"),
        ("general_contractor","General Contractor"),
        ("distributors","Distributors"),
        ("architect","Architect"),("end_user","End User")], string="Customer Type")
    customer_industry = fields.Selection([("architect","Architect"),
        ("project_manager","Project Manager"),
        ("superintendent","Superintendent"),("purchasing","Purchasing/AP"),
        ("sanitation_expert","Sanitation Expert"),
        ("maintenance_supervisor","Maintenance Supervisor"),
        ("plant_manager_engineer","Plant Manager/Engineer"),
        ("shipping_receiving_contact","Shipping/Receiving Contact"),
        ("owner_vip","Owner or VIP")], string="Contact Type")
    top_10 = fields.Boolean(string="Top 10")
    top_25 = fields.Boolean(string="Top 25")
    gets_a_1099 = fields.Boolean(string="Gets a 1099")
    vendor_contact_type = fields.Selection([
        ("accounts_receivable_payable","Accounts Receivable/Payable"),
        ("sales","Sales"),("estimating","Estimating"),("drafting","Drafting"),
        ("plant_manager","Plant Manager"),("sales_exec","Sales Exec"),
        ("shipping_receiving","Shipping/Receiving"),
        ("president_ceo","President/CEO")], string="Vendor Contact Type")
    fax_number = fields.Char(string="Fax #")
    opportunity_won = fields.Boolean(string="Opportunity Won")
    partner_tags = fields.Many2many('res.partner.category', 'res_partner_id', string='Partner Tags')
    total_receivable = fields.Monetary('Total Receivable', compute='_compute_total_receivables')
    currency_id = fields.Many2one('res.currency', string='Currency ID')
    account_number = fields.Char(string="Account #")
    linkedin = fields.Char(string="LinkedIn")
    employee_id = fields.Many2one('hr.employee', string="Account Exec")
    blacklist_contact = fields.Boolean('Blacklist Contact', default=False)

    def _compute_total_receivables(self):
        self.total_receivable = 0.0
        receivable = 0.0
        sale_ids_with_invoice = self.env['sale.order'].search([
            ('partner_id', '=', self.id),
            ('state', '=', 'sale'), ('invoice_ids', '!=', False)])
        amount_residual = sum(sale_ids_with_invoice.mapped('invoice_ids').mapped('amount_residual'))
        amount_total = sum(self.env['sale.order'].search([
            ('partner_id', '=', self.id),
            ('state', '=', 'sale'), ('invoice_ids', '=', False)]).mapped('amount_total'))

        self.total_receivable = amount_residual + amount_total
