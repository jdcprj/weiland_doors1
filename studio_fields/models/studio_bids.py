from odoo import fields, models

class StudioBids(models.Model):
    _name = "studio.bids"
    _description = "Studio Bids"

    name = fields.Char(string='Name')
    bidder_id = fields.Many2one('res.partner', string="Bidder")
    contact_name = fields.Char(string="Contact Name")
    contact_email = fields.Char(string="Contact Email")
    contact_phone = fields.Char(string="Contact Phone")
    opportunity_id = fields.Many2one('crm.lead', string="Opportunity")
    sale_id = fields.Many2one('sale.order', string="Sale Order")
    chance_to_bid = fields.Boolean(string="Chance to Bid")
    quoted = fields.Boolean(string="Quoted")
    our = fields.Boolean(string="Our $")
    currency_id = fields.Many2one('res.currency', string="Currency")
    bidder_overdue = fields.Monetary(string="Bidder Overdue",
        related="bidder_id.total_overdue", currency_field='currency_id')
