from odoo import fields, models


class CrmLeadTag(models.Model):
    _inherit = "crm.lead.tag"

    priority = fields.Selection(
        [('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')], string="New Priority")
