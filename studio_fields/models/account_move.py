from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    studio_1099 = fields.Boolean(string="1099", related='partner_id.gets_a_1099')
    source_so_commitment_date = fields.Datetime(
        string="Source SO Commitment date")
    city_sales_tax = fields.Char(string="City-Sales Tax", 
        related='partner_shipping_id.city')
    state_sales_tax = fields.Many2one('res.country.state', string="State-Sales Tax", 
        related='partner_shipping_id.state_id')
    bill_analytic_tag_ids = fields.Many2many(
        'account.analytic.tag', string="Analytic Tags")
    payment_id = fields.Many2one('account.payment', string="Payments")
    payment_method = fields.Many2one('account.payment.method', string="account.payment.method")
    payment_transaction_id = fields.Many2one('payment.transaction', string="Payment Transactions")
    job_name = fields.Char(string="Job Name")
    customer_reference = fields.Char(string="Customer PO#")
    account_exec_crm_so = fields.Many2one(
        'hr.employee', string="Account Exec crm_so")
