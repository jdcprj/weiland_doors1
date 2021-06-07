from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    new_related_field_1 = fields.Char(string="New Related Field", 
        related="partner_id.city")
    new_related_field_2 = fields.Char(string="New Related Field", 
        related="payment_transaction_id.sale_order_ids.partner_shipping_id.city")
    new_related_field_3 = fields.Char(string="New Related Field", 
        related="payment_transaction_id.sale_order_ids.partner_shipping_id.city")
    new_related_field_4 = fields.Char(string="New Related Field", 
        related="partner_id.sale_order_ids.partner_shipping_id.city")
    new_related_field_5 = fields.Char(string="New Related Field", 
        related="payment_method_id.name")
    new_related_field_6 = fields.Char(string="New Related Field", 
        related="payment_method_id.display_name")
    new_related_field_7 = fields.Selection(
        [('inbound', 'Inbound'), ('outbound', 'Outbound')], 
        string="New Related Field", related="payment_method_id.payment_type")
    move_id_2 = fields.Many2one(
        'account.move', string="Payment Method")
