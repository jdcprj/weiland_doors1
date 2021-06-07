from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_a_parts_order = fields.Boolean(string="Is A Parts Order")
    customer_reference = fields.Char(string="Customer PO#")
    expected_ship_date = fields.Date(string="Expected Ship Date")
    job_name = fields.Char(string="Job Name")
    awaiting_approval = fields.Boolean(string="Awaiting Approval", default=False)
    is_approved = fields.Boolean(string="Approved")
    mrp_count = fields.Integer(string="Manufacturing")
    target_completion_date = fields.Datetime(
        string="Our Target Completion Date")
    initial_shop_drawings_complete = fields.Date(
        string="Initial Shop Drawings Complete")
    final_shops_approved = fields.Date(string="Final Shops Approved")
    total_due = fields.Monetary(string="Total Due", related="partner_id.total_due")
    total_overdue = fields.Monetary(string="Total Overdue", related="partner_id.total_overdue")
    initial_shops_sent = fields.Boolean(string="Initial Shops Sent")
    if_needed_revised_shops_sent = fields.Boolean(
        string="If needed, revised shops sent")
    lead_time = fields.Char(string="Lead time")
    early_invoice = fields.Boolean(string="Early Invoice Done")
    is_early_ship = fields.Boolean(string="EARLY SHIP is OK")
    # move_id = fields.Many2one(
    #     'account.move', string="Left to invoice")
    # invoice_monetary = fields.Monetary(
    #     string="Left to Invoice", related="move_id.amount_residual")
    on_site_date = fields.Datetime(string="On site Date")
    # project_name = fields.Char(
    #     string="Project Name", related="opportunity_id.display_name")
    crm_id = fields.Many2one('crm.lead', string="Estimator & CSR")
    # account_exec_crm_so = fields.Char(string="Account Exec crm_so")
    account_exec_crm_so = fields.Many2one(
        'hr.employee', string="Account Exec crm_so")
    customer_overdue = fields.Monetary(string="Customer Overdue")
    customer_overdue_1 = fields.Monetary(string="Customer Overdue",
                                         related="partner_id.total_overdue")
    ship_date_1 = fields.Date(string="Ship date 1")
    is_payment_term = fields.Boolean(string="Is Payment Term", default=False)
    freight_company_1 = fields.Char(string="Freight Company 1")
    freight_company_2 = fields.Char(string="Freight Company 2")
    freight_company_3 = fields.Char(string="Freight Company 3")
    freight_company_4 = fields.Char(string="Freight Company 4")
    ship_date_2 = fields.Date(string="Ship Date 2")
    ship_date_3 = fields.Date(string="Ship Date 3")
    ship_date_4 = fields.Date(string="Ship Date 4")
    delivery_method = fields.Selection(
        [("Our_truck", "Our truck"), ("LTL_Truck", "LTL Truck"),
         ("Direct", "Direct"), ("Partial_Direct", "Partial Direct"),
         ("Parcel_Pickup", "Parcel Package"), ("Pickup", "Pickup")],
        string="Delivery Method")
    due_invoice_ids = fields.Many2many('account.move', string='Due Invoices')
    commitment_date = fields.Datetime(
        'Delivery Date', copy=False, help="This is the delivery date promised "
        "to the customer. If set, the delivery order will be scheduled based "
        "on this date rather than product lead times.")

    @api.depends('order_line.invoice_lines')
    def _get_invoiced(self):
        super(SaleOrder, self)._get_invoiced()
        for order in self:
            for inv in order.invoice_ids:
                inv.customer_reference = self.customer_reference
                inv.job_name = self.job_name
                inv.account_exec_crm_so = self.opportunity_id.account_manager_id
                if self.account_exec_crm_so:
                    inv.account_exec_crm_so = self.account_exec_crm_so

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        res = super(SaleOrder, self).onchange_partner_id()
        if self.partner_id.blacklist_contact:
            raise ValidationError(_("The contact is blacklisted."))
        return res

    @api.onchange('opportunity_id')
    def onchange_opportunity_id(self):
        if self.opportunity_id:
            self.account_exec_crm_so = self.opportunity_id.account_exec_crm_so
            self.job_name = self.opportunity_id.display_name

    @api.onchange('is_a_parts_order')
    def check_awaiting_approval(self):
        for record in self:
            record.awaiting_approval = False
            if not record.is_a_parts_order:
                record.awaiting_approval = True

    @api.onchange('payment_term_id')
    def onchange_payment_term(self):
        self.is_payment_term = False
        if self.payment_term_id.name == '30 Days':
            self.is_payment_term = True

    @api.onchange('partner_id')
    def _get_due_invoices(self):
        self.due_invoice_ids = [(6,0,self.partner_id.unreconciled_aml_ids.move_id.ids)]

